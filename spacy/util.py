from typing import List, Union, Dict, Any, Optional, Iterable, Callable, Tuple
from typing import Iterator, Type, Pattern, Sequence, TYPE_CHECKING
from types import ModuleType
import os
import importlib
import importlib.util
import re
from pathlib import Path
import thinc
from thinc.api import NumpyOps, get_current_ops, Adam, Config, Optimizer
import functools
import itertools
import numpy.random
import numpy
import srsly
import catalogue
import sys
import warnings
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.version import Version, InvalidVersion
import subprocess
from contextlib import contextmanager
import tempfile
import shutil
import shlex
import inspect

try:
    import cupy.random
except ImportError:
    cupy = None

try:  # Python 3.8
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

# These are functions that were previously (v2.x) available from spacy.util
# and have since moved to Thinc. We're importing them here so people's code
# doesn't break, but they should always be imported from Thinc from now on,
# not from spacy.util.
from thinc.api import fix_random_seed, compounding, decaying  # noqa: F401


from .symbols import ORTH
from .compat import cupy, CudaStream, is_windows
from .errors import Errors, Warnings
from . import about

if TYPE_CHECKING:
    # This lets us add type hints for mypy etc. without causing circular imports
    from .language import Language  # noqa: F401
    from .tokens import Doc, Span  # noqa: F401
    from .vocab import Vocab  # noqa: F401


_PRINT_ENV = False
OOV_RANK = numpy.iinfo(numpy.uint64).max
LEXEME_NORM_LANGS = ["da", "de", "el", "en", "id", "lb", "pt", "ru", "sr", "ta", "th"]


class registry(thinc.registry):
    languages = catalogue.create("spacy", "languages", entry_points=True)
    architectures = catalogue.create("spacy", "architectures", entry_points=True)
    tokenizers = catalogue.create("spacy", "tokenizers", entry_points=True)
    lemmatizers = catalogue.create("spacy", "lemmatizers", entry_points=True)
    lookups = catalogue.create("spacy", "lookups", entry_points=True)
    displacy_colors = catalogue.create("spacy", "displacy_colors", entry_points=True)
    assets = catalogue.create("spacy", "assets", entry_points=True)
    # These are factories registered via third-party packages and the
    # spacy_factories entry point. This registry only exists so we can easily
    # load them via the entry points. The "true" factories are added via the
    # Language.factory decorator (in the spaCy code base and user code) and those
    # are the factories used to initialize components via registry.make_from_config.
    _entry_point_factories = catalogue.create("spacy", "factories", entry_points=True)
    factories = catalogue.create("spacy", "internal_factories")
    # This is mostly used to get a list of all installed models in the current
    # environment. spaCy models packaged with `spacy package` will "advertise"
    # themselves via entry points.
    models = catalogue.create("spacy", "models", entry_points=True)


class SimpleFrozenDict(dict):
    """Simplified implementation of a frozen dict, mainly used as default
    function or method argument (for arguments that should default to empty
    dictionary). Will raise an error if user or spaCy attempts to add to dict.
    """

    def __init__(self, *args, error: str = Errors.E095, **kwargs) -> None:
        """Initialize the frozen dict. Can be initialized with pre-defined
        values.

        error (str): The error message when user tries to assign to dict.
        """
        super().__init__(*args, **kwargs)
        self.error = error

    def __setitem__(self, key, value):
        raise NotImplementedError(self.error)

    def pop(self, key, default=None):
        raise NotImplementedError(self.error)

    def update(self, other):
        raise NotImplementedError(self.error)


def set_env_log(value: bool) -> None:
    global _PRINT_ENV
    _PRINT_ENV = value


def lang_class_is_loaded(lang: str) -> bool:
    """Check whether a Language class is already loaded. Language classes are
    loaded lazily, to avoid expensive setup code associated with the language
    data.

    lang (str): Two-letter language code, e.g. 'en'.
    RETURNS (bool): Whether a Language class has been loaded.
    """
    return lang in registry.languages


def get_lang_class(lang: str) -> "Language":
    """Import and load a Language class.

    lang (str): Two-letter language code, e.g. 'en'.
    RETURNS (Language): Language class.
    """
    # Check if language is registered / entry point is available
    if lang in registry.languages:
        return registry.languages.get(lang)
    else:
        try:
            module = importlib.import_module(f".lang.{lang}", "spacy")
        except ImportError as err:
            raise ImportError(Errors.E048.format(lang=lang, err=err))
        set_lang_class(lang, getattr(module, module.__all__[0]))
    return registry.languages.get(lang)


def set_lang_class(name: str, cls: Type["Language"]) -> None:
    """Set a custom Language class name that can be loaded via get_lang_class.

    name (str): Name of Language class.
    cls (Language): Language class.
    """
    registry.languages.register(name, func=cls)


