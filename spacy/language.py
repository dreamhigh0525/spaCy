# coding: utf8
from __future__ import absolute_import, unicode_literals
from contextlib import contextmanager
import shutil

from .tokenizer import Tokenizer
from .vocab import Vocab
from .tagger import Tagger
from .matcher import Matcher
from .lemmatizer import Lemmatizer
from .train import Trainer
from .syntax.parser import get_templates
from .syntax.nonproj import PseudoProjectivity
from .pipeline import DependencyParser, EntityRecognizer
from .syntax.arc_eager import ArcEager
from .syntax.ner import BiluoPushDown
from .compat import json_dumps
from .attrs import IS_STOP
from . import attrs
from . import orth
from . import util
from . import language_data


class BaseDefaults(object):
    @classmethod
    def create_lemmatizer(cls, nlp=None):
        return Lemmatizer(cls.lemma_index, cls.lemma_exc, cls.lemma_rules)

    @classmethod
    def create_vocab(cls, nlp=None):
        lemmatizer = cls.create_lemmatizer(nlp)
        if nlp is None or nlp.path is None:
            lex_attr_getters = dict(cls.lex_attr_getters)
            # This is very messy, but it's the minimal working fix to Issue #639.
            # This defaults stuff needs to be refactored (again)
            lex_attr_getters[IS_STOP] = lambda string: string.lower() in cls.stop_words
            vocab = Vocab(lex_attr_getters=lex_attr_getters, tag_map=cls.tag_map,
                         lemmatizer=lemmatizer)
        else:
            vocab = Vocab.load(nlp.path, lex_attr_getters=cls.lex_attr_getters,
                             tag_map=cls.tag_map, lemmatizer=lemmatizer)
        for tag_str, exc in cls.morph_rules.items():
            for orth_str, attrs in exc.items():
                vocab.morphology.add_special_case(tag_str, orth_str, attrs)
        return vocab

    @classmethod
    def add_vectors(cls, nlp=None):
        if nlp is None or nlp.path is None:
            return False
        else:
            vec_path = nlp.path / 'vocab' / 'vec.bin'
            if vec_path.exists():
                return lambda vocab: vocab.load_vectors_from_bin_loc(vec_path)

    @classmethod
    def create_tokenizer(cls, nlp=None):
        rules = cls.tokenizer_exceptions
        if cls.token_match:
            token_match = cls.token_match
        if cls.prefixes:
            prefix_search  = util.compile_prefix_regex(cls.prefixes).search
        else:
            prefix_search = None
        if cls.suffixes:
            suffix_search  = util.compile_suffix_regex(cls.suffixes).search
        else:
            suffix_search = None
        if cls.infixes:
            infix_finditer = util.compile_infix_regex(cls.infixes).finditer
        else:
            infix_finditer = None
        vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        return Tokenizer(vocab, rules=rules,
                         prefix_search=prefix_search, suffix_search=suffix_search,
                         infix_finditer=infix_finditer, token_match=token_match)

    @classmethod
    def create_tagger(cls, nlp=None):
        if nlp is None:
            return Tagger(cls.create_vocab(), features=cls.tagger_features)
        elif nlp.path is False:
            return Tagger(nlp.vocab, features=cls.tagger_features)
        elif nlp.path is None or not (nlp.path / 'pos').exists():
            return None
        else:
            return Tagger.load(nlp.path / 'pos', nlp.vocab)

    @classmethod
    def create_parser(cls, nlp=None, **cfg):
        if nlp is None:
            return DependencyParser(cls.create_vocab(), features=cls.parser_features,
                                    **cfg)
        elif nlp.path is False:
            return DependencyParser(nlp.vocab, features=cls.parser_features, **cfg)
        elif nlp.path is None or not (nlp.path / 'deps').exists():
            return None
        else:
            return DependencyParser.load(nlp.path / 'deps', nlp.vocab, **cfg)

    @classmethod
    def create_entity(cls, nlp=None, **cfg):
        if nlp is None:
            return EntityRecognizer(cls.create_vocab(), features=cls.entity_features, **cfg)
        elif nlp.path is False:
            return EntityRecognizer(nlp.vocab, features=cls.entity_features, **cfg)
        elif nlp.path is None or not (nlp.path / 'ner').exists():
            return None
        else:
            return EntityRecognizer.load(nlp.path / 'ner', nlp.vocab, **cfg)

    @classmethod
    def create_matcher(cls, nlp=None):
        if nlp is None:
            return Matcher(cls.create_vocab())
        elif nlp.path is False:
            return Matcher(nlp.vocab)
        elif nlp.path is None or not (nlp.path / 'vocab').exists():
            return None
        else:
            return Matcher.load(nlp.path / 'vocab', nlp.vocab)

    @classmethod
    def create_pipeline(self, nlp=None):
        pipeline = []
        if nlp is None:
            return []
        if nlp.tagger:
            pipeline.append(nlp.tagger)
        if nlp.parser:
            pipeline.append(nlp.parser)
            pipeline.append(PseudoProjectivity.deprojectivize)
        if nlp.entity:
            pipeline.append(nlp.entity)
        return pipeline

    token_match = language_data.TOKEN_MATCH
    prefixes = tuple(language_data.TOKENIZER_PREFIXES)
    suffixes = tuple(language_data.TOKENIZER_SUFFIXES)
    infixes = tuple(language_data.TOKENIZER_INFIXES)
    tag_map = dict(language_data.TAG_MAP)
    tokenizer_exceptions = {}
    parser_features = get_templates('parser')
    entity_features = get_templates('ner')
    tagger_features = Tagger.feature_templates # TODO -- fix this
    stop_words = set()
    lemma_rules = {}
    lemma_exc = {}
    lemma_index = {}
    morph_rules = {}

    lex_attr_getters = {
        attrs.LOWER: lambda string: string.lower(),
        attrs.NORM: lambda string: string,
        attrs.SHAPE: orth.word_shape,
        attrs.PREFIX: lambda string: string[0],
        attrs.SUFFIX: lambda string: string[-3:],
        attrs.CLUSTER: lambda string: 0,
        attrs.IS_ALPHA: orth.is_alpha,
        attrs.IS_ASCII: orth.is_ascii,
        attrs.IS_DIGIT: lambda string: string.isdigit(),
        attrs.IS_LOWER: orth.is_lower,
        attrs.IS_PUNCT: orth.is_punct,
        attrs.IS_SPACE: lambda string: string.isspace(),
        attrs.IS_TITLE: orth.is_title,
        attrs.IS_UPPER: orth.is_upper,
        attrs.IS_BRACKET: orth.is_bracket,
        attrs.IS_QUOTE: orth.is_quote,
        attrs.IS_LEFT_PUNCT: orth.is_left_punct,
        attrs.IS_RIGHT_PUNCT: orth.is_right_punct,
        attrs.LIKE_URL: orth.like_url,
        attrs.LIKE_NUM: orth.like_number,
        attrs.LIKE_EMAIL: orth.like_email,
        attrs.IS_STOP: lambda string: False,
        attrs.IS_OOV: lambda string: True
    }


