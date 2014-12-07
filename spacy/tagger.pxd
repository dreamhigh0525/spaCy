from cymem.cymem cimport Pool

from thinc.learner cimport LinearModel
from thinc.features cimport Extractor
from thinc.typedefs cimport atom_t, feat_t, weight_t, class_t

from .typedefs cimport hash_t
from .tokens cimport Tokens


cdef class Tagger:
    cdef class_t predict(self, atom_t* context, object golds=*) except *
 
    cpdef readonly Pool mem
    cpdef readonly Extractor extractor
    cpdef readonly LinearModel model

    cpdef readonly list tag_names
    cdef dict tagdict
