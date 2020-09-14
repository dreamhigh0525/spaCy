def add_codes(err_cls):
    """Add error codes to string messages via class attribute names."""

    class ErrorsWithCodes(err_cls):
        def __getattribute__(self, code):
            msg = super(ErrorsWithCodes, self).__getattribute__(code)
            if code.startswith("__"):  # python system attributes like __class__
                return msg
            else:
                return "[{code}] {msg}".format(code=code, msg=msg)

    return ErrorsWithCodes()


# fmt: off

@add_codes
class Warnings:
    W004 = ("No text fixing enabled. Run `pip install ftfy` to enable fixing "
            "using ftfy.fix_text if necessary.")
    W005 = ("Doc object not parsed. This means displaCy won't be able to "
            "generate a dependency visualization for it. Make sure the Doc "
            "was processed with a model that supports dependency parsing, and "
            "not just a language class like `English()`. For more info, see "
            "the docs:\nhttps://nightly.spacy.io/usage/models")
    W006 = ("No entities to visualize found in Doc object. If this is "
            "surprising to you, make sure the Doc was processed using a model "
            "that supports named entity recognition, and check the `doc.ents` "
            "property manually if necessary.")
    W007 = ("The model you're using has no word vectors loaded, so the result "
            "of the {obj}.similarity method will be based on the tagger, "
            "parser and NER, which may not give useful similarity judgements. "
            "This may happen if you're using one of the small models, e.g. "
            "`en_core_web_sm`, which don't ship with word vectors and only "
            "use context-sensitive tensors. You can always add your own word "
            "vectors, or use one of the larger models instead if available.")
    W008 = ("Evaluating {obj}.similarity based on empty vectors.")
    W011 = ("It looks like you're calling displacy.serve from within a "
            "Jupyter notebook or a similar environment. This likely means "
            "you're already running a local web server, so there's no need to "
            "make displaCy start another one. Instead, you should be able to "
            "replace displacy.serve with displacy.render to show the "
            "visualization.")
    W012 = ("A Doc object you're adding to the PhraseMatcher for pattern "
            "'{key}' is parsed and/or tagged, but to match on '{attr}', you "
            "don't actually need this information. This means that creating "
            "the patterns is potentially much slower, because all pipeline "
            "components are applied. To only create tokenized Doc objects, "
            "try using `nlp.make_doc(text)` or process all texts as a stream "
            "using `list(nlp.tokenizer.pipe(all_texts))`.")
    W017 = ("Alias '{alias}' already exists in the Knowledge Base.")
    W018 = ("Entity '{entity}' already exists in the Knowledge Base - "
            "ignoring the duplicate entry.")
    W020 = ("Unnamed vectors. This won't allow multiple vectors models to be "
            "loaded. (Shape: {shape})")
    W021 = ("Unexpected hash collision in PhraseMatcher. Matches may be "
            "incorrect. Modify PhraseMatcher._terminal_hash to fix.")
    W024 = ("Entity '{entity}' - Alias '{alias}' combination already exists in "
            "the Knowledge Base.")
    W026 = ("Unable to set all sentence boundaries from dependency parses.")
    W027 = ("Found a large training file of {size} bytes. Note that it may "
            "be more efficient to split your training data into multiple "
            "smaller JSON files instead.")
    W028 = ("Doc.from_array was called with a vector of type '{type}', "
            "but is expecting one of type 'uint64' instead. This may result "
            "in problems with the vocab further on in the pipeline.")
    W030 = ("Some entities could not be aligned in the text \"{text}\" with "
            "entities \"{entities}\". Use "
            "`spacy.training.biluo_tags_from_offsets(nlp.make_doc(text), entities)`"
            " to check the alignment. Misaligned entities ('-') will be "
            "ignored during training.")
    W033 = ("Training a new {model} using a model with no lexeme normalization "
            "table. This may degrade the performance of the model to some "
            "degree. If this is intentional or the language you're using "
            "doesn't have a normalization table, please ignore this warning. "
            "If this is surprising, make sure you have the spacy-lookups-data "
            "package installed. The languages with lexeme normalization tables "
            "are currently: {langs}")
    W034 = ("Please install the package spacy-lookups-data in order to include "
            "the default lexeme normalization table for the language '{lang}'.")
    W035 = ('Discarding subpattern "{pattern}" due to an unrecognized '
            "attribute or operator.")

    # TODO: fix numbering after merging develop into master
    W090 = ("Could not locate any binary .spacy files in path '{path}'.")
    W091 = ("Could not clean/remove the temp directory at {dir}: {msg}.")
    W092 = ("Ignoring annotations for sentence starts, as dependency heads are set.")
    W093 = ("Could not find any data to train the {name} on. Is your "
            "input data correctly formatted?")
    W094 = ("Model '{model}' ({model_version}) specifies an under-constrained "
            "spaCy version requirement: {version}. This can lead to compatibility "
            "problems with older versions, or as new spaCy versions are "
            "released, because the model may say it's compatible when it's "
            'not. Consider changing the "spacy_version" in your meta.json to a '
            "version range, with a lower and upper pin. For example: {example}")
    W095 = ("Model '{model}' ({model_version}) requires spaCy {version} and is "
            "incompatible with the current version ({current}). This may lead "
            "to unexpected results or runtime errors. To resolve this, "
            "download a newer compatible model or retrain your custom model "
            "with the current spaCy version. For more details and available "
            "updates, run: python -m spacy validate")
    W096 = ("The method 'disable_pipes' has become deprecated - use 'select_pipes' "
            "instead.")
    W097 = ("No Model config was provided to create the '{name}' component, "
            "and no default configuration could be found either.")
    W098 = ("No Model config was provided to create the '{name}' component, "
            "so a default configuration was used.")
    W099 = ("Expected 'dict' type for the 'model' argument of pipe '{pipe}', "
            "but got '{type}' instead, so ignoring it.")
    W100 = ("Skipping unsupported morphological feature(s): '{feature}'. "
            "Provide features as a dict {{\"Field1\": \"Value1,Value2\"}} or "
            "string \"Field1=Value1,Value2|Field2=Value3\".")
    W101 = ("Skipping `Doc` custom extension '{name}' while merging docs.")
    W102 = ("Skipping unsupported user data '{key}: {value}' while merging docs.")
    W103 = ("Unknown {lang} word segmenter '{segmenter}'. Supported "
            "word segmenters: {supported}. Defaulting to {default}.")
    W104 = ("Skipping modifications for '{target}' segmenter. The current "
            "segmenter is '{current}'.")
    W105 = ("As of spaCy v3.0, the {matcher}.pipe method is deprecated. If you "
            "need to match on a stream of documents, you can use nlp.pipe and "
            "call the {matcher} on each Doc object.")


