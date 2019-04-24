# cython: infer_types=True
# cython: profile=True
# coding: utf8
from collections import OrderedDict
from cpython.exc cimport PyErr_CheckSignals

from spacy import util
from spacy.errors import Errors, Warnings, user_warning

from cymem.cymem cimport Pool
from preshed.maps cimport PreshMap

from cpython.mem cimport PyMem_Malloc
from cpython.exc cimport PyErr_SetFromErrno

from libc.stdio cimport FILE, fopen, fclose, fread, fwrite, feof, fseek
from libc.stdint cimport int32_t, int64_t
from libc.stdlib cimport qsort

from .typedefs cimport hash_t

from os import path
from libcpp.vector cimport vector



cdef class Candidate:

    def __init__(self, KnowledgeBase kb, entity_hash, alias_hash, prior_prob):
        self.kb = kb
        self.entity_hash = entity_hash
        self.alias_hash = alias_hash
        self.prior_prob = prior_prob

    @property
    def entity(self):
        """RETURNS (uint64): hash of the entity's KB ID/name"""
        return self.entity_hash

    @property
    def entity_(self):
        """RETURNS (unicode): ID/name of this entity in the KB"""
        return self.kb.vocab.strings[self.entity_hash]

    @property
    def alias(self):
        """RETURNS (uint64): hash of the alias"""
        return self.alias_hash

    @property
    def alias_(self):
        """RETURNS (unicode): ID of the original alias"""
        return self.kb.vocab.strings[self.alias_hash]

    @property
    def prior_prob(self):
        return self.prior_prob


cdef class KnowledgeBase:
    def __init__(self, Vocab vocab):
        self.vocab = vocab
        self.mem = Pool()
        self._entry_index = PreshMap()
        self._alias_index = PreshMap()

        # TODO initialize self._entries and self._aliases_table ?

        self.vocab.strings.add("")
        self._create_empty_vectors(dummy_hash=self.vocab.strings[""])

    def __len__(self):
        return self.get_size_entities()

    def get_size_entities(self):
        return len(self._entry_index)

    def get_entity_strings(self):
        return [self.vocab.strings[x] for x in self._entry_index][1:] # removing the dummy element on index 0

    def get_size_aliases(self):
        return len(self._alias_index)

    def get_alias_strings(self):
        return [self.vocab.strings[x] for x in self._alias_index][1:] # removing the dummy element on index 0

    def add_entity(self, unicode entity, float prob=0.5, vectors=None, features=None):
        """
        Add an entity to the KB, optionally specifying its log probability based on corpus frequency
        Return the hash of the entity ID/name at the end
        """
        cdef hash_t entity_hash = self.vocab.strings.add(entity)

        # Return if this entity was added before
        if entity_hash in self._entry_index:
            user_warning(Warnings.W018.format(entity=entity))
            return

        cdef int32_t dummy_value = 342
        new_index = self.c_add_entity(entity_hash=entity_hash, prob=prob,
                                      vector_rows=&dummy_value, feats_row=dummy_value)
        self._entry_index[entity_hash] = new_index

        # TODO self._vectors_table.get_pointer(vectors),
        # self._features_table.get(features))

        return entity_hash

    def add_alias(self, unicode alias, entities, probabilities):
        """
        For a given alias, add its potential entities and prior probabilies to the KB.
        Return the alias_hash at the end
        """

        # Throw an error if the length of entities and probabilities are not the same
        if not len(entities) == len(probabilities):
            raise ValueError(Errors.E132.format(alias=alias,
                                                entities_length=len(entities),
                                                probabilities_length=len(probabilities)))

        # Throw an error if the probabilities sum up to more than 1
        prob_sum = sum(probabilities)
        if prob_sum > 1:
            raise ValueError(Errors.E133.format(alias=alias, sum=prob_sum))

        cdef hash_t alias_hash = self.vocab.strings.add(alias)

        # Return if this alias was added before
        if alias_hash in self._alias_index:
            user_warning(Warnings.W017.format(alias=alias))
            return

        cdef vector[int64_t] entry_indices
        cdef vector[float] probs

        for entity, prob in zip(entities, probabilities):
            entity_hash = self.vocab.strings[entity]
            if not entity_hash in self._entry_index:
                raise ValueError(Errors.E134.format(alias=alias, entity=entity))

            entry_index = <int64_t>self._entry_index.get(entity_hash)
            entry_indices.push_back(int(entry_index))
            probs.push_back(float(prob))

        new_index = self.c_add_aliases(alias_hash=alias_hash, entry_indices=entry_indices, probs=probs)
        self._alias_index[alias_hash] = new_index

        return alias_hash


    def get_candidates(self, unicode alias):
        """ TODO: where to put this functionality ?"""
        cdef hash_t alias_hash = self.vocab.strings[alias]
        alias_index = <int64_t>self._alias_index.get(alias_hash)
        alias_entry = self._aliases_table[alias_index]

        return [Candidate(kb=self,
                          entity_hash=self._entries[entry_index].entity_hash,
                          alias_hash=alias_hash,
                          prior_prob=prob)
                for (entry_index, prob) in zip(alias_entry.entry_indices, alias_entry.probs)
                if entry_index != 0]


    def dump(self, loc):
        cdef Writer writer = Writer(loc)
        writer.write_header(self.get_size_entities())

        # dumping the entry records in the order in which they are in the _entries vector.
        # index 0 is a dummy object not stored in the _entry_index and can be ignored.
        i = 1
        for entry_hash, entry_index in sorted(self._entry_index.items(), key=lambda x: x[1]):
            entry = self._entries[entry_index]
            assert entry.entity_hash ==  entry_hash
            assert entry_index == i
            writer.write_entry(entry_index, entry.entity_hash, entry.prob)
            i = i+1

        writer.close()

    cpdef load_bulk(self, loc):
        cdef int64_t entry_id
        cdef hash_t entity_hash
        cdef float prob
        cdef EntryC entry
        cdef int32_t dummy_value = 342

        cdef Reader reader = Reader(loc)
        cdef int64_t nr_entities
        reader.read_header(&nr_entities)

        self._entry_index = PreshMap(nr_entities+1)
        self._entries = entry_vec(nr_entities+1)

        # we assume the data was written in sequence
        # index 0 is a dummy object not stored in the _entry_index and can be ignored.
        # TODO: should we initialize the dummy objects ?
        cdef int i = 1
        while reader.read_entry(&entry_id, &entity_hash, &prob) and i <= nr_entities:
            assert i == entry_id

            # TODO features and vectors
            entry.entity_hash = entity_hash
            entry.prob = prob
            entry.vector_rows = &dummy_value
            entry.feats_row = dummy_value

            self._entries[i] = entry
            self._entry_index[entity_hash] = i

            i += 1


