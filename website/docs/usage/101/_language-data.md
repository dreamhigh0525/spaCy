Every language is different – and usually full of **exceptions and special
cases**, especially amongst the most common words. Some of these exceptions are
shared across languages, while others are **entirely specific** – usually so
specific that they need to be hard-coded. The
[`lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang) module
contains all language-specific data, organized in simple Python files. This
makes the data easy to update and extend.

The **shared language data** in the directory root includes rules that can be
generalized across languages – for example, rules for basic punctuation, emoji,
emoticons, single-letter abbreviations and norms for equivalent tokens with
different spellings, like `"` and `”`. This helps the models make more accurate
predictions. The **individual language data** in a submodule contains rules that
are only relevant to a particular language. It also takes care of putting
together all components and creating the `Language` subclass – for example,
`English` or `German`.

> ```python
> from spacy.lang.en import English
> from spacy.lang.de import German
>
> nlp_en = English()  # Includes English data
> nlp_de = German()  # Includes German data
> ```

![Language data architecture](../../images/language_data.svg)

| Name                                                                               | Description                                                                                                                                              |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stop words**<br />[`stop_words.py`][stop_words.py]                               | List of most common words of a language that are often useful to filter out, for example "and" or "I". Matching tokens will return `True` for `is_stop`. |
| **Tokenizer exceptions**<br />[`tokenizer_exceptions.py`][tokenizer_exceptions.py] | Special-case rules for the tokenizer, for example, contractions like "can't" and abbreviations with punctuation, like "U.K.".                            |
| **Norm exceptions**<br />[`norm_exceptions.py`][norm_exceptions.py]                | Special-case rules for normalizing tokens to improve the model's predictions, for example on American vs. British spelling.                              |
| **Punctuation rules**<br />[`punctuation.py`][punctuation.py]                      | Regular expressions for splitting tokens, e.g. on punctuation or special characters like emoji. Includes rules for prefixes, suffixes and infixes.       |
| **Character classes**<br />[`char_classes.py`][char_classes.py]                    | Character classes to be used in regular expressions, for example, latin characters, quotes, hyphens or icons.                                            |
| **Lexical attributes**<br />[`lex_attrs.py`][lex_attrs.py]                         | Custom functions for setting lexical attributes on tokens, e.g. `like_num`, which includes language-specific words like "ten" or "hundred".              |
| **Syntax iterators**<br />[`syntax_iterators.py`][syntax_iterators.py]             | Functions that compute views of a `Doc` object based on its syntax. At the moment, only used for [noun chunks](/usage/linguistic-features#noun-chunks).  |
| **Lemmatizer**<br />[`lemmatizer.py`][lemmatizer.py]                               | Lemmatization rules or a lookup-based lemmatization table to assign base forms, for example "be" for "was".                                              |
| **Tag map**<br />[`tag_map.py`][tag_map.py]                                        | Dictionary mapping strings in your tag set to [Universal Dependencies](http://universaldependencies.org/u/pos/all.html) tags.                            |
| **Morph rules**<br />[`morph_rules.py`][morph_rules.py]                            | Exception rules for morphological analysis of irregular words like personal pronouns.                                                                    |

[stop_words.py]:
  https://github.com/explosion/spacy-dev-resources/tree/master/templates/new_language/stop_words.py
[tokenizer_exceptions.py]:
  https://github.com/explosion/spacy-dev-resources/tree/master/templates/new_language/tokenizer_exceptions.py
[norm_exceptions.py]:
  https://github.com/explosion/spaCy/tree/master/spacy/lang/norm_exceptions.py
[punctuation.py]:
  https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py
[char_classes.py]:
  https://github.com/explosion/spaCy/tree/master/spacy/lang/char_classes.py
[lex_attrs.py]:
  https://github.com/explosion/spacy-dev-resources/tree/master/templates/new_language/lex_attrs.py
[syntax_iterators.py]:
  https://github.com/explosion/spaCy/tree/master/spacy/lang/en/syntax_iterators.py
[lemmatizer.py]:
  https://github.com/explosion/spacy-dev-resources/tree/master/templates/new_language/lemmatizer.py
[tag_map.py]:
  https://github.com/explosion/spacy-dev-resources/tree/master/templates/new_language/tag_map.py
[morph_rules.py]:
  https://github.com/explosion/spaCy/tree/master/spacy/lang/en/morph_rules.py
