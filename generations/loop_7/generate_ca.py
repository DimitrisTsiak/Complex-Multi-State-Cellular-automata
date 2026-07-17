import numpy as np
import os
from PIL import Image

# Simulation Parameters
W = 800  # Lattice width
T = 800  # Number of time steps (height of diagram)

# Rule 1: Polar Auxin & Apical Dominance (N=5)
def rule1(S):
    left1 = np.roll(S, 1)
    left2 = np.roll(S, 2)
    next_S = np.zeros_like(S)
    
    # State 3 is stable
    next_S[S == 3] = 3
    
    # State 1 becomes 3
    next_S[S == 1] = 3
    
    # State 2 becomes 4
    next_S[S == 2] = 4
    
    # State 4 becomes 0
    next_S[S == 4] = 0
    
    # State 0 transitions
    quiescent = (S == 0)
    cond1 = quiescent & (left1 == 2) & (left2 != 1)
    cond2 = quiescent & ~cond1 & ((left1 == 1) | (left1 == 2))
    
    next_S[cond1] = 1
    next_S[cond2] = 2
    
    return next_S

# Rule 2: Anchored Apical Growth (N=5)
def rule2(S):
    left = np.roll(S, 1)
    right = np.roll(S, -1)
    next_S = np.zeros_like(S)
    
    # State 3 is stable
    next_S[S == 3] = 3
    
    # State 2 becomes 3
    next_S[S == 2] = 3
    
    # State 4 becomes 0
    next_S[S == 4] = 0
    
    # State 1 matures
    tip_mask = (S == 1)
    next_S[tip_mask & (left == 2)] = 3
    next_S[tip_mask & (left != 2)] = 4
    
    # State 0 transitions
    quiescent = (S == 0)
    cond1 = quiescent & (left == 1) & (right != 4)
    cond2 = quiescent & ~cond1 & (right == 1)
    
    next_S[cond1] = 1
    next_S[cond2] = 2
    
    return next_S

# Rule 3: Chiral Turing Branching (N=5)
def rule3(S):
    is_act = (S == 1).astype(np.int8)
    is_inh = (S == 2).astype(np.int8)
    
    A = np.roll(is_act, 1) + np.roll(is_act, -1)
    I = np.roll(is_inh, 3) + np.roll(is_inh, 2) + np.roll(is_inh, 1)
    
    left = np.roll(S, 1)
    next_S = np.zeros_like(S)
    
    # State 3 is stable
    next_S[S == 3] = 3
    
    # State 4 becomes 0
    next_S[S == 4] = 0
    
    # State 2 becomes 4
    next_S[S == 2] = 4
    
    # State 1 matures
    act_mask = (S == 1)
    next_S[act_mask & (A >= 1)] = 3
    next_S[act_mask & (A < 1)] = 4
    
    # State 0 transitions
    quiescent = (S == 0)
    cond1 = quiescent & (A >= 1) & (I == 0)
    cond2 = quiescent & ~cond1 & (left == 1)
    
    next_S[cond1] = 1
    next_S[cond2] = 2
    
    return next_S

# Rule 4: Sinuous Helical Circumnutation (N=6)
def rule4(S):
    is_stem = (S == 5).astype(np.int8)
    C_L = np.roll(is_stem, 3) + np.roll(is_stem, 2) + np.roll(is_stem, 1)
    C_R = np.roll(is_stem, -1) + np.roll(is_stem, -2) + np.roll(is_stem, -3)
    
    C_L_left = np.roll(C_L, 1)
    C_R_right = np.roll(C_R, -1)
    
    left = np.roll(S, 1)
    right = np.roll(S, -1)
    
    next_S = np.zeros_like(S)
    
    # State 5 is stable
    next_S[S == 5] = 5
    
    # States 3 and 4 become 5
    next_S[(S == 3) | (S == 4)] = 5
    
    # State 1: 3 if C_L >= 2 else 5
    tip_r = (S == 1)
    next_S[tip_r & (C_L >= 2)] = 3
    next_S[tip_r & (C_L < 2)] = 5
    
    # State 2: 4 if C_R >= 2 else 5
    tip_l = (S == 2)
    next_S[tip_l & (C_R >= 2)] = 4
    next_S[tip_l & (C_R < 2)] = 5
    
    # State 0 transitions
    quiescent = (S == 0)
    cond1 = quiescent & (left == 1) & (C_L_left < 2)
    cond2 = quiescent & ~cond1 & (right == 2) & (C_R_right < 2)
    cond3 = quiescent & ~cond1 & ~cond2 & (right == 3)
    cond4 = quiescent & ~cond1 & ~cond2 & ~cond3 & (left == 4)
    
    next_S[cond1] = 1
    next_S[cond2] = 2
    next_S[cond3] = 2
    next_S[cond4] = 1
    
    return next_S

