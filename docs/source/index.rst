.. spaCy documentation master file, created by
   sphinx-quickstart on Tue Aug 19 16:27:38 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================
spaCy: Industrial-strength NLP
==============================

spaCy is a new library for text processing in Python and Cython.

Most commercial NLP development is based on obsolete
technology.  Over the last 3-5 years, the field has advanced dramatically, but
only the tech giants have really been able to capitalize.  The research is all
public, but it's been too hard for small companies to read and apply it.  
Many end up relying on `NLTK`_, which is intended primarily as an educational
resource.

.. _NLTK: https://www.nltk.org/

If you're a small company doing NLP, I think spaCy will seem like a minor miracle.
It's by far the fastest NLP software available.  The full processing pipeline
completes in 7ms per document, including accurate tagging and parsing.  All strings
are mapped to integer IDs, tokens are linked to embedded word representations,
and a range of useful features are pre-calculated and cached.

If none of that made any sense to you, here's the gist of it.  Computers don't
understand text. This is unfortunate, because that's what the web almost entirely
consists of.  We want to recommend people text based on other text they liked.
We want to shorten text to display it on a mobile screen.  We want to aggregate
it, link it, filter it, categorise it, generate it and correct it.

spaCy provides a library of utility functions that help programmers build such
products.  It's commercial open source software: you can either use it under
the AGPL, or you can `buy a commercial license`_ for a one-time fee. 

.. _buy a commercial license: license.rst

Example functionality
---------------------

Let's say you're developing a proofreading tool, or possibly an IDE for
writers.  You're convinced by Stephen King's advice that `adverbs are not your
friend <http://www.brainpickings.org/2013/03/13/stephen-king-on-adverbs/>`_, so
you want to **highlight all adverbs**.  We'll use one of the examples he finds
particularly egregious:

    >>> import spacy.en
    >>> from spacy.postags import ADVERB
    >>> # Load the pipeline, and call it with some text.
    >>> nlp = spacy.en.English()
    >>> tokens = nlp("‘Give it back,’ he pleaded abjectly, ‘it’s mine.’",
                     tag=True, parse=True)
    >>> output = ''
    >>> for tok in tokens:
    ...     output += tok.string.upper() if tok.pos == ADVERB else tok.string
    ...     output += tok.whitespace
    >>> print(output)
    ‘Give it BACK,’ he pleaded ABJECTLY, ‘it’s mine.’


Easy enough --- but the problem is that we've also highlighted "back", when probably
we only wanted to highlight "abjectly". While "back" is undoubtedly an adverb,
we probably don't want to highlight it.

There are lots of ways we might refine our logic, depending on just what words
we want to flag.  The simplest way to filter out adverbs like "back" and "not"
is by word frequency: these words are much more common than the prototypical
manner adverbs that the style guides are worried about.

The prob attribute of a Lexeme or Token object gives a log probability estimate
of the word, based on smoothed counts from a 3bn word corpus:

   >>> nlp.vocab[u'back'].prob
   -7.403977394104004
   >>> nlp.vocab[u'not'].prob
   -5.407193660736084
   >>> nlp.vocab[u'quietly'].prob
   -11.07155704498291

So we can easily exclude the N most frequent words in English from our adverb
marker.  Let's try N=1000 for now:

    >>> import spacy.en
    >>> from spacy.postags import ADVERB
    >>> nlp = spacy.en.English()
    >>> # Find log probability of Nth most frequent word
    >>> probs = [lex.prob for lex in nlp.vocab]
    >>> is_adverb = lambda tok: tok.pos == ADVERB and tok.prob < probs[-1000]
    >>> tokens = nlp("‘Give it back,’ he pleaded abjectly, ‘it’s mine.’",
                     tag=True, parse=True)
    >>> print(''.join(tok.string.upper() if is_adverb(tok) else tok.string))
    ‘Give it back,’ he pleaded ABJECTLY, ‘it’s mine.’