def ensure_path(path: Any) -> Any:
    """Ensure string is converted to a Path.

    path (Any): Anything. If string, it's converted to Path.
    RETURNS: Path or original argument.
    """
    if isinstance(path, str):
        return Path(path)
    else:
        return path


def load_language_data(path: Union[str, Path]) -> Union[dict, list]:
    """Load JSON language data using the given path as a base. If the provided
    path isn't present, will attempt to load a gzipped version before giving up.

    path (str / Path): The data to load.
    RETURNS: The loaded data.
    """
    path = ensure_path(path)
    if path.exists():
        return srsly.read_json(path)
    path = path.with_suffix(path.suffix + ".gz")
    if path.exists():
        return srsly.read_gzip_json(path)
    raise ValueError(Errors.E160.format(path=path))


def get_module_path(module: ModuleType) -> Path:
    """Get the path of a Python module.

    module (ModuleType): The Python module.
    RETURNS (Path): The path.
    """
    if not hasattr(module, "__module__"):
        raise ValueError(Errors.E169.format(module=repr(module)))
    return Path(sys.modules[module.__module__].__file__).parent


def load_model(
    name: Union[str, Path],
    disable: Iterable[str] = tuple(),
    component_cfg: Dict[str, Dict[str, Any]] = SimpleFrozenDict(),
) -> "Language":
    """Load a model from a package or data path.

    name (str): Package name or model path.
    disable (Iterable[str]): Names of pipeline components to disable.
    component_cfg (Dict[str, dict]): Config overrides for pipeline components,
        keyed by component names.
    RETURNS (Language): The loaded nlp object.
    """
    cfg = component_cfg
    if isinstance(name, str):  # name or string path
        if name.startswith("blank:"):  # shortcut for blank model
            return get_lang_class(name.replace("blank:", ""))()
        if is_package(name):  # installed as package
            return load_model_from_package(name, disable=disable, component_cfg=cfg)
        if Path(name).exists():  # path to model data directory
            return load_model_from_path(Path(name), disable=disable, component_cfg=cfg)
    elif hasattr(name, "exists"):  # Path or Path-like to model data
        return load_model_from_path(name, disable=disable, component_cfg=cfg)
    raise IOError(Errors.E050.format(name=name))


def load_model_from_package(
    name: str,
    disable: Iterable[str] = tuple(),
    component_cfg: Dict[str, Dict[str, Any]] = SimpleFrozenDict(),
) -> "Language":
    """Load a model from an installed package."""
    cls = importlib.import_module(name)
    return cls.load(disable=disable, component_cfg=component_cfg)


def load_model_from_path(
    model_path: Union[str, Path],
    meta: Optional[Dict[str, Any]] = None,
    disable: Iterable[str] = tuple(),
    component_cfg: Dict[str, Dict[str, Any]] = SimpleFrozenDict(),
) -> "Language":
    """Load a model from a data directory path. Creates Language class with
    pipeline from config.cfg and then calls from_disk() with path."""
    if not model_path.exists():
        raise IOError(Errors.E052.format(path=model_path))
    if not meta:
        meta = get_model_meta(model_path)
    config_path = model_path / "config.cfg"
    if not config_path.exists() or not config_path.is_file():
        raise IOError(Errors.E053.format(path=config_path, name="config.cfg"))
    config = Config().from_disk(config_path)
    override_cfg = {"components": {p: dict_to_dot(c) for p, c in component_cfg.items()}}
    overrides = dict_to_dot(override_cfg)
    nlp, _ = load_model_from_config(config, disable=disable, overrides=overrides)
    return nlp.from_disk(model_path, exclude=disable)


def load_model_from_config(
    config: Union[Dict[str, Any], Config],
    disable: Iterable[str] = tuple(),
    overrides: Dict[str, Any] = {},
    auto_fill: bool = False,
    validate: bool = True,
) -> Tuple["Language", Config]:
    """Create an nlp object from a config. Expects the full config file including
    a section "nlp" containing the settings for the nlp object.
    """
    if "nlp" not in config:
        raise ValueError(Errors.E985.format(config=config))
    nlp_config = config["nlp"]
    if "lang" not in nlp_config or nlp_config["lang"] is None:
        raise ValueError(Errors.E993.format(config=nlp_config))
    # This will automatically handle all codes registered via the languages
    # registry, including custom subclasses provided via entry points
    lang_cls = get_lang_class(nlp_config["lang"])
    nlp = lang_cls.from_config(
        config,
        disable=disable,
        overrides=overrides,
        auto_fill=auto_fill,
        validate=validate,
    )
    return nlp, nlp.resolved


