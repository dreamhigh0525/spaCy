# cython: profile=True
# cython: infer_types=True
# coding: utf8
from __future__ import unicode_literals

import ujson
from cymem.cymem cimport Pool
from preshed.maps cimport PreshMap
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from cython.operator cimport dereference as deref
from murmurhash.mrmr cimport hash64
from libc.stdint cimport int32_t

# try:
#     from libcpp.unordered_map cimport unordered_map as umap
# except:
#     from libcpp.map cimport map as umap

from .typedefs cimport attr_t
from .typedefs cimport hash_t
from .structs cimport TokenC
from .tokens.doc cimport Doc, get_token_attr
from .vocab cimport Vocab

from .attrs import IDS
from .attrs cimport attr_id_t, ID, NULL_ATTR
from .attrs import FLAG61 as U_ENT
from .attrs import FLAG60 as B2_ENT
from .attrs import FLAG59 as B3_ENT
from .attrs import FLAG58 as B4_ENT
from .attrs import FLAG57 as B5_ENT
from .attrs import FLAG56 as B6_ENT
from .attrs import FLAG55 as B7_ENT
from .attrs import FLAG54 as B8_ENT
from .attrs import FLAG53 as B9_ENT
from .attrs import FLAG52 as B10_ENT
from .attrs import FLAG51 as I3_ENT
from .attrs import FLAG50 as I4_ENT
from .attrs import FLAG49 as I5_ENT
from .attrs import FLAG48 as I6_ENT
from .attrs import FLAG47 as I7_ENT
from .attrs import FLAG46 as I8_ENT
from .attrs import FLAG45 as I9_ENT
from .attrs import FLAG44 as I10_ENT
from .attrs import FLAG43 as L2_ENT
from .attrs import FLAG42 as L3_ENT
from .attrs import FLAG41 as L4_ENT
from .attrs import FLAG40 as L5_ENT
from .attrs import FLAG39 as L6_ENT
from .attrs import FLAG38 as L7_ENT
from .attrs import FLAG37 as L8_ENT
from .attrs import FLAG36 as L9_ENT
from .attrs import FLAG35 as L10_ENT


cpdef enum quantifier_t:
    _META
    ONE
    ZERO
    ZERO_ONE
    ZERO_PLUS


cdef enum action_t:
    REJECT
    ADVANCE
    REPEAT
    ACCEPT
    ADVANCE_ZERO
    ADVANCE_PLUS
    ACCEPT_PREV
    PANIC


# Each token pattern consists of a quantifier and 0+ (attr, value) pairs.
# A state is an (int, pattern pointer) pair, where the int is the start
# position, and the pattern pointer shows where we're up to
# in the pattern.

cdef struct AttrValueC:
    attr_id_t attr
    attr_t value


cdef struct TokenPatternC:
    AttrValueC* attrs
    int32_t nr_attr
    quantifier_t quantifier


ctypedef TokenPatternC* TokenPatternC_ptr
# ctypedef pair[int, TokenPatternC_ptr] StateC

# Match Dictionary entry type
cdef struct MatchEntryC:
    int32_t start
    int32_t end
    int32_t offset

# A state instance represents the information that defines a 
# partial match
# start: the index of the first token in the partial match
# pattern: a pointer to the current token pattern in the full
#       pattern
# last_match: The entry of the last span matched by the
#       same pattern
cdef struct StateC:
    int32_t start
    TokenPatternC_ptr pattern
    MatchEntryC* last_match


cdef TokenPatternC* init_pattern(Pool mem, attr_t entity_id,
                                 object token_specs) except NULL:
    pattern = <TokenPatternC*>mem.alloc(len(token_specs) + 1, sizeof(TokenPatternC))
    cdef int i
    for i, (quantifier, spec) in enumerate(token_specs):
        pattern[i].quantifier = quantifier
        pattern[i].attrs = <AttrValueC*>mem.alloc(len(spec), sizeof(AttrValueC))
        pattern[i].nr_attr = len(spec)
        for j, (attr, value) in enumerate(spec):
            pattern[i].attrs[j].attr = attr
            pattern[i].attrs[j].value = value
    i = len(token_specs)
    pattern[i].attrs = <AttrValueC*>mem.alloc(2, sizeof(AttrValueC))
    pattern[i].attrs[0].attr = ID
    pattern[i].attrs[0].value = entity_id
    pattern[i].nr_attr = 0
    return pattern