# Rule 5: Asymmetric Stem Cell Niche (N=6)
def rule5(S):
    is_diff = (S == 4).astype(np.int8)
    D = np.roll(is_diff, 1) + np.roll(is_diff, -1)
    
    left1 = np.roll(S, 1)
    left2 = np.roll(S, 2)
    
    next_S = np.zeros_like(S)
    
    # State 2 is stable
    next_S[S == 2] = 2
    
    # State 1: 1 if left1 == 2 else 3
    stem_mask = (S == 1)
    next_S[stem_mask & (left1 == 2)] = 1
    next_S[stem_mask & (left1 != 2)] = 3
    
    # State 3 becomes 4
    next_S[S == 3] = 4
    
    # State 4: 5 if D == 2 else 4
    diff_mask = (S == 4)
    next_S[diff_mask & (D == 2)] = 5
    next_S[diff_mask & (D != 2)] = 4
    
    # State 5 becomes 0
    next_S[S == 5] = 0
    
    # State 0 transitions
    quiescent = (S == 0)
    cond1 = quiescent & (left1 == 3)
    cond2 = quiescent & ~cond1 & (left1 == 1) & (left2 == 2)
    
    next_S[cond1 | cond2] = 3
    
    return next_S

# Rule 6: Vascular Lumen Formation (N=5)
def rule6(S):
    is_wall = (S == 2).astype(np.int8)
    W_count = np.roll(is_wall, 1) + np.roll(is_wall, -1)
    
    left = np.roll(S, 1)
    right = np.roll(S, -1)
    
    next_S = np.zeros_like(S)
    
    # State 1: 2 if right != 0 else 1
    tip_mask = (S == 1)
    next_S[tip_mask & (right != 0)] = 2
    next_S[tip_mask & (right == 0)] = 1
    
    # State 2: 3 if W_count == 2 else 2
    wall_mask = (S == 2)
    next_S[wall_mask & (W_count == 2)] = 3
    next_S[wall_mask & (W_count != 2)] = 2
    
    # State 3 becomes 4
    next_S[S == 3] = 4
    
    # State 4 becomes 0
    next_S[S == 4] = 0
    
    # State 0 transitions
    quiescent = (S == 0)
    cond = quiescent & (left == 1) & (right == 0)
    next_S[cond] = 1
    
    return next_S

# Rule 7: Morphogenetic French Flag Wave (N=7)
def rule7(S):
    left = np.roll(S, 1)
    next_S = np.zeros_like(S)
    
    # State 1 is stable
    next_S[S == 1] = 1
    
    # State 4, 5, 6 are stable
    stable_diff = (S == 4) | (S == 5) | (S == 6)
    next_S[stable_diff] = S[stable_diff]
    
    # State 2 becomes 3
    next_S[S == 2] = 3
    
    # State 3 transitions
    s3_mask = (S == 3)
    cond3_4 = s3_mask & ((left == 2) | (left == 3))
    cond3_5 = s3_mask & ~cond3_4 & (left == 4)
    cond3_6 = s3_mask & ~cond3_4 & ~cond3_5 & (left == 5)
    
    next_S[cond3_4] = 4
    next_S[cond3_5] = 5
    next_S[cond3_6] = 6
    # otherwise becomes 0 (which is default value in next_S)
    
    # State 0 transitions
    quiescent = (S == 0)
    cond0_2 = quiescent & ((left == 1) | (left == 2))
    next_S[cond0_2] = 2
    
    return next_S

# Rule 8: Polar Filament Dynamic Instability (N=6)
def rule8(S):
    left1 = np.roll(S, 1)
    left2 = np.roll(S, 2)
    right1 = np.roll(S, -1)
    right2 = np.roll(S, -2)
    
    next_S = np.zeros_like(S)
    
    # State 1 and 2 become 3
    next_S[(S == 1) | (S == 2)] = 3
    
    # State 4 becomes 5
    next_S[S == 4] = 5
    
    # State 5 becomes 0
    next_S[S == 5] = 0
    
    # State 3 transitions
    core_mask = (S == 3)
    catastrophe_prop = core_mask & ((left1 == 4) | (right1 == 4))
    isolated_deg = core_mask & ~catastrophe_prop & (left1 == 0) & (right1 == 0)
    
    next_S[catastrophe_prop | isolated_deg] = 4
    next_S[core_mask & ~catastrophe_prop & ~isolated_deg] = 3
    
    # State 0 transitions
    quiescent = (S == 0)
    cond0_1 = quiescent & (left1 == 1)
    cond0_2 = quiescent & ~cond0_1 & (right1 == 2) & (right2 == 3)
    
    next_S[cond0_1] = 1
    next_S[cond0_2] = 2
    
    return next_S

