from cymem.cymem cimport Pool

from .structs cimport Move, State


cdef class PyState:
    cdef Pool mem
    cdef readonly list tag_names
    cdef readonly int n_classes
    cdef readonly dict moves_by_name
    
    cdef Move* _moves
    cdef Move* _golds
    cdef State* _s

    cdef Move* _get_move(self, unicode move_name) except NULL
