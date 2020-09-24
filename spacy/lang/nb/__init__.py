from typing import Optional
from thinc.api import Model
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from .punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES
from .punctuation import TOKENIZER_SUFFIXES
from .stop_words import STOP_WORDS
from .syntax_iterators import SYNTAX_ITERATORS
from ...language import Language
from ...lookups import Lookups
from ...pipeline import Lemmatizer


class NorwegianDefaults(Language.Defaults):
    tokenizer_exceptions = TOKENIZER_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    infixes = TOKENIZER_INFIXES
    suffixes = TOKENIZER_SUFFIXES
    syntax_iterators = SYNTAX_ITERATORS
    stop_words = STOP_WORDS


class Norwegian(Language):
    lang = "nb"
    Defaults = NorwegianDefaults


@Norwegian.factory(
    "lemmatizer",
    assigns=["token.lemma"],
    default_config={"model": None, "mode": "rule", "lookups": None},
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language,
    model: Optional[Model],
    name: str,
    mode: str,
    lookups: Optional[Lookups],
):
    lookups = Lemmatizer.load_lookups(nlp.lang, mode, lookups)
    return Lemmatizer(nlp.vocab, model, name, mode=mode, lookups=lookups)


__all__ = ["Norwegian"]
