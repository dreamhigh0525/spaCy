# cython: infer_types=True
# coding: utf8
from __future__ import unicode_literals, absolute_import

cimport cython
from libc.string cimport memcpy
from libc.stdint cimport uint64_t, uint32_t
from murmurhash.mrmr cimport hash64, hash32
from preshed.maps cimport map_iter, key_t
from libc.stdint cimport uint32_t
import ujson
import dill

from .symbols import IDS as SYMBOLS_BY_STR
from .symbols import NAMES as SYMBOLS_BY_INT

from .typedefs cimport hash_t
from . import util
from .compat import json_dumps


cpdef hash_t hash_string(unicode string) except 0:
    chars = string.encode('utf8')
    return hash_utf8(chars, len(chars))


cdef hash_t hash_utf8(char* utf8_string, int length) nogil:
    return hash64(utf8_string, length, 1)


cdef uint32_t hash32_utf8(char* utf8_string, int length) nogil:
    return hash32(utf8_string, length, 1)


cdef unicode decode_Utf8Str(const Utf8Str* string):
    cdef int i, length
    if string.s[0] < sizeof(string.s) and string.s[0] != 0:
        return string.s[1:string.s[0]+1].decode('utf8')
    elif string.p[0] < 255:
        return string.p[1:string.p[0]+1].decode('utf8')
    else:
        i = 0
        length = 0
        while string.p[i] == 255:
            i += 1
            length += 255
        length += string.p[i]
        i += 1
        return string.p[i:length + i].decode('utf8')