class Language(object):
    """
    A text-processing pipeline. Usually you'll load this once per process, and
    pass the instance around your program.
    """
    Defaults = BaseDefaults
    lang = None

    @classmethod
    def setup_directory(cls, path, **configs):
        """
        Initialise a model directory.
        """
        for name, config in configs.items():
            directory = path / name
            if directory.exists():
                shutil.rmtree(str(directory))
            directory.mkdir()
            with (directory / 'config.json').open('w') as file_:
                data = json_dumps(config)
                file_.write(data)
        if not (path / 'vocab').exists():
            (path / 'vocab').mkdir()

    @classmethod
    @contextmanager
    def train(cls, path, gold_tuples, **configs):
        parser_cfg = configs.get('deps', {})
        if parser_cfg.get('pseudoprojective'):
            # preprocess training data here before ArcEager.get_labels() is called
            gold_tuples = PseudoProjectivity.preprocess_training_data(gold_tuples)

        for subdir in ('deps', 'ner', 'pos'):
            if subdir not in configs:
                configs[subdir] = {}
        if parser_cfg:
            configs['deps']['actions'] = ArcEager.get_actions(gold_parses=gold_tuples)
        if 'ner' in configs:
            configs['ner']['actions'] = BiluoPushDown.get_actions(gold_parses=gold_tuples)

        cls.setup_directory(path, **configs)

        self = cls(
                path=path,
                vocab=False,
                tokenizer=False,
                tagger=False,
                parser=False,
                entity=False,
                matcher=False,
                serializer=False,
                vectors=False,
                pipeline=False)

        self.vocab = self.Defaults.create_vocab(self)
        self.tokenizer = self.Defaults.create_tokenizer(self)
        self.tagger = self.Defaults.create_tagger(self)
        self.parser = self.Defaults.create_parser(self)
        self.entity = self.Defaults.create_entity(self)
        self.pipeline = self.Defaults.create_pipeline(self)
        yield Trainer(self, gold_tuples)
        self.end_training()
        self.save_to_directory(path)

    def __init__(self, **overrides):
        """
        Create or load the pipeline.

        Arguments:
            **overrides: Keyword arguments indicating which defaults to override.

        Returns:
            Language: The newly constructed object.
        """
        if 'data_dir' in overrides and 'path' not in overrides:
            raise ValueError("The argument 'data_dir' has been renamed to 'path'")
        path = util.ensure_path(overrides.get('path', True))
        if path is True:
            path = util.get_data_path() / self.lang
            if not path.exists() and 'path' not in overrides:
                path = None
        self.meta = overrides.get('meta', {})
        self.path = path

        self.vocab     = self.Defaults.create_vocab(self) \
                         if 'vocab' not in overrides \
                         else overrides['vocab']
        add_vectors    = self.Defaults.add_vectors(self) \
                         if 'add_vectors' not in overrides \
                         else overrides['add_vectors']
        if self.vocab and add_vectors:
            add_vectors(self.vocab)
        self.tokenizer = self.Defaults.create_tokenizer(self) \
                         if 'tokenizer' not in overrides \
                         else overrides['tokenizer']
        self.tagger    = self.Defaults.create_tagger(self) \
                         if 'tagger' not in overrides \
                         else overrides['tagger']
        self.parser    = self.Defaults.create_parser(self) \
                         if 'parser' not in overrides \
                         else overrides['parser']
        self.entity    = self.Defaults.create_entity(self) \
                         if 'entity' not in overrides \
                         else overrides['entity']
        self.matcher   = self.Defaults.create_matcher(self) \
                         if 'matcher' not in overrides \
                         else overrides['matcher']

        if 'make_doc' in overrides:
            self.make_doc = overrides['make_doc']
        elif 'create_make_doc' in overrides:
            self.make_doc = overrides['create_make_doc'](self)
        elif not hasattr(self, 'make_doc'):
            self.make_doc = lambda text: self.tokenizer(text)
        if 'pipeline' in overrides:
            self.pipeline = overrides['pipeline']
        elif 'create_pipeline' in overrides:
            self.pipeline = overrides['create_pipeline'](self)
        else:
            self.pipeline = [self.tagger, self.parser, self.matcher, self.entity]

    def __call__(self, text, tag=True, parse=True, entity=True):
        """
        Apply the pipeline to some text.  The text can span multiple sentences,
        and can contain arbtrary whitespace.  Alignment into the original string
        is preserved.

        Argsuments:
            text (unicode): The text to be processed.

        Returns:
            doc (Doc): A container for accessing the annotations.

        Example:
            >>> from spacy.en import English
            >>> nlp = English()
            >>> tokens = nlp('An example sentence. Another example sentence.')
            >>> tokens[0].orth_, tokens[0].head.tag_
            ('An', 'NN')
        """
        doc = self.make_doc(text)
        if self.entity and entity:
            # Add any of the entity labels already set, in case we don't have them.
            for token in doc:
                if token.ent_type != 0:
                    self.entity.add_label(token.ent_type)
        skip = {self.tagger: not tag, self.parser: not parse, self.entity: not entity}
        for proc in self.pipeline:
            if proc and not skip.get(proc):
                proc(doc)
        return doc

    def pipe(self, texts, tag=True, parse=True, entity=True, n_threads=2, batch_size=1000):
        """
        Process texts as a stream, and yield Doc objects in order.

        Supports GIL-free multi-threading.

        Arguments:
            texts (iterator)
            tag (bool)
            parse (bool)
            entity (bool)
        """
        skip = {self.tagger: not tag, self.parser: not parse, self.entity: not entity}
        stream = (self.make_doc(text) for text in texts)
        for proc in self.pipeline:
            if proc and not skip.get(proc):
                if hasattr(proc, 'pipe'):
                    stream = proc.pipe(stream, n_threads=n_threads, batch_size=batch_size)
                else:
                    stream = (proc(item) for item in stream)
        for doc in stream:
            yield doc

    def save_to_directory(self, path):
        """
        Save the Vocab, StringStore and pipeline to a directory.

        Arguments:
            path (string or pathlib path): Path to save the model.
        """
        configs = {
            'pos': self.tagger.cfg if self.tagger else {},
            'deps': self.parser.cfg if self.parser else {},
            'ner': self.entity.cfg if self.entity else {},
        }

        path = util.ensure_path(path)
        if not path.exists():
            path.mkdir()
        self.setup_directory(path, **configs)

        strings_loc = path / 'vocab' / 'strings.json'
        with strings_loc.open('w', encoding='utf8') as file_:
            self.vocab.strings.dump(file_)
        self.vocab.dump(path / 'vocab' / 'lexemes.bin')
        # TODO: Word vectors?
        if self.tagger:
            self.tagger.model.dump(str(path / 'pos' / 'model'))
        if self.parser:
            self.parser.model.dump(str(path / 'deps' / 'model'))
        if self.entity:
            self.entity.model.dump(str(path / 'ner' / 'model'))

    def end_training(self, path=None):
        if self.tagger:
            self.tagger.model.end_training()
        if self.parser:
            self.parser.model.end_training()
        if self.entity:
            self.entity.model.end_training()
        # NB: This is slightly different from before --- we no longer default
        # to taking nlp.path
        if path is not None:
            self.save_to_directory(path)
