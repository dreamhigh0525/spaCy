cdef struct Transition:
    int clas
    int move
    int label

    weight_t score
    int cost

    int (*get_cost)(const Transition* self, const State* state, const TokenC* gold) except -1

    int (*is_valid)(const Transition* self, const State* state) except -1
    
    int (*do)(const Transition* self, State* state) except -1


cdef class TransitionSystem:
    cdef readonly dict label_ids
    cdef Pool mem
    cdef const Transition* c

    cdef const Transition best_valid(self, const weight_t*, const State*) except *

    cdef const Transition best_gold(self, const weight_t*, const State*,
                                    const TokenC*) except *

