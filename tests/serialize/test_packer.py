from __future__ import unicode_literals

import re

import pytest
import numpy

from spacy.vocab import Vocab
from spacy.tokens.doc import Doc
from spacy.tokenizer import Tokenizer
from spacy.en import LOCAL_DATA_DIR
from os import path

from spacy.attrs import ORTH, SPACY, TAG, DEP, HEAD
from spacy.serialize.packer import Packer

from spacy.serialize.bits import BitArray


def get_lex_props(string, prob=-22):
    return {
        'flags': 0,
        'length': len(string),
        'orth': string,
        'lower': string, 
        'norm': string,
        'shape': string,
        'prefix': string[0],
        'suffix': string[-3:],
        'cluster': 0,
        'prob': prob,
        'sentiment': 0
    }


@pytest.fixture
def vocab():
    vocab = Vocab(get_lex_props=get_lex_props)
    vocab['dog'] = get_lex_props('dog', 0.001)
    assert vocab[vocab.strings['dog']].orth_ == 'dog'
    vocab['the'] = get_lex_props('the', 0.01)
    vocab['quick'] = get_lex_props('quick', 0.005)
    vocab['jumped'] = get_lex_props('jumped', 0.007)
    return vocab


@pytest.fixture
def tokenizer(vocab):
    null_re = re.compile(r'!!!!!!!!!')
    tokenizer = Tokenizer(vocab, {}, null_re, null_re, null_re)
    return tokenizer


def test_char_packer(vocab):
    packer = Packer(vocab, [])
    bits = BitArray()
    bits.seek(0)

    byte_str = b'the dog jumped'
    packer.char_codec.encode(byte_str, bits)
    bits.seek(0)
    result = [b''] * len(byte_str)
    packer.char_codec.decode(bits, result)
    assert b''.join(result) == byte_str


def test_packer_unannotated(tokenizer):
    packer = Packer(tokenizer.vocab, [])

    msg = tokenizer(u'the dog jumped')

    assert msg.string == 'the dog jumped'
    

    bits = packer.pack(msg)

    result = packer.unpack(bits)

    assert result.string == 'the dog jumped'


def test_packer_annotated(tokenizer):
    vocab = tokenizer.vocab
    nn = vocab.strings['NN']
    dt = vocab.strings['DT']
    vbd = vocab.strings['VBD']
    jj = vocab.strings['JJ']
    det = vocab.strings['det']
    nsubj = vocab.strings['nsubj']
    adj = vocab.strings['adj']
    root = vocab.strings['ROOT']

    attr_freqs = [
        (TAG, [(nn, 0.1), (dt, 0.2), (jj, 0.01), (vbd, 0.05)]),
        (DEP, {det: 0.2, nsubj: 0.1, adj: 0.05, root: 0.1}.items()),
        (HEAD, {0: 0.05, 1: 0.2, -1: 0.2, -2: 0.1, 2: 0.1}.items())
    ]

    packer = Packer(vocab, attr_freqs)

    msg = tokenizer(u'the dog jumped')

    msg.from_array(
        [TAG, DEP, HEAD],
        numpy.array([
            [dt, det, 1],
            [nn, nsubj, 1],
            [vbd, root, 0]
        ], dtype=numpy.int32))

    assert msg.string == 'the dog jumped'
    assert [t.tag_ for t in msg] == ['DT', 'NN', 'VBD']
    assert [t.dep_ for t in msg] == ['det', 'nsubj', 'ROOT']
    assert [(t.head.i - t.i) for t in msg] == [1, 1, 0]

    bits = packer.pack(msg)
    result = packer.unpack(bits)

    assert result.string == 'the dog jumped'
    assert [t.tag_ for t in result] == ['DT', 'NN', 'VBD']
    assert [t.dep_ for t in result] == ['det', 'nsubj', 'ROOT']
    assert [(t.head.i - t.i) for t in result] == [1, 1, 0]


