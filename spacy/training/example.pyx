from collections import Iterable as IterableInstance
import warnings
import numpy

from ..tokens.doc cimport Doc
from ..tokens.span cimport Span
from ..tokens.span import Span
from ..attrs import IDS
from .align import Alignment
from .iob_utils import biluo_to_iob, biluo_tags_from_offsets, biluo_tags_from_doc
from .iob_utils import spans_from_biluo_tags
from ..errors import Errors, Warnings
from ..pipeline._parser_internals import nonproj


cpdef Doc annotations2doc(vocab, tok_annot, doc_annot):
    """ Create a Doc from dictionaries with token and doc annotations. """
    attrs, array = _annot2array(vocab, tok_annot, doc_annot)
    output = Doc(vocab, words=tok_annot["ORTH"], spaces=tok_annot["SPACY"])
    if "entities" in doc_annot:
       _add_entities_to_doc(output, doc_annot["entities"])
    if array.size:
        output = output.from_array(attrs, array)
    # links are currently added with ENT_KB_ID on the token level
    output.cats.update(doc_annot.get("cats", {}))
    return output


def validate_examples(examples, method):
    """Check that a batch of examples received during processing is valid.
    This function lives here to prevent circular imports.

    examples (Iterable[Examples]): A batch of examples.
    method (str): The method name to show in error messages.
    """
    if not isinstance(examples, IterableInstance):
        err = Errors.E978.format(name=method, types=type(examples))
        raise TypeError(err)
    wrong = set([type(eg) for eg in examples if not isinstance(eg, Example)])
    if wrong:
        err = Errors.E978.format(name=method, types=wrong)
        raise TypeError(err)


