# coding: utf8
from __future__ import unicode_literals

from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS, TOKEN_MATCH
from .punctuation import TOKENIZER_SUFFIXES, TOKENIZER_INFIXES
from .stop_words import STOP_WORDS
from .lex_attrs import LEX_ATTRS
from .lemmatizer import LOOKUP
from .syntax_iterators import SYNTAX_ITERATORS

from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ..norm_exceptions import BASE_NORMS
from ...language import Language
from ...lemmatizerlookup import Lemmatizer
from ...attrs import LANG, NORM
from ...util import update_exc, add_lookups


class FrenchDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: 'fr'
    lex_attr_getters[NORM] = add_lookups(Language.Defaults.lex_attr_getters[NORM], BASE_NORMS)

    tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)
    stop_words = set(STOP_WORDS)
    infixes = tuple(TOKENIZER_INFIXES)
    suffixes = tuple(TOKENIZER_SUFFIXES)
    token_match = TOKEN_MATCH
    syntax_iterators = dict(SYNTAX_ITERATORS)

    @classmethod
    def create_lemmatizer(cls, nlp=None):
        return Lemmatizer(LOOKUP)


class French(Language):
    lang = 'fr'
    Defaults = FrenchDefaults


__all__ = ['French']
