import pytest

@pytest.mark.models
def test_simple_types(EN):
    tokens = EN(u'Mr. Best flew to New York on Saturday morning.')
    ents = list(tokens.ents)
    assert ents[0].start == 1
    assert ents[0].end == 2
    assert ents[0].label_ == 'PERSON'
    assert ents[1].start == 4
    assert ents[1].end == 6
    assert ents[1].label_ == 'GPE'


@pytest.mark.models
def test_consistency_bug(EN):
    '''Test an arbitrary sequence-consistency bug encountered during speed test'''
    tokens = EN(u'Where rap essentially went mainstream, illustrated by seminal Public Enemy, Beastie Boys and L.L. Cool J. tracks.')
