import pytest
from spacy.language import Language


def test_label_types():
    nlp = Language()
    nlp.add_pipe(nlp.create_pipe("tagger"))
    nlp.get_pipe("tagger").add_label("A")
    with pytest.raises(ValueError):
        nlp.get_pipe("tagger").add_label(9)


TAG_MAP = {"N": {"pos": "NOUN"}, "V": {"pos": "VERB"}, "J": {"pos": "ADJ"}}

TRAIN_DATA = [
    ("I like green eggs", {"tags": ["N", "V", "J", "N"]}),
    ("Eat blue ham", {"tags": ["V", "J", "N"]}),
]


def test_overfitting():
    # Simple test to try and quickly overfit the tagger - ensuring the ML models work correctly
    nlp = Language()
    tagger = nlp.create_pipe("tagger")
    for tag, values in TAG_MAP.items():
        tagger.add_label(tag, values)
    nlp.add_pipe(tagger)
    optimizer = nlp.begin_training()

    for i in range(50):
        losses = {}
        nlp.update(TRAIN_DATA, sgd=optimizer, losses=losses)
    assert losses["tagger"] < 0.00001

    # test the trained model
    test_text = "I like blue eggs"
    doc = nlp(test_text)

    assert doc[0].tag_ is "N"
    assert doc[1].tag_ is "V"
    assert doc[2].tag_ is "J"
    assert doc[3].tag_ is "N"
