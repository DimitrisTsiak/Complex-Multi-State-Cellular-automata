import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Lattice size and simulation steps
W = 800
H = 800

# ----------------- Transition Rules -----------------

def step_rule_1(S):
    # Rule 1: Discrete Gray-Scott Activator-Inhibitor
    u = S % 4
    v = S // 4
    
    A_local = np.roll(u, 1) + u + np.roll(u, -1)
    I_local = np.roll(v, 2) + np.roll(v, 1) + v + np.roll(v, -1) + np.roll(v, -2)
    
    u_next = np.copy(u)
    cond_dec = I_local >= 2
    cond_inc = (I_local < 2) & (A_local >= 3)
    u_next[cond_dec] = np.maximum(0, u[cond_dec] - 1)
    u_next[cond_inc] = np.minimum(3, u[cond_inc] + 1)
    
    v_next = np.copy(v)
    v_next[u == 3] = 1
    v_next[u == 0] = 0
    
    return u_next + 4 * v_next

def step_rule_2(S):
    # Rule 2: FitzHugh-Nagumo Excitable Wave
    a = S % 3
    w = S // 3
    
    A_diff = np.roll(a, 1) + np.roll(a, -1)
    W_diff = np.roll(w, 2) + np.roll(w, 1) + np.roll(w, -1) + np.roll(w, -2)
    
    a_next = np.copy(a)
    cond1 = (a == 0) & (w == 0) & (A_diff >= 2)
    cond2 = (a == 1) & (W_diff <= 1)
    cond3 = (a == 1) & (W_diff >= 2)
    cond4 = (a == 2)
    
    a_next[cond1] = 1
    a_next[cond2] = 2
    a_next[cond3] = 0
    a_next[cond4] = 0
    
    w_next = np.copy(w)
    cond_w1 = (a == 2)
    cond_w2 = (a == 0) & (W_diff <= 1)
    w_next[cond_w1] = 1
    w_next[cond_w2] = 0
    
    return a_next + 3 * w_next

def step_rule_3(S):
    # Rule 3: Autocatalytic Reversible Brusselator
    X = S % 4
    Y = S // 4
    
    X_sum = np.roll(X, 1) + np.roll(X, -1)
    Y_sum = np.roll(Y, 3) + np.roll(Y, 2) + np.roll(Y, 1) + np.roll(Y, -1) + np.roll(Y, -2) + np.roll(Y, -3)
    
    Y_next = np.copy(Y)
    cond_y1 = (Y == 0) & (Y_sum <= 2)
    cond_y2 = (Y == 1) & (X >= 2)
    Y_next[cond_y1] = 1
    Y_next[cond_y2] = 0
    
    X_next = np.copy(X)
    cond_x1 = (Y == 1) & ((X >= 1) | (X_sum >= 2))
    cond_x2 = (Y == 0)
    X_next[cond_x1] = np.minimum(3, X[cond_x1] + 1)
    X_next[cond_x2] = np.maximum(0, X[cond_x2] - 1)
    
    return X_next + 4 * Y_next

def step_rule_4(S):
    # Rule 4: Chiral Oregonator (BZ with Flow)
    A = S % 3
    C = S // 3
    
    A_chiral = np.roll(A, 2) + 2 * np.roll(A, 1) + np.roll(A, -1)
    
    A_next = np.copy(A)
    cond1 = (A == 0) & (C == 0) & (A_chiral >= 2)
    cond2 = (A == 1) & (C <= 1)
    cond3 = (A >= 1) & (C == 2)
    cond4 = (A == 2) & (C <= 1)
    
    A_next[cond3] = np.maximum(0, A[cond3] - 1)
    A_next[cond1] = 1
    A_next[cond2] = 2
    A_next[cond4] = 1
    
    C_next = np.copy(C)
    cond_c1 = (A == 2)
    cond_c2 = (A == 0)
    C_next[cond_c1] = np.minimum(2, C[cond_c1] + 1)
    C_next[cond_c2] = np.maximum(0, C[cond_c2] - 1)
    
    return A_next + 3 * C_next

def step_rule_5(S):
    # Rule 5: Turing Patterning Sandpile
    L_t = np.roll(S, 1) - 2 * S + np.roll(S, -1)
    I_t = np.roll(S, 3) + np.roll(S, 2) + np.roll(S, -2) + np.roll(S, -3)
    
    delta_S = np.zeros_like(S, dtype=np.int32)
    cond_up = (L_t >= 1) & (I_t <= 6)
    cond_down = (L_t <= -1) | (I_t >= 10)
    
    delta_S[cond_up] = 1
    delta_S[cond_down] = -1
    
    return np.clip(S + delta_S, 0, 5)

