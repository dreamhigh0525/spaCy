from os import path
import io
import json
import re
from .attrs import TAG, HEAD, DEP, ENT_IOB, ENT_TYPE

DATA_DIR = path.join(path.dirname(__file__), '..', 'data')


def normalize_slice(length, start, stop, step=None):
    if not (step is None or step == 1):
        raise ValueError("Stepped slices not supported in Span objects."
                         "Try: list(tokens)[start:stop:step] instead.")
    if start is None:
       start = 0
    elif start < 0:
       start += length
    start = min(length, max(0, start))

    if stop is None:
       stop = length
    elif stop < 0:
       stop += length
    stop = min(length, max(start, stop))

    assert 0 <= start <= stop <= length
    return start, stop


def utf8open(loc, mode='r'):
    return io.open(loc, mode, encoding='utf8')


def read_lang_data(data_dir):
    with open(path.join(data_dir, 'specials.json')) as file_:
        tokenization = json.load(file_)
    prefix = read_prefix(data_dir)
    suffix = read_suffix(data_dir)
    infix = read_infix(data_dir)
    return tokenization, prefix, suffix, infix


def read_prefix(data_dir):
    with  utf8open(path.join(data_dir, 'prefix.txt')) as file_:
        entries = file_.read().split('\n')
        expression = '|'.join(['^' + re.escape(piece) for piece in entries if piece.strip()])
    return expression


def read_suffix(data_dir):
    with utf8open(path.join(data_dir, 'suffix.txt')) as file_:
        entries = file_.read().split('\n')
        expression = '|'.join([piece + '$' for piece in entries if piece.strip()])
    return expression


def read_infix(data_dir):
    with utf8open(path.join(data_dir, 'infix.txt')) as file_:
        entries = file_.read().split('\n')
        expression = '|'.join([piece for piece in entries if piece.strip()])
    return expression


def read_tokenization(lang):
    loc = path.join(DATA_DIR, lang, 'tokenization')
    entries = []
    seen = set()
    with utf8open(loc) as file_:
        for line in file_:
            line = line.strip()
            if line.startswith('#'):
                continue
            if not line:
                continue
            pieces = line.split()
            chunk = pieces.pop(0)
            assert chunk not in seen, chunk
            seen.add(chunk)
            entries.append((chunk, list(pieces)))
            if chunk[0].isalpha() and chunk[0].islower():
                chunk = chunk[0].title() + chunk[1:]
                pieces[0] = pieces[0][0].title() + pieces[0][1:]
                seen.add(chunk)
                entries.append((chunk, pieces))
    return entries


def read_detoken_rules(lang): # Deprecated?
    loc = path.join(DATA_DIR, lang, 'detokenize')
    entries = []
    with utf8open(loc) as file_:
        for line in file_:
            entries.append(line.strip())
    return entries


def align_tokens(ref, indices): # Deprecated, surely?
    start = 0
    queue = list(indices)
    for token in ref:
        end = start + len(token)
        emit = []
        while queue and queue[0][1] <= end:
            emit.append(queue.pop(0))
        yield token, emit
        start = end
    assert not queue


def detokenize(token_rules, words): # Deprecated?
    """To align with treebanks, return a list of "chunks", where a chunk is a
    sequence of tokens that are separated by whitespace in actual strings. Each
    chunk should be a tuple of token indices, e.g.

    >>> detokenize(["ca<SEP>n't", '<SEP>!'], ["I", "ca", "n't", "!"])
    [(0,), (1, 2, 3)]
    """
    string = ' '.join(words)
    for subtoks in token_rules:
        # Algorithmically this is dumb, but writing a little list-based match
        # machine? Ain't nobody got time for that.
        string = string.replace(subtoks.replace('<SEP>', ' '), subtoks)
    positions = []
    i = 0
    for chunk in string.split():
        subtoks = chunk.split('<SEP>')
        positions.append(tuple(range(i, i+len(subtoks))))
        i += len(subtoks)
    return positions
