from typing import cast
import pytest
from numpy.testing import assert_equal
from spacy.attrs import TAG

from spacy import util
from spacy.training import Example
from spacy.lang.en import English
from spacy.language import Language
from spacy.pipeline import TrainablePipe
from thinc.api import compounding

from ..util import make_tempdir


@pytest.mark.issue(4348)
def test_issue4348():
    """Test that training the tagger with empty data, doesn't throw errors"""
    nlp = English()
    example = Example.from_dict(nlp.make_doc(""), {"tags": []})
    TRAIN_DATA = [example, example]
    tagger = nlp.add_pipe("tagger")
    tagger.add_label("A")
    optimizer = nlp.initialize()
    for i in range(5):
        losses = {}
        batches = util.minibatch(
            TRAIN_DATA, size=compounding(4.0, 32.0, 1.001).to_generator()
        )
        for batch in batches:
            nlp.update(batch, sgd=optimizer, losses=losses)


def test_label_types():
    nlp = Language()
    tagger = nlp.add_pipe("tagger")
    tagger.add_label("A")
    with pytest.raises(ValueError):
        tagger.add_label(9)


def test_tagger_initialize_tag_map():
    """Test that Tagger.initialize() without gold tuples does not clobber
    the tag map."""
    nlp = Language()
    tagger = nlp.add_pipe("tagger")
    orig_tag_count = len(tagger.labels)
    tagger.add_label("A")
    nlp.initialize()
    assert orig_tag_count + 1 == len(nlp.get_pipe("tagger").labels)


TAGS = ("N", "V", "J")

TRAIN_DATA = [
    ("I like green eggs", {"tags": ["N", "V", "J", "N"]}),
    ("Eat blue ham", {"tags": ["V", "J", "N"]}),
]

PARTIAL_DATA = [
    # partial annotation
    ("I like green eggs", {"tags": ["", "V", "J", ""]}),
    # misaligned partial annotation
    (
        "He hates green eggs",
        {
            "words": ["He", "hate", "s", "green", "eggs"],
            "tags": ["", "V", "S", "J", ""],
        },
    ),
]


def test_no_label():
    nlp = Language()
    nlp.add_pipe("tagger")
    with pytest.raises(ValueError):
        nlp.initialize()


def test_no_resize():
    nlp = Language()
    tagger = nlp.add_pipe("tagger")
    tagger.add_label("N")
    tagger.add_label("V")
    assert tagger.labels == ("N", "V")
    nlp.initialize()
    assert tagger.model.get_dim("nO") == 2
    # this throws an error because the tagger can't be resized after initialization
    with pytest.raises(ValueError):
        tagger.add_label("J")


def test_implicit_label():
    nlp = Language()
    nlp.add_pipe("tagger")
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    nlp.initialize(get_examples=lambda: train_examples)


def test_initialize_examples():
    nlp = Language()
    tagger = nlp.add_pipe("tagger")
    train_examples = []
    for tag in TAGS:
        tagger.add_label(tag)
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    # you shouldn't really call this more than once, but for testing it should be fine
    nlp.initialize()
    nlp.initialize(get_examples=lambda: train_examples)
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: None)
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: train_examples[0])
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: [])
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=train_examples)


def test_no_data():
    # Test that the tagger provides a nice error when there's no tagging data / labels
    TEXTCAT_DATA = [
        ("I'm so happy.", {"cats": {"POSITIVE": 1.0, "NEGATIVE": 0.0}}),
        ("I'm so angry", {"cats": {"POSITIVE": 0.0, "NEGATIVE": 1.0}}),
    ]
    nlp = English()
    nlp.add_pipe("tagger")
    nlp.add_pipe("textcat")
    train_examples = []
    for t in TEXTCAT_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    with pytest.raises(ValueError):
        nlp.initialize(get_examples=lambda: train_examples)


def test_incomplete_data():
    # Test that the tagger works with incomplete information
    nlp = English()
    nlp.add_pipe("tagger")
    train_examples = []
    for t in PARTIAL_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    optimizer = nlp.initialize(get_examples=lambda: train_examples)
    for i in range(50):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)
    assert losses["tagger"] < 0.00001

    # test the trained model
    test_text = "I like blue eggs"
    doc = nlp(test_text)
    assert doc[1].tag_ == "V"
    assert doc[2].tag_ == "J"


