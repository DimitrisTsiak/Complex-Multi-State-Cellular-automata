import os
import numpy as np
from PIL import Image

# Output directory
output_dir = "generations/loop_24/output"
os.makedirs(output_dir, exist_ok=True)

# Grid dimensions
WIDTH = 800
STEPS = 800

# ----------------- Color Palettes -----------------
palettes = {
    1: np.array([[15, 15, 20], [0, 255, 240], [255, 0, 127]], dtype=np.uint8),  # 3 states
    2: np.array([[10, 18, 20], [57, 255, 20], [0, 255, 127], [0, 191, 255], [148, 0, 211], [255, 140, 0]], dtype=np.uint8),  # 6 states
    3: np.array([[15, 5, 20], [220, 20, 60], [255, 69, 0], [255, 215, 0], [50, 205, 50], [64, 224, 208], [65, 105, 225], [255, 105, 180]], dtype=np.uint8),  # 8 states
    4: np.array([[5, 10, 25], [173, 255, 47], [0, 255, 255], [255, 30, 30]], dtype=np.uint8),  # 4 states
    5: np.array([[0, 0, 0], [30, 144, 255], [0, 255, 255], [220, 20, 60], [255, 165, 0]], dtype=np.uint8),  # 5 states
    6: np.array([[20, 20, 20], [0, 128, 128], [0, 255, 255], [255, 127, 80], [255, 69, 0], [191, 85, 236]], dtype=np.uint8),  # 6 states
    7: np.array([[10, 10, 12], [255, 255, 0], [0, 102, 255]], dtype=np.uint8),  # 3 states
    8: np.array([[15, 20, 25], [0, 255, 100], [255, 230, 0], [255, 80, 0]], dtype=np.uint8),  # 4 states
    9: np.array([[18, 18, 18], [70, 130, 180], [0, 191, 255], [188, 143, 143], [255, 20, 147], [255, 191, 0]], dtype=np.uint8),  # 6 states
    10: np.array([[12, 12, 14], [50, 255, 50], [218, 112, 214], [255, 69, 0], [240, 240, 255]], dtype=np.uint8)  # 5 states
}


# ----------------- CA Simulation Rules -----------------

def run_rule_1(S_init, steps, eta=0.08):
    """Stochastic Vicsek-1D Flocking"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    for t in range(1, steps):
        S_left = np.roll(S, 1)
        S_right = np.roll(S, -1)
        N_L = (S == 1).astype(int) + (S_left == 1).astype(int) + (S_right == 1).astype(int)
        N_R = (S == 2).astype(int) + (S_left == 2).astype(int) + (S_right == 2).astype(int)
        N_active = N_L + N_R
        
        scatter = np.random.randint(0, 3, size=W)
        bernoulli = np.random.randint(0, 2, size=W) + 1
        align = np.where(N_L > N_R, 1, np.where(N_R > N_L, 2, bernoulli))
        
        noise_mask = np.random.random(size=W) < eta
        next_S = np.where(noise_mask, scatter, align)
        next_S = np.where(N_active == 0, 0, next_S)
        S = next_S.astype(np.uint8)
        history[t] = S
    return history


def run_rule_2(S_init, steps, eta=0.15):
    """Multi-Angle Filament Alignment"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    theta_vals = 2 * np.pi * np.arange(6) / 6
    cos_vals = np.cos(theta_vals)
    sin_vals = np.sin(theta_vals)
    
    for t in range(1, steps):
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_c = S
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        V_mean_x = (cos_vals[S_l2] + cos_vals[S_l1] + cos_vals[S_c] + cos_vals[S_r1] + cos_vals[S_r2]) / 5.0
        V_mean_y = (sin_vals[S_l2] + sin_vals[S_l1] + sin_vals[S_c] + sin_vals[S_r1] + sin_vals[S_r2]) / 5.0
        
        zero_mask = (V_mean_x**2 + V_mean_y**2) < 1e-6
        theta_target = np.arctan2(V_mean_y, V_mean_x)
        random_thetas = np.random.random(size=W) * 2 * np.pi
        theta_target[zero_mask] = random_thetas[zero_mask]
        
        diffs = np.zeros((6, W))
        for k in range(6):
            diffs[k] = np.abs((theta_vals[k] - theta_target + np.pi) % (2 * np.pi) - np.pi)
        k_target = np.argmin(diffs, axis=0)
        
        r = np.random.random(size=W)
        xi = np.where(r < 0.25, -1, np.where(r < 0.75, 0, 1))
        noise_val = (S + xi) % 6
        noise_mask = np.random.random(size=W) < eta
        
        S = np.where(noise_mask, noise_val, k_target).astype(np.uint8)
        history[t] = S
    return history