cdef class Writer:
    def __init__(self, object loc):
        if path.exists(loc):
            assert not path.isdir(loc), "%s is directory." % loc
        cdef bytes bytes_loc = loc.encode('utf8') if type(loc) == unicode else loc
        self._fp = fopen(<char*>bytes_loc, 'wb')
        assert self._fp != NULL
        fseek(self._fp, 0, 0)

    def close(self):
        cdef size_t status = fclose(self._fp)
        assert status == 0

    cdef int write_header(self, int64_t nr_entries) except -1:
        self._write(&nr_entries, sizeof(nr_entries))

    cdef int write_entry(self, int64_t entry_id, hash_t entry_hash, float entry_prob) except -1:
        # TODO: feats_rows and vector rows
        self._write(&entry_id, sizeof(entry_id))
        self._write(&entry_hash, sizeof(entry_hash))
        self._write(&entry_prob, sizeof(entry_prob))

    cdef int _write(self, void* value, size_t size) except -1:
        status = fwrite(value, size, 1, self._fp)
        assert status == 1, status


cdef class Reader:
    def __init__(self, object loc):
        assert path.exists(loc)
        assert not path.isdir(loc)
        cdef bytes bytes_loc = loc.encode('utf8') if type(loc) == unicode else loc
        self._fp = fopen(<char*>bytes_loc, 'rb')
        if not self._fp:
            PyErr_SetFromErrno(IOError)
        status = fseek(self._fp, 0, 0)  # this can be 0 if there is no header

    def __dealloc__(self):
        fclose(self._fp)

    cdef int read_header(self, int64_t* nr_entries) except -1:
        status = self._read(nr_entries, sizeof(int64_t))
        if status < 1:
            if feof(self._fp):
                return 0  # end of file
            raise IOError("error reading header from input file")

    cdef int read_entry(self, int64_t* entry_id, hash_t* entity_hash, float* prob) except -1:
        status = self._read(entry_id, sizeof(int64_t))
        if status < 1:
            if feof(self._fp):
                return 0  # end of file
            raise IOError("error reading entry ID from input file")

        status = self._read(entity_hash, sizeof(hash_t))
        if status < 1:
            if feof(self._fp):
                return 0  # end of file
            raise IOError("error reading entity hash from input file")

        status = self._read(prob, sizeof(float))
        if status < 1:
            if feof(self._fp):
                return 0  # end of file
            raise IOError("error reading entity prob from input file")

        if feof(self._fp):
            return 0
        else:
            return 1

    cdef int _read(self, void* value, size_t size) except -1:
        status = fread(value, size, 1, self._fp)
        return status


