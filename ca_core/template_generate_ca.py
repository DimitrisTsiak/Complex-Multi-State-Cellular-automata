"""Loop N: <domain focus>

Template for generations/loop_N/generate_ca.py. Copy it, replace the example rules
with the 10 rules from rules.md (same order), then run from the repository root:

    python -m ca_core run generations/loop_N

The shared engine (ca_core) does the initial conditions, seeding, simulation, PNG
rendering, file naming and the triage gate. Do not write simulation loops, file I/O
or image code here: only declare RULES.

Each rule is a ca_core.Rule:
    step(S, rng, t) -> next S
        S is one row: a 1-D integer array of `width` cells (default 800) with values
        in 0..n_states-1. Boundaries are periodic, so use np.roll. Return a NEW integer
        array. Use `rng` (numpy Generator: rng.random(n), rng.integers(lo, hi, n)) for
        ALL randomness, never np.random.*, so every image is reproducible.
        t is the time step, for rules that need it.
    palette     exactly n_states distinct RGB triples; the index is the state.
    seed_state  centre-cell value for the default single_seed start (default 1).
    init(init_type, width, rng) -> state     optional custom start; return None to keep
                the default for that init_type ("single_seed" or "random").
    view(state) -> row                       optional; needed when the state carries
                hidden channels (example 3).
"""
import numpy as np

from ca_core import Rule


def count_neighbours(S, value, offsets):
    """Per cell: how many of the cells at `offsets` (e.g. (-2, -1, 1, 2)) are in `value`."""
    return sum((np.roll(S, -d) == value).astype(np.int32) for d in offsets)


# -- Example 1: deterministic, totalistic lookup table (Wolfram code 1599, 3 states) -----
TOTALISTIC_1599 = np.array([0, 2, 0, 2, 1, 0, 2])  # new state indexed by L + C + R


def totalistic_step(S, rng, t):
    return TOTALISTIC_1599[np.roll(S, 1) + S + np.roll(S, -1)]


# -- Example 2: stochastic excitable medium (0 rest, 1 firing, 2..7 refractory) ----------
FIRE_P, SPONTANEOUS_P = 0.55, 2e-4


def noisy_excitable_step(S, rng, t):
    firing_neighbours = count_neighbours(S, 1, (-2, -1, 1, 2))
    p_fire = 1.0 - (1.0 - FIRE_P) ** firing_neighbours
    ignite = (S == 0) & ((rng.random(S.size) < p_fire) | (rng.random(S.size) < SPONTANEOUS_P))
    return np.where(S == 0, ignite.astype(S.dtype), (S + 1) % 8)


# -- Example 3: hidden channel, second-order reversible rule (Wolfram's ECA 150R) --------
# The state is (previous row, current row) of 0/1 cells:
#     next = ECA150(left, centre, right) XOR previous
# `view` shows both channels at once as 4 colours: 2 * previous + current.
ECA_150 = np.array([(150 >> i) & 1 for i in range(8)])  # new cell indexed by 4L + 2C + R


def reversible_init(init_type, width, rng):
    current = np.zeros(width, dtype=np.int32)
    if init_type == "single_seed":
        current[width // 2] = 1
    else:
        current = rng.integers(0, 2, size=width, dtype=np.int32)
    return (np.zeros(width, dtype=np.int32), current)


def reversible_step(state, rng, t):
    previous, current = state
    following = ECA_150[4 * np.roll(current, 1) + 2 * current + np.roll(current, -1)] ^ previous
    return (current, following)


RULES = [
    Rule(
        name="Totalistic Code 1599",
        n_states=3,
        step=totalistic_step,
        palette=[(12, 12, 30), (255, 196, 0), (0, 190, 255)],
    ),
    Rule(
        name="Noisy Excitable Medium",
        n_states=8,
        step=noisy_excitable_step,
        palette=[(8, 10, 24), (255, 255, 210), (255, 90, 40), (230, 40, 90),
                 (170, 20, 140), (110, 20, 160), (60, 20, 120), (30, 15, 70)],
    ),
    Rule(
        name="Reversible ECA 150R",
        n_states=4,
        step=reversible_step,
        init=reversible_init,
        view=lambda state: 2 * state[0] + state[1],
        palette=[(10, 14, 30), (0, 220, 170), (240, 60, 110), (255, 235, 150)],
    ),
]
