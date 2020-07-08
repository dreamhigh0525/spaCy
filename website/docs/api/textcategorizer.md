---
title: TextCategorizer
tag: class
source: spacy/pipeline/pipes.pyx
new: 2
---

This class is a subclass of `Pipe` and follows the same API. The pipeline
component is available in the [processing pipeline](/usage/processing-pipelines)
via the ID `"textcat"`.

## TextCategorizer.\_\_init\_\_ {#init tag="method"}

> #### Example
>
> ```python
> # Construction via create_pipe
> textcat = nlp.create_pipe("textcat")
> 
> # Construction via create_pipe with custom model
> config = {"model": {"@architectures": "my_textcat"}}
> parser = nlp.create_pipe("textcat", config)
> 
> # Construction from class with custom model from file
> from spacy.pipeline import TextCategorizer
> model = util.load_config("model.cfg", create_objects=True)["model"]
> textcat = TextCategorizer(nlp.vocab, model)
> ```

Create a new pipeline instance. In your application, you would normally use a
shortcut for this and instantiate the component using its string name and
[`nlp.create_pipe`](/api/language#create_pipe).

| Name        | Type              | Description                                                                     |
| ----------- | ----------------- | ------------------------------------------------------------------------------- |
| `vocab`     | `Vocab`           | The shared vocabulary.                                                          |
| `model`     | `Model`           | The [`Model`](https://thinc.ai/docs/api-model) powering the pipeline component. |
| `**cfg`     | -                 | Configuration parameters.                                                       |
| **RETURNS** | `TextCategorizer` | The newly constructed object.                                                   |

<!-- TODO move to config page 
### Architectures {#architectures new="2.1"}

Text classification models can be used to solve a wide variety of problems.
Differences in text length, number of labels, difficulty, and runtime
performance constraints mean that no single algorithm performs well on all types
of problems. To handle a wider variety of problems, the `TextCategorizer` object
allows configuration of its model architecture, using the `architecture` keyword
argument.

| Name           | Description                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"ensemble"`   | **Default:** Stacked ensemble of a bag-of-words model and a neural network model. The neural network uses a CNN with mean pooling and attention. The "ngram_size" and "attr" arguments can be used to configure the feature extraction for the bag-of-words model.                                                                                                                                               |
| `"simple_cnn"` | A neural network model where token vectors are calculated using a CNN. The vectors are mean pooled and used as features in a feed-forward network. This architecture is usually less accurate than the ensemble, but runs faster.                                                                                                                                                                                |
| `"bow"`        | An ngram "bag-of-words" model. This architecture should run much faster than the others, but may not be as accurate, especially if texts are short. The features extracted can be controlled using the keyword arguments `ngram_size` and `attr`. For instance, `ngram_size=3` and `attr="lower"` would give lower-cased unigram, trigram and bigram features. 2, 3 or 4 are usually good choices of ngram size. |
-->

## TextCategorizer.\_\_call\_\_ {#call tag="method"}

Apply the pipe to one document. The document is modified in place, and returned.
This usually happens under the hood when the `nlp` object is called on a text
and all pipeline components are applied to the `Doc` in order. Both
[`__call__`](/api/textcategorizer#call) and [`pipe`](/api/textcategorizer#pipe)
delegate to the [`predict`](/api/textcategorizer#predict) and
[`set_annotations`](/api/textcategorizer#set_annotations) methods.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> doc = nlp("This is a sentence.")
> # This usually happens under the hood
> processed = textcat(doc)
> ```

| Name        | Type  | Description              |
| ----------- | ----- | ------------------------ |
| `doc`       | `Doc` | The document to process. |
| **RETURNS** | `Doc` | The processed document.  |

## TextCategorizer.pipe {#pipe tag="method"}

Apply the pipe to a stream of documents. This usually happens under the hood
when the `nlp` object is called on a text and all pipeline components are
applied to the `Doc` in order. Both [`__call__`](/api/textcategorizer#call) and
[`pipe`](/api/textcategorizer#pipe) delegate to the
[`predict`](/api/textcategorizer#predict) and
[`set_annotations`](/api/textcategorizer#set_annotations) methods.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> for doc in textcat.pipe(docs, batch_size=50):
>     pass
> ```

| Name         | Type            | Description                                            |
| ------------ | --------------- | ------------------------------------------------------ |
| `stream`     | `Iterable[Doc]` | A stream of documents.                                 |
| `batch_size` | int             | The number of texts to buffer. Defaults to `128`.      |
| **YIELDS**   | `Doc`           | Processed documents in the order of the original text. |

## TextCategorizer.predict {#predict tag="method"}

Apply the pipeline's model to a batch of docs, without modifying them.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> scores, tensors = textcat.predict([doc1, doc2])
> ```

| Name        | Type     | Description                                                                                                                                                                                                                        |
| ----------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docs`      | iterable | The documents to predict.                                                                                                                                                                                                          |
| **RETURNS** | tuple    | A `(scores, tensors)` tuple where `scores` is the model's prediction for each document and `tensors` is the token representations used to predict the scores. Each tensor is an array with one row for each token in the document. |

## TextCategorizer.set_annotations {#set_annotations tag="method"}

Modify a batch of documents, using pre-computed scores.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> scores, tensors = textcat.predict([doc1, doc2])
> textcat.set_annotations([doc1, doc2], scores, tensors)
> ```

| Name      | Type     | Description                                               |
| --------- | -------- | --------------------------------------------------------- |
| `docs`    | iterable | The documents to modify.                                  |
| `scores`  | -        | The scores to set, produced by `TextCategorizer.predict`. |
| `tensors` | iterable | The token representations used to predict the scores.     |

## TextCategorizer.update {#update tag="method"}

Learn from a batch of documents and gold-standard information, updating the
pipe's model. Delegates to [`predict`](/api/textcategorizer#predict) and
[`get_loss`](/api/textcategorizer#get_loss).

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab, textcat_model)
> optimizer = nlp.begin_training()
> losses = textcat.update(examples, sgd=optimizer)
> ```

| Name              | Type                | Description                                                                                                                                   |
| ----------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `examples`        | `Iterable[Example]` | A batch of [`Example`](/api/example) objects to learn from.                                                                                   |
| _keyword-only_    |                     |                                                                                                                                               |
| `drop`            | float               | The dropout rate.                                                                                                                             |
| `set_annotations` | bool                | Whether or not to update the `Example` objects with the predictions, delegating to [`set_annotations`](/api/textcategorizer#set_annotations). |
| `sgd`             | `Optimizer`         | The [`Optimizer`](https://thinc.ai/docs/api-optimizers) object.                                                                               |
| `losses`          | `Dict[str, float]`  | Optional record of the loss during training. The value keyed by the model's name is updated.                                                  |
| **RETURNS**       | `Dict[str, float]`  | The updated `losses` dictionary.                                                                                                              |

## TextCategorizer.get_loss {#get_loss tag="method"}

Find the loss and gradient of loss for the batch of documents and their
predicted scores.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> scores = textcat.predict([doc1, doc2])
> loss, d_loss = textcat.get_loss([doc1, doc2], [gold1, gold2], scores)
> ```

| Name        | Type     | Description                                                  |
| ----------- | -------- | ------------------------------------------------------------ |
| `docs`      | iterable | The batch of documents.                                      |
| `golds`     | iterable | The gold-standard data. Must have the same length as `docs`. |
| `scores`    | -        | Scores representing the model's predictions.                 |
| **RETURNS** | tuple    | The loss and the gradient, i.e. `(loss, gradient)`.          |

## TextCategorizer.begin_training {#begin_training tag="method"}

Initialize the pipe for training, using data examples if available. Return an
[`Optimizer`](https://thinc.ai/docs/api-optimizers) object.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> nlp.pipeline.append(textcat)
> optimizer = textcat.begin_training(pipeline=nlp.pipeline)
> ```

| Name           | Type                    | Description                                                                                                                                                         |
| -------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_examples` | `Iterable[Example]`     | Optional gold-standard annotations in the form of [`Example`](/api/example) objects.                                                                                |
| `pipeline`     | `List[(str, callable)]` | Optional list of pipeline components that this component is part of.                                                                                                |
| `sgd`          | `Optimizer`             | An optional [`Optimizer`](https://thinc.ai/docs/api-optimizers) object. Will be created via [`create_optimizer`](/api/textcategorizer#create_optimizer) if not set. |
| **RETURNS**    | `Optimizer`             | An optimizer.                                                                                                                                                       |

## TextCategorizer.create_optimizer {#create_optimizer tag="method"}

Create an optimizer for the pipeline component.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> optimizer = textcat.create_optimizer()
> ```

| Name        | Type     | Description    |
| ----------- | -------- | -------------- |
| **RETURNS** | callable | The optimizer. |

## TextCategorizer.use_params {#use_params tag="method, contextmanager"}

Modify the pipe's model, to use the given parameter values.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> with textcat.use_params(optimizer.averages):
>     textcat.to_disk("/best_model")
> ```

| Name     | Type | Description                                                                                                |
| -------- | ---- | ---------------------------------------------------------------------------------------------------------- |
| `params` | dict | The parameter values to use in the model. At the end of the context, the original parameters are restored. |

## TextCategorizer.add_label {#add_label tag="method"}

Add a new label to the pipe.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> textcat.add_label("MY_LABEL")
> ```

| Name    | Type | Description       |
| ------- | ---- | ----------------- |
| `label` | str  | The label to add. |

## TextCategorizer.to_disk {#to_disk tag="method"}

Serialize the pipe to disk.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> textcat.to_disk("/path/to/textcat")
> ```

| Name      | Type         | Description                                                                                                           |
| --------- | ------------ | --------------------------------------------------------------------------------------------------------------------- |
| `path`    | str / `Path` | A path to a directory, which will be created if it doesn't exist. Paths may be either strings or `Path`-like objects. |
| `exclude` | list         | String names of [serialization fields](#serialization-fields) to exclude.                                             |

## TextCategorizer.from_disk {#from_disk tag="method"}

Load the pipe from disk. Modifies the object in place and returns it.

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> textcat.from_disk("/path/to/textcat")
> ```

| Name        | Type              | Description                                                                |
| ----------- | ----------------- | -------------------------------------------------------------------------- |
| `path`      | str / `Path`      | A path to a directory. Paths may be either strings or `Path`-like objects. |
| `exclude`   | list              | String names of [serialization fields](#serialization-fields) to exclude.  |
| **RETURNS** | `TextCategorizer` | The modified `TextCategorizer` object.                                     |

## TextCategorizer.to_bytes {#to_bytes tag="method"}

> #### Example
>
> ```python
> textcat = TextCategorizer(nlp.vocab)
> textcat_bytes = textcat.to_bytes()
> ```

Serialize the pipe to a bytestring.

| Name        | Type  | Description                                                               |
| ----------- | ----- | ------------------------------------------------------------------------- |
| `exclude`   | list  | String names of [serialization fields](#serialization-fields) to exclude. |
| **RETURNS** | bytes | The serialized form of the `TextCategorizer` object.                      |

## TextCategorizer.from_bytes {#from_bytes tag="method"}

Load the pipe from a bytestring. Modifies the object in place and returns it.

> #### Example
>
> ```python
> textcat_bytes = textcat.to_bytes()
> textcat = TextCategorizer(nlp.vocab)
> textcat.from_bytes(textcat_bytes)
> ```

| Name         | Type              | Description                                                               |
| ------------ | ----------------- | ------------------------------------------------------------------------- |
| `bytes_data` | bytes             | The data to load from.                                                    |
| `exclude`    | list              | String names of [serialization fields](#serialization-fields) to exclude. |
| **RETURNS**  | `TextCategorizer` | The `TextCategorizer` object.                                             |

## TextCategorizer.labels {#labels tag="property"}

The labels currently added to the component.

> #### Example
>
> ```python
> textcat.add_label("MY_LABEL")
> assert "MY_LABEL" in textcat.labels
> ```

| Name        | Type  | Description                        |
| ----------- | ----- | ---------------------------------- |
| **RETURNS** | tuple | The labels added to the component. |

## Serialization fields {#serialization-fields}

During serialization, spaCy will export several data fields used to restore
different aspects of the object. If needed, you can exclude them from
serialization by passing in the string names via the `exclude` argument.

> #### Example
>
> ```python
> data = textcat.to_disk("/path", exclude=["vocab"])
> ```

| Name    | Description                                                    |
| ------- | -------------------------------------------------------------- |
| `vocab` | The shared [`Vocab`](/api/vocab).                              |
| `cfg`   | The config file. You usually don't want to exclude this.       |
| `model` | The binary model data. You usually don't want to exclude this. |