cdef attr_t get_pattern_key(const TokenPatternC* pattern) except 0:
    while pattern.nr_attr != 0:
        pattern += 1
    id_attr = pattern[0].attrs[0]
    assert id_attr.attr == ID
    return id_attr.value


cdef int get_action(const TokenPatternC* pattern, const TokenC* token) nogil:
    lookahead = &pattern[1]
    for attr in pattern.attrs[:pattern.nr_attr]:
        if get_token_attr(token, attr.attr) != attr.value:
            if pattern.quantifier == ONE:
                return REJECT
            elif pattern.quantifier == ZERO:
                return ACCEPT if lookahead.nr_attr == 0 else ADVANCE
            elif pattern.quantifier in (ZERO_ONE, ZERO_PLUS):
                return ACCEPT_PREV if lookahead.nr_attr == 0 else ADVANCE_ZERO
            else:
                return PANIC
    if pattern.quantifier == ZERO:
        return REJECT
    elif lookahead.nr_attr == 0:
        if pattern.quantifier == ZERO_PLUS:
            return REPEAT
        else:
            return ACCEPT
    elif pattern.quantifier in (ONE, ZERO_ONE):
        return ADVANCE
    elif pattern.quantifier == ZERO_PLUS:
        # This is a bandaid over the 'shadowing' problem described here:
        # https://github.com/explosion/spaCy/issues/864
        next_action = get_action(lookahead, token)
        if next_action is REJECT:
            return REPEAT
        else:
            return ADVANCE_PLUS
    else:
        return PANIC


def _convert_strings(token_specs, string_store):
    # Support 'syntactic sugar' operator '+', as combination of ONE, ZERO_PLUS
    operators = {'!': (ZERO,), '*': (ZERO_PLUS,), '+': (ONE, ZERO_PLUS),
                 '?': (ZERO_ONE,), '1': (ONE,)}
    tokens = []
    op = ONE
    for spec in token_specs:
        if not spec:
            # Signifier for 'any token'
            tokens.append((ONE, [(NULL_ATTR, 0)]))
            continue
        token = []
        ops = (ONE,)
        for attr, value in spec.items():
            if isinstance(attr, basestring) and attr.upper() == 'OP':
                if value in operators:
                    ops = operators[value]
                else:
                    msg = "Unknown operator '%s'. Options: %s"
                    raise KeyError(msg % (value, ', '.join(operators.keys())))
            if isinstance(attr, basestring):
                attr = IDS.get(attr.upper())
            if isinstance(value, basestring):
                value = string_store.add(value)
            if isinstance(value, bool):
                value = int(value)
            if attr is not None:
                token.append((attr, value))
        for op in ops:
            tokens.append((op, token))
    return tokens


def merge_phrase(matcher, doc, i, matches):
    """Callback to merge a phrase on match."""
    ent_id, label, start, end = matches[i]
    span = doc[start:end]
    span.merge(ent_type=label, ent_id=ent_id)


def unpickle_matcher(vocab, patterns, callbacks):
    matcher = Matcher(vocab)
    for key, specs in patterns.items():
        callback = callbacks.get(key, None)
        matcher.add(key, callback, *specs)
    return matcher


