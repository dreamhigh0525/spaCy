from cymem.cymem cimport Pool
from thinc.typedefs cimport weight_t

from ..structs cimport TokenC
from ._state cimport State
from .conll cimport GoldParse


cdef struct Transition:
    int clas
    int move
    int label

    weight_t score

    int (*get_cost)(const Transition* self, const State* state, GoldParse gold) except -1
    int (*do)(const Transition* self, State* state) except -1


ctypedef int (*get_cost_func_t)(const Transition* self, const State* state,
              GoldParse gold) except -1

ctypedef int (*do_func_t)(const Transition* self, State* state) except -1


cdef class TransitionSystem:
    cdef readonly dict label_ids
    cdef Pool mem
    cdef const Transition* c

    cdef Transition init_transition(self, int clas, int move, int label) except *

    cdef const Transition best_valid(self, const weight_t*, const State*) except *

    cdef const Transition best_gold(self, const weight_t*, const State*,
                                    GoldParse gold) except *
