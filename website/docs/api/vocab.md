---
title: Vocab
teaser: A storage class for vocabulary and other data shared across a language
tag: class
source: spacy/vocab.pyx
---

The `Vocab` object provides a lookup table that allows you to access
[`Lexeme`](/api/lexeme) objects, as well as the
[`StringStore`](/api/stringstore). It also owns underlying C-data that is shared
between `Doc` objects.

## Vocab.\_\_init\_\_ {#init tag="method"}

Create the vocabulary.

> #### Example
>
> ```python
> from spacy.vocab import Vocab
> vocab = Vocab(strings=[u"hello", u"world"])
> ```

| Name               | Type                 | Description                                                                                                        |
| ------------------ | -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `lex_attr_getters` | dict                 | A dictionary mapping attribute IDs to functions to compute them. Defaults to `None`.                               |
| `tag_map`          | dict                 | A dictionary mapping fine-grained tags to coarse-grained parts-of-speech, and optionally morphological attributes. |
| `lemmatizer`       | object               | A lemmatizer. Defaults to `None`.                                                                                  |
| `strings`          | `StringStore` / list | A [`StringStore`](/api/stringstore) that maps strings to hash values, and vice versa, or a list of strings.        |
| **RETURNS**        | `Vocab`              | The newly constructed object.                                                                                      |

## Vocab.\_\_len\_\_ {#len tag="method"}

Get the current number of lexemes in the vocabulary.

> #### Example
>
> ```python
> doc = nlp(u"This is a sentence.")
> assert len(nlp.vocab) > 0
> ```

| Name        | Type | Description                              |
| ----------- | ---- | ---------------------------------------- |
| **RETURNS** | int  | The number of lexemes in the vocabulary. |

## Vocab.\_\_getitem\_\_ {#getitem tag="method"}

Retrieve a lexeme, given an int ID or a unicode string. If a previously unseen
unicode string is given, a new lexeme is created and stored.

> #### Example
>
> ```python
> apple = nlp.vocab.strings[u"apple"]
> assert nlp.vocab[apple] == nlp.vocab[u"apple"]
> ```

| Name           | Type          | Description                                      |
| -------------- | ------------- | ------------------------------------------------ |
| `id_or_string` | int / unicode | The hash value of a word, or its unicode string. |
| **RETURNS**    | `Lexeme`      | The lexeme indicated by the given ID.            |

## Vocab.\_\_iter\_\_ {#iter tag="method"}

Iterate over the lexemes in the vocabulary.

> #### Example
>
> ```python
> stop_words = (lex for lex in nlp.vocab if lex.is_stop)
> ```

| Name       | Type     | Description                 |
| ---------- | -------- | --------------------------- |
| **YIELDS** | `Lexeme` | An entry in the vocabulary. |

## Vocab.\_\_contains\_\_ {#contains tag="method"}