cdef class Matcher:
    """Match sequences of tokens, based on pattern rules."""
    cdef Pool mem
    cdef vector[TokenPatternC*] patterns
    cdef readonly Vocab vocab
    cdef public object _patterns
    cdef public object _entities
    cdef public object _callbacks

    def __init__(self, vocab):
        """Create the Matcher.

        vocab (Vocab): The vocabulary object, which must be shared with the
            documents the matcher will operate on.
        RETURNS (Matcher): The newly constructed object.
        """
        self._patterns = {}
        self._entities = {}
        self._callbacks = {}
        self.vocab = vocab
        self.mem = Pool()

    def __reduce__(self):
        data = (self.vocab, self._patterns, self._callbacks)
        return (unpickle_matcher, data, None, None)

    def __len__(self):
        """Get the number of rules added to the matcher. Note that this only
        returns the number of rules (identical with the number of IDs), not the
        number of individual patterns.

        RETURNS (int): The number of rules.
        """
        return len(self._patterns)

    def __contains__(self, key):
        """Check whether the matcher contains rules for a match ID.

        key (unicode): The match ID.
        RETURNS (bool): Whether the matcher contains rules for this match ID.
        """
        return self._normalize_key(key) in self._patterns

    def add(self, key, on_match, *patterns):
        """Add a match-rule to the matcher. A match-rule consists of: an ID
        key, an on_match callback, and one or more patterns.

        If the key exists, the patterns are appended to the previous ones, and
        the previous on_match callback is replaced. The `on_match` callback
        will receive the arguments `(matcher, doc, i, matches)`. You can also
        set `on_match` to `None` to not perform any actions.

        A pattern consists of one or more `token_specs`, where a `token_spec`
        is a dictionary mapping attribute IDs to values, and optionally a
        quantifier operator under the key "op". The available quantifiers are:

        '!': Negate the pattern, by requiring it to match exactly 0 times.
        '?': Make the pattern optional, by allowing it to match 0 or 1 times.
        '+': Require the pattern to match 1 or more times.
        '*': Allow the pattern to zero or more times.

        The + and * operators are usually interpretted "greedily", i.e. longer
        matches are returned where possible. However, if you specify two '+'
        and '*' patterns in a row and their matches overlap, the first
        operator will behave non-greedily. This quirk in the semantics makes
        the matcher more efficient, by avoiding the need for back-tracking.

        key (unicode): The match ID.
        on_match (callable): Callback executed on match.
        *patterns (list): List of token descritions.
        """
        for pattern in patterns:
            if len(pattern) == 0:
                msg = ("Cannot add pattern for zero tokens to matcher.\n"
                       "key: {key}\n")
                raise ValueError(msg.format(key=key))
        key = self._normalize_key(key)
        for pattern in patterns:
            specs = _convert_strings(pattern, self.vocab.strings)
            self.patterns.push_back(init_pattern(self.mem, key, specs))
        self._patterns.setdefault(key, [])
        self._callbacks[key] = on_match
        self._patterns[key].extend(patterns)

    def remove(self, key):
        """Remove a rule from the matcher. A KeyError is raised if the key does
        not exist.

        key (unicode): The ID of the match rule.
        """
        key = self._normalize_key(key)
        self._patterns.pop(key)
        self._callbacks.pop(key)
        cdef int i = 0
        while i < self.patterns.size():
            pattern_key = get_pattern_key(self.patterns.at(i))
            if pattern_key == key:
                self.patterns.erase(self.patterns.begin()+i)
            else:
                i += 1

    def has_key(self, key):
        """Check whether the matcher has a rule with a given key.

        key (string or int): The key to check.
        RETURNS (bool): Whether the matcher has the rule.
        """
        key = self._normalize_key(key)
        return key in self._patterns

    def get(self, key, default=None):
        """Retrieve the pattern stored for a key.

        key (unicode or int): The key to retrieve.
        RETURNS (tuple): The rule, as an (on_match, patterns) tuple.
        """
        key = self._normalize_key(key)
        if key not in self._patterns:
            return default
        return (self._callbacks[key], self._patterns[key])

    def pipe(self, docs, batch_size=1000, n_threads=2):
        """Match a stream of documents, yielding them in turn.

        docs (iterable): A stream of documents.
        batch_size (int): Number of documents to accumulate into a working set.
        n_threads (int): The number of threads with which to work on the buffer
            in parallel, if the implementation supports multi-threading.
        YIELDS (Doc): Documents, in order.
        """
        for doc in docs:
            self(doc)
            yield doc

    def __call__(self, Doc doc):
        """Find all token sequences matching the supplied pattern.

        doc (Doc): The document to match over.
        RETURNS (list): A list of `(key, start, end)` tuples,
            describing the matches. A match tuple describes a span
            `doc[start:end]`. The `label_id` and `key` are both integers.
        """
        cdef vector[StateC] partials
        cdef int n_partials = 0
        cdef int q = 0
        cdef int i, token_i
        cdef const TokenC* token
        cdef StateC state
        cdef int j = 0
        cdef int k
        cdef bint overlap = False
        cdef MatchEntryC* state_match 
        cdef MatchEntryC* last_matches = <MatchEntryC*>self.mem.alloc(self.patterns.size(),sizeof(MatchEntryC))

        for i in range(self.patterns.size()):
            last_matches[i].start = 0
            last_matches[i].end = 0
            last_matches[i].offset = 0

        matches = []
        for token_i in range(doc.length):
            token = &doc.c[token_i]
            q = 0
            # Go over the open matches, extending or finalizing if able.
            # Otherwise, we over-write them (q doesn't advance)
            #for state in partials:
            j=0
            while j < n_partials:
                state = partials[j]
                action = get_action(state.pattern, token)
                j += 1
                # Skip patterns that would overlap with an existing match
                # Patterns overlap an existing match if they point to the
                # same final state and start between the start and end
                # of said match.
                # Different patterns with the same label are allowed to 
                # overlap.
                state_match = state.last_match
                if (state.start > state_match.start 
                    and state.start < state_match.end):
                    continue
                if action == PANIC:
                    raise Exception("Error selecting action in matcher")
                while action == ADVANCE_ZERO:
                    state.pattern += 1
                    action = get_action(state.pattern, token)
                if action == PANIC:
                    raise Exception("Error selecting action in matcher")
                
                # ADVANCE_PLUS acts like REPEAT, but also pushes a partial that
                # acts like and ADVANCE_ZERO
                if action == ADVANCE_PLUS:
                    state.pattern += 1
                    partials.push_back(state)
                    n_partials += 1
                    state.pattern -= 1
                    action = REPEAT

                if action == ADVANCE:
                    state.pattern += 1

                # Check for partial matches that are at the same spec in the same pattern
                # Keep the longer of the matches
                # This ensures that there are never more then 2 partials for every spec
                # in a pattern (one of which gets pruned in this step)

                overlap=False
                for i in range(q):
                    if state.pattern == partials[i].pattern and state.start < partials[i].start:
                        partials[i] = state
                        j = i
                        overlap = True
                        break
                if overlap:
                    continue
                overlap=False
                for i in range(q):
                    if state.pattern == partials[i].pattern:
                        overlap = True
                        break
                if overlap:
                    continue

    
                if action == REPEAT:
                    # Leave the state in the queue, and advance to next slot
                    # (i.e. we don't overwrite -- we want to greedily match
                    # more pattern.
                    partials[q] = state
                    q += 1
                elif action == REJECT:
                    pass
                elif action == ADVANCE:
                    partials[q] = state
                    q += 1
                elif action in (ACCEPT, ACCEPT_PREV):
                    # TODO: What to do about patterns starting with ZERO? Need
                    # to adjust the start position.
                    start = state.start
                    end = token_i+1 if action == ACCEPT else token_i
                    ent_id = state.pattern[1].attrs[0].value
                    label = state.pattern[1].attrs[1].value
                    # Check that this match doesn't overlap with an earlier match.
                    # Only overwrite an earlier match if it is a substring of this
                    # match (i.e. it starts after this match starts).
                    state_match = state.last_match

                    if start >= state_match.end:
                        state_match.start = start
                        state_match.end = end
                        state_match.offset = len(matches)
                        matches.append((ent_id,start,end))
                    elif start <= state_match.start and end >= state_match.end:
                        if len(matches) == 0:
                            assert state_match.offset==0
                            state_match.offset = 0
                            matches.append((ent_id,start,end))
                        else:
                            i = state_match.offset
                            matches[i] = (ent_id,start,end)
                        state_match.start = start
                        state_match.end = end
                    else:
                        pass

            partials.resize(q)
            n_partials = q
            # Check whether we open any new patterns on this token
            i=0
            for pattern in self.patterns:
                # Skip patterns that would overlap with an existing match
                # state_match = pattern.last_match
                state_match = &last_matches[i]
                i+=1
                if (token_i > state_match.start 
                    and token_i < state_match.end):
                    continue
                action = get_action(pattern, token)
                if action == PANIC:
                    raise Exception("Error selecting action in matcher")
                while action in (ADVANCE_PLUS,ADVANCE_ZERO):
                    if action == ADVANCE_PLUS:
                        state.start = token_i
                        state.pattern = pattern
                        state.last_match = state_match
                        partials.push_back(state)
                        n_partials += 1
                    pattern += 1
                    action = get_action(pattern, token)

                if action == ADVANCE:
                    pattern += 1
                j=0
                overlap = False
                for j in range(q):
                    if pattern == partials[j].pattern:
                        overlap = True
                        break
                if overlap:
                    continue


                if action == REPEAT:
                    state.start = token_i
                    state.pattern = pattern
                    state.last_match = state_match
                    partials.push_back(state)
                    n_partials += 1
                elif action == ADVANCE:
                    # TODO: What to do about patterns starting with ZERO? Need
                    # to adjust the start position.
                    state.start = token_i
                    state.pattern = pattern
                    state.last_match = state_match
                    partials.push_back(state)
                    n_partials += 1
                elif action in (ACCEPT, ACCEPT_PREV):
                    start = token_i
                    end = token_i+1 if action == ACCEPT else token_i
                    ent_id = pattern[1].attrs[0].value

                    label = pattern[1].attrs[1].value
                    if start >= state_match.end:
                        state_match.start = start
                        state_match.end = end
                        state_match.offset = len(matches)
                        matches.append((ent_id,start,end))
                    if start <= state_match.start and end >= state_match.end:
                        if len(matches) == 0:
                            state_match.offset = 0
                            matches.append((ent_id,start,end))
                        else:
                            j = state_match.offset
                            matches[j] = (ent_id,start,end)
                        state_match.start = start
                        state_match.end = end
                    else:
                        pass

        # Look for open patterns that are actually satisfied
        for state in partials:
            while state.pattern.quantifier in (ZERO, ZERO_ONE, ZERO_PLUS):
                state.pattern += 1
                if state.pattern.nr_attr == 0:
                    start = state.start
                    end = len(doc)
                    ent_id = state.pattern.attrs[0].value
                    label = state.pattern.attrs[1].value
                    state_match = state.last_match
                    if start >= state_match.end:
                        state_match.start = start
                        state_match.end = end
                        state_match.offset = len(matches)
                        matches.append((ent_id,start,end))
                    if start <= state_match.start and end >= state_match.end:
                        j = state_match.offset
                        if len(matches) == 0:
                            state_match.offset = 0
                            matches.append((ent_id,start,end))
                        else:
                            matches[j] = (ent_id,start,end)
                        state_match.start = start
                        state_match.end = end
                    else:
                        pass
        for i, (ent_id, start, end) in enumerate(matches):
            on_match = self._callbacks.get(ent_id)
            if on_match is not None:
                on_match(self, doc, i, matches)
        return matches

    def _normalize_key(self, key):
        if isinstance(key, basestring):
            return self.vocab.strings.add(key)
        else:
            return key


