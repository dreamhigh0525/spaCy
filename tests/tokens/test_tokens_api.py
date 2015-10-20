from __future__ import unicode_literals

from spacy.tokens import Doc

import pytest

@pytest.mark.models
def test_getitem(EN):
    tokens = EN(u'Give it back! He pleaded.')
    assert tokens[0].orth_ == 'Give'
    assert tokens[-1].orth_ == '.'
    with pytest.raises(IndexError):
        tokens[len(tokens)]

    def to_str(span):
       return '/'.join(token.orth_ for token in span)

    span = tokens[1:1]
    assert not to_str(span)
    span = tokens[1:4]
    assert to_str(span) == 'it/back/!'
    span = tokens[1:4:1]
    assert to_str(span) == 'it/back/!'
    with pytest.raises(ValueError):
        tokens[1:4:2]
    with pytest.raises(ValueError):
        tokens[1:4:-1]

    span = tokens[-3:6]
    assert to_str(span) == 'He/pleaded'
    span = tokens[4:-1]
    assert to_str(span) == 'He/pleaded'
    span = tokens[-5:-3]
    assert to_str(span) == 'back/!'
    span = tokens[5:4]
    assert span.start == span.end == 5 and not to_str(span)
    span = tokens[4:-3]
    assert span.start == span.end == 4 and not to_str(span)

    span = tokens[:]
    assert to_str(span) == 'Give/it/back/!/He/pleaded/.'
    span = tokens[4:]
    assert to_str(span) == 'He/pleaded/.'
    span = tokens[:4]
    assert to_str(span) == 'Give/it/back/!'
    span = tokens[:-3]
    assert to_str(span) == 'Give/it/back/!'
    span = tokens[-3:]
    assert to_str(span) == 'He/pleaded/.'

    span = tokens[4:50]
    assert to_str(span) == 'He/pleaded/.'
    span = tokens[-50:4]
    assert to_str(span) == 'Give/it/back/!'
    span = tokens[-50:-40]
    assert span.start == span.end == 0 and not to_str(span)
    span = tokens[40:50]
    assert span.start == span.end == 7 and not to_str(span)

    span = tokens[1:4]
    assert span[0].orth_ == 'it'
    subspan = span[:]
    assert to_str(subspan) == 'it/back/!'
    subspan = span[:2]
    assert to_str(subspan) == 'it/back'
    subspan = span[1:]
    assert to_str(subspan) == 'back/!'
    subspan = span[:-1]
    assert to_str(subspan) == 'it/back'
    subspan = span[-2:]
    assert to_str(subspan) == 'back/!'
    subspan = span[1:2]
    assert to_str(subspan) == 'back'
    subspan = span[-2:-1]
    assert to_str(subspan) == 'back'
    subspan = span[-50:50]
    assert to_str(subspan) == 'it/back/!'
    subspan = span[50:-50]
    assert subspan.start == subspan.end == 4 and not to_str(subspan)


@pytest.mark.models
def test_serialize(EN):
    tokens = EN(u'Give it back! He pleaded.')
    packed = tokens.to_bytes()
    new_tokens = Doc(EN.vocab).from_bytes(packed)
    assert tokens.string == new_tokens.string
    assert [t.orth_ for t in tokens] == [t.orth_ for t in new_tokens]
    assert [t.orth for t in tokens] == [t.orth for t in new_tokens]


@pytest.mark.models
def test_serialize_whitespace(EN):
    tokens = EN(u' Give it back! He pleaded. ')
    packed = tokens.to_bytes()
    new_tokens = Doc(EN.vocab).from_bytes(packed)
    assert tokens.string == new_tokens.string
    assert [t.orth_ for t in tokens] == [t.orth_ for t in new_tokens]
    assert [t.orth for t in tokens] == [t.orth for t in new_tokens]


def test_set_ents(EN):
    tokens = EN.tokenizer(u'I use goggle chrone to surf the web')
    assert len(tokens.ents) == 0
    tokens.ents = [(EN.vocab.strings['PRODUCT'], 2, 4)]
    assert len(list(tokens.ents)) == 1
    assert [t.ent_iob for t in tokens] == [0, 0, 3, 1, 0, 0, 0, 0]
    ent = tokens.ents[0]
    assert ent.label_ == 'PRODUCT'
    assert ent.start == 2
    assert ent.end == 4


def test_merge(EN):
    doc = EN('WKRO played songs by the beach boys all night')

    assert len(doc) == 9
    # merge 'The Beach Boys'
    doc.merge(doc[4].idx, doc[6].idx + len(doc[6]), 'NAMED', 'LEMMA', 'TYPE')
    assert len(doc) == 7

    assert doc[4].text == 'the beach boys'
    assert doc[4].text_with_ws == 'the beach boys '
    assert doc[4].tag_ == 'NAMED'


def test_merge_end_string(EN):
    doc = EN('WKRO played songs by the beach boys all night')

    assert len(doc) == 9
    # merge 'The Beach Boys'
    doc.merge(doc[7].idx, doc[8].idx + len(doc[8]), 'NAMED', 'LEMMA', 'TYPE')
    assert len(doc) == 8

    assert doc[7].text == 'all night'
    assert doc[7].text_with_ws == 'all night'


@pytest.mark.models
def test_merge_children(EN):
    """Test that attachments work correctly after merging."""
    doc = EN('WKRO played songs by the beach boys all night')
    # merge 'The Beach Boys'
    doc.merge(doc[4].idx, doc[6].idx + len(doc[6]), 'NAMED', 'LEMMA', 'TYPE')
    
    for word in doc:
        if word.i < word.head.i:
            assert word in list(word.head.lefts)
        elif word.i > word.head.i:
            assert word in list(word.head.rights)
