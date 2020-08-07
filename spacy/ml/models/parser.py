from typing import Optional, List
from thinc.api import Model, chain, list2array, Linear, zero_init, use_ops
from thinc.types import Floats2d

from ...util import registry
from .._precomputable_affine import PrecomputableAffine
from ..tb_framework import TransitionModel
from ...tokens import Doc


@registry.architectures.register("spacy.TransitionBasedParser.v1")
def build_tb_parser_model(
    tok2vec: Model[List[Doc], List[Floats2d]],
    nr_feature_tokens: int,
    hidden_width: int,
    maxout_pieces: int,
    use_upper: bool = True,
    nO: Optional[int] = None,
) -> Model:
    """
    Build a transition-based parser model. Can apply to NER or dependency-parsing.

    Transition-based parsing is an approach to structured prediction where the
    task of predicting the structure is mapped to a series of state transitions.
    You might find this tutorial helpful as background:
    https://explosion.ai/blog/parsing-english-in-python

    The neural network state prediction model consists of either two or three
    subnetworks:

    * tok2vec: Map each token into a vector representations. This subnetwork
        is run once for each batch.
    * lower: Construct a feature-specific vector for each (token, feature) pair.
        This is also run once for each batch. Constructing the state
        representation is then simply a matter of summing the component features
        and applying the non-linearity.
    * upper (optional): A feed-forward network that predicts scores from the
        state representation. If not present, the output from the lower model is
        used as action scores directly.

    tok2vec (Model[List[Doc], List[Floats2d]]):
        Subnetwork to map tokens into vector representations.
    nr_feature_tokens (int): The number of tokens in the context to use to
        construct the state vector. Valid choices are 1, 2, 3, 6, 8 and 13. The
        2, 8 and 13 feature sets are designed for the parser, while the 3 and 6
        feature sets are designed for the NER. The recommended feature sets are
        3 for NER, and 8 for the dependency parser.

        TODO: This feature should be split into two, state_type: ["deps", "ner"]
        and extra_state_features: [True, False]. This would map into:

        (deps, False): 8
        (deps, True): 13
        (ner, False): 3
        (ner, True): 6

    hidden_width (int): The width of the hidden layer.
    maxout_pieces (int): How many pieces to use in the state prediction layer.
        Recommended values are 1, 2 or 3. If 1, the maxout non-linearity
        is replaced with a ReLu non-linearity if use_upper=True, and no
        non-linearity if use_upper=False.
    use_upper (bool): Whether to use an additional hidden layer after the state
        vector in order to predict the action scores. It is recommended to set
        this to False for large pretrained models such as transformers, and False
        for smaller networks. The upper layer is computed on CPU, which becomes
        a bottleneck on larger GPU-based models, where it's also less necessary.
    nO (int or None): The number of actions the model will predict between.
        Usually inferred from data at the beginning of training, or loaded from
        disk.
    """
    t2v_width = tok2vec.get_dim("nO") if tok2vec.has_dim("nO") else None
    tok2vec = chain(tok2vec, list2array(), Linear(hidden_width, t2v_width),)
    tok2vec.set_dim("nO", hidden_width)
    lower = PrecomputableAffine(
        nO=hidden_width if use_upper else nO,
        nF=nr_feature_tokens,
        nI=tok2vec.get_dim("nO"),
        nP=maxout_pieces,
    )
    if use_upper:
        with use_ops("numpy"):
            # Initialize weights at zero, as it's a classification layer.
            upper = Linear(nO=nO, init_W=zero_init)
    else:
        upper = None
    return TransitionModel(tok2vec, lower, upper)
