from .structs cimport TokenC, Lexeme, Morphology, PosTag


cdef int set_morph_from_dict(Morphology* morph, dict props) except -1
