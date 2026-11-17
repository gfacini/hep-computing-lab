"""Operations on four-vectors in natural units, with components (E, px, py, pz)."""

from math import sqrt


def invariant_mass(*vectors: tuple[float, float, float, float]) -> float:
    energy, px, py, pz = map(sum, zip(*vectors, strict=True))
    momentum_squared = px**2 + py**2 + pz**2
    mass_squared = energy**2 - momentum_squared
    if mass_squared < -1e-12 * max(energy**2, momentum_squared):
        raise ValueError("The summed four-vector is spacelike.")
    return sqrt(max(0.0, mass_squared))
