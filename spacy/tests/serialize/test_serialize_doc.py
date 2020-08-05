import spacy
from spacy.lang.en import English
from spacy.tokens import Doc, DocBin

from ..util import make_tempdir


def test_serialize_empty_doc(en_vocab):
    doc = Doc(en_vocab)
    data = doc.to_bytes()
    doc2 = Doc(en_vocab)
    doc2.from_bytes(data)
    assert len(doc) == len(doc2)
    for token1, token2 in zip(doc, doc2):
        assert token1.text == token2.text


def test_serialize_doc_roundtrip_bytes(en_vocab):
    doc = Doc(en_vocab, words=["hello", "world"])
    doc.cats = {"A": 0.5}
    doc_b = doc.to_bytes()
    new_doc = Doc(en_vocab).from_bytes(doc_b)
    assert new_doc.to_bytes() == doc_b


def test_serialize_doc_roundtrip_disk(en_vocab):
    doc = Doc(en_vocab, words=["hello", "world"])
    with make_tempdir() as d:
        file_path = d / "doc"
        doc.to_disk(file_path)
        doc_d = Doc(en_vocab).from_disk(file_path)
        assert doc.to_bytes() == doc_d.to_bytes()


def test_serialize_doc_roundtrip_disk_str_path(en_vocab):
    doc = Doc(en_vocab, words=["hello", "world"])
    with make_tempdir() as d:
        file_path = d / "doc"
        file_path = str(file_path)
        doc.to_disk(file_path)
        doc_d = Doc(en_vocab).from_disk(file_path)
        assert doc.to_bytes() == doc_d.to_bytes()


def test_serialize_doc_exclude(en_vocab):
    doc = Doc(en_vocab, words=["hello", "world"])
    doc.user_data["foo"] = "bar"
    new_doc = Doc(en_vocab).from_bytes(doc.to_bytes())
    assert new_doc.user_data["foo"] == "bar"
    new_doc = Doc(en_vocab).from_bytes(doc.to_bytes(), exclude=["user_data"])
    assert not new_doc.user_data
    new_doc = Doc(en_vocab).from_bytes(doc.to_bytes(exclude=["user_data"]))
    assert not new_doc.user_data


def test_serialize_doc_bin():
    doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)
    texts = ["Some text", "Lots of texts...", "..."]
    cats = {"A": 0.5}
    nlp = English()
    for doc in nlp.pipe(texts):
        doc.cats = cats
        doc_bin.add(doc)
    bytes_data = doc_bin.to_bytes()

    # Deserialize later, e.g. in a new process
    nlp = spacy.blank("en")
    doc_bin = DocBin().from_bytes(bytes_data)
    reloaded_docs = list(doc_bin.get_docs(nlp.vocab))
    for i, doc in enumerate(reloaded_docs):
        assert doc.text == texts[i]
        assert doc.cats == cats


def test_serialize_doc_bin_unknown_spaces(en_vocab):
    doc1 = Doc(en_vocab, words=["that", "'s"])
    assert doc1.has_unknown_spaces
    assert doc1.text == "that 's "
    doc2 = Doc(en_vocab, words=["that", "'s"], spaces=[False, False])
    assert not doc2.has_unknown_spaces
    assert doc2.text == "that's"

    doc_bin = DocBin().from_bytes(DocBin(docs=[doc1, doc2]).to_bytes())
    re_doc1, re_doc2 = doc_bin.get_docs(en_vocab)
    assert re_doc1.has_unknown_spaces
    assert re_doc1.text == "that 's "
    assert not re_doc2.has_unknown_spaces
    assert re_doc2.text == "that's"