cdef class Example:
    def __init__(self, Doc predicted, Doc reference, *, alignment=None):
        if predicted is None:
            raise TypeError(Errors.E972.format(arg="predicted"))
        if reference is None:
            raise TypeError(Errors.E972.format(arg="reference"))
        self.predicted = predicted
        self.reference = reference
        self._cached_alignment = alignment

    def __len__(self):
        return len(self.predicted)

    property predicted:
        def __get__(self):
            return self.x

        def __set__(self, doc):
            self.x = doc
            self._cached_alignment = None
            self._cached_words_x = [t.text for t in doc]

    property reference:
        def __get__(self):
            return self.y

        def __set__(self, doc):
            self.y = doc
            self._cached_alignment = None
            self._cached_words_y = [t.text for t in doc]

    def copy(self):
        return Example(
            self.x.copy(),
            self.y.copy()
        )

    @classmethod
    def from_dict(cls, Doc predicted, dict example_dict):
        if predicted is None:
            raise ValueError(Errors.E976.format(n="first", type="Doc"))
        if example_dict is None:
            raise ValueError(Errors.E976.format(n="second", type="dict"))
        example_dict = _fix_legacy_dict_data(example_dict)
        tok_dict, doc_dict = _parse_example_dict_data(example_dict)
        if "ORTH" not in tok_dict:
            tok_dict["ORTH"] = [tok.text for tok in predicted]
            tok_dict["SPACY"] = [tok.whitespace_ for tok in predicted]
        return Example(
            predicted,
            annotations2doc(predicted.vocab, tok_dict, doc_dict)
        )

    @property
    def alignment(self):
        words_x = [token.text for token in self.x]
        words_y = [token.text for token in self.y]
        if self._cached_alignment is None or \
                words_x != self._cached_words_x or \
                words_y != self._cached_words_y:
            self._cached_alignment = Alignment.from_strings(words_x, words_y)
            self._cached_words_x = words_x
            self._cached_words_y = words_y
        return self._cached_alignment

    def get_aligned(self, field, as_string=False):
        """Return an aligned array for a token attribute."""
        align = self.alignment.x2y

        vocab = self.reference.vocab
        gold_values = self.reference.to_array([field])
        output = [None] * len(self.predicted)
        for token in self.predicted:
            if token.is_space:
                output[token.i] = None
            else:
                values = gold_values[align[token.i].dataXd]
                values = values.ravel()
                if len(values) == 0:
                    output[token.i] = None
                elif len(values) == 1:
                    output[token.i] = values[0]
                elif len(set(list(values))) == 1:
                    # If all aligned tokens have the same value, use it.
                    output[token.i] = values[0]
                else:
                    output[token.i] = None
        if as_string and field not in ["ENT_IOB", "SENT_START"]:
            output = [vocab.strings[o] if o is not None else o for o in output]
        return output

    def get_aligned_parse(self, projectivize=True):
        cand_to_gold = self.alignment.x2y
        gold_to_cand = self.alignment.y2x
        aligned_heads = [None] * self.x.length
        aligned_deps = [None] * self.x.length
        heads = [token.head.i for token in self.y]
        deps = [token.dep_ for token in self.y]
        if projectivize:
            heads, deps = nonproj.projectivize(heads, deps)
        for cand_i in range(self.x.length):
            if cand_to_gold.lengths[cand_i] == 1:
                gold_i = cand_to_gold[cand_i].dataXd[0, 0]
                if gold_to_cand.lengths[heads[gold_i]] == 1:
                    aligned_heads[cand_i] = int(gold_to_cand[heads[gold_i]].dataXd[0, 0])
                    aligned_deps[cand_i] = deps[gold_i]
        return aligned_heads, aligned_deps

    def get_aligned_spans_x2y(self, x_spans):
        return self._get_aligned_spans(self.y, x_spans, self.alignment.x2y)

    def get_aligned_spans_y2x(self, y_spans):
        return self._get_aligned_spans(self.x, y_spans, self.alignment.y2x)

    def _get_aligned_spans(self, doc, spans, align):
        seen = set()
        output = []
        for span in spans:
            indices = align[span.start : span.end].data.ravel()
            indices = [idx for idx in indices if idx not in seen]
            if len(indices) >= 1:
                aligned_span = Span(doc, indices[0], indices[-1] + 1, label=span.label)
                target_text = span.text.lower().strip().replace(" ", "")
                our_text = aligned_span.text.lower().strip().replace(" ", "")
                if our_text == target_text:
                    output.append(aligned_span)
                    seen.update(indices)
        return output

    def get_aligned_ner(self):
        if not self.y.is_nered:
            return [None] * len(self.x)  # should this be 'missing' instead of 'None' ?
        x_ents = self.get_aligned_spans_y2x(self.y.ents)
        # Default to 'None' for missing values
        x_tags = biluo_tags_from_offsets(
            self.x,
            [(e.start_char, e.end_char, e.label_) for e in x_ents],
            missing=None
        )
        # Now fill the tokens we can align to O.
        O = 2 # I=1, O=2, B=3
        for i, ent_iob in enumerate(self.get_aligned("ENT_IOB")):
            if x_tags[i] is None:
                if ent_iob == O:
                    x_tags[i] = "O"
                elif self.x[i].is_space:
                    x_tags[i] = "O"
        return x_tags

    def to_dict(self):
        return {
            "doc_annotation": {
                "cats": dict(self.reference.cats),
                "entities": biluo_tags_from_doc(self.reference),
                "links": self._links_to_dict()
            },
            "token_annotation": {
                "ORTH": [t.text for t in self.reference],
                "SPACY": [bool(t.whitespace_) for t in self.reference],
                "TAG": [t.tag_ for t in self.reference],
                "LEMMA": [t.lemma_ for t in self.reference],
                "POS": [t.pos_ for t in self.reference],
                "MORPH": [t.morph_ for t in self.reference],
                "HEAD": [t.head.i for t in self.reference],
                "DEP": [t.dep_ for t in self.reference],
                "SENT_START": [int(bool(t.is_sent_start)) for t in self.reference]
            }
        }

    def _links_to_dict(self):
        links = {}
        for ent in self.reference.ents:
            if ent.kb_id_:
                links[(ent.start_char, ent.end_char)] = {ent.kb_id_: 1.0}
        return links

    def split_sents(self):
        """ Split the token annotations into multiple Examples based on
        sent_starts and return a list of the new Examples"""
        if not self.reference.is_sentenced:
            return [self]

        align = self.alignment.y2x
        seen_indices = set()
        output = []
        for y_sent in self.reference.sents:
            indices = align[y_sent.start : y_sent.end].data.ravel()
            indices = [idx for idx in indices if idx not in seen_indices]
            if indices:
                x_sent = self.predicted[indices[0] : indices[-1] + 1]
                output.append(Example(x_sent.as_doc(), y_sent.as_doc()))
                seen_indices.update(indices)
        return output

    property text:
        def __get__(self):
            return self.x.text

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self.to_dict())


def _annot2array(vocab, tok_annot, doc_annot):
    attrs = []
    values = []

    for key, value in doc_annot.items():
        if value:
            if key == "entities":
                pass
            elif key == "links":
                ent_kb_ids = _parse_links(vocab, tok_annot["ORTH"], tok_annot["SPACY"], value)
                tok_annot["ENT_KB_ID"] = ent_kb_ids
            elif key == "cats":
                pass
            else:
                raise ValueError(Errors.E974.format(obj="doc", key=key))

    for key, value in tok_annot.items():
        if key not in IDS:
            raise ValueError(Errors.E974.format(obj="token", key=key))
        elif key in ["ORTH", "SPACY"]:
            pass
        elif key == "HEAD":
            attrs.append(key)
            values.append([h-i for i, h in enumerate(value)])
        elif key == "SENT_START":
            attrs.append(key)
            values.append(value)
        elif key == "MORPH":
            attrs.append(key)
            values.append([vocab.morphology.add(v) for v in value])
        else:
            attrs.append(key)
            if not all(isinstance(v, str) for v in value):
                types = set([type(v) for v in value])
                raise TypeError(Errors.E969.format(field=key, types=types)) from None
            values.append([vocab.strings.add(v) for v in value])
    array = numpy.asarray(values, dtype="uint64")
    return attrs, array.T


