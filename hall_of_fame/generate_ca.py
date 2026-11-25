"""Hall of fame: the 30 showcase picks, ported to the shared engine.

Each rule is copied from its original script (generations/loop_N/generate_ca.py) with
the same dynamics, starting rows, data types and colours. The one change: randomness
comes from the engine's seeded `rng` instead of np.random, so every image here can be
regenerated exactly:

    python -m ca_core run hall_of_fame

RULES follows the order of gif_showcase.py and showcase/. Each Rule's description names
the start that was picked for the showcase. README.md lists which picks reproduce the
showcase image pixel for pixel; the others had unseeded randomness, so they come out
as new images of the same rule.
"""
import numpy as np

from ca_core import Rule


def centre_seed(value, dtype=np.int32):
    """Single-seed start: one cell of `value` in the centre of a 0 background."""
    def make(width):
        row = np.zeros(width, dtype=dtype)
        row[width // 2] = value
        return row
    return make


# =====================================================================================
# Loop 1: Multi-state Cyclic & Excitable Media
# =====================================================================================

# -- Loop 1, Rule 4: Staged Excitation Cascade -----------------------------------------
# 0 quiescent, 1-2 excited, 3-7 refractory; inner r=1 and outer r=3 neighbourhoods.
def l01_r04_step(arr, rng, t):
    E = ((arr == 1) | (arr == 2)).astype(int)
    sum_in = np.roll(E, 1) + np.roll(E, -1)
    sum_out = np.roll(E, 3) + np.roll(E, 2) + np.roll(E, -2) + np.roll(E, -3)

    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    excite = (sum_in >= 1) | (sum_out >= 1)
    new_arr[mask_zero] = np.where(excite[mask_zero], 1, 0)

    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 8
    return new_arr


L01_R04 = Rule(
    name="Loop 1 Rule 4: Staged Excitation Cascade",
    n_states=8,
    step=l01_r04_step,
    palette=[(10, 5, 5), (255, 255, 255), (255, 230, 0), (255, 140, 0),
             (230, 50, 0), (160, 0, 80), (90, 0, 120), (30, 0, 60)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 2: Multi-state Generations & Outer-Totalistic
# Original starts: single seed = state 1 in the centre; random = 70% state 0,
# 15% state 1, the remaining 15% spread evenly over the decay states. Cells are uint8.
# =====================================================================================

def loop2_init(n_states):
    def init(init_type, width, rng):
        if init_type == "single_seed":
            return centre_seed(1, np.uint8)(width)
        p = np.zeros(n_states)
        p[0], p[1] = 0.70, 0.15
        p[2:] = 0.15 / (n_states - 2)
        return rng.choice(n_states, size=width, p=p).astype(np.uint8)
    return init


# -- Loop 2, Rule 2: Parity-Gated Birth Generations ------------------------------------
def l02_r02_step(S, rng, t):
    is_active = (S == 1).astype(np.int8)
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    next_S = np.zeros_like(S)
    birth = (S == 0) & ((A == 1) | (A == 3))  # birth on 1 or 3 active neighbours
    next_S[birth] = 1
    survival = (S == 1) & ((A == 1) | (A == 2))
    next_S[survival] = 1
    decay_start = (S == 1) & ~((A == 1) | (A == 2))
    next_S[decay_start] = 2
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    return next_S


L02_R02 = Rule(
    name="Loop 2 Rule 2: Parity-Gated Birth Generations",
    n_states=5,
    step=l02_r02_step,
    init=loop2_init(5),
    palette=[(15, 10, 15), (255, 220, 0), (255, 100, 0), (220, 20, 60), (100, 0, 50)],
    description="Showcase pick: random start.",
)


# -- Loop 2, Rule 4: Chiral Drifting Generations ---------------------------------------
def l02_r04_step(S, rng, t):
    is_active = (S == 1).astype(np.int8)
    # weighted, left-heavy neighbourhood: W(x) = S(x-3) + S(x-2) + 2*S(x-1) + S(x+1)
    W = np.roll(is_active, 3) + np.roll(is_active, 2) + 2 * np.roll(is_active, 1) + np.roll(is_active, -1)
    next_S = np.zeros_like(S)
    birth = (S == 0) & ((W == 2) | (W == 3))
    next_S[birth] = 1
    survival = (S == 1) & ((W >= 1) & (W <= 3))
    next_S[survival] = 1
    decay_start = (S == 1) & ~((W >= 1) & (W <= 3))
    next_S[decay_start] = 2
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 4
    return next_S


L02_R04 = Rule(
    name="Loop 2 Rule 4: Chiral Drifting Generations",
    n_states=4,
    step=l02_r04_step,
    init=loop2_init(4),
    palette=[(15, 5, 20), (255, 50, 255), (150, 0, 200), (70, 0, 120)],
    description="Showcase pick: random start.",
)


# -- Loop 2, Rule 7: Totalistic-Sum Generations ----------------------------------------
def l02_r07_step(S, rng, t):
    K = np.roll(S, 2) + np.roll(S, 1) + S + np.roll(S, -1) + np.roll(S, -2)  # sum of states, r=2
    next_S = np.zeros_like(S)
    birth = (S == 0) & (K >= 3) & (K <= 6)
    next_S[birth] = 1
    survival = (S == 1) & (K >= 4) & (K <= 7)
    next_S[survival] = 1
    decay_start = (S == 1) & ~((K >= 4) & (K <= 7))
    next_S[decay_start] = 2
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    return next_S


L02_R07 = Rule(
    name="Loop 2 Rule 7: Totalistic-Sum Generations",
    n_states=5,
    step=l02_r07_step,
    init=loop2_init(5),
    palette=[(10, 10, 10), (255, 255, 255), (191, 255, 0), (34, 139, 34), (0, 80, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 3: Reaction-Diffusion & Chemical Waves
# =====================================================================================

# -- Loop 3, Rule 8: Anomalous Fractional Diffusion Wave -------------------------------
# Colours: matplotlib "rainbow" sampled at state / 6, as the original rendered them.
def l03_r08_step(S, rng, t):
    mask_active = (S >= 1)
    C_1 = np.roll(mask_active.astype(np.int32), 1) + np.roll(mask_active.astype(np.int32), -1)
    C_3 = np.roll(mask_active.astype(np.int32), 3) + np.roll(mask_active.astype(np.int32), -3)
    D = 2 * C_1 + C_3

    S_next = np.zeros_like(S)
    cond1 = (S == 0) & ((D == 2) | (D == 3))
    cond2 = (S >= 1) & (S < 4)
    cond3 = (S >= 4)
    S_next[cond1] = 1
    S_next[cond2] = S[cond2] + 1
    S_next[cond3] = (S[cond3] + 1) % 7
    return S_next


def l03_r08_init(init_type, width, rng):
    if init_type == "single_seed":
        return centre_seed(1, np.uint8)(width)
    return rng.integers(0, 7, size=width, dtype=np.uint8)


L03_R08 = Rule(
    name="Loop 3 Rule 8: Anomalous Fractional Diffusion Wave",
    n_states=7,
    step=l03_r08_step,
    init=l03_r08_init,
    palette=[(127, 0, 255), (43, 126, 246), (42, 220, 220), (128, 254, 179),
             (212, 220, 127), (255, 126, 65), (255, 0, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 6: Fluid & Convective Systems
# =====================================================================================

# -- Loop 6, Rule 1: Clamped Advection-Diffusion ---------------------------------------
def l06_r01_step(S, rng, t):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    sgn = np.sign(S_right - S_left).astype(int)
    return np.clip(S_left + sgn, 0, 7)


L06_R01 = Rule(
    name="Loop 6 Rule 1: Clamped Advection-Diffusion",
    n_states=8,
    step=l06_r01_step,
    seed_state=7,  # the original seeded the top state, N - 1
    palette=[(15, 15, 35), (30, 80, 150), (40, 150, 180), (50, 180, 120),
             (100, 200, 80), (220, 200, 50), (240, 120, 30), (255, 30, 30)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 8: Quantum-Walk & Wave Interference
# Cells are int8. Random starts are mostly vacuum (state 0) with rule-specific odds.
# =====================================================================================

def loop8_init(single_seed, probs):
    def init(init_type, width, rng):
        if init_type == "single_seed":
            return single_seed(width)
        return rng.choice(np.arange(len(probs)), size=width, p=probs).astype(np.int8)
    return init


# -- Loop 8, Rule 1: Discrete Hadamard Walk --------------------------------------------
# Each cell holds a right- and a left-moving amplitude in {-1, 0, +1}; states 1-8 encode
# the eight non-vacuum combinations.
def l08_r01_step(S, rng, t):
    W = S.size
    psi_R = np.zeros(W, dtype=np.int8)
    psi_L = np.zeros(W, dtype=np.int8)

    psi_R[S == 1] = 1
    psi_R[S == 3] = -1
    psi_R[S == 5] = 1
    psi_R[S == 6] = -1
    psi_R[S == 7] = 1
    psi_R[S == 8] = -1

    psi_L[S == 2] = 1
    psi_L[S == 4] = -1
    psi_L[S == 5] = 1
    psi_L[S == 6] = -1
    psi_L[S == 7] = -1
    psi_L[S == 8] = 1

    a = np.roll(psi_R, 1)
    b = np.roll(psi_L, -1)

    R_new = np.sign(a + b)
    L_new = np.sign(a - b)

    S_new = np.zeros(W, dtype=np.int8)
    S_new[(R_new == 1) & (L_new == 0)] = 1
    S_new[(R_new == 0) & (L_new == 1)] = 2
    S_new[(R_new == -1) & (L_new == 0)] = 3
    S_new[(R_new == 0) & (L_new == -1)] = 4
    S_new[(R_new == 1) & (L_new == 1)] = 5
    S_new[(R_new == -1) & (L_new == -1)] = 6
    S_new[(R_new == 1) & (L_new == -1)] = 7
    S_new[(R_new == -1) & (L_new == 1)] = 8
    return S_new


L08_R01 = Rule(
    name="Loop 8 Rule 1: Discrete Hadamard Walk",
    n_states=9,
    step=l08_r01_step,
    init=loop8_init(centre_seed(5, np.int8), [0.85] + [0.15 / 8] * 8),
    palette=[(10, 10, 20), (0, 220, 255), (255, 0, 128), (0, 100, 255), (255, 0, 0),
             (255, 200, 0), (128, 0, 255), (0, 255, 128), (255, 128, 0)],
    description="Showcase pick: random start.",
)


# -- Loop 8, Rule 2: Quantum Tunneling & Scattering ------------------------------------
# States 5 (barrier) and 6 (wall) are static and scatter the moving amplitudes.
def l08_r02_step(S, rng, t):
    W = S.size
    psi_R = np.zeros(W, dtype=np.int8)
    psi_R[(S == 1) | (S == 7)] = 1
    psi_R[S == 3] = -1

    psi_L = np.zeros(W, dtype=np.int8)
    psi_L[(S == 2) | (S == 7)] = 1
    psi_L[S == 4] = -1

    S_left = np.roll(S, 1)
    cond_6 = (S_left == 6)
    cond_5 = (S_left == 5)
    cond_other = ~(cond_6 | cond_5)

    a = np.zeros(W, dtype=np.int8)
    a[cond_6] = -psi_L[cond_6]
    a[cond_5] = np.roll(psi_R, 2)[cond_5] - psi_L[cond_5]
    a[cond_other] = np.roll(psi_R, 1)[cond_other]

    S_right = np.roll(S, -1)
    cond_6_b = (S_right == 6)
    cond_5_b = (S_right == 5)
    cond_other_b = ~(cond_6_b | cond_5_b)

    b = np.zeros(W, dtype=np.int8)
    b[cond_6_b] = -psi_R[cond_6_b]
    b[cond_5_b] = np.roll(psi_L, -2)[cond_5_b] - psi_R[cond_5_b]
    b[cond_other_b] = np.roll(psi_L, -1)[cond_other_b]

    a_prime = np.clip(a, -1, 1)
    b_prime = np.clip(b, -1, 1)

    S_new = np.zeros(W, dtype=np.int8)
    static_mask = (S == 5) | (S == 6)
    S_new[static_mask] = S[static_mask]

    non_static = ~static_mask
    S_ns = np.zeros(W, dtype=np.int8)
    S_ns[(a_prime == 1) & (b_prime == 0)] = 1
    S_ns[(a_prime == -1) & (b_prime == 0)] = 3
    S_ns[(a_prime == 0) & (b_prime == 1)] = 2
    S_ns[(a_prime == 0) & (b_prime == -1)] = 4
    S_ns[(a_prime == 1) & (b_prime == 1)] = 7

    S_new[non_static] = S_ns[non_static]
    return S_new


def l08_r02_single_seed(width):
    S = np.zeros(width, dtype=np.int8)
    S[width // 4] = 1
    S[width // 2 - 1: width // 2 + 2] = 5
    S[3 * width // 4 - 1: 3 * width // 4 + 2] = 6
    return S


L08_R02 = Rule(
    name="Loop 8 Rule 2: Quantum Tunneling & Scattering",
    n_states=8,
    step=l08_r02_step,
    init=loop8_init(l08_r02_single_seed, [0.80, 0.08, 0.02, 0.02, 0.02, 0.03, 0.02, 0.01]),
    palette=[(15, 10, 15), (0, 255, 100), (0, 150, 255), (100, 255, 0), (0, 50, 200),
             (120, 120, 120), (220, 220, 220), (255, 255, 0)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 9: Social Segregation & Game Theory
# =====================================================================================

# -- Loop 9, Rule 8: Class Struggle and Elite Overproduction ---------------------------
# 0-3 social classes, 4 revolutionary, 5 revolution. Cells are uint8.
def l09_r08_step(S, rng, t):
    S_l2 = np.roll(S, 2)
    S_l1 = np.roll(S, 1)
    S_r1 = np.roll(S, -1)
    S_r2 = np.roll(S, -2)

    E = (S_l2 == 4).astype(int) + (S_l1 == 4).astype(int) + (S_r1 == 4).astype(int) + (S_r2 == 4).astype(int)
    R = (S_l2 == 5).astype(int) + (S_l1 == 5).astype(int) + (S_r1 == 5).astype(int) + (S_r2 == 5).astype(int)
    W_index = S_l2 + S_l1 + S_r1 + S_r2

    S_next = np.zeros_like(S)

    mask4 = (S == 4)
    S_next[mask4] = np.where(E[mask4] >= 3, 5, np.where(W_index[mask4] < 4, 3, 4))

    mask5 = (S == 5)
    S_next[mask5] = 1

    mask03 = np.isin(S, [0, 1, 2, 3])
    cond_rev = (R >= 1)
    res_rev = np.where(S == 3, 0, 1)

    cond_mobility = (W_index >= 2 * S + 2)
    cond_decline = (W_index < S)
    res_no_rev = np.where(cond_mobility, S + 1, np.where(cond_decline, np.maximum(0, S - 1), S))

    S_next[mask03] = np.where(cond_rev[mask03], res_rev[mask03], res_no_rev[mask03])
    return S_next


def l09_r08_init(init_type, width, rng):
    if init_type == "single_seed":
        return centre_seed(4, np.uint8)(width)
    return rng.integers(0, 6, size=width).astype(np.uint8)


L09_R08 = Rule(
    name="Loop 9 Rule 8: Class Struggle and Elite Overproduction",
    n_states=6,
    step=l09_r08_step,
    init=l09_r08_init,
    palette=[(15, 10, 20), (139, 69, 19), (218, 165, 32), (0, 128, 128), (255, 255, 255), (255, 0, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 10: Cryptographic Scramblers & Chaotic Maps
# =====================================================================================

# -- Loop 10, Rule 8: Arnold's Cat Map Lattice -----------------------------------------
# 16 states = a pair (X, Y) in Z4 x Z4, mixed with the neighbours like a discrete cat map.
def l10_r08_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    X = arr % 4
    Y = arr // 4
    X_new = (X + Y + left) % 4
    Y_new = (X + 2 * Y + right) % 4
    return X_new + 4 * Y_new


L10_R08 = Rule(
    name="Loop 10 Rule 8: Arnold's Cat Map Lattice",
    n_states=16,
    step=l10_r08_step,
    palette=[(5, 5, 30), (37, 3, 90), (70, 2, 150), (102, 1, 210), (135, 1, 247), (169, 6, 219),
             (203, 12, 190), (237, 17, 161), (255, 34, 127), (255, 62, 88), (255, 91, 49),
             (255, 119, 9), (255, 152, 30), (255, 186, 70), (255, 220, 110), (255, 255, 150)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 11: Stochastic Behaviors & Markovian Processes
# =====================================================================================

# -- Loop 11, Rule 3: Directed Percolation (Branching Organic Dendrites) ---------------
# An active cell activates each neighbour independently with probability 0.65.
def l11_r03_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    r_left = rng.random(arr.shape) < 0.65
    r_right = rng.random(arr.shape) < 0.65
    prop = (left == 1) & r_left | (right == 1) & r_right
    return prop.astype(np.int32)


L11_R03 = Rule(
    name="Loop 11 Rule 3: Directed Percolation",
    n_states=2,
    step=l11_r03_step,
    palette=[(5, 5, 25), (0, 191, 255)],
    description="Showcase pick: random start.",
)


# -- Loop 11, Rule 5: Noisy Majority (Cyan-White Digital Rain) -------------------------
# Majority of (left, self, right); with probability 0.05 a cell takes a random state.
def l11_r05_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    stacked = np.stack([left, arr, right], axis=0)
    maj = np.zeros_like(arr)
    for i in range(3):
        c = np.sum(stacked == i, axis=0)
        maj = np.where(c >= 2, i, maj)
    r = rng.random(arr.shape)
    return np.where(r < 0.95, maj, rng.integers(0, 3, size=arr.shape))


L11_R05 = Rule(
    name="Loop 11 Rule 5: Noisy Majority",
    n_states=3,
    step=l11_r05_step,
    palette=[(10, 15, 20), (0, 255, 255), (255, 255, 255)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 12: Classical General Relativity
# =====================================================================================

# -- Loop 12, Rule 2: Gravitational Wave Interferometer --------------------------------
# Second-order wave equation mod 3, packed into one state: S = u_now + 3 * u_previous
# (states 0-8). State 9 is a static lens; two lenses sit at 1/4 and 3/4 of the row.
def l12_r02_step(S, rng, t):
    mask_9 = (S == 9)
    u_curr = S % 3
    u_prev = S // 3
    W = np.where(S < 9, u_curr, 0)
    u_next = (np.roll(W, 1) + np.roll(W, -1) - u_prev + 3) % 3
    S_next = u_next + 3 * u_curr
    S_next[mask_9] = 9
    return S_next


def l12_r02_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.zeros(width, dtype=np.int32)
        S[width // 2 - 5: width // 2 + 6] = 1  # a wave packet: u_now = 1, u_previous = 0
    else:
        S = rng.integers(0, 9, size=width, dtype=np.int32)
        S[rng.random(width) < 0.05] = 9  # extra random lenses
    for lens in (width // 4, 3 * width // 4):
        S[lens] = 9
    return S


L12_R02 = Rule(
    name="Loop 12 Rule 2: Gravitational Wave Interferometer",
    n_states=10,
    step=l12_r02_step,
    init=l12_r02_init,
    palette=[(15, 15, 25), (0, 80, 100), (0, 180, 140), (40, 30, 90), (120, 40, 180),
             (220, 60, 200), (180, 80, 0), (240, 150, 0), (255, 220, 50), (255, 255, 255)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 12, Rule 4: Gravitational Redshift (Time Dilation) ---------------------------
# S = P + 2 * Phi: a signal bit P drifting right, slowed by a static potential Phi in 0..3
# (it moves with probability 1 - Phi / 4).
def l12_r04_step(S, rng, t):
    P = S % 2
    Phi = S // 2
    P_update = 1.0 - 0.25 * Phi
    r = rng.random(S.size)
    P_next = np.copy(P)
    update_mask = (r < P_update)
    P_next[update_mask] = np.roll(P, 1)[update_mask]
    return P_next + 2 * Phi


def l12_r04_init(init_type, width, rng):
    if init_type == "single_seed":
        P = (np.arange(width) % 20 < 5).astype(np.int32)  # a regular pulse train
        Phi = np.zeros(width, dtype=np.int32)
        Phi[width // 3: width // 3 + 40] = 3  # two potential wells
        Phi[2 * width // 3: 2 * width // 3 + 40] = 3
    else:
        P = (rng.random(width) < 0.50).astype(np.int32)
        Phi = rng.integers(0, 4, size=width, dtype=np.int32)
    return P + 2 * Phi


L12_R04 = Rule(
    name="Loop 12 Rule 4: Gravitational Redshift (Time Dilation)",
    n_states=8,
    step=l12_r04_step,
    init=l12_r04_init,
    palette=[(10, 10, 12), (50, 255, 100), (10, 50, 60), (0, 230, 230),
             (15, 30, 90), (50, 120, 255), (50, 15, 80), (255, 50, 150)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 13: Loop Quantum Gravity
# Single seed = the top state (N - 1) in the centre.
# =====================================================================================

# -- Loop 13, Rule 4: Spinfoam Amplitude Sum-Over-Histories ----------------------------
def l13_r04_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    parity = (left + arr + right) % 2
    constructive = (left + right) % 6
    return np.where(parity == 0, constructive, 0)


L13_R04 = Rule(
    name="Loop 13 Rule 4: Spinfoam Amplitude Sum-Over-Histories",
    n_states=6,
    step=l13_r04_step,
    seed_state=5,
    palette=[(5, 0, 10), (78, 0, 80), (153, 4, 131), (229, 16, 143), (255, 98, 88), (255, 215, 0)],
    description="Showcase pick: random start.",
)


# -- Loop 13, Rule 10: Chiral Immirzi Asymmetry ----------------------------------------
def l13_r10_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)

    mask_weak = (arr == 1) | (arr == 3)  # weak chiral states
    weak_val = np.where(right > left, right, left)

    mask_strong = (arr == 2) | (arr == 4)  # strong chiral states
    strong_val = (arr + left - 2 * right + 5) % 5

    mask_neutral = (arr == 0)
    neutral_val = np.zeros_like(arr)
    neutral_val = np.where((left > right) & (left > 0), 1, neutral_val)
    neutral_val = np.where((right > left) & (right > 0), 3, neutral_val)

    new_arr = np.zeros_like(arr)
    new_arr = np.where(mask_weak, weak_val, new_arr)
    new_arr = np.where(mask_strong, strong_val, new_arr)
    new_arr = np.where(mask_neutral, neutral_val, new_arr)
    return new_arr


L13_R10 = Rule(
    name="Loop 13 Rule 10: Chiral Immirzi Asymmetry",
    n_states=5,
    step=l13_r10_step,
    seed_state=4,
    palette=[(20, 20, 20), (0, 191, 255), (0, 0, 255), (255, 99, 71), (255, 0, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 14: String Theory
# =====================================================================================

# -- Loop 14, Rule 3: Calabi-Yau Dimension Compactification ----------------------------
# 12 states = an "energy" e in 0..3 times an "internal" i in 0..2 (state = 3e + i).
def l14_r03_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)

    e_L, i_L = left // 3, left % 3
    e_x, i_x = arr // 3, arr % 3
    e_R, i_R = right // 3, right % 3

    i_next = (i_L + i_x + i_R) % 3

    e_next_0 = (e_L + e_R) % 4

    e_next_1 = np.zeros_like(arr)
    cond_ex_not_0 = (e_x != 0)
    e_next_1[cond_ex_not_0] = (e_x[cond_ex_not_0] + 1) % 4
    cond_ex_0_trigger = (e_x == 0) & ((e_L == 1) | (e_R == 1))
    e_next_1[cond_ex_0_trigger] = 1

    e_next_2 = (e_x**2 + e_L * e_R) % 4

    e_next = np.zeros_like(arr)
    e_next = np.where(i_next == 0, e_next_0, e_next)
    e_next = np.where(i_next == 1, e_next_1, e_next)
    e_next = np.where(i_next == 2, e_next_2, e_next)
    return 3 * e_next + i_next


def l14_r03_init(init_type, width, rng):
    if init_type == "single_seed":
        row = np.zeros(width, dtype=np.int32)
        row[width // 2 - 10] = 5
        row[width // 2] = 11
        row[width // 2 + 10] = 8
        return row
    return None  # default: uniform over all 12 states


L14_R03 = Rule(
    name="Loop 14 Rule 3: Calabi-Yau Dimension Compactification",
    n_states=12,
    step=l14_r03_step,
    init=l14_r03_init,
    palette=[(10, 15, 25), (75, 0, 130), (128, 0, 128), (0, 0, 139), (0, 0, 255), (30, 144, 255),
             (0, 128, 128), (0, 128, 0), (154, 205, 50), (255, 255, 0), (255, 165, 0), (255, 0, 0)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 14, Rule 7: Holographic Boundary-to-Bulk Projection (AdS/CFT) ----------------
# Even sites follow a "boundary" law, odd sites a "bulk" law.
def l14_r07_step(arr, rng, t):
    left2 = np.roll(arr, 2)
    left1 = np.roll(arr, 1)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)

    val_boundary = (3 * arr + left2 * right2) % 10
    val_bulk = (left1 + right1 + left2 + right2) % 10

    is_even = (np.arange(len(arr)) % 2 == 0)
    return np.where(is_even, val_boundary, val_bulk)


def l14_r07_init(init_type, width, rng):
    if init_type == "single_seed":
        row = np.zeros(width, dtype=np.int32)
        row[width // 2] = 9
        row[width // 2 - 20] = 7
        row[width // 2 + 20] = 8
        return row
    return None


L14_R07 = Rule(
    name="Loop 14 Rule 7: Holographic Boundary-to-Bulk Projection (AdS/CFT)",
    n_states=10,
    step=l14_r07_step,
    init=l14_r07_init,
    palette=[(15, 15, 15), (32, 178, 170), (0, 139, 139), (144, 238, 144), (50, 205, 50),
             (34, 139, 34), (255, 165, 0), (255, 127, 80), (255, 99, 71), (255, 215, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 15: Extraterrestrial Life
# =====================================================================================

# -- Loop 15, Rule 9: Quantum-Coherent Extremophile ------------------------------------
def l15_r09_step(arr, rng, t):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)

    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_4 = (arr == 4)

    new_arr[is_4] = 1

    cond_2_1 = is_2 & (((left == 1) & (right != 1)) | ((right == 1) & (left != 1)))
    cond_2_0 = is_2 & ~cond_2_1 & ((left == 3) | (right == 3))
    cond_2_2 = is_2 & ~cond_2_1 & ~cond_2_0
    new_arr[cond_2_1] = 1
    new_arr[cond_2_2] = 2

    cond_1_0 = is_1 & ((left == 3) | (right == 3))
    new_arr[is_1 & ~cond_1_0] = 2

    cond_0_1 = is_0 & (((left == 1) & (right == 2)) | ((left == 2) & (right == 1)))
    cond_0_4 = is_0 & ~cond_0_1 & ((left == 3) | (right == 3))
    new_arr[cond_0_1] = 1
    new_arr[cond_0_4] = 4
    return new_arr


L15_R09 = Rule(
    name="Loop 15 Rule 9: Quantum-Coherent Extremophile",
    n_states=5,
    step=l15_r09_step,
    seed_state=3,
    palette=[(10, 10, 35), (0, 255, 204), (75, 0, 130), (255, 69, 0), (230, 230, 250)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 17: Parasitic Memetic Infections & Mind Control
# =====================================================================================

# -- Loop 17, Rule 9: Symbiotic Subversion (Mutualistic Hijacking) ---------------------
# Cells are uint8. The original placed its seeds at fixed positions on an 800-cell row;
# here they scale with the width (identical at 800).
def l17_r09_step(S, rng, t):
    S_left1 = np.roll(S, 1)
    S_left2 = np.roll(S, 2)
    S_right1 = np.roll(S, -1)
    S_right2 = np.roll(S, -2)

    N_S = ((S_left1 == 1).astype(int) + (S_left2 == 1).astype(int) +
           (S_right1 == 1).astype(int) + (S_right2 == 1).astype(int))
    N_P = ((S_left1 == 2).astype(int) + (S_left2 == 2).astype(int) +
           (S_right1 == 2).astype(int) + (S_right2 == 2).astype(int))

    S_next = np.copy(S)

    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where((N_S >= 1) & (N_P == 0), 1, val_for_0)
    val_for_0 = np.where((N_P >= 2) & (N_S < 1), 2, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]

    mask_1 = (S == 1)
    S_next[mask_1] = np.where(N_S[mask_1] >= 3, 3, 1)
    mask_2 = (S == 2)
    S_next[mask_2] = np.where(N_S[mask_2] >= 2, 1, 5)
    mask_3 = (S == 3)
    S_next[mask_3] = 4
    mask_4 = (S == 4)
    S_next[mask_4] = 5
    mask_5 = (S == 5)
    S_next[mask_5] = np.where(N_S[mask_5] >= 1, 0, 5)
    return S_next


def l17_r09_init(init_type, width, rng):
    if init_type == "random":
        return rng.choice([0, 1, 2, 3, 4, 5], size=width, p=[0.85, 0.10, 0.05, 0.0, 0.0, 0.0]).astype(np.uint8)
    at = lambda x: x * width // 800  # noqa: E731 - position on the original 800-cell row
    grid = np.zeros(width, dtype=np.uint8)
    grid[at(199):at(199) + 3] = 1
    grid[at(398):at(398) + 5] = 1
    grid[at(596):at(596) + 9] = 1
    grid[at(100)] = 2
    grid[at(700)] = 2
    return grid


L17_R09 = Rule(
    name="Loop 17 Rule 9: Symbiotic Subversion (Mutualistic Hijacking)",
    n_states=6,
    step=l17_r09_step,
    init=l17_r09_init,
    palette=[(28, 40, 51), (51, 204, 255), (204, 51, 255), (204, 255, 51), (255, 153, 51), (15, 15, 15)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 20: Non-Euclidean Wormholes & Spatial Folding
# The original used per-cell Python loops; these are the same rules, vectorised.
# =====================================================================================

# -- Loop 20, Rule 5: Non-Euclidean Thermal Wormhole -----------------------------------
# Totalistic sum mod 12, except that the hottest cell (first maximum) and the coldest
# cell (last minimum) swap their own value in the sum: a wormhole between them.
def l20_r05_step(grid, rng, t):
    x_max = np.flatnonzero(grid == grid.max())[0]
    x_min = np.flatnonzero(grid == grid.min())[-1]
    middle = grid.copy()
    middle[x_max] = grid[x_min]
    middle[x_min] = grid[x_max]
    return (np.roll(grid, 1) + middle + np.roll(grid, -1)) % 12


def l20_r05_init(init_type, width, rng):
    if init_type == "single_seed":
        grid = np.zeros(width, dtype=np.int32)
        grid[width // 2 - 5: width // 2 + 5] = 11  # a heat spike
        return grid
    p = [0.2, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1]
    return rng.choice(12, size=width, p=p)


L20_R05 = Rule(
    name="Loop 20 Rule 5: Non-Euclidean Thermal Wormhole",
    n_states=12,
    step=l20_r05_step,
    init=l20_r05_init,
    palette=[(10, 10, 26), (24, 30, 64), (38, 50, 102), (52, 70, 140), (66, 90, 178), (80, 110, 216),
             (94, 130, 254), (130, 100, 220), (180, 60, 160), (220, 40, 100), (250, 90, 40), (255, 220, 100)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 20, Rule 6: Möbius Boundary Twist --------------------------------------------
# next = (left * self + self * right + 1) mod 6, where a neighbour seen across the wrap-around
# edge is shifted by 3 (a half twist, as on a Möbius strip).
def l20_r06_step(grid, rng, t):
    left = np.roll(grid, 1)
    right = np.roll(grid, -1)
    left[0] = (grid[-1] + 3) % 6
    right[-1] = (grid[0] + 3) % 6
    return (left * grid + grid * right + 1) % 6


def l20_r06_init(init_type, width, rng):
    if init_type == "single_seed":
        grid = np.zeros(width, dtype=np.int32)
        grid[width // 2] = 3
        grid[width // 2 + 1] = 4
        return grid
    return rng.choice(6, size=width, p=[0.25, 0.15, 0.15, 0.15, 0.15, 0.15])


L20_R06 = Rule(
    name="Loop 20 Rule 6: Möbius Boundary Twist",
    n_states=6,
    step=l20_r06_step,
    init=l20_r06_init,
    palette=[(20, 10, 20), (63, 81, 181), (0, 150, 136), (139, 195, 74), (255, 193, 7), (233, 30, 99)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 22: Quantum Decoherence & Wavefunction Collapse
# =====================================================================================

# -- Loop 22, Rule 7: Dissipative Decoherence in a Thermal Bath ------------------------
# 0 coherent, 1 dissipated, 2 thermal noise, 3 ground state. The spontaneous-noise rate
# theta depends on the start (0.003 single seed, 0.03 random), so the state carries it:
# state = (row, theta), and view shows the row.
L22_R07_P = dict(p_decay=0.35, p_diss=0.75, p_relax=0.12, p_drive=0.04, p_th_ex=0.22)


def l22_r07_step(state, rng, t):
    S, theta = state
    p = L22_R07_P
    width = S.size
    S_next = S.copy()
    left_S = np.roll(S, 1)
    right_S = np.roll(S, -1)

    r_noise = rng.random(width)  # spontaneous noise
    noise_mask = (S != 2) & (r_noise < theta)

    mask_2 = S == 2  # noise decays to the ground state
    r_decay = rng.random(width)
    S_next[mask_2] = np.where(r_decay[mask_2] < p["p_decay"], 3, 2)

    mask_1 = S == 1  # dissipated cells relax
    r_relax = rng.random(width)
    S_next[mask_1] = np.where(r_relax[mask_1] < p["p_relax"], 3, 1)

    mask_0 = S == 0  # coherent cells next to noise dissipate
    near_noise = (left_S == 2) | (right_S == 2)
    r_diss = rng.random(width)
    S_next[mask_0 & near_noise] = np.where(r_diss[mask_0 & near_noise] < p["p_diss"], 1, 0)

    mask_3 = S == 3  # ground state: thermal excitation or coherent drive
    if np.any(mask_3):
        r_drive = rng.random(width)
        r_ex = rng.random(width)
        th_ex_cond = mask_3 & near_noise
        S_next[th_ex_cond] = np.where(r_ex[th_ex_cond] < p["p_th_ex"], 1,
                                      np.where(r_drive[th_ex_cond] < p["p_drive"], 0, 3))
        std_drive_cond = mask_3 & ~near_noise
        S_next[std_drive_cond] = np.where(r_drive[std_drive_cond] < p["p_drive"], 0, 3)

    S_next[noise_mask] = 2
    return (S_next, theta)


def l22_r07_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.full(width, 3, dtype=np.int32)
        S[width // 2 - 150: width // 2 + 150] = 0  # a coherent region in a ground-state sea
        return (S, 0.003)
    r = rng.random(width)
    S = np.where(r < 0.4, 0, np.where(r < 0.8, 3, np.where(r < 0.9, 1, 2)))
    return (S, 0.03)


L22_R07 = Rule(
    name="Loop 22 Rule 7: Dissipative Decoherence in a Thermal Bath",
    n_states=4,
    step=l22_r07_step,
    init=l22_r07_init,
    view=lambda state: state[0],
    palette=[(0, 100, 200), (255, 50, 50), (255, 215, 0), (20, 20, 20)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 23: Evolutionary Mutational Wars & Stochastic Pathology
# Cells are uint8.
# =====================================================================================

def loop23_init(single_seed, states, probs):
    def init(init_type, width, rng):
        if init_type == "single_seed":
            return single_seed(width)
        return rng.choice(states, size=width, p=probs).astype(np.uint8)
    return init


# -- Loop 23, Rule 7: Recombination-Driven Zoonotic Spillover --------------------------
# 0 susceptible, 1 strain A, 2 strain B, 3 co-infected, 4 recombinant, 5 dead.
def l23_r07_step(S, rng, t):
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)

    N_A = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_B = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_AB = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)
    N_R = (S_L1 == 4).astype(int) + (S_R1 == 4).astype(int)

    p_A = 1.0 - 0.55**(N_A + 0.5 * N_AB)
    p_B = 1.0 - 0.55**(N_B + 0.5 * N_AB)
    p_R = 1.0 - 0.20**N_R

    expose_R = rng.random(width) < p_R
    expose_A = rng.random(width) < p_A
    expose_B = rng.random(width) < p_B

    is_zero = (S == 0)
    S_next[is_zero & expose_R] = 4
    S_next[is_zero & ~expose_R & (expose_A & expose_B)] = 3
    S_next[is_zero & ~expose_R & (expose_A & ~expose_B)] = 1
    S_next[is_zero & ~expose_R & (expose_B & ~expose_A)] = 2

    is_one = (S == 1)
    p_super_B = 1.0 - 0.55**(N_B + 0.5 * N_AB)
    super_B = rng.random(width) < p_super_B
    recovery_1 = ~super_B & (rng.random(width) < 0.20)
    S_next[is_one & super_B] = 3
    S_next[is_one & recovery_1] = 0

    is_two = (S == 2)
    p_super_A = 1.0 - 0.55**(N_A + 0.5 * N_AB)
    super_A = rng.random(width) < p_super_A
    recovery_2 = ~super_A & (rng.random(width) < 0.20)
    S_next[is_two & super_A] = 3
    S_next[is_two & recovery_2] = 0

    is_three = (S == 3)
    r_3 = rng.random(width)
    S_next[is_three & (r_3 < 0.25)] = 4
    S_next[is_three & (r_3 >= 0.25) & (r_3 < 0.35)] = 0

    is_four = (S == 4)
    r_4 = rng.random(width)
    S_next[is_four & (r_4 < 0.40)] = 5
    S_next[is_four & (r_4 >= 0.40) & (r_4 < 0.50)] = 0

    is_five = (S == 5)
    S_next[is_five & (rng.random(width) < 0.25)] = 0
    return S_next


def l23_r07_single_seed(width):
    c = width // 2
    grid = np.zeros(width, dtype=np.uint8)
    grid[c - 30: c - 5] = 1
    grid[c + 5: c + 30] = 2
    return grid


L23_R07 = Rule(
    name="Loop 23 Rule 7: Recombination-Driven Zoonotic Spillover",
    n_states=6,
    step=l23_r07_step,
    init=loop23_init(l23_r07_single_seed, [0, 1, 2], [0.90, 0.05, 0.05]),
    palette=[(10, 25, 15), (240, 128, 128), (135, 206, 250), (186, 85, 211), (255, 23, 68), (47, 79, 79)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 23, Rule 5: Viroid Hyperparasitism -------------------------------------------
# 0 healthy, 1 infected, 2 co-infected by the hyperparasite, 3 suppressed, 4 dead, 5 immune.
def l23_r05_step(S, rng, t):
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)

    N_I = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_C = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_V = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)

    p_inf = 1.0 - (0.45**N_I) * (0.725**N_C)
    is_zero = (S == 0)
    S_next[is_zero & (rng.random(width) < p_inf)] = 1

    is_one = (S == 1)
    p_hyper = 1.0 - 0.40**(N_C + N_V)
    hyperinfected_1 = rng.random(width) < p_hyper
    r_choice_1 = rng.random(width)
    death_1 = ~hyperinfected_1 & (r_choice_1 < 0.10)
    recover_1 = ~hyperinfected_1 & (r_choice_1 >= 0.10) & (r_choice_1 < 0.20)
    S_next[is_one & hyperinfected_1] = 2
    S_next[is_one & death_1] = 4
    S_next[is_one & recover_1] = 5

    is_two = (S == 2)
    r_c = rng.random(width)
    S_next[is_two & (r_c < 0.35)] = 3
    S_next[is_two & (r_c >= 0.35) & (r_c < 0.55)] = 4

    is_three = (S == 3)
    S_next[is_three & (rng.random(width) < 0.45)] = 5

    is_four = (S == 4)
    S_next[is_four & (rng.random(width) < 0.30)] = 0

    is_five = (S == 5)
    S_next[is_five & (rng.random(width) < 0.15)] = 0
    return S_next


def l23_r05_single_seed(width):
    c = width // 2
    grid = np.zeros(width, dtype=np.uint8)
    grid[c - 10: c + 10] = 1
    grid[c] = 2
    return grid


L23_R05 = Rule(
    name="Loop 23 Rule 5: Viroid Hyperparasitism",
    n_states=6,
    step=l23_r05_step,
    init=loop23_init(l23_r05_single_seed, [0, 1, 2], [0.85, 0.10, 0.05]),
    palette=[(12, 12, 24), (220, 20, 60), (127, 255, 0), (0, 191, 255), (70, 130, 180), (230, 230, 250)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Loop 24: Self-Organized Flocking & Active Matter Turbulence
# Cells are uint8. ETA is each rule's noise level (the original's default argument).
# =====================================================================================

# -- Loop 24, Rule 1: Stochastic Vicsek-1D Flocking ------------------------------------
# 0 empty, 1 left-mover, 2 right-mover; movers align with the local majority.
L24_R01_ETA = 0.08


def l24_r01_step(S, rng, t):
    W = S.size
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    N_L = (S == 1).astype(int) + (S_left == 1).astype(int) + (S_right == 1).astype(int)
    N_R = (S == 2).astype(int) + (S_left == 2).astype(int) + (S_right == 2).astype(int)
    N_active = N_L + N_R

    scatter = rng.integers(0, 3, size=W)
    bernoulli = rng.integers(0, 2, size=W) + 1
    align = np.where(N_L > N_R, 1, np.where(N_R > N_L, 2, bernoulli))

    noise_mask = rng.random(size=W) < L24_R01_ETA
    next_S = np.where(noise_mask, scatter, align)
    next_S = np.where(N_active == 0, 0, next_S)
    return next_S.astype(np.uint8)


def l24_r01_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.zeros(width, dtype=np.uint8)
        S[width // 2 - 20: width // 2] = 1
        S[width // 2: width // 2 + 20] = 2
        return S
    return rng.choice([0, 1, 2], p=[0.4, 0.3, 0.3], size=width)


L24_R01 = Rule(
    name="Loop 24 Rule 1: Stochastic Vicsek-1D Flocking",
    n_states=3,
    step=l24_r01_step,
    init=l24_r01_init,
    palette=[(15, 15, 20), (0, 255, 240), (255, 0, 127)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 24, Rule 2: Multi-Angle Filament Alignment -----------------------------------
# Six headings (60 degrees apart); each cell turns towards the mean heading of its r=2
# neighbourhood, with random wobble.
L24_R02_ETA = 0.15
THETA_6 = 2 * np.pi * np.arange(6) / 6
COS_6 = np.cos(THETA_6)
SIN_6 = np.sin(THETA_6)


def l24_r02_step(S, rng, t):
    W = S.size
    S_l2 = np.roll(S, 2)
    S_l1 = np.roll(S, 1)
    S_c = S
    S_r1 = np.roll(S, -1)
    S_r2 = np.roll(S, -2)

    V_mean_x = (COS_6[S_l2] + COS_6[S_l1] + COS_6[S_c] + COS_6[S_r1] + COS_6[S_r2]) / 5.0
    V_mean_y = (SIN_6[S_l2] + SIN_6[S_l1] + SIN_6[S_c] + SIN_6[S_r1] + SIN_6[S_r2]) / 5.0

    zero_mask = (V_mean_x**2 + V_mean_y**2) < 1e-6
    theta_target = np.arctan2(V_mean_y, V_mean_x)
    random_thetas = rng.random(size=W) * 2 * np.pi
    theta_target[zero_mask] = random_thetas[zero_mask]

    diffs = np.zeros((6, W))
    for k in range(6):
        diffs[k] = np.abs((THETA_6[k] - theta_target + np.pi) % (2 * np.pi) - np.pi)
    k_target = np.argmin(diffs, axis=0)

    r = rng.random(size=W)
    xi = np.where(r < 0.25, -1, np.where(r < 0.75, 0, 1))
    noise_val = (S + xi) % 6
    noise_mask = rng.random(size=W) < L24_R02_ETA
    return np.where(noise_mask, noise_val, k_target).astype(np.uint8)


def l24_r02_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.zeros(width, dtype=np.uint8)
        for i in range(100):  # five 20-cell bands with headings 1..5
            S[width // 2 - 50 + i] = (i // 20) + 1
        return S
    return rng.choice([0, 1, 2, 3, 4, 5], p=[0.2, 0.16, 0.16, 0.16, 0.16, 0.16], size=width)


L24_R02 = Rule(
    name="Loop 24 Rule 2: Multi-Angle Filament Alignment",
    n_states=6,
    step=l24_r02_step,
    init=l24_r02_init,
    palette=[(10, 18, 20), (57, 255, 20), (0, 255, 127), (0, 191, 255), (148, 0, 211), (255, 140, 0)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 24, Rule 9: Active Matter Phase Transition -----------------------------------
# 0 empty, 1-2 left-moving (slow/fast), 3-4 right-moving, 5 jammed. Low local density
# gives a gas, higher density a polar liquid, very high density a jam.
L24_R09_ETA = 0.10


def l24_r09_step(S, rng, t):
    W = S.size
    S_l2 = np.roll(S, 2)
    S_l1 = np.roll(S, 1)
    S_c = S
    S_r1 = np.roll(S, -1)
    S_r2 = np.roll(S, -2)
    eta = L24_R09_ETA

    active_count = (
        (S_l2 != 0).astype(int) + (S_l1 != 0).astype(int) + (S_c != 0).astype(int)
        + (S_r1 != 0).astype(int) + (S_r2 != 0).astype(int)
    )
    rho_a = active_count / 5.0
    rho_c = 0.4

    r_gas = rng.random(size=W)  # gas phase
    gas_val = np.where(r_gas < 0.7, 0, np.where(r_gas < 0.85, 1, 3))

    N_L = (  # polar liquid phase
        np.isin(S_l2, [1, 2]).astype(int) + np.isin(S_l1, [1, 2]).astype(int) + np.isin(S_c, [1, 2]).astype(int)
        + np.isin(S_r1, [1, 2]).astype(int) + np.isin(S_r2, [1, 2]).astype(int)
    )
    N_R = (
        np.isin(S_l2, [3, 4]).astype(int) + np.isin(S_l1, [3, 4]).astype(int) + np.isin(S_c, [3, 4]).astype(int)
        + np.isin(S_r1, [3, 4]).astype(int) + np.isin(S_r2, [3, 4]).astype(int)
    )

    align_val = np.zeros(W, dtype=np.uint8)
    r_align = rng.random(size=W)
    r_noise_L = rng.random(size=W)
    r_noise_R = rng.random(size=W)
    cond_L = (N_L > N_R)
    cond_R = (N_R > N_L)
    align_val[cond_L] = np.where(r_align[cond_L] < (1 - eta), 2, np.where(r_noise_L[cond_L] < 0.5, 1, 0))
    align_val[cond_R] = np.where(r_align[cond_R] < (1 - eta), 4, np.where(r_noise_R[cond_R] < 0.5, 3, 0))

    high_dens = (rho_a > 0.8)
    r_high = rng.random(size=W)
    liquid_val = np.where(high_dens & (r_high < (1 - eta)), 5, align_val)
    return np.where(rho_a < rho_c, gas_val, liquid_val).astype(np.uint8)


def l24_r09_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.zeros(width, dtype=np.uint8)
        S[width // 2 - 40: width // 2 + 40] = rng.choice([1, 2, 3, 4], size=80)  # a random swarm
        return S
    return rng.choice([0, 1, 2, 3, 4, 5], p=[0.55, 0.10, 0.10, 0.10, 0.10, 0.05], size=width)


L24_R09 = Rule(
    name="Loop 24 Rule 9: Active Matter Phase Transition",
    n_states=6,
    step=l24_r09_step,
    init=l24_r09_init,
    palette=[(18, 18, 18), (70, 130, 180), (0, 191, 255), (188, 143, 143), (255, 20, 147), (255, 191, 0)],
    description="Showcase pick: single-seed start.",
)


# =====================================================================================
# Loop 25: Self-Organized Criticality, Avalanches & Forest Fires
# The driving rate depends on the start, so the state is (row, rate); view shows the row.
# =====================================================================================

# -- Loop 25, Rule 1: Stochastic Sandpile Cascade --------------------------------------
# Grains drop with probability p_d; a cell with 4+ grains topples one grain to each side.
def l25_r01_step(state, rng, t):
    S, p_d = state
    xi = rng.binomial(1, p_d, size=S.size)
    T = (S >= 4).astype(np.int32)
    S = np.clip(S + xi - 2 * T + np.roll(T, 1) + np.roll(T, -1), 0, 5)
    return (S, p_d)


def l25_r01_init(init_type, width, rng):
    if init_type == "single_seed":
        S = rng.choice([2, 3], size=width, p=[0.5, 0.5])  # a stable background
        S[width // 2] = 5
        return (S, 0.005)  # low deposition, so the seed's avalanches stand out
    return (rng.choice([0, 1, 2, 3], size=width, p=[0.1, 0.2, 0.4, 0.3]), 0.02)


L25_R01 = Rule(
    name="Loop 25 Rule 1: Stochastic Sandpile Cascade",
    n_states=6,
    step=l25_r01_step,
    init=l25_r01_init,
    view=lambda state: state[0],
    palette=[(15, 15, 20), (40, 50, 90), (0, 180, 180), (50, 220, 100), (255, 220, 0), (255, 60, 60)],
    description="Showcase pick: single-seed start.",
)


# -- Loop 25, Rule 8: Stochastic Neuronal Avalanche ------------------------------------
# 0-2 charging, 3 firing, 4 refractory, 5 recovering. Firing neighbours (r=2) and random
# input with probability p_n push charging cells towards firing.
def l25_r08_step(state, rng, t):
    S, p_n = state
    xi_n = rng.binomial(1, p_n, size=S.size)
    F = ((np.roll(S, 2) == 3).astype(np.int32) + (np.roll(S, 1) == 3).astype(np.int32)
         + (np.roll(S, -1) == 3).astype(np.int32) + (np.roll(S, -2) == 3).astype(np.int32))

    S_next = S.copy()
    mask_exc = (S <= 2)
    S_next[mask_exc] = np.minimum(3, S[mask_exc] + F[mask_exc] + xi_n[mask_exc])
    mask_ref = (S == 3) | (S == 4)
    S_next[mask_ref] = S[mask_ref] + 1
    S_next[S == 5] = 0
    return (S_next, p_n)


def l25_r08_init(init_type, width, rng):
    if init_type == "single_seed":
        S = np.full(width, 2, dtype=np.int32)  # everything just below threshold
        S[width // 2] = 3
        return (S, 0.001)
    return (rng.choice([0, 1, 2], size=width, p=[0.4, 0.4, 0.2]), 0.03)


L25_R08 = Rule(
    name="Loop 25 Rule 8: Stochastic Neuronal Avalanche",
    n_states=6,
    step=l25_r08_step,
    init=l25_r08_init,
    view=lambda state: state[0],
    palette=[(18, 18, 18), (10, 60, 30), (100, 180, 100), (255, 255, 150), (80, 0, 120), (30, 45, 60)],
    description="Showcase pick: random start.",
)


# =====================================================================================
# Showcase order (matches gif_showcase.py and showcase/)
# =====================================================================================

RULES = [
    L01_R04, L02_R02, L02_R04, L02_R07, L03_R08,
    L06_R01, L08_R01, L08_R02, L09_R08, L10_R08,
    L11_R03, L25_R08, L11_R05, L12_R02, L12_R04,
    L13_R04, L13_R10, L14_R03, L14_R07, L15_R09,
    L17_R09, L20_R05, L20_R06, L22_R07, L23_R07,
    L23_R05, L24_R01, L24_R02, L24_R09, L25_R01,
]
