---
title: Legacy functions and architectures
teaser: Archived implementations available through spacy-legacy
source: spacy/legacy
---

The [`spacy-legacy`](https://github.com/explosion/spacy-legacy) package includes 
outdated registered functions and architectures. It is installed automatically as 
a dependency of spaCy, and provides backwards compatibility for archived functions 
that may still be used in projects.

You can find the detailed documentation of each such legacy function on this page.

## Architectures {#architectures}

These functions are available from `@spacy.registry.architectures`.

### spacy.Tok2Vec.v1 {#Tok2Vec_v1}

The `spacy.Tok2Vec.v1` architecture was expecting an `encode` model of type 
`Model[Floats2D, Floats2D]` such as `spacy.MaxoutWindowEncoder.v1` or 
`spacy.MishWindowEncoder.v1`.

> #### Example config
>
> ```ini
> [model]
> @architectures = "spacy.Tok2Vec.v1"
>
> [model.embed]
> @architectures = "spacy.CharacterEmbed.v1"
> # ...
>
> [model.encode]
> @architectures = "spacy.MaxoutWindowEncoder.v1"
> # ...
> ```

Construct a tok2vec model out of two subnetworks: one for embedding and one for
encoding. See the
["Embed, Encode, Attend, Predict"](https://explosion.ai/blog/deep-learning-formula-nlp)
blog post for background.

| Name        | Description                                                                                                                                                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `embed`     | Embed tokens into context-independent word vector representations. For example, [CharacterEmbed](/api/architectures#CharacterEmbed) or [MultiHashEmbed](/api/architectures#MultiHashEmbed). ~~Model[List[Doc], List[Floats2d]]~~ |
| `encode`    | Encode context into the embeddings, using an architecture such as a CNN, BiLSTM or transformer. For example, [MaxoutWindowEncoder.v1](/api/legacy#MaxoutWindowEncoder_v1). ~~Model[Floats2d, Floats2d]~~                            |
| **CREATES** | The model using the architecture. ~~Model[List[Doc], List[Floats2d]]~~                                                                                                                                                           |

### spacy.MaxoutWindowEncoder.v1 {#MaxoutWindowEncoder_v1}

The `spacy.MaxoutWindowEncoder.v1` architecture was producing a model of type 
`Model[Floats2D, Floats2D]`. Since `spacy.MaxoutWindowEncoder.v2`, this has been changed to output 
type `Model[List[Floats2d], List[Floats2d]]`.


> #### Example config
>
> ```ini
> [model]
> @architectures = "spacy.MaxoutWindowEncoder.v1"
> width = 128
> window_size = 1
> maxout_pieces = 3
> depth = 4
> ```

Encode context using convolutions with maxout activation, layer normalization
and residual connections.

| Name            | Description                                                                                                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `width`         | The input and output width. These are required to be the same, to allow residual connections. This value will be determined by the width of the inputs. Recommended values are between `64` and `300`. ~~int~~ |
| `window_size`   | The number of words to concatenate around each token to construct the convolution. Recommended value is `1`. ~~int~~                                                                                           |
| `maxout_pieces` | The number of maxout pieces to use. Recommended values are `2` or `3`. ~~int~~                                                                                                                                 |
| `depth`         | The number of convolutional layers. Recommended value is `4`. ~~int~~                                                                                                                                          |
| **CREATES**     | The model using the architecture. ~~Model[Floats2d, Floats2d]~~                                                                                                                                                |

### spacy.MishWindowEncoder.v1 {#MishWindowEncoder_v1}

The `spacy.MishWindowEncoder.v1` architecture was producing a model of type 
`Model[Floats2D, Floats2D]`. Since `spacy.MishWindowEncoder.v2`, this has been changed to output 
type `Model[List[Floats2d], List[Floats2d]]`.

> #### Example config
>
> ```ini
> [model]
> @architectures = "spacy.MishWindowEncoder.v1"
> width = 64
> window_size = 1
> depth = 4
> ```

Encode context using convolutions with
[`Mish`](https://thinc.ai/docs/api-layers#mish) activation, layer normalization
and residual connections.

| Name          | Description                                                                                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `width`       | The input and output width. These are required to be the same, to allow residual connections. This value will be determined by the width of the inputs. Recommended values are between `64` and `300`. ~~int~~ |
| `window_size` | The number of words to concatenate around each token to construct the convolution. Recommended value is `1`. ~~int~~                                                                                           |
| `depth`       | The number of convolutional layers. Recommended value is `4`. ~~int~~                                                                                                                                          |
| **CREATES**   | The model using the architecture. ~~Model[Floats2d, Floats2d]~~                                                                                                                                                |


### spacy.TextCatEnsemble.v1 {#TextCatEnsemble_v1}

The `spacy.TextCatEnsemble.v1` architecture built an internal `tok2vec` and `linear_model`. 
Since `spacy.TextCatEnsemble.v2`, this has been refactored so that the `TextCatEnsemble` takes these 
two sublayers as input.

> #### Example Config
>
> ```ini
> [model]
> @architectures = "spacy.TextCatEnsemble.v1"
> exclusive_classes = false
> pretrained_vectors = null
> width = 64
> embed_size = 2000
> conv_depth = 2
> window_size = 1
> ngram_size = 1
> dropout = null
> nO = null
> ```

Stacked ensemble of a bag-of-words model and a neural network model. The neural
network has an internal CNN Tok2Vec layer and uses attention.

| Name                 | Description                                                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exclusive_classes`  | Whether or not categories are mutually exclusive. ~~bool~~                                                                                                                                     |
| `pretrained_vectors` | Whether or not pretrained vectors will be used in addition to the feature vectors. ~~bool~~                                                                                                    |
| `width`              | Output dimension of the feature encoding step. ~~int~~                                                                                                                                         |
| `embed_size`         | Input dimension of the feature encoding step. ~~int~~                                                                                                                                          |
| `conv_depth`         | Depth of the tok2vec layer. ~~int~~                                                                                                                                                            |
| `window_size`        | The number of contextual vectors to [concatenate](https://thinc.ai/docs/api-layers#expand_window) from the left and from the right. ~~int~~                                                    |
| `ngram_size`         | Determines the maximum length of the n-grams in the BOW model. For instance, `ngram_size=3`would give unigram, trigram and bigram features. ~~int~~                                            |
| `dropout`            | The dropout rate. ~~float~~                                                                                                                                                                    |
| `nO`                 | Output dimension, determined by the number of different labels. If not set, the [`TextCategorizer`](/api/textcategorizer) component will set it when `initialize` is called. ~~Optional[int]~~ |
| **CREATES**          | The model using the architecture. ~~Model[List[Doc], Floats2d]~~                                                                                                                               |


## Loggers {#loggers}

These functions are available from `@spacy.registry.loggers`.

### spacy.WandbLogger.v1 {#WandbLogger_v1}

The first version of the [`WandbLogger`](/api/top-level#WandbLogger) did not yet 
support the `log_dataset_dir` and `model_log_interval` arguments.

> #### Example config
>
> ```ini
> [training.logger]
> @loggers = "spacy.WandbLogger.v1"
> project_name = "monitor_spacy_training"
> remove_config_values = ["paths.train", "paths.dev", "corpora.train.path", "corpora.dev.path"]
> ```
| Name                   | Description                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `project_name`         | The name of the project in the Weights & Biases interface. The project will be created automatically if it doesn't exist yet. ~~str~~ |
| `remove_config_values` | A list of values to include from the config before it is uploaded to W&B (default: empty). ~~List[str]~~                              |