def _add_entities_to_doc(doc, ner_data):
    if ner_data is None:
        return
    elif ner_data == []:
        doc.ents = []
    elif isinstance(ner_data[0], tuple):
        return _add_entities_to_doc(
            doc,
            biluo_tags_from_offsets(doc, ner_data)
        )
    elif isinstance(ner_data[0], str) or ner_data[0] is None:
        return _add_entities_to_doc(
            doc,
            spans_from_biluo_tags(doc, ner_data)
        )
    elif isinstance(ner_data[0], Span):
        # Ugh, this is super messy. Really hard to set O entities
        doc.ents = ner_data
        doc.ents = [span for span in ner_data if span.label_]
    else:
        raise ValueError(Errors.E973)


def _parse_example_dict_data(example_dict):
    return (
        example_dict["token_annotation"],
        example_dict["doc_annotation"]
    )


def _fix_legacy_dict_data(example_dict):
    token_dict = example_dict.get("token_annotation", {})
    doc_dict = example_dict.get("doc_annotation", {})
    for key, value in example_dict.items():
        if value:
            if key in ("token_annotation", "doc_annotation"):
                pass
            elif key == "ids":
                pass
            elif key in ("cats", "links"):
                doc_dict[key] = value
            elif key in ("ner", "entities"):
                doc_dict["entities"] = value
            else:
                token_dict[key] = value
    # Remap keys
    remapping = {
        "words": "ORTH",
        "tags": "TAG",
        "pos": "POS",
        "lemmas": "LEMMA",
        "deps": "DEP",
        "heads": "HEAD",
        "sent_starts": "SENT_START",
        "morphs": "MORPH",
        "spaces": "SPACY",
    }
    old_token_dict = token_dict
    token_dict = {}
    for key, value in old_token_dict.items():
        if key in ("text", "ids", "brackets"):
            pass
        elif key in remapping.values():
            token_dict[key] = value
        elif key.lower() in remapping:
            token_dict[remapping[key.lower()]] = value
        else:
            all_keys = set(remapping.values())
            all_keys.update(remapping.keys())
            raise KeyError(Errors.E983.format(key=key, dict="token_annotation", keys=all_keys))
    text = example_dict.get("text", example_dict.get("raw"))
    if _has_field(token_dict, "ORTH") and not _has_field(token_dict, "SPACY"):
        token_dict["SPACY"] = _guess_spaces(text, token_dict["ORTH"])
    if "HEAD" in token_dict and "SENT_START" in token_dict:
        # If heads are set, we don't also redundantly specify SENT_START.
        token_dict.pop("SENT_START")
        warnings.warn(Warnings.W092)
    return {
        "token_annotation": token_dict,
        "doc_annotation": doc_dict
    }

def _has_field(annot, field):
    if field not in annot:
        return False
    elif annot[field] is None:
        return False
    elif len(annot[field]) == 0:
        return False
    elif all([value is None for value in annot[field]]):
        return False
    else:
        return True


def _parse_ner_tags(biluo_or_offsets, vocab, words, spaces):
    if isinstance(biluo_or_offsets[0], (list, tuple)):
        # Convert to biluo if necessary
        # This is annoying but to convert the offsets we need a Doc
        # that has the target tokenization.
        reference = Doc(vocab, words=words, spaces=spaces)
        biluo = biluo_tags_from_offsets(reference, biluo_or_offsets)
    else:
        biluo = biluo_or_offsets
    ent_iobs = []
    ent_types = []
    for iob_tag in biluo_to_iob(biluo):
        if iob_tag in (None, "-"):
            ent_iobs.append("")
            ent_types.append("")
        else:
            ent_iobs.append(iob_tag.split("-")[0])
            if iob_tag.startswith("I") or iob_tag.startswith("B"):
                ent_types.append(iob_tag.split("-", 1)[1])
            else:
                ent_types.append("")
    return ent_iobs, ent_types

def _parse_links(vocab, words, spaces, links):
    reference = Doc(vocab, words=words, spaces=spaces)
    starts = {token.idx: token.i for token in reference}
    ends = {token.idx + len(token): token.i for token in reference}
    ent_kb_ids = ["" for _ in reference]

    for index, annot_dict in links.items():
        true_kb_ids = []
        for key, value in annot_dict.items():
            if value == 1.0:
                true_kb_ids.append(key)
        if len(true_kb_ids) > 1:
            raise ValueError(Errors.E980)

        if len(true_kb_ids) == 1:
            start_char, end_char = index
            start_token = starts.get(start_char)
            end_token = ends.get(end_char)
            if start_token is None or end_token is None:
                raise ValueError(Errors.E981)
            for i in range(start_token, end_token+1):
                ent_kb_ids[i] = true_kb_ids[0]

    return ent_kb_ids


def _guess_spaces(text, words):
    if text is None:
        return None
    spaces = []
    text_pos = 0
    # align words with text
    for word in words:
        try:
            word_start = text[text_pos:].index(word)
        except ValueError:
            spaces.append(True)
            continue
        text_pos += word_start + len(word)
        if text_pos < len(text) and text[text_pos] == " ":
            spaces.append(True)
        else:
            spaces.append(False)
    return spaces