def run_rule_3(S_init, steps, eta=0.10):
    """Chiral Active Rotators (Kuramoto CA)"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    phi = 2 * np.pi * np.arange(8) / 8
    cos_vals = np.cos(phi)
    sin_vals = np.sin(phi)
    
    for t in range(1, steps):
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        
        Zx = cos_vals[S_l1] + cos_vals[S_r1]
        Zy = sin_vals[S_l1] + sin_vals[S_r1]
        
        R_sq = Zx**2 + Zy**2
        Phi_avg = np.arctan2(Zy, Zx)
        zero_mask = R_sq < 1e-6
        Phi_avg[zero_mask] = phi[S[zero_mask]]
        
        diffs = np.zeros((8, W))
        for k in range(8):
            diffs[k] = np.abs((phi[k] - Phi_avg + np.pi) % (2 * np.pi) - np.pi)
        k_align = np.argmin(diffs, axis=0)
        
        delta = np.sign(((k_align - S + 4) % 8) - 4).astype(int)
        
        align_state = (S + 1 + delta) % 8
        scatter_state = np.random.randint(0, 8, size=W)
        noise_mask = np.random.random(size=W) < eta
        
        S = np.where(noise_mask, scatter_state, align_state).astype(np.uint8)
        history[t] = S
    return history


def run_rule_4(S_init, steps, gamma=0.3):
    """Run-and-Tumble Active Matter (MIPS)"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    for t in range(1, steps):
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        In_L = (S_r1 == 1)
        In_R = (S_l1 == 2)
        
        next_S = np.zeros(W, dtype=np.uint8)
        
        # State 0 transitions
        s0_mask = (S == 0)
        cond_1 = s0_mask & In_L & ~In_R
        cond_2 = s0_mask & In_R & ~In_L
        cond_3 = s0_mask & In_L & In_R
        
        r_0_1 = np.random.random(size=W)
        r_0_2 = np.random.random(size=W)
        r_0_3 = np.random.random(size=W)
        
        next_S[cond_1] = np.where(r_0_1[cond_1] < 0.9, 1, 3)
        next_S[cond_2] = np.where(r_0_2[cond_2] < 0.9, 2, 3)
        next_S[cond_3] = np.where(r_0_3[cond_3] < 0.8, 3, 0)
        
        # State 1 transitions (Left-running)
        s1_mask = (S == 1)
        blocked_1 = (S_l1 != 0)
        r_1 = np.random.random(size=W)
        next_S[s1_mask & blocked_1] = np.where(r_1[s1_mask & blocked_1] < 0.8, 3, 1)
        next_S[s1_mask & ~blocked_1] = 0
        
        # State 2 transitions (Right-running)
        s2_mask = (S == 2)
        blocked_2 = (S_r1 != 0)
        r_2 = np.random.random(size=W)
        next_S[s2_mask & blocked_2] = np.where(r_2[s2_mask & blocked_2] < 0.8, 3, 2)
        next_S[s2_mask & ~blocked_2] = 0
        
        # State 3 transitions (Tumbling)
        s3_mask = (S == 3)
        r_3 = np.random.random(size=W)
        r_resolve = np.random.random(size=W)
        resolved = np.where(r_resolve < 0.5, 1, 2)
        next_S[s3_mask] = np.where(r_3[s3_mask] < gamma, resolved[s3_mask], 3)
        
        S = next_S
        history[t] = S
    return history


