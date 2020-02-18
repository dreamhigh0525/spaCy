from thinc.api import Model, chain, clone, concatenate, with_array, uniqued, noop
from thinc.api import with_padded, Maxout, expand_window, HashEmbed, StaticVectors
from thinc.api import residual, LayerNorm, FeatureExtractor

from ..ml import _character_embed
from ..util import make_layer, registry


@registry.architectures.register("spacy.Tok2Vec.v1")
def Tok2Vec(config):
    doc2feats = make_layer(config["@doc2feats"])
    embed = make_layer(config["@embed"])
    encode = make_layer(config["@encode"])
    field_size = 0
    if encode.has_attr("receptive_field"):
        field_size = encode.attrs["receptive_field"]
    tok2vec = chain(doc2feats, with_array(chain(embed, encode), pad=field_size))
    tok2vec.attrs["cfg"] = config
    tok2vec.set_dim("nO", encode.get_dim("nO"))
    tok2vec.set_ref("embed", embed)
    tok2vec.set_ref("encode", encode)
    return tok2vec


@registry.architectures.register("spacy.Doc2Feats.v1")
def Doc2Feats(config):
    columns = config["columns"]
    return FeatureExtractor(columns)


@registry.architectures.register("spacy.MultiHashEmbed.v1")
def MultiHashEmbed(config):
    # For backwards compatibility with models before the architecture registry,
    # we have to be careful to get exactly the same model structure. One subtle
    # trick is that when we define concatenation with the operator, the operator
    # is actually binary associative. So when we write (a | b | c), we're actually
    # getting concatenate(concatenate(a, b), c). That's why the implementation
    # is a bit ugly here.
    cols = config["columns"]
    width = config["width"]
    rows = config["rows"]

    norm = HashEmbed(width, rows, column=cols.index("NORM"), dropout=0.0)
    if config["use_subwords"]:
        prefix = HashEmbed(width, rows // 2, column=cols.index("PREFIX"), dropout=0.0)
        suffix = HashEmbed(width, rows // 2, column=cols.index("SUFFIX"), dropout=0.0)
        shape = HashEmbed(width, rows // 2, column=cols.index("SHAPE"), dropout=0.0)
    if config.get("@pretrained_vectors"):
        glove = make_layer(config["@pretrained_vectors"])
    mix = make_layer(config["@mix"])

    with Model.define_operators({">>": chain, "|": concatenate}):
        if config["use_subwords"] and config["@pretrained_vectors"]:
            mix._layers[0].set_dim("nI", width * 5)
            layer = uniqued(
                (glove | norm | prefix | suffix | shape) >> mix,
                column=cols.index("ORTH"),
            )
        elif config["use_subwords"]:
            mix._layers[0].set_dim("nI", width * 4)
            layer = uniqued(
                (norm | prefix | suffix | shape) >> mix, column=cols.index("ORTH")
            )
        elif config["@pretrained_vectors"]:
            mix._layers[0].set_dim("nI", width * 2)
            layer = uniqued((glove | norm) >> mix, column=cols.index("ORTH"),)
        else:
            layer = norm
    layer.attrs["cfg"] = config
    return layer


@registry.architectures.register("spacy.CharacterEmbed.v1")
def CharacterEmbed(config):
    width = config["width"]
    chars = config["chars"]

    chr_embed = _character_embed.CharacterEmbed(nM=width, nC=chars)
    other_tables = make_layer(config["@embed_features"])
    mix = make_layer(config["@mix"])

    model = chain(concatenate(chr_embed, other_tables), mix)
    model.attrs["cfg"] = config
    return model


@registry.architectures.register("spacy.MaxoutWindowEncoder.v1")
def MaxoutWindowEncoder(config):
    nO = config["width"]
    nW = config["window_size"]
    nP = config["pieces"]
    depth = config["depth"]
    cnn = (
        expand_window(window_size=nW),
        Maxout(nO=nO, nI=nO * ((nW * 2) + 1), nP=nP, dropout=0.0, normalize=True),
    )
    model = clone(residual(cnn), depth)
    model.set_dim("nO", nO)
    model.attrs["receptive_field"] = nW * depth
    return model


@registry.architectures.register("spacy.MishWindowEncoder.v1")
def MishWindowEncoder(config):
    from thinc.api import Mish

    nO = config["width"]
    nW = config["window_size"]
    depth = config["depth"]
    cnn = chain(
        expand_window(window_size=nW),
        Mish(nO=nO, nI=nO * ((nW * 2) + 1)),
        LayerNorm(nO),
    )
    model = clone(residual(cnn), depth)
    model.set_dim("nO", nO)
    return model


@registry.architectures.register("spacy.PretrainedVectors.v1")
def PretrainedVectors(config):
    # TODO: actual vectors instead of name
    return StaticVectors(
        vectors=config["vectors_name"],
        nO=config["width"],
        column=config["column"],
        dropout=0.0,
    )


@registry.architectures.register("spacy.TorchBiLSTMEncoder.v1")
def TorchBiLSTMEncoder(config):
    import torch.nn

    # TODO: FIX
    from thinc.api import PyTorchRNNWrapper

    width = config["width"]
    depth = config["depth"]
    if depth == 0:
        return noop()
    return with_padded(
        PyTorchRNNWrapper(torch.nn.LSTM(width, width // 2, depth, bidirectional=True))
    )


# TODO: update
_EXAMPLE_CONFIG = {
    "@doc2feats": {
        "arch": "Doc2Feats",
        "config": {"columns": ["ID", "NORM", "PREFIX", "SUFFIX", "SHAPE", "ORTH"]},
    },
    "@embed": {
        "arch": "spacy.MultiHashEmbed.v1",
        "config": {
            "width": 96,
            "rows": 2000,
            "columns": ["ID", "NORM", "PREFIX", "SUFFIX", "SHAPE", "ORTH"],
            "use_subwords": True,
            "@pretrained_vectors": {
                "arch": "TransformedStaticVectors",
                "config": {
                    "vectors_name": "en_vectors_web_lg.vectors",
                    "width": 96,
                    "column": 0,
                },
            },
            "@mix": {
                "arch": "LayerNormalizedMaxout",
                "config": {"width": 96, "pieces": 3},
            },
        },
    },
    "@encode": {
        "arch": "MaxoutWindowEncode",
        "config": {"width": 96, "window_size": 1, "depth": 4, "pieces": 3},
    },
}
