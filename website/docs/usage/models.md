---
title: Models & Languages
next: usage/facts-figures
menu:
  - ['Quickstart', 'quickstart']
  - ['Language Support', 'languages']
  - ['Installation & Usage', 'download']
  - ['Production Use', 'production']
---

spaCy's trained pipelines can be installed as **Python packages**. This means
that they're a component of your application, just like any other module.
They're versioned and can be defined as a dependency in your `requirements.txt`.
Trained pipelines can be installed from a download URL or a local directory,
manually or via [pip](https://pypi.python.org/pypi/pip). Their data can be
located anywhere on your file system.

> #### Important note
>
> If you're upgrading to spaCy v3.x, you need to **download the new pipeline
> packages**. If you've trained your own pipelines, you need to **retrain** them
> after updating spaCy.

## Quickstart {hidden="true"}

import QuickstartModels from 'widgets/quickstart-models.js'

<QuickstartModels title="Quickstart" id="quickstart" description="Install a default trained pipeline package, get the code to load it from within spaCy and an example to test it. For more options, see the section on available packages below." />

## Language support {#languages}

spaCy currently provides support for the following languages. You can help by
[improving the existing language data](/usage/adding-languages#language-data)
and extending the tokenization patterns.
[See here](https://github.com/explosion/spaCy/issues/3056) for details on how to
contribute to development.

> #### Usage note
>
> If a trained pipeline is available for a language, you can download it using
> the [`spacy download`](/api/cli#download) command. In order to use languages
> that don't yet come with a trained pipeline, you have to import them directly,
> or use [`spacy.blank`](/api/top-level#spacy.blank):
>
> ```python
> from spacy.lang.fi import Finnish
> nlp = Finnish()  # use directly
> nlp = spacy.blank("fi")  # blank instance
> ```
>
> If lemmatization rules are available for your language, make sure to install
> spaCy with the `lookups` option, or install
> [`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data)
> separately in the same environment:
>
> ```bash
> $ pip install spacy[lookups]
> ```

import Languages from 'widgets/languages.js'

<Languages />

### Multi-language support {#multi-language new="2"}

> ```python
> # Standard import
> from spacy.lang.xx import MultiLanguage
> nlp = MultiLanguage()
>
> # With lazy-loading
> nlp = spacy.blank("xx")
> ```

spaCy also supports pipelines trained on more than one language. This is
especially useful for named entity recognition. The language ID used for
multi-language or language-neutral pipelines is `xx`. The language class, a
generic subclass containing only the base language data, can be found in
[`lang/xx`](%%GITHUB_SPACY/spacy/lang/xx).

To train a pipeline using the neutral multi-language class, you can set
`lang = "xx"` in your [training config](/usage/training#config). You can also
import the `MultiLanguage` class directly, or call
[`spacy.blank("xx")`](/api/top-level#spacy.blank) for lazy-loading.

### Chinese language support {#chinese new=2.3}

The Chinese language class supports three word segmentation options:

> ```python
> from spacy.lang.zh import Chinese
>
> # Character segmentation (default)
> nlp = Chinese()
>
> # Jieba
> cfg = {"segmenter": "jieba"}
> nlp = Chinese(meta={"tokenizer": {"config": cfg}})
>
> # PKUSeg with "default" model provided by pkuseg
> cfg = {"segmenter": "pkuseg", "pkuseg_model": "default"}
> nlp = Chinese(meta={"tokenizer": {"config": cfg}})
> ```

1. **Character segmentation:** Character segmentation is the default
   segmentation option. It's enabled when you create a new `Chinese` language
   class or call `spacy.blank("zh")`.
2. **Jieba:** `Chinese` uses [Jieba](https://github.com/fxsjy/jieba) for word
   segmentation with the tokenizer option `{"segmenter": "jieba"}`.
3. **PKUSeg**: As of spaCy v2.3.0, support for
   [PKUSeg](https://github.com/lancopku/PKUSeg-python) has been added to support
   better segmentation for Chinese OntoNotes and the provided
   [Chinese pipelines](/models/zh). Enable PKUSeg with the tokenizer option
   `{"segmenter": "pkuseg"}`.

<Infobox variant="warning">

In spaCy v3.0, the default Chinese word segmenter has switched from Jieba to
character segmentation. Also note that
[`pkuseg`](https://github.com/lancopku/pkuseg-python) doesn't yet ship with
pre-compiled wheels for Python 3.8. If you're running Python 3.8, you can
install it from our fork and compile it locally:

```bash
$ pip install https://github.com/honnibal/pkuseg-python/archive/master.zip
```

</Infobox>

<Accordion title="Details on spaCy's Chinese API">

The `meta` argument of the `Chinese` language class supports the following
following tokenizer config settings:

| Name               | Description                                                                                                     |
| ------------------ | --------------------------------------------------------------------------------------------------------------- |
| `segmenter`        | Word segmenter: `char`, `jieba` or `pkuseg`. Defaults to `char`. ~~str~~                                        |
| `pkuseg_model`     | **Required for `pkuseg`:** Name of a model provided by `pkuseg` or the path to a local model directory. ~~str~~ |
| `pkuseg_user_dict` | Optional path to a file with one word per line which overrides the default `pkuseg` user dictionary. ~~str~~    |

```python
### Examples
# Load "default" model
cfg = {"segmenter": "pkuseg", "pkuseg_model": "default"}
nlp = Chinese(config={"tokenizer": {"config": cfg}})

# Load local model
cfg = {"segmenter": "pkuseg", "pkuseg_model": "/path/to/pkuseg_model"}
nlp = Chinese(config={"tokenizer": {"config": cfg}})

# Override the user directory
cfg = {"segmenter": "pkuseg", "pkuseg_model": "default", "pkuseg_user_dict": "/path"}
nlp = Chinese(config={"tokenizer": {"config": cfg}})
```

You can also modify the user dictionary on-the-fly:

```python
# Append words to user dict
nlp.tokenizer.pkuseg_update_user_dict(["中国", "ABC"])

# Remove all words from user dict and replace with new words
nlp.tokenizer.pkuseg_update_user_dict(["中国"], reset=True)

# Remove all words from user dict
nlp.tokenizer.pkuseg_update_user_dict([], reset=True)
```

</Accordion>

<Accordion title="Details on trained and custom Chinese pipelines" spaced>

The [Chinese pipelines](/models/zh) provided by spaCy include a custom `pkuseg`
model trained only on
[Chinese OntoNotes 5.0](https://catalog.ldc.upenn.edu/LDC2013T19), since the
models provided by `pkuseg` include data restricted to research use. For
research use, `pkuseg` provides models for several different domains
(`"default"`, `"news"` `"web"`, `"medicine"`, `"tourism"`) and for other uses,
`pkuseg` provides a simple
[training API](https://github.com/lancopku/pkuseg-python/blob/master/readme/readme_english.md#usage):

```python
import pkuseg
from spacy.lang.zh import Chinese

# Train pkuseg model
pkuseg.train("train.utf8", "test.utf8", "/path/to/pkuseg_model")
# Load pkuseg model in spaCy Chinese tokenizer
nlp = Chinese(meta={"tokenizer": {"config": {"pkuseg_model": "/path/to/pkuseg_model", "require_pkuseg": True}}})
```

</Accordion>

### Japanese language support {#japanese new=2.3}

> ```python
> from spacy.lang.ja import Japanese
>
> # Load SudachiPy with split mode A (default)
> nlp = Japanese()
>
> # Load SudachiPy with split mode B
> cfg = {"split_mode": "B"}
> nlp = Japanese(meta={"tokenizer": {"config": cfg}})
> ```

The Japanese language class uses
[SudachiPy](https://github.com/WorksApplications/SudachiPy) for word
segmentation and part-of-speech tagging. The default Japanese language class and
the provided Japanese pipelines use SudachiPy split mode `A`. The `meta`
argument of the `Japanese` language class can be used to configure the split
mode to `A`, `B` or `C`.

<Infobox variant="warning">

If you run into errors related to `sudachipy`, which is currently under active
development, we suggest downgrading to `sudachipy==0.4.5`, which is the version
used for training the current [Japanese pipelines](/models/ja).

</Infobox>

## Installing and using trained pipelines {#download}

The easiest way to download a trained pipeline is via spaCy's
[`download`](/api/cli#download) command. It takes care of finding the
best-matching package compatible with your spaCy installation.

> #### Important note for v3.0
>
> Note that as of spaCy v3.0, shortcut links like `en` that create (potentially
> brittle) symlinks in your spaCy installation are **deprecated**. To download
> and load an installed pipeline package, use its full name:
>
> ```diff
> - python -m spacy download en
> + python -m spacy dowmload en_core_web_sm
> ```
>
> ```diff
> - nlp = spacy.load("en")
> + nlp = spacy.load("en_core_web_sm")
> ```

```cli
# Download best-matching version of a package for your spaCy installation
$ python -m spacy download en_core_web_sm

# Download exact package version
$ python -m spacy download en_core_web_sm-3.0.0 --direct
```

The download command will [install the package](/usage/models#download-pip) via
pip and place the package in your `site-packages` directory.

```cli
$ pip install -U spacy
$ python -m spacy download en_core_web_sm
```

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
```

### Installation via pip {#download-pip}

To download a trained pipeline directly using
[pip](https://pypi.python.org/pypi/pip), point `pip install` to the URL or local
path of the archive file. To find the direct link to a package, head over to the
[releases](https://github.com/explosion/spacy-models/releases), right click on
the archive link and copy it to your clipboard.

```bash
# With external URL
$ pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz

# With local file
$ pip install /Users/you/en_core_web_sm-3.0.0.tar.gz
```

By default, this will install the pipeline package into your `site-packages`
directory. You can then use `spacy.load` to load it via its package name or
[import it](#usage-import) explicitly as a module. If you need to download
pipeline packages as part of an automated process, we recommend using pip with a
direct link, instead of relying on spaCy's [`download`](/api/cli#download)
command.

You can also add the direct download link to your application's
`requirements.txt`. For more details, see the section on
[working with pipeline packages in production](#production).

### Manual download and installation {#download-manual}

In some cases, you might prefer downloading the data manually, for example to
place it into a custom directory. You can download the package via your browser
from the [latest releases](https://github.com/explosion/spacy-models/releases),
or configure your own download script using the URL of the archive file. The
archive consists of a package directory that contains another directory with the
pipeline data.

```yaml
### Directory structure {highlight="6"}
└── en_core_web_md-3.0.0.tar.gz       # downloaded archive
    ├── setup.py                      # setup file for pip installation
    ├── meta.json                     # copy of pipeline meta
    └── en_core_web_md                # 📦 pipeline package
        ├── __init__.py               # init for pip installation
        └── en_core_web_md-3.0.0      # pipeline data
            ├── config.cfg            # pipeline config
            ├── meta.json             # pipeline meta
            └── ...                   # directories with component data
```

You can place the **pipeline package directory** anywhere on your local file
system.

### Using trained pipelines with spaCy {#usage}

To load a pipeline package, use [`spacy.load`](/api/top-level#spacy.load) with
the package name or a path to the data directory:

> #### Important note for v3.0
>
> Note that as of spaCy v3.0, shortcut links like `en` that create (potentially
> brittle) symlinks in your spaCy installation are **deprecated**. To download
> and load an installed pipeline package, use its full name:
>
> ```diff
> - python -m spacy download en
> + python -m spacy dowmload en_core_web_sm
> ```

```python
import spacy
nlp = spacy.load("en_core_web_sm")           # load package "en_core_web_sm"
nlp = spacy.load("/path/to/en_core_web_sm")  # load package from a directory

doc = nlp("This is a sentence.")
```

<Infobox title="Tip: Preview model info" emoji="💡">

You can use the [`info`](/api/cli#info) command or
[`spacy.info()`](/api/top-level#spacy.info) method to print a pipeline
packages's meta data before loading it. Each `Language` object with a loaded
pipeline also exposes the pipeline's meta data as the attribute `meta`. For
example, `nlp.meta['version']` will return the package version.

</Infobox>

### Importing pipeline packages as modules {#usage-import}

If you've installed a trained pipeline via [`spacy download`](/api/cli#download)
or directly via pip, you can also `import` it and then call its `load()` method
with no arguments:

```python
### {executable="true"}
import en_core_web_sm

nlp = en_core_web_sm.load()
doc = nlp("This is a sentence.")
```

How you choose to load your trained pipelines ultimately depends on personal
preference. However, **for larger code bases**, we usually recommend native
imports, as this will make it easier to integrate pipeline packages with your
existing build process, continuous integration workflow and testing framework.
It'll also prevent you from ever trying to load a package that is not installed,
as your code will raise an `ImportError` immediately, instead of failing
somewhere down the line when calling `spacy.load()`. For more details, see the
section on [working with pipeline packages in production](#production).

## Using trained pipelines in production {#production}

If your application depends on one or more trained pipeline packages, you'll
usually want to integrate them into your continuous integration workflow and
build process. While spaCy provides a range of useful helpers for downloading
and loading pipeline packages, the underlying functionality is entirely based on
native Python packaging. This allows your application to handle a spaCy pipeline
like any other package dependency.

### Downloading and requiring package dependencies {#models-download}

spaCy's built-in [`download`](/api/cli#download) command is mostly intended as a
convenient, interactive wrapper. It performs compatibility checks and prints
detailed error messages and warnings. However, if you're downloading pipeline
packages as part of an automated build process, this only adds an unnecessary
layer of complexity. If you know which packages your application needs, you
should be specifying them directly.

Because pipeline packages are valid Python packages, you can add them to your
application's `requirements.txt`. If you're running your own internal PyPi
installation, you can upload the pipeline packages there. pip's
[requirements file format](https://pip.pypa.io/en/latest/reference/pip_install/#requirements-file-format)
supports both package names to download via a PyPi server, as well as direct
URLs.

```text
### requirements.txt
spacy>=2.2.0,<3.0.0
https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz#egg=en_core_web_sm
```

Specifying `#egg=` with the package name tells pip which package to expect from
the download URL. This way, the package won't be re-downloaded and overwritten
if it's already installed - just like when you're downloading a package from
PyPi.

All pipeline packages are versioned and specify their spaCy dependency. This
ensures cross-compatibility and lets you specify exact version requirements for
each pipeline. If you've [trained](/usage/training) your own pipeline, you can
use the [`spacy package`](/api/cli#package) command to generate the required
meta data and turn it into a loadable package.

### Loading and testing pipeline packages {#models-loading}

Pipeline packages are regular Python packages, so you can also import them as a
package using Python's native `import` syntax, and then call the `load` method
to load the data and return an `nlp` object:

```python
import en_core_web_sm
nlp = en_core_web_sm.load()
```

In general, this approach is recommended for larger code bases, as it's more
"native", and doesn't rely on spaCy's loader to resolve string names to
packages. If a package can't be imported, Python will raise an `ImportError`
immediately. And if a package is imported but not used, any linter will catch
that.

Similarly, it'll give you more flexibility when writing tests that require
loading pipelines. For example, instead of writing your own `try` and `except`
logic around spaCy's loader, you can use
[pytest](http://pytest.readthedocs.io/en/latest/)'s
[`importorskip()`](https://docs.pytest.org/en/latest/builtin.html#_pytest.outcomes.importorskip)
method to only run a test if a specific pipeline package or version is
installed. Each pipeline package package exposes a `__version__` attribute which
you can also use to perform your own version compatibility checks before loading
it.
