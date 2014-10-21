from os import path
import os
import shutil
import ujson
import random
import codecs


from thinc.weights cimport arg_max
from thinc.features import NonZeroConjFeat
from thinc.features import ConjFeat

from .en import EN
from .lexeme import LexStr_shape, LexStr_suff, LexStr_pre, LexStr_norm
from .lexeme import LexDist_upper, LexDist_title
from .lexeme import LexDist_upper, LexInt_cluster, LexInt_id


NULL_TAG = 0


cdef class Tagger:
    tags = {'NULL': NULL_TAG}
    def __init__(self, model_dir):
        self.mem = Pool()
        self.extractor = Extractor(TEMPLATES, [ConjFeat for _ in TEMPLATES])
        self.model = LinearModel(len(self.tags), self.extractor.n)
        self._atoms = <atom_t*>self.mem.alloc(CONTEXT_SIZE, sizeof(atom_t))
        self._feats = <feat_t*>self.mem.alloc(self.extractor.n+1, sizeof(feat_t))
        self._values = <weight_t*>self.mem.alloc(self.extractor.n+1, sizeof(weight_t))
        self._scores = <weight_t*>self.mem.alloc(len(self.tags), sizeof(weight_t))
        self._guess = NULL_TAG
        if path.exists(path.join(model_dir, 'model.gz')):
            with open(path.join(model_dir, 'model.gz'), 'r') as file_:
                self.model.load(file_)

    cpdef class_t predict(self, int i, Tokens tokens, class_t prev, class_t prev_prev) except 0:
        get_atoms(self._atoms, i, tokens, prev, prev_prev)
        self.extractor.extract(self._feats, self._values, self._atoms, NULL)
        assert self._feats[self.extractor.n] == 0
        self._guess = self.model.score(self._scores, self._feats, self._values)
        return self._guess

    cpdef bint tell_answer(self, class_t gold) except *:
        cdef class_t guess = self._guess
        if gold == guess or gold == NULL_TAG:
            self.model.update({})
            return 0
        counts = {guess: {}, gold: {}}
        self.extractor.count(counts[gold], self._feats, 1)
        self.extractor.count(counts[guess], self._feats, -1)
        self.model.update(counts)

    @classmethod
    def encode_pos(cls, tag):
        if tag not in cls.tags:
            cls.tags[tag] = len(cls.tags)
        return cls.tags[tag]



cpdef enum:
    P2i
    P2c
    P2shape
    P2suff
    P2pref
    P2w
    P2oft_title
    P2oft_upper

    P1i
    P1c
    P1shape
    P1suff
    P1pref
    P1w
    P1oft_title
    P1oft_upper

    N0i
    N0c
    N0shape
    N0suff
    N0pref
    N0w
    N0oft_title
    N0oft_upper

    N1i
    N1c
    N1shape
    N1suff
    N1pref
    N1w
    N1oft_title
    N1oft_upper
    
    N2i
    N2c
    N2shape
    N2suff
    N2pref
    N2w
    N2oft_title
    N2oft_upper

    P1t
    P2t
    CONTEXT_SIZE


cdef int get_atoms(atom_t* context, int i, Tokens tokens, class_t prev_tag,
                   class_t prev_prev_tag) except -1:
    cdef int j
    for j in range(CONTEXT_SIZE):
        context[j] = 0
    indices = [i-2, i-1, i, i+1, i+2]
    ints = tokens.int_array(indices, [LexInt_id, LexInt_cluster])
    flags = tokens.bool_array(indices, [LexDist_title, LexDist_upper])
    strings = tokens.string_hash_array(indices, [LexStr_shape, LexStr_suff,
                                                 LexStr_pre, LexStr_norm])
    _fill_token(&context[P2i], flags[0], ints[0], strings[0])
    _fill_token(&context[P1i], flags[1], ints[1], strings[1])
    _fill_token(&context[N0i], flags[2], ints[2], strings[2])
    _fill_token(&context[N1i], flags[3], ints[3], strings[3])
    _fill_token(&context[N2i], flags[4], ints[4], strings[4])
    context[P1t] = prev_tag
    context[P2t] = prev_prev_tag


cdef int _fill_token(atom_t* c, flags, ints, strings) except -1:
    cdef int i = 0
    c[i] = ints[0]; i += 1
    c[i] = ints[1]; i += 1
    c[i] = strings[0]; i += 1
    c[i] = strings[1]; i += 1
    c[i] = strings[2]; i += 1
    c[i] = strings[3]; i += 1
    c[i] = flags[0]; i += 1
    c[i] = flags[1]; i += 1


TEMPLATES = (
    (N0i,),
    #(N0w,),
    #(N0suff,),
    #(N0pref,),
    (P1t,),
    (P2t,),
    #(P1t, P2t),
    #(P1t, N0w),
    #(P1w,),
    #(P1suff,),
    #(P2w,),
    #(N1w,),
    #(N1suff,),
    #(N2w,),

    #(N0shape,),
    #(N0c,),
    #(N1c,),
    #(N2c,),
    #(P1c,),
    #(P2c,),
    #(N0oft_upper,),
    #(N0oft_title,),
)

