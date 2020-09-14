from itertools import islice
from typing import Iterable, Tuple, Optional, Dict, List, Callable, Iterator, Any
from thinc.api import get_array_module, Model, Optimizer, set_dropout_rate, Config
from thinc.types import Floats2d
import numpy

from .pipe import Pipe
from ..language import Language
from ..training import Example, validate_examples
from ..errors import Errors
from ..scorer import Scorer
from .. import util
from ..tokens import Doc
from ..vocab import Vocab


default_model_config = """
[model]
@architectures = "spacy.TextCatEnsemble.v1"
exclusive_classes = false
pretrained_vectors = null
width = 64
conv_depth = 2
embed_size = 2000
window_size = 1
ngram_size = 1
dropout = null
"""
DEFAULT_TEXTCAT_MODEL = Config().from_str(default_model_config)["model"]

bow_model_config = """
[model]
@architectures = "spacy.TextCatBOW.v1"
exclusive_classes = false
ngram_size = 1
no_output_layer = false
"""

cnn_model_config = """
[model]
@architectures = "spacy.TextCatCNN.v1"
exclusive_classes = false

[model.tok2vec]
@architectures = "spacy.HashEmbedCNN.v1"
pretrained_vectors = null
width = 96
depth = 4
embed_size = 2000
window_size = 1
maxout_pieces = 3
subword_features = true
"""


@Language.factory(
    "textcat",
    assigns=["doc.cats"],
    default_config={
        "labels": [],
        "threshold": 0.5,
        "positive_label": None,
        "model": DEFAULT_TEXTCAT_MODEL,
    },
    scores=[
        "cats_score",
        "cats_score_desc",
        "cats_p",
        "cats_r",
        "cats_f",
        "cats_macro_f",
        "cats_macro_auc",
        "cats_f_per_type",
        "cats_macro_auc_per_type",
    ],
    default_score_weights={"cats_score": 1.0},
)
def make_textcat(
    nlp: Language,
    name: str,
    model: Model[List[Doc], List[Floats2d]],
    labels: List[str],
    threshold: float,
    positive_label: Optional[str],
) -> "TextCategorizer":
    """Create a TextCategorizer compoment. The text categorizer predicts categories
    over a whole document. It can learn one or more labels, and the labels can
    be mutually exclusive (i.e. one true label per doc) or non-mutually exclusive
    (i.e. zero or more labels may be true per doc). The multi-label setting is
    controlled by the model instance that's provided.

    model (Model[List[Doc], List[Floats2d]]): A model instance that predicts
        scores for each category.
    labels (list): A list of categories to learn. If empty, the model infers the
        categories from the data.
    threshold (float): Cutoff to consider a prediction "positive".
    positive_label (Optional[str]): The positive label for a binary task with exclusive classes, None otherwise.
    """
    return TextCategorizer(
        nlp.vocab,
        model,
        name,
        labels=labels,
        threshold=threshold,
        positive_label=positive_label,
    )


