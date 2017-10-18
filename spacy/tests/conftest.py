# coding: utf-8
from __future__ import unicode_literals

from ..en import English
from ..de import German
from ..es import Spanish
from ..it import Italian
from ..ja import Japanese
from ..fr import French
from ..pt import Portuguese
from ..nl import Dutch
from ..sv import Swedish
from ..hu import Hungarian
from ..fi import Finnish
from ..bn import Bengali
from ..he import Hebrew
from ..nb import Norwegian
from ..th import Thai
from ..ru import Russian

from ..tokens import Doc
from ..strings import StringStore
from ..lemmatizer import Lemmatizer
from ..attrs import ORTH, TAG, HEAD, DEP

from io import StringIO, BytesIO
from pathlib import Path
import os
import pytest

# These languages get run through generic tokenizer tests
LANGUAGES = [English, German, Spanish, Italian, French, Portuguese, Dutch,
             Swedish, Hungarian, Finnish, Bengali, Norwegian]


@pytest.fixture(params=LANGUAGES)
def tokenizer(request):
    lang = request.param
    return lang.Defaults.create_tokenizer()


@pytest.fixture
def en_tokenizer():
    return English.Defaults.create_tokenizer()


@pytest.fixture
def en_vocab():
    return English.Defaults.create_vocab()


@pytest.fixture
def en_parser():
    return English.Defaults.create_parser()


@pytest.fixture
def es_tokenizer():
    return Spanish.Defaults.create_tokenizer()


@pytest.fixture
def de_tokenizer():
    return German.Defaults.create_tokenizer()


@pytest.fixture(scope='module')
def fr_tokenizer():
    return French.Defaults.create_tokenizer()


@pytest.fixture
def hu_tokenizer():
    return Hungarian.Defaults.create_tokenizer()


@pytest.fixture
def fi_tokenizer():
    return Finnish.Defaults.create_tokenizer()


@pytest.fixture
def ja_tokenizer():
    pytest.importorskip("MeCab")
    return Japanese.Defaults.create_tokenizer()


@pytest.fixture
def japanese():
    pytest.importorskip("MeCab")
    return Japanese()


@pytest.fixture
def sv_tokenizer():
    return Swedish.Defaults.create_tokenizer()


@pytest.fixture
def bn_tokenizer():
    return Bengali.Defaults.create_tokenizer()


@pytest.fixture
def he_tokenizer():
    return Hebrew.Defaults.create_tokenizer()


@pytest.fixture
def nb_tokenizer():
    return Norwegian.Defaults.create_tokenizer()


@pytest.fixture
def th_tokenizer():
    pythainlp = pytest.importorskip("pythainlp")
    return Thai.Defaults.create_tokenizer()


@pytest.fixture
def ru_tokenizer():
    pytest.importorskip("pymorphy2")
    return Russian.Defaults.create_tokenizer()


@pytest.fixture
def russian():
    pytest.importorskip("pymorphy2")
    return Russian()


@pytest.fixture
def stringstore():
    return StringStore()


@pytest.fixture
def en_entityrecognizer():
    return English.Defaults.create_entity()


@pytest.fixture
def lemmatizer():
    return English.Defaults.create_lemmatizer()


@pytest.fixture
def text_file():
    return StringIO()


@pytest.fixture
def text_file_b():
    return BytesIO()


# only used for tests that require loading the models
# in all other cases, use specific instances
@pytest.fixture(scope="session")
def EN():
    return English()


@pytest.fixture(scope="session")
def DE():
    return German()


def pytest_addoption(parser):
    parser.addoption("--models", action="store_true",
                     help="include tests that require full models")
    parser.addoption("--vectors", action="store_true",
                     help="include word vectors tests")
    parser.addoption("--slow", action="store_true",
                     help="include slow tests")


def pytest_runtest_setup(item):
    for opt in ['models', 'vectors', 'slow']:
        if opt in item.keywords and not item.config.getoption("--%s" % opt):
            pytest.skip("need --%s option to run" % opt)
