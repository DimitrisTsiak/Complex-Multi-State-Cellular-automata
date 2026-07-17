import os
import numpy as np
import PIL.Image

# Simulation Parameters
STEPS = 800
WIDTH = 800
OUTPUT_DIR = "generations/loop_9/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_initial_grid(init_type, num_states, seed_val=1):
    if init_type in ("single", "single_seed"):
        grid = np.zeros(WIDTH, dtype=int)
        grid[WIDTH // 2] = seed_val
        return grid
    elif init_type == "random":
        return np.random.randint(0, num_states, size=WIDTH)
    else:
        raise ValueError(f"Unknown initialization type: {init_type}")

def save_image(history, palette, filename):
    h, w = history.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for state, color in palette.items():
        rgb[history == state] = color
    img = PIL.Image.fromarray(rgb)
    img.save(filename)
    print(f"Saved: {filename}")

# --- Rule Implementations ---

def run_rule_1(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 3, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        N1 = (S_l2 == 1).astype(int) + (S_l1 == 1).astype(int) + (S_r1 == 1).astype(int) + (S_r2 == 1).astype(int)
        N2 = (S_l2 == 2).astype(int) + (S_l1 == 2).astype(int) + (S_r1 == 2).astype(int) + (S_r2 == 2).astype(int)
        D = N1 + N2
        
        S_next = np.zeros_like(S)
        
        mask1 = (S == 1)
        S_next[mask1 & (D >= 1) & (N1 >= N2)] = 1
        
        mask2 = (S == 2)
        S_next[mask2 & (D >= 1) & (N2 >= N1)] = 2
        
        mask0 = (S == 0)
        S_next[mask0 & (N1 > N2) & (N1 >= 2)] = 1
        S_next[mask0 & (N2 > N1) & (N2 >= 2)] = 2
        
        history[t] = S_next
    return history

def run_rule_2(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 4, seed_val=3)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    payoff_matrix = np.array([[3, 0], [5, 1]]) # [self_strat, opp_strat]
    
    for t in range(1, steps):
        S = history[t-1]
        strat = (S >= 2).astype(int)
        strat_l = np.roll(strat, 1)
        strat_r = np.roll(strat, -1)
        
        P = payoff_matrix[strat, strat_l] + payoff_matrix[strat, strat_r]
        
        P_self = P
        P_left = np.roll(P, 1)
        P_right = np.roll(P, -1)
        
        S_left = np.roll(S, 1)
        S_right = np.roll(S, -1)
        
        P_star = P.copy()
        S_star = S.copy()
        
        mask_l = P_left > P_star
        P_star[mask_l] = P_left[mask_l]
        S_star[mask_l] = S_left[mask_l]
        
        mask_r = P_right > P_star
        P_star[mask_r] = P_right[mask_r]
        S_star[mask_r] = S_right[mask_r]
        
        strat_new = (S_star >= 2)
        S_next = np.zeros_like(S)
        S_next[~strat_new] = np.where(P_star[~strat_new] >= 4, 1, 0)
        S_next[strat_new] = np.where(P_star[strat_new] >= 6, 3, 2)
        
        history[t] = S_next
    return history

def run_rule_3(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 5, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    payoff_matrix = np.zeros((5, 5), dtype=int)
    payoff_matrix[1, 1] = -2
    payoff_matrix[1, 2] = 4
    payoff_matrix[2, 1] = 0
    payoff_matrix[2, 2] = 2
    
    for t in range(1, steps):
        S = history[t-1]
        S_l = np.roll(S, 1)
        S_r = np.roll(S, -1)
        
        P = payoff_matrix[S, S_l] + payoff_matrix[S, S_r]
        
        S_next = np.zeros_like(S)
        
        mask1 = (S == 1)
        S_next[mask1] = np.where(P[mask1] > 0, 1, 3)
        
        mask2 = (S == 2)
        S_next[mask2] = np.where(P[mask2] > 0, 2, 3)
        
        mask3 = (S == 3)
        S_next[mask3] = 4
        
        mask4 = (S == 4)
        S_next[mask4] = 0
        
        mask0 = (S == 0)
        H = (S_l == 1).astype(int) + (S_r == 1).astype(int)
        D_count = (S_l == 2).astype(int) + (S_r == 2).astype(int)
        
        cond_h = (H >= 1) & (H >= D_count)
        cond_d = (D_count >= 1) & (D_count > H)
        
        S_next[mask0 & cond_h] = 1
        S_next[mask0 & cond_d] = 2
        
        history[t] = S_next
    return history

def run_rule_4(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 6, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        L = (S_l2 <= 2).astype(int) + (S_l1 <= 2).astype(int) + (S_r1 <= 2).astype(int) + (S_r2 <= 2).astype(int)
        R = (S_l2 >= 3).astype(int) + (S_l1 >= 3).astype(int) + (S_r1 >= 3).astype(int) + (S_r2 >= 3).astype(int)
        
        S_next = np.zeros_like(S)
        
        # Case 1: L > R
        mask_l = (L > R)
        S_next[mask_l & (S == 2)] = 1
        S_next[mask_l & (S == 1)] = 0
        S_next[mask_l & (S == 0)] = 3
        S_next[mask_l & (S == 3)] = 4
        S_next[mask_l & (S == 4)] = 5
        S_next[mask_l & (S == 5)] = 5
        
        # Case 2: R > L
        mask_r = (R > L)
        S_next[mask_r & (S == 5)] = 4
        S_next[mask_r & (S == 4)] = 3
        S_next[mask_r & (S == 3)] = 0
        S_next[mask_r & (S == 0)] = 1
        S_next[mask_r & (S == 1)] = 2
        S_next[mask_r & (S == 2)] = 2
        
        # Case 3: L == R
        mask_e = (L == R)
        S_next[mask_e & (S == 2)] = 1
        S_next[mask_e & (S == 1)] = 0
        S_next[mask_e & (S == 0)] = 0
        S_next[mask_e & (S == 5)] = 4
        S_next[mask_e & (S == 4)] = 3
        S_next[mask_e & (S == 3)] = 3
        
        history[t] = S_next
    return history

def run_rule_5(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 5, seed_val=2)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
        S_l = np.roll(S, 1)
        S_r = np.roll(S, -1)
        
        D = (S_l == 0).astype(int) + (S_r == 0).astype(int)
        P = (S_l == 2).astype(int) + (S_r == 2).astype(int)
        C = np.isin(S_l, [1, 4]).astype(int) + np.isin(S_r, [1, 4]).astype(int)
        
        S_next = np.zeros_like(S)
        
        mask0 = (S == 0)
        S_next[mask0] = np.where(P[mask0] >= 1, 4, np.where((C[mask0] == 0) & (P[mask0] == 0), 1, 0))
        
        mask1 = (S == 1)
        S_next[mask1] = np.where((D[mask1] >= 1) & (P[mask1] == 0), 0, np.where((C[mask1] >= 1) & (D[mask1] == 0), 2, 1))
        
        mask2 = (S == 2)
        S_next[mask2] = np.where(D[mask2] >= 1, 3, 2)
        
        mask3 = (S == 3)
        S_next[mask3] = 1
        
        mask4 = (S == 4)
        S_next[mask4] = 0
        
        history[t] = S_next
    return history

def run_rule_6(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 5, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        N1 = (S_l2 == 1).astype(int) + (S_l1 == 1).astype(int) + (S_r1 == 1).astype(int) + (S_r2 == 1).astype(int)
        N2 = (S_l2 == 2).astype(int) + (S_l1 == 2).astype(int) + (S_r1 == 2).astype(int) + (S_r2 == 2).astype(int)
        N3 = (S_l2 == 3).astype(int) + (S_l1 == 3).astype(int) + (S_r1 == 3).astype(int) + (S_r2 == 3).astype(int)
        N4 = (S_l2 == 4).astype(int) + (S_l1 == 4).astype(int) + (S_r1 == 4).astype(int) + (S_r2 == 4).astype(int)
        
        S_next = np.zeros_like(S)
        
        max_seg = np.maximum(N1, np.maximum(N2, N3))
        for k, Nk in [(1, N1), (2, N2), (3, N3)]:
            mask = (S == k)
            cond = (Nk >= 1) & (Nk >= max_seg)
            S_next[mask] = np.where(cond[mask], k, 0)
            
        mask4 = (S == 4)
        ActiveStates = (N1 > 0).astype(int) + (N2 > 0).astype(int) + (N3 > 0).astype(int) + (N4 > 0).astype(int)
        max_all = np.maximum(np.maximum(N1, N2), np.maximum(N3, N4))
        cond4 = (ActiveStates >= 2) & (max_all <= 2)
        S_next[mask4] = np.where(cond4[mask4], 4, 0)
        
        mask0 = (S == 0)
        eq_count = (N1 == max_seg).astype(int) + (N2 == max_seg).astype(int) + (N3 == max_seg).astype(int)
        cond_seg = (eq_count == 1) & (max_seg >= 2)
        
        k_val = np.zeros_like(S)
        k_val[N1 == max_seg] = 1
        k_val[N2 == max_seg] = 2
        k_val[N3 == max_seg] = 3
        
        S_next[mask0] = np.where(cond_seg[mask0], k_val[mask0], np.where(N4[mask0] >= 2, 4, 0))
        
        history[t] = S_next
    return history

def run_rule_7(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 4, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    payoff_matrix = np.zeros((4, 4), dtype=int)
    payoff_matrix[1, 1] = -2
    payoff_matrix[1, 2] = 4
    payoff_matrix[1, 3] = -2
    payoff_matrix[2, 1] = 0
    payoff_matrix[2, 2] = 2
    payoff_matrix[2, 3] = 2
    payoff_matrix[3, 1] = -2
    payoff_matrix[3, 2] = 2
    payoff_matrix[3, 3] = 2
    
    for t in range(1, steps):
        S = history[t-1]
        S_l = np.roll(S, 1)
        S_r = np.roll(S, -1)
        
        P = payoff_matrix[S, S_l] + payoff_matrix[S, S_r]
        
        P_self = P
        P_left = np.roll(P, 1)
        P_right = np.roll(P, -1)
        
        S_left = np.roll(S, 1)
        S_right = np.roll(S, -1)
        
        P_star = P.copy()
        S_star = S.copy()
        
        mask_l = P_left > P_star
        P_star[mask_l] = P_left[mask_l]
        S_star[mask_l] = S_left[mask_l]
        
        mask_r = P_right > P_star
        P_star[mask_r] = P_right[mask_r]
        S_star[mask_r] = S_right[mask_r]
        
        S_next = np.zeros_like(S)
        cond_neg = P_star < 0
        S_next[cond_neg] = 0
        S_next[~cond_neg] = np.where(S_star[~cond_neg] >= 1, S_star[~cond_neg], S[~cond_neg])
        
        history[t] = S_next
    return history

def run_rule_8(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 6, seed_val=4)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
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
        
        history[t] = S_next
    return history

def run_rule_9(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 7, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    for t in range(1, steps):
        S = history[t-1]
        S_l2 = np.roll(S, 2)
        S_l1 = np.roll(S, 1)
        S_r1 = np.roll(S, -1)
        S_r2 = np.roll(S, -2)
        
        B = (S_l2 == 1).astype(int) + (S_l1 == 1).astype(int) + (S_r1 == 1).astype(int) + (S_r2 == 1).astype(int)
        SB = (S_l2 == 2).astype(int) + (S_l1 == 2).astype(int) + (S_r1 == 2).astype(int) + (S_r2 == 2).astype(int)
        D = (S_l2 == 5).astype(int) + (S_l1 == 5).astype(int) + (S_r1 == 5).astype(int) + (S_r2 == 5).astype(int)
        Spreading = B + SB
        
        S_next = np.zeros_like(S)
        
        mask0 = (S == 0)
        cond_prot = (Spreading >= 2) & (D >= 1)
        cond_conv = (B >= 2)
        cond_skep = (Spreading >= 2)
        S_next[mask0] = np.where(cond_prot[mask0], 4, np.where(cond_conv[mask0], 1, np.where(cond_skep[mask0], 2, 0)))
        
        mask1 = (S == 1)
        S_next[mask1] = np.where(D[mask1] >= 1, 4, 2)
        
        mask2 = (S == 2)
        S_next[mask2] = 3
        
        mask3 = (S == 3)
        S_next[mask3] = 6
        
        mask4 = (S == 4)
        S_next[mask4] = np.where(B[mask4] >= 3, 2, 5)
        
        mask5 = (S == 5)
        S_next[mask5] = 6
        
        mask6 = (S == 6)
        S_next[mask6] = 0
        
        history[t] = S_next
    return history

def run_rule_10(init_type, steps=STEPS, W=WIDTH):
    grid = get_initial_grid(init_type, 5, seed_val=1)
    history = np.zeros((steps, W), dtype=np.uint8)
    history[0] = grid
    
    G_matrix = np.zeros((5, 5), dtype=int)
    O_val = np.array([2, 5, 8, 2, 5])
    T_val = np.array([1, 5, 3, 5, 5])
    for s1 in range(5):
        for s2 in range(5):
            prop = (10 - O_val[s1]) if (O_val[s1] >= T_val[s2]) else 0
            resp = O_val[s2] if (O_val[s2] >= T_val[s1]) else 0
            G_matrix[s1, s2] = prop + resp
            
    for t in range(1, steps):
        S = history[t-1]
        S_l = np.roll(S, 1)
        S_r = np.roll(S, -1)
        
        P = G_matrix[S, S_l] + G_matrix[S, S_r]
        
        P_self = P
        P_left = np.roll(P, 1)
        P_right = np.roll(P, -1)
        
        S_left = np.roll(S, 1)
        S_right = np.roll(S, -1)
        
        P_star = P.copy()
        S_star = S.copy()
        
        mask_l = P_left > P_star
        P_star[mask_l] = P_left[mask_l]
        S_star[mask_l] = S_left[mask_l]
        
        mask_r = P_right > P_star
        P_star[mask_r] = P_right[mask_r]
        S_star[mask_r] = S_right[mask_r]
        
        S_next = np.where(S_star != 4, S_star, S)
        
        history[t] = S_next
    return history

# --- Color Palettes ---

palettes = {
    1: {
        0: [15, 15, 15],       # Dark Gray/Black (Vacant)
        1: [255, 50, 50],      # Bright Red
        2: [50, 100, 255]      # Bright Blue
    },
    2: {
        0: [20, 20, 20],       # Near Black (Poor C)
        1: [0, 255, 200],      # Bright Cyan (Rich C)
        2: [255, 100, 0],      # Orange (Poor D)
        3: [255, 255, 0]       # Yellow (Rich D)
    },
    3: {
        0: [30, 0, 50],        # Dark Indigo (Resource Ready)
        1: [255, 69, 0],       # Red-Orange (Hawk)
        2: [0, 200, 100],      # Emerald Green (Dove)
        3: [100, 50, 0],       # Dark Brown (Depleted 1)
        4: [200, 150, 50]      # Ochre/Gold (Depleted 2)
    },
    4: {
        0: [0, 128, 128],      # Teal
        1: [0, 191, 255],      # DeepSkyBlue
        2: [0, 0, 255],        # Blue
        3: [255, 215, 0],      # Gold
        4: [255, 69, 0],       # OrangeRed
        5: [255, 0, 255]       # Magenta
    },
    5: {
        0: [10, 10, 10],       # Charcoal
        1: [135, 206, 250],    # LightSkyBlue
        2: [148, 0, 211],      # DarkViolet
        3: [178, 34, 34],      # Firebrick
        4: [50, 205, 50]       # LimeGreen
    },
    6: {
        0: [25, 25, 25],       # Dark gray
        1: [255, 0, 100],      # Hot Pink
        2: [50, 205, 50],      # Lime Green
        3: [0, 191, 255],      # Deep Sky Blue
        4: [255, 215, 0]       # Gold
    },
    7: {
        0: [5, 5, 15],         # Very Dark Navy
        1: [255, 30, 30],      # Neon Red
        2: [30, 255, 30],      # Neon Green
        3: [30, 200, 255]      # Electric Blue
    },
    8: {
        0: [15, 10, 20],       # Dark Purple/Black
        1: [139, 69, 19],      # SaddleBrown
        2: [218, 165, 32],     # GoldenRod
        3: [0, 128, 128],      # Teal
        4: [255, 255, 255],    # White
        5: [255, 0, 0]         # Red
    },
    9: {
        0: [20, 24, 30],       # Dark Slate
        1: [255, 140, 0],      # DarkOrange
        2: [240, 128, 128],     # LightCoral
        3: [112, 128, 144],     # SlateGray
        4: [255, 255, 50],     # Yellow
        5: [255, 20, 147],     # DeepPink
        6: [127, 255, 212]     # Aquamarine
    },
    10: {
        0: [40, 0, 80],        # Indigo
        1: [0, 255, 255],      # Cyan
        2: [255, 223, 0],      # Golden Yellow
        3: [255, 0, 128],      # Dark Pink
        4: [230, 230, 250]     # Lavender
    }
}

rules_fns = {
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

def main():
    for rule_num in range(1, 11):
        print(f"Simulating Rule {rule_num}...")
        fn = rules_fns[rule_num]
        palette = palettes[rule_num]
        
        # Single Seed
        history_single = fn("single_seed")
        save_image(history_single, palette, f"{OUTPUT_DIR}/rule_{rule_num:02d}_single_seed.png")
        
        # Random
        history_random = fn("random")
        save_image(history_random, palette, f"{OUTPUT_DIR}/rule_{rule_num:02d}_random.png")

if __name__ == "__main__":
    main()
