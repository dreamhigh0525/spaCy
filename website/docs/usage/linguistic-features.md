---
title: Linguistic Features
next: /usage/rule-based-matching
menu:
  - ['POS Tagging', 'pos-tagging']
  - ['Dependency Parse', 'dependency-parse']
  - ['Named Entities', 'named-entities']
  - ['Entity Linking', 'entity-linking']
  - ['Tokenization', 'tokenization']
  - ['Merging & Splitting', 'retokenization']
  - ['Sentence Segmentation', 'sbd']
---

Processing raw text intelligently is difficult: most words are rare, and it's
common for words that look completely different to mean almost the same thing.
The same words in a different order can mean something completely different.
Even splitting text into useful word-like units can be difficult in many
languages. While it's possible to solve some problems starting from only the raw
characters, it's usually better to use linguistic knowledge to add useful
information. That's exactly what spaCy is designed to do: you put in raw text,
and get back a [`Doc`](/api/doc) object, that comes with a variety of
annotations.

## Part-of-speech tagging {#pos-tagging model="tagger, parser"}

import PosDeps101 from 'usage/101/\_pos-deps.md'

<PosDeps101 />

<Infobox title="📖 Part-of-speech tag scheme">

For a list of the fine-grained and coarse-grained part-of-speech tags assigned
by spaCy's models across different languages, see the
[POS tag scheme documentation](/api/annotation#pos-tagging).

</Infobox>

### Rule-based morphology {#rule-based-morphology}

Inflectional morphology is the process by which a root form of a word is
modified by adding prefixes or suffixes that specify its grammatical function
but do not changes its part-of-speech. We say that a **lemma** (root form) is
**inflected** (modified/combined) with one or more **morphological features** to
create a surface form. Here are some examples:

| Context                                  | Surface | Lemma | POS  |  Morphological Features                  |
| ---------------------------------------- | ------- | ----- | ---- | ---------------------------------------- |
| I was reading the paper                  | reading | read  | verb | `VerbForm=Ger`                           |
| I don't watch the news, I read the paper | read    | read  | verb | `VerbForm=Fin`, `Mood=Ind`, `Tense=Pres` |
| I read the paper yesterday               | read    | read  | verb | `VerbForm=Fin`, `Mood=Ind`, `Tense=Past` |

English has a relatively simple morphological system, which spaCy handles using
rules that can be keyed by the token, the part-of-speech tag, or the combination
of the two. The system works as follows:

1. The tokenizer consults a
   [mapping table](/usage/adding-languages#tokenizer-exceptions)
   `TOKENIZER_EXCEPTIONS`, which allows sequences of characters to be mapped to
   multiple tokens. Each token may be assigned a part of speech and one or more
   morphological features.
2. The part-of-speech tagger then assigns each token an **extended POS tag**. In
   the API, these tags are known as `Token.tag`. They express the part-of-speech
   (e.g. `VERB`) and some amount of morphological information, e.g. that the
   verb is past tense.
3. For words whose POS is not set by a prior process, a
   [mapping table](/usage/adding-languages#tag-map) `TAG_MAP` maps the tags to a
   part-of-speech and a set of morphological features.
4. Finally, a **rule-based deterministic lemmatizer** maps the surface form, to
   a lemma in light of the previously assigned extended part-of-speech and
   morphological information, without consulting the context of the token. The
   lemmatizer also accepts list-based exception files, acquired from
   [WordNet](https://wordnet.princeton.edu/).

## Dependency Parsing {#dependency-parse model="parser"}

spaCy features a fast and accurate syntactic dependency parser, and has a rich
API for navigating the tree. The parser also powers the sentence boundary
detection, and lets you iterate over base noun phrases, or "chunks". You can
check whether a [`Doc`](/api/doc) object has been parsed with the
`doc.is_parsed` attribute, which returns a boolean value. If this attribute is
`False`, the default sentence iterator will raise an exception.

### Noun chunks {#noun-chunks}

Noun chunks are "base noun phrases" – flat phrases that have a noun as their
head. You can think of noun chunks as a noun plus the words describing the noun
– for example, "the lavish green grass" or "the world’s largest tech fund". To
get the noun chunks in a document, simply iterate over
[`Doc.noun_chunks`](/api/doc#noun_chunks)

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)
```

> - **Text:** The original noun chunk text.
> - **Root text:** The original text of the word connecting the noun chunk to
>   the rest of the parse.
> - **Root dep:** Dependency relation connecting the root to its head.
> - **Root head text:** The text of the root token's head.

| Text                | root.text     | root.dep\_ | root.head.text |
| ------------------- | ------------- | ---------- | -------------- |
| Autonomous cars     | cars          | `nsubj`    | shift          |
| insurance liability | liability     | `dobj`     | shift          |
| manufacturers       | manufacturers | `pobj`     | toward         |

### Navigating the parse tree {#navigating}

spaCy uses the terms **head** and **child** to describe the words **connected by
a single arc** in the dependency tree. The term **dep** is used for the arc
label, which describes the type of syntactic relation that connects the child to
the head. As with other attributes, the value of `.dep` is a hash value. You can
get the string value with `.dep_`.

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])
```

> - **Text:** The original token text.
> - **Dep:** The syntactic relation connecting child to head.
> - **Head text:** The original text of the token head.
> - **Head POS:** The part-of-speech tag of the token head.
> - **Children:** The immediate syntactic dependents of the token.

| Text          | Dep        | Head text | Head POS | Children                |
| ------------- | ---------- | --------- | -------- | ----------------------- |
| Autonomous    | `amod`     | cars      | `NOUN`   |                         |
| cars          | `nsubj`    | shift     | `VERB`   | Autonomous              |
| shift         | `ROOT`     | shift     | `VERB`   | cars, liability, toward |
| insurance     | `compound` | liability | `NOUN`   |                         |
| liability     | `dobj`     | shift     | `VERB`   | insurance               |
| toward        | `prep`     | shift     | `NOUN`   | manufacturers           |
| manufacturers | `pobj`     | toward    | `ADP`    |                         |

import DisplaCyLong2Html from 'images/displacy-long2.html'

<Iframe title="displaCy visualization of dependencies and entities 2" html={DisplaCyLong2Html} height={450} />

Because the syntactic relations form a tree, every word has **exactly one
head**. You can therefore iterate over the arcs in the tree by iterating over
the words in the sentence. This is usually the best way to match an arc of
interest — from below:

```python
### {executable="true"}
import spacy
from spacy.symbols import nsubj, VERB

nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")

# Finding a verb with a subject from below — good
verbs = set()
for possible_subject in doc:
    if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
        verbs.add(possible_subject.head)
print(verbs)
```

If you try to match from above, you'll have to iterate twice. Once for the head,
and then again through the children:

```python
# Finding a verb with a subject from above — less good
verbs = []
for possible_verb in doc:
    if possible_verb.pos == VERB:
        for possible_subject in possible_verb.children:
            if possible_subject.dep == nsubj:
                verbs.append(possible_verb)
                break
```

To iterate through the children, use the `token.children` attribute, which
provides a sequence of [`Token`](/api/token) objects.

#### Iterating around the local tree {#navigating-around}

A few more convenience attributes are provided for iterating around the local
tree from the token. [`Token.lefts`](/api/token#lefts) and
[`Token.rights`](/api/token#rights) attributes provide sequences of syntactic
children that occur before and after the token. Both sequences are in sentence
order. There are also two integer-typed attributes,
[`Token.n_lefts`](/api/token#n_lefts) and
[`Token.n_rights`](/api/token#n_rights) that give the number of left and right
children.

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("bright red apples on the tree")
print([token.text for token in doc[2].lefts])  # ['bright', 'red']
print([token.text for token in doc[2].rights])  # ['on']
print(doc[2].n_lefts)  # 2
print(doc[2].n_rights)  # 1
```

```python
### {executable="true"}
import spacy

nlp = spacy.load("de_core_news_sm")
doc = nlp("schöne rote Äpfel auf dem Baum")
print([token.text for token in doc[2].lefts])  # ['schöne', 'rote']
print([token.text for token in doc[2].rights])  # ['auf']
```

You can get a whole phrase by its syntactic head using the
[`Token.subtree`](/api/token#subtree) attribute. This returns an ordered
sequence of tokens. You can walk up the tree with the
[`Token.ancestors`](/api/token#ancestors) attribute, and check dominance with
[`Token.is_ancestor`](/api/token#is_ancestor)

> #### Projective vs. non-projective
>
> For the [default English model](/models/en), the parse tree is **projective**,
> which means that there are no crossing brackets. The tokens returned by
> `.subtree` are therefore guaranteed to be contiguous. This is not true for the
> German model, which has many
> [non-projective dependencies](https://explosion.ai/blog/german-model#word-order).

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Credit and mortgage account holders must submit their requests")

root = [token for token in doc if token.head == token][0]
subject = list(root.lefts)[0]
for descendant in subject.subtree:
    assert subject is descendant or subject.is_ancestor(descendant)
    print(descendant.text, descendant.dep_, descendant.n_lefts,
            descendant.n_rights,
            [ancestor.text for ancestor in descendant.ancestors])
```

| Text     | Dep        | n_lefts | n_rights | ancestors                        |
| -------- | ---------- | ------- | -------- | -------------------------------- |
| Credit   | `nmod`     | `0`     | `2`      | holders, submit                  |
| and      | `cc`       | `0`     | `0`      | holders, submit                  |
| mortgage | `compound` | `0`     | `0`      | account, Credit, holders, submit |
| account  | `conj`     | `1`     | `0`      | Credit, holders, submit          |
| holders  | `nsubj`    | `1`     | `0`      | submit                           |

Finally, the `.left_edge` and `.right_edge` attributes can be especially useful,
because they give you the first and last token of the subtree. This is the
easiest way to create a `Span` object for a syntactic phrase. Note that
`.right_edge` gives a token **within** the subtree — so if you use it as the
end-point of a range, don't forget to `+1`!

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Credit and mortgage account holders must submit their requests")
span = doc[doc[4].left_edge.i : doc[4].right_edge.i+1]
with doc.retokenize() as retokenizer:
    retokenizer.merge(span)
for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)
```

| Text                                |  POS   | Dep     | Head text |
| ----------------------------------- | ------ | ------- | --------- |
| Credit and mortgage account holders | `NOUN` | `nsubj` | submit    |
| must                                | `VERB` | `aux`   | submit    |
| submit                              | `VERB` | `ROOT`  | submit    |
| their                               | `ADJ`  | `poss`  | requests  |
| requests                            | `NOUN` | `dobj`  | submit    |

<Infobox title="📖 Dependency label scheme">

For a list of the syntactic dependency labels assigned by spaCy's models across
different languages, see the
[dependency label scheme documentation](/api/annotation#dependency-parsing).

</Infobox>

### Visualizing dependencies {#displacy}

The best way to understand spaCy's dependency parser is interactively. To make
this easier, spaCy v2.0+ comes with a visualization module. You can pass a `Doc`
or a list of `Doc` objects to displaCy and run
[`displacy.serve`](/api/top-level#displacy.serve) to run the web server, or
[`displacy.render`](/api/top-level#displacy.render) to generate the raw markup.
If you want to know how to write rules that hook into some type of syntactic
construction, just plug the sentence into the visualizer and see how spaCy
annotates it.

```python
### {executable="true"}
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
# Since this is an interactive Jupyter environment, we can use displacy.render here
displacy.render(doc, style='dep')
```

<Infobox>

For more details and examples, see the
[usage guide on visualizing spaCy](/usage/visualizers). You can also test
displaCy in our [online demo](https://explosion.ai/demos/displacy)..

</Infobox>

### Disabling the parser {#disabling}

In the [default models](/models), the parser is loaded and enabled as part of
the [standard processing pipeline](/usage/processing-pipelin). If you don't need
any of the syntactic information, you should disable the parser. Disabling the
parser will make spaCy load and run much faster. If you want to load the parser,
but need to disable it for specific documents, you can also control its use on
the `nlp` object.

```python
nlp = spacy.load("en_core_web_sm", disable=["parser"])
nlp = English().from_disk("/model", disable=["parser"])
doc = nlp("I don't want parsed", disable=["parser"])
```

<Infobox title="Important note: disabling pipeline components" variant="warning">

Since spaCy v2.0 comes with better support for customizing the processing
pipeline components, the `parser` keyword argument has been replaced with
`disable`, which takes a list of
[pipeline component names](/usage/processing-pipelines). This lets you disable
both default and custom components when loading a model, or initializing a
Language class via [`from_disk`](/api/language#from_disk).

```diff
+ nlp = spacy.load("en_core_web_sm", disable=["parser"])
+ doc = nlp("I don't want parsed", disable=["parser"])

- nlp = spacy.load("en_core_web_sm", parser=False)
- doc = nlp("I don't want parsed", parse=False)
```

</Infobox>

## Named Entity Recognition {#named-entities}

spaCy features an extremely fast statistical entity recognition system, that
assigns labels to contiguous spans of tokens. The default model identifies a
variety of named and numeric entities, including companies, locations,
organizations and products. You can add arbitrary classes to the entity
recognition system, and update the model with new examples.

### Named Entity Recognition 101 {#named-entities-101}

import NER101 from 'usage/101/\_named-entities.md'

<NER101 />

### Accessing entity annotations {#accessing}

The standard way to access entity annotations is the [`doc.ents`](/api/doc#ents)
property, which produces a sequence of [`Span`](/api/span) objects. The entity
type is accessible either as a hash value or as a string, using the attributes
`ent.label` and `ent.label_`. The `Span` object acts as a sequence of tokens, so
you can iterate over the entity or index into it. You can also get the text form
of the whole entity, as though it were a single token.

You can also access token entity annotations using the
[`token.ent_iob`](/api/token#attributes) and
[`token.ent_type`](/api/token#attributes) attributes. `token.ent_iob` indicates
whether an entity starts, continues or ends on the tag. If no entity type is set
on a token, it will return an empty string.

> #### IOB Scheme
>
> - `I` – Token is inside an entity.
> - `O` – Token is outside an entity.
> - `B` – Token is the beginning of an entity.

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("San Francisco considers banning sidewalk delivery robots")

# document level
ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
print(ents)

# token level
ent_san = [doc[0].text, doc[0].ent_iob_, doc[0].ent_type_]
ent_francisco = [doc[1].text, doc[1].ent_iob_, doc[1].ent_type_]
print(ent_san)  # ['San', 'B', 'GPE']
print(ent_francisco)  # ['Francisco', 'I', 'GPE']
```

| Text      | ent_iob | ent_iob\_ | ent_type\_ | Description            |
| --------- | ------- | --------- | ---------- | ---------------------- |
| San       | `3`     | `B`       | `"GPE"`    | beginning of an entity |
| Francisco | `1`     | `I`       | `"GPE"`    | inside an entity       |
| considers | `2`     | `O`       | `""`       | outside an entity      |
| banning   | `2`     | `O`       | `""`       | outside an entity      |
| sidewalk  | `2`     | `O`       | `""`       | outside an entity      |
| delivery  | `2`     | `O`       | `""`       | outside an entity      |
| robots    | `2`     | `O`       | `""`       | outside an entity      |

### Setting entity annotations {#setting-entities}

To ensure that the sequence of token annotations remains consistent, you have to
set entity annotations **at the document level**. However, you can't write
directly to the `token.ent_iob` or `token.ent_type` attributes, so the easiest
way to set entities is to assign to the [`doc.ents`](/api/doc#ents) attribute
and create the new entity as a [`Span`](/api/span).

```python
### {executable="true"}
import spacy
from spacy.tokens import Span

nlp = spacy.load("en_core_web_sm")
doc = nlp("FB is hiring a new Vice President of global policy")
ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
print('Before', ents)
# the model didn't recognise "FB" as an entity :(

fb_ent = Span(doc, 0, 1, label="ORG") # create a Span for the new entity
doc.ents = list(doc.ents) + [fb_ent]

ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
print('After', ents)
# [('FB', 0, 2, 'ORG')] 🎉
```

Keep in mind that you need to create a `Span` with the start and end index of
the **token**, not the start and end index of the entity in the document. In
this case, "FB" is token `(0, 1)` – but at the document level, the entity will
have the start and end indices `(0, 2)`.

#### Setting entity annotations from array {#setting-from-array}

You can also assign entity annotations using the
[`doc.from_array`](/api/doc#from_array) method. To do this, you should include
both the `ENT_TYPE` and the `ENT_IOB` attributes in the array you're importing
from.

```python
### {executable="true"}
import numpy
import spacy
from spacy.attrs import ENT_IOB, ENT_TYPE

nlp = spacy.load("en_core_web_sm")
doc = nlp.make_doc("London is a big city in the United Kingdom.")
print("Before", doc.ents)  # []

header = [ENT_IOB, ENT_TYPE]
attr_array = numpy.zeros((len(doc), len(header)))
attr_array[0, 0] = 3  # B
attr_array[0, 1] = doc.vocab.strings["GPE"]
doc.from_array(header, attr_array)
print("After", doc.ents)  # [London]
```

#### Setting entity annotations in Cython {#setting-cython}

Finally, you can always write to the underlying struct, if you compile a
[Cython](http://cython.org/) function. This is easy to do, and allows you to
write efficient native code.

```python
# cython: infer_types=True
from spacy.tokens.doc cimport Doc

cpdef set_entity(Doc doc, int start, int end, int ent_type):
    for i in range(start, end):
        doc.c[i].ent_type = ent_type
    doc.c[start].ent_iob = 3
    for i in range(start+1, end):
        doc.c[i].ent_iob = 2
```

Obviously, if you write directly to the array of `TokenC*` structs, you'll have
responsibility for ensuring that the data is left in a consistent state.

### Built-in entity types {#entity-types}

> #### Tip: Understanding entity types
>
> You can also use `spacy.explain()` to get the description for the string
> representation of an entity label. For example, `spacy.explain("LANGUAGE")`
> will return "any named language".

<Infobox title="Annotation scheme">

For details on the entity types available in spaCy's pretrained models, see the
[NER annotation scheme](/api/annotation#named-entities).

</Infobox>

### Training and updating {#updating}

To provide training examples to the entity recognizer, you'll first need to
create an instance of the [`GoldParse`](/api/goldparse) class. You can specify
your annotations in a stand-off format or as token tags. If a character offset
in your entity annotations doesn't fall on a token boundary, the `GoldParse`
class will treat that annotation as a missing value. This allows for more
realistic training, because the entity recognizer is allowed to learn from
examples that may feature tokenizer errors.

```python
train_data = [
    ("Who is Chaka Khan?", [(7, 17, "PERSON")]),
    ("I like London and Berlin.", [(7, 13, "LOC"), (18, 24, "LOC")]),
]
```

```python
doc = Doc(nlp.vocab, ["rats", "make", "good", "pets"])
gold = GoldParse(doc, entities=["U-ANIMAL", "O", "O", "O"])
```

<Infobox>

For more details on **training and updating** the named entity recognizer, see
the usage guides on [training](/usage/training) or check out the runnable
[training script](https://github.com/explosion/spaCy/tree/master/examples/training/train_ner.py)
on GitHub.

</Infobox>

### Visualizing named entities {#displacy}

The
[displaCy <sup>ENT</sup> visualizer](https://explosion.ai/demos/displacy-ent)
lets you explore an entity recognition model's behavior interactively. If you're
training a model, it's very useful to run the visualization yourself. To help
you do that, spaCy v2.0+ comes with a visualization module. You can pass a `Doc`
or a list of `Doc` objects to displaCy and run
[`displacy.serve`](/api/top-level#displacy.serve) to run the web server, or
[`displacy.render`](/api/top-level#displacy.render) to generate the raw markup.

For more details and examples, see the
[usage guide on visualizing spaCy](/usage/visualizers).

```python
### Named Entity example
import spacy
from spacy import displacy

text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
displacy.serve(doc, style="ent")
```

import DisplacyEntHtml from 'images/displacy-ent2.html'

<Iframe title="displaCy visualizer for entities" html={DisplacyEntHtml} height={180} />

## Entity Linking {#entity-linking}

To ground the named entities into the "real world", spaCy provides functionality
to perform entity linking, which resolves a textual entity to a unique
identifier from a knowledge base (KB). The
[processing scripts](https://github.com/explosion/spaCy/tree/master/bin/wiki_entity_linking)
we provide use WikiData identifiers, but you can create your own
[`KnowledgeBase`](/api/kb) and
[train a new Entity Linking model](/usage/training#entity-linker) using that
custom-made KB.

### Accessing entity identifiers {#entity-linking-accessing}

The annotated KB identifier is accessible as either a hash value or as a string,
using the attributes `ent.kb_id` and `ent.kb_id_` of a [`Span`](/api/span)
object, or the `ent_kb_id` and `ent_kb_id_` attributes of a
[`Token`](/api/token) object.

```python
import spacy

nlp = spacy.load("my_custom_el_model")
doc = nlp("Ada Lovelace was born in London")

# document level
ents = [(e.text, e.label_, e.kb_id_) for e in doc.ents]
print(ents)  # [('Ada Lovelace', 'PERSON', 'Q7259'), ('London', 'GPE', 'Q84')]

# token level
ent_ada_0 = [doc[0].text, doc[0].ent_type_, doc[0].ent_kb_id_]
ent_ada_1 = [doc[1].text, doc[1].ent_type_, doc[1].ent_kb_id_]
ent_london_5 = [doc[5].text, doc[5].ent_type_, doc[5].ent_kb_id_]
print(ent_ada_0)  # ['Ada', 'PERSON', 'Q7259']
print(ent_ada_1)  # ['Lovelace', 'PERSON', 'Q7259']
print(ent_london_5)  # ['London', 'GPE', 'Q84']
```

| Text     | ent_type\_ | ent_kb_id\_ |
| -------- | ---------- | ----------- |
| Ada      | `"PERSON"` | `"Q7259"`   |
| Lovelace | `"PERSON"` | `"Q7259"`   |
| was      | -          | -           |
| born     | -          | -           |
| in       | -          | -           |
| London   | `"GPE"`    | `"Q84"`     |

## Tokenization {#tokenization}

Tokenization is the task of splitting a text into meaningful segments, called
_tokens_. The input to the tokenizer is a unicode text, and the output is a
[`Doc`](/api/doc) object. To construct a `Doc` object, you need a
[`Vocab`](/api/vocab) instance, a sequence of `word` strings, and optionally a
sequence of `spaces` booleans, which allow you to maintain alignment of the
tokens into the original string.

<Infobox title="Important note" variant="warning">

spaCy's tokenization is **non-destructive**, which means that you'll always be
able to reconstruct the original input from the tokenized output. Whitespace
information is preserved in the tokens and no information is added or removed
during tokenization. This is kind of a core principle of spaCy's `Doc` object:
`doc.text == input_text` should always hold true.

</Infobox>

import Tokenization101 from 'usage/101/\_tokenization.md'

<Tokenization101 />

### Tokenizer data {#101-data}

**Global** and **language-specific** tokenizer data is supplied via the language
data in
[`spacy/lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang). The
tokenizer exceptions define special cases like "don't" in English, which needs
to be split into two tokens: `{ORTH: "do"}` and `{ORTH: "n't", NORM: "not"}`.
The prefixes, suffixes and infixes mostly define punctuation rules – for
example, when to split off periods (at the end of a sentence), and when to leave
tokens containing periods intact (abbreviations like "U.S.").

![Language data architecture](../images/language_data.svg)

<Infobox title="📖 Language data">

For more details on the language-specific data, see the usage guide on
[adding languages](/usage/adding-languages).

</Infobox>

<Accordion title="Should I change the language data or add custom tokenizer rules?" id="lang-data-vs-tokenizer">

Tokenization rules that are specific to one language, but can be **generalized
across that language** should ideally live in the language data in
[`spacy/lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang) – we
always appreciate pull requests! Anything that's specific to a domain or text
type – like financial trading abbreviations, or Bavarian youth slang – should be
added as a special case rule to your tokenizer instance. If you're dealing with
a lot of customizations, it might make sense to create an entirely custom
subclass.

</Accordion>

---

### Adding special case tokenization rules {#special-cases}

Most domains have at least some idiosyncrasies that require custom tokenization
rules. This could be very certain expressions, or abbreviations only used in
this specific field. Here's how to add a special case rule to an existing
[`Tokenizer`](/api/tokenizer) instance:

```python
### {executable="true"}
import spacy
from spacy.symbols import ORTH

nlp = spacy.load("en_core_web_sm")
doc = nlp("gimme that")  # phrase to tokenize
print([w.text for w in doc])  # ['gimme', 'that']

# Add special case rule
special_case = [{ORTH: "gim"}, {ORTH: "me"}]
nlp.tokenizer.add_special_case("gimme", special_case)

# Check new tokenization
print([w.text for w in nlp("gimme that")])  # ['gim', 'me', 'that']
```

The special case doesn't have to match an entire whitespace-delimited substring.
The tokenizer will incrementally split off punctuation, and keep looking up the
remaining substring:

```python
assert "gimme" not in [w.text for w in nlp("gimme!")]
assert "gimme" not in [w.text for w in nlp('("...gimme...?")')]
```

The special case rules have precedence over the punctuation splitting:

```python
nlp.tokenizer.add_special_case("...gimme...?", [{"ORTH": "...gimme...?"}])
assert len(nlp("...gimme...?")) == 1
```

### How spaCy's tokenizer works {#how-tokenizer-works}

spaCy introduces a novel tokenization algorithm, that gives a better balance
between performance, ease of definition, and ease of alignment into the original
string.

After consuming a prefix or suffix, we consult the special cases again. We want
the special cases to handle things like "don't" in English, and we want the same
rule to work for "(don't)!". We do this by splitting off the open bracket, then
the exclamation, then the close bracket, and finally matching the special case.
Here's an implementation of the algorithm in Python, optimized for readability
rather than performance:

```python
def tokenizer_pseudo_code(self, special_cases, prefix_search, suffix_search,
                          infix_finditer, token_match):
    tokens = []
    for substring in text.split():
        suffixes = []
        while substring:
            while prefix_search(substring) or suffix_search(substring):
                if substring in special_cases:
                    tokens.extend(special_cases[substring])
                    substring = ''
                    break
                if prefix_search(substring):
                    split = prefix_search(substring).end()
                    tokens.append(substring[:split])
                    substring = substring[split:]
                    if substring in special_cases:
                        continue
                if suffix_search(substring):
                    split = suffix_search(substring).start()
                    suffixes.append(substring[split:])
                    substring = substring[:split]
            if substring in special_cases:
                tokens.extend(special_cases[substring])
                substring = ''
            elif token_match(substring):
                tokens.append(substring)
                substring = ''
            elif list(infix_finditer(substring)):
                infixes = infix_finditer(substring)
                offset = 0
                for match in infixes:
                    tokens.append(substring[offset : match.start()])
                    tokens.append(substring[match.start() : match.end()])
                    offset = match.end()
                if substring[offset:]:
                    tokens.append(substring[offset:])
                substring = ''
            elif substring:
                tokens.append(substring)
                substring = ''
        tokens.extend(reversed(suffixes))
    return tokens
```

The algorithm can be summarized as follows:

1. Iterate over whitespace-separated substrings.
2. Check whether we have an explicitly defined rule for this substring. If we
   do, use it.
3. Otherwise, try to consume one prefix. If we consumed a prefix, go back to #2,
   so that special cases always get priority.
4. If we didn't consume a prefix, try to consume a suffix and then go back to
   #2.
5. If we can't consume a prefix or a suffix, look for a special case.
6. Next, look for a token match.
7. Look for "infixes" — stuff like hyphens etc. and split the substring into
   tokens on all infixes.
8. Once we can't consume any more of the string, handle it as a single token.

### Customizing spaCy's Tokenizer class {#native-tokenizers}

Let's imagine you wanted to create a tokenizer for a new language or specific
domain. There are five things you would need to define:

1. A dictionary of **special cases**. This handles things like contractions,
   units of measurement, emoticons, certain abbreviations, etc.
2. A function `prefix_search`, to handle **preceding punctuation**, such as open
   quotes, open brackets, etc.
3. A function `suffix_search`, to handle **succeeding punctuation**, such as
   commas, periods, close quotes, etc.
4. A function `infixes_finditer`, to handle non-whitespace separators, such as
   hyphens etc.
5. An optional boolean function `token_match` matching strings that should never
   be split, overriding the infix rules. Useful for things like URLs or numbers.
   Note that prefixes and suffixes will be split off before `token_match` is
   applied.

You shouldn't usually need to create a `Tokenizer` subclass. Standard usage is
to use `re.compile()` to build a regular expression object, and pass its
`.search()` and `.finditer()` methods:

```python
### {executable="true"}
import re
import spacy
from spacy.tokenizer import Tokenizer

special_cases = {":)": [{"ORTH": ":)"}]}
prefix_re = re.compile(r'''^[\[\("']''')
suffix_re = re.compile(r'''[\]\)"']$''')
infix_re = re.compile(r'''[-~]''')
simple_url_re = re.compile(r'''^https?://''')

def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, rules=special_cases,
                                prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=simple_url_re.match)

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = custom_tokenizer(nlp)
doc = nlp("hello-world. :)")
print([t.text for t in doc]) # ['hello', '-', 'world.', ':)']
```

If you need to subclass the tokenizer instead, the relevant methods to
specialize are `find_prefix`, `find_suffix` and `find_infix`.

<Infobox title="Important note" variant="warning">

When customizing the prefix, suffix and infix handling, remember that you're
passing in **functions** for spaCy to execute, e.g. `prefix_re.search` – not
just the regular expressions. This means that your functions also need to define
how the rules should be applied. For example, if you're adding your own prefix
rules, you need to make sure they're only applied to characters at the
**beginning of a token**, e.g. by adding `^`. Similarly, suffix rules should
only be applied at the **end of a token**, so your expression should end with a
`$`.

</Infobox>

#### Modifying existing rule sets {#native-tokenizer-additions}

In many situations, you don't necessarily need entirely custom rules. Sometimes
you just want to add another character to the prefixes, suffixes or infixes. The
default prefix, suffix and infix rules are available via the `nlp` object's
`Defaults` and the `Tokenizer` attributes such as
[`Tokenizer.suffix_search`](/api/tokenizer#attributes) are writable, so you can
overwrite them with compiled regular expression objects using modified default
rules. spaCy ships with utility functions to help you compile the regular
expressions – for example,
[`compile_suffix_regex`](/api/top-level#util.compile_suffix_regex):

```python
suffixes = nlp.Defaults.suffixes + (r'''-+$''',)
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search
```

Similarly, you can remove a character from the default suffixes:

```python
suffixes = list(nlp.Defaults.suffixes)
suffixes.remove("\\\\[")
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search
```

The `Tokenizer.suffix_search` attribute should be a function which takes a
unicode string and returns a **regex match object** or `None`. Usually we use
the `.search` attribute of a compiled regex object, but you can use some other
function that behaves the same way.

<Infobox title="Important note" variant="warning">

If you're using a statistical model, writing to the `nlp.Defaults` or
`English.Defaults` directly won't work, since the regular expressions are read
from the model and will be compiled when you load it. If you modify
`nlp.Defaults`, you'll only see the effect if you call
[`spacy.blank`](/api/top-level#spacy.blank) or `Defaults.create_tokenizer()`. If
you want to modify the tokenizer loaded from a statistical model, you should
modify `nlp.tokenizer` directly.

</Infobox>

The prefix, infix and suffix rule sets include not only individual characters
but also detailed regular expressions that take the surrounding context into
account. For example, there is a regular expression that treats a hyphen between
letters as an infix. If you do not want the tokenizer to split on hyphens
between letters, you can modify the existing infix definition from
[`lang/punctuation.py`](https://github.com/explosion/spaCy/blob/master/spacy/lang/punctuation.py):

```python
### {executable="true"}
import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

# default tokenizer
nlp = spacy.load("en_core_web_sm")
doc = nlp("mother-in-law")
print([t.text for t in doc]) # ['mother', '-', 'in', '-', 'law']

# modify tokenizer infix patterns
infixes = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\\-\\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
        ),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        # EDIT: commented out regex that splits on hyphens between letters:
        #r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
        r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
    ]
)

infix_re = compile_infix_regex(infixes)
nlp.tokenizer.infix_finditer = infix_re.finditer
doc = nlp("mother-in-law")
print([t.text for t in doc]) # ['mother-in-law']
```

For an overview of the default regular expressions, see
[`lang/punctuation.py`](https://github.com/explosion/spaCy/blob/master/spacy/lang/punctuation.py)
and language-specific definitions such as
[`lang/de/punctuation.py`](https://github.com/explosion/spaCy/blob/master/spacy/lang/de/punctuation.py)
for German.

### Hooking an arbitrary tokenizer into the pipeline {#custom-tokenizer}

The tokenizer is the first component of the processing pipeline and the only one
that can't be replaced by writing to `nlp.pipeline`. This is because it has a
different signature from all the other components: it takes a text and returns a
`Doc`, whereas all other components expect to already receive a tokenized `Doc`.

![The processing pipeline](../images/pipeline.svg)

To overwrite the existing tokenizer, you need to replace `nlp.tokenizer` with a
custom function that takes a text, and returns a `Doc`.

```python
nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = my_tokenizer
```

| Argument    | Type    | Description               |
| ----------- | ------- | ------------------------- |
| `text`      | unicode | The raw text to tokenize. |
| **RETURNS** | `Doc`   | The tokenized document.   |

<Infobox title="Important note: using a custom tokenizer" variant="warning">

In spaCy v1.x, you had to add a custom tokenizer by passing it to the `make_doc`
keyword argument, or by passing a tokenizer "factory" to `create_make_doc`. This
was unnecessarily complicated. Since spaCy v2.0, you can write to
`nlp.tokenizer` instead. If your tokenizer needs the vocab, you can write a
function and use `nlp.vocab`.

```diff
- nlp = spacy.load("en_core_web_sm", make_doc=my_tokenizer)
- nlp = spacy.load("en_core_web_sm", create_make_doc=my_tokenizer_factory)

+ nlp.tokenizer = my_tokenizer
+ nlp.tokenizer = my_tokenizer_factory(nlp.vocab)
```

</Infobox>

### Example: A custom whitespace tokenizer {#custom-tokenizer-example}

To construct the tokenizer, we usually want attributes of the `nlp` pipeline.
Specifically, we want the tokenizer to hold a reference to the vocabulary
object. Let's say we have the following class as our tokenizer:

```python
### {executable="true"}
import spacy
from spacy.tokens import Doc

class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)
doc = nlp("What's happened to me? he thought. It wasn't a dream.")
print([t.text for t in doc])
```

As you can see, we need a `Vocab` instance to construct this — but we won't have
it until we get back the loaded `nlp` object. The simplest solution is to build
the tokenizer in two steps. This also means that you can reuse the "tokenizer
factory" and initialize it with different instances of `Vocab`.

### Bringing your own annotations {#own-annotations}

spaCy generally assumes by default that your data is raw text. However,
sometimes your data is partially annotated, e.g. with pre-existing tokenization,
part-of-speech tags, etc. The most common situation is that you have pre-defined
tokenization. If you have a list of strings, you can create a `Doc` object
directly. Optionally, you can also specify a list of boolean values, indicating
whether each word has a subsequent space.

```python
### {executable="true"}
import spacy
from spacy.tokens import Doc
from spacy.lang.en import English

nlp = English()
doc = Doc(nlp.vocab, words=["Hello", ",", "world", "!"],
          spaces=[False, True, False, False])
print([(t.text, t.text_with_ws, t.whitespace_) for t in doc])
```

If provided, the spaces list must be the same length as the words list. The
spaces list affects the `doc.text`, `span.text`, `token.idx`, `span.start_char`
and `span.end_char` attributes. If you don't provide a `spaces` sequence, spaCy
will assume that all words are whitespace delimited.

```python
### {executable="true"}
import spacy
from spacy.tokens import Doc
from spacy.lang.en import English

nlp = English()
bad_spaces = Doc(nlp.vocab, words=["Hello", ",", "world", "!"])
good_spaces = Doc(nlp.vocab, words=["Hello", ",", "world", "!"],
                  spaces=[False, True, False, False])

print(bad_spaces.text)   # 'Hello , world !'
print(good_spaces.text)  # 'Hello, world!'
```

Once you have a [`Doc`](/api/doc) object, you can write to its attributes to set
the part-of-speech tags, syntactic dependencies, named entities and other
attributes. For details, see the respective usage pages.

### Aligning tokenization {#aligning-tokenization}

spaCy's tokenization is non-destructive and uses language-specific rules
optimized for compatibility with treebank annotations. Other tools and resources
can sometimes tokenize things differently – for example, `"I'm"` →
`["I", "'", "m"]` instead of `["I", "'m"]`.

In situations like that, you often want to align the tokenization so that you
can merge annotations from different sources together, or take vectors predicted
by a
[pretrained BERT model](https://github.com/huggingface/pytorch-transformers) and
apply them to spaCy tokens. spaCy's [`gold.align`](/api/goldparse#align) helper
returns a `(cost, a2b, b2a, a2b_multi, b2a_multi)` tuple describing the number
of misaligned tokens, the one-to-one mappings of token indices in both
directions and the indices where multiple tokens align to one single token.

> #### ✏️ Things to try
>
> 1. Change the capitalization in one of the token lists – for example,
>    `"obama"` to `"Obama"`. You'll see that the alignment is case-insensitive.
> 2. Change `"podcasts"` in `other_tokens` to `"pod", "casts"`. You should see
>    that there are now 4 misaligned tokens and that the new many-to-one mapping
>    is reflected in `a2b_multi`.
> 3. Make `other_tokens` and `spacy_tokens` identical. You'll see that the
>    `cost` is `0` and all corresponding mappings are also identical.

```python
### {executable="true"}
from spacy.gold import align

other_tokens = ["i", "listened", "to", "obama", "'", "s", "podcasts", "."]
spacy_tokens = ["i", "listened", "to", "obama", "'s", "podcasts", "."]
cost, a2b, b2a, a2b_multi, b2a_multi = align(other_tokens, spacy_tokens)
print("Misaligned tokens:", cost)  # 2
print("One-to-one mappings a -> b", a2b)  # array([0, 1, 2, 3, -1, -1, 5, 6])
print("One-to-one mappings b -> a", b2a)  # array([0, 1, 2, 3, 5, 6, 7])
print("Many-to-one mappings a -> b", a2b_multi)  # {4: 4, 5: 4}
print("Many-to-one mappings b-> a", b2a_multi)  # {}
```

Here are some insights from the alignment information generated in the example
above:

- Two tokens are misaligned.
- The one-to-one mappings for the first four tokens are identical, which means
  they map to each other. This makes sense because they're also identical in the
  input: `"i"`, `"listened"`, `"to"` and `"obama"`.
- The index mapped to `a2b[6]` is `5`, which means that `other_tokens[6]`
  (`"podcasts"`) aligns to `spacy_tokens[5]` (also `"podcasts"`).
- `a2b[4]` is `-1`, which means that there is no one-to-one alignment for the
  token at `other_tokens[4]`. The token `"'"` doesn't exist on its own in
  `spacy_tokens`. The same goes for `a2b[5]` and `other_tokens[5]`, i.e. `"s"`.
- The dictionary `a2b_multi` shows that both tokens 4 and 5 of `other_tokens`
  (`"'"` and `"s"`) align to token 4 of `spacy_tokens` (`"'s"`).
- The dictionary `b2a_multi` shows that there are no tokens in `spacy_tokens`
  that map to multiple tokens in `other_tokens`.

<Infobox title="Important note" variant="warning">

The current implementation of the alignment algorithm assumes that both
tokenizations add up to the same string. For example, you'll be able to align
`["I", "'", "m"]` and `["I", "'m"]`, which both add up to `"I'm"`, but not
`["I", "'m"]` and `["I", "am"]`.

</Infobox>

## Merging and splitting {#retokenization new="2.1"}

The [`Doc.retokenize`](/api/doc#retokenize) context manager lets you merge and
split tokens. Modifications to the tokenization are stored and performed all at
once when the context manager exits. To merge several tokens into one single
token, pass a `Span` to [`retokenizer.merge`](/api/doc#retokenizer.merge). An
optional dictionary of `attrs` lets you set attributes that will be assigned to
the merged token – for example, the lemma, part-of-speech tag or entity type. By
default, the merged token will receive the same attributes as the merged span's
root.

> #### ✏️ Things to try
>
> 1. Inspect the `token.lemma_` attribute with and without setting the `attrs`.
>    You'll see that the lemma defaults to "New", the lemma of the span's root.
> 2. Overwrite other attributes like the `"ENT_TYPE"`. Since "New York" is also
>    recognized as a named entity, this change will also be reflected in the
>    `doc.ents`.

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("I live in New York")
print("Before:", [token.text for token in doc])

with doc.retokenize() as retokenizer:
    retokenizer.merge(doc[3:5], attrs={"LEMMA": "new york"})
print("After:", [token.text for token in doc])
```

> #### Tip: merging entities and noun phrases
>
> If you need to merge named entities or noun chunks, check out the built-in
> [`merge_entities`](/api/pipeline-functions#merge_entities) and
> [`merge_noun_chunks`](/api/pipeline-functions#merge_noun_chunks) pipeline
> components. When added to your pipeline using `nlp.add_pipe`, they'll take
> care of merging the spans automatically.

If an attribute in the `attrs` is a context-dependent token attribute, it will
be applied to the underlying [`Token`](/api/token). For example `LEMMA`, `POS`
or `DEP` only apply to a word in context, so they're token attributes. If an
attribute is a context-independent lexical attribute, it will be applied to the
underlying [`Lexeme`](/api/lexeme), the entry in the vocabulary. For example,
`LOWER` or `IS_STOP` apply to all words of the same spelling, regardless of the
context.

<Infobox variant="warning" title="Note on merging overlapping spans">

If you're trying to merge spans that overlap, spaCy will raise an error because
it's unclear how the result should look. Depending on the application, you may
want to match the shortest or longest possible span, so it's up to you to filter
them. If you're looking for the longest non-overlapping span, you can use the
[`util.filter_spans`](/api/top-level#util.filter_spans) helper:

```python
doc = nlp("I live in Berlin Kreuzberg")
spans = [doc[3:5], doc[3:4], doc[4:5]]
filtered_spans = filter_spans(spans)
```

</Infobox>

### Splitting tokens

The [`retokenizer.split`](/api/doc#retokenizer.split) method allows splitting
one token into two or more tokens. This can be useful for cases where
tokenization rules alone aren't sufficient. For example, you might want to split
"its" into the tokens "it" and "is" — but not the possessive pronoun "its". You
can write rule-based logic that can find only the correct "its" to split, but by
that time, the `Doc` will already be tokenized.

This process of splitting a token requires more settings, because you need to
specify the text of the individual tokens, optional per-token attributes and how
the should be attached to the existing syntax tree. This can be done by
supplying a list of `heads` – either the token to attach the newly split token
to, or a `(token, subtoken)` tuple if the newly split token should be attached
to another subtoken. In this case, "New" should be attached to "York" (the
second split subtoken) and "York" should be attached to "in".

> #### ✏️ Things to try
>
> 1. Assign different attributes to the subtokens and compare the result.
> 2. Change the heads so that "New" is attached to "in" and "York" is attached
>    to "New".
> 3. Split the token into three tokens instead of two – for example,
>    `["New", "Yo", "rk"]`.

```python
### {executable="true"}
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("I live in NewYork")
print("Before:", [token.text for token in doc])
displacy.render(doc)  # displacy.serve if you're not in a Jupyter environment

with doc.retokenize() as retokenizer:
    heads = [(doc[3], 1), doc[2]]
    attrs = {"POS": ["PROPN", "PROPN"], "DEP": ["pobj", "compound"]}
    retokenizer.split(doc[3], ["New", "York"], heads=heads, attrs=attrs)
print("After:", [token.text for token in doc])
displacy.render(doc)  # displacy.serve if you're not in a Jupyter environment
```

Specifying the heads as a list of `token` or `(token, subtoken)` tuples allows
attaching split subtokens to other subtokens, without having to keep track of
the token indices after splitting.

| Token    | Head          | Description                                                                                         |
| -------- | ------------- | --------------------------------------------------------------------------------------------------- |
| `"New"`  | `(doc[3], 1)` | Attach this token to the second subtoken (index `1`) that `doc[3]` will be split into, i.e. "York". |
| `"York"` | `doc[2]`      | Attach this token to `doc[1]` in the original `Doc`, i.e. "in".                                     |

If you don't care about the heads (for example, if you're only running the
tokenizer and not the parser), you can each subtoken to itself:

```python
### {highlight="3"}
doc = nlp("I live in NewYorkCity")
with doc.retokenize() as retokenizer:
    heads = [(doc[3], 0), (doc[3], 1), (doc[3], 2)]
    retokenizer.split(doc[3], ["New", "York", "City"], heads=heads)
```

<Infobox title="Important note" variant="warning">

When splitting tokens, the subtoken texts always have to match the original
token text – or, put differently `"".join(subtokens) == token.text` always needs
to hold true. If this wasn't the case, splitting tokens could easily end up
producing confusing and unexpected results that would contradict spaCy's
non-destructive tokenization policy.

```diff
doc = nlp("I live in L.A.")
with doc.retokenize() as retokenizer:
-    retokenizer.split(doc[3], ["Los", "Angeles"], heads=[(doc[3], 1), doc[2]])
+    retokenizer.split(doc[3], ["L.", "A."], heads=[(doc[3], 1), doc[2]])
```

</Infobox>

### Overwriting custom extension attributes {#retokenization-extensions}

If you've registered custom
[extension attributes](/usage/processing-pipelines##custom-components-attributes),
you can overwrite them during tokenization by providing a dictionary of
attribute names mapped to new values as the `"_"` key in the `attrs`. For
merging, you need to provide one dictionary of attributes for the resulting
merged token. For splitting, you need to provide a list of dictionaries with
custom attributes, one per split subtoken.

<Infobox title="Important note" variant="warning">

To set extension attributes during retokenization, the attributes need to be
**registered** using the [`Token.set_extension`](/api/token#set_extension)
method and they need to be **writable**. This means that they should either have
a default value that can be overwritten, or a getter _and_ setter. Method
extensions or extensions with only a getter are computed dynamically, so their
values can't be overwritten. For more details, see the
[extension attribute docs](/usage/processing-pipelines/#custom-components-attributes).

</Infobox>

> #### ✏️ Things to try
>
> 1. Add another custom extension – maybe `"music_style"`? – and overwrite it.
> 2. Change the extension attribute to use only a `getter` function. You should
>    see that spaCy raises an error, because the attribute is not writable
>    anymore.
> 3. Rewrite the code to split a token with `retokenizer.split`. Remember that
>    you need to provide a list of extension attribute values as the `"_"`
>    property, one for each split subtoken.

```python
### {executable="true"}
import spacy
from spacy.tokens import Token

# Register a custom token attribute, token._.is_musician
Token.set_extension("is_musician", default=False)

nlp = spacy.load("en_core_web_sm")
doc = nlp("I like David Bowie")
print("Before:", [(token.text, token._.is_musician) for token in doc])

with doc.retokenize() as retokenizer:
    retokenizer.merge(doc[2:4], attrs={"_": {"is_musician": True}})
print("After:", [(token.text, token._.is_musician) for token in doc])
```

## Sentence Segmentation {#sbd}

A [`Doc`](/api/doc) object's sentences are available via the `Doc.sents`
property. Unlike other libraries, spaCy uses the dependency parse to determine
sentence boundaries. This is usually more accurate than a rule-based approach,
but it also means you'll need a **statistical model** and accurate predictions.
If your texts are closer to general-purpose news or web text, this should work
well out-of-the-box. For social media or conversational text that doesn't follow
the same rules, your application may benefit from a custom rule-based
implementation. You can either use the built-in
[`Sentencizer`](/api/sentencizer) or plug an entirely custom rule-based function
into your [processing pipeline](/usage/processing-pipelines).

spaCy's dependency parser respects already set boundaries, so you can preprocess
your `Doc` using custom rules _before_ it's parsed. Depending on your text, this
may also improve accuracy, since the parser is constrained to predict parses
consistent with the sentence boundaries.

### Default: Using the dependency parse {#sbd-parser model="parser"}

To view a `Doc`'s sentences, you can iterate over the `Doc.sents`, a generator
that yields [`Span`](/api/span) objects.

```python
### {executable="true"}
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence. This is another sentence.")
for sent in doc.sents:
    print(sent.text)
```

### Rule-based pipeline component {#sbd-component}

The [`Sentencizer`](/api/sentencizer) component is a
[pipeline component](/usage/processing-pipelines) that splits sentences on
punctuation like `.`, `!` or `?`. You can plug it into your pipeline if you only
need sentence boundaries without the dependency parse.

```python
### {executable="true"}
import spacy
from spacy.lang.en import English

nlp = English()  # just the language with no model
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)
doc = nlp("This is a sentence. This is another sentence.")
for sent in doc.sents:
    print(sent.text)
```

### Custom rule-based strategy {id="sbd-custom"}

If you want to implement your own strategy that differs from the default
rule-based approach of splitting on sentences, you can also create a
[custom pipeline component](/usage/processing-pipelines#custom-components) that
takes a `Doc` object and sets the `Token.is_sent_start` attribute on each
individual token. If set to `False`, the token is explicitly marked as _not_ the
start of a sentence. If set to `None` (default), it's treated as a missing value
and can still be overwritten by the parser.

<Infobox title="Important note" variant="warning">

To prevent inconsistent state, you can only set boundaries **before** a document
is parsed (and `Doc.is_parsed` is `False`). To ensure that your component is
added in the right place, you can set `before='parser'` or `first=True` when
adding it to the pipeline using [`nlp.add_pipe`](/api/language#add_pipe).

</Infobox>

Here's an example of a component that implements a pre-processing rule for
splitting on `'...'` tokens. The component is added before the parser, which is
then used to further segment the text. That's possible, because `is_sent_start`
is only set to `True` for some of the tokens – all others still specify `None`
for unset sentence boundaries. This approach can be useful if you want to
implement **additional** rules specific to your data, while still being able to
take advantage of dependency-based sentence segmentation.

```python
### {executable="true"}
import spacy

text = "this is a sentence...hello...and another sentence."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
print("Before:", [sent.text for sent in doc.sents])

def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "...":
            doc[token.i+1].is_sent_start = True
    return doc

nlp.add_pipe(set_custom_boundaries, before="parser")
doc = nlp(text)
print("After:", [sent.text for sent in doc.sents])
```

## Rule-based matching {#rule-based-matching hidden="true"}

<div id="rule-based-matching">
<Infobox title="📖 Rule-based matching" id="rule-based-matching">

The documentation on rule-based matching
[has moved to its own page](/usage/rule-based-matching).

</Infobox>
</div>