def run_rule_5(S_init, steps, eta=0.10):
    """Active Burgers Turbulence"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    U_vals = np.array([0, -1, -2, 1, 2], dtype=float)
    
    for t in range(1, steps):
        U_S = U_vals[S]
        U_l1 = U_vals[np.roll(S, 1)]
        U_r1 = U_vals[np.roll(S, -1)]
        
        A = U_S * (U_l1 - U_r1)
        D = U_l1 - 2 * U_S + U_r1
        H = U_S + 0.5 * A + 0.3 * D
        
        diffs = np.zeros((5, W))
        for k in range(5):
            diffs[k] = np.abs(U_vals[k] - H)
        k_target = np.argmin(diffs, axis=0)
        
        scatter = np.random.randint(0, 5, size=W)
        noise_mask = np.random.random(size=W) < eta
        
        S = np.where(noise_mask, scatter, k_target).astype(np.uint8)
        history[t] = S
    return history


def run_rule_6(S_init, steps, eta=0.10):
    """Stochastic Velocity-Modulated Flocking"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    U_vals = np.array([0, -1, -2, 1, 2, 0])
    
    for t in range(1, steps):
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        active = (S_l2 != 0).astype(int) + (S_l1 != 0).astype(int) + (S_r1 != 0).astype(int) + (S_r2 != 0).astype(int)
        rho = active / 4.0
        
        V_sum = U_vals[S_l2] + U_vals[S_l1] + U_vals[S_r1] + U_vals[S_r2]
        
        dir_left = np.zeros(W, dtype=bool)
        dir_left[V_sum < 0] = True
        dir_left[V_sum > 0] = False
        
        v_zero = (V_sum == 0)
        dir_left[v_zero] = np.isin(S[v_zero], [1, 2])
        
        speed_fast = (rho < 0.3)
        
        k_target = np.zeros(W, dtype=int)
        k_target[dir_left & speed_fast] = 2
        k_target[dir_left & ~speed_fast] = 1
        k_target[~dir_left & speed_fast] = 4
        k_target[~dir_left & ~speed_fast] = 3
        
        next_S = np.zeros(W, dtype=np.uint8)
        
        # Overcrowded case
        overcrowded = (rho > 0.75)
        r_overcrowd = np.random.random(size=W)
        scatter_overcrowd = np.random.choice([1, 3, 5], size=W)
        next_S[overcrowded] = np.where(r_overcrowd[overcrowded] < eta, scatter_overcrowd[overcrowded], 5)
        
        # Normal case
        normal = ~overcrowded
        r_normal = np.random.random(size=W)
        scatter_normal = np.random.choice([1, 2, 3, 4], size=W)
        next_S[normal] = np.where(r_normal[normal] < eta, scatter_normal[normal], k_target[normal])
        
        S = next_S
        history[t] = S
    return history