def load_model_from_init_py(
    init_file: Union[Path, str],
    disable: Iterable[str] = tuple(),
    component_cfg: Dict[str, Dict[str, Any]] = SimpleFrozenDict(),
) -> "Language":
    """Helper function to use in the `load()` method of a model package's
    __init__.py.

    init_file (str): Path to model's __init__.py, i.e. `__file__`.
    **overrides: Specific overrides, like pipeline components to disable.
    RETURNS (Language): `Language` class with loaded model.
    """
    model_path = Path(init_file).parent
    meta = get_model_meta(model_path)
    data_dir = f"{meta['lang']}_{meta['name']}-{meta['version']}"
    data_path = model_path / data_dir
    if not model_path.exists():
        raise IOError(Errors.E052.format(path=data_path))
    return load_model_from_path(
        data_path, meta, disable=disable, component_cfg=component_cfg
    )


def get_installed_models() -> List[str]:
    """List all model packages currently installed in the environment.

    RETURNS (List[str]): The string names of the models.
    """
    return list(registry.models.get_all().keys())


def get_package_version(name: str) -> Optional[str]:
    """Get the version of an installed package. Typically used to get model
    package versions.

    name (str): The name of the installed Python package.
    RETURNS (str / None): The version or None if package not installed.
    """
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def is_compatible_version(
    version: str, constraint: str, prereleases: bool = True
) -> Optional[bool]:
    """Check if a version (e.g. "2.0.0") is compatible given a version
    constraint (e.g. ">=1.9.0,<2.2.1"). If the constraint is a specific version,
    it's interpreted as =={version}.

    version (str): The version to check.
    constraint (str): The constraint string.
    prereleases (bool): Whether to allow prereleases. If set to False,
        prerelease versions will be considered incompatible.
    RETURNS (bool / None): Whether the version is compatible, or None if the
        version or constraint are invalid.
    """
    # Handle cases where exact version is provided as constraint
    if constraint[0].isdigit():
        constraint = f"=={constraint}"
    try:
        spec = SpecifierSet(constraint)
        version = Version(version)
    except (InvalidSpecifier, InvalidVersion):
        return None
    spec.prereleases = prereleases
    return version in spec


def is_unconstrained_version(
    constraint: str, prereleases: bool = True
) -> Optional[bool]:
    # We have an exact version, this is the ultimate constrained version
    if constraint[0].isdigit():
        return False
    try:
        spec = SpecifierSet(constraint)
    except InvalidSpecifier:
        return None
    spec.prereleases = prereleases
    specs = [sp for sp in spec]
    # We only have one version spec and it defines > or >=
    if len(specs) == 1 and specs[0].operator in (">", ">="):
        return True
    # One specifier is exact version
    if any(sp.operator in ("==") for sp in specs):
        return False
    has_upper = any(sp.operator in ("<", "<=") for sp in specs)
    has_lower = any(sp.operator in (">", ">=") for sp in specs)
    # We have a version spec that defines an upper and lower bound
    if has_upper and has_lower:
        return False
    # Everything else, like only an upper version, only a lower version etc.
    return True


def get_model_version_range(spacy_version: str) -> str:
    """Generate a version range like >=1.2.3,<1.3.0 based on a given spaCy
    version. Models are always compatible across patch versions but not
    across minor or major versions.
    """
    release = Version(spacy_version).release
    return f">={spacy_version},<{release[0]}.{release[1] + 1}.0"


def get_base_version(version: str) -> str:
    """Generate the base version without any prerelease identifiers.

    version (str): The version, e.g. "3.0.0.dev1".
    RETURNS (str): The base version, e.g. "3.0.0".
    """
    return Version(version).base_version


def get_model_meta(path: Union[str, Path]) -> Dict[str, Any]:
    """Get model meta.json from a directory path and validate its contents.

    path (str / Path): Path to model directory.
    RETURNS (Dict[str, Any]): The model's meta data.
    """
    model_path = ensure_path(path)
    if not model_path.exists():
        raise IOError(Errors.E052.format(path=model_path))
    meta_path = model_path / "meta.json"
    if not meta_path.is_file():
        raise IOError(Errors.E053.format(path=meta_path, name="meta.json"))
    meta = srsly.read_json(meta_path)
    for setting in ["lang", "name", "version"]:
        if setting not in meta or not meta[setting]:
            raise ValueError(Errors.E054.format(setting=setting))
    if "spacy_version" in meta:
        if not is_compatible_version(about.__version__, meta["spacy_version"]):
            warn_msg = Warnings.W095.format(
                model=f"{meta['lang']}_{meta['name']}",
                model_version=meta["version"],
                version=meta["spacy_version"],
                current=about.__version__,
            )
            warnings.warn(warn_msg)
        if is_unconstrained_version(meta["spacy_version"]):
            warn_msg = Warnings.W094.format(
                model=f"{meta['lang']}_{meta['name']}",
                model_version=meta["version"],
                version=meta["spacy_version"],
                example=get_model_version_range(about.__version__),
            )
            warnings.warn(warn_msg)
    return meta


def is_package(name: str) -> bool:
    """Check if string maps to a package installed via pip.

    name (str): Name of package.
    RETURNS (bool): True if installed package, False if not.
    """
    try:
        importlib_metadata.distribution(name)
        return True
    except:  # noqa: E722
        return False