# Rule 9: Chiral Biofilm Shear Expansion (N=6)
def rule9(S):
    is_nut = (S == 0).astype(np.int8)
    N_nut = np.roll(is_nut, 2) + np.roll(is_nut, 1) + np.roll(is_nut, -1) + np.roll(is_nut, -2)
    
    left1 = np.roll(S, 1)
    right1 = np.roll(S, -1)
    right2 = np.roll(S, -2)
    
    next_S = np.zeros_like(S)
    
    # State 1 and 4 become 2
    next_S[(S == 1) | (S == 4)] = 2
    
    # State 2: 3 if N_nut == 0 else 2
    active_mask = (S == 2)
    next_S[active_mask & (N_nut == 0)] = 3
    next_S[active_mask & (N_nut != 0)] = 2
    
    # State 3 becomes 5
    next_S[S == 3] = 5
    
    # State 5 remains 5
    next_S[S == 5] = 5
    
    # State 0 transitions
    quiescent = (S == 0)
    cond0_1 = quiescent & (left1 == 1)
    cond0_4 = quiescent & ~cond0_1 & (right1 == 1) & (right2 != 0)
    
    next_S[cond0_1] = 1
    next_S[cond0_4] = 4
    
    return next_S

# Rule 10: Asymmetric Mycelial Branching (N=6)
def rule10(S):
    is_tip = (S == 1).astype(np.int8)
    T_count = np.roll(is_tip, 2) + np.roll(is_tip, 1) + np.roll(is_tip, -1) + np.roll(is_tip, -2)
    
    left1 = np.roll(S, 1)
    right1 = np.roll(S, -1)
    right2 = np.roll(S, -2)
    
    next_S = np.zeros_like(S)
    
    # State 1 becomes 2
    next_S[S == 1] = 2
    
    # State 2 becomes 3
    next_S[S == 2] = 3
    
    # State 3: 4 if T_count == 0 else 3
    mature_mask = (S == 3)
    next_S[mature_mask & (T_count == 0)] = 4
    next_S[mature_mask & (T_count != 0)] = 3
    
    # State 4 becomes 5
    next_S[S == 4] = 5
    
    # State 5 remains 5
    next_S[S == 5] = 5
    
    # State 0 transitions
    quiescent = (S == 0)
    cond0_main = quiescent & (left1 == 1)
    cond0_branch = quiescent & ~cond0_main & (right1 == 2) & (right2 == 3)
    
    next_S[cond0_main | cond0_branch] = 1
    
    return next_S

# Color Palettes dictionary mapping rule index to list of RGB colors (length N)
PALETTES = {
    1: [  # N=5, Apical Fire
        (15, 15, 20),      # State 0: Very dark blue
        (255, 255, 100),   # State 1: Vibrant yellow
        (255, 140, 0),     # State 2: Vibrant orange
        (34, 139, 34),     # State 3: Forest green
        (178, 34, 34)      # State 4: Firebrick red
    ],
    2: [  # N=5, Neon Coral
        (20, 20, 30),      # State 0: Dark slate blue
        (255, 0, 127),     # State 1: Neon pink/coral
        (0, 255, 255),     # State 2: Electric cyan
        (138, 43, 226),    # State 3: Blue violet
        (75, 0, 130)       # State 4: Indigo
    ],
    3: [  # N=5, Turing Emerald
        (10, 25, 15),      # State 0: Dark green-black
        (50, 255, 150),    # State 1: Spring green
        (255, 20, 147),    # State 2: Deep pink
        (0, 128, 128),     # State 3: Teal
        (47, 79, 79)       # State 4: Dark slate gray
    ],
    4: [  # N=6, Electric Helix
        (10, 10, 25),      # State 0: Very dark blue
        (0, 255, 255),     # State 1: Cyan
        (0, 255, 0),       # State 2: Green
        (255, 0, 255),     # State 3: Magenta
        (255, 255, 0),     # State 4: Yellow
        (128, 0, 255)      # State 5: Purple
    ],
    5: [  # N=6, Cyber Niche
        (15, 15, 15),      # State 0: Charcoal
        (255, 215, 0),     # State 1: Gold
        (255, 69, 0),      # State 2: Red-orange
        (0, 191, 255),     # State 3: Deep sky blue
        (0, 250, 154),     # State 4: Medium spring green
        (105, 105, 105)    # State 5: Dim gray
    ],
    6: [  # N=5, Vascular Blood
        (0, 0, 0),         # State 0: Black
        (255, 50, 50),     # State 1: Bright red
        (180, 0, 0),       # State 2: Dark red
        (255, 165, 0),     # State 3: Orange
        (70, 70, 70)       # State 4: Dark gray
    ],
    7: [  # N=7, French Flag Wave
        (30, 30, 40),      # State 0: Dark gray-blue
        (255, 255, 255),   # State 1: White organizer
        (255, 192, 203),   # State 2: Pink morphogen high
        (218, 112, 214),   # State 3: Orchid morphogen med
        (30, 144, 255),    # State 4: Dodger blue (mesoderm)
        (255, 99, 71),     # State 5: Tomato red (endoderm)
        (50, 205, 50)      # State 6: Lime green (neural crest)
    ],
    8: [  # N=6, Aurora Filament
        (10, 5, 20),       # State 0: Midnight violet
        (0, 255, 127),     # State 1: Spring green
        (0, 255, 255),     # State 2: Cyan
        (75, 0, 130),      # State 3: Indigo
        (255, 0, 0),       # State 4: Vibrant red catastrophe
        (139, 0, 139)      # State 5: Dark magenta
    ],
    9: [  # N=6, Biofilm Toxic
        (25, 25, 0),       # State 0: Dark olive yellow
        (173, 255, 47),    # State 1: Green yellow
        (0, 255, 0),       # State 2: Lime green
        (210, 180, 140),   # State 3: Tan
        (255, 127, 80),    # State 4: Coral
        (85, 107, 47)      # State 5: Dark olive green
    ],
    10: [ # N=6, Mycelium Gold
        (20, 15, 10),      # State 0: Dark soil brown
        (255, 215, 0),     # State 1: Gold tip
        (255, 165, 0),     # State 2: Orange hub
        (222, 184, 135),   # State 3: Burlywood mature
        (139, 69, 19),     # State 4: Saddlebrown senescent
        (50, 30, 20)       # State 5: Very dark brown necrotic
    ]
}

