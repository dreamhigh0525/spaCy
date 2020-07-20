from ...util import get_doc


def test_de_parser_noun_chunks_standard_de(de_tokenizer):
    text = "Eine Tasse steht auf dem Tisch."
    heads = [1, 1, 0, -1, 1, -2, -4]
    pos = ["DET", "NOUN", "VERB", "ADP", "DET", "NOUN", "PUNCT"]
    deps = ["nk", "sb", "ROOT", "mo", "nk", "nk", "punct"]
    tokens = de_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], pos=pos, deps=deps, heads=heads
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 2
    assert chunks[0].text_with_ws == "Eine Tasse "
    assert chunks[1].text_with_ws == "dem Tisch "


def test_de_extended_chunk(de_tokenizer):
    text = "Die Sängerin singt mit einer Tasse Kaffee Arien."
    heads = [1, 1, 0, -1, 1, -2, -1, -5, -6]
    pos = ["DET", "NOUN", "VERB", "ADP", "DET", "NOUN", "NOUN", "NOUN", "PUNCT"]
    deps = ["nk", "sb", "ROOT", "mo", "nk", "nk", "nk", "oa", "punct"]
    tokens = de_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], pos=pos, deps=deps, heads=heads
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 3
    assert chunks[0].text_with_ws == "Die Sängerin "
    assert chunks[1].text_with_ws == "einer Tasse Kaffee "
    assert chunks[2].text_with_ws == "Arien "