def get_package_path(name: str) -> Path:
    """Get the path to an installed package.

    name (str): Package name.
    RETURNS (Path): Path to installed package.
    """
    name = name.lower()  # use lowercase version to be safe
    # Here we're importing the module just to find it. This is worryingly
    # indirect, but it's otherwise very difficult to find the package.
    pkg = importlib.import_module(name)
    return Path(pkg.__file__).parent


def split_command(command: str) -> List[str]:
    """Split a string command using shlex. Handles platform compatibility.

    command (str) : The command to split
    RETURNS (List[str]): The split command.
    """
    return shlex.split(command, posix=not is_windows)


def join_command(command: List[str]) -> str:
    """Join a command using shlex. shlex.join is only available for Python 3.8+,
    so we're using a workaround here.

    command (List[str]): The command to join.
    RETURNS (str): The joined command
    """
    return " ".join(shlex.quote(cmd) for cmd in command)


def run_command(command: Union[str, List[str]]) -> None:
    """Run a command on the command line as a subprocess. If the subprocess
    returns a non-zero exit code, a system exit is performed.

    command (str / List[str]): The command. If provided as a string, the
        string will be split using shlex.split.
    """
    if isinstance(command, str):
        command = split_command(command)
    try:
        status = subprocess.call(command, env=os.environ.copy())
    except FileNotFoundError:
        raise FileNotFoundError(
            Errors.E970.format(str_command=" ".join(command), tool=command[0])
        )
    if status != 0:
        sys.exit(status)


@contextmanager
def working_dir(path: Union[str, Path]) -> None:
    """Change current working directory and returns to previous on exit.

    path (str / Path): The directory to navigate to.
    YIELDS (Path): The absolute path to the current working directory. This
        should be used if the block needs to perform actions within the working
        directory, to prevent mismatches with relative paths.
    """
    prev_cwd = Path.cwd()
    current = Path(path).resolve()
    os.chdir(str(current))
    try:
        yield current
    finally:
        os.chdir(str(prev_cwd))


@contextmanager
def make_tempdir() -> None:
    """Execute a block in a temporary directory and remove the directory and
    its contents at the end of the with block.

    YIELDS (Path): The path of the temp directory.
    """
    d = Path(tempfile.mkdtemp())
    yield d
    try:
        shutil.rmtree(str(d))
    except PermissionError as e:
        warnings.warn(Warnings.W091.format(dir=d, msg=e))


def is_cwd(path: Union[Path, str]) -> bool:
    """Check whether a path is the current working directory.

    path (Union[Path, str]): The directory path.
    RETURNS (bool): Whether the path is the current working directory.
    """
    return str(Path(path).resolve()).lower() == str(Path.cwd().resolve()).lower()


def is_in_jupyter() -> bool:
    """Check if user is running spaCy from a Jupyter notebook by detecting the
    IPython kernel. Mainly used for the displaCy visualizer.
    RETURNS (bool): True if in Jupyter, False if not.
    """
    # https://stackoverflow.com/a/39662359/6400719
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
    except NameError:
        return False  # Probably standard Python interpreter
    return False


def get_object_name(obj: Any) -> str:
    """Get a human-readable name of a Python object, e.g. a pipeline component.

    obj (Any): The Python object, typically a function or class.
    RETURNS (str): A human-readable name.
    """
    if hasattr(obj, "name"):
        return obj.name
    if hasattr(obj, "__name__"):
        return obj.__name__
    if hasattr(obj, "__class__") and hasattr(obj.__class__, "__name__"):
        return obj.__class__.__name__
    return repr(obj)


def get_cuda_stream(
    require: bool = False, non_blocking: bool = True
) -> Optional[CudaStream]:
    ops = get_current_ops()
    if CudaStream is None:
        return None
    elif isinstance(ops, NumpyOps):
        return None
    else:
        return CudaStream(non_blocking=non_blocking)


def get_async(stream, numpy_array):
    if cupy is None:
        return numpy_array
    else:
        array = cupy.ndarray(numpy_array.shape, order="C", dtype=numpy_array.dtype)
        array.set(numpy_array, stream=stream)
        return array


def env_opt(name: str, default: Optional[Any] = None) -> Optional[Any]:
    if type(default) is float:
        type_convert = float
    else:
        type_convert = int
    if "SPACY_" + name.upper() in os.environ:
        value = type_convert(os.environ["SPACY_" + name.upper()])
        if _PRINT_ENV:
            print(name, "=", repr(value), "via", "$SPACY_" + name.upper())
        return value
    elif name in os.environ:
        value = type_convert(os.environ[name])
        if _PRINT_ENV:
            print(name, "=", repr(value), "via", "$" + name)
        return value
    else:
        if _PRINT_ENV:
            print(name, "=", repr(default), "by default")
        return default


