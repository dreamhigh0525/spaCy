from __future__ import unicode_literals

from spacy.en import EN


def test_single_word():
    lex_ids = EN.tokenize(u'hello')
    assert lex_ids[0] == EN.lexicon.lookup(u'hello')


def test_two_words():
    words = EN.tokenize('hello possums')
    assert len(words) == 2
    assert words[0] == EN.lexicon.lookup('hello')
    assert words[0] != words[1]


def test_punct():
    tokens = EN.tokenize('hello, possums.')
    assert len(tokens) == 4
    assert tokens[0].string == EN.lexicon.lookup('hello').string
    assert tokens[1].string == EN.lexicon.lookup(',').string
    assert tokens[2].string == EN.lexicon.lookup('possums').string
    assert tokens[1].string != EN.lexicon.lookup('hello').string


def test_digits():
    lex_ids = EN.tokenize('The year: 1984.')
    assert len(lex_ids) == 5
    assert lex_ids[0].string == EN.lexicon.lookup('The').string
    assert lex_ids[3].string == EN.lexicon.lookup('1984').string
    assert lex_ids[4].string == EN.lexicon.lookup('.').string


def test_contraction():
    lex_ids = EN.tokenize("don't giggle")
    assert len(lex_ids) == 3
    assert lex_ids[1].string == EN.lexicon.lookup("not").string
    lex_ids = EN.tokenize("i said don't!")
    assert len(lex_ids) == 4
    assert lex_ids[3].string == EN.lexicon.lookup('!').string
