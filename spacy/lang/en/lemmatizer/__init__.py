# coding: utf8
from __future__ import unicode_literals

from pathlib import Path

from ._adjectives import ADJECTIVES
from ._adjectives_irreg import ADJECTIVES_IRREG
from ._adverbs import ADVERBS
from ._adverbs_irreg import ADVERBS_IRREG
from ._nouns_irreg import NOUNS_IRREG
from ._verbs import VERBS
from ._verbs_irreg import VERBS_IRREG
from ._lemma_rules import ADJECTIVE_RULES, NOUN_RULES, VERB_RULES, PUNCT_RULES

from ....util import load_language_data

LOOKUP = load_language_data(Path(__file__).parent / "lookup.json")
NOUNS = load_language_data(Path(__file__).parent / "_nouns.json")

LEMMA_INDEX = {"adj": ADJECTIVES, "adv": ADVERBS, "noun": NOUNS, "verb": VERBS}

LEMMA_EXC = {
    "adj": ADJECTIVES_IRREG,
    "adv": ADVERBS_IRREG,
    "noun": NOUNS_IRREG,
    "verb": VERBS_IRREG,
}

LEMMA_RULES = {
    "adj": ADJECTIVE_RULES,
    "noun": NOUN_RULES,
    "verb": VERB_RULES,
    "punct": PUNCT_RULES,
}
