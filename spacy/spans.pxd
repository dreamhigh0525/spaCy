from .tokens cimport Tokens
from .typedefs cimport flags_t, attr_id_t, attr_t
from .parts_of_speech cimport univ_pos_t
from .structs cimport Morphology, TokenC, LexemeC
from .vocab cimport Vocab
from .strings cimport StringStore


cdef class Spans:
    cdef Vocab vocab
    cdef Tokens tokens
    cdef readonly list spans
    cpdef long[:,:] to_array(self, object py_attr_ids)

    
cdef class Span:
    cdef readonly Tokens _seq
    cdef public int i
    cdef public int start
    cdef public int end
    cdef readonly int label
    cdef public Span head
    cdef public list rights
    cdef public list lefts

