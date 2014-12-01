.. spaCy documentation master file, created by
   sphinx-quickstart on Tue Aug 19 16:27:38 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
spaCy NLP Tokenizer and Lexicon
================================

spaCy is a library for industrial-strength NLP in Python and Cython.  It
assumes that NLP is mostly about solving large machine learning problems, and that
solving these problems is mostly about feature extraction.  So, spaCy helps you
do feature extraction --- it includes an excellent set of distributional and
orthographic features, memoizes them efficiently, and maps strings to
consecutive integer values.

For commercial users, a trial license costs $0, with a one-time license fee of
$1,000 to use spaCy in production.  For non-commercial users, a GPL license is
available.  To quickly get the gist of the license terms, check out the license
user stories.


Tokenization done right
=======================

Most tokenizers rely on complicated regular expressions.  Often, they leave you
with no way to align the tokens back to the original string --- a vital feature
if you want to display some mark-up, such as spelling correction.  The regular
expressions also interact, making it hard to accommodate special cases.

spaCy introduces a **novel tokenization algorithm** that's much faster and much
more flexible:

.. code-block:: python

    def tokenize(string, prefixes={}, suffixes={}, specials={}):
        '''Sketch of spaCy's tokenization algorithm.'''
        tokens = []
        cache = {}
        for chunk in string.split():
            # Because of Zipf's law, the cache serves the majority of "chunks".
            if chunk in cache:
                tokens.extend(cache[chunl])
                continue
            key = chunk

            subtokens = []
            # Process a chunk by splitting off prefixes e.g. ( " { and suffixes e.g. , . :
            # If we split one off, check whether we're left with a special-case, 
            # e.g. contractions (can't, won't, etc), emoticons, abbreviations, etc.
            # This makes the tokenization easy to update and customize.
            while chunk:
                prefix, chunk = _consume_prefix(chunk, prefixes)
                if prefix:
                    subtokens.append(prefix)
                    if chunk in specials:
                        subtokens.extend(specials[chunk])
                        break
                suffix, chunk = _consume_suffix(chunk, suffixes)
                if suffix:
                    subtokens.append(suffix)
                    if chunk in specials:
                        subtokens.extend(specials[chunk])
                        break
            cache[key] = subtokens

Your data is going to have its own quirks, so it's really useful to have
a tokenizer you can easily control.  To see the limitations of the standard
regex-based approach, check out `CMU's recent work on tokenizing tweets <http://www.ark.cs.cmu.edu/TweetNLP/>`_. Despite a lot of careful attention, they can't handle all of their
known emoticons correctly --- doing so would interfere with the way they
process other punctuation.  This isn't a problem for spaCy: we just add them
all to the special tokenization rules.

spaCy's tokenizer is also incredibly efficient:

+--------+---------------+--------------+
| System | Tokens/second | Speed Factor |
+--------+---------------+--------------+
| NLTK   | 89 000        | 1.00         |
+--------+---------------+--------------+
| spaCy  | 3 093 000     | 38.30        |
+--------+---------------+--------------+

spaCy can create an inverted index of the 1.8 billion word Gigaword corpus,
keyed by lemmas, in under half an hour --- on a Macbook Air.

Unique Lexicon-centric design
=============================

spaCy takes care of all string-processing, efficiently and accurately.  This
makes a night-and-day difference to your feature extraction code.
Instead of a list of strings, spaCy's tokenizer gives you references to feature-rich
lexeme objects:

    >>> from spacy.en import EN
    >>> from spacy.feature_names import SIC, NORM, SHAPE, ASCIIED, PREFIX, SUFFIX, \
            LENGTH, CLUSTER, POS_TYPE, SENSE_TYPE, \
            IS_ALPHA, IS_ASCII, IS_DIGIT, IS_PUNCT, IS_SPACE, IS_TITLE, IS_UPPER, \
            LIKE_URL, LIKE_NUMBER
    >>> feats = (
            SIC, # ID of the original word form
            NORM, # ID of the normalized word form
            CLUSTER, # ID of the word's Brown cluster
            IS_TITLE, # Was the word title-cased?
            POS_TYPE # A cluster ID describing what POS tags the word is usually assigned
        )
    >>> tokens = EN.tokenize(u'Split words, punctuation, emoticons etc.! ^_^')
    >>> tokens.to_strings()
    [u'Split', u'words', u',', u'punctuation', u',', u'emoticons', u'etc.', u'!', u'^_^']
    >>> tokens.to_array(feats)[:5]
        array([[    1,  2,  3,  4],
               [...],
               [...],
               [...]])