class TextCategorizer(Pipe):
    """Pipeline component for text classification.

    DOCS: https://nightly.spacy.io/api/textcategorizer
    """

    def __init__(
        self,
        vocab: Vocab,
        model: Model,
        name: str = "textcat",
        *,
        labels: List[str],
        threshold: float,
        positive_label: Optional[str],
    ) -> None:
        """Initialize a text categorizer.

        vocab (Vocab): The shared vocabulary.
        model (thinc.api.Model): The Thinc Model powering the pipeline component.
        name (str): The component instance name, used to add entries to the
            losses during training.
        labels (List[str]): The labels to use.
        threshold (float): Cutoff to consider a prediction "positive".
        positive_label (Optional[str]): The positive label for a binary task with exclusive classes, None otherwise.

        DOCS: https://nightly.spacy.io/api/textcategorizer#init
        """
        self.vocab = vocab
        self.model = model
        self.name = name
        self._rehearsal_model = None
        cfg = {
            "labels": labels,
            "threshold": threshold,
            "positive_label": positive_label,
        }
        self.cfg = dict(cfg)

    @property
    def labels(self) -> Tuple[str]:
        """RETURNS (Tuple[str]): The labels currently added to the component.

        DOCS: https://nightly.spacy.io/api/textcategorizer#labels
        """
        return tuple(self.cfg["labels"])

    @labels.setter
    def labels(self, value: List[str]) -> None:
        self.cfg["labels"] = tuple(value)

    def pipe(self, stream: Iterable[Doc], *, batch_size: int = 128) -> Iterator[Doc]:
        """Apply the pipe to a stream of documents. This usually happens under
        the hood when the nlp object is called on a text and all components are
        applied to the Doc.

        stream (Iterable[Doc]): A stream of documents.
        batch_size (int): The number of documents to buffer.
        YIELDS (Doc): Processed documents in order.

        DOCS: https://nightly.spacy.io/api/textcategorizer#pipe
        """
        for docs in util.minibatch(stream, size=batch_size):
            scores = self.predict(docs)
            self.set_annotations(docs, scores)
            yield from docs

    def predict(self, docs: Iterable[Doc]):
        """Apply the pipeline's model to a batch of docs, without modifying them.

        docs (Iterable[Doc]): The documents to predict.
        RETURNS: The models prediction for each document.

        DOCS: https://nightly.spacy.io/api/textcategorizer#predict
        """
        tensors = [doc.tensor for doc in docs]
        if not any(len(doc) for doc in docs):
            # Handle cases where there are no tokens in any docs.
            xp = get_array_module(tensors)
            scores = xp.zeros((len(docs), len(self.labels)))
            return scores
        scores = self.model.predict(docs)
        scores = self.model.ops.asarray(scores)
        return scores

    def set_annotations(self, docs: Iterable[Doc], scores) -> None:
        """Modify a batch of [`Doc`](/api/doc) objects, using pre-computed scores.

        docs (Iterable[Doc]): The documents to modify.
        scores: The scores to set, produced by TextCategorizer.predict.

        DOCS: https://nightly.spacy.io/api/textcategorizer#set_annotations
        """
        for i, doc in enumerate(docs):
            for j, label in enumerate(self.labels):
                doc.cats[label] = float(scores[i, j])

    def update(
        self,
        examples: Iterable[Example],
        *,
        drop: float = 0.0,
        set_annotations: bool = False,
        sgd: Optional[Optimizer] = None,
        losses: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Learn from a batch of documents and gold-standard information,
        updating the pipe's model. Delegates to predict and get_loss.

        examples (Iterable[Example]): A batch of Example objects.
        drop (float): The dropout rate.
        set_annotations (bool): Whether or not to update the Example objects
            with the predictions.
        sgd (thinc.api.Optimizer): The optimizer.
        losses (Dict[str, float]): Optional record of the loss during training.
            Updated using the component name as the key.
        RETURNS (Dict[str, float]): The updated losses dictionary.

        DOCS: https://nightly.spacy.io/api/textcategorizer#update
        """
        if losses is None:
            losses = {}
        losses.setdefault(self.name, 0.0)
        validate_examples(examples, "TextCategorizer.update")
        if not any(len(eg.predicted) if eg.predicted else 0 for eg in examples):
            # Handle cases where there are no tokens in any docs.
            return losses
        set_dropout_rate(self.model, drop)
        scores, bp_scores = self.model.begin_update([eg.predicted for eg in examples])
        loss, d_scores = self.get_loss(examples, scores)
        bp_scores(d_scores)
        if sgd is not None:
            self.model.finish_update(sgd)
        losses[self.name] += loss
        if set_annotations:
            docs = [eg.predicted for eg in examples]
            self.set_annotations(docs, scores=scores)
        return losses

    def rehearse(
        self,
        examples: Iterable[Example],
        *,
        drop: float = 0.0,
        sgd: Optional[Optimizer] = None,
        losses: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Perform a "rehearsal" update from a batch of data. Rehearsal updates
        teach the current model to make predictions similar to an initial model,
        to try to address the "catastrophic forgetting" problem. This feature is
        experimental.

        examples (Iterable[Example]): A batch of Example objects.
        drop (float): The dropout rate.
        sgd (thinc.api.Optimizer): The optimizer.
        losses (Dict[str, float]): Optional record of the loss during training.
            Updated using the component name as the key.
        RETURNS (Dict[str, float]): The updated losses dictionary.

        DOCS: https://nightly.spacy.io/api/textcategorizer#rehearse
        """
        if losses is not None:
            losses.setdefault(self.name, 0.0)
        if self._rehearsal_model is None:
            return losses
        validate_examples(examples, "TextCategorizer.rehearse")
        docs = [eg.predicted for eg in examples]
        if not any(len(doc) for doc in docs):
            # Handle cases where there are no tokens in any docs.
            return losses
        set_dropout_rate(self.model, drop)
        scores, bp_scores = self.model.begin_update(docs)
        target = self._rehearsal_model(examples)
        gradient = scores - target
        bp_scores(gradient)
        if sgd is not None:
            self.model.finish_update(sgd)
        if losses is not None:
            losses[self.name] += (gradient ** 2).sum()
        return losses

    def _examples_to_truth(
        self, examples: List[Example]
    ) -> Tuple[numpy.ndarray, numpy.ndarray]:
        truths = numpy.zeros((len(examples), len(self.labels)), dtype="f")
        not_missing = numpy.ones((len(examples), len(self.labels)), dtype="f")
        for i, eg in enumerate(examples):
            for j, label in enumerate(self.labels):
                if label in eg.reference.cats:
                    truths[i, j] = eg.reference.cats[label]
                else:
                    not_missing[i, j] = 0.0
        truths = self.model.ops.asarray(truths)
        return truths, not_missing

    def get_loss(self, examples: Iterable[Example], scores) -> Tuple[float, float]:
        """Find the loss and gradient of loss for the batch of documents and
        their predicted scores.

        examples (Iterable[Examples]): The batch of examples.
        scores: Scores representing the model's predictions.
        RETUTNRS (Tuple[float, float]): The loss and the gradient.

        DOCS: https://nightly.spacy.io/api/textcategorizer#get_loss
        """
        validate_examples(examples, "TextCategorizer.get_loss")
        truths, not_missing = self._examples_to_truth(examples)
        not_missing = self.model.ops.asarray(not_missing)
        d_scores = (scores - truths) / scores.shape[0]
        d_scores *= not_missing
        mean_square_error = (d_scores ** 2).sum(axis=1).mean()
        return float(mean_square_error), d_scores

    def add_label(self, label: str) -> int:
        """Add a new label to the pipe.

        label (str): The label to add.
        RETURNS (int): 0 if label is already present, otherwise 1.

        DOCS: https://nightly.spacy.io/api/textcategorizer#add_label
        """
        if not isinstance(label, str):
            raise ValueError(Errors.E187)
        if label in self.labels:
            return 0
        self._allow_extra_label()
        self.labels = tuple(list(self.labels) + [label])
        return 1

    def begin_training(
        self,
        get_examples: Callable[[], Iterable[Example]],
        *,
        pipeline: Optional[List[Tuple[str, Callable[[Doc], Doc]]]] = None,
        sgd: Optional[Optimizer] = None,
    ) -> Optimizer:
        """Initialize the pipe for training, using a representative set
        of data examples.

        get_examples (Callable[[], Iterable[Example]]): Function that
            returns a representative sample of gold-standard Example objects.
        pipeline (List[Tuple[str, Callable]]): Optional list of pipeline
            components that this component is part of. Corresponds to
            nlp.pipeline.
        sgd (thinc.api.Optimizer): Optional optimizer. Will be created with
            create_optimizer if it doesn't exist.
        RETURNS (thinc.api.Optimizer): The optimizer.

        DOCS: https://nightly.spacy.io/api/textcategorizer#begin_training
        """
        self._ensure_examples(get_examples)
        subbatch = []  # Select a subbatch of examples to initialize the model
        for example in islice(get_examples(), 10):
            if len(subbatch) < 2:
                subbatch.append(example)
            for cat in example.y.cats:
                self.add_label(cat)
        doc_sample = [eg.reference for eg in subbatch]
        label_sample, _ = self._examples_to_truth(subbatch)
        self._require_labels()
        assert len(doc_sample) > 0, Errors.E923.format(name=self.name)
        assert len(label_sample) > 0, Errors.E923.format(name=self.name)
        self.model.initialize(X=doc_sample, Y=label_sample)
        if sgd is None:
            sgd = self.create_optimizer()
        return sgd

    def score(self, examples: Iterable[Example], **kwargs) -> Dict[str, Any]:
        """Score a batch of examples.

        examples (Iterable[Example]): The examples to score.
        RETURNS (Dict[str, Any]): The scores, produced by Scorer.score_cats.

        DOCS: https://nightly.spacy.io/api/textcategorizer#score
        """
        validate_examples(examples, "TextCategorizer.score")
        return Scorer.score_cats(
            examples,
            "cats",
            labels=self.labels,
            multi_label=self.model.attrs["multi_label"],
            positive_label=self.cfg["positive_label"],
            threshold=self.cfg["threshold"],
            **kwargs,
        )
