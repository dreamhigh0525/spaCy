---
title: Pipe
tag: class
teaser: Base class for trainable pipeline components
---

This class is a base class and **not instantiated directly**. Trainable pipeline
components like the [`EntityRecognizer`](/api/entityrecognizer) or
[`TextCategorizer`](/api/textcategorizer) inherit from it and it defines the
interface that components should follow to function as trainable components in a
spaCy pipeline. See the docs on
[writing trainable components](/usage/processing-pipelines#trainable-components)
for how to use the `Pipe` base class to implement custom components.

> #### Why is Pipe implemented in Cython?
>
> The `Pipe` class is implemented in a `.pyx` module, the extension used by
> [Cython](/api/cython). This is needed so that **other** Cython classes, like
> the [`EntityRecognizer`](/api/entityrecognizer) can inherit from it. But it
> doesn't mean you have to implement trainable components in Cython – pure
> Python components like the [`TextCategorizer`](/api/textcategorizer) can also
> inherit from `Pipe`.

```python
https://github.com/explosion/spaCy/blob/develop/spacy/pipeline/pipe.pyx
```

## Pipe.\_\_init\_\_ {#init tag="method"}

> #### Example
>
> ```python
> from spacy.pipeline import Pipe
> from spacy.language import Language
>
> class CustomPipe(Pipe):
>     ...
>
> @Language.factory("your_custom_pipe", default_config={"model": MODEL})
> def make_custom_pipe(nlp, name, model):
>     return CustomPipe(nlp.vocab, model, name)
> ```

Create a new pipeline instance. In your application, you would normally use a
shortcut for this and instantiate the component using its string name and
[`nlp.add_pipe`](/api/language#create_pipe).

| Name    | Description                                                                                                                     |
| ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `vocab` | The shared vocabulary. ~~Vocab~~                                                                                                |
| `model` | The Thinc [`Model`](https://thinc.ai/docs/api-model) powering the pipeline component. ~~Model[List[Doc], Any]~~                 |
| `name`  | String name of the component instance. Used to add entries to the `losses` during training. ~~str~~                             |
| `**cfg` | Additional config parameters and settings. Will be available as the dictionary `Pipe.cfg` and is serialized with the component. |

## Pipe.\_\_call\_\_ {#call tag="method"}

Apply the pipe to one document. The document is modified in place, and returned.
This usually happens under the hood when the `nlp` object is called on a text
and all pipeline components are applied to the `Doc` in order. Both
[`__call__`](/api/pipe#call) and [`pipe`](/api/pipe#pipe) delegate to the
[`predict`](/api/pipe#predict) and
[`set_annotations`](/api/pipe#set_annotations) methods.

> #### Example
>
> ```python
> doc = nlp("This is a sentence.")
> pipe = nlp.add_pipe("your_custom_pipe")
> # This usually happens under the hood
> processed = pipe(doc)
> ```

| Name        | Description                      |
| ----------- | -------------------------------- |
| `doc`       | The document to process. ~~Doc~~ |
| **RETURNS** | The processed document. ~~Doc~~  |

## Pipe.pipe {#pipe tag="method"}

Apply the pipe to a stream of documents. This usually happens under the hood
when the `nlp` object is called on a text and all pipeline components are
applied to the `Doc` in order. Both [`__call__`](/api/pipe#call) and
[`pipe`](/api/pipe#pipe) delegate to the [`predict`](/api/pipe#predict) and
[`set_annotations`](/api/pipe#set_annotations) methods.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> for doc in pipe.pipe(docs, batch_size=50):
>     pass
> ```

| Name           | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| `stream`       | A stream of documents. ~~Iterable[Doc]~~                      |
| _keyword-only_ |                                                               |
| `batch_size`   | The number of documents to buffer. Defaults to `128`. ~~int~~ |
| **YIELDS**     | The processed documents in order. ~~Doc~~                     |

## Pipe.begin_training {#begin_training tag="method"}

Initialize the component for training and return an
[`Optimizer`](https://thinc.ai/docs/api-optimizers). `get_examples` should be a
function that returns an iterable of [`Example`](/api/example) objects. The data
examples are used to **initialize the model** of the component and can either be
the full training data or a representative sample. Initialization includes
validating the network,
[inferring missing shapes](https://thinc.ai/docs/usage-models#validation) and
setting up the label scheme based on the data.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> optimizer = pipe.begin_training(lambda: [], pipeline=nlp.pipeline)
> ```

| Name           | Description                                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `get_examples` | Function that returns gold-standard annotations in the form of [`Example`](/api/example) objects. ~~Callable[[], Iterable[Example]]~~ |
| _keyword-only_ |                                                                                                                                       |
| `pipeline`     | Optional list of pipeline components that this component is part of. ~~Optional[List[Tuple[str, Callable[[Doc], Doc]]]]~~             |
| `sgd`          | An optimizer. Will be created via [`create_optimizer`](#create_optimizer) if not set. ~~Optional[Optimizer]~~                         |
| **RETURNS**    | The optimizer. ~~Optimizer~~                                                                                                          |

## Pipe.predict {#predict tag="method"}

Apply the component's model to a batch of [`Doc`](/api/doc) objects, without
modifying them.

<Infobox variant="danger">

This method needs to be overwritten with your own custom `predict` method.

</Infobox>

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> scores = pipe.predict([doc1, doc2])
> ```

| Name        | Description                                 |
| ----------- | ------------------------------------------- |
| `docs`      | The documents to predict. ~~Iterable[Doc]~~ |
| **RETURNS** | The model's prediction for each document.   |

## Pipe.set_annotations {#set_annotations tag="method"}

Modify a batch of [`Doc`](/api/doc) objects, using pre-computed scores.

<Infobox variant="danger">

This method needs to be overwritten with your own custom `set_annotations`
method.

</Infobox>

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> scores = pipe.predict(docs)
> pipe.set_annotations(docs, scores)
> ```

| Name     | Description                                      |
| -------- | ------------------------------------------------ |
| `docs`   | The documents to modify. ~~Iterable[Doc]~~       |
| `scores` | The scores to set, produced by `Tagger.predict`. |

## Pipe.update {#update tag="method"}

Learn from a batch of [`Example`](/api/example) objects containing the
predictions and gold-standard annotations, and update the component's model.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> optimizer = nlp.begin_training()
> losses = pipe.update(examples, sgd=optimizer)
> ```

| Name              | Description                                                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `examples`        | A batch of [`Example`](/api/example) objects to learn from. ~~Iterable[Example]~~                                                  |
| _keyword-only_    |                                                                                                                                    |  |
| `drop`            | The dropout rate. ~~float~~                                                                                                        |
| `set_annotations` | Whether or not to update the `Example` objects with the predictions, delegating to [`set_annotations`](#set_annotations). ~~bool~~ |
| `sgd`             | An optimizer. Will be created via [`create_optimizer`](#create_optimizer) if not set. ~~Optional[Optimizer]~~                      |
| `losses`          | Optional record of the loss during training. Updated using the component name as the key. ~~Optional[Dict[str, float]]~~           |
| **RETURNS**       | The updated `losses` dictionary. ~~Dict[str, float]~~                                                                              |

## Pipe.rehearse {#rehearse tag="method,experimental" new="3"}

Perform a "rehearsal" update from a batch of data. Rehearsal updates teach the
current model to make predictions similar to an initial model, to try to address
the "catastrophic forgetting" problem. This feature is experimental.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> optimizer = nlp.resume_training()
> losses = pipe.rehearse(examples, sgd=optimizer)
> ```

| Name           | Description                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `examples`     | A batch of [`Example`](/api/example) objects to learn from. ~~Iterable[Example]~~                                        |
| _keyword-only_ |                                                                                                                          |  |
| `drop`         | The dropout rate. ~~float~~                                                                                              |
| `sgd`          | An optimizer. Will be created via [`create_optimizer`](#create_optimizer) if not set. ~~Optional[Optimizer]~~            |
| `losses`       | Optional record of the loss during training. Updated using the component name as the key. ~~Optional[Dict[str, float]]~~ |
| **RETURNS**    | The updated `losses` dictionary. ~~Dict[str, float]~~                                                                    |

## Pipe.get_loss {#get_loss tag="method"}

Find the loss and gradient of loss for the batch of documents and their
predicted scores.

> #### Example
>
> ```python
> ner = nlp.add_pipe("ner")
> scores = ner.predict([eg.predicted for eg in examples])
> loss, d_loss = ner.get_loss(examples, scores)
> ```

| Name        | Description                                                                 |
| ----------- | --------------------------------------------------------------------------- |
| `examples`  | The batch of examples. ~~Iterable[Example]~~                                |
| `scores`    | Scores representing the model's predictions.                                |
| **RETURNS** | The loss and the gradient, i.e. `(loss, gradient)`. ~~Tuple[float, float]~~ |

## Pipe.score {#score tag="method" new="3"}

Score a batch of examples.

> #### Example
>
> ```python
> scores = pipe.score(examples)
> ```

| Name        | Description                                                                                             |
| ----------- | ------------------------------------------------------------------------------------------------------- |
| `examples`  | The examples to score. ~~Iterable[Example]~~                                                            |
| **RETURNS** | The scores, e.g. produced by the [`Scorer`](/api/scorer). ~~Dict[str, Union[float, Dict[str, float]]]~~ |

## Pipe.create_optimizer {#create_optimizer tag="method"}

Create an optimizer for the pipeline component. Defaults to
[`Adam`](https://thinc.ai/docs/api-optimizers#adam) with default settings.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> optimizer = pipe.create_optimizer()
> ```

| Name        | Description                  |
| ----------- | ---------------------------- |
| **RETURNS** | The optimizer. ~~Optimizer~~ |

## Pipe.use_params {#use_params tag="method, contextmanager"}

Modify the pipe's model, to use the given parameter values. At the end of the
context, the original parameters are restored.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> with pipe.use_params(optimizer.averages):
>     pipe.to_disk("/best_model")
> ```

| Name     | Description                                        |
| -------- | -------------------------------------------------- |
| `params` | The parameter values to use in the model. ~~dict~~ |

## Pipe.add_label {#add_label tag="method"}

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> pipe.add_label("MY_LABEL")
> ```

Add a new label to the pipe, to be predicted by the model. The actual
implementation depends on the specific component, but in general `add_label`
shouldn't be called if the output dimension is already set, or if the model has
already been fully [initialized](#begin_training). If these conditions are
violated, the function will raise an Error. The exception to this rule is when
the component is [resizable](#is_resizable), in which case
[`set_output`](#set_output) should be called to ensure that the model is
properly resized.

<Infobox variant="danger">

This method needs to be overwritten with your own custom `add_label` method.

</Infobox>

| Name        | Description                                             |
| ----------- | ------------------------------------------------------- |
| `label`     | The label to add. ~~str~~                               |
| **RETURNS** | 0 if the label is already present, otherwise 1. ~~int~~ |

Note that in general, you don't have to call `pipe.add_label` if you provide a
representative data sample to the [`begin_training`](#begin_training) method. In
this case, all labels found in the sample will be automatically added to the
model, and the output dimension will be
[inferred](/usage/layers-architectures#thinc-shape-inference) automatically.

## Pipe.is_resizable {#is_resizable tag="method"}

> #### Example
>
> ```python
> can_resize = pipe.is_resizable()
> ```
>
> ```python
> ### Custom resizing
> def custom_resize(model, new_nO):
>     # adjust model
>     return model
>
> custom_model.attrs["resize_output"] = custom_resize
> ```

Check whether or not the output dimension of the component's model can be
resized. If this method returns `True`, [`set_output`](#set_output) can be
called to change the model's output dimension.

For built-in components that are not resizable, you have to create and train a
new model from scratch with the appropriate architecture and output dimension.
For custom components, you can implement a `resize_output` function and add it
as an attribute to the component's model.

| Name        | Description                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------- |
| **RETURNS** | Whether or not the output dimension of the model can be changed after initialization. ~~bool~~ |

## Pipe.set_output {#set_output tag="method"}

Change the output dimension of the component's model. If the component is not
[resizable](#is_resizable), this method will raise a `NotImplementedError`. If a
component is resizable, the model's attribute `resize_output` will be called.
This is a function that takes the original model and the new output dimension
`nO`, and changes the model in place. When resizing an already trained model,
care should be taken to avoid the "catastrophic forgetting" problem.

> #### Example
>
> ```python
> if pipe.is_resizable():
>     pipe.set_output(512)
> ```

| Name | Description                       |
| ---- | --------------------------------- |
| `nO` | The new output dimension. ~~int~~ |

## Pipe.to_disk {#to_disk tag="method"}

Serialize the pipe to disk.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> pipe.to_disk("/path/to/pipe")
> ```

| Name           | Description                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `path`         | A path to a directory, which will be created if it doesn't exist. Paths may be either strings or `Path`-like objects. ~~Union[str, Path]~~ |
| _keyword-only_ |                                                                                                                                            |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~                                                |

## Pipe.from_disk {#from_disk tag="method"}

Load the pipe from disk. Modifies the object in place and returns it.

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> pipe.from_disk("/path/to/pipe")
> ```

| Name           | Description                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `path`         | A path to a directory. Paths may be either strings or `Path`-like objects. ~~Union[str, Path]~~ |
| _keyword-only_ |                                                                                                 |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~     |
| **RETURNS**    | The modified pipe. ~~Pipe~~                                                                     |

## Pipe.to_bytes {#to_bytes tag="method"}

> #### Example
>
> ```python
> pipe = nlp.add_pipe("your_custom_pipe")
> pipe_bytes = pipe.to_bytes()
> ```

Serialize the pipe to a bytestring.

| Name           | Description                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| _keyword-only_ |                                                                                             |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~ |
| **RETURNS**    | The serialized form of the pipe. ~~bytes~~                                                  |

## Pipe.from_bytes {#from_bytes tag="method"}

Load the pipe from a bytestring. Modifies the object in place and returns it.

> #### Example
>
> ```python
> pipe_bytes = pipe.to_bytes()
> pipe = nlp.add_pipe("your_custom_pipe")
> pipe.from_bytes(pipe_bytes)
> ```

| Name           | Description                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| `bytes_data`   | The data to load from. ~~bytes~~                                                            |
| _keyword-only_ |                                                                                             |
| `exclude`      | String names of [serialization fields](#serialization-fields) to exclude. ~~Iterable[str]~~ |
| **RETURNS**    | The pipe. ~~Pipe~~                                                                          |

## Attributes {#attributes}

| Name    | Description                                                                                                              |
| ------- | ------------------------------------------------------------------------------------------------------------------------ |
| `vocab` | The shared vocabulary that's passed in on initialization. ~~Vocab~~                                                      |
| `model` | The model powering the component. ~~Model[List[Doc], Any]~~                                                              |
| `name`  | The name of the component instance in the pipeline. Can be used in the losses. ~~str~~                                   |
| `cfg`   | Keyword arguments passed to [`Pipe.__init__`](/api/pipe#init). Will be serialized with the component. ~~Dict[str, Any]~~ |

## Serialization fields {#serialization-fields}

During serialization, spaCy will export several data fields used to restore
different aspects of the object. If needed, you can exclude them from
serialization by passing in the string names via the `exclude` argument.

> #### Example
>
> ```python
> data = pipe.to_disk("/path", exclude=["vocab"])
> ```

| Name    | Description                                                    |
| ------- | -------------------------------------------------------------- |
| `vocab` | The shared [`Vocab`](/api/vocab).                              |
| `cfg`   | The config file. You usually don't want to exclude this.       |
| `model` | The binary model data. You usually don't want to exclude this. |
