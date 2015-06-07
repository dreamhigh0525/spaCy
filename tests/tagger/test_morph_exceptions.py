from __future__ import unicode_literals
from spacy.en import English

import pytest

from spacy.en import English

@pytest.fixture
def morph_exc():
    return {
            'PRP$': {'his': {'L': '-PRP-', 'person': 3, 'case': 2}},
           }


def test_load_exc(morph_exc):
    # Do this local as we want to modify it
    nlp =  English()
    nlp.tagger.load_morph_exceptions(morph_exc)
    tokens = nlp('I like his style.', tag=True, parse=False)
    his = tokens[2]
    assert his.tag_ == 'PRP$'
    assert his.lemma_ == '-PRP-'