def run_rule_7(S_init, steps, eta=0.10):
    """Active Nematic Defect Dynamics"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    for t in range(1, steps):
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        
        defect = (S_l1 != S_r1) & (S_l1 != 0) & (S_r1 != 0)
        
        N1 = (S_l1 == 1).astype(int) + (S == 1).astype(int) + (S_r1 == 1).astype(int)
        N2 = (S_l1 == 2).astype(int) + (S == 2).astype(int) + (S_r1 == 2).astype(int)
        
        next_S = np.zeros(W, dtype=np.uint8)
        
        # Defect case
        r_defect = np.random.random(size=W)
        flip_val = np.where(S != 0, 3 - S, np.random.choice([1, 2], size=W))
        next_S[defect] = np.where(r_defect[defect] < eta, 0, flip_val[defect])
        
        # Non-defect case
        non_defect = ~defect
        
        # Non-defect S == 0
        cond_0 = non_defect & (S == 0)
        align_val = np.where(N1 > N2, 1, np.where(N2 > N1, 2, 0))
        r_cond_0 = np.random.random(size=W)
        scatter_0 = np.random.randint(0, 3, size=W)
        next_S[cond_0] = np.where(r_cond_0[cond_0] < eta, scatter_0[cond_0], align_val[cond_0])
        
        # Non-defect S in (1, 2)
        cond_12 = non_defect & (S != 0)
        r_cond_12 = np.random.random(size=W)
        next_S[cond_12] = np.where(r_cond_12[cond_12] < eta, 0, S[cond_12])
        
        S = next_S
        history[t] = S
    return history


def run_rule_8(S_init, steps, spawn_rate=0.02, eta=0.10):
    """Chemotactic Predator-Prey Flocking"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    for t in range(1, steps):
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        G_L = (S_l1 == 1).astype(int) + 2 * (S_l2 == 1).astype(int)
        G_R = (S_r1 == 1).astype(int) + 2 * (S_r2 == 1).astype(int)
        
        P_L = np.isin(S_l1, [2, 3]).astype(int) + np.isin(S_l2, [2, 3]).astype(int)
        P_R = np.isin(S_r1, [2, 3]).astype(int) + np.isin(S_r2, [2, 3]).astype(int)
        
        # S == 1 (nutrient) transition
        adj_flocker_L = (S_l1 == 3)
        adj_flocker_R = (S_r1 == 2)
        has_adj = adj_flocker_L | adj_flocker_R
        
        r_choice = np.random.random(size=W)
        incoming_state = np.where(adj_flocker_L & ~adj_flocker_R, 3,
                         np.where(adj_flocker_R & ~adj_flocker_L, 2,
                         np.where(r_choice < 0.5, 2, 3)))
        
        next_S_1 = np.zeros(W, dtype=np.uint8)
        r_c1 = np.random.random(size=W)
        next_S_1[has_adj] = np.where(r_c1[has_adj] < 0.9, incoming_state[has_adj], 1)
        
        r_c2 = np.random.random(size=W)
        next_S_1[~has_adj] = np.where(r_c2[~has_adj] < 0.02, 0, 1)
        
        # S == 0 (empty) transition
        nut_state = np.zeros(W, dtype=np.uint8)
        r_nut = np.random.random(size=W)
        nut_guided_L = (G_L > G_R)
        nut_guided_R = (G_R > G_L)
        nut_guided_eq = (G_L == G_R) & (G_L > 0)
        
        nut_state[nut_guided_L] = np.where(r_nut[nut_guided_L] < 0.8, 2, 0)
        nut_state[nut_guided_R] = np.where(r_nut[nut_guided_R] < 0.8, 3, 0)
        
        r_eq = np.random.random(size=W)
        eq_choice = np.where(r_eq < 0.5, 2, 3)
        nut_state[nut_guided_eq] = np.where(r_nut[nut_guided_eq] < 0.8, eq_choice[nut_guided_eq], 0)
        
        flock_state = np.zeros(W, dtype=np.uint8)
        r_flock = np.random.random(size=W)
        flock_guided_L = (P_L > P_R)
        flock_guided_R = (P_R > P_L)
        flock_state[flock_guided_L] = np.where(r_flock[flock_guided_L] < 0.6, 2, 0)
        flock_state[flock_guided_R] = np.where(r_flock[flock_guided_R] < 0.6, 3, 0)
        
        has_nutrients = (G_L > 0) | (G_R > 0)
        base_empty_state = np.where(has_nutrients, nut_state, flock_state)
        
        r_spawn = np.random.random(size=W)
        next_S_0 = np.where(r_spawn < spawn_rate, 1, base_empty_state)
        
        # S in (2, 3) (flocker) transition
        r_move = np.random.random(size=W)
        r_turn = np.random.random(size=W)
        stay_state = np.where(r_turn < eta, 5 - S, S)
        next_S_flock = np.where(r_move < 0.9, 0, stay_state)
        
        next_S = np.zeros(W, dtype=np.uint8)
        next_S[S == 0] = next_S_0[S == 0]
        next_S[S == 1] = next_S_1[S == 1]
        flock_mask = (S == 2) | (S == 3)
        next_S[flock_mask] = next_S_flock[flock_mask]
        
        S = next_S
        history[t] = S
    return history


