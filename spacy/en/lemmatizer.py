from __future__ import unicode_literals
from os import path
import codecs


class Lemmatizer(object):
    def __init__(self, wn_dict_dir, noun_id, verb_id, adj_id):
        self.noun_id = noun_id
        self.verb_id = verb_id
        self.adj_id = adj_id
        self.index = {}
        self.exc = {}
        for pos in ['adj', 'adv', 'noun', 'verb']:
            self.index[pos] = read_index(path.join(wn_dict_dir, 'index.%s' % pos))
            self.exc[pos] = read_exc(path.join(wn_dict_dir, '%s.exc' % pos))

    def __call__(self, string, pos):

        return lemmatize(string, self.index[pos], self.exc[pos], self.rules[pos])
        if pos == self.noun_id:
            return self.noun(string)
        elif pos == self.verb_id:
            return self.verb(string)
        elif pos == self.adj_id:
            return self.adj(string)
        else:
            raise Exception("Cannot lemmatize with unknown pos: %s" % pos)

    def noun(self, string):
        return self(string, 'noun')

    def verb(self, string):
        return self(string, 'verb')

    def adj(self, string):
        return self(string, 'adj')


def lemmatize(string, index, exceptions, rules):
    string = string.lower()
    forms = []
    if string in index:
        forms.append(string)
    forms.extend(exceptions.get(string, []))
    for old, new in rules:
        if string.endswith(old):
            form = string[:len(string) - len(old)] + new
            if form in index:
                forms.append(form)
    if not forms:
        forms.append(string)
    return set(forms)


def read_index(loc):
    index = set()
    for line in codecs.open(loc, 'r', 'utf8'):
        if line.startswith(' '):
            continue
        pieces = line.split()
        word = pieces[0]
        if word.count('_') == 0:
            index.add(word)
    return index


def read_exc(loc):
    exceptions = {}
    for line in codecs.open(loc, 'r', 'utf8'):
        if line.startswith(' '):
            continue
        pieces = line.split()
        exceptions[pieces[0]] = tuple(pieces[1:])
    return exceptions
