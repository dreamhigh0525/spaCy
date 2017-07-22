# encoding: utf8
from __future__ import unicode_literals, print_function

from os import path

from ..language import Language, BaseDefaults
from ..tokenizer import Tokenizer
from ..attrs import LANG
from ..tokens import Doc

from .language_data import *

class JapaneseTokenizer(object):
    def __init__(self, cls, nlp=None):
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        try:
            from janome.tokenizer import Tokenizer
        except ImportError:
            raise ImportError("The Japanese tokenizer requires the Janome library: "
                              "https://github.com/mocobeta/janome")
        self.tokenizer = Tokenizer()

    def __call__(self, text):
        words = [x.surface for x in self.tokenizer.tokenize(text)]
        return Doc(self.vocab, words=words, spaces=[False]*len(words))

class JapaneseDefaults(BaseDefaults):
    @classmethod
    def create_tokenizer(cls, nlp=None):
        return JapaneseTokenizer(cls, nlp)

class Japanese(Language):
    lang = 'ja'

    Defaults = JapaneseDefaults

    def make_doc(self, text):
        words = self.tokenizer(text)
        return Doc(self.vocab, words=words, spaces=[False]*len(words))

        