There are lots of ways we could refine the logic, depending on just what words we
want to flag.  Let's say we wanted to only flag adverbs that modified words
similar to "pleaded".  This is easy to do, as spaCy loads a vector-space
representation for every word (by default, the vectors produced by
`Levy and Goldberg (2014)`_.  Naturally, the vector is provided as a numpy
array:

    >>> pleaded = tokens[8]
    >>> pleaded.repvec.shape
    (300,)

.. _Levy and Goldberg (2014): https://levyomer.wordpress.com/2014/04/25/dependency-based-word-embeddings/

We want to sort the words in our vocabulary by their similarity to "pleaded".
There are lots of ways to measure the similarity of two vectors.  We'll use the
cosine metric:

    >>> from numpy import dot
    >>> from numpy.linalg import norm
    >>> cosine = lambda v1, v2: dot(v1, v2) / (norm(v1), norm(v2))
    >>> words = [w for w in nlp.vocab if w.is_lower and w.has_repvec]
    >>> words.sort(key=lambda w: cosine(w, pleaded))
    >>> words.reverse()
    >>> print '1-20', ', '.join(w.orth_ for w in words[0:20])
    1-20 pleaded, pled, plead, confessed, interceded, pleads, testified, conspired, motioned, demurred, countersued, remonstrated, begged, apologised, consented, acquiesced, petitioned, quarreled, appealed, pleading
    >>> print '50-60', ', '.join(w.orth_ for w in words[50:60])
    50-60 counselled, bragged, backtracked, caucused, refiled, dueled, mused, dissented, yearned, confesses
    >>> print '100-110', ', '.join(w.orth_ for w in words[100:110])
    cabled, ducked, sentenced, perjured, absconded, bargained, overstayed, clerked, confided, sympathizes
    >>> print '1000-1010', ', '.join(w.orth_ for w in words[1000:1010])
    scorned, baled, righted, requested, swindled, posited, firebombed, slimed, deferred, sagged
    >>> print ', '.join(w.orth_ for w in words[50000:50010])
    fb, ford, systems, puck, anglers, ik, tabloid, dirty, rims, artists

As you can see, the similarity model that these vectors give us is excellent
--- we're still getting meaningful results at 1000 words, off a single
prototype!  The only problem is that the list really contains two clusters of
words: one associated with the legal meaning of "pleaded", and one for the more
general sense.  Sorting out these clusters is an area of active research.

A simple work-around is to average the vectors of several words, and use that
as our target:

    >>> say_verbs = [u'pleaded', u'confessed', u'remonstrated', u'begged',
                     u'bragged', u'confided', u'requested']
    >>> say_vector = numpy.zeros(shape=(300,))
    >>> for verb in say_verbs:
    ...   say_vector += nlp.vocab[verb].repvec
    >>> words.sort(key=lambda w: cosine(w.repvec, say_vector))
    >>> words.reverse()
    >>> print '1-20', ', '.join(w.orth_ for w in words[0:20])
    1-20 bragged, remonstrated, enquired, demurred, sighed, mused, intimated, retorted, entreated, motioned, ranted, confided, countersued, gestured, implored, interceded, muttered, marvelled, bickered, despaired
    50-60 flaunted, quarrelled, ingratiated, vouched, agonized, apologised, lunched, joked, chafed, schemed
    >>> print '1000-1010', ', '.join(w.orth_ for w in words[1000:1010])
    1000-1010 hoarded, waded, ensnared, clamoring, abided, deploring, shriveled, endeared, rethought, berate

These definitely look like words that King might scold a writer for attaching
adverbs to.  Recall that our previous adverb highlighting function looked like
this:

    >>> import spacy.en
    >>> from spacy.postags import ADVERB
    >>> # Load the pipeline, and call it with some text.
    >>> nlp = spacy.en.English()
    >>> tokens = nlp("‘Give it back,’ he pleaded abjectly, ‘it’s mine.’",
                     tag=True, parse=True)
    >>> output = ''
    >>> for tok in tokens:
    ...     output += tok.string.upper() if tok.pos == ADVERB else tok.string
    ...     output += tok.whitespace
    >>> print(output)
    ‘Give it BACK,’ he pleaded ABJECTLY, ‘it’s mine.’

We wanted to refine the logic so that only adverbs modifying evocative verbs 
of communication, like "pleaded", were highlighted.  We've now built a vector that
represents that type of word, so now we can highlight adverbs based on very
subtle logic, honing in on adverbs that seem the most stylistically
problematic, given our starting assumptions:

    >>> import numpy
    >>> from numpy import dot
    >>> from numpy.linalg import norm
    >>> import spacy.en
    >>> from spacy.postags import ADVERB, VERB
    >>> def is_bad_adverb(token, target_verb, tol):
    ...   if token.pos != ADVERB 
    ...     return False
    ...   elif toke.head.pos != VERB:
    ...     return False
    ...   elif cosine(token.head.repvec, target_verb) < tol:
    ...     return False
    ...   else:
    ...     return True


This example was somewhat contrived --- and, truth be told, I've never really
bought the idea that adverbs were a grave stylistic sin.  But hopefully it got
the message across: the state-of-the-art NLP technologies are very powerful.
spaCy gives you easy and efficient access to them, which lets you build all
sorts of use products and features that were previously impossible.


Efficiency
----------

.. table:: Efficiency comparison. See `Benchmarks`_ for details.

  +--------------+---------------------------+--------------------------------+
  |              | Absolute (ms per doc)     | Relative (to spaCy)            |
  +--------------+----------+--------+-------+----------+---------+-----------+
  | System       | Tokenize | Tag    | Parse | Tokenize | Tag     | Parse     |
  +--------------+----------+--------+-------+----------+---------+-----------+
  | spaCy        | 0.2ms    | 1ms    | 7ms   | 1x       | 1x      | 1x        |
  +--------------+----------+--------+-------+----------+---------+-----------+
  | CoreNLP      | 2ms      | 10ms   | 49ms  | 10x      | 10x     | 7x        |
  +--------------+----------+--------+-------+----------+---------+-----------+
  | ZPar         | 1ms      | 8ms    | 850ms | 5x       | 8x      | 121x      |
  +--------------+----------+--------+-------+----------+---------+-----------+
  | NLTK         | 4ms      | 443ms  | n/a   | 20x      | 443x    |  n/a      |
  +--------------+----------+--------+-------+----------+---------+-----------+


Efficiency is a major concern for NLP applications.  It is very common to hear
people say that they cannot afford more detailed processing, because their
datasets are too large.  This is a bad position to be in.  If you can't apply
detailed processing, you generally have to cobble together various heuristics.
This normally takes a few iterations, and what you come up with will usually be
brittle and difficult to reason about.

spaCy's parser is faster than most taggers, and its tokenizer is fast enough
for any workload.  And the tokenizer doesn't just give you a list
of strings.  A spaCy token is a pointer to a Lexeme struct, from which you can
access a wide range of pre-computed features, including embedded word
representations.

.. I wrote spaCy because I think existing commercial NLP engines are crap.
  Alchemy API are a typical example.  Check out this part of their terms of
  service:
  publish or perform any benchmark or performance tests or analysis relating to
  the Service or the use thereof without express authorization from AlchemyAPI;

.. Did you get that? You're not allowed to evaluate how well their system works,
  unless you're granted a special exception.  Their system must be pretty
  terrible to motivate such an embarrassing restriction.
  They must know this makes them look bad, but they apparently believe allowing
  you to evaluate their product would make them look even worse!

.. spaCy is based on science, not alchemy.  It's open source, and I am happy to
  clarify any detail of the algorithms I've implemented.
  It's evaluated against the current best published systems, following the standard
  methodologies.  These evaluations show that it performs extremely well.  

Accuracy
--------

.. table:: Accuracy comparison, on the standard benchmark data from the Wall Street Journal.

.. See `Benchmarks`_ for details.

  +--------------+----------+------------+
  | System       | POS acc. | Parse acc. |
  +--------------+----------+------------+
  | spaCy        | 97.2     | 92.4       |
  +--------------+----------+------------+
  | CoreNLP      | 96.9     | 92.2       | 
  +--------------+----------+------------+
  | ZPar         | 97.3     | 92.9       |
  +--------------+----------+------------+
  | Redshift     | 97.3     | 93.5       |
  +--------------+----------+------------+
  | NLTK         | 94.3     | n/a        |
  +--------------+----------+------------+

The table above compares spaCy to some of the current state-of-the-art systems,
on the standard evaluation from the Wall Street Journal, given gold-standard
sentence boundaries and tokenization.  I'm in the process of completing a more
realistic evaluation on web text.

spaCy's parser offers a better speed/accuracy trade-off than any published
system: its accuracy is within 1% of the current state-of-the-art, and it's
seven times faster than the 2014 CoreNLP neural network parser, which is the
previous fastest parser that I'm aware of.


.. toctree::
    :maxdepth: 3

    index.rst
    quickstart.rst
    api.rst
    howworks.rst
    license.rst 