def read_regex(path: Union[str, Path]) -> Pattern:
    path = ensure_path(path)
    with path.open(encoding="utf8") as file_:
        entries = file_.read().split("\n")
    expression = "|".join(
        ["^" + re.escape(piece) for piece in entries if piece.strip()]
    )
    return re.compile(expression)


def compile_prefix_regex(entries: Iterable[Union[str, Pattern]]) -> Pattern:
    """Compile a sequence of prefix rules into a regex object.

    entries (Iterable[Union[str, Pattern]]): The prefix rules, e.g.
        spacy.lang.punctuation.TOKENIZER_PREFIXES.
    RETURNS (Pattern): The regex object. to be used for Tokenizer.prefix_search.
    """
    expression = "|".join(["^" + piece for piece in entries if piece.strip()])
    return re.compile(expression)


def compile_suffix_regex(entries: Iterable[Union[str, Pattern]]) -> Pattern:
    """Compile a sequence of suffix rules into a regex object.

    entries (Iterable[Union[str, Pattern]]): The suffix rules, e.g.
        spacy.lang.punctuation.TOKENIZER_SUFFIXES.
    RETURNS (Pattern): The regex object. to be used for Tokenizer.suffix_search.
    """
    expression = "|".join([piece + "$" for piece in entries if piece.strip()])
    return re.compile(expression)


def compile_infix_regex(entries: Iterable[Union[str, Pattern]]) -> Pattern:
    """Compile a sequence of infix rules into a regex object.

    entries (Iterable[Union[str, Pattern]]): The infix rules, e.g.
        spacy.lang.punctuation.TOKENIZER_INFIXES.
    RETURNS (regex object): The regex object. to be used for Tokenizer.infix_finditer.
    """
    expression = "|".join([piece for piece in entries if piece.strip()])
    return re.compile(expression)


def add_lookups(default_func: Callable[[str], Any], *lookups) -> Callable[[str], Any]:
    """Extend an attribute function with special cases. If a word is in the
    lookups, the value is returned. Otherwise the previous function is used.

    default_func (callable): The default function to execute.
    *lookups (dict): Lookup dictionary mapping string to attribute value.
    RETURNS (callable): Lexical attribute getter.
    """
    # This is implemented as functools.partial instead of a closure, to allow
    # pickle to work.
    return functools.partial(_get_attr_unless_lookup, default_func, lookups)


def _get_attr_unless_lookup(
    default_func: Callable[[str], Any], lookups: Dict[str, Any], string: str
) -> Any:
    for lookup in lookups:
        if string in lookup:
            return lookup[string]
    return default_func(string)


def update_exc(
    base_exceptions: Dict[str, List[dict]], *addition_dicts
) -> Dict[str, List[dict]]:
    """Update and validate tokenizer exceptions. Will overwrite exceptions.

    base_exceptions (Dict[str, List[dict]]): Base exceptions.
    *addition_dicts (Dict[str, List[dict]]): Exceptions to add to the base dict, in order.
    RETURNS (Dict[str, List[dict]]): Combined tokenizer exceptions.
    """
    exc = dict(base_exceptions)
    for additions in addition_dicts:
        for orth, token_attrs in additions.items():
            if not all(isinstance(attr[ORTH], str) for attr in token_attrs):
                raise ValueError(Errors.E055.format(key=orth, orths=token_attrs))
            described_orth = "".join(attr[ORTH] for attr in token_attrs)
            if orth != described_orth:
                raise ValueError(Errors.E056.format(key=orth, orths=described_orth))
        exc.update(additions)
    exc = expand_exc(exc, "'", "’")
    return exc


def expand_exc(
    excs: Dict[str, List[dict]], search: str, replace: str
) -> Dict[str, List[dict]]:
    """Find string in tokenizer exceptions, duplicate entry and replace string.
    For example, to add additional versions with typographic apostrophes.

    excs (Dict[str, List[dict]]): Tokenizer exceptions.
    search (str): String to find and replace.
    replace (str): Replacement.
    RETURNS (Dict[str, List[dict]]): Combined tokenizer exceptions.
    """

    def _fix_token(token, search, replace):
        fixed = dict(token)
        fixed[ORTH] = fixed[ORTH].replace(search, replace)
        return fixed

    new_excs = dict(excs)
    for token_string, tokens in excs.items():
        if search in token_string:
            new_key = token_string.replace(search, replace)
            new_value = [_fix_token(t, search, replace) for t in tokens]
            new_excs[new_key] = new_value
    return new_excs


def normalize_slice(
    length: int, start: int, stop: int, step: Optional[int] = None
) -> Tuple[int, int]:
    if not (step is None or step == 1):
        raise ValueError(Errors.E057)
    if start is None:
        start = 0
    elif start < 0:
        start += length
    start = min(length, max(0, start))
    if stop is None:
        stop = length
    elif stop < 0:
        stop += length
    stop = min(length, max(start, stop))
    return start, stop


