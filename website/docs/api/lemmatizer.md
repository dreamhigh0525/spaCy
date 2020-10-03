---
title: Lemmatizer
tag: class
source: spacy/pipeline/lemmatizer.py
new: 3
teaser: 'Pipeline component for lemmatization'
api_base_class: /api/pipe
api_string_name: lemmatizer
api_trainable: false
---

Component for assigning base forms to tokens using rules based on part-of-speech
tags, or lookup tables. Functionality to train the component is coming soon.
Different [`Language`](/api/language) subclasses can implement their own
lemmatizer components via
[language-specific factories](/usage/processing-pipelines#factories-language).
The default data used is provided by the
[`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data)
extension package.

<Infobox variant="warning" title="New in v3.0">

As of v3.0, the `Lemmatizer` is a **standalone pipeline component** that can be
added to your pipeline, and not a hidden part of the vocab that runs behind the
scenes. This makes it easier to customize how lemmas should be assigned in your
pipeline.

If the lemmatization mode is set to `"rule"`, which requires coarse-grained POS
(`Token.pos`) to be assigned, make sure a [`Tagger`](/api/tagger),
[`Morphologizer`](/api/morphologizer) or another component assigning POS is
available in the pipeline and runs _before_ the lemmatizer.

</Infobox>

## Config and implementation

The default config is defined by the pipeline component factory and describes
how the component should be configured. You can override its settings via the
`config` argument on [`nlp.add_pipe`](/api/language#add_pipe) or in your
[`config.cfg` for training](/usage/training#config). For examples of the lookups
data format used by the lookup and rule-based lemmatizers, see
[`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data).

> #### Example
>
> ```python
> config = {"mode": "rule"}
> nlp.add_pipe("lemmatizer", config=config)
> ```

| Setting     | Description                                                                       |
| ----------- | --------------------------------------------------------------------------------- |
| `mode`      | The lemmatizer mode, e.g. `"lookup"` or `"rule"`. Defaults to `"lookup"`. ~~str~~ |
| `overwrite` | Whether to overwrite existing lemmas. Defaults to `False`. ~~bool~~               |
| `model`     | **Not yet implemented:** the model to use. ~~Model~~                              |

```python
%%GITHUB_SPACY/spacy/pipeline/lemmatizer.py
```

## Lemmatizer.\_\_init\_\_ {#init tag="method"}

> #### Example
>
> ```python
> # Construction via add_pipe with default model
> lemmatizer = nlp.add_pipe("lemmatizer")
>
> # Construction via add_pipe with custom settings
> config = {"mode": "rule", overwrite=True}
> lemmatizer = nlp.add_pipe("lemmatizer", config=config)
> ```

Create a new pipeline instance. In your application, you would normally use a
shortcut for this and instantiate the component using its string name and
[`nlp.add_pipe`](/api/language#add_pipe).

| Name           | Description                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------- |
| `vocab`        | The shared vocabulary. ~~Vocab~~                                                                    |
| `model`        | **Not yet implemented:** The model to use. ~~Model~~                                                |
| `name`         | String name of the component instance. Used to add entries to the `losses` during training. ~~str~~ |
| _keyword-only_ |                                                                                                     |
| mode           | The lemmatizer mode, e.g. `"lookup"` or `"rule"`. Defaults to `"lookup"`. ~~str~~                   |
| overwrite      | Whether to overwrite existing lemmas. ~~bool~                                                       |

## Lemmatizer.\_\_call\_\_ {#call tag="method"}

Apply the pipe to one document. The document is modified in place, and returned.
This usually happens under the hood when the `nlp` object is called on a text
and all pipeline components are applied to the `Doc` in order.

> #### Example
>
> ```python
> doc = nlp("This is a sentence.")
> lemmatizer = nlp.add_pipe("lemmatizer")
> # This usually happens under the hood
> processed = lemmatizer(doc)
> ```

| Name        | Description                      |
| ----------- | -------------------------------- |
| `doc`       | The document to process. ~~Doc~~ |
| **RETURNS** | The processed document. ~~Doc~~  |

## Lemmatizer.pipe {#pipe tag="method"}

Apply the pipe to a stream of documents. This usually happens under the hood
when the `nlp` object is called on a text and all pipeline components are
applied to the `Doc` in order.

> #### Example
>
> ```python
> lemmatizer = nlp.add_pipe("lemmatizer")
> for doc in lemmatizer.pipe(docs, batch_size=50):
>     pass
> ```

| Name           | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| `stream`       | A stream of documents. ~~Iterable[Doc]~~                      |
| _keyword-only_ |                                                               |
| `batch_size`   | The number of documents to buffer. Defaults to `128`. ~~int~~ |
| **YIELDS**     | The processed documents in order. ~~Doc~~                     |

## Lemmatizer.initialize {#initialize tag="method"}

Initialize the lemmatizer and load any data resources. This method is typically
called by [`Language.initialize`](/api/language#initialize) and lets you
customize arguments it receives via the
[`[initialize.components]`](/api/data-formats#config-initialize) block in the
config. The loading only happens during initialization, typically before
training. At runtime, all data is loaded from disk.

> #### Example
>
> ```python
> lemmatizer = nlp.add_pipe("lemmatizer")
> lemmatizer.initialize(lookups=lookups)
> ```
>
> ```ini
> ### config.cfg
> [initialize.components.lemmatizer]
>
> [initialize.components.lemmatizer.lookups]
> @misc = "load_my_lookups.v1"
> ```

| Name           | Description                                                                                                                                                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_examples` | Function that returns gold-standard annotations in the form of [`Example`](/api/example) objects. Defaults to `None`. ~~Optional[Callable[[], Iterable[Example]]]~~                                                                                                                 |
| _keyword-only_ |                                                                                                                                                                                                                                                                                     |
| `nlp`          | The current `nlp` object. Defaults to `None`. ~~Optional[Language]~~                                                                                                                                                                                                                |
| `lookups`      | The lookups object containing the tables such as `"lemma_rules"`, `"lemma_index"`, `"lemma_exc"` and `"lemma_lookup"`. If `None`, default tables are loaded from [`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data). Defaults to `None`. ~~Optional[Lookups]~~ |

## Lemmatizer.lookup_lemmatize {#lookup_lemmatize tag="method"}

Lemmatize a token using a lookup-based approach. If no lemma is found, the
original string is returned.

| Name        | Description                                         |
| ----------- | --------------------------------------------------- |
| `token`     | The token to lemmatize. ~~Token~~                   |
| **RETURNS** | A list containing one or more lemmas. ~~List[str]~~ |

## Lemmatizer.rule_lemmatize {#rule_lemmatize tag="method"}

Lemmatize a token using a rule-based approach. Typically relies on POS tags.

| Name        | Description                                         |
| ----------- | --------------------------------------------------- |
| `token`     | The token to lemmatize. ~~Token~~                   |
| **RETURNS** | A list containing one or more lemmas. ~~List[str]~~ |

## Lemmatizer.is_base_form {#is_base_form tag="method"}

Check whether we're dealing with an uninflected paradigm, so we can avoid
lemmatization entirely.

| Name        | Description                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------- |
| `token`     | The token to analyze. ~~Token~~                                                                                  |
| **RETURNS** | Whether the token's attributes (e.g., part-of-speech tag, morphological features) describe a base form. ~~bool~~ |

## Lemmatizer.get_lookups_config {#get_lookups_config tag="classmethod"}

Returns the lookups configuration settings for a given mode for use in
[`Lemmatizer.load_lookups`](/api/lemmatizer#load_lookups).

| Name        | Description                                                                            |
| ----------- | -------------------------------------------------------------------------------------- |
| `mode`      | The lemmatizer mode. ~~str~~                                                           |
| **RETURNS** | The required table names and the optional table names. ~~Tuple[List[str], List[str]]~~ |

## Lemmatizer.to_disk {#to_disk tag="method"}

Serialize the pipe to disk.

> #### Example
>
> ```python
> lemmatizer = nlp.add_pipe("lemmatizer")
> lemmatizer.to_disk("/path/to/lemmatizer")
> ```

| Name           | Description                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `path`         | A path to a directory, which will be created if it doesn't exist. Paths may be either strings or `Path`-like objects. ~~Union[str, Path]~~ |
| _keyword-only_ |                                                                                                                                            |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~                                                |

## Lemmatizer.from_disk {#from_disk tag="method"}

Load the pipe from disk. Modifies the object in place and returns it.

> #### Example
>
> ```python
> lemmatizer = nlp.add_pipe("lemmatizer")
> lemmatizer.from_disk("/path/to/lemmatizer")
> ```

| Name           | Description                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `path`         | A path to a directory. Paths may be either strings or `Path`-like objects. ~~Union[str, Path]~~ |
| _keyword-only_ |                                                                                                 |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~     |
| **RETURNS**    | The modified `Lemmatizer` object. ~~Lemmatizer~~                                                |

## Lemmatizer.to_bytes {#to_bytes tag="method"}

> #### Example
>
> ```python
> lemmatizer = nlp.add_pipe("lemmatizer")
> lemmatizer_bytes = lemmatizer.to_bytes()
> ```

Serialize the pipe to a bytestring.

| Name           | Description                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| _keyword-only_ |                                                                                             |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~ |
| **RETURNS**    | The serialized form of the `Lemmatizer` object. ~~bytes~~                                   |

## Lemmatizer.from_bytes {#from_bytes tag="method"}

Load the pipe from a bytestring. Modifies the object in place and returns it.

> #### Example
>
> ```python
> lemmatizer_bytes = lemmatizer.to_bytes()
> lemmatizer = nlp.add_pipe("lemmatizer")
> lemmatizer.from_bytes(lemmatizer_bytes)
> ```

| Name           | Description                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| `bytes_data`   | The data to load from. ~~bytes~~                                                            |
| _keyword-only_ |                                                                                             |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~ |
| **RETURNS**    | The `Lemmatizer` object. ~~Lemmatizer~~                                                     |

## Attributes {#attributes}

| Name      | Description                                 |
| --------- | ------------------------------------------- |
| `vocab`   | The shared [`Vocab`](/api/vocab). ~~Vocab~~ |
| `lookups` | The lookups object. ~~Lookups~~             |
| `mode`    | The lemmatizer mode. ~~str~~                |

## Serialization fields {#serialization-fields}

During serialization, spaCy will export several data fields used to restore
different aspects of the object. If needed, you can exclude them from
serialization by passing in the string names via the `exclude` argument.

> #### Example
>
> ```python
> data = lemmatizer.to_disk("/path", exclude=["vocab"])
> ```

| Name      | Description                                          |
| --------- | ---------------------------------------------------- |
| `vocab`   | The shared [`Vocab`](/api/vocab).                    |
| `lookups` | The lookups. You usually don't want to exclude this. |