Check whether the string has an entry in the vocabulary. To get the ID for a
given string, you need to look it up in
[`vocab.strings`](/api/vocab#attributes).

> #### Example
>
> ```python
> apple = nlp.vocab.strings[u"apple"]
> oov = nlp.vocab.strings[u"dskfodkfos"]
> assert apple in nlp.vocab
> assert oov not in nlp.vocab
> ```

| Name        | Type    | Description                                        |
| ----------- | ------- | -------------------------------------------------- |
| `string`    | unicode | The ID string.                                     |
| **RETURNS** | bool    | Whether the string has an entry in the vocabulary. |

## Vocab.add_flag {#add_flag tag="method"}

Set a new boolean flag to words in the vocabulary. The `flag_getter` function
will be called over the words currently in the vocab, and then applied to new
words as they occur. You'll then be able to access the flag value on each token,
using `token.check_flag(flag_id)`.

> #### Example
>
> ```python
> def is_my_product(text):
>     products = [u"spaCy", u"Thinc", u"displaCy"]
>     return text in products
>
> MY_PRODUCT = nlp.vocab.add_flag(is_my_product)
> doc = nlp(u"I like spaCy")
> assert doc[2].check_flag(MY_PRODUCT) == True
> ```

| Name          | Type | Description                                                                                                                                     |
| ------------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `flag_getter` | dict | A function `f(unicode) -> bool`, to get the flag value.                                                                                         |
| `flag_id`     | int  | An integer between 1 and 63 (inclusive), specifying the bit at which the flag will be stored. If `-1`, the lowest available bit will be chosen. |
| **RETURNS**   | int  | The integer ID by which the flag value can be checked.                                                                                          |

## Vocab.reset_vectors {#reset_vectors tag="method" new="2"}

Drop the current vector table. Because all vectors must be the same width, you
have to call this to change the size of the vectors. Only one of the `width` and
`shape` keyword arguments can be specified.

> #### Example
>
> ```python
> nlp.vocab.reset_vectors(width=300)
> ```

| Name    | Type | Description                            |
| ------- | ---- | -------------------------------------- |
| `width` | int  | The new width (keyword argument only). |
| `shape` | int  | The new shape (keyword argument only). |

## Vocab.prune_vectors {#prune_vectors tag="method" new="2"}

Reduce the current vector table to `nr_row` unique entries. Words mapped to the
discarded vectors will be remapped to the closest vector among those remaining.
For example, suppose the original table had vectors for the words:
`['sat', 'cat', 'feline', 'reclined']`. If we prune the vector table to, two
rows, we would discard the vectors for "feline" and "reclined". These words
would then be remapped to the closest remaining vector – so "feline" would have
the same vector as "cat", and "reclined" would have the same vector as "sat".
The similarities are judged by cosine. The original vectors may be large, so the
cosines are calculated in minibatches, to reduce memory usage.

> #### Example
>
> ```python
> nlp.vocab.prune_vectors(10000)
> assert len(nlp.vocab.vectors) <= 1000
> ```

| Name         | Type | Description                                                                                                                                                                                 |
| ------------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nr_row`     | int  | The number of rows to keep in the vector table.                                                                                                                                             |
| `batch_size` | int  | Batch of vectors for calculating the similarities. Larger batch sizes might be faster, while temporarily requiring more memory.                                                             |
| **RETURNS**  | dict | A dictionary keyed by removed words mapped to `(string, score)` tuples, where `string` is the entry the removed word was mapped to, and `score` the similarity score between the two words. |

## Vocab.get_vector {#get_vector tag="method" new="2"}

Retrieve a vector for a word in the vocabulary. Words can be looked up by string
or hash value. If no vectors data is loaded, a `ValueError` is raised.

> #### Example
>
> ```python
> nlp.vocab.get_vector(u"apple")
> ```

| Name        | Type                                     | Description                                                                   |
| ----------- | ---------------------------------------- | ----------------------------------------------------------------------------- |
| `orth`      | int / unicode                            | The hash value of a word, or its unicode string.                              |
| **RETURNS** | `numpy.ndarray[ndim=1, dtype='float32']` | A word vector. Size and shape are determined by the `Vocab.vectors` instance. |

## Vocab.set_vector {#set_vector tag="method" new="2"}

Set a vector for a word in the vocabulary. Words can be referenced by by string
or hash value.

> #### Example
>
> ```python
> nlp.vocab.set_vector(u"apple", array([...]))
> ```

| Name     | Type                                     | Description                                      |
| -------- | ---------------------------------------- | ------------------------------------------------ |
| `orth`   | int / unicode                            | The hash value of a word, or its unicode string. |
| `vector` | `numpy.ndarray[ndim=1, dtype='float32']` | The vector to set.                               |

## Vocab.has_vector {#has_vector tag="method" new="2"}

Check whether a word has a vector. Returns `False` if no vectors are loaded.
Words can be looked up by string or hash value.

> #### Example
>
> ```python
> if nlp.vocab.has_vector(u"apple"):
>     vector = nlp.vocab.get_vector(u"apple")
> ```

| Name        | Type          | Description                                      |
| ----------- | ------------- | ------------------------------------------------ |
| `orth`      | int / unicode | The hash value of a word, or its unicode string. |
| **RETURNS** | bool          | Whether the word has a vector.                   |

## Vocab.to_disk {#to_disk tag="method" new="2"}

Save the current state to a directory.

> #### Example
>
> ```python
> nlp.vocab.to_disk("/path/to/vocab")
> ```

| Name      | Type             | Description                                                                                                           |
| --------- | ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| `path`    | unicode / `Path` | A path to a directory, which will be created if it doesn't exist. Paths may be either strings or `Path`-like objects. |
| `exclude` | list             | String names of [serialization fields](#serialization-fields) to exclude.                                             |

## Vocab.from_disk {#from_disk tag="method" new="2"}

Loads state from a directory. Modifies the object in place and returns it.

> #### Example
>
> ```python
> from spacy.vocab import Vocab
> vocab = Vocab().from_disk("/path/to/vocab")
> ```

| Name        | Type             | Description                                                                |
| ----------- | ---------------- | -------------------------------------------------------------------------- |
| `path`      | unicode / `Path` | A path to a directory. Paths may be either strings or `Path`-like objects. |
| `exclude`   | list             | String names of [serialization fields](#serialization-fields) to exclude.  |
| **RETURNS** | `Vocab`          | The modified `Vocab` object.                                               |

## Vocab.to_bytes {#to_bytes tag="method"}

Serialize the current state to a binary string.

> #### Example
>
> ```python
> vocab_bytes = nlp.vocab.to_bytes()
> ```

| Name        | Type  | Description                                                               |
| ----------- | ----- | ------------------------------------------------------------------------- |
| `exclude`   | list  | String names of [serialization fields](#serialization-fields) to exclude. |
| **RETURNS** | bytes | The serialized form of the `Vocab` object.                                |

## Vocab.from_bytes {#from_bytes tag="method"}

Load state from a binary string.

> #### Example
>
> ```python
> from spacy.vocab import Vocab
> vocab_bytes = nlp.vocab.to_bytes()
> vocab = Vocab()
> vocab.from_bytes(vocab_bytes)
> ```

| Name         | Type    | Description                                                               |
| ------------ | ------- | ------------------------------------------------------------------------- |
| `bytes_data` | bytes   | The data to load from.                                                    |
| `exclude`    | list    | String names of [serialization fields](#serialization-fields) to exclude. |
| **RETURNS**  | `Vocab` | The `Vocab` object.                                                       |

## Attributes {#attributes}

> #### Example
>
> ```python
> apple_id = nlp.vocab.strings[u"apple"]
> assert type(apple_id) == int
> PERSON = nlp.vocab.strings[u"PERSON"]
> assert type(PERSON) == int
> ```

| Name                                          | Type          | Description                                                  |
| --------------------------------------------- | ------------- | ------------------------------------------------------------ |
| `strings`                                     | `StringStore` | A table managing the string-to-int mapping.                  |
| `vectors` <Tag variant="new">2</Tag>          | `Vectors`     | A table associating word IDs to word vectors.                |
| `vectors_length`                              | int           | Number of dimensions for each word vector.                   |
| `lookups`                                     | `Lookups`     | The available lookup tables in this vocab.                   |
| `writing_system` <Tag variant="new">2.1</Tag> | dict          | A dict with information about the language's writing system. |

## Serialization fields {#serialization-fields}

During serialization, spaCy will export several data fields used to restore
different aspects of the object. If needed, you can exclude them from
serialization by passing in the string names via the `exclude` argument.

> #### Example
>
> ```python
> data = vocab.to_bytes(exclude=["strings", "vectors"])
> vocab.from_disk("./vocab", exclude=["strings"])
> ```

| Name      | Description                                           |
| --------- | ----------------------------------------------------- |
| `strings` | The strings in the [`StringStore`](/api/stringstore). |
| `lexemes` | The lexeme data.                                      |
| `vectors` | The word vectors, if available.                       |
| `lookups` | The lookup tables, if available.                      |