def minibatch(
    items: Iterable[Any], size: Union[Iterator[int], int] = 8
) -> Iterator[Any]:
    """Iterate over batches of items. `size` may be an iterator,
    so that batch-size can vary on each step.
    """
    if isinstance(size, int):
        size_ = itertools.repeat(size)
    else:
        size_ = size
    items = iter(items)
    while True:
        batch_size = next(size_)
        batch = list(itertools.islice(items, int(batch_size)))
        if len(batch) == 0:
            break
        yield list(batch)


def minibatch_by_padded_size(
    docs: Iterator["Doc"],
    size: Union[Iterator[int], int],
    buffer: int = 256,
    discard_oversize: bool = False,
) -> Iterator[Iterator["Doc"]]:
    if isinstance(size, int):
        size_ = itertools.repeat(size)
    else:
        size_ = size
    for outer_batch in minibatch(docs, buffer):
        outer_batch = list(outer_batch)
        target_size = next(size_)
        for indices in _batch_by_length(outer_batch, target_size):
            subbatch = [outer_batch[i] for i in indices]
            padded_size = max(len(seq) for seq in subbatch) * len(subbatch)
            if discard_oversize and padded_size >= target_size:
                pass
            else:
                yield subbatch


def _batch_by_length(seqs: Sequence[Any], max_words: int) -> List[List[Any]]:
    """Given a list of sequences, return a batched list of indices into the
    list, where the batches are grouped by length, in descending order.

    Batches may be at most max_words in size, defined as max sequence length * size.
    """
    # Use negative index so we can get sort by position ascending.
    lengths_indices = [(len(seq), i) for i, seq in enumerate(seqs)]
    lengths_indices.sort()
    batches = []
    batch = []
    for length, i in lengths_indices:
        if not batch:
            batch.append(i)
        elif length * (len(batch) + 1) <= max_words:
            batch.append(i)
        else:
            batches.append(batch)
            batch = [i]
    if batch:
        batches.append(batch)
    # Check lengths match
    assert sum(len(b) for b in batches) == len(seqs)
    batches = [list(sorted(batch)) for batch in batches]
    batches.reverse()
    return batches


def minibatch_by_words(docs, size, tolerance=0.2, discard_oversize=False):
    """Create minibatches of roughly a given number of words. If any examples
    are longer than the specified batch length, they will appear in a batch by
    themselves, or be discarded if discard_oversize=True.
    The argument 'docs' can be a list of strings, Doc's or Example's. """
    from .gold import Example

    if isinstance(size, int):
        size_ = itertools.repeat(size)
    elif isinstance(size, List):
        size_ = iter(size)
    else:
        size_ = size
    target_size = next(size_)
    tol_size = target_size * tolerance
    batch = []
    overflow = []
    batch_size = 0
    overflow_size = 0
    for doc in docs:
        if isinstance(doc, Example):
            n_words = len(doc.reference)
        elif isinstance(doc, str):
            n_words = len(doc.split())
        else:
            n_words = len(doc)
        # if the current example exceeds the maximum batch size, it is returned separately
        # but only if discard_oversize=False.
        if n_words > target_size + tol_size:
            if not discard_oversize:
                yield [doc]
        # add the example to the current batch if there's no overflow yet and it still fits
        elif overflow_size == 0 and (batch_size + n_words) <= target_size:
            batch.append(doc)
            batch_size += n_words
        # add the example to the overflow buffer if it fits in the tolerance margin
        elif (batch_size + overflow_size + n_words) <= (target_size + tol_size):
            overflow.append(doc)
            overflow_size += n_words
        # yield the previous batch and start a new one. The new one gets the overflow examples.
        else:
            if batch:
                yield batch
            target_size = next(size_)
            tol_size = target_size * tolerance
            batch = overflow
            batch_size = overflow_size
            overflow = []
            overflow_size = 0
            # this example still fits
            if (batch_size + n_words) <= target_size:
                batch.append(doc)
                batch_size += n_words
            # this example fits in overflow
            elif (batch_size + n_words) <= (target_size + tol_size):
                overflow.append(doc)
                overflow_size += n_words
            # this example does not fit with the previous overflow: start another new batch
            else:
                if batch:
                    yield batch
                target_size = next(size_)
                tol_size = target_size * tolerance
                batch = [doc]
                batch_size = n_words
    batch.extend(overflow)
    if batch:
        yield batch


def filter_spans(spans: Iterable["Span"]) -> List["Span"]:
    """Filter a sequence of spans and remove duplicates or overlaps. Useful for
    creating named entities (where one token can only be part of one entity) or
    when merging spans with `Retokenizer.merge`. When spans overlap, the (first)
    longest span is preferred over shorter spans.

    spans (Iterable[Span]): The spans to filter.
    RETURNS (List[Span]): The filtered spans.
    """
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result


