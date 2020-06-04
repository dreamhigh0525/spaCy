# encoding: utf8
from __future__ import unicode_literals, print_function

import re
from collections import namedtuple

from .stop_words import STOP_WORDS
from .syntax_iterators import SYNTAX_ITERATORS
from .tag_map import TAG_MAP
from .tag_orth_map import TAG_ORTH_MAP
from .tag_bigram_map import TAG_BIGRAM_MAP
from ...attrs import LANG
from ...compat import copy_reg
from ...language import Language
from ...symbols import POS
from ...tokens import Doc
from ...util import DummyTokenizer, get_words_and_spaces

# Hold the attributes we need with convenient names
DetailedToken = namedtuple("DetailedToken", ["surface", "pos", "lemma"])

# Handling for multiple spaces in a row is somewhat awkward, this simplifies
# the flow by creating a dummy with the same interface.
DummyNode = namedtuple("DummyNode", ["surface", "pos", "lemma"])
DummySpace = DummyNode(" ", " ", " ")


def try_sudachi_import():
    """SudachiPy is required for Japanese support, so check for it.
    It it's not available blow up and explain how to fix it."""
    try:
        from sudachipy import dictionary, tokenizer

        tok = dictionary.Dictionary().create(
            mode=tokenizer.Tokenizer.SplitMode.A
        )
        return tok
    except ImportError:
        raise ImportError(
            "Japanese support requires SudachiPy: " "https://github.com/WorksApplications/SudachiPy"
        )


def resolve_pos(token, next_token):
    """If necessary, add a field to the POS tag for UD mapping.
    Under Universal Dependencies, sometimes the same Unidic POS tag can
    be mapped differently depending on the literal token or its context
    in the sentence. This function returns resolved POSs for both token
    and next_token by tuple.
    """

    # Some tokens have their UD tag decided based on the POS of the following
    # token.

    # orth based rules
    if token.pos in TAG_ORTH_MAP:
        orth_map = TAG_ORTH_MAP[token.pos[0]]
        if token.surface in orth_map:
            return orth_map[token.surface], None

    # tag bi-gram mapping
    if next_token:
        tag_bigram = token.pos[0], next_token.pos[0]
        if tag_bigram in TAG_BIGRAM_MAP:
            bipos = TAG_BIGRAM_MAP[tag_bigram]
            if bipos[0] is None:
                return TAG_MAP[token.pos[0]][POS], bipos[1]
            else:
                return bipos

    return TAG_MAP[token.pos[0]][POS], None


# Use a mapping of paired punctuation to avoid splitting quoted sentences.
pairpunct = {'「':'」', '『': '』', '【': '】'}


def separate_sentences(doc):
    """Given a doc, mark tokens that start sentences based on Unidic tags.
    """

    stack = [] # save paired punctuation

    for i, token in enumerate(doc[:-2]):
        # Set all tokens after the first to false by default. This is necessary
        # for the doc code to be aware we've done sentencization, see
        # `is_sentenced`.
        token.sent_start = (i == 0)
        if token.tag_:
            if token.tag_ == "補助記号-括弧開":
                ts = str(token)
                if ts in pairpunct:
                    stack.append(pairpunct[ts])
                elif stack and ts == stack[-1]:
                    stack.pop()

            if token.tag_ == "補助記号-句点":
                next_token = doc[i+1]
                if next_token.tag_ != token.tag_ and not stack:
                    next_token.sent_start = True


def get_dtokens(tokenizer, text):
    tokens = tokenizer.tokenize(text)
    words = []
    for ti, token in enumerate(tokens):
        tag = '-'.join([xx for xx in token.part_of_speech()[:4] if xx != '*'])
        inf = '-'.join([xx for xx in token.part_of_speech()[4:] if xx != '*'])
        dtoken = DetailedToken(
                token.surface(),
                (tag, inf),
                token.dictionary_form())
        if ti > 0 and words[-1].pos[0] == '空白' and tag == '空白':
            # don't add multiple space tokens in a row
            continue
        words.append(dtoken)

    # remove empty tokens. These can be produced with characters like … that
    # Sudachi normalizes internally. 
    words = [ww for ww in words if len(ww.surface) > 0]
    return words

class JapaneseTokenizer(DummyTokenizer):
    def __init__(self, cls, nlp=None):
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.tokenizer = try_sudachi_import()

    def __call__(self, text):
        dtokens = get_dtokens(self.tokenizer, text)

        words = [x.surface for x in dtokens]
        words, spaces = get_words_and_spaces(words, text)
        unidic_tags = [",".join(x.pos) for x in dtokens]
        doc = Doc(self.vocab, words=words, spaces=spaces)
        next_pos = None
        for ii, (token, dtoken) in enumerate(zip(doc, dtokens)):
            ntoken = dtokens[ii+1] if ii+1 < len(dtokens) else None
            token.tag_ = dtoken.pos[0]
            if next_pos:
                token.pos = next_pos
                next_pos = None
            else:
                token.pos, next_pos = resolve_pos(dtoken, ntoken)

            # if there's no lemma info (it's an unk) just use the surface
            token.lemma_ = dtoken.lemma
        doc.user_data["unidic_tags"] = unidic_tags

        separate_sentences(doc)
        return doc


class JapaneseDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda _text: "ja"
    stop_words = STOP_WORDS
    tag_map = TAG_MAP
    syntax_iterators = SYNTAX_ITERATORS
    writing_system = {"direction": "ltr", "has_case": False, "has_letters": False}

    @classmethod
    def create_tokenizer(cls, nlp=None):
        return JapaneseTokenizer(cls, nlp)


class Japanese(Language):
    lang = "ja"
    Defaults = JapaneseDefaults

    def make_doc(self, text):
        return self.tokenizer(text)


def pickle_japanese(instance):
    return Japanese, tuple()


copy_reg.pickle(Japanese, pickle_japanese)

__all__ = ["Japanese"]
