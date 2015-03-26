cdef class GoldParse:
    def __init__(self, raw_text, words, ids, tags, heads, labels):
        self.mem = Pool()
        self.loss = 0
        self.length = len(words)
        self.raw_text = raw_text
        self.words = words
        self.ids = ids
        self.tags = tags
        self.heads = heads
        self.labels = labels
        self.c_heads = <int*>self.mem.alloc(self.length, sizeof(int))
        self.c_labels = <int*>self.mem.alloc(self.length, sizeof(int))

    cdef int heads_correct(self, TokenC* tokens, bint score_punct=False) except -1:
        pass

    @classmethod
    def from_conll(cls, unicode sent_str):
        ids = []
        words = []
        heads = []
        labels = []
        tags = []
        for i, line in enumerate(sent_str.split('\n')):
            id_, word, pos_string, head_idx, label = _parse_line(line)
            words.append(word)
            if head_idx == -1:
                head_idx = i
            ids.append(id_)
            heads.append(head_idx)
            labels.append(label)
            tags.append(pos_string)
        text = ' '.join(words)
        return cls(text, [words], ids, words, tags, heads, labels)

    @classmethod
    def from_docparse(cls, unicode sent_str):
        words = []
        heads = []
        labels = []
        tags = []
        ids = []
        lines = sent_str.strip().split('\n')
        raw_text = lines.pop(0).strip()
        tok_text = lines.pop(0).strip()
        for i, line in enumerate(lines):
            id_, word, pos_string, head_idx, label = _parse_line(line)
            if label == 'root':
                label = 'ROOT'
            words.append(word)
            if head_idx < 0:
                head_idx = id_
            ids.append(id_)
            heads.append(head_idx)
            labels.append(label)
            tags.append(pos_string)
        tokenized = [sent_str.replace('<SEP>', ' ').split(' ')
                     for sent_str in tok_text.split('<SENT>')]
        return cls(raw_text, tokenized, ids, words, tags, heads, labels)

    def align_to_tokens(self, tokens, label_ids):
        orig_words = list(self.words)
        annot = zip(self.ids, self.tags, self.heads, self.labels)
        self.ids = []
        self.tags = []
        self.heads = []
        self.labels = []
        missed = []
        for token in tokens:
            while annot and token.idx > annot[0][0]:
                miss_id, miss_tag, miss_head, miss_label = annot.pop(0)
                miss_w = self.words.pop(0)
                if not is_punct_label(miss_label):
                    missed.append(miss_w)
                    self.loss += 1
            if not annot:
                self.tags.append(None)
                self.heads.append(None)
                self.labels.append(None)
                continue
            id_, tag, head, label = annot[0]
            if token.idx == id_:
                self.tags.append(tag)
                self.heads.append(head)
                self.labels.append(label)
                annot.pop(0)
                self.words.pop(0)
            elif token.idx < id_:
                self.tags.append(None)
                self.heads.append(None)
                self.labels.append(None)
            else:
                raise StandardError
        mapped_heads = _map_indices_to_tokens(self.ids, self.heads)
        for i in range(self.length):
            self.c_heads[i] = mapped_heads[i]
            self.c_labels[i] = label_ids[self.labels[i]]
        return self.loss


def is_punct_label(label):
    return label == 'P' or label.lower() == 'punct'


def _map_indices_to_tokens(ids, heads):
    mapped = []
    for head in heads:
        if head not in ids:
            mapped.append(None)
        else:
            mapped.append(ids.index(head))
    return mapped



def _parse_line(line):
    pieces = line.split()
    if len(pieces) == 4:
        return 0, pieces[0], pieces[1], int(pieces[2]) - 1, pieces[3]
    else:
        id_ = int(pieces[0])
        word = pieces[1]
        pos = pieces[3]
        head_idx = int(pieces[6])
        label = pieces[7]
        return id_, word, pos, head_idx, label


"""
# TODO
def evaluate(Language, dev_loc, model_dir, gold_preproc=False):
    global loss
    nlp = Language()
    n_corr = 0
    pos_corr = 0
    n_tokens = 0
    total = 0
    skipped = 0
    loss = 0
    with codecs.open(dev_loc, 'r', 'utf8') as file_:
        #paragraphs = read_tokenized_gold(file_)
        paragraphs = read_docparse_gold(file_)
    for tokens, tag_strs, heads, labels in iter_data(paragraphs, nlp.tokenizer,
                                                     gold_preproc=gold_preproc):
        assert len(tokens) == len(labels)
        nlp.tagger(tokens)
        nlp.parser(tokens)
        for i, token in enumerate(tokens):
            pos_corr += token.tag_ == tag_strs[i]
            n_tokens += 1
            if heads[i] is None:
                skipped += 1
                continue
            if is_punct_label(labels[i]):
                continue
            n_corr += token.head.i == heads[i]
            total += 1
    print loss, skipped, (loss+skipped + total)
    print pos_corr / n_tokens
    return float(n_corr) / (total + loss)
"""