def to_bytes(getters: Dict[str, Callable[[], bytes]], exclude: Iterable[str]) -> bytes:
    return srsly.msgpack_dumps(to_dict(getters, exclude))


def from_bytes(
    bytes_data: bytes,
    setters: Dict[str, Callable[[bytes], Any]],
    exclude: Iterable[str],
) -> None:
    return from_dict(srsly.msgpack_loads(bytes_data), setters, exclude)


def to_dict(
    getters: Dict[str, Callable[[], Any]], exclude: Iterable[str]
) -> Dict[str, Any]:
    serialized = {}
    for key, getter in getters.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude:
            serialized[key] = getter()
    return serialized


def from_dict(
    msg: Dict[str, Any],
    setters: Dict[str, Callable[[Any], Any]],
    exclude: Iterable[str],
) -> Dict[str, Any]:
    for key, setter in setters.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude and key in msg:
            setter(msg[key])
    return msg


def to_disk(
    path: Union[str, Path],
    writers: Dict[str, Callable[[Path], None]],
    exclude: Iterable[str],
) -> Path:
    path = ensure_path(path)
    if not path.exists():
        path.mkdir()
    for key, writer in writers.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude:
            writer(path / key)
    return path


def from_disk(
    path: Union[str, Path],
    readers: Dict[str, Callable[[Path], None]],
    exclude: Iterable[str],
) -> Path:
    path = ensure_path(path)
    for key, reader in readers.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude:
            reader(path / key)
    return path


def import_file(name: str, loc: Union[str, Path]) -> ModuleType:
    """Import module from a file. Used to load models from a directory.

    name (str): Name of module to load.
    loc (str / Path): Path to the file.
    RETURNS: The loaded module.
    """
    loc = str(loc)
    spec = importlib.util.spec_from_file_location(name, str(loc))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minify_html(html: str) -> str:
    """Perform a template-specific, rudimentary HTML minification for displaCy.
    Disclaimer: NOT a general-purpose solution, only removes indentation and
    newlines.

    html (str): Markup to minify.
    RETURNS (str): "Minified" HTML.
    """
    return html.strip().replace("    ", "").replace("\n", "")


