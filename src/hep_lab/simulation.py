"""Generate small, unweighted teaching samples with Pythia 8."""

from dataclasses import dataclass

import pythia8mc


@dataclass(frozen=True)
class Particle:
    pdg_id: int
    charge: float
    px: float
    py: float
    pz: float
    energy: float
    pt: float
    eta: float


def generate(process: str, n_events: int, seed: int = 42) -> list[list[Particle]]:
    """Return exactly n_events successful events, containing final particles."""
    if n_events < 1:
        raise ValueError("Request at least one event.")
    if not 1 <= seed <= 900_000_000:
        raise ValueError("Choose a Pythia seed between 1 and 900000000.")

    processes = {
        "soft": ["SoftQCD:nonDiffractive = on"],
        "dimuon": [
            "WeakSingleBoson:ffbar2gmZ = on",
            "PhaseSpace:mHatMin = 60.",
            "23:onMode = off",
            "23:onIfMatch = 13 -13",
        ],
    }
    if process not in processes:
        raise ValueError(f"Unknown process: {process}")

    pythia = pythia8mc.Pythia("", False)
    for setting in [
        "Print:quiet = on",
        "Beams:idA = 2212",
        "Beams:idB = 2212",
        "Beams:eCM = 13000.",
        "Random:setSeed = on",
        f"Random:seed = {seed}",
        *processes[process],
    ]:
        if not pythia.readString(setting):
            raise RuntimeError(f"Pythia rejected {setting!r}")
    if not pythia.init():
        raise RuntimeError("Pythia could not initialize. Check the XML data path.")

    events = []
    for _ in range(n_events + 10):
        if not pythia.next():
            continue
        # Copy values now. The next event replaces the C++ event record.
        events.append([
            Particle(p.id(), p.charge(), p.px(), p.py(), p.pz(), p.e(), p.pT(), p.eta())
            for p in pythia.event if p.isFinal()
        ])
        if len(events) == n_events:
            return events
    raise RuntimeError(f"Generated only {len(events)} of {n_events} requested events.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--process", choices=["soft", "dimuon"], default="soft")
    parser.add_argument("--events", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    sample = generate(args.process, args.events, args.seed)
    print(f"{len(sample)} events, {sum(map(len, sample))} final particles")
