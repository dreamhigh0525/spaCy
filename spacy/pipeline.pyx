# cython: infer_types=True
# cython: profile=True
# coding: utf8
from __future__ import unicode_literals

from thinc.api import chain, layerize, with_getitem
from thinc.neural import Model, Softmax
import numpy
cimport numpy as np
import cytoolz

from thinc.api import add, layerize, chain, clone, concatenate
from thinc.neural import Model, Maxout, Softmax, Affine
from thinc.neural._classes.hash_embed import HashEmbed
from thinc.neural.util import to_categorical

from thinc.neural._classes.convolution import ExtractWindow
from thinc.neural._classes.resnet import Residual
from thinc.neural._classes.batchnorm import BatchNorm as BN

from .tokens.doc cimport Doc
from .syntax.parser cimport Parser as LinearParser
from .syntax.nn_parser cimport Parser as NeuralParser
from .syntax.parser import get_templates as get_feature_templates
from .syntax.beam_parser cimport BeamParser
from .syntax.ner cimport BiluoPushDown
from .syntax.arc_eager cimport ArcEager
from .tagger import Tagger
from .gold cimport GoldParse

from .attrs import ID, LOWER, PREFIX, SUFFIX, SHAPE, TAG, DEP
from ._ml import Tok2Vec, flatten, get_col, doc2feats


class TokenVectorEncoder(object):
    '''Assign position-sensitive vectors to tokens, using a CNN or RNN.'''
    name = 'tok2vec'

    @classmethod
    def Model(cls, width=128, embed_size=5000, **cfg):
        return Tok2Vec(width, embed_size, preprocess=None)

    def __init__(self, vocab, model=True, **cfg):
        self.vocab = vocab
        self.doc2feats = doc2feats()
        self.model = self.Model() if model is True else model
    
    def __call__(self, docs, state=None):
        if isinstance(docs, Doc):
            docs = [docs]
        tokvecs = self.predict(docs)
        self.set_annotations(docs, tokvecs)
        state = {} if state is not None else state
        state['tokvecs'] = tokvecs
        return state

    def pipe(self, docs, **kwargs):
        raise NotImplementedError
 
    def predict(self, docs):
        cdef Doc doc
        feats = self.doc2feats(docs)
        tokvecs = self.model(feats)
        return tokvecs

    def set_annotations(self, docs, tokvecs):
        start = 0
        for doc in docs:
            doc.tensor = tokvecs[start : start + len(doc)]
            start += len(doc)
   
    def update(self, docs, golds, state=None,
               drop=0., sgd=None):
        if isinstance(docs, Doc):
            docs = [docs]
            golds = [golds]
        state = {} if state is None else state
        feats = self.doc2feats(docs)
        tokvecs, bp_tokvecs = self.model.begin_update(feats, drop=drop)
        state['feats'] = feats
        state['tokvecs'] = tokvecs
        state['bp_tokvecs'] = bp_tokvecs
        return state

    def get_loss(self, docs, golds, scores):
        raise NotImplementedError


class NeuralTagger(object):
    name = 'nn_tagger'
    def __init__(self, vocab):
        self.vocab = vocab
        self.model = Softmax(self.vocab.morphology.n_tags)

    def __call__(self, doc, state=None):
        assert state is not None
        assert 'tokvecs' in state
        tokvecs = state['tokvecs']
        tags = self.predict(tokvecs)
        self.set_annotations([doc], tags)
        return state

    def pipe(self, stream, batch_size=128, n_threads=-1):
        for batch in cytoolz.partition_all(batch_size, batch):
            docs, tokvecs = zip(*batch)
            tag_ids = self.predict(docs, tokvecs)
            self.set_annotations(docs, tag_ids)
            yield from docs

    def predict(self, tokvecs):
        scores = self.model(tokvecs)
        guesses = scores.argmax(axis=1)
        if not isinstance(guesses, numpy.ndarray):
            guesses = guesses.get()
        return guesses

    def set_annotations(self, docs, tag_ids):
        if isinstance(docs, Doc):
            docs = [docs]
        cdef Doc doc
        cdef int idx = 0
        for i, doc in enumerate(docs):
            tag_ids = tag_ids[idx:idx+len(doc)]
            for j, tag_id in enumerate(tag_ids):
                doc.vocab.morphology.assign_tag_id(&doc.c[j], tag_id)
                idx += 1

    def update(self, docs, golds, state=None, drop=0., sgd=None):
        state = {} if state is None else state

        tokvecs = state['tokvecs']
        bp_tokvecs = state['bp_tokvecs']
        if self.model.nI is None:
            self.model.nI = tokvecs.shape[1]
 
        tag_scores, bp_tag_scores = self.model.begin_update(tokvecs, drop=drop)
        loss, d_tag_scores = self.get_loss(docs, golds, tag_scores)
        d_tokvecs = bp_tag_scores(d_tag_scores, sgd)

        state['tag_scores'] = tag_scores
        state['bp_tag_scores'] = bp_tag_scores
        state['d_tag_scores'] = d_tag_scores
        state['tag_loss'] = loss
        
        if 'd_tokvecs' in state:
            state['d_tokvecs'] += d_tokvecs
        else:
            state['d_tokvecs'] = d_tokvecs
        return state

    def get_loss(self, docs, golds, scores):
        tag_index = {tag: i for i, tag in enumerate(docs[0].vocab.morphology.tag_names)}

        idx = 0
        correct = numpy.zeros((scores.shape[0],), dtype='i')
        for gold in golds:
            for tag in gold.tags:
                correct[idx] = tag_index[tag]
                idx += 1
        correct = self.model.ops.xp.array(correct)
        d_scores = scores - to_categorical(correct, nb_classes=scores.shape[1])
        return (d_scores**2).sum(), d_scores


cdef class EntityRecognizer(LinearParser):
    """
    Annotate named entities on Doc objects.
    """
    TransitionSystem = BiluoPushDown

    feature_templates = get_feature_templates('ner')

    def add_label(self, label):
        LinearParser.add_label(self, label)
        if isinstance(label, basestring):
            label = self.vocab.strings[label]


cdef class BeamEntityRecognizer(BeamParser):
    """
    Annotate named entities on Doc objects.
    """
    TransitionSystem = BiluoPushDown

    feature_templates = get_feature_templates('ner')

    def add_label(self, label):
        LinearParser.add_label(self, label)
        if isinstance(label, basestring):
            label = self.vocab.strings[label]


cdef class DependencyParser(LinearParser):
    TransitionSystem = ArcEager
    feature_templates = get_feature_templates('basic')

    def add_label(self, label):
        LinearParser.add_label(self, label)
        if isinstance(label, basestring):
            label = self.vocab.strings[label]


cdef class NeuralDependencyParser(NeuralParser):
    name = 'parser'
    TransitionSystem = ArcEager


cdef class NeuralEntityRecognizer(NeuralParser):
    name = 'entity'
    TransitionSystem = BiluoPushDown


cdef class BeamDependencyParser(BeamParser):
    TransitionSystem = ArcEager

    feature_templates = get_feature_templates('basic')

    def add_label(self, label):
        Parser.add_label(self, label)
        if isinstance(label, basestring):
            label = self.vocab.strings[label]


__all__ = ['Tagger', 'DependencyParser', 'EntityRecognizer', 'BeamDependencyParser',
           'BeamEntityRecognizer', 'TokenVectorEnoder']