def step_rule_6(S):
    # Rule 6: Precipitation-Dissolution (Liesegang Rings)
    A_mask = (S == 1) | (S == 2)
    B_mask = (S == 3) | (S == 4)
    A_count = np.roll(A_mask.astype(np.int32), 1) + np.roll(A_mask.astype(np.int32), -1)
    B_count = np.roll(B_mask.astype(np.int32), 1) + np.roll(B_mask.astype(np.int32), -1)
    
    S_next = np.copy(S)
    
    # S == 0 (empty)
    cond0 = (S == 0)
    cond0_prec = cond0 & (A_count >= 1) & (B_count >= 1)
    cond0_A = cond0 & (A_count >= 1) & (B_count == 0)
    cond0_B = cond0 & (B_count >= 1) & (A_count == 0)
    S_next[cond0_prec] = 5
    S_next[cond0_A] = 1
    S_next[cond0_B] = 3
    
    # S in {1, 2} (Reactant A)
    condAB = (S == 1) | (S == 2)
    condAB_prec = condAB & (B_count >= 1)
    condAB_A = condAB & (B_count == 0) & (A_count >= 2)
    condAB_zero = condAB & (B_count == 0) & (A_count == 0)
    S_next[condAB_prec] = 5
    S_next[condAB_A] = 2
    S_next[condAB_zero] = 0
    
    # S in {3, 4} (Reactant B)
    condB = (S == 3) | (S == 4)
    condB_prec = condB & (A_count >= 1)
    condB_B = condB & (A_count == 0) & (B_count >= 2)
    condB_zero = condB & (A_count == 0) & (B_count == 0)
    S_next[condB_prec] = 5
    S_next[condB_B] = 4
    S_next[condB_zero] = 0
    
    # S in {5, 6} (Precipitate)
    condP_5 = (S == 5)
    condP_6 = condP_5 & (A_count >= 1) & (B_count >= 1)
    condP_A = condP_5 & (A_count >= 2) & (B_count == 0)
    condP_B = condP_5 & (B_count >= 2) & (A_count == 0)
    S_next[condP_6] = 6
    S_next[condP_A] = 1
    S_next[condP_B] = 3
    
    return S_next

def step_rule_7(S):
    # Rule 7: Thermally-Coupled Combustion Wave
    T = S % 4
    F = S // 4
    
    T_local_sum = np.roll(T, 1) + T + np.roll(T, -1)
    T_local = T_local_sum / 3.0
    T_max_all = np.maximum(np.maximum(np.roll(T, 1), T), np.roll(T, -1))
    
    T_next = np.copy(T)
    F_next = np.copy(F)
    
    cond_fuel = (F == 1)
    cond_combust = cond_fuel & ((T >= 1) | (T_max_all >= 2))
    cond_nocombust = cond_fuel & ~((T >= 1) | (T_max_all >= 2))
    cond_nofuel = (F == 0)
    
    T_next[cond_combust] = 3
    F_next[cond_combust] = 0
    
    T_next[cond_nocombust] = np.floor(T_local[cond_nocombust]).astype(np.int32)
    F_next[cond_nocombust] = 1
    
    T_next[cond_nofuel] = np.maximum(0, np.floor(T_local[cond_nofuel]).astype(np.int32) - 1)
    F_next[cond_nofuel] = 0
    
    return T_next + 4 * F_next

def step_rule_8(S):
    # Rule 8: Anomalous Fractional Diffusion Wave
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

def step_rule_9(S):
    # Rule 9: Solute-Inhibited Crystallization
    mask_solid = (S >= 4)
    Solid_count = np.roll(mask_solid.astype(np.int32), 1) + np.roll(mask_solid.astype(np.int32), -1)
    
    S_next = np.copy(S)
    cond_liq = (S < 4)
    cond_solid = (S >= 4)
    
    # Liquid behavior
    cond_sol_count = cond_liq & (Solid_count >= 1)
    cond_liq_0 = (S == 0)
    cond_liq_123 = (S >= 1) & (S <= 3)
    
    cond_solidify = cond_sol_count & (cond_liq_0 | (cond_liq_123 & (S + Solid_count <= 3)))
    cond_reject = cond_sol_count & ~cond_solidify
    
    S_next[cond_solidify] = 4
    S_next[cond_reject] = np.minimum(3, S[cond_reject] + 1)
    
    # Solid behavior
    cond_solid_lt7 = cond_solid & (S < 7)
    cond_solid_eq7 = cond_solid & (S == 7)
    
    S_next[cond_solid_lt7] = S[cond_solid_lt7] + 1
    S_next[cond_solid_eq7] = 7
    
    return S_next