def escape_html(text: str) -> str:
    """Replace <, >, &, " with their HTML encoded representation. Intended to
    prevent HTML errors in rendered displaCy markup.

    text (str): The original text.
    RETURNS (str): Equivalent text to be safely used within HTML.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


def get_words_and_spaces(
    words: Iterable[str], text: str
) -> Tuple[List[str], List[bool]]:
    if "".join("".join(words).split()) != "".join(text.split()):
        raise ValueError(Errors.E194.format(text=text, words=words))
    text_words = []
    text_spaces = []
    text_pos = 0
    # normalize words to remove all whitespace tokens
    norm_words = [word for word in words if not word.isspace()]
    # align words with text
    for word in norm_words:
        try:
            word_start = text[text_pos:].index(word)
        except ValueError:
            raise ValueError(Errors.E194.format(text=text, words=words))
        if word_start > 0:
            text_words.append(text[text_pos : text_pos + word_start])
            text_spaces.append(False)
            text_pos += word_start
        text_words.append(word)
        text_spaces.append(False)
        text_pos += len(word)
        if text_pos < len(text) and text[text_pos] == " ":
            text_spaces[-1] = True
            text_pos += 1
    if text_pos < len(text):
        text_words.append(text[text_pos:])
        text_spaces.append(False)
    return (text_words, text_spaces)


def copy_config(config: Union[Dict[str, Any], Config]) -> Config:
    """Deep copy a Config. Will raise an error if the config contents are not
    JSON-serializable.

    config (Config): The config to copy.
    RETURNS (Config): The copied config.
    """
    try:
        return Config(config).copy()
    except ValueError:
        raise ValueError(Errors.E961.format(config=config))


def deep_merge_configs(
    config: Union[Dict[str, Any], Config], defaults: Union[Dict[str, Any], Config]
) -> Config:
    """Deep merge two configs, a base config and its defaults. Ignores
    references to registered functions to avoid filling in

    config (Dict[str, Any]): The config.
    destination (Dict[str, Any]): The config defaults.
    RETURNS (Dict[str, Any]): The merged config.
    """
    config = copy_config(config)
    merged = _deep_merge_configs(config, defaults)
    return Config(merged)


def _deep_merge_configs(
    config: Union[Dict[str, Any], Config], defaults: Union[Dict[str, Any], Config]
) -> Union[Dict[str, Any], Config]:
    for key, value in defaults.items():
        if isinstance(value, dict):
            node = config.setdefault(key, {})
            if not isinstance(node, dict):
                continue
            promises = [key for key in value if key.startswith("@")]
            promise = promises[0] if promises else None
            # We only update the block from defaults if it refers to the same
            # registered function
            if (
                promise
                and any(k.startswith("@") for k in node)
                and (promise in node and node[promise] != value[promise])
            ):
                continue
            defaults = _deep_merge_configs(node, value)
        elif key not in config:
            config[key] = value
    return config


def dot_to_dict(values: Dict[str, Any]) -> Dict[str, dict]:
    """Convert dot notation to a dict. For example: {"token.pos": True,
    "token._.xyz": True} becomes {"token": {"pos": True, "_": {"xyz": True }}}.

    values (Dict[str, Any]): The key/value pairs to convert.
    RETURNS (Dict[str, dict]): The converted values.
    """
    result = {}
    for key, value in values.items():
        path = result
        parts = key.lower().split(".")
        for i, item in enumerate(parts):
            is_last = i == len(parts) - 1
            path = path.setdefault(item, value if is_last else {})
    return result


def dict_to_dot(obj: Dict[str, dict]) -> Dict[str, Any]:
    """Convert dot notation to a dict. For example: {"token": {"pos": True,
    "_": {"xyz": True }}} becomes {"token.pos": True, "token._.xyz": True}.

    values (Dict[str, dict]): The dict to convert.
    RETURNS (Dict[str, Any]): The key/value pairs.
    """
    return {".".join(key): value for key, value in walk_dict(obj)}


def dot_to_object(config: Config, section: str):
    """Convert dot notation of a "section" to a specific part of the Config.
    e.g. "training.optimizer" would return the Optimizer object.
    Throws an error if the section is not defined in this config.

    config (Config): The config.
    section (str): The dot notation of the section in the config.
    RETURNS: The object denoted by the section
    """
    component = config
    parts = section.split(".")
    for item in parts:
        try:
            component = component[item]
        except (KeyError, TypeError) as e:
            msg = f"The section '{section}' is not a valid section in the provided config."
            raise KeyError(msg)
    return component


def walk_dict(
    node: Dict[str, Any], parent: List[str] = []
) -> Iterator[Tuple[List[str], Any]]:
    """Walk a dict and yield the path and values of the leaves."""
    for key, value in node.items():
        key_parent = [*parent, key]
        if isinstance(value, dict):
            yield from walk_dict(value, key_parent)
        else:
            yield (key_parent, value)


def get_arg_names(func: Callable) -> List[str]:
    """Get a list of all named arguments of a function (regular,
    keyword-only).

    func (Callable): The function
    RETURNS (List[str]): The argument names.
    """
    argspec = inspect.getfullargspec(func)
    return list(set([*argspec.args, *argspec.kwonlyargs]))


def combine_score_weights(weights: List[Dict[str, float]]) -> Dict[str, float]:
    """Combine and normalize score weights defined by components, e.g.
    {"ents_r": 0.2, "ents_p": 0.3, "ents_f": 0.5} and {"some_other_score": 1.0}.

    weights (List[dict]): The weights defined by the components.
    RETURNS (Dict[str, float]): The combined and normalized weights.
    """
    result = {}
    for w_dict in weights:
        # We need to account for weights that don't sum to 1.0 and normalize
        # the score weights accordingly, then divide score by the number of
        # components.
        total = sum(w_dict.values())
        for key, value in w_dict.items():
            weight = round(value / total / len(weights), 2)
            result[key] = result.get(key, 0.0) + weight
    return result


class DummyTokenizer:
    # add dummy methods for to_bytes, from_bytes, to_disk and from_disk to
    # allow serialization (see #1557)
    def to_bytes(self, **kwargs):
        return b""

    def from_bytes(self, _bytes_data, **kwargs):
        return self

    def to_disk(self, _path, **kwargs):
        return None

    def from_disk(self, _path, **kwargs):
        return self


def link_vectors_to_models(vocab: "Vocab") -> None:
    vectors = vocab.vectors
    if vectors.name is None:
        vectors.name = VECTORS_KEY
        if vectors.data.size != 0:
            warnings.warn(Warnings.W020.format(shape=vectors.data.shape))
    for word in vocab:
        if word.orth in vectors.key2row:
            word.rank = vectors.key2row[word.orth]
        else:
            word.rank = 0


VECTORS_KEY = "spacy_pretrained_vectors"


def create_default_optimizer() -> Optimizer:
    # TODO: Do we still want to allow env_opt?
    learn_rate = env_opt("learn_rate", 0.001)
    beta1 = env_opt("optimizer_B1", 0.9)
    beta2 = env_opt("optimizer_B2", 0.999)
    eps = env_opt("optimizer_eps", 1e-8)
    L2 = env_opt("L2_penalty", 1e-6)
    grad_clip = env_opt("grad_norm_clip", 10.0)
    L2_is_weight_decay = env_opt("L2_is_weight_decay", False)
    optimizer = Adam(
        learn_rate,
        L2=L2,
        beta1=beta1,
        beta2=beta2,
        eps=eps,
        grad_clip=grad_clip,
        L2_is_weight_decay=L2_is_weight_decay,
    )
    return optimizer