def get_bilou(length):
    if length == 1:
        return [U_ENT]
    elif length == 2:
        return [B2_ENT, L2_ENT]
    elif length == 3:
        return [B3_ENT, I3_ENT, L3_ENT]
    elif length == 4:
        return [B4_ENT, I4_ENT, I4_ENT, L4_ENT]
    elif length == 5:
        return [B5_ENT, I5_ENT, I5_ENT, I5_ENT, L5_ENT]
    elif length == 6:
        return [B6_ENT, I6_ENT, I6_ENT, I6_ENT, I6_ENT, L6_ENT]
    elif length == 7:
        return [B7_ENT, I7_ENT, I7_ENT, I7_ENT, I7_ENT, I7_ENT, L7_ENT]
    elif length == 8:
        return [B8_ENT, I8_ENT, I8_ENT, I8_ENT, I8_ENT, I8_ENT, I8_ENT, L8_ENT]
    elif length == 9:
        return [B9_ENT, I9_ENT, I9_ENT, I9_ENT, I9_ENT, I9_ENT, I9_ENT, I9_ENT,
                L9_ENT]
    elif length == 10:
        return [B10_ENT, I10_ENT, I10_ENT, I10_ENT, I10_ENT, I10_ENT, I10_ENT,
                I10_ENT, I10_ENT, L10_ENT]
    else:
        raise ValueError("Max length currently 10 for phrase matching")