def simulate(rule_func, initial_grid):
    history = np.zeros((T, W), dtype=np.uint8)
    history[0] = initial_grid
    
    current_grid = initial_grid.copy()
    for t in range(1, T):
        current_grid = rule_func(current_grid)
        history[t] = current_grid
    return history

def main():
    output_dir = "generations/loop_7/output"
    os.makedirs(output_dir, exist_ok=True)
    
    rules = [
        (1, rule1, 5),
        (2, rule2, 5),
        (3, rule3, 5),
        (4, rule4, 6),
        (5, rule5, 6),
        (6, rule6, 5),
        (7, rule7, 7),
        (8, rule8, 6),
        (9, rule9, 6),
        (10, rule10, 6)
    ]
    
    print("Starting Cellular Automata Simulations...")
    
    for idx, rule_func, N in rules:
        print(f"Simulating Rule {idx} (N={N} states)...")
        palette = PALETTES[idx]
        
        # 1. Single Seed Initialization
        if idx == 5:
            # Stem Cell Niche requires both Niche Signal (2) and Stem Cell (1) next to it
            single_seed = np.zeros(W, dtype=np.uint8)
            single_seed[W // 2 - 1] = 2
            single_seed[W // 2] = 1
        else:
            single_seed = np.zeros(W, dtype=np.uint8)
            single_seed[W // 2] = 1
            
        history_single = simulate(rule_func, single_seed)
        palette_np = np.array(palette, dtype=np.uint8)
        
        img_single = Image.fromarray(palette_np[history_single])
        single_filename = os.path.join(output_dir, f"rule_{idx:02d}_single_seed.png")
        img_single.save(single_filename)
        print(f" Saved: {single_filename}")
        
        # 2. Random Initialization
        np.random.seed(42)  # Reproducible randomness
        p = np.zeros(N)
        p[0] = 0.70
        p[1] = 0.15
        if N > 2:
            p[2:] = 0.15 / (N - 2)
        else:
            p[0] = 0.85
            
        random_grid = np.random.choice(N, size=W, p=p).astype(np.uint8)
        history_random = simulate(rule_func, random_grid)
        
        img_random = Image.fromarray(palette_np[history_random])
        random_filename = os.path.join(output_dir, f"rule_{idx:02d}_random.png")
        img_random.save(random_filename)
        print(f" Saved: {random_filename}")
        
    print("\nAll simulations completed. Verifying output files...")
    # Verification
    all_exist = True
    for idx, _, _ in rules:
        f_single = os.path.join(output_dir, f"rule_{idx:02d}_single_seed.png")
        f_random = os.path.join(output_dir, f"rule_{idx:02d}_random.png")
        
        for f in [f_single, f_random]:
            if os.path.exists(f):
                size = os.path.getsize(f)
                print(f"  Verified {f} exists (size: {size} bytes)")
            else:
                print(f"  ERROR: {f} does not exist!")
                all_exist = False
                
    if all_exist:
        print("\nSuccess! All 20 files successfully generated and verified.")
    else:
        print("\nFailure! Some files are missing.")

if __name__ == "__main__":
    main()