spaCy is designed to **make the right thing easy**, where the right thing is to:

* **Use rich distributional and orthographic features**. Without these, your model
  will be very brittle and domain dependent.

* **Compute features per type, not per token**. Because of Zipf's law, you can
  expect this to be exponentially more efficient.

* **Minimize string processing**, and instead compute with arrays of ID ints.
  

Comparison with NLTK
====================

`NLTK <http://nltk.org>`_ provides interfaces to a wide-variety of NLP
tools and resources, and its own implementations of a few algorithms.  It comes
with comprehensive documentation, and a book introducing concepts in NLP.  For
these reasons, it's very widely known.  However, if you're trying to make money
or do cutting-edge research, NLTK is not a good choice.

The `list of stuff in NLTK <http://www.nltk.org/py-modindex.html>`_ looks impressive,
but almost none of it is useful for real work.  You're not going to make any money,
or do top research, by using the NLTK chat bots, theorem provers, toy CCG implementation,
etc.  Most of NLTK is there to assist in the explanation ideas in computational
linguistics, at roughly an undergraduate level.
But it also claims to support serious work, by wrapping external tools.

In a pretty well known essay, Joel Spolsky discusses the pain of dealing with 
`leaky abstractions <http://www.joelonsoftware.com/articles/LeakyAbstractions.html>`_.
An abstraction tells you to not care about implementation
details, but sometimes the implementation matters after all. When it
does, you have to waste time revising your assumptions.

NLTK's wrappers call external tools via subprocesses, and wrap this up so
that it looks like a native API.  This abstraction leaks *a lot*.  The system
calls impose far more overhead than a normal Python function call, which makes
the most natural way to program against the API infeasible. 


Case study: POS tagging
-----------------------

Here's a quick comparison of the following POS taggers:

* **Stanford (CLI)**: The Stanford POS tagger, invoked once as a batch process
  from the command-line;
* **nltk.tag.stanford**: The Stanford tagger, invoked document-by-document via
  NLTK's wrapper;
* **nltk.pos_tag**: NLTK's own POS tagger, invoked document-by-document.
* **spacy.en.pos_tag**: spaCy's POS tagger, invoked document-by-document.


+-------------------+-------------+--------+
| System            | Speed (w/s) | % Acc. |
+-------------------+-------------+--------+
| spaCy             | 107,000     | 96.7   |
+-------------------+-------------+--------+
| Stanford (CLI)    | 8,000       | 96.7   |
+-------------------+-------------+--------+
| nltk.pos_tag      | 543         | 94.0   |
+-------------------+-------------+--------+
| nltk.tag.stanford | 209         | 96.7   |
+-------------------+-------------+--------+

Experimental details TODO.  Three things are apparent from this comparison:

1. The native NLTK tagger, nltk.pos_tag, is both slow and inaccurate;

2. Calling the Stanford tagger document-by-document via NLTK is **40x** slower
   than invoking the model once as a batch process, via the command-line;

3. spaCy is over 10x faster than the Stanford tagger, even when called
   **sentence-by-sentence**.

The problem is that NLTK simply wraps the command-line
interfaces of these tools, so communication is via a subprocess.  NLTK does not
even hold open a pipe for you --- the model is reloaded, again and again.

To use the wrapper effectively, you should batch up your text as much as possible.
This probably isn't how you would like to structure your pipeline, and you
might not be able to batch up much text at all, e.g. if serving a single
request means processing a single document.
Technically, NLTK does give you Python functions to access lots of different
systems --- but, you can't use them as you would expect to use a normal Python
function.  The abstraction leaks.

Here's the bottom-line: the Stanford tools are written in Java, so using them
from Python sucks.  You shouldn't settle for this.  It's a problem that springs
purely from the tooling, rather than the domain.

Summary
-------

NLTK is a well-known Python library for NLP, but for the important bits, you
don't get actual Python modules.  You get wrappers which throw to external
tools, via subprocesses.  This is not at all the same thing.

spaCy is implemented in Cython, just like numpy, scikit-learn, lxml and other
high-performance Python libraries.  So you get a native Python API, but the
performance you expect from a program written in C.


.. toctree::
    :hidden:
    :maxdepth: 3

    features.rst
    
