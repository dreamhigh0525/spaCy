from spacy.lang cimport Language
from spacy.word cimport Lexeme
from spacy.tokens cimport Tokens


cdef class EnglishTokens(Tokens):
    cpdef size_t canon(self, size_t i)
    cpdef size_t shape(self, size_t i)
    cpdef size_t non_sparse(self, size_t i)
    cpdef size_t asciied(self, size_t i)
    cpdef unicode canon_string(self, size_t i)
    cpdef unicode shape_string(self, size_t i)
    cpdef unicode non_sparse_string(self, size_t i)
    cpdef unicode asciied_string(self, size_t i)
    cpdef bint is_alpha(self, size_t i)
    cpdef bint is_ascii(self, size_t i)
    cpdef bint is_digit(self, size_t i)
    cpdef bint is_lower(self, size_t i)
    cpdef bint is_punct(self, size_t i)
    cpdef bint is_space(self, size_t i)
    cpdef bint is_title(self, size_t i)
    cpdef bint is_upper(self, size_t i)
    cpdef bint can_adj(self, size_t i)
    cpdef bint can_adp(self, size_t i)
    cpdef bint can_adv(self, size_t i)
    cpdef bint can_conj(self, size_t i)
    cpdef bint can_det(self, size_t i)
    cpdef bint can_noun(self, size_t i)
    cpdef bint can_num(self, size_t i)
    cpdef bint can_pdt(self, size_t i)
    cpdef bint can_pos(self, size_t i)
    cpdef bint can_pron(self, size_t i)
    cpdef bint can_prt(self, size_t i)
    cpdef bint can_punct(self, size_t i)
    cpdef bint can_verb(self, size_t i)
    cpdef bint oft_lower(self, size_t i)
    cpdef bint oft_title(self, size_t i)
    cpdef bint oft_upper(self, size_t i)


cdef class English(Language):
    cdef int _split_one(self, Py_UNICODE* characters, size_t length)