def test_overfitting_IO():
    # Simple test to try and quickly overfit the tagger - ensuring the ML models work correctly
    nlp = English()
    tagger = nlp.add_pipe("tagger")
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    optimizer = nlp.initialize(get_examples=lambda: train_examples)
    assert tagger.model.get_dim("nO") == len(TAGS)

    for i in range(50):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)
    assert losses["tagger"] < 0.00001

    # test the trained model
    test_text = "I like blue eggs"
    doc = nlp(test_text)
    assert doc[0].tag_ == "N"
    assert doc[1].tag_ == "V"
    assert doc[2].tag_ == "J"
    assert doc[3].tag_ == "N"

    # Also test the results are still the same after IO
    with make_tempdir() as tmp_dir:
        nlp.to_disk(tmp_dir)
        nlp2 = util.load_model_from_path(tmp_dir)
        doc2 = nlp2(test_text)
        assert doc2[0].tag_ == "N"
        assert doc2[1].tag_ == "V"
        assert doc2[2].tag_ == "J"
        assert doc2[3].tag_ == "N"

    # Make sure that running pipe twice, or comparing to call, always amounts to the same predictions
    texts = [
        "Just a sentence.",
        "I like green eggs.",
        "Here is another one.",
        "I eat ham.",
    ]
    batch_deps_1 = [doc.to_array([TAG]) for doc in nlp.pipe(texts)]
    batch_deps_2 = [doc.to_array([TAG]) for doc in nlp.pipe(texts)]
    no_batch_deps = [doc.to_array([TAG]) for doc in [nlp(text) for text in texts]]
    assert_equal(batch_deps_1, batch_deps_2)
    assert_equal(batch_deps_1, no_batch_deps)

    # Try to unlearn the first 'N' tag with negative annotation
    neg_ex = Example.from_dict(nlp.make_doc(test_text), {"tags": ["!N", "V", "J", "N"]})

    for i in range(20):
        losses = {}
        nlp.update([neg_ex], sgd=optimizer, losses=losses)

    # test the "untrained" tag
    doc3 = nlp(test_text)
    assert doc3[0].tag_ != "N"


def test_is_distillable():
    nlp = English()
    tagger = nlp.add_pipe("tagger")
    assert tagger.is_distillable


def test_distill():
    teacher = English()
    teacher_tagger = teacher.add_pipe("tagger")
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(teacher.make_doc(t[0]), t[1]))

    optimizer = teacher.initialize(get_examples=lambda: train_examples)

    for i in range(50):
        losses = {}
        teacher.update(train_examples, sgd=optimizer, losses=losses)
    assert losses["tagger"] < 0.00001

    student = English()
    student_tagger = student.add_pipe("tagger")
    student_tagger.min_tree_freq = 1
    student_tagger.initialize(
        get_examples=lambda: train_examples, labels=teacher_tagger.label_data
    )

    distill_examples = [
        Example.from_dict(teacher.make_doc(t[0]), {}) for t in TRAIN_DATA
    ]

    for i in range(50):
        losses = {}
        student_tagger.distill(
            teacher_tagger, distill_examples, sgd=optimizer, losses=losses
        )
    assert losses["tagger"] < 0.00001

    test_text = "I like blue eggs"
    doc = student(test_text)
    assert doc[0].tag_ == "N"
    assert doc[1].tag_ == "V"
    assert doc[2].tag_ == "J"
    assert doc[3].tag_ == "N"


def test_save_activations():
    # Test if activations are correctly added to Doc when requested.
    nlp = English()
    tagger = cast(TrainablePipe, nlp.add_pipe("tagger"))
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    nlp.initialize(get_examples=lambda: train_examples)

    doc = nlp("This is a test.")
    assert "tagger" not in doc.activations

    tagger.save_activations = True
    doc = nlp("This is a test.")
    assert "tagger" in doc.activations
    assert set(doc.activations["tagger"].keys()) == {"label_ids", "probabilities"}
    assert doc.activations["tagger"]["probabilities"].shape == (5, len(TAGS))
    assert doc.activations["tagger"]["label_ids"].shape == (5,)


def test_tagger_requires_labels():
    nlp = English()
    nlp.add_pipe("tagger")
    with pytest.raises(ValueError):
        nlp.initialize()
