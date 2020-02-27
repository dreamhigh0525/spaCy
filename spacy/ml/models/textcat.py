from spacy.attrs import ORTH
from spacy.util import registry
from spacy.ml.extract_ngrams import extract_ngrams

from thinc.api import Model, chain, reduce_mean, Linear, list2ragged, Logistic, SparseLinear, Softmax


@registry.architectures.register("spacy.TextCatCNN.v1")
def build_simple_cnn_text_classifier(tok2vec, exclusive_classes, nO=None):
    """
    Build a simple CNN text classifier, given a token-to-vector model as inputs.
    If exclusive_classes=True, a softmax non-linearity is applied, so that the
    outputs sum to 1. If exclusive_classes=False, a logistic non-linearity
    is applied instead, so that outputs are in the range [0, 1].
    """
    with Model.define_operators({">>": chain}):
        if exclusive_classes:
            output_layer = Softmax(nO=nO, nI=tok2vec.get_dim("nO"))
            model = tok2vec >> list2ragged() >> reduce_mean() >> output_layer
            model.set_ref("output_layer", output_layer)
        else:
            # TODO: experiment with init_w=zero_init
            linear_layer = Linear(nO=nO, nI=tok2vec.get_dim("nO"))
            model = tok2vec >> list2ragged() >> reduce_mean() >> linear_layer >> Logistic()
            model.set_ref("output_layer", linear_layer)
    model.set_ref("tok2vec", tok2vec)
    model.set_dim("nO", nO)
    return model


@registry.architectures.register("spacy.TextCatBOW.v1")
def build_bow_text_classifier(exclusive_classes, ngram_size, no_output_layer, nO=None):
    # Note: original defaults were ngram_size=1 and no_output_layer=False
    with Model.define_operators({">>": chain}):
        model = extract_ngrams(ngram_size, attr=ORTH) >> SparseLinear(nO)
        model.to_cpu()
        if not no_output_layer:
            output_layer = Softmax(nO) if exclusive_classes else Logistic(nO)
            output_layer.to_cpu()
            model = model >> output_layer
            model.set_ref("output_layer", output_layer)
    return model
