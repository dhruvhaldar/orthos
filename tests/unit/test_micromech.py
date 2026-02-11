import pytest
from orthos.micromechanics import HalpinTsai, RuleOfMixtures

def test_rule_of_mixtures():
    Ef = 230e9
    Em = 3e9
    vf = 0.5
    E1 = RuleOfMixtures.calculate_E1(Ef, Em, vf)
    expected = Ef*vf + Em*(1-vf)
    assert abs(E1 - expected) < 1e-5

def test_halpin_tsai():
    Ef = 230e9
    Em = 3e9
    vf = 0.5
    xi = 2.0
    E2 = HalpinTsai.calculate_E2(Ef, Em, vf, xi)
    # Check bounds: E_m < E2 < Ef
    assert E2 > Em
    assert E2 < Ef