def run_rule_9(S_init, steps, eta=0.10):
    """Active Matter Phase Transition"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    for t in range(1, steps):
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_c = S
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        active_count = (
            (S_l2 != 0).astype(int) +
            (S_l1 != 0).astype(int) +
            (S_c != 0).astype(int) +
            (S_r1 != 0).astype(int) +
            (S_r2 != 0).astype(int)
        )
        rho_a = active_count / 5.0
        rho_c = 0.4
        
        # Gas phase
        r_gas = np.random.random(size=W)
        gas_val = np.where(r_gas < 0.7, 0, np.where(r_gas < 0.85, 1, 3))
        
        # Polar Liquid phase
        N_L = (
            np.isin(S_l2, [1, 2]).astype(int) +
            np.isin(S_l1, [1, 2]).astype(int) +
            np.isin(S_c, [1, 2]).astype(int) +
            np.isin(S_r1, [1, 2]).astype(int) +
            np.isin(S_r2, [1, 2]).astype(int)
        )
        N_R = (
            np.isin(S_l2, [3, 4]).astype(int) +
            np.isin(S_l1, [3, 4]).astype(int) +
            np.isin(S_c, [3, 4]).astype(int) +
            np.isin(S_r1, [3, 4]).astype(int) +
            np.isin(S_r2, [3, 4]).astype(int)
        )
        
        align_val = np.zeros(W, dtype=np.uint8)
        r_align = np.random.random(size=W)
        r_noise_L = np.random.random(size=W)
        r_noise_R = np.random.random(size=W)
        
        cond_L = (N_L > N_R)
        cond_R = (N_R > N_L)
        
        align_val[cond_L] = np.where(r_align[cond_L] < (1 - eta), 2, np.where(r_noise_L[cond_L] < 0.5, 1, 0))
        align_val[cond_R] = np.where(r_align[cond_R] < (1 - eta), 4, np.where(r_noise_R[cond_R] < 0.5, 3, 0))
        
        high_dens = (rho_a > 0.8)
        r_high = np.random.random(size=W)
        liquid_val = np.where(high_dens & (r_high < (1 - eta)), 5, align_val)
        
        S = np.where(rho_a < rho_c, gas_val, liquid_val).astype(np.uint8)
        history[t] = S
    return history


def run_rule_10(S_init, steps, eta=0.10):
    """Active Emulsion Phase-Separation"""
    W = len(S_init)
    history = np.zeros((steps, W), dtype=np.uint8)
    S = S_init.copy()
    history[0] = S
    
    for t in range(1, steps):
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_c = S
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        N_A = (
            (S_l2 == 1).astype(int) +
            (S_l1 == 1).astype(int) +
            (S_c == 1).astype(int) +
            (S_r1 == 1).astype(int) +
            (S_r2 == 1).astype(int)
        )
        N_B = (
            (S_l2 == 2).astype(int) +
            (S_l1 == 2).astype(int) +
            (S_c == 2).astype(int) +
            (S_r1 == 2).astype(int) +
            (S_r2 == 2).astype(int)
        )
        
        # Mixed zone
        r_mix = np.random.random(size=W)
        r_seg = np.random.random(size=W)
        seg_choice = np.where(N_A > N_B, 1, np.where(N_B > N_A, 2, np.where(r_seg < 0.5, 1, 2)))
        mix_val = np.where(r_mix < 0.6, 3, np.where(r_mix < 0.9, seg_choice, 0))
        
        # Species A domain
        r_a = np.random.random(size=W)
        r_a_noise = np.random.random(size=W)
        domain_a_val = np.where(r_a < (1 - eta), 1, np.where(r_a_noise < 0.5, 0, 3))
        
        # Species B domain
        r_b = np.random.random(size=W)
        r_b_noise = np.random.random(size=W)
        domain_b_val = np.where(r_b < (1 - eta), 2, np.where(r_b_noise < 0.5, 0, 3))
        
        # Empty background
        r_empty = np.random.random(size=W)
        r_empty_noise = np.random.random(size=W)
        empty_val = np.where(r_empty < 0.98, 0, np.where(r_empty_noise < 0.5, 1, 2))
        
        next_S = np.zeros(W, dtype=np.uint8)
        cond_mix = (N_A > 0) & (N_B > 0)
        cond_a = (N_A > 0) & (N_B == 0)
        cond_b = (N_B > 0) & (N_A == 0)
        cond_empty = (N_A == 0) & (N_B == 0)
        
        next_S[cond_mix] = mix_val[cond_mix]
        next_S[cond_a] = domain_a_val[cond_a]
        next_S[cond_b] = domain_b_val[cond_b]
        next_S[cond_empty] = empty_val[cond_empty]
        
        S = next_S
        history[t] = S
    return history


# Mapping functions from rule number to implementation function
rule_functions = {
    1: run_rule_1,
    2: run_rule_2,
    3: run_rule_3,
    4: run_rule_4,
    5: run_rule_5,
    6: run_rule_6,
    7: run_rule_7,
    8: run_rule_8,
    9: run_rule_9,
    10: run_rule_10
}


# ----------------- Seeds Setup -----------------

def get_initial_states(rule_num, init_type):
    np.random.seed(42 + rule_num)  # Keep it reproducible but randomized between rules
    W = WIDTH
    
    if init_type == "random":
        if rule_num == 1:
            return np.random.choice([0, 1, 2], p=[0.4, 0.3, 0.3], size=W)
        elif rule_num == 2:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.2, 0.16, 0.16, 0.16, 0.16, 0.16], size=W)
        elif rule_num == 3:
            return np.random.randint(0, 8, size=W)
        elif rule_num == 4:
            return np.random.choice([0, 1, 2, 3], p=[0.6, 0.15, 0.15, 0.10], size=W)
        elif rule_num == 5:
            return np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.175, 0.175, 0.175, 0.175], size=W)
        elif rule_num == 6:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.4, 0.125, 0.125, 0.125, 0.125, 0.10], size=W)
        elif rule_num == 7:
            return np.random.choice([0, 1, 2], p=[0.2, 0.4, 0.4], size=W)
        elif rule_num == 8:
            return np.random.choice([0, 1, 2, 3], p=[0.7, 0.1, 0.1, 0.1], size=W)
        elif rule_num == 9:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.55, 0.10, 0.10, 0.10, 0.10, 0.05], size=W)
        elif rule_num == 10:
            return np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.3, 0.3, 0.05, 0.05], size=W)
            
    elif init_type == "single_seed":
        S = np.zeros(W, dtype=np.uint8)
        mid = W // 2
        
        if rule_num == 1:
            S[mid-20:mid] = 1
            S[mid:mid+20] = 2
        elif rule_num == 2:
            for i in range(100):
                S[mid-50+i] = (i // 20) + 1
        elif rule_num == 3:
            for i in range(80):
                S[mid-40+i] = i % 8
        elif rule_num == 4:
            S[mid-30:mid-5] = 2
            S[mid-5:mid+5] = 3
            S[mid+5:mid+30] = 1
        elif rule_num == 5:
            S[mid-50:mid-10] = 4
            S[mid+10:mid+50] = 2
        elif rule_num == 6:
            S[mid-50:mid+50] = np.random.choice([1, 2, 3, 4], size=100)
            S[mid-10:mid+10] = 5
        elif rule_num == 7:
            S[mid-100:mid-50] = 1
            S[mid-50:mid] = 2
            S[mid:mid+50] = 1
            S[mid+50:mid+100] = 2
        elif rule_num == 8:
            S[mid-10:mid+10] = 1
            S[mid-30:mid-10] = 3
            S[mid+10:mid+30] = 2
        elif rule_num == 9:
            S[mid-40:mid+40] = np.random.choice([1, 2, 3, 4], size=80)
        elif rule_num == 10:
            S[mid-100:mid] = 1
            S[mid:mid+100] = 2
            S[mid-5:mid+5] = 3
            
        return S


# ----------------- Execution & Image Saving -----------------

for r_num in range(1, 11):
    palette = palettes[r_num]
    run_func = rule_functions[r_num]
    
    for init_type in ["single_seed", "random"]:
        print(f"Simulating Rule {r_num} ({init_type})...")
        S_init = get_initial_states(r_num, init_type)
        history = run_func(S_init, STEPS)
        
        # Map history grid to RGB values using the palette
        rgb_data = palette[history]
        
        # Save as PNG
        img = Image.fromarray(rgb_data)
        file_name = f"rule_{r_num:02d}_{init_type}.png"
        file_path = os.path.join(output_dir, file_name)
        img.save(file_path)
        print(f"Saved: {file_path}")

print("All simulations completed successfully!")
