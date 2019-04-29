from ..util import make_tempdir
from ...util import ensure_path

from spacy.kb import KnowledgeBase


def test_serialize_kb_disk(en_vocab):
    kb1 = KnowledgeBase(vocab=en_vocab)

    kb1.add_entity(entity="Q53", prob=0.33)
    kb1.add_entity(entity="Q17", prob=0.2)
    kb1.add_entity(entity="Q007", prob=0.7)
    kb1.add_entity(entity="Q44", prob=0.4)
    kb1.add_alias(alias="double07", entities=["Q17", "Q007"], probabilities=[0.1, 0.9])
    kb1.add_alias(alias="guy", entities=["Q53", "Q007", "Q17", "Q44"], probabilities=[0.3, 0.3, 0.2, 0.1])
    kb1.add_alias(alias="random", entities=["Q007"], probabilities=[1.0])

    # baseline assertions
    _check_kb(kb1)

    # dumping to file & loading back in
    with make_tempdir() as d:
        dir_path = ensure_path(d)
        if not dir_path.exists():
            dir_path.mkdir()
        file_path = dir_path / "kb"
        print(file_path, type(file_path))
        kb1.dump(str(file_path))

        kb2 = KnowledgeBase(vocab=en_vocab)
        kb2.load_bulk(str(file_path))

    # final assertions
    _check_kb(kb2)


def _check_kb(kb):
    # check entities
    assert kb.get_size_entities() == 4
    for entity_string in ["Q53", "Q17", "Q007", "Q44"]:
        assert entity_string in kb.get_entity_strings()
    for entity_string in ["", "Q0"]:
        assert entity_string not in kb.get_entity_strings()

    # check aliases
    assert kb.get_size_aliases() == 3
    for alias_string in ["double07", "guy", "random"]:
        assert alias_string in kb.get_alias_strings()
    for alias_string in ["nothingness", "", "randomnoise"]:
        assert alias_string not in kb.get_alias_strings()

    # check candidates & probabilities
    candidates = sorted(kb.get_candidates("double07"), key=lambda x: x.entity_)
    assert len(candidates) == 2

    assert candidates[0].entity_ == "Q007"
    assert 0.6999 < candidates[0].entity_freq < 0.701
    assert candidates[0].alias_ == "double07"
    assert 0.899 < candidates[0].prior_prob < 0.901

    assert candidates[1].entity_ == "Q17"
    assert 0.199 < candidates[1].entity_freq < 0.201
    assert candidates[1].alias_ == "double07"
    assert 0.099 < candidates[1].prior_prob < 0.101