cdef class PhraseMatcher:
    cdef Pool mem
    cdef Vocab vocab
    cdef Matcher matcher
    cdef PreshMap phrase_ids
    cdef int max_length
    cdef attr_t* _phrase_key
    cdef public object _callbacks
    cdef public object _patterns

    def __init__(self, Vocab vocab, max_length=10):
        self.mem = Pool()
        self._phrase_key = <attr_t*>self.mem.alloc(max_length, sizeof(attr_t))
        self.max_length = max_length
        self.vocab = vocab
        self.matcher = Matcher(self.vocab)
        self.phrase_ids = PreshMap()
        abstract_patterns = []
        for length in range(1, max_length):
            abstract_patterns.append([{tag: True}
                                      for tag in get_bilou(length)])
        self.matcher.add('Candidate', None, *abstract_patterns)
        self._callbacks = {}

    def __len__(self):
        """Get the number of rules added to the matcher. Note that this only
        returns the number of rules (identical with the number of IDs), not the
        number of individual patterns.

        RETURNS (int): The number of rules.
        """
        return len(self.phrase_ids)

    def __contains__(self, key):
        """Check whether the matcher contains rules for a match ID.

        key (unicode): The match ID.
        RETURNS (bool): Whether the matcher contains rules for this match ID.
        """
        cdef hash_t ent_id = self.matcher._normalize_key(key)
        return ent_id in self._callbacks

    def __reduce__(self):
        return (self.__class__, (self.vocab,), None, None)

    def add(self, key, on_match, *docs):
        """Add a match-rule to the matcher. A match-rule consists of: an ID
        key, an on_match callback, and one or more patterns.

        key (unicode): The match ID.
        on_match (callable): Callback executed on match.
        *docs (Doc): `Doc` objects representing match patterns.
        """
        cdef Doc doc
        for doc in docs:
            if len(doc) >= self.max_length:
                msg = (
                    "Pattern length (%d) >= phrase_matcher.max_length (%d). "
                    "Length can be set on initialization, up to 10."
                )
                raise ValueError(msg % (len(doc), self.max_length))
        cdef hash_t ent_id = self.matcher._normalize_key(key)
        self._callbacks[ent_id] = on_match
        cdef int length
        cdef int i
        cdef hash_t phrase_hash
        for doc in docs:
            length = doc.length
            tags = get_bilou(length)
            for i in range(self.max_length):
                self._phrase_key[i] = 0
            for i, tag in enumerate(tags):
                lexeme = self.vocab[doc.c[i].lex.orth]
                lexeme.set_flag(tag, True)
                self._phrase_key[i] = lexeme.orth
            phrase_hash = hash64(self._phrase_key,
                                 self.max_length * sizeof(attr_t), 0)
            self.phrase_ids.set(phrase_hash, <void*>ent_id)

    def __call__(self, Doc doc):
        """Find all sequences matching the supplied patterns on the `Doc`.

        doc (Doc): The document to match over.
        RETURNS (list): A list of `(key, start, end)` tuples,
            describing the matches. A match tuple describes a span
            `doc[start:end]`. The `label_id` and `key` are both integers.
        """
        matches = []
        for _, start, end in self.matcher(doc):
            ent_id = self.accept_match(doc, start, end)
            if ent_id is not None:
                matches.append((ent_id, start, end))
        for i, (ent_id, start, end) in enumerate(matches):
            on_match = self._callbacks.get(ent_id)
            if on_match is not None:
                on_match(self, doc, i, matches)
        return matches

    def pipe(self, stream, batch_size=1000, n_threads=2):
        """Match a stream of documents, yielding them in turn.

        docs (iterable): A stream of documents.
        batch_size (int): Number of documents to accumulate into a working set.
        n_threads (int): The number of threads with which to work on the buffer
            in parallel, if the implementation supports multi-threading.
        YIELDS (Doc): Documents, in order.
        """
        for doc in stream:
            self(doc)
            yield doc

    def accept_match(self, Doc doc, int start, int end):
        assert (end - start) < self.max_length
        cdef int i, j
        for i in range(self.max_length):
            self._phrase_key[i] = 0
        for i, j in enumerate(range(start, end)):
            self._phrase_key[i] = doc.c[j].lex.orth
        cdef hash_t key = hash64(self._phrase_key,
                                 self.max_length * sizeof(attr_t), 0)
        ent_id = <hash_t>self.phrase_ids.get(key)
        if ent_id == 0:
            return None
        else:
            return ent_id
