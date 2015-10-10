from __future__ import unicode_literals
from spacy.en import English
from spacy.attrs import IS_ALPHA, IS_ASCII, IS_DIGIT, IS_LOWER, IS_PUNCT
from spacy.attrs import IS_SPACE, IS_TITLE, IS_UPPER, LIKE_URL, LIKE_NUM
from spacy.attrs import IS_STOP

import pytest


@pytest.mark.models
def test_strings(EN):
    tokens = EN(u'Give it back! He pleaded.')
    token = tokens[0]
    assert token.orth_ == 'Give'
    assert token.text == 'Give'
    assert token.text_with_ws == 'Give '
    assert token.lower_ == 'give'
    assert token.shape_ == 'Xxxx'
    assert token.prefix_ == 'G'
    assert token.suffix_ == 'ive'
    assert token.lemma_ == 'give'
    assert token.pos_ == 'VERB'
    assert token.tag_ == 'VB'
    assert token.dep_ == 'ROOT'


def test_flags(EN):
    tokens = EN(u'Give it back! He pleaded.')
    token = tokens[0]
 
    assert token.check_flag(IS_ALPHA)
    assert not token.check_flag(IS_DIGIT)
    # TODO: Test more of these, esp. if a bug is found


def test_single_token_string(EN):
    tokens = EN(u'foobar')
    assert tokens[0].text == 'foobar'


def test_is_properties(EN):
    Hi, comma, my, email, is_, addr = EN(u'Hi, my email is test@me.com')
    assert Hi.is_title
    assert Hi.is_alpha
    assert not Hi.is_digit
    assert comma.is_punct
    assert email.is_ascii
    assert not email.like_url
    assert is_.is_lower
    assert addr.like_email
    assert addr.is_oov
    assert not Hi.is_oov

@pytest.mark.models
def test_vectors(EN):
    apples, oranges, oov = EN(u'apples oranges ldskbjlsdkbflzdfbl')
    assert apples.has_vector
    assert oranges.has_vector
    assert not oov.has_vector
    assert apples.similarity(oranges) > apples.similarity(oov)
    assert apples.similarity(oranges) == oranges.similarity(apples)
    assert sum(apples.vector) != sum(oranges.vector)
    assert apples.vector_norm != oranges.vector_norm
    
