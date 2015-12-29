# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import io
import pickle

from spacy.lemmatizer import Lemmatizer, read_index, read_exc
from spacy.util import get_package, MockPackage

import pytest


@pytest.fixture
def package():
    if os.environ.get('SPACY_DATA'):
        data_path = os.environ.get('SPACY_DATA')
    else:
        data_path = None
    return get_package(data_path=data_path)


@pytest.fixture
def lemmatizer(package):
    return Lemmatizer.load(package)


def test_read_index(package):
    index = package.load_utf8(read_index, 'wordnet', 'index.noun')
    assert 'man' in index
    assert 'plantes' not in index
    assert 'plant' in index


def test_read_exc(package):
    exc = package.load_utf8(read_exc, 'wordnet', 'verb.exc')
    assert exc['was'] == ('be',)


def test_noun_lemmas(lemmatizer):
    do = lemmatizer.noun

    assert do('aardwolves') == set(['aardwolf'])
    assert do('aardwolf') == set(['aardwolf'])
    assert do('planets') == set(['planet'])
    assert do('ring') == set(['ring'])
    assert do('axes') == set(['axis', 'axe', 'ax'])


def test_smart_quotes(lemmatizer):
    do = lemmatizer.punct
    assert do('“') == set(['"'])
    assert do('“') == set(['"'])


def test_pickle_lemmatizer(lemmatizer):
    file_ = io.BytesIO()
    pickle.dump(lemmatizer, file_)

    file_.seek(0)
    
    loaded = pickle.load(file_)
