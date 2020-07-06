from spacy.gold import Example
from spacy.lang.en import English
from spacy.util import minibatch, compounding
import pytest


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_issue4348():
    """Test that training the tagger with empty data, doesn't throw errors"""

    nlp = English()
    example = Example.from_dict(nlp.make_doc(""), {"tags": []})
    TRAIN_DATA = [example, example]

    tagger = nlp.create_pipe("tagger")
    nlp.add_pipe(tagger)

    optimizer = nlp.begin_training()
    for i in range(5):
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            nlp.update(batch, sgd=optimizer, losses=losses)