@add_codes
class Errors:
    E001 = ("No component '{name}' found in pipeline. Available names: {opts}")
    E002 = ("Can't find factory for '{name}' for language {lang} ({lang_code}). "
            "This usually happens when spaCy calls nlp.{method} with custom "
            "component name that's not registered on the current language class. "
            "If you're using a custom component, make sure you've added the "
            "decorator @Language.component (for function components) or "
            "@Language.factory (for class components).\n\nAvailable "
            "factories: {opts}")
    E003 = ("Not a valid pipeline component. Expected callable, but "
            "got {component} (name: '{name}'). If you're using a custom "
            "component factory, double-check that it correctly returns your "
            "initialized component.")
    E004 = ("Can't set up pipeline component: a factory for '{name}' already "
            "exists. Existing factory: {func}. New factory: {new_func}")
    E005 = ("Pipeline component '{name}' returned None. If you're using a "
            "custom component, maybe you forgot to return the processed Doc?")
    E006 = ("Invalid constraints for adding pipeline component. You can only "
            "set one of the following: before (component name or index), "
            "after (component name or index), first (True) or last (True). "
            "Invalid configuration: {args}. Existing components: {opts}")
    E007 = ("'{name}' already exists in pipeline. Existing names: {opts}")
    E008 = ("Can't restore disabled pipeline component '{name}' because it "
            "doesn't exist in the pipeline anymore. If you want to remove "
            "components from the pipeline, you should do it before calling "
            "`nlp.select_pipes()` or after restoring the disabled components.")
    E010 = ("Word vectors set to length 0. This may be because you don't have "
            "a model installed or loaded, or because your model doesn't "
            "include word vectors. For more info, see the docs:\n"
            "https://nightly.spacy.io/usage/models")
    E011 = ("Unknown operator: '{op}'. Options: {opts}")
    E012 = ("Cannot add pattern for zero tokens to matcher.\nKey: {key}")
    E014 = ("Unknown tag ID: {tag}")
    E016 = ("MultitaskObjective target should be function or one of: dep, "
            "tag, ent, dep_tag_offset, ent_tag.")
    E017 = ("Can only add unicode or bytes. Got type: {value_type}")
    E018 = ("Can't retrieve string for hash '{hash_value}'. This usually "
            "refers to an issue with the `Vocab` or `StringStore`.")
    E019 = ("Can't create transition with unknown action ID: {action}. Action "
            "IDs are enumerated in spacy/syntax/{src}.pyx.")
    E022 = ("Could not find a transition with the name '{name}' in the NER "
            "model.")
    E024 = ("Could not find an optimal move to supervise the parser. Usually, "
            "this means that the model can't be updated in a way that's valid "
            "and satisfies the correct annotations specified in the GoldParse. "
            "For example, are all labels added to the model? If you're "
            "training a named entity recognizer, also make sure that none of "
            "your annotated entity spans have leading or trailing whitespace "
            "or punctuation. "
            "You can also use the experimental `debug data` command to "
            "validate your JSON-formatted training data. For details, run:\n"
            "python -m spacy debug data --help")
    E025 = ("String is too long: {length} characters. Max is 2**30.")
    E026 = ("Error accessing token at position {i}: out of bounds in Doc of "
            "length {length}.")
    E027 = ("Arguments 'words' and 'spaces' should be sequences of the same "
            "length, or 'spaces' should be left default at None. spaces "
            "should be a sequence of booleans, with True meaning that the "
            "word owns a ' ' character following it.")
    E028 = ("orths_and_spaces expects either a list of unicode string or a "
            "list of (unicode, bool) tuples. Got bytes instance: {value}")
    E029 = ("noun_chunks requires the dependency parse, which requires a "
            "statistical model to be installed and loaded. For more info, see "
            "the documentation:\nhttps://nightly.spacy.io/usage/models")
    E030 = ("Sentence boundaries unset. You can add the 'sentencizer' "
            "component to the pipeline with: "
            "nlp.add_pipe('sentencizer'). "
            "Alternatively, add the dependency parser, or set sentence "
            "boundaries by setting doc[i].is_sent_start.")
    E031 = ("Invalid token: empty string ('') at position {i}.")
    E032 = ("Conflicting attributes specified in doc.from_array(): "
            "(HEAD, SENT_START). The HEAD attribute currently sets sentence "
            "boundaries implicitly, based on the tree structure. This means "
            "the HEAD attribute would potentially override the sentence "
            "boundaries set by SENT_START.")
    E033 = ("Cannot load into non-empty Doc of length {length}.")
    E035 = ("Error creating span with start {start} and end {end} for Doc of "
            "length {length}.")
    E036 = ("Error calculating span: Can't find a token starting at character "
            "offset {start}.")
    E037 = ("Error calculating span: Can't find a token ending at character "
            "offset {end}.")
    E039 = ("Array bounds exceeded while searching for root word. This likely "
            "means the parse tree is in an invalid state. Please report this "
            "issue here: http://github.com/explosion/spaCy/issues")
    E040 = ("Attempt to access token at {i}, max length {max_length}.")
    E041 = ("Invalid comparison operator: {op}. Likely a Cython bug?")
    E042 = ("Error accessing doc[{i}].nbor({j}), for doc of length {length}.")
    E043 = ("Refusing to write to token.sent_start if its document is parsed, "
            "because this may cause inconsistent state.")
    E044 = ("Invalid value for token.sent_start: {value}. Must be one of: "
            "None, True, False")
    E045 = ("Possibly infinite loop encountered while looking for {attr}.")
    E046 = ("Can't retrieve unregistered extension attribute '{name}'. Did "
            "you forget to call the `set_extension` method?")
    E047 = ("Can't assign a value to unregistered extension attribute "
            "'{name}'. Did you forget to call the `set_extension` method?")
    E048 = ("Can't import language {lang} from spacy.lang: {err}")
    E050 = ("Can't find model '{name}'. It doesn't seem to be a Python "
            "package or a valid path to a data directory.")
    E052 = ("Can't find model directory: {path}")
    E053 = ("Could not read {name} from {path}")
    E054 = ("No valid '{setting}' setting found in model meta.json.")
    E055 = ("Invalid ORTH value in exception:\nKey: {key}\nOrths: {orths}")
    E056 = ("Invalid tokenizer exception: ORTH values combined don't match "
            "original string.\nKey: {key}\nOrths: {orths}")
    E057 = ("Stepped slices not supported in Span objects. Try: "
            "list(tokens)[start:stop:step] instead.")
    E058 = ("Could not retrieve vector for key {key}.")
    E059 = ("One (and only one) keyword arg must be set. Got: {kwargs}")
    E060 = ("Cannot add new key to vectors: the table is full. Current shape: "
            "({rows}, {cols}).")
    E062 = ("Cannot find empty bit for new lexical flag. All bits between 0 "
            "and 63 are occupied. You can replace one by specifying the "
            "`flag_id` explicitly, e.g. "
            "`nlp.vocab.add_flag(your_func, flag_id=IS_ALPHA`.")
    E063 = ("Invalid value for flag_id: {value}. Flag IDs must be between 1 "
            "and 63 (inclusive).")
    E064 = ("Error fetching a Lexeme from the Vocab. When looking up a "
            "string, the lexeme returned had an orth ID that did not match "
            "the query string. This means that the cached lexeme structs are "
            "mismatched to the string encoding table. The mismatched:\n"
            "Query string: {string}\nOrth cached: {orth}\nOrth ID: {orth_id}")
    E065 = ("Only one of the vector table's width and shape can be specified. "
            "Got width {width} and shape {shape}.")
    E067 = ("Invalid BILUO tag sequence: Got a tag starting with {start} "
            "without a preceding 'B' (beginning of an entity). "
            "Tag sequence:\n{tags}")
    E068 = ("Invalid BILUO tag: '{tag}'.")
    E071 = ("Error creating lexeme: specified orth ID ({orth}) does not "
            "match the one in the vocab ({vocab_orth}).")
    E073 = ("Cannot assign vector of length {new_length}. Existing vectors "
            "are of length {length}. You can use `vocab.reset_vectors` to "
            "clear the existing vectors and resize the table.")
    E074 = ("Error interpreting compiled match pattern: patterns are expected "
            "to end with the attribute {attr}. Got: {bad_attr}.")
    E082 = ("Error deprojectivizing parse: number of heads ({n_heads}), "
            "projective heads ({n_proj_heads}) and labels ({n_labels}) do not "
            "match.")
    E083 = ("Error setting extension: only one of `default`, `method`, or "
            "`getter` (plus optional `setter`) is allowed. Got: {nr_defined}")
    E084 = ("Error assigning label ID {label} to span: not in StringStore.")
    E085 = ("Can't create lexeme for string '{string}'.")
    E087 = ("Unknown displaCy style: {style}.")
    E088 = ("Text of length {length} exceeds maximum of {max_length}. The "
            "v2.x parser and NER models require roughly 1GB of temporary "
            "memory per 100,000 characters in the input. This means long "
            "texts may cause memory allocation errors. If you're not using "
            "the parser or NER, it's probably safe to increase the "
            "`nlp.max_length` limit. The limit is in number of characters, so "
            "you can check whether your inputs are too long by checking "
            "`len(text)`.")
    E089 = ("Extensions can't have a setter argument without a getter "
            "argument. Check the keyword arguments on `set_extension`.")
    E090 = ("Extension '{name}' already exists on {obj}. To overwrite the "
            "existing extension, set `force=True` on `{obj}.set_extension`.")
    E091 = ("Invalid extension attribute {name}: expected callable or None, "
            "but got: {value}")
    E093 = ("token.ent_iob values make invalid sequence: I without B\n{seq}")
    E094 = ("Error reading line {line_num} in vectors file {loc}.")
    E095 = ("Can't write to frozen dictionary. This is likely an internal "
            "error. Are you writing to a default function argument?")
    E096 = ("Invalid object passed to displaCy: Can only visualize Doc or "
            "Span objects, or dicts if set to manual=True.")
    E097 = ("Invalid pattern: expected token pattern (list of dicts) or "
            "phrase pattern (string) but got:\n{pattern}")
    E098 = ("Invalid pattern: expected both RIGHT_ID and RIGHT_ATTRS.")
    E099 = ("Invalid pattern: the first node of pattern should be an anchor "
            "node. The node should only contain RIGHT_ID and RIGHT_ATTRS.")
    E100 = ("Nodes other than the anchor node should all contain LEFT_ID, "
            "REL_OP and RIGHT_ID.")
    E101 = ("RIGHT_ID should be a new node and LEFT_ID should already have "
            "have been declared in previous edges.")
    E102 = ("Can't merge non-disjoint spans. '{token}' is already part of "
            "tokens to merge. If you want to find the longest non-overlapping "
            "spans, you can use the util.filter_spans helper:\n"
            "https://nightly.spacy.io/api/top-level#util.filter_spans")
    E103 = ("Trying to set conflicting doc.ents: '{span1}' and '{span2}'. A "
            "token can only be part of one entity, so make sure the entities "
            "you're setting don't overlap.")
    E106 = ("Can't find doc._.{attr} attribute specified in the underscore "
            "settings: {opts}")
    E107 = ("Value of doc._.{attr} is not JSON-serializable: {value}")
    E109 = ("Component '{name}' could not be run. Did you forget to "
            "call begin_training()?")
    E110 = ("Invalid displaCy render wrapper. Expected callable, got: {obj}")
    E111 = ("Pickling a token is not supported, because tokens are only views "
            "of the parent Doc and can't exist on their own. A pickled token "
            "would always have to include its Doc and Vocab, which has "
            "practically no advantage over pickling the parent Doc directly. "
            "So instead of pickling the token, pickle the Doc it belongs to.")
    E112 = ("Pickling a span is not supported, because spans are only views "
            "of the parent Doc and can't exist on their own. A pickled span "
            "would always have to include its Doc and Vocab, which has "
            "practically no advantage over pickling the parent Doc directly. "
            "So instead of pickling the span, pickle the Doc it belongs to or "
            "use Span.as_doc to convert the span to a standalone Doc object.")
    E115 = ("All subtokens must have associated heads.")
    E117 = ("The newly split tokens must match the text of the original token. "
            "New orths: {new}. Old text: {old}.")
    E118 = ("The custom extension attribute '{attr}' is not registered on the "
            "Token object so it can't be set during retokenization. To "
            "register an attribute, use the Token.set_extension classmethod.")
    E119 = ("Can't set custom extension attribute '{attr}' during "
            "retokenization because it's not writable. This usually means it "
            "was registered with a getter function (and no setter) or as a "
            "method extension, so the value is computed dynamically. To "
            "overwrite a custom attribute manually, it should be registered "
            "with a default value or with a getter AND setter.")
    E120 = ("Can't set custom extension attributes during retokenization. "
            "Expected dict mapping attribute names to values, but got: {value}")
    E121 = ("Can't bulk merge spans. Attribute length {attr_len} should be "
            "equal to span length ({span_len}).")
    E122 = ("Cannot find token to be split. Did it get merged?")
    E123 = ("Cannot find head of token to be split. Did it get merged?")
    E125 = ("Unexpected value: {value}")
    E126 = ("Unexpected matcher predicate: '{bad}'. Expected one of: {good}. "
            "This is likely a bug in spaCy, so feel free to open an issue.")
    E129 = ("Cannot write the label of an existing Span object because a Span "
            "is a read-only view of the underlying Token objects stored in the "
            "Doc. Instead, create a new Span object and specify the `label` "
            "keyword argument, for example:\nfrom spacy.tokens import Span\n"
            "span = Span(doc, start={start}, end={end}, label='{label}')")
    E130 = ("You are running a narrow unicode build, which is incompatible "
            "with spacy >= 2.1.0. To fix this, reinstall Python and use a wide "
            "unicode build instead. You can also rebuild Python and set the "
            "--enable-unicode=ucs4 flag.")
    E131 = ("Cannot write the kb_id of an existing Span object because a Span "
            "is a read-only view of the underlying Token objects stored in "
            "the Doc. Instead, create a new Span object and specify the "
            "`kb_id` keyword argument, for example:\nfrom spacy.tokens "
            "import Span\nspan = Span(doc, start={start}, end={end}, "
            "label='{label}', kb_id='{kb_id}')")
    E132 = ("The vectors for entities and probabilities for alias '{alias}' "
            "should have equal length, but found {entities_length} and "
            "{probabilities_length} respectively.")
    E133 = ("The sum of prior probabilities for alias '{alias}' should not "
            "exceed 1, but found {sum}.")
    E134 = ("Entity '{entity}' is not defined in the Knowledge Base.")
    E137 = ("Expected 'dict' type, but got '{type}' from '{line}'. Make sure "
            "to provide a valid JSON object as input with either the `text` "
            "or `tokens` key. For more info, see the docs:\n"
            "https://nightly.spacy.io/api/cli#pretrain-jsonl")
    E138 = ("Invalid JSONL format for raw text '{text}'. Make sure the input "
            "includes either the `text` or `tokens` key. For more info, see "
            "the docs:\nhttps://nightly.spacy.io/api/cli#pretrain-jsonl")
    E139 = ("Knowledge Base for component '{name}' is empty. Use the methods "
            "kb.add_entity and kb.add_alias to add entries.")
    E140 = ("The list of entities, prior probabilities and entity vectors "
            "should be of equal length.")
    E141 = ("Entity vectors should be of length {required} instead of the "
            "provided {found}.")
    E143 = ("Labels for component '{name}' not initialized. This can be fixed "
            "by calling add_label, or by providing a representative batch of "
            "examples to the component's begin_training method.")
    E145 = ("Error reading `{param}` from input file.")
    E146 = ("Could not access `{path}`.")
    E147 = ("Unexpected error in the {method} functionality of the "
            "EntityLinker: {msg}. This is likely a bug in spaCy, so feel free "
            "to open an issue.")
    E148 = ("Expected {ents} KB identifiers but got {ids}. Make sure that "
            "each entity in `doc.ents` is assigned to a KB identifier.")
    E149 = ("Error deserializing model. Check that the config used to create "
            "the component matches the model being loaded.")
    E150 = ("The language of the `nlp` object and the `vocab` should be the "
            "same, but found '{nlp}' and '{vocab}' respectively.")
    E152 = ("The attribute {attr} is not supported for token patterns. "
            "Please use the option validate=True with Matcher, PhraseMatcher, "
            "or EntityRuler for more details.")
    E153 = ("The value type {vtype} is not supported for token patterns. "
            "Please use the option validate=True with Matcher, PhraseMatcher, "
            "or EntityRuler for more details.")
    E154 = ("One of the attributes or values is not supported for token "
            "patterns. Please use the option validate=True with Matcher, "
            "PhraseMatcher, or EntityRuler for more details.")
    E155 = ("The pipeline needs to include a tagger in order to use "
            "Matcher or PhraseMatcher with the attributes POS, TAG, or LEMMA. "
            "Try using nlp() instead of nlp.make_doc() or list(nlp.pipe()) "
            "instead of list(nlp.tokenizer.pipe()).")
    E156 = ("The pipeline needs to include a parser in order to use "
            "Matcher or PhraseMatcher with the attribute DEP. Try using "
            "nlp() instead of nlp.make_doc() or list(nlp.pipe()) instead of "
            "list(nlp.tokenizer.pipe()).")
    E157 = ("Can't render negative values for dependency arc start or end. "
            "Make sure that you're passing in absolute token indices, not "
            "relative token offsets.\nstart: {start}, end: {end}, label: "
            "{label}, direction: {dir}")
    E158 = ("Can't add table '{name}' to lookups because it already exists.")
    E159 = ("Can't find table '{name}' in lookups. Available tables: {tables}")
    E160 = ("Can't find language data file: {path}")
    E161 = ("Found an internal inconsistency when predicting entity links. "
            "This is likely a bug in spaCy, so feel free to open an issue.")
    E162 = ("Cannot evaluate textcat model on data with different labels.\n"
            "Labels in model: {model_labels}\nLabels in evaluation "
            "data: {eval_labels}")
    E163 = ("cumsum was found to be unstable: its last element does not "
            "correspond to sum")
    E164 = ("x is neither increasing nor decreasing: {}.")
    E165 = ("Only one class present in y_true. ROC AUC score is not defined in "
            "that case.")
    E166 = ("Can only merge DocBins with the same pre-defined attributes.\n"
            "Current DocBin: {current}\nOther DocBin: {other}")
    E169 = ("Can't find module: {module}")
    E170 = ("Cannot apply transition {name}: invalid for the current state.")
    E171 = ("Matcher.add received invalid 'on_match' callback argument: expected "
            "callable or None, but got: {arg_type}")
    E175 = ("Can't remove rule for unknown match pattern ID: {key}")
    E176 = ("Alias '{alias}' is not defined in the Knowledge Base.")
    E177 = ("Ill-formed IOB input detected: {tag}")
    E178 = ("Each pattern should be a list of dicts, but got: {pat}. Maybe you "
            "accidentally passed a single pattern to Matcher.add instead of a "
            "list of patterns? If you only want to add one pattern, make sure "
            "to wrap it in a list. For example: matcher.add('{key}', [pattern])")
    E179 = ("Invalid pattern. Expected a list of Doc objects but got a single "
            "Doc. If you only want to add one pattern, make sure to wrap it "
            "in a list. For example: matcher.add('{key}', [doc])")
    E180 = ("Span attributes can't be declared as required or assigned by "
            "components, since spans are only views of the Doc. Use Doc and "
            "Token attributes (or custom extension attributes) only and remove "
            "the following: {attrs}")
    E181 = ("Received invalid attributes for unkown object {obj}: {attrs}. "
            "Only Doc and Token attributes are supported.")
    E182 = ("Received invalid attribute declaration: {attr}\nDid you forget "
            "to define the attribute? For example: {attr}.???")
    E183 = ("Received invalid attribute declaration: {attr}\nOnly top-level "
            "attributes are supported, for example: {solution}")
    E184 = ("Only attributes without underscores are supported in component "
            "attribute declarations (because underscore and non-underscore "
            "attributes are connected anyways): {attr} -> {solution}")
    E185 = ("Received invalid attribute in component attribute declaration: "
            "{obj}.{attr}\nAttribute '{attr}' does not exist on {obj}.")
    E186 = ("'{tok_a}' and '{tok_b}' are different texts.")
    E187 = ("Only unicode strings are supported as labels.")
    E189 = ("Each argument to `get_doc` should be of equal length.")
    E190 = ("Token head out of range in `Doc.from_array()` for token index "
            "'{index}' with value '{value}' (equivalent to relative head "
            "index: '{rel_head_index}'). The head indices should be relative "
            "to the current token index rather than absolute indices in the "
            "array.")
    E191 = ("Invalid head: the head token must be from the same doc as the "
            "token itself.")
    E192 = ("Unable to resize vectors in place with cupy.")
    E193 = ("Unable to resize vectors in place if the resized vector dimension "
            "({new_dim}) is not the same as the current vector dimension "
            "({curr_dim}).")
    E194 = ("Unable to aligned mismatched text '{text}' and words '{words}'.")
    E195 = ("Matcher can be called on {good} only, got {got}.")
    E196 = ("Refusing to write to token.is_sent_end. Sentence boundaries can "
            "only be fixed with token.is_sent_start.")
    E197 = ("Row out of bounds, unable to add row {row} for key {key}.")
    E198 = ("Unable to return {n} most similar vectors for the current vectors "
            "table, which contains {n_rows} vectors.")
    E199 = ("Unable to merge 0-length span at doc[{start}:{end}].")
    E200 = ("Specifying a base model with a pretrained component '{component}' "
            "can not be combined with adding a pretrained Tok2Vec layer.")
    E201 = ("Span index out of range.")

    # TODO: fix numbering after merging develop into master
    E919 = ("A textcat 'positive_label' '{pos_label}' was provided for training "
            "data that does not appear to be a binary classification problem "
            "with two labels. Labels found: {labels}")
    E920 = ("The textcat's 'positive_label' config setting '{pos_label}' "
            "does not match any label in the training data. Labels found: {labels}")
    E921 = ("The method 'set_output' can only be called on components that have "
            "a Model with a 'resize_output' attribute. Otherwise, the output "
            "layer can not be dynamically changed.")
    E922 = ("Component '{name}' has been initialized with an output dimension of "
            "{nO} - cannot add any more labels.")
    E923 = ("It looks like there is no proper sample data to initialize the "
            "Model of component '{name}'. "
            "This is likely a bug in spaCy, so feel free to open an issue.")
    E924 = ("The '{name}' component does not seem to be initialized properly. "
            "This is likely a bug in spaCy, so feel free to open an issue.")
    E925 = ("Invalid color values for displaCy visualizer: expected dictionary "
            "mapping label names to colors but got: {obj}")
    E926 = ("It looks like you're trying to modify nlp.{attr} directly. This "
            "doesn't work because it's an immutable computed property. If you "
            "need to modify the pipeline, use the built-in methods like "
            "nlp.add_pipe, nlp.remove_pipe, nlp.disable_pipe or nlp.enable_pipe "
            "instead.")
    E927 = ("Can't write to frozen list Maybe you're trying to modify a computed "
            "property or default function argument?")
    E928 = ("A 'KnowledgeBase' should be written to / read from a file, but the "
            "provided argument {loc} is an existing directory.")
    E929 = ("A 'KnowledgeBase' could not be read from {loc} - the path does "
            "not seem to exist.")
    E930 = ("Received invalid get_examples callback in {name}.begin_training. "
            "Expected function that returns an iterable of Example objects but "
            "got: {obj}")
    E931 = ("Encountered Pipe subclass without Pipe.{method} method in component "
            "'{name}'. If the component is trainable and you want to use this "
            "method, make sure it's overwritten on the subclass. If your "
            "component isn't trainable, add a method that does nothing or "
            "don't use the Pipe base class.")
    E940 = ("Found NaN values in scores.")
    E941 = ("Can't find model '{name}'. It looks like you're trying to load a "
            "model from a shortcut, which is deprecated as of spaCy v3.0. To "
            "load the model, use its full name instead:\n\n"
            "nlp = spacy.load(\"{full}\")\n\nFor more details on the available "
            "models, see the models directory: https://spacy.io/models. If you "
            "want to create a blank model, use spacy.blank: "
            "nlp = spacy.blank(\"{name}\")")
    E942 = ("Executing after_{name} callback failed. Expected the function to "
            "return an initialized nlp object but got: {value}. Maybe "
            "you forgot to return the modified object in your function?")
    E943 = ("Executing before_creation callback failed. Expected the function to "
            "return an uninitialized Language subclass but got: {value}. Maybe "
            "you forgot to return the modified object in your function or "
            "returned the initialized nlp object instead?")
    E944 = ("Can't copy pipeline component '{name}' from source model '{model}': "
            "not found in pipeline. Available components: {opts}")
    E945 = ("Can't copy pipeline component '{name}' from source. Expected loaded "
            "nlp object, but got: {source}")
    E947 = ("Matcher.add received invalid 'greedy' argument: expected "
            "a string value from {expected} but got: '{arg}'")
    E948 = ("Matcher.add received invalid 'patterns' argument: expected "
            "a List, but got: {arg_type}")
    E949 = ("Can only create an alignment when the texts are the same.")
    E952 = ("The section '{name}' is not a valid section in the provided config.")
    E953 = ("Mismatched IDs received by the Tok2Vec listener: {id1} vs. {id2}")
    E954 = ("The Tok2Vec listener did not receive a valid input.")
    E955 = ("Can't find table(s) '{table}' for language '{lang}' in spacy-lookups-data.")
    E956 = ("Can't find component '{name}' in [components] block in the config. "
            "Available components: {opts}")
    E957 = ("Writing directly to Language.factories isn't needed anymore in "
            "spaCy v3. Instead, you can use the @Language.factory decorator "
            "to register your custom component factory or @Language.component "
            "to register a simple stateless function component that just takes "
            "a Doc and returns it.")
    E958 = ("Language code defined in config ({bad_lang_code}) does not match "
            "language code of current Language subclass {lang} ({lang_code})")
    E959 = ("Can't insert component {dir} index {idx}. Existing components: {opts}")
    E960 = ("No config data found for component '{name}'. This is likely a bug "
            "in spaCy.")
    E961 = ("Found non-serializable Python object in config. Configs should "
            "only include values that can be serialized to JSON. If you need "
            "to pass models or other objects to your component, use a reference "
            "to a registered function or initialize the object in your "
            "component.\n\n{config}")
    E962 = ("Received incorrect {style} for pipe '{name}'. Expected dict, "
            "got: {cfg_type}.")
    E963 = ("Can't read component info from @Language.{decorator} decorator. "
            "Maybe you forgot to call it? Make sure you're using "
            "@Language.{decorator}() instead of @Language.{decorator}.")
    E964 = ("The pipeline component factory for '{name}' needs to have the "
            "following named arguments, which are passed in by spaCy:\n- nlp: "
            "receives the current nlp object and lets you access the vocab\n- "
            "name: the name of the component instance, can be used to identify "
            "the component, output losses etc.")
    E965 = ("It looks like you're using the @Language.component decorator to "
            "register '{name}' on a class instead of a function component. If "
            "you need to register a class or function that *returns* a component "
            "function, use the @Language.factory decorator instead.")
    E966 = ("nlp.add_pipe now takes the string name of the registered component "
            "factory, not a callable component. Expected string, but got "
            "{component} (name: '{name}').\n\n- If you created your component "
            "with nlp.create_pipe('name'): remove nlp.create_pipe and call "
            "nlp.add_pipe('name') instead.\n\n- If you passed in a component "
            "like TextCategorizer(): call nlp.add_pipe with the string name "
            "instead, e.g. nlp.add_pipe('textcat').\n\n- If you're using a custom "
            "component: Add the decorator @Language.component (for function "
            "components) or @Language.factory (for class components / factories) "
            "to your custom component and assign it a name, e.g. "
            "@Language.component('your_name'). You can then run "
            "nlp.add_pipe('your_name') to add it to the pipeline.")
    E967 = ("No {meta} meta information found for '{name}'. This is likely a bug in spaCy.")
    E968 = ("nlp.replace_pipe now takes the string name of the registered component "
            "factory, not a callable component. Expected string, but got "
            "{component}.\n\n- If you created your component with"
            "with nlp.create_pipe('name'): remove nlp.create_pipe and call "
            "nlp.replace_pipe('{name}', 'name') instead.\n\n- If you passed in a "
            "component like TextCategorizer(): call nlp.replace_pipe with the "
            "string name instead, e.g. nlp.replace_pipe('{name}', 'textcat').\n\n"
            "- If you're using a custom component: Add the decorator "
            "@Language.component (for function components) or @Language.factory "
            "(for class components / factories) to your custom component and "
            "assign it a name, e.g. @Language.component('your_name'). You can "
            "then run nlp.replace_pipe('{name}', 'your_name').")
    E969 = ("Expected string values for field '{field}', but received {types} instead. ")
    E970 = ("Can not execute command '{str_command}'. Do you have '{tool}' installed?")
    E971 = ("Found incompatible lengths in Doc.from_array: {array_length} for the "
            "array and {doc_length} for the Doc itself.")
    E972 = ("Example.__init__ got None for '{arg}'. Requires Doc.")
    E973 = ("Unexpected type for NER data")
    E974 = ("Unknown {obj} attribute: {key}")
    E976 = ("The method 'Example.from_dict' expects a {type} as {n} argument, "
            "but received None.")
    E977 = ("Can not compare a MorphAnalysis with a string object. "
            "This is likely a bug in spaCy, so feel free to open an issue.")
    E978 = ("The {name} method takes a list of Example objects, but got: {types}")
    E979 = ("Cannot convert {type} to an Example object.")
    E980 = ("Each link annotation should refer to a dictionary with at most one "
            "identifier mapping to 1.0, and all others to 0.0.")
    E981 = ("The offsets of the annotations for 'links' could not be aligned "
            "to token boundaries.")
    E982 = ("The 'ent_iob' attribute of a Token should be an integer indexing "
            "into {values}, but found {value}.")
    E983 = ("Invalid key for '{dict}': {key}. Available keys: "
            "{keys}")
    E984 = ("Invalid component config for '{name}': component block needs either "
            "a key 'factory' specifying the registered function used to "
            "initialize the component, or a key 'source' key specifying a "
            "spaCy model to copy the component from. For example, factory = "
            "\"ner\" will use the 'ner' factory and all other settings in the "
            "block will be passed to it as arguments. Alternatively, source = "
            "\"en_core_web_sm\" will copy the component from that model.\n\n{config}")
    E985 = ("Can't load model from config file: no 'nlp' section found.\n\n{config}")
    E986 = ("Could not create any training batches: check your input. "
            "Are the train and dev paths defined? "
            "Is 'discard_oversize' set appropriately? ")
    E987 = ("The text of an example training instance is either a Doc or "
            "a string, but found {type} instead.")
    E988 = ("Could not parse any training examples. Ensure the data is "
            "formatted correctly.")
    E989 = ("'nlp.update()' was called with two positional arguments. This "
            "may be due to a backwards-incompatible change to the format "
            "of the training data in spaCy 3.0 onwards. The 'update' "
            "function should now be called with a batch of 'Example' "
            "objects, instead of (text, annotation) tuples. ")
    E991 = ("The function 'select_pipes' should be called with either a "
            "'disable' argument to list the names of the pipe components "
            "that should be disabled, or with an 'enable' argument that "
            "specifies which pipes should not be disabled.")
    E992 = ("The function `select_pipes` was called with `enable`={enable} "
            "and `disable`={disable} but that information is conflicting "
            "for the `nlp` pipeline with components {names}.")
    E993 = ("The config for 'nlp' needs to include a key 'lang' specifying "
            "the code of the language to initialize it with (for example "
            "'en' for English) - this can't be 'None'.\n\n{config}")
    E996 = ("Could not parse {file}: {msg}")
    E997 = ("Tokenizer special cases are not allowed to modify the text. "
            "This would map '{chunk}' to '{orth}' given token attributes "
            "'{token_attrs}'.")
    E999 = ("Unable to merge the `Doc` objects because they do not all share "
            "the same `Vocab`.")
    E1000 = ("No pkuseg model available. Provide a pkuseg model when "
             "initializing the pipeline:\n"
             'cfg = {"tokenizer": {"segmenter": "pkuseg", "pkuseg_model": name_or_path}}\n'
             'nlp = Chinese(config=cfg)')
    E1001 = ("Target token outside of matched span for match with tokens "
             "'{span}' and offset '{index}' matched by patterns '{patterns}'.")
    E1002 = ("Span index out of range.")
    E1003 = ("Unsupported lemmatizer mode '{mode}'.")
    E1004 = ("Missing lemmatizer table(s) found for lemmatizer mode '{mode}'. "
             "Required tables '{tables}', found '{found}'. If you are not "
             "providing custom lookups, make sure you have the package "
             "spacy-lookups-data installed.")
    E1005 = ("Unable to set attribute '{attr}' in tokenizer exception for "
             "'{chunk}'. Tokenizer exceptions are only allowed to specify "
             "`ORTH` and `NORM`.")
    E1006 = ("Unable to initialize {name} model with 0 labels.")
    E1007 = ("Unsupported DependencyMatcher operator '{op}'.")
    E1008 = ("Invalid pattern: each pattern should be a list of dicts. Check "
             "that you are providing a list of patterns as `List[List[dict]]`.")
    E1009 = ("String for hash '{val}' not found in StringStore. Set the value "
             "through token.morph_ instead or add the string to the "
             "StringStore with `nlp.vocab.strings.add(string)`.")