def step_rule_10(S):
    # Rule 10: Stefan Gradient-Stifled Cross-Diffusion
    G_t_left = np.abs(S - np.roll(S, 2))
    G_t_right = np.abs(np.roll(S, -2) - S)
    
    Flux_t = np.roll(S, 1) * (G_t_left <= 1).astype(np.int32) + np.roll(S, -1) * (G_t_right <= 1).astype(np.int32)
    
    S_next = np.copy(S)
    cond_up = (S <= 2) & (Flux_t >= 3)
    cond_down = (S >= 3) & (Flux_t <= 1)
    
    S_next[cond_up] = np.minimum(5, S[cond_up] + 1)
    S_next[cond_down] = np.maximum(0, S[cond_down] - 1)
    
    return S_next

# ----------------- Grid Initialization -----------------

def init_grid(rule_num, seed_type):
    grid = np.zeros(W, dtype=np.uint8)
    
    if seed_type == "single_seed":
        if rule_num == 1:
            grid[W // 2] = 3
        elif rule_num == 2:
            grid[W // 2] = 2
        elif rule_num == 3:
            grid[:] = 4
            grid[W // 2] = 7
        elif rule_num == 4:
            grid[W // 2] = 2
        elif rule_num == 5:
            grid[W // 2] = 5
        elif rule_num == 6:
            grid[W // 2 - 40 : W // 2] = 2
            grid[W // 2 + 1 : W // 2 + 41] = 4
        elif rule_num == 7:
            grid[:] = 4
            grid[W // 2] = 7
        elif rule_num == 8:
            grid[W // 2] = 1
        elif rule_num == 9:
            grid[W // 2] = 4
        elif rule_num == 10:
            grid[W // 2] = 5
            
    elif seed_type == "random":
        if rule_num == 1:
            grid = np.random.randint(0, 8, size=W, dtype=np.uint8)
        elif rule_num == 2:
            grid = np.random.randint(0, 6, size=W, dtype=np.uint8)
        elif rule_num == 3:
            grid = np.random.randint(0, 8, size=W, dtype=np.uint8)
        elif rule_num == 4:
            grid = np.random.randint(0, 9, size=W, dtype=np.uint8)
        elif rule_num == 5:
            grid = np.random.randint(0, 6, size=W, dtype=np.uint8)
        elif rule_num == 6:
            grid = np.random.randint(0, 5, size=W, dtype=np.uint8)
        elif rule_num == 7:
            grid = np.random.randint(0, 8, size=W, dtype=np.uint8)
        elif rule_num == 8:
            grid = np.random.randint(0, 7, size=W, dtype=np.uint8)
        elif rule_num == 9:
            grid = np.random.randint(0, 8, size=W, dtype=np.uint8)
        elif rule_num == 10:
            grid = np.random.randint(0, 6, size=W, dtype=np.uint8)
            
    return grid

# ----------------- Main Simulation Loop -----------------

rules_meta = {
    1: {"step": step_rule_1, "states": 8, "cmap": "plasma"},
    2: {"step": step_rule_2, "states": 6, "cmap": "inferno"},
    3: {"step": step_rule_3, "states": 8, "cmap": "viridis"},
    4: {"step": step_rule_4, "states": 9, "cmap": "magma"},
    5: {"step": step_rule_5, "states": 6, "cmap": "nipy_spectral"},
    6: {"step": step_rule_6, "states": 7, "cmap": "gist_ncar"},
    7: {"step": step_rule_7, "states": 8, "cmap": "hot"},
    8: {"step": step_rule_8, "states": 7, "cmap": "rainbow"},
    9: {"step": step_rule_9, "states": 8, "cmap": "ocean"},
    10: {"step": step_rule_10, "states": 6, "cmap": "coolwarm"}
}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    for rule_num in range(1, 11):
        meta = rules_meta[rule_num]
        step_func = meta["step"]
        num_states = meta["states"]
        colormap_name = meta["cmap"]
        
        for seed_type in ["single_seed", "random"]:
            # Set random seed for reproducibility
            np.random.seed(42 + rule_num)
            
            grid = init_grid(rule_num, seed_type)
            space_time = np.zeros((H, W), dtype=np.uint8)
            space_time[0, :] = grid
            
            for t in range(1, H):
                grid = step_func(grid)
                space_time[t, :] = grid
                
            # Convert values to colormapped RGB image
            norm_space_time = space_time / (num_states - 1)
            cmap = plt.get_cmap(colormap_name)
            rgb_data = (cmap(norm_space_time)[:, :, :3] * 255).astype(np.uint8)
            
            # Save using PIL Image
            img = Image.fromarray(rgb_data)
            filename = f"rule_{rule_num:02d}_{seed_type}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            print(f"Saved: {filename} to {filepath}")

if __name__ == "__main__":
    main()
