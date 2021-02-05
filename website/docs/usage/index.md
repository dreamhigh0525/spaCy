---
title: Install spaCy
next: /usage/models
menu:
  - ['Quickstart', 'quickstart']
  - ['Instructions', 'installation']
  - ['Troubleshooting', 'troubleshooting']
  - ['Changelog', 'changelog']
---

## Quickstart {hidden="true"}

> #### 📖 Looking for the old docs?
>
> To help you make the transition from v2.x to v3.0, we've uploaded the old
> website to [**v2.spacy.io**](https://v2.spacy.io/docs). To see what's changed
> and how to migrate, see the [v3.0 guide](/usage/v3).

import QuickstartInstall from 'widgets/quickstart-install.js'

<QuickstartInstall id="quickstart" />

## Installation instructions {#installation}

spaCy is compatible with **64-bit CPython 3.6+** and runs on **Unix/Linux**,
**macOS/OS X** and **Windows**. The latest spaCy releases are available over
[pip](https://pypi.python.org/pypi/spacy) and
[conda](https://anaconda.org/conda-forge/spacy).

### pip {#pip}

Using pip, spaCy releases are available as source packages and binary wheels.
Before you install spaCy and its dependencies, make sure that your `pip`,
`setuptools` and `wheel` are up to date.

> #### Download pipelines
>
> After installation you typically want to download a trained pipeline. For more
> info and available packages, see the [models directory](/models).
>
> ```cli
> $ python -m spacy download en_core_web_sm
>
> >>> import spacy
> >>> nlp = spacy.load("en_core_web_sm")
> ```

```bash
$ pip install -U pip setuptools wheel
$ pip install -U %%SPACY_PKG_NAME%%SPACY_PKG_FLAGS
```

When using pip it is generally recommended to install packages in a virtual
environment to avoid modifying system state:

```bash
$ python -m venv .env
$ source .env/bin/activate
$ pip install -U pip setuptools wheel
$ pip install -U %%SPACY_PKG_NAME%%SPACY_PKG_FLAGS
```

spaCy also lets you install extra dependencies by specifying the following
keywords in brackets, e.g. `spacy[ja]` or `spacy[lookups,transformers]` (with
multiple comma-separated extras). See the `[options.extras_require]` section in
spaCy's [`setup.cfg`](%%GITHUB_SPACY/setup.cfg) for details on what's included.

> #### Example
>
> ```bash
> $ pip install %%SPACY_PKG_NAME[lookups,transformers]%%SPACY_PKG_FLAGS
> ```

| Name                   | Description                                                                                                                                                                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lookups`              | Install [`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data) for data tables for lemmatization and lexeme normalization. The data is serialized with trained pipelines, so you only need this package if you want to train your own models. |
| `transformers`         | Install [`spacy-transformers`](https://github.com/explosion/spacy-transformers). The package will be installed automatically when you install a transformer-based pipeline.                                                                                    |
| `ray`                  | Install [`spacy-ray`](https://github.com/explosion/spacy-ray) to add CLI commands for [parallel training](/usage/training#parallel-training).                                                                                                                  |
| `cuda`, ...            | Install spaCy with GPU support provided by [CuPy](https://cupy.chainer.org) for your given CUDA version. See the GPU [installation instructions](#gpu) for details and options.                                                                                |
| `ja`, `ko`, `th`, `zh` | Install additional dependencies required for tokenization for the [languages](/usage/models#languages).                                                                                                                                                        |

### conda {#conda}

Thanks to our great community, we've been able to re-add conda support. You can
also install spaCy via `conda-forge`:

```bash
$ conda install -c conda-forge spacy
```

For the feedstock including the build recipe and configuration, check out
[this repository](https://github.com/conda-forge/spacy-feedstock). Note that we
currently don't publish any [pre-releases](#changelog-pre) on conda.

### Upgrading spaCy {#upgrading}

> #### Upgrading from v2 to v3
>
> Although we've tried to keep breaking changes to a minimum, upgrading from
> spaCy v2.x to v3.x may still require some changes to your code base. For
> details see the sections on [backwards incompatibilities](/usage/v3#incompat)
> and [migrating](/usage/v3#migrating). Also remember to download the new
> trained pipelines, and retrain your own pipelines.

When updating to a newer version of spaCy, it's generally recommended to start
with a clean virtual environment. If you're upgrading to a new major version,
make sure you have the latest **compatible trained pipelines** installed, and
that there are no old and incompatible packages left over in your environment,
as this can often lead to unexpected results and errors. If you've trained your
own models, keep in mind that your train and runtime inputs must match. This
means you'll have to **retrain your pipelines** with the new version.

spaCy also provides a [`validate`](/api/cli#validate) command, which lets you
verify that all installed pipeline packages are compatible with your spaCy
version. If incompatible packages are found, tips and installation instructions
are printed. It's recommended to run the command with `python -m` to make sure
you're executing the correct version of spaCy.

```cli
$ pip install -U %%SPACY_PKG_NAME%%SPACY_PKG_FLAGS
$ python -m spacy validate
```

### Run spaCy with GPU {#gpu new="2.0.14"}

As of v2.0, spaCy comes with neural network models that are implemented in our
machine learning library, [Thinc](https://thinc.ai). For GPU support, we've been
grateful to use the work of Chainer's [CuPy](https://cupy.chainer.org) module,
which provides a numpy-compatible interface for GPU arrays.

spaCy can be installed on GPU by specifying `spacy[cuda]`, `spacy[cuda90]`,
`spacy[cuda91]`, `spacy[cuda92]`, `spacy[cuda100]`, `spacy[cuda101]`,
`spacy[cuda102]`, `spacy[cuda110]` or `spacy[cuda111]`. If you know your cuda
version, using the more explicit specifier allows cupy to be installed via
wheel, saving some compilation time. The specifiers should install
[`cupy`](https://cupy.chainer.org).

```bash
$ pip install -U %%SPACY_PKG_NAME[cuda92]%%SPACY_PKG_FLAGS
```

Once you have a GPU-enabled installation, the best way to activate it is to call
[`spacy.prefer_gpu`](/api/top-level#spacy.prefer_gpu) or
[`spacy.require_gpu()`](/api/top-level#spacy.require_gpu) somewhere in your
script before any pipelines have been loaded. `require_gpu` will raise an error
if no GPU is available.

```python
import spacy

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")
```

### Compile from source {#source}

The other way to install spaCy is to clone its
[GitHub repository](https://github.com/explosion/spaCy) and build it from
source. That is the common way if you want to make changes to the code base.
You'll need to make sure that you have a development environment consisting of a
Python distribution including header files, a compiler,
[pip](https://pip.pypa.io/en/stable/) and [git](https://git-scm.com) installed.
The compiler part is the trickiest. How to do that depends on your system. See
notes on [Ubuntu](#source-ubuntu), [macOS / OS X](#source-osx) and
[Windows](#source-windows) for details.

```bash
$ python -m pip install -U pip setuptools wheel # install/update build tools
$ git clone https://github.com/explosion/spaCy  # clone spaCy
$ cd spaCy                                      # navigate into dir
$ python -m venv .env                           # create environment in .env
$ source .env/bin/activate                      # activate virtual env
$ pip install -r requirements.txt               # install requirements
$ pip install --no-build-isolation --editable . # compile and install spaCy
```

To install with extras:

```bash
$ pip install --no-build-isolation --editable .[lookups,cuda102]
```

How to install compilers and related build tools:

<a id="source-ubuntu"></a><a id="source-osx"></a><a id="source-windows"></a>

- **Ubuntu:** Install system-level dependencies via `apt-get`:
  `sudo apt-get install build-essential python-dev git`
- **macOS / OS X:** Install a recent version of
  [XCode](https://developer.apple.com/xcode/), including the so-called "Command
  Line Tools". macOS and OS X ship with Python and Git preinstalled.
- **Windows:** Install a version of the
  [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  or
  [Visual Studio Express](https://www.visualstudio.com/vs/visual-studio-express/)
  that matches the version that was used to compile your Python interpreter.

#### Additional options for developers {#source-developers}

Some additional options may be useful for spaCy developers who are editing the
source code and recompiling frequently.

- Install in editable mode. Changes to `.py` files will be reflected as soon as
  the files are saved, but edits to Cython files (`.pxd`, `.pyx`) will require
  the `pip install` or `python setup.py build_ext` command below to be run
  again. Before installing in editable mode, be sure you have removed any
  previous installs with `pip uninstall spacy`, which you may need to run
  multiple times to remove all traces of earlier installs.

  ```bash
  $ pip install -r requirements.txt
  $ pip install --no-build-isolation --editable .
  ```

- Build in parallel using `N` CPUs to speed up compilation and then install in
  editable mode:

  ```bash
  $ pip install -r requirements.txt
  $ python setup.py build_ext --inplace -j N
  $ python setup.py develop
  ```

### Building an executable {#executable}

The spaCy repository includes a [`Makefile`](%%GITHUB_SPACY/Makefile) that
builds an executable zip file using [`pex`](https://github.com/pantsbuild/pex)
(**P**ython **Ex**ecutable). The executable includes spaCy and all its package
dependencies and only requires the system Python at runtime. Building an
executable `.pex` file is often the most convenient way to deploy spaCy, as it
lets you separate the build from the deployment process.

> #### Usage
>
> To use a `.pex` file, just replace `python` with the path to the file when you
> execute your code or CLI commands. This is equivalent to running Python in a
> virtual environment with spaCy installed.
>
> ```bash
> $ ./spacy.pex my_script.py
> $ ./spacy.pex -m spacy info
> ```

```bash
$ git clone https://github.com/explosion/spaCy
$ cd spaCy
$ make
```

You can configure the build process with the following environment variables:

| Variable       | Description                                                                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SPACY_EXTRAS` | Additional Python packages to install alongside spaCy with optional version specifications. Should be a string that can be passed to `pip install`. See [`Makefile`](%%GITHUB_SPACY/Makefile) for defaults. |
| `PYVER`        | The Python version to build against. This version needs to be available on your build and runtime machines. Defaults to `3.6`.                                                                              |
| `WHEELHOUSE`   | Directory to store the wheel files during compilation. Defaults to `./wheelhouse`.                                                                                                                          |

### Run tests {#run-tests}

spaCy comes with an [extensive test suite](%%GITHUB_SPACY/spacy/tests). In order
to run the tests, you'll usually want to clone the [repository](%%GITHUB_SPACY)
and [build spaCy from source](#source). This will also install the required
development dependencies and test utilities defined in the `requirements.txt`.

Alternatively, you can find out where spaCy is installed and run `pytest` on
that directory. Don't forget to also install the test utilities via spaCy's
[`requirements.txt`](%%GITHUB_SPACY/requirements.txt):

```bash
$ python -c "import os; import spacy; print(os.path.dirname(spacy.__file__))"
$ pip install -r path/to/requirements.txt
$ python -m pytest --pyargs %%SPACY_PKG_NAME
```

Calling `pytest` on the spaCy directory will run only the basic tests. The flag
`--slow` is optional and enables additional tests that take longer.

```bash
$ python -m pip install -U pytest               # update pytest
$ python -m pytest --pyargs %%SPACY_PKG_NAME               # basic tests
$ python -m pytest --pyargs %%SPACY_PKG_NAME --slow        # basic and slow tests
```

## Troubleshooting guide {#troubleshooting}

This section collects some of the most common errors you may come across when
installing, loading and using spaCy, as well as their solutions.

> #### Help us improve this guide
>
> Did you come across a problem like the ones listed here and want to share the
> solution? You can find the "Suggest edits" button at the bottom of this page
> that points you to the source. We always appreciate
> [pull requests](https://github.com/explosion/spaCy/pulls)!

<Accordion title="No compatible model found" id="compatible-model">

```
No compatible package found for [lang] (spaCy vX.X.X).
```

This usually means that the trained pipeline you're trying to download does not
exist, or isn't available for your version of spaCy. Check the
[compatibility table](https://github.com/explosion/spacy-models/tree/master/compatibility.json)
to see which packages are available for your spaCy version. If you're using an
old version, consider upgrading to the latest release. Note that while spaCy
supports tokenization for [a variety of languages](/usage/models#languages), not
all of them come with trained pipelines. To only use the tokenizer, import the
language's `Language` class instead, for example
`from spacy.lang.fr import French`.

</Accordion>

<Accordion title="No such option: --no-cache-dir" id="no-cache-dir">

```
no such option: --no-cache-dir
```

The `download` command uses pip to install the pipeline packages and sets the
`--no-cache-dir` flag to prevent it from requiring too much memory.
[This setting](https://pip.pypa.io/en/stable/reference/pip_install/#caching)
requires pip v6.0 or newer. Run `pip install -U pip` to upgrade to the latest
version of pip. To see which version you have installed, run `pip --version`.

</Accordion>

<Accordion title="sre_constants.error: bad character range" id="narrow-unicode">

```
sre_constants.error: bad character range
```

In [v2.1](/usage/v2-1), spaCy changed its implementation of regular expressions
for tokenization to make it up to 2-3 times faster. But this also means that
it's very important now that you run spaCy with a wide unicode build of Python.
This means that the build has 1114111 unicode characters available, instead of
only 65535 in a narrow unicode build. You can check this by running the
following command:

```bash
$ python -c "import sys; print(sys.maxunicode)"
```

If you're running a narrow unicode build, reinstall Python and use a wide
unicode build instead. You can also rebuild Python and set the
`--enable-unicode=ucs4` flag.

</Accordion>

<Accordion title="Unknown locale: UTF-8" id="unknown-locale">

```
ValueError: unknown locale: UTF-8
```

This error can sometimes occur on OSX and is likely related to a still
unresolved [Python bug](https://bugs.python.org/issue18378). However, it's easy
to fix: just add the following to your `~/.bash_profile` or `~/.zshrc` and then
run `source ~/.bash_profile` or `source ~/.zshrc`. Make sure to add **both
lines** for `LC_ALL` and `LANG`.

```bash
$ export LC_ALL=en_US.UTF-8
$ export LANG=en_US.UTF-8
```

</Accordion>

<Accordion title="Import error: No module named spacy" id="import-error">

```
Import Error: No module named spacy
```

This error means that the spaCy module can't be located on your system, or in
your environment. Make sure you have spaCy installed. If you're using a virtual
environment, make sure it's activated and check that spaCy is installed in that
environment – otherwise, you're trying to load a system installation. You can
also run `which python` to find out where your Python executable is located.

</Accordion>

<Accordion title="Import error: No module named [name]" id="import-error-models">

```
ImportError: No module named 'en_core_web_sm'
```

As of spaCy v1.7, all trained pipelines can be installed as Python packages.
This means that they'll become importable modules of your application. If this
fails, it's usually a sign that the package is not installed in the current
environment. Run `pip list` or `pip freeze` to check which pipeline packages you
have installed, and install the [correct package](/models) if necessary. If
you're importing a package manually at the top of a file, make sure to use the
full name of the package.

</Accordion>

<Accordion title="Command not found: spacy" id="command-not-found">

```
command not found: spacy
```

This error may occur when running the `spacy` command from the command line.
spaCy does not currently add an entry to your `PATH` environment variable, as
this can lead to unexpected results, especially when using a virtual
environment. Instead, spaCy adds an auto-alias that maps `spacy` to
`python -m spacy`. If this is not working as expected, run the command with
`python -m`, yourself – for example `python -m spacy download en_core_web_sm`.
For more info on this, see the [`download`](/api/cli#download) command.

</Accordion>

<Accordion title="'module' object has no attribute 'load'" id="module-load">

```
AttributeError: 'module' object has no attribute 'load'
```

While this could technically have many causes, including spaCy being broken, the
most likely one is that your script's file or directory name is "shadowing" the
module – e.g. your file is called `spacy.py`, or a directory you're importing
from is called `spacy`. So, when using spaCy, never call anything else `spacy`.

</Accordion>

<Accordion title="NER model doesn't recognize other entities anymore after training" id="catastrophic-forgetting">

If your training data only contained new entities and you didn't mix in any
examples the model previously recognized, it can cause the model to "forget"
what it had previously learned. This is also referred to as the "catastrophic
forgetting problem". A solution is to pre-label some text, and mix it with the
new text in your updates. You can also do this by running spaCy over some text,
extracting a bunch of entities the model previously recognized correctly, and
adding them to your training examples.

</Accordion>

<Accordion title="Unhashable type: 'list'" id="unhashable-list">

```
TypeError: unhashable type: 'list'
```

If you're training models, writing them to disk, and versioning them with git,
you might encounter this error when trying to load them in a Windows
environment. This happens because a default install of Git for Windows is
configured to automatically convert Unix-style end-of-line characters (LF) to
Windows-style ones (CRLF) during file checkout (and the reverse when
committing). While that's mostly fine for text files, a trained model written to
disk has some binary files that should not go through this conversion. When they
do, you get the error above. You can fix it by either changing your
[`core.autocrlf`](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
setting to `"false"`, or by committing a
[`.gitattributes`](https://git-scm.com/docs/gitattributes) file to your
repository to tell Git on which files or folders it shouldn't do LF-to-CRLF
conversion, with an entry like `path/to/spacy/model/** -text`. After you've done
either of these, clone your repository again.

</Accordion>

## Changelog {#changelog}

import Changelog from 'widgets/changelog.js'

<Changelog />