@add_codes
class TempErrors:
    T003 = ("Resizing pretrained Tagger models is not currently supported.")
    T007 = ("Can't yet set {attr} from Span. Vote for this feature on the "
            "issue tracker: http://github.com/explosion/spaCy/issues")


# Deprecated model shortcuts, only used in errors and warnings
OLD_MODEL_SHORTCUTS = {
    "en": "en_core_web_sm", "de": "de_core_news_sm", "es": "es_core_news_sm",
    "pt": "pt_core_news_sm", "fr": "fr_core_news_sm", "it": "it_core_news_sm",
    "nl": "nl_core_news_sm", "el": "el_core_news_sm", "nb": "nb_core_news_sm",
    "lt": "lt_core_news_sm", "xx": "xx_ent_wiki_sm"
}


# fmt: on


class MatchPatternError(ValueError):
    def __init__(self, key, errors):
        """Custom error for validating match patterns.

        key (str): The name of the matcher rule.
        errors (dict): Validation errors (sequence of strings) mapped to pattern
            ID, i.e. the index of the added pattern.
        """
        msg = f"Invalid token patterns for matcher rule '{key}'\n"
        for pattern_idx, error_msgs in errors.items():
            pattern_errors = "\n".join([f"- {e}" for e in error_msgs])
            msg += f"\nPattern {pattern_idx}:\n{pattern_errors}\n"
        ValueError.__init__(self, msg)
