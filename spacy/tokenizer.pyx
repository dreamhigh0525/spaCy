# cython: embedsignature=True
# coding: utf8
from __future__ import unicode_literals

from collections import OrderedDict
from cython.operator cimport dereference as deref
from cython.operator cimport preincrement as preinc
from cymem.cymem cimport Pool
from preshed.maps cimport PreshMap
import regex as re

from .strings cimport hash_string
from . import util
cimport cython

from .tokens.doc cimport Doc


cdef class Tokenizer:
    """Segment text, and create Doc objects with the discovered segment
    boundaries.
    """
    def __init__(self, Vocab vocab, rules=None, prefix_search=None,
            suffix_search=None, infix_finditer=None, token_match=None):
        """Create a `Tokenizer`, to create `Doc` objects given unicode text.

        vocab (Vocab): A storage container for lexical types.
        rules (dict): Exceptions and special-cases for the tokenizer.
        prefix_search (callable): A function matching the signature of
            `re.compile(string).search` to match prefixes.
        suffix_search (callable): A function matching the signature of
            `re.compile(string).search` to match suffixes.
        `infix_finditer` (callable): A function matching the signature of
            `re.compile(string).finditer` to find infixes.
        token_match (callable): A boolean function matching strings to be
            recognised as tokens.
        RETURNS (Tokenizer): The newly constructed object.

        EXAMPLE:
            >>> tokenizer = Tokenizer(nlp.vocab)
            >>> tokenizer = English().Defaults.create_tokenizer(nlp)
        """
        self.mem = Pool()
        self._cache = PreshMap()
        self._specials = PreshMap()
        self.token_match = token_match
        self.prefix_search = prefix_search
        self.suffix_search = suffix_search
        self.infix_finditer = infix_finditer
        self.vocab = vocab
        self._rules = {}
        if rules is not None:
            for chunk, substrings in sorted(rules.items()):
                self.add_special_case(chunk, substrings)

    def __reduce__(self):
        args = (self.vocab,
                self._rules,
                self.prefix_search,
                self.suffix_search,
                self.infix_finditer,
                self.token_match)
        return (self.__class__, args, None, None)

    cpdef Doc tokens_from_list(self, list strings):
        # TODO: deprecation warning
        return Doc(self.vocab, words=strings)

    @cython.boundscheck(False)
    def __call__(self, unicode string):
        """Tokenize a string.

        string (unicode): The string to tokenize.
        RETURNS (Doc): A container for linguistic annotations.
        """
        if len(string) >= (2 ** 30):
            raise ValueError(
                "String is too long: %d characters. Max is 2**30." % len(string)
            )
        cdef int length = len(string)
        cdef Doc doc = Doc(self.vocab)
        if length == 0:
            return doc
        cdef int i = 0
        cdef int start = 0
        cdef bint cache_hit
        cdef bint in_ws = string[0].isspace()
        cdef unicode span
        # The task here is much like string.split, but not quite
        # We find spans of whitespace and non-space characters, and ignore
        # spans that are exactly ' '. So, our sequences will all be separated
        # by either ' ' or nothing.
        for uc in string:
            if uc.isspace() != in_ws:
                if start < i:
                    # When we want to make this fast, get the data buffer once
                    # with PyUnicode_AS_DATA, and then maintain a start_byte
                    # and end_byte, so we can call hash64 directly. That way
                    # we don't have to create the slice when we hit the cache.
                    span = string[start:i]
                    key = hash_string(span)
                    cache_hit = self._try_cache(key, doc)
                    if not cache_hit:
                        self._tokenize(doc, span, key)
                if uc == ' ':
                    doc.c[doc.length - 1].spacy = True
                    start = i + 1
                else:
                    start = i
                in_ws = not in_ws
            i += 1
        if start < i:
            span = string[start:]
            key = hash_string(span)
            cache_hit = self._try_cache(key, doc)
            if not cache_hit:
                self._tokenize(doc, span, key)
            doc.c[doc.length - 1].spacy = string[-1] == ' ' and not in_ws
        return doc

    def pipe(self, texts, batch_size=1000, n_threads=2):
        """Tokenize a stream of texts.

        texts: A sequence of unicode texts.
        batch_size (int): The number of texts to accumulate in an internal buffer.
        n_threads (int): The number of threads to use, if the implementation
            supports multi-threading. The default tokenizer is single-threaded.
        YIELDS (Doc): A sequence of Doc objects, in order.
        """
        for text in texts:
            yield self(text)

    cdef int _try_cache(self, hash_t key, Doc tokens) except -1:
        cached = <_Cached*>self._cache.get(key)
        if cached == NULL:
            return False
        cdef int i
        if cached.is_lex:
            for i in range(cached.length):
                tokens.push_back(cached.data.lexemes[i], False)
        else:
            for i in range(cached.length):
                tokens.push_back(&cached.data.tokens[i], False)
        return True

    cdef int _tokenize(self, Doc tokens, unicode span, hash_t orig_key) except -1:
        cdef vector[LexemeC*] prefixes
        cdef vector[LexemeC*] suffixes
        cdef int orig_size
        cdef int has_special
        orig_size = tokens.length
        span = self._split_affixes(tokens.mem, span, &prefixes, &suffixes,
                                   &has_special)
        self._attach_tokens(tokens, span, &prefixes, &suffixes)
        self._save_cached(&tokens.c[orig_size], orig_key, has_special,
                          tokens.length - orig_size)

    cdef unicode _split_affixes(self, Pool mem, unicode string,
                                vector[const LexemeC*] *prefixes,
                                vector[const LexemeC*] *suffixes,
                                int* has_special):
        cdef size_t i
        cdef unicode prefix
        cdef unicode suffix
        cdef unicode minus_pre
        cdef unicode minus_suf
        cdef size_t last_size = 0
        while string and len(string) != last_size:
            if self.token_match and self.token_match(string):
                break
            last_size = len(string)
            pre_len = self.find_prefix(string)
            if pre_len != 0:
                prefix = string[:pre_len]
                minus_pre = string[pre_len:]
                # Check whether we've hit a special-case
                if minus_pre and self._specials.get(hash_string(minus_pre)) != NULL:
                    string = minus_pre
                    prefixes.push_back(self.vocab.get(mem, prefix))
                    has_special[0] = 1
                    break
                if self.token_match and self.token_match(string):
                    break
            suf_len = self.find_suffix(string)
            if suf_len != 0:
                suffix = string[-suf_len:]
                minus_suf = string[:-suf_len]
                # Check whether we've hit a special-case
                if minus_suf and (self._specials.get(hash_string(minus_suf)) != NULL):
                    string = minus_suf
                    suffixes.push_back(self.vocab.get(mem, suffix))
                    has_special[0] = 1
                    break
            if pre_len and suf_len and (pre_len + suf_len) <= len(string):
                string = string[pre_len:-suf_len]
                prefixes.push_back(self.vocab.get(mem, prefix))
                suffixes.push_back(self.vocab.get(mem, suffix))
            elif pre_len:
                string = minus_pre
                prefixes.push_back(self.vocab.get(mem, prefix))
            elif suf_len:
                string = minus_suf
                suffixes.push_back(self.vocab.get(mem, suffix))
            if string and (self._specials.get(hash_string(string)) != NULL):
                has_special[0] = 1
                break
        return string

    cdef int _attach_tokens(self, Doc tokens, unicode string,
                            vector[const LexemeC*] *prefixes,
                            vector[const LexemeC*] *suffixes) except -1:
        cdef bint cache_hit
        cdef int split, end
        cdef const LexemeC* const* lexemes
        cdef const LexemeC* lexeme
        cdef unicode span
        cdef int i
        if prefixes.size():
            for i in range(prefixes.size()):
                tokens.push_back(prefixes[0][i], False)
        if string:
            cache_hit = self._try_cache(hash_string(string), tokens)
            if cache_hit:
                pass
            elif self.token_match and self.token_match(string):
                # We're always saying 'no' to spaces here -- the caller will
                # fix up the outermost one, with reference to the original.
                # See Issue #859
                tokens.push_back(self.vocab.get(tokens.mem, string), False)
            else:
                matches = self.find_infix(string)
                if not matches:
                    tokens.push_back(self.vocab.get(tokens.mem, string), False)
                else:
                    # let's say we have dyn-o-mite-dave
                    # the regex finds the start and end positions of the hyphens
                    start = 0
                    for match in matches:
                        infix_start = match.start()
                        infix_end = match.end()
                        if infix_start == start:
                            continue

                        span = string[start:infix_start]
                        tokens.push_back(self.vocab.get(tokens.mem, span), False)

                        if infix_start != infix_end:
                            # If infix_start != infix_end, it means the infix
                            # token is non-empty. Empty infix tokens are useful
                            # for tokenization in some languages (see
                            # https://github.com/explosion/spaCy/issues/768)
                            infix_span = string[infix_start:infix_end]
                            tokens.push_back(self.vocab.get(tokens.mem, infix_span), False)

                        start = infix_end
                    span = string[start:]
                    if span:
                        tokens.push_back(self.vocab.get(tokens.mem, span), False)
        cdef vector[const LexemeC*].reverse_iterator it = suffixes.rbegin()
        while it != suffixes.rend():
            lexeme = deref(it)
            preinc(it)
            tokens.push_back(lexeme, False)

    cdef int _save_cached(self, const TokenC* tokens, hash_t key,
                          int has_special, int n) except -1:
        cdef int i
        for i in range(n):
            if tokens[i].lex.id == 0:
                return 0
        # See https://github.com/explosion/spaCy/issues/1250
        if has_special:
            return 0
        cached = <_Cached*>self.mem.alloc(1, sizeof(_Cached))
        cached.length = n
        cached.is_lex = True
        lexemes = <const LexemeC**>self.mem.alloc(n, sizeof(LexemeC**))
        for i in range(n):
            lexemes[i] = tokens[i].lex
        cached.data.lexemes = <const LexemeC* const*>lexemes
        self._cache.set(key, cached)

    def find_infix(self, unicode string):
        """Find internal split points of the string, such as hyphens.

        string (unicode): The string to segment.
        RETURNS (list): A list of `re.MatchObject` objects that have `.start()`
            and `.end()` methods, denoting the placement of internal segment
            separators, e.g. hyphens.
        """
        if self.infix_finditer is None:
            return 0
        return list(self.infix_finditer(string))

    def find_prefix(self, unicode string):
        """Find the length of a prefix that should be segmented from the string,
        or None if no prefix rules match.

        string (unicode): The string to segment.
        RETURNS (int): The length of the prefix if present, otherwise `None`.
        """
        if self.prefix_search is None:
            return 0
        match = self.prefix_search(string)
        return (match.end() - match.start()) if match is not None else 0

    def find_suffix(self, unicode string):
        """Find the length of a suffix that should be segmented from the string,
        or None if no suffix rules match.

        string (unicode): The string to segment.
        Returns (int): The length of the suffix if present, otherwise `None`.
        """
        if self.suffix_search is None:
            return 0
        match = self.suffix_search(string)
        return (match.end() - match.start()) if match is not None else 0

    def _load_special_tokenization(self, special_cases):
        """Add special-case tokenization rules."""
        for chunk, substrings in sorted(special_cases.items()):
            self.add_special_case(chunk, substrings)

    def add_special_case(self, unicode string, substrings):
        """Add a special-case tokenization rule.

        string (unicode): The string to specially tokenize.
        token_attrs (iterable): A sequence of dicts, where each dict describes
            a token and its attributes. The `ORTH` fields of the attributes must
            exactly match the string when they are concatenated.
        """
        substrings = list(substrings)
        cached = <_Cached*>self.mem.alloc(1, sizeof(_Cached))
        cached.length = len(substrings)
        cached.is_lex = False
        cached.data.tokens = self.vocab.make_fused_token(substrings)
        key = hash_string(string)
        self._specials.set(key, cached)
        self._cache.set(key, cached)
        self._rules[string] = substrings

    def to_disk(self, path, **exclude):
        """Save the current state to a directory.

        path (unicode or Path): A path to a directory, which will be created if
            it doesn't exist. Paths may be either strings or `Path`-like objects.
        """
        with path.open('wb') as file_:
            file_.write(self.to_bytes(**exclude))

    def from_disk(self, path, **exclude):
        """Loads state from a directory. Modifies the object in place and
        returns it.

        path (unicode or Path): A path to a directory. Paths may be either
            strings or `Path`-like objects.
        RETURNS (Tokenizer): The modified `Tokenizer` object.
        """
        with path.open('rb') as file_:
            bytes_data = file_.read()
        self.from_bytes(bytes_data, **exclude)
        return self

    def to_bytes(self, **exclude):
        """Serialize the current state to a binary string.

        **exclude: Named attributes to prevent from being serialized.
        RETURNS (bytes): The serialized form of the `Tokenizer` object.
        """
        serializers = OrderedDict((
            ('vocab', lambda: self.vocab.to_bytes()),
            ('prefix_search', lambda: self.prefix_search.__self__.pattern),
            ('suffix_search', lambda: self.suffix_search.__self__.pattern),
            ('infix_finditer', lambda: self.infix_finditer.__self__.pattern),
            ('token_match', lambda: self.token_match.__self__.pattern),
            ('exceptions', lambda: OrderedDict(sorted(self._rules.items())))
        ))
        return util.to_bytes(serializers, exclude)

    def from_bytes(self, bytes_data, **exclude):
        """Load state from a binary string.

        bytes_data (bytes): The data to load from.
        **exclude: Named attributes to prevent from being loaded.
        RETURNS (Tokenizer): The `Tokenizer` object.
        """
        data = OrderedDict()
        deserializers = OrderedDict((
            ('vocab', lambda b: self.vocab.from_bytes(b)),
            ('prefix_search', lambda b: data.setdefault('prefix', b)),
            ('suffix_search', lambda b: data.setdefault('suffix_search', b)),
            ('infix_finditer', lambda b: data.setdefault('infix_finditer', b)),
            ('token_match', lambda b: data.setdefault('token_match', b)),
            ('exceptions', lambda b: data.setdefault('rules', b))
        ))
        msg = util.from_bytes(bytes_data, deserializers, exclude)
        if 'prefix_search' in data:
            self.prefix_search = re.compile(data['prefix_search']).search
        if 'suffix_search' in data:
            self.suffix_search = re.compile(data['suffix_search']).search
        if 'infix_finditer' in data:
            self.infix_finditer = re.compile(data['infix_finditer']).finditer
        if 'token_match' in data:
            self.token_match = re.compile(data['token_match']).search
        for string, substrings in data.get('rules', {}).items():
            self.add_special_case(string, substrings)
        return self
