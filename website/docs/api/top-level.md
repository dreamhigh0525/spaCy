---
title: Top-level Functions
menu:
  - ['spacy', 'spacy']
  - ['displacy', 'displacy']
  - ['registry', 'registry']
  - ['Loggers', 'loggers']
  - ['Batchers', 'batchers']
  - ['Data & Alignment', 'gold']
  - ['Utility Functions', 'util']
---

## spaCy {#spacy hidden="true"}

### spacy.load {#spacy.load tag="function" model="any"}

Load a model using the name of an installed
[model package](/usage/training#models-generating), a string path or a
`Path`-like object. spaCy will try resolving the load argument in this order. If
a model is loaded from a model name, spaCy will assume it's a Python package and
import it and call the model's own `load()` method. If a model is loaded from a
path, spaCy will assume it's a data directory, load its
[`config.cfg`](/api/data-formats#config) and use the language and pipeline
information to construct the `Language` class. The data will be loaded in via
[`Language.from_disk`](/api/language#from_disk).

<Infobox variant="warning" title="Changed in v3.0">

As of v3.0, the `disable` keyword argument specifies components to load but
disable, instead of components to not load at all. Those components can now be
specified separately using the new `exclude` keyword argument.

</Infobox>

> #### Example
>
> ```python
> nlp = spacy.load("en_core_web_sm") # package
> nlp = spacy.load("/path/to/en") # string path
> nlp = spacy.load(Path("/path/to/en")) # pathlib Path
>
> nlp = spacy.load("en_core_web_sm", exclude=["parser", "tagger"])
> ```

| Name                                 | Description                                                                                                                                                                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                               | Model to load, i.e. package name or path. ~~Union[str, Path]~~                                                                                                                                                                                 |
| _keyword-only_                       |                                                                                                                                                                                                                                                |
| `disable`                            | Names of pipeline components to [disable](/usage/processing-pipelines#disabling). Disabled pipes will be loaded but they won't be run unless you explicitly enable them by calling [nlp.enable_pipe](/api/language#enable_pipe). ~~List[str]~~ |
| `exclude` <Tag variant="new">3</Tag> | Names of pipeline components to [exclude](/usage/processing-pipelines#disabling). Excluded components won't be loaded. ~~List[str]~~                                                                                                           |
| `config` <Tag variant="new">3</Tag>  | Optional config overrides, either as nested dict or dict keyed by section value in dot notation, e.g. `"components.name.value"`. ~~Union[Dict[str, Any], Config]~~                                                                             |
| **RETURNS**                          | A `Language` object with the loaded model. ~~Language~~                                                                                                                                                                                        |

Essentially, `spacy.load()` is a convenience wrapper that reads the model's
[`config.cfg`](/api/data-formats#config), uses the language and pipeline
information to construct a `Language` object, loads in the model data and
returns it.

```python
### Abstract example
cls = util.get_lang_class(lang)         #  get language for ID, e.g. "en"
nlp = cls()                             #  initialize the language
for name in pipeline:
    nlp.add_pipe(name)                  #  add component to pipeline
nlp.from_disk(model_data_path)          #  load in model data
```

### spacy.blank {#spacy.blank tag="function" new="2"}

Create a blank model of a given language class. This function is the twin of
`spacy.load()`.

> #### Example
>
> ```python
> nlp_en = spacy.blank("en")   # equivalent to English()
> nlp_de = spacy.blank("de")   # equivalent to German()
> ```

| Name        | Description                                                                                              |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| `name`      | [ISO code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the language class to load. ~~str~~ |
| **RETURNS** | An empty `Language` object of the appropriate subclass. ~~Language~~                                     |

### spacy.info {#spacy.info tag="function"}

The same as the [`info` command](/api/cli#info). Pretty-print information about
your installation, models and local setup from within spaCy. To get the model
meta data as a dictionary instead, you can use the `meta` attribute on your
`nlp` object with a loaded model, e.g. `nlp.meta`.

> #### Example
>
> ```python
> spacy.info()
> spacy.info("en_core_web_sm")
> markdown = spacy.info(markdown=True, silent=True)
> ```

| Name           | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `model`        | A model, i.e. a package name or path (optional). ~~Optional[str]~~ |
| _keyword-only_ |                                                                    |
| `markdown`     | Print information as Markdown. ~~bool~~                            |
| `silent`       | Don't print anything, just return. ~~bool~~                        |

### spacy.explain {#spacy.explain tag="function"}

Get a description for a given POS tag, dependency label or entity type. For a
list of available terms, see
[`glossary.py`](https://github.com/explosion/spaCy/tree/master/spacy/glossary.py).

> #### Example
>
> ```python
> spacy.explain("NORP")
> # Nationalities or religious or political groups
>
> doc = nlp("Hello world")
> for word in doc:
>    print(word.text, word.tag_, spacy.explain(word.tag_))
> # Hello UH interjection
> # world NN noun, singular or mass
> ```

| Name        | Description                                                                |
| ----------- | -------------------------------------------------------------------------- |
| `term`      | Term to explain. ~~str~~                                                   |
| **RETURNS** | The explanation, or `None` if not found in the glossary. ~~Optional[str]~~ |

### spacy.prefer_gpu {#spacy.prefer_gpu tag="function" new="2.0.14"}

Allocate data and perform operations on [GPU](/usage/#gpu), if available. If
data has already been allocated on CPU, it will not be moved. Ideally, this
function should be called right after importing spaCy and _before_ loading any
models.

> #### Example
>
> ```python
> import spacy
> activated = spacy.prefer_gpu()
> nlp = spacy.load("en_core_web_sm")
> ```

| Name        | Description                             |
| ----------- | --------------------------------------- |
| **RETURNS** | Whether the GPU was activated. ~~bool~~ |

### spacy.require_gpu {#spacy.require_gpu tag="function" new="2.0.14"}

Allocate data and perform operations on [GPU](/usage/#gpu). Will raise an error
if no GPU is available. If data has already been allocated on CPU, it will not
be moved. Ideally, this function should be called right after importing spaCy
and _before_ loading any models.

> #### Example
>
> ```python
> import spacy
> spacy.require_gpu()
> nlp = spacy.load("en_core_web_sm")
> ```

| Name        | Description     |
| ----------- | --------------- |
| **RETURNS** | `True` ~~bool~~ |

## displaCy {#displacy source="spacy/displacy"}

As of v2.0, spaCy comes with a built-in visualization suite. For more info and
examples, see the usage guide on [visualizing spaCy](/usage/visualizers).

### displacy.serve {#displacy.serve tag="method" new="2"}

Serve a dependency parse tree or named entity visualization to view it in your
browser. Will run a simple web server.

> #### Example
>
> ```python
> import spacy
> from spacy import displacy
> nlp = spacy.load("en_core_web_sm")
> doc1 = nlp("This is a sentence.")
> doc2 = nlp("This is another sentence.")
> displacy.serve([doc1, doc2], style="dep")
> ```

| Name      | Description                                                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `docs`    | Document(s) or span(s) to visualize. ~~Union[Iterable[Union[Doc, Span]], Doc, Span]~~                                                                              |
| `style`   | Visualization style, `"dep"` or `"ent"`. Defaults to `"dep"`. ~~str~~                                                                                              |
| `page`    | Render markup as full HTML page. Defaults to `True`. ~~bool~~                                                                                                      |
| `minify`  | Minify HTML markup. Defaults to `False`. ~~bool~~                                                                                                                  |
| `options` | [Visualizer-specific options](#displacy_options), e.g. colors. ~~Dict[str, Any]~~                                                                                  |
| `manual`  | Don't parse `Doc` and instead, expect a dict or list of dicts. [See here](/usage/visualizers#manual-usage) for formats and examples. Defaults to `False`. ~~bool~~ |
| `port`    | Port to serve visualization. Defaults to `5000`. ~~int~~                                                                                                           |
| `host`    | Host to serve visualization. Defaults to `"0.0.0.0"`. ~~str~~                                                                                                      |

### displacy.render {#displacy.render tag="method" new="2"}

Render a dependency parse tree or named entity visualization.

> #### Example
>
> ```python
> import spacy
> from spacy import displacy
> nlp = spacy.load("en_core_web_sm")
> doc = nlp("This is a sentence.")
> html = displacy.render(doc, style="dep")
> ```

| Name        | Description                                                                                                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs`      | Document(s) or span(s) to visualize. ~~Union[Iterable[Union[Doc, Span]], Doc, Span]~~                                                                                                  |
| `style`     | Visualization style, `"dep"` or `"ent"`. Defaults to `"dep"`. ~~str~~                                                                                                                  |
| `page`      | Render markup as full HTML page. Defaults to `True`. ~~bool~~                                                                                                                          |
| `minify`    | Minify HTML markup. Defaults to `False`. ~~bool~~                                                                                                                                      |
| `options`   | [Visualizer-specific options](#displacy_options), e.g. colors. ~~Dict[str, Any]~~                                                                                                      |
| `manual`    | Don't parse `Doc` and instead, expect a dict or list of dicts. [See here](/usage/visualizers#manual-usage) for formats and examples. Defaults to `False`. ~~bool~~                     |
| `jupyter`   | Explicitly enable or disable "[Jupyter](http://jupyter.org/) mode" to return markup ready to be rendered in a notebook. Detected automatically if `None` (default). ~~Optional[bool]~~ |
| **RETURNS** | The rendered HTML markup. ~~str~~                                                                                                                                                      |

### Visualizer options {#displacy_options}

The `options` argument lets you specify additional settings for each visualizer.
If a setting is not present in the options, the default value will be used.

#### Dependency Visualizer options {#options-dep}

> #### Example
>
> ```python
> options = {"compact": True, "color": "blue"}
> displacy.serve(doc, style="dep", options=options)
> ```

| Name                                       | Description                                                                                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `fine_grained`                             | Use fine-grained part-of-speech tags (`Token.tag_`) instead of coarse-grained tags (`Token.pos_`). Defaults to `False`. ~~bool~~             |
| `add_lemma` <Tag variant="new">2.2.4</Tag> | Print the lemma's in a separate row below the token texts. Defaults to `False`. ~~bool~~                                                     |
| `collapse_punct`                           | Attach punctuation to tokens. Can make the parse more readable, as it prevents long arcs to attach punctuation. Defaults to `True`. ~~bool~~ |
| `collapse_phrases`                         | Merge noun phrases into one token. Defaults to `False`. ~~bool~~                                                                             |
| `compact`                                  | "Compact mode" with square arrows that takes up less space. Defaults to `False`. ~~bool~~                                                    |
| `color`                                    | Text color (HEX, RGB or color names). Defaults to `"#000000"`. ~~str~~                                                                       |
| `bg`                                       | Background color (HEX, RGB or color names). Defaults to `"#ffffff"`. ~~str~~                                                                 |
| `font`                                     | Font name or font family for all text. Defaults to `"Arial"`. ~~str~~                                                                        |
| `offset_x`                                 | Spacing on left side of the SVG in px. Defaults to `50`. ~~int~~                                                                             |
| `arrow_stroke`                             | Width of arrow path in px. Defaults to `2`. ~~int~~                                                                                          |
| `arrow_width`                              | Width of arrow head in px. Defaults to `10` in regular mode and `8` in compact mode. ~~int~~                                                 |
| `arrow_spacing`                            | Spacing between arrows in px to avoid overlaps. Defaults to `20` in regular mode and `12` in compact mode. ~~int~~                           |
| `word_spacing`                             | Vertical spacing between words and arcs in px. Defaults to `45`. ~~int~~                                                                     |
| `distance`                                 | Distance between words in px. Defaults to `175` in regular mode and `150` in compact mode. ~~int~~                                           |

#### Named Entity Visualizer options {#displacy_options-ent}

> #### Example
>
> ```python
> options = {"ents": ["PERSON", "ORG", "PRODUCT"],
>            "colors": {"ORG": "yellow"}}
> displacy.serve(doc, style="ent", options=options)
> ```

| Name                                    | Description                                                                                                                                                                                                                                                                 |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ents`                                  | Entity types to highlight or `None` for all types (default). ~~Optional[List[str]]~~                                                                                                                                                                                        |
| `colors`                                | Color overrides. Entity types should be mapped to color names or values. ~~Dict[str, str]~~                                                                                                                                                                                 |
| `template` <Tag variant="new">2.2</Tag> | Optional template to overwrite the HTML used to render entity spans. Should be a format string and can use `{bg}`, `{text}` and `{label}`. See [`templates.py`](https://github.com/explosion/spaCy/blob/master/spacy/displacy/templates.py) for examples. ~~Optional[str]~~ |

By default, displaCy comes with colors for all entity types used by
[spaCy models](/models). If you're using custom entity types, you can use the
`colors` setting to add your own colors for them. Your application or model
package can also expose a
[`spacy_displacy_colors` entry point](/usage/saving-loading#entry-points-displacy)
to add custom labels and their colors automatically.

## registry {#registry source="spacy/util.py" new="3"}

spaCy's function registry extends
[Thinc's `registry`](https://thinc.ai/docs/api-config#registry) and allows you
to map strings to functions. You can register functions to create architectures,
optimizers, schedules and more, and then refer to them and set their arguments
in your [config file](/usage/training#config). Python type hints are used to
validate the inputs. See the
[Thinc docs](https://thinc.ai/docs/api-config#registry) for details on the
`registry` methods and our helper library
[`catalogue`](https://github.com/explosion/catalogue) for some background on the
concept of function registries. spaCy also uses the function registry for
language subclasses, model architecture, lookups and pipeline component
factories.

> #### Example
>
> ```python
> from typing import Iterator
> import spacy
>
> @spacy.registry.schedules("waltzing.v1")
> def waltzing() -> Iterator[float]:
>     i = 0
>     while True:
>         yield i % 3 + 1
>         i += 1
> ```

| Registry name     | Description                                                                                                                                                                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `architectures`   | Registry for functions that create [model architectures](/api/architectures). Can be used to register custom model architectures and reference them in the `config.cfg`.                                                                           |
| `assets`          | Registry for data assets, knowledge bases etc.                                                                                                                                                                                                     |
| `batchers`        | Registry for training and evaluation [data batchers](#batchers).                                                                                                                                                                                   |
| `callbacks`       | Registry for custom callbacks to [modify the `nlp` object](/usage/training#custom-code-nlp-callbacks) before training.                                                                                                                             |
| `displacy_colors` | Registry for custom color scheme for the [`displacy` NER visualizer](/usage/visualizers). Automatically reads from [entry points](/usage/saving-loading#entry-points).                                                                             |
| `factories`       | Registry for functions that create [pipeline components](/usage/processing-pipelines#custom-components). Added automatically when you use the `@spacy.component` decorator and also reads from [entry points](/usage/saving-loading#entry-points). |
| `initializers`    | Registry for functions that create [initializers](https://thinc.ai/docs/api-initializers).                                                                                                                                                         |
| `languages`       | Registry for language-specific `Language` subclasses. Automatically reads from [entry points](/usage/saving-loading#entry-points).                                                                                                                 |
| `layers`          | Registry for functions that create [layers](https://thinc.ai/docs/api-layers).                                                                                                                                                                     |
| `loggers`         | Registry for functions that log [training results](/usage/training).                                                                                                                                                                               |
| `lookups`         | Registry for large lookup tables available via `vocab.lookups`.                                                                                                                                                                                    |
| `losses`          | Registry for functions that create [losses](https://thinc.ai/docs/api-loss).                                                                                                                                                                       |
| `optimizers`      | Registry for functions that create [optimizers](https://thinc.ai/docs/api-optimizers).                                                                                                                                                             |
| `readers`         | Registry for training and evaluation data readers like [`Corpus`](/api/corpus).                                                                                                                                                                    |
| `schedules`       | Registry for functions that create [schedules](https://thinc.ai/docs/api-schedules).                                                                                                                                                               |
| `tokenizers`      | Registry for tokenizer factories. Registered functions should return a callback that receives the `nlp` object and returns a [`Tokenizer`](/api/tokenizer) or a custom callable.                                                                   |

### spacy-transformers registry {#registry-transformers}

The following registries are added by the
[`spacy-transformers`](https://github.com/explosion/spacy-transformers) package.
See the [`Transformer`](/api/transformer) API reference and
[usage docs](/usage/embeddings-transformers) for details.

> #### Example
>
> ```python
> import spacy_transformers
>
> @spacy_transformers.registry.annotation_setters("my_annotation_setter.v1")
> def configure_custom_annotation_setter():
>     def annotation_setter(docs, trf_data) -> None:
>        # Set annotations on the docs
>
>     return annotation_setter
> ```

| Registry name                                               | Description                                                                                                                                                                                                                                       |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`span_getters`](/api/transformer#span_getters)             | Registry for functions that take a batch of `Doc` objects and return a list of `Span` objects to process by the transformer, e.g. sentences.                                                                                                      |
| [`annotation_setters`](/api/transformer#annotation_setters) | Registry for functions that create annotation setters. Annotation setters are functions that take a batch of `Doc` objects and a [`FullTransformerBatch`](/api/transformer#fulltransformerbatch) and can set additional annotations on the `Doc`. |

## Loggers {#loggers source="spacy/gold/loggers.py" new="3"}

A logger records the training results. When a logger is created, two functions
are returned: one for logging the information for each training step, and a
second function that is called to finalize the logging when the training is
finished. To log each training step, a
[dictionary](/usage/training#custom-logging) is passed on from the
[training script](/api/cli#train), including information such as the training
loss and the accuracy scores on the development set.

There are two built-in logging functions: a logger printing results to the
console in tabular format (which is the default), and one that also sends the
results to a [Weights & Biases](https://www.wandb.com/) dashboard. Instead of
using one of the built-in loggers listed here, you can also
[implement your own](/usage/training#custom-logging).

> #### Example config
>
> ```ini
> [training.logger]
> @loggers = "spacy.ConsoleLogger.v1"
> ```

#### spacy.ConsoleLogger.v1 {#ConsoleLogger tag="registered function"}

Writes the results of a training step to the console in a tabular format.

#### spacy.WandbLogger.v1 {#WandbLogger tag="registered function"}

> #### Installation
>
> ```bash
> $ pip install wandb
> $ wandb login
> ```

Built-in logger that sends the results of each training step to the dashboard of
the [Weights & Biases](https://www.wandb.com/) tool. To use this logger, Weights
& Biases should be installed, and you should be logged in. The logger will send
the full config file to W&B, as well as various system information such as
memory utilization, network traffic, disk IO, GPU statistics, etc. This will
also include information such as your hostname and operating system, as well as
the location of your Python executable.

<Infobox variant="warning">

Note that by default, the full (interpolated)
[training config](/usage/training#config) is sent over to the W&B dashboard. If
you prefer to **exclude certain information** such as path names, you can list
those fields in "dot notation" in the `remove_config_values` parameter. These
fields will then be removed from the config before uploading, but will otherwise
remain in the config file stored on your local system.

</Infobox>

> #### Example config
>
> ```ini
> [training.logger]
> @loggers = "spacy.WandbLogger.v1"
> project_name = "monitor_spacy_training"
> remove_config_values = ["paths.train", "paths.dev", "training.dev_corpus.path", "training.train_corpus.path"]
> ```

| Name                   | Description                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `project_name`         | The name of the project in the Weights & Biases interface. The project will be created automatically if it doesn't exist yet. ~~str~~ |
| `remove_config_values` | A list of values to include from the config before it is uploaded to W&B (default: empty). ~~List[str]~~                              |

## Batchers {#batchers source="spacy/gold/batchers.py" new="3"}

A data batcher implements a batching strategy that essentially turns a stream of
items into a stream of batches, with each batch consisting of one item or a list
of items. During training, the models update their weights after processing one
batch at a time. Typical batching strategies include presenting the training
data as a stream of batches with similar sizes, or with increasing batch sizes.
See the Thinc documentation on
[`schedules`](https://thinc.ai/docs/api-schedules) for a few standard examples.

Instead of using one of the built-in batchers listed here, you can also
[implement your own](/usage/training#custom-code-readers-batchers), which may or
may not use a custom schedule.

#### batch_by_words.v1 {#batch_by_words tag="registered function"}

Create minibatches of roughly a given number of words. If any examples are
longer than the specified batch length, they will appear in a batch by
themselves, or be discarded if `discard_oversize` is set to `True`. The argument
`docs` can be a list of strings, [`Doc`](/api/doc) objects or
[`Example`](/api/example) objects.

> #### Example config
>
> ```ini
> [training.batcher]
> @batchers = "batch_by_words.v1"
> size = 100
> tolerance = 0.2
> discard_oversize = false
> get_length = null
> ```

| Name               | Description                                                                                                                                                                             |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `seqs`             | The sequences to minibatch. ~~Iterable[Any]~~                                                                                                                                           |
| `size`             | The target number of words per batch. Can also be a block referencing a schedule, e.g. [`compounding`](https://thinc.ai/docs/api-schedules/#compounding). ~~Union[int, Sequence[int]]~~ |
| `tolerance`        | What percentage of the size to allow batches to exceed. ~~float~~                                                                                                                       |
| `discard_oversize` | Whether to discard sequences that by themselves exceed the tolerated size. ~~bool~~                                                                                                     |
| `get_length`       | Optional function that receives a sequence item and returns its length. Defaults to the built-in `len()` if not set. ~~Optional[Callable[[Any], int]]~~                                 |

#### batch_by_sequence.v1 {#batch_by_sequence tag="registered function"}

> #### Example config
>
> ```ini
> [training.batcher]
> @batchers = "batch_by_sequence.v1"
> size = 32
> get_length = null
> ```

Create a batcher that creates batches of the specified size.

| Name         | Description                                                                                                                                                                             |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `size`       | The target number of items per batch. Can also be a block referencing a schedule, e.g. [`compounding`](https://thinc.ai/docs/api-schedules/#compounding). ~~Union[int, Sequence[int]]~~ |
| `get_length` | Optional function that receives a sequence item and returns its length. Defaults to the built-in `len()` if not set. ~~Optional[Callable[[Any], int]]~~                                 |

#### batch_by_padded.v1 {#batch_by_padded tag="registered function"}

> #### Example config
>
> ```ini
> [training.batcher]
> @batchers = "batch_by_padded.v1"
> size = 100
> buffer = 256
> discard_oversize = false
> get_length = null
> ```

Minibatch a sequence by the size of padded batches that would result, with
sequences binned by length within a window. The padded size is defined as the
maximum length of sequences within the batch multiplied by the number of
sequences in the batch.

| Name               | Description                                                                                                                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `size`             | The largest padded size to batch sequences into. Can also be a block referencing a schedule, e.g. [`compounding`](https://thinc.ai/docs/api-schedules/#compounding). ~~Union[int, Sequence[int]]~~                                          |
| `buffer`           | The number of sequences to accumulate before sorting by length. A larger buffer will result in more even sizing, but if the buffer is very large, the iteration order will be less random, which can result in suboptimal training. ~~int~~ |
| `discard_oversize` | Whether to discard sequences that are by themselves longer than the largest padded batch size. ~~bool~~                                                                                                                                     |
| `get_length`       | Optional function that receives a sequence item and returns its length. Defaults to the built-in `len()` if not set. ~~Optional[Callable[[Any], int]]~~                                                                                     |

## Training data and alignment {#gold source="spacy/gold"}

### gold.biluo_tags_from_offsets {#biluo_tags_from_offsets tag="function"}

Encode labelled spans into per-token tags, using the
[BILUO scheme](/usage/linguistic-features#accessing-ner) (Begin, In, Last, Unit,
Out). Returns a list of strings, describing the tags. Each tag string will be of
the form of either `""`, `"O"` or `"{action}-{label}"`, where action is one of
`"B"`, `"I"`, `"L"`, `"U"`. The string `"-"` is used where the entity offsets
don't align with the tokenization in the `Doc` object. The training algorithm
will view these as missing values. `O` denotes a non-entity token. `B` denotes
the beginning of a multi-token entity, `I` the inside of an entity of three or
more tokens, and `L` the end of an entity of two or more tokens. `U` denotes a
single-token entity.

> #### Example
>
> ```python
> from spacy.gold import biluo_tags_from_offsets
>
> doc = nlp("I like London.")
> entities = [(7, 13, "LOC")]
> tags = biluo_tags_from_offsets(doc, entities)
> assert tags == ["O", "O", "U-LOC", "O"]
> ```

| Name        | Description                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `doc`       | The document that the entity offsets refer to. The output tags will refer to the token boundaries within the document. ~~Doc~~                                                             |
| `entities`  | A sequence of `(start, end, label)` triples. `start` and `end` should be character-offset integers denoting the slice into the original string. ~~List[Tuple[int, int, Union[str, int]]]~~ |
| **RETURNS** | A list of strings, describing the [BILUO](/usage/linguistic-features#accessing-ner) tags. ~~List[str]~~                                                                                    |

### gold.offsets_from_biluo_tags {#offsets_from_biluo_tags tag="function"}

Encode per-token tags following the
[BILUO scheme](/usage/linguistic-features#accessing-ner) into entity offsets.

> #### Example
>
> ```python
> from spacy.gold import offsets_from_biluo_tags
>
> doc = nlp("I like London.")
> tags = ["O", "O", "U-LOC", "O"]
> entities = offsets_from_biluo_tags(doc, tags)
> assert entities == [(7, 13, "LOC")]
> ```

| Name        | Description                                                                                                                                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `doc`       | The document that the BILUO tags refer to. ~~Doc~~                                                                                                                                                                                                           |
| `entities`  | A sequence of [BILUO](/usage/linguistic-features#accessing-ner) tags with each tag describing one token. Each tag string will be of the form of either `""`, `"O"` or `"{action}-{label}"`, where action is one of `"B"`, `"I"`, `"L"`, `"U"`. ~~List[str]~~ |
| **RETURNS** | A sequence of `(start, end, label)` triples. `start` and `end` will be character-offset integers denoting the slice into the original string. ~~List[Tuple[int, int, str]]~~                                                                                 |

### gold.spans_from_biluo_tags {#spans_from_biluo_tags tag="function" new="2.1"}

Encode per-token tags following the
[BILUO scheme](/usage/linguistic-features#accessing-ner) into
[`Span`](/api/span) objects. This can be used to create entity spans from
token-based tags, e.g. to overwrite the `doc.ents`.

> #### Example
>
> ```python
> from spacy.gold import spans_from_biluo_tags
>
> doc = nlp("I like London.")
> tags = ["O", "O", "U-LOC", "O"]
> doc.ents = spans_from_biluo_tags(doc, tags)
> ```

| Name        | Description                                                                                                                                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `doc`       | The document that the BILUO tags refer to. ~~Doc~~                                                                                                                                                                                                           |
| `entities`  | A sequence of [BILUO](/usage/linguistic-features#accessing-ner) tags with each tag describing one token. Each tag string will be of the form of either `""`, `"O"` or `"{action}-{label}"`, where action is one of `"B"`, `"I"`, `"L"`, `"U"`. ~~List[str]~~ |
| **RETURNS** | A sequence of `Span` objects with added entity labels. ~~List[Span]~~                                                                                                                                                                                        |

## Utility functions {#util source="spacy/util.py"}

spaCy comes with a small collection of utility functions located in
[`spacy/util.py`](https://github.com/explosion/spaCy/tree/master/spacy/util.py).
Because utility functions are mostly intended for **internal use within spaCy**,
their behavior may change with future releases. The functions documented on this
page should be safe to use and we'll try to ensure backwards compatibility.
However, we recommend having additional tests in place if your application
depends on any of spaCy's utilities.

### util.get_lang_class {#util.get_lang_class tag="function"}

Import and load a `Language` class. Allows lazy-loading
[language data](/usage/adding-languages) and importing languages using the
two-letter language code. To add a language code for a custom language class,
you can register it using the [`@registry.languages`](/api/top-level#registry)
decorator.

> #### Example
>
> ```python
> for lang_id in ["en", "de"]:
>     lang_class = util.get_lang_class(lang_id)
>     lang = lang_class()
> ```

| Name        | Description                                    |
| ----------- | ---------------------------------------------- |
| `lang`      | Two-letter language code, e.g. `"en"`. ~~str~~ |
| **RETURNS** | The respective subclass. ~~Language~~          |

### util.lang_class_is_loaded {#util.lang_class_is_loaded tag="function" new="2.1"}

Check whether a `Language` subclass is already loaded. `Language` subclasses are
loaded lazily, to avoid expensive setup code associated with the language data.

> #### Example
>
> ```python
> lang_cls = util.get_lang_class("en")
> assert util.lang_class_is_loaded("en") is True
> assert util.lang_class_is_loaded("de") is False
> ```

| Name        | Description                                    |
| ----------- | ---------------------------------------------- |
| `name`      | Two-letter language code, e.g. `"en"`. ~~str~~ |
| **RETURNS** | Whether the class has been loaded. ~~bool~~    |

### util.load_model {#util.load_model tag="function" new="2"}

Load a model from a package or data path. If called with a package name, spaCy
will assume the model is a Python package and import and call its `load()`
method. If called with a path, spaCy will assume it's a data directory, read the
language and pipeline settings from the [`config.cfg`](/api/data-formats#config)
and create a `Language` object. The model data will then be loaded in via
[`Language.from_disk`](/api/language#from_disk).

> #### Example
>
> ```python
> nlp = util.load_model("en_core_web_sm")
> nlp = util.load_model("en_core_web_sm", exclude=["ner"])
> nlp = util.load_model("/path/to/data")
> ```

| Name                                 | Description                                                                                                                                                                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                               | Package name or model path. ~~str~~                                                                                                                                                                                                            |
| `vocab` <Tag variant="new">3</Tag>   | Optional shared vocab to pass in on initialization. If `True` (default), a new `Vocab` object will be created. ~~Union[Vocab, bool]~~.                                                                                                         |
| `disable`                            | Names of pipeline components to [disable](/usage/processing-pipelines#disabling). Disabled pipes will be loaded but they won't be run unless you explicitly enable them by calling [nlp.enable_pipe](/api/language#enable_pipe). ~~List[str]~~ |
| `exclude` <Tag variant="new">3</Tag> | Names of pipeline components to [exclude](/usage/processing-pipelines#disabling). Excluded components won't be loaded. ~~List[str]~~                                                                                                           |
| `config` <Tag variant="new">3</Tag>  | Config overrides as nested dict or flat dict keyed by section values in dot notation, e.g. `"nlp.pipeline"`. ~~Union[Dict[str, Any], Config]~~                                                                                                 |
| **RETURNS**                          | `Language` class with the loaded model. ~~Language~~                                                                                                                                                                                           |

### util.load_model_from_init_py {#util.load_model_from_init_py tag="function" new="2"}

A helper function to use in the `load()` method of a model package's
[`__init__.py`](https://github.com/explosion/spacy-models/tree/master/template/model/xx_model_name/__init__.py).

> #### Example
>
> ```python
> from spacy.util import load_model_from_init_py
>
> def load(**overrides):
>     return load_model_from_init_py(__file__, **overrides)
> ```

| Name                                 | Description                                                                                                                                                                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `init_file`                          | Path to model's `__init__.py`, i.e. `__file__`. ~~Union[str, Path]~~                                                                                                                                                                           |
| `vocab` <Tag variant="new">3</Tag>   | Optional shared vocab to pass in on initialization. If `True` (default), a new `Vocab` object will be created. ~~Union[Vocab, bool]~~.                                                                                                         |
| `disable`                            | Names of pipeline components to [disable](/usage/processing-pipelines#disabling). Disabled pipes will be loaded but they won't be run unless you explicitly enable them by calling [nlp.enable_pipe](/api/language#enable_pipe). ~~List[str]~~ |
| `exclude` <Tag variant="new">3</Tag> | Names of pipeline components to [exclude](/usage/processing-pipelines#disabling). Excluded components won't be loaded. ~~List[str]~~                                                                                                           |
| `config` <Tag variant="new">3</Tag>  | Config overrides as nested dict or flat dict keyed by section values in dot notation, e.g. `"nlp.pipeline"`. ~~Union[Dict[str, Any], Config]~~                                                                                                 |
| **RETURNS**                          | `Language` class with the loaded model. ~~Language~~                                                                                                                                                                                           |

### util.load_config {#util.load_config tag="function" new="3"}

Load a model's [`config.cfg`](/api/data-formats#config) from a file path. The
config typically includes details about the model pipeline and how its
components are created, as well as all training settings and hyperparameters.

> #### Example
>
> ```python
> config = util.load_config("/path/to/model/config.cfg")
> print(config.to_str())
> ```

| Name          | Description                                                                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path`        | Path to the model's `config.cfg`. ~~Union[str, Path]~~                                                                                                                      |
| `overrides`   | Optional config overrides to replace in loaded config. Can be provided as nested dict, or as flat dict with keys in dot notation, e.g. `"nlp.pipeline"`. ~~Dict[str, Any]~~ |
| `interpolate` | Whether to interpolate the config and replace variables like `${paths.train}` with their values. Defaults to `False`. ~~bool~~                                              |
| **RETURNS**   | The model's config. ~~Config~~                                                                                                                                              |

### util.load_meta {#util.load_meta tag="function" new="3"}

Get a model's [`meta.json`](/api/data-formats#meta) from a file path and
validate its contents.

> #### Example
>
> ```python
> meta = util.load_meta("/path/to/model/meta.json")
> ```

| Name        | Description                                           |
| ----------- | ----------------------------------------------------- |
| `path`      | Path to the model's `meta.json`. ~~Union[str, Path]~~ |
| **RETURNS** | The model's meta data. ~~Dict[str, Any]~~             |

### util.get_installed_models {#util.get_installed_models tag="function" new="3"}

List all model packages installed in the current environment. This will include
any spaCy model that was packaged with [`spacy package`](/api/cli#package).
Under the hood, model packages expose a Python entry point that spaCy can check,
without having to load the model.

> #### Example
>
> ```python
> model_names = util.get_installed_models()
> ```

| Name        | Description                                                                        |
| ----------- | ---------------------------------------------------------------------------------- |
| **RETURNS** | The string names of the models installed in the current environment. ~~List[str]~~ |

### util.is_package {#util.is_package tag="function"}

Check if string maps to a package installed via pip. Mainly used to validate
[model packages](/usage/models).

> #### Example
>
> ```python
> util.is_package("en_core_web_sm") # True
> util.is_package("xyz") # False
> ```

| Name        | Description                                           |
| ----------- | ----------------------------------------------------- |
| `name`      | Name of package. ~~str~~                              |
| **RETURNS** | `True` if installed package, `False` if not. ~~bool~~ |

### util.get_package_path {#util.get_package_path tag="function" new="2"}

Get path to an installed package. Mainly used to resolve the location of
[model packages](/usage/models). Currently imports the package to find its path.

> #### Example
>
> ```python
> util.get_package_path("en_core_web_sm")
> # /usr/lib/python3.6/site-packages/en_core_web_sm
> ```

| Name           | Description                               |
| -------------- | ----------------------------------------- |
| `package_name` | Name of installed package. ~~str~~        |
| **RETURNS**    | Path to model package directory. ~~Path~~ |

### util.is_in_jupyter {#util.is_in_jupyter tag="function" new="2"}

Check if user is running spaCy from a [Jupyter](https://jupyter.org) notebook by
detecting the IPython kernel. Mainly used for the
[`displacy`](/api/top-level#displacy) visualizer.

> #### Example
>
> ```python
> html = "<h1>Hello world!</h1>"
> if util.is_in_jupyter():
>     from IPython.core.display import display, HTML
>     display(HTML(html))
> ```

| Name        | Description                                    |
| ----------- | ---------------------------------------------- |
| **RETURNS** | `True` if in Jupyter, `False` if not. ~~bool~~ |

### util.compile_prefix_regex {#util.compile_prefix_regex tag="function"}

Compile a sequence of prefix rules into a regex object.

> #### Example
>
> ```python
> prefixes = ("§", "%", "=", r"\+")
> prefix_regex = util.compile_prefix_regex(prefixes)
> nlp.tokenizer.prefix_search = prefix_regex.search
> ```

| Name        | Description                                                                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `entries`   | The prefix rules, e.g. [`lang.punctuation.TOKENIZER_PREFIXES`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py). ~~Iterable[Union[str, Pattern]]~~ |
| **RETURNS** | The regex object. to be used for [`Tokenizer.prefix_search`](/api/tokenizer#attributes). ~~Pattern~~                                                                        |

### util.compile_suffix_regex {#util.compile_suffix_regex tag="function"}

Compile a sequence of suffix rules into a regex object.

> #### Example
>
> ```python
> suffixes = ("'s", "'S", r"(?<=[0-9])\+")
> suffix_regex = util.compile_suffix_regex(suffixes)
> nlp.tokenizer.suffix_search = suffix_regex.search
> ```

| Name        | Description                                                                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `entries`   | The suffix rules, e.g. [`lang.punctuation.TOKENIZER_SUFFIXES`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py). ~~Iterable[Union[str, Pattern]]~~ |
| **RETURNS** | The regex object. to be used for [`Tokenizer.suffix_search`](/api/tokenizer#attributes). ~~Pattern~~                                                                        |

### util.compile_infix_regex {#util.compile_infix_regex tag="function"}

Compile a sequence of infix rules into a regex object.

> #### Example
>
> ```python
> infixes = ("…", "-", "—", r"(?<=[0-9])[+\-\*^](?=[0-9-])")
> infix_regex = util.compile_infix_regex(infixes)
> nlp.tokenizer.infix_finditer = infix_regex.finditer
> ```

| Name        | Description                                                                                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `entries`   | The infix rules, e.g. [`lang.punctuation.TOKENIZER_INFIXES`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py). ~~Iterable[Union[str, Pattern]]~~ |
| **RETURNS** | The regex object. to be used for [`Tokenizer.infix_finditer`](/api/tokenizer#attributes). ~~Pattern~~                                                                     |

### util.minibatch {#util.minibatch tag="function" new="2"}

Iterate over batches of items. `size` may be an iterator, so that batch-size can
vary on each step.

> #### Example
>
> ```python
> batches = minibatch(train_data)
> for batch in batches:
>     nlp.update(batch)
> ```

| Name       | Description                              |
| ---------- | ---------------------------------------- |
| `items`    | The items to batch up. ~~Iterable[Any]~~ |
| `size`     | int / iterable                           | The batch size(s). ~~Union[int, Sequence[int]]~~ |
| **YIELDS** | The batches.                             |

### util.filter_spans {#util.filter_spans tag="function" new="2.1.4"}

Filter a sequence of [`Span`](/api/span) objects and remove duplicates or
overlaps. Useful for creating named entities (where one token can only be part
of one entity) or when merging spans with
[`Retokenizer.merge`](/api/doc#retokenizer.merge). When spans overlap, the
(first) longest span is preferred over shorter spans.

> #### Example
>
> ```python
> doc = nlp("This is a sentence.")
> spans = [doc[0:2], doc[0:2], doc[0:4]]
> filtered = filter_spans(spans)
> ```

| Name        | Description                             |
| ----------- | --------------------------------------- |
| `spans`     | The spans to filter. ~~Iterable[Span]~~ |
| **RETURNS** | The filtered spans. ~~List[Span]~~      |

### util.get_words_and_spaces {#get_words_and_spaces tag="function" new="3"}

Given a list of words and a text, reconstruct the original tokens and return a
list of words and spaces that can be used to create a [`Doc`](/api/doc#init).
This can help recover destructive tokenization that didn't preserve any
whitespace information.

> #### Example
>
> ```python
> orig_words = ["Hey", ",", "what", "'s", "up", "?"]
> orig_text = "Hey, what's up?"
> words, spaces = get_words_and_spaces(orig_words, orig_text)
> # ['Hey', ',', 'what', "'s", 'up', '?']
> # [False, True, False, True, False, False]
> ```

| Name        | Description                                                                                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `words`     | The list of words. ~~Iterable[str]~~                                                                                                               |
| `text`      | The original text. ~~str~~                                                                                                                         |
| **RETURNS** | A list of words and a list of boolean values indicating whether the word at this position is followed by a space. ~~Tuple[List[str], List[bool]]~~ |
