from math import isfinite

import pytest

from hep_lab.kinematics import invariant_mass
from hep_lab.simulation import generate


def test_back_to_back_mass_and_order():
    left, right = (10, 10, 0, 0), (10, -10, 0, 0)
    assert invariant_mass(left, right) == pytest.approx(20)
    assert invariant_mass(right, left) == pytest.approx(20)


def test_collinear_and_spacelike():
    assert invariant_mass((10, 10, 0, 0), (10, 10, 0, 0)) == pytest.approx(0)
    with pytest.raises(ValueError, match="spacelike"):
        invariant_mass((1, 2, 0, 0))


@pytest.mark.parametrize("process,count,seed", [("bad", 1, 42), ("soft", 0, 42), ("soft", 1, 0)])
def test_bad_settings(process, count, seed):
    with pytest.raises(ValueError):
        generate(process, count, seed)


def test_soft_events_repeat_with_fixed_seed():
    first = generate("soft", 10, 42)
    assert len(first) == 10
    assert all(event for event in first)
    assert any(p.charge for event in first for p in event)
    assert all(isfinite(p.pt) and p.pt >= 0 for event in first for p in event)
    assert first == generate("soft", 10, 42)
    assert first != generate("soft", 10, 43)


def test_dimuon_sample_has_z_peak():
    events = generate("dimuon", 100)
    masses = []
    for event in events:
        negative = [p for p in event if p.pdg_id == 13]
        positive = [p for p in event if p.pdg_id == -13]
        if negative and positive:
            muons = [max(group, key=lambda p: p.pt) for group in (negative, positive)]
            masses.append(invariant_mass(*[(p.energy, p.px, p.py, p.pz) for p in muons]))
    assert len(events) == 100
    assert sum(80 <= mass <= 100 for mass in masses) > 50
