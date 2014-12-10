from spacy.lemmatizer import Lemmatizer, read_index, read_exc
from spacy.util import DATA_DIR
from os import path

import pytest


def test_read_index():
    wn = path.join(DATA_DIR, 'wordnet')
    index = read_index(path.join(wn, 'index.noun'))
    assert 'man' in index
    assert 'plantes' not in index
    assert 'plant' in index


def test_read_exc():
    wn = path.join(DATA_DIR, 'wordnet')
    exc = read_exc(path.join(wn, 'verb.exc'))
    assert exc['was'] == ('be',)


@pytest.fixture
def lemmatizer():
    return Lemmatizer(path.join(DATA_DIR, 'wordnet'))


def test_noun_lemmas(lemmatizer):
    do = lemmatizer.noun

    assert do('aardwolves') == set(['aardwolf'])
    assert do('aardwolf') == set(['aardwolf'])
    assert do('planets') == set(['planet'])
    assert do('ring') == set(['ring'])
    assert do('axes') == set(['axis', 'axe', 'ax'])