cdef Utf8Str* _allocate(Pool mem, const unsigned char* chars, uint32_t length) except *:
    cdef int n_length_bytes
    cdef int i
    cdef Utf8Str* string = <Utf8Str*>mem.alloc(1, sizeof(Utf8Str))
    cdef uint32_t ulength = length
    if length < sizeof(string.s):
        string.s[0] = <unsigned char>length
        memcpy(&string.s[1], chars, length)
        return string
    elif length < 255:
        string.p = <unsigned char*>mem.alloc(length + 1, sizeof(unsigned char))
        string.p[0] = length
        memcpy(&string.p[1], chars, length)
        assert string.s[0] >= sizeof(string.s) or string.s[0] == 0, string.s[0]
        return string
    else:
        i = 0
        n_length_bytes = (length // 255) + 1
        string.p = <unsigned char*>mem.alloc(length + n_length_bytes, sizeof(unsigned char))
        for i in range(n_length_bytes-1):
            string.p[i] = 255
        string.p[n_length_bytes-1] = length % 255
        memcpy(&string.p[n_length_bytes], chars, length)
        assert string.s[0] >= sizeof(string.s) or string.s[0] == 0, string.s[0]
        return string


cdef class StringStore:
    """Look up strings by 64-bit hashes."""
    def __init__(self, strings=None, freeze=False):
        """Create the StringStore.

        strings (iterable): A sequence of unicode strings to add to the store.
        RETURNS (StringStore): The newly constructed object.
        """
        self.mem = Pool()
        self._map = PreshMap()
        self._oov = PreshMap()
        self.is_frozen = freeze
        if strings is not None:
            for string in strings:
                self.add(string)

    def __getitem__(self, object string_or_id):
        """Retrieve a string from a given hash, or vice versa.

        string_or_id (bytes, unicode or uint64): The value to encode.
        Returns (unicode or uint64): The value to be retrieved.
        """
        if isinstance(string_or_id, basestring) and len(string_or_id) == 0:
            return 0
        elif string_or_id == 0:
            return u''
        elif string_or_id in SYMBOLS_BY_STR:
            return SYMBOLS_BY_STR[string_or_id]

        cdef hash_t key

        if isinstance(string_or_id, unicode):
            key = hash_string(string_or_id)
            return key
        elif isinstance(string_or_id, bytes):
            key = hash_utf8(string_or_id, len(string_or_id))
            return key
        elif string_or_id < len(SYMBOLS_BY_INT):
            return SYMBOLS_BY_INT[string_or_id]
        else:
            key = string_or_id
            utf8str = <Utf8Str*>self._map.get(key)
            if utf8str is NULL:
                raise KeyError(string_or_id)
            else:
                return decode_Utf8Str(utf8str)

    def add(self, string):
        """Add a string to the StringStore.

        string (unicode): The string to add.
        RETURNS (uint64): The string's hash value.
        """
        if isinstance(string, unicode):
            if string in SYMBOLS_BY_STR:
                return SYMBOLS_BY_STR[string]
            key = hash_string(string)
            self.intern_unicode(string)
        elif isinstance(string, bytes):
            if string in SYMBOLS_BY_STR:
                return SYMBOLS_BY_STR[string]
            key = hash_utf8(string, len(string))
            self._intern_utf8(string, len(string))
        else:
            raise TypeError(
                "Can only add unicode or bytes. Got type: %s" % type(string))
        return key

    def __len__(self):
        """The number of strings in the store.

        RETURNS (int): The number of strings in the store.
        """
        return self.keys.size()

    def __contains__(self, string not None):
        """Check whether a string is in the store.

        string (unicode): The string to check.
        RETURNS (bool): Whether the store contains the string.
        """
        cdef hash_t key
        if isinstance(string, int) or isinstance(string, long):
            if string == 0:
                return True
            key = string
        elif len(string) == 0:
            return True
        elif string in SYMBOLS_BY_STR:
            return True
        elif isinstance(string, unicode):
            key = hash_string(string)
        else:
            string = string.encode('utf8')
            key = hash_utf8(string, len(string))
        if key < len(SYMBOLS_BY_INT):
            return True
        else:
            return self._map.get(key) is not NULL

    def __iter__(self):
        """Iterate over the strings in the store, in order.

        YIELDS (unicode): A string in the store.
        """
        cdef int i
        cdef hash_t key
        for i in range(self.keys.size()):
            key = self.keys[i]
            utf8str = <Utf8Str*>self._map.get(key)
            yield decode_Utf8Str(utf8str)
        # TODO: Iterate OOV here?

    def __reduce__(self):
        strings = list(self)
        return (StringStore, (strings,), None, None, None)

    def to_disk(self, path):
        """Save the current state to a directory.

        path (unicode or Path): A path to a directory, which will be created if
            it doesn't exist. Paths may be either strings or `Path`-like objects.
        """
        path = util.ensure_path(path)
        strings = list(self)
        with path.open('w') as file_:
            file_.write(json_dumps(strings))

    def from_disk(self, path):
        """Loads state from a directory. Modifies the object in place and
        returns it.

        path (unicode or Path): A path to a directory. Paths may be either
            strings or `Path`-like objects.
        RETURNS (StringStore): The modified `StringStore` object.
        """
        path = util.ensure_path(path)
        with path.open('r') as file_:
            strings = ujson.load(file_)
        prev = list(self)
        self._reset_and_load(strings)
        for word in prev:
            self.add(word)
        return self

    def to_bytes(self, **exclude):
        """Serialize the current state to a binary string.

        **exclude: Named attributes to prevent from being serialized.
        RETURNS (bytes): The serialized form of the `StringStore` object.
        """
        return ujson.dumps(list(self))

    def from_bytes(self, bytes_data, **exclude):
        """Load state from a binary string.

        bytes_data (bytes): The data to load from.
        **exclude: Named attributes to prevent from being loaded.
        RETURNS (StringStore): The `StringStore` object.
        """
        strings = ujson.loads(bytes_data)
        prev = list(self)
        self._reset_and_load(strings)
        for word in prev:
            self.add(word)
        return self

    def set_frozen(self, bint is_frozen):
        # TODO
        self.is_frozen = is_frozen

    def flush_oov(self):
        self._oov = PreshMap()

    def _reset_and_load(self, strings, freeze=False):
        self.mem = Pool()
        self._map = PreshMap()
        self._oov = PreshMap()
        self.keys.clear()
        for string in strings:
            self.add(string)
        self.is_frozen = freeze

    cdef const Utf8Str* intern_unicode(self, unicode py_string):
        # 0 means missing, but we don't bother offsetting the index.
        cdef bytes byte_string = py_string.encode('utf8')
        return self._intern_utf8(byte_string, len(byte_string))

    @cython.final
    cdef const Utf8Str* _intern_utf8(self, char* utf8_string, int length):
        # TODO: This function's API/behaviour is an unholy mess...
        # 0 means missing, but we don't bother offsetting the index.
        cdef hash_t key = hash_utf8(utf8_string, length)
        cdef Utf8Str* value = <Utf8Str*>self._map.get(key)
        if value is not NULL:
            return value
        value = <Utf8Str*>self._oov.get(key)
        if value is not NULL:
            return value
        if self.is_frozen:
            # OOV store uses 32 bit hashes. Pretty ugly :(
            key32 = hash32_utf8(utf8_string, length)
            # Important: Make the OOV store own the memory. That way it's trivial
            # to flush them all.
            value = _allocate(self._oov.mem, <unsigned char*>utf8_string, length)
            self._oov.set(key32, value)
            return NULL

        value = _allocate(self.mem, <unsigned char*>utf8_string, length)
        self._map.set(key, value)
        self.keys.push_back(key)
        return value
