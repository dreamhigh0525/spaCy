from __future__ import unicode_literals

from spacy.en import EN

import pytest


@pytest.fixture
def close_puncts():
    return [')', ']', '}', '*']


def test_close(close_puncts):
    word_str = 'Hello'
    for p in close_puncts:
        string = word_str + p
        tokens = EN.tokenize(string)
        assert len(tokens) == 2
        assert tokens[1].string == p
        assert tokens[0].string == word_str


def test_two_different_close(close_puncts):
    word_str = 'Hello'
    for p in close_puncts:
        string = word_str + p + "'"
        tokens = EN.tokenize(string)
        assert len(tokens) == 3
        assert tokens[0].string == word_str
        assert tokens[1].string == p
        assert tokens[2].string == "'"


def test_three_same_close(close_puncts):
    word_str = 'Hello'
    for p in close_puncts:
        string = word_str + p + p + p
        tokens = EN.tokenize(string)
        assert len(tokens) == 4
        assert tokens[0].string == word_str
        assert tokens[1].string == p
