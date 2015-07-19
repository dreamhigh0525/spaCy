# cython: profile=True
from libc.stdint cimport uint32_t
from libc.stdint cimport uint64_t
from libc.math cimport exp as c_exp
from libcpp.queue cimport priority_queue
from libcpp.pair cimport pair

from cymem.cymem cimport Address, Pool
from preshed.maps cimport PreshMap

from ..attrs cimport ORTH, ID, SPACY, TAG, HEAD, DEP, ENT_IOB, ENT_TYPE
from ..tokens.doc cimport Doc
from ..vocab cimport Vocab
from ..structs cimport LexemeC
from ..typedefs cimport attr_t
from .bits cimport BitArray
from .huffman cimport HuffmanCodec

from os import path
import numpy
from .. import util

cimport cython


# Format
# - Total number of bytes in message (32 bit int) --- handled outside this
# - Number of words (32 bit int)
# - Words, terminating in an EOL symbol, huffman coded ~12 bits per word
# - Spaces 1 bit per word
# - Attributes:
#       POS tag
#       Head offset
#       Dep label
#       Entity IOB
#       Entity tag


cdef class _BinaryCodec:
    def encode(self, attr_t[:] msg, BitArray bits):
        cdef int i
        for i in range(len(msg)):
            bits.append(msg[i])

    def decode(self, BitArray bits, attr_t[:] msg):
        cdef int i = 0 
        for bit in bits:
            msg[i] = bit
            i += 1
            if i == len(msg):
                break


cdef class _AttributeCodec:
    cdef Pool mem
    cdef attr_t* _keys
    cdef dict _map
    cdef HuffmanCodec _codec

    def __init__(self, freqs):
        self.mem = Pool()
        cdef attr_t key
        cdef float count
        cdef pair[float, attr_t] item

        cdef priority_queue[pair[float, attr_t]] items

        for key, count in freqs:
            item.first = count
            item.second = key
            items.push(item)
        weights = numpy.ndarray(shape=(items.size(),), dtype=numpy.float32)
        self._keys = <attr_t*>self.mem.alloc(items.size(), sizeof(attr_t))
        self._map = {}
        cdef int i = 0
        while not items.empty():
            item = items.top()
            # We put freq first above, for sorting
            self._keys[i] = item.second
            weights[i] = item.first
            self._map[self._keys[i]] = i
            items.pop()
            i += 1
        self._codec = HuffmanCodec(weights)

    def encode(self, attr_t[:] msg, BitArray dest):
        cdef int i
        for i in range(len(msg)):
            msg[i] = self._map[msg[i]]
        self._codec.encode(msg, dest)

    def decode(self, BitArray bits, attr_t[:] dest):
        cdef int i
        self._codec.decode(bits, dest)
        for i in range(len(dest)):
            dest[i] = <attr_t>self._keys[dest[i]]


def _gen_orths(Vocab vocab):
    cdef attr_t orth
    cdef size_t addr
    for orth, addr in vocab._by_orth.items():
        lex = <LexemeC*>addr
        yield orth, c_exp(lex.prob)


cdef class Packer:
    def __init__(self, Vocab vocab, attr_freqs):
        self.vocab = vocab
        self.lex_codec = _AttributeCodec(_gen_orths(vocab))
        
        codecs = [_AttributeCodec(_gen_orths(vocab)), _BinaryCodec()]
        attrs = [ORTH, SPACY]
        for attr, freqs in sorted(attr_freqs):
            if attr in (ORTH, ID, SPACY):
                continue
            codecs.append(_AttributeCodec(freqs))
            attrs.append(attr)
        self._codecs = tuple(codecs)
        self.attrs = tuple(attrs)

    @classmethod
    def from_dir(cls, Vocab vocab, data_dir):
        return cls(vocab, util.read_encoding_freqs(data_dir))

    def pack(self, Doc doc):
        array = doc.to_array(self.attrs)
        cdef BitArray bits = BitArray()
        cdef uint32_t length = len(doc)
        bits.extend(length, 32)
        for i, codec in enumerate(self._codecs):
            codec.encode(array[:, i], bits)
        return bits

    def unpack(self, BitArray bits):
        bits.seek(0)
        cdef uint32_t length = bits.read32()
        array = numpy.zeros(shape=(length, len(self._codecs)), dtype=numpy.int32)
        for i, codec in enumerate(self._codecs):
            codec.decode(bits, array[:, i])
        return array
