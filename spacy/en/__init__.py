from __future__ import unicode_literals
from os import path
import re

from .. import orth
from ..vocab import Vocab
from ..tokenizer import Tokenizer
from ..syntax.parser import GreedyParser
from ..tokens import Tokens
from .pos import EnPosTagger
from .pos import POS_TAGS
from .attrs import get_flags


from ..util import read_lang_data


def get_lex_props(string):
    return {
        'flags': get_flags(string),
        'length': len(string),
        'orth': string,
        'lower': string.lower(),
        'norm': string,
        'shape': orth.word_shape(string),
        'prefix': string[0],
        'suffix': string[-3:],
        'cluster': 0,
        'prob': 0,
        'sentiment': 0
    }


LOCAL_DATA_DIR = path.join(path.dirname(__file__), 'data')


class English(object):
    """The English NLP pipeline.

    Provides a tokenizer, lexicon, part-of-speech tagger and parser.

    Keyword args:
        data_dir (unicode): A path to a directory, from which to load the pipeline.
            If None, looks for a directory named "data/" in the same directory as
            the present file, i.e. path.join(path.dirname(__file__, 'data')).
            If path.join(data_dir, 'pos') exists, the tagger is loaded from it.
            If path.join(data_dir, 'deps') exists, the parser is loaded from it.
            See Pipeline Directory Structure for details.

    Attributes:
        vocab (spacy.vocab.Vocab): The lexicon.

        strings (spacy.strings.StringStore): Encode/decode strings to/from integer IDs.

        tokenizer (spacy.tokenizer.Tokenizer): The start of the pipeline.

        tagger (spacy.en.pos.EnPosTagger):
            The part-of-speech tagger, which also performs lemmatization and
            morphological analysis.

        parser (spacy.syntax.parser.GreedyParser):
            A greedy shift-reduce dependency parser.
    """
    def __init__(self, data_dir=LOCAL_DATA_DIR):
        self._data_dir = data_dir
        self.vocab = Vocab(data_dir=path.join(data_dir, 'vocab') if data_dir else None,
                           get_lex_props=get_lex_props)
        tag_names = list(POS_TAGS.keys())
        tag_names.sort()
        if data_dir is None:
            tok_rules = {}
            prefix_re = None
            suffix_re = None
            infix_re = None
        else:
            tok_data_dir = path.join(data_dir, 'tokenizer')
            tok_rules, prefix_re, suffix_re, infix_re = read_lang_data(tok_data_dir)
            prefix_re = re.compile(prefix_re)
            suffix_re = re.compile(suffix_re)
            infix_re = re.compile(infix_re)
        self.tokenizer = Tokenizer(self.vocab, tok_rules, prefix_re,
                                   suffix_re, infix_re,
                                   POS_TAGS, tag_names)
        self._tagger = None
        self._parser = None

        self.has_parser_model = path.exists(path.join(self._data_dir, 'deps'))
        self.has_tagger_model = path.exists(path.join(self._data_dir, 'pos'))

    @property
    def tagger(self):
        if self._tagger is None:
            self._tagger = EnPosTagger(self.vocab.strings, self._data_dir)
        return self._tagger

    @property
    def parser(self):
        if self._parser is None:
            self._parser = GreedyParser(path.join(self._data_dir, 'deps'))
        return self._parser

    def __call__(self, text, tag=True, parse=True):
        """Apply the pipeline to some text.
        
        Args:
            text (unicode): The text to be processed.

        Keyword args:
            tag (bool): Whether to add part-of-speech tags to the text.  This
                will also set morphological analysis and lemmas.

            parse (bool): Whether to add dependency-heads and labels to the text.

        Returns:
            tokens (spacy.tokens.Tokens):
        """
        tokens = self.tokenizer(text)
        if tag or parse and self.has_tagger_model:
            self.tagger(tokens)
        if parse and self.has_parser_model:
            self.parser(tokens)
        return tokens

    @property
    def tags(self):
        """List of part-of-speech tag names."""
        return self.tagger.tag_names
