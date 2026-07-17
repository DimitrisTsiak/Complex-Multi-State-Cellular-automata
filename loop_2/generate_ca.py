import numpy as np
import os
from PIL import Image

# Simulation Parameters
W = 800  # Lattice width
T = 800  # Number of time steps (height of diagram)

# Rule 1: Standard Generations Baseline (N=4)
def rule1(S):
    is_active = (S == 1).astype(np.int8)
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    next_S = np.zeros_like(S)
    
    # S == 0 and A == 2 -> Birth
    birth = (S == 0) & (A == 2)
    next_S[birth] = 1
    
    # S == 1 and A in {1, 2} -> Survival
    survival = (S == 1) & ((A == 1) | (A == 2))
    next_S[survival] = 1
    
    # S == 1 and A not in {1, 2} -> Decay start (to 2)
    decay_start = (S == 1) & ~((A == 1) | (A == 2))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 4
    
    return next_S

# Rule 2: Parity-Gated Birth Generations (N=5)
def rule2(S):
    is_active = (S == 1).astype(np.int8)
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    next_S = np.zeros_like(S)
    
    # S == 0 and A in {1, 3} -> Birth
    birth = (S == 0) & ((A == 1) | (A == 3))
    next_S[birth] = 1
    
    # S == 1 and A in {1, 2} -> Survival
    survival = (S == 1) & ((A == 1) | (A == 2))
    next_S[survival] = 1
    
    # S == 1 and A not in {1, 2} -> Decay start
    decay_start = (S == 1) & ~((A == 1) | (A == 2))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    
    return next_S

# Rule 3: Refractory-Feedback Generations (N=6)
def rule3(S):
    is_active = (S == 1).astype(np.int8)
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    next_S = np.zeros_like(S)
    
    # S == 0 and A in {2, 3} -> Birth
    birth = (S == 0) & ((A == 2) | (A == 3))
    next_S[birth] = 1
    
    # S == 1 and A == 2 -> Survival
    survival = (S == 1) & (A == 2)
    next_S[survival] = 1
    
    # S == 1 and A != 2 -> Decay start
    decay_start = (S == 1) & (A != 2)
    next_S[decay_start] = 2
    
    # S >= 2
    refractory = (S >= 2)
    # A >= 3 -> resist decay
    resist = refractory & (A >= 3)
    next_S[resist] = S[resist]
    # A < 3 -> progress decay
    decay = refractory & (A < 3)
    next_S[decay] = (S[decay] + 1) % 6
    
    return next_S

# Rule 4: Chiral Drifting Generations (N=4)
def rule4(S):
    is_active = (S == 1).astype(np.int8)
    # W(x) = S(x-3) + S(x-2) + 2*S(x-1) + S(x+1)
    W = np.roll(is_active, 3) + np.roll(is_active, 2) + 2 * np.roll(is_active, 1) + np.roll(is_active, -1)
    next_S = np.zeros_like(S)
    
    # S == 0 and W in {2, 3} -> Birth
    birth = (S == 0) & ((W == 2) | (W == 3))
    next_S[birth] = 1
    
    # S == 1 and W in {1, 2, 3} -> Survival
    survival = (S == 1) & ((W >= 1) & (W <= 3))
    next_S[survival] = 1
    
    # S == 1 and W not in {1, 2, 3} -> Decay start
    decay_start = (S == 1) & ~((W >= 1) & (W <= 3))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 4
    
    return next_S

# Rule 5: Dual-Threshold Density Generations (N=5)
def rule5(S):
    is_active = (S == 1).astype(np.int8)
    # Radius 3 excluding cell itself
    A = (np.roll(is_active, 3) + np.roll(is_active, 2) + np.roll(is_active, 1) +
         np.roll(is_active, -1) + np.roll(is_active, -2) + np.roll(is_active, -3))
    next_S = np.zeros_like(S)
    
    # S == 0 and A in {2, 4} -> Birth
    birth = (S == 0) & ((A == 2) | (A == 4))
    next_S[birth] = 1
    
    # S == 1 and A in {2, 3, 5} -> Survival
    survival = (S == 1) & ((A == 2) | (A == 3) | (A == 5))
    next_S[survival] = 1
    
    # S == 1 and A not in {2, 3, 5} -> Decay start
    decay_start = (S == 1) & ~((A == 2) | (A == 3) | (A == 5))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    
    return next_S

# Rule 6: Refractory-Inhibited Birth Generations (N=5)
def rule6(S):
    is_active = (S == 1).astype(np.int8)
    is_refractory = (S >= 2).astype(np.int8)
    
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    R = np.roll(is_refractory, 2) + np.roll(is_refractory, 1) + np.roll(is_refractory, -1) + np.roll(is_refractory, -2)
    next_S = np.zeros_like(S)
    
    # S == 0 and A == 2 and R <= 1 -> Birth
    birth = (S == 0) & (A == 2) & (R <= 1)
    next_S[birth] = 1
    
    # S == 1 and A in {1, 2} -> Survival
    survival = (S == 1) & ((A == 1) | (A == 2))
    next_S[survival] = 1
    
    # S == 1 and A not in {1, 2} -> Decay start
    decay_start = (S == 1) & ~((A == 1) | (A == 2))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    
    return next_S

# Rule 7: Totalistic-Sum Generations (N=5)
def rule7(S):
    K = np.roll(S, 2) + np.roll(S, 1) + S + np.roll(S, -1) + np.roll(S, -2)
    next_S = np.zeros_like(S)
    
    # S == 0 and K in {3, 4, 5, 6} -> Birth
    birth = (S == 0) & (K >= 3) & (K <= 6)
    next_S[birth] = 1
    
    # S == 1 and K in {4, 5, 6, 7} -> Survival
    survival = (S == 1) & (K >= 4) & (K <= 7)
    next_S[survival] = 1
    
    # S == 1 and K not in {4, 5, 6, 7} -> Decay start
    decay_start = (S == 1) & ~((K >= 4) & (K <= 7))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 5
    
    return next_S

# Rule 8: Velocity-Modulated Range-Shifting (N=6)
def rule8(S):
    is_active = (S == 1).astype(np.int8)
    is_refractory = (S >= 2).astype(np.int8)
    
    # R is the refractory count in N1 (radius 1)
    R = np.roll(is_refractory, 1) + np.roll(is_refractory, -1)
    
    # A1 is active count in N1 (radius 1)
    A1 = np.roll(is_active, 1) + np.roll(is_active, -1)
    
    # A2 is active count in N2 (radius 2)
    A2 = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    
    # R >= 1 => N_use = N2, B = S = {2, 3}
    # R == 0 => N_use = N1, B = S = {1}
    birth_A = (A2 == 2) | (A2 == 3)
    survival_A = (A2 == 2) | (A2 == 3)
    
    birth_B = (A1 == 1)
    survival_B = (A1 == 1)
    
    use_A = (R >= 1)
    birth = np.where(use_A, birth_A, birth_B)
    survival = np.where(use_A, survival_A, survival_B)
    
    next_S = np.zeros_like(S)
    
    # S == 0 and birth -> Birth
    birth_mask = (S == 0) & birth
    next_S[birth_mask] = 1
    
    # S == 1 and survival -> Survival
    survival_mask = (S == 1) & survival
    next_S[survival_mask] = 1
    
    # S == 1 and not survival -> Decay start
    decay_start_mask = (S == 1) & ~survival
    next_S[decay_start_mask] = 2
    
    # S >= 2 -> Decay progression
    refractory_mask = (S >= 2)
    next_S[refractory_mask] = (S[refractory_mask] + 1) % 6
    
    return next_S

# Rule 9: Chaotic-Gate Generations (N=8)
def rule9(S):
    is_active = (S == 1).astype(np.int8)
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    
    S_int = S.astype(np.int32)
    V = (1 * np.roll(S_int, 2) + 
         2 * np.roll(S_int, 1) + 
         3 * S_int + 
         4 * np.roll(S_int, -1) + 
         5 * np.roll(S_int, -2))
    
    next_S = np.zeros_like(S)
    
    # S == 0 and A == 2 and V % 3 != 0 -> Birth
    birth = (S == 0) & (A == 2) & ((V % 3) != 0)
    next_S[birth] = 1
    
    # S == 1 and A in {1, 2} -> Survival
    survival = (S == 1) & ((A == 1) | (A == 2))
    next_S[survival] = 1
    
    # S == 1 and A not in {1, 2} -> Decay start
    decay_start = (S == 1) & ~((A == 1) | (A == 2))
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 8
    
    return next_S

# Rule 10: Mutual-Exclusion Generations (N=6)
def rule10(S):
    is_active = (S == 1).astype(np.int8)
    is_d2 = (S == 2).astype(np.int8)
    
    A = np.roll(is_active, 2) + np.roll(is_active, 1) + np.roll(is_active, -1) + np.roll(is_active, -2)
    D = np.roll(is_d2, 2) + np.roll(is_d2, 1) + np.roll(is_d2, -1) + np.roll(is_d2, -2)
    
    next_S = np.zeros_like(S)
    
    # S == 0 and A == 2 and D % 2 == 0 -> Birth
    birth = (S == 0) & (A == 2) & ((D % 2) == 0)
    next_S[birth] = 1
    
    # S == 1 and A in {1, 2} and D <= 1 -> Survival
    survival = (S == 1) & ((A == 1) | (A == 2)) & (D <= 1)
    next_S[survival] = 1
    
    # S == 1 and otherwise -> Decay start
    decay_start = (S == 1) & ~survival
    next_S[decay_start] = 2
    
    # S >= 2 -> Decay progression
    refractory = (S >= 2)
    next_S[refractory] = (S[refractory] + 1) % 6
    
    return next_S


# Color Palettes dictionary mapping rule index to list of RGB colors (length N)
PALETTES = {
    1: [  # N=4, Electric Cyan
        (10, 15, 30),      # State 0: Deep space blue
        (0, 255, 255),     # State 1: Neon Cyan
        (0, 128, 255),     # State 2: Electric blue
        (0, 0, 150)        # State 3: Dark blue
    ],
    2: [  # N=5, Sunset Fire
        (15, 10, 15),      # State 0: Dark purple-black
        (255, 220, 0),     # State 1: Vibrant gold
        (255, 100, 0),     # State 2: Bright orange
        (220, 20, 60),     # State 3: Crimson red
        (100, 0, 50)       # State 4: Deep plum
    ],
    3: [  # N=6, Forest Acid
        (10, 20, 10),      # State 0: Dark forest floor
        (50, 255, 50),     # State 1: Acid lime green
        (0, 200, 100),     # State 2: Emerald
        (0, 150, 150),     # State 3: Teal
        (0, 80, 120),      # State 4: Ocean blue
        (40, 20, 80)       # State 5: Deep night violet
    ],
    4: [  # N=4, Purple Rain
        (15, 5, 20),       # State 0: Dark mauve
        (255, 50, 255),    # State 1: Neon magenta
        (150, 0, 200),     # State 2: Violet
        (70, 0, 120)       # State 3: Deep indigo
    ],
    5: [  # N=5, Cyberpunk Grid
        (20, 10, 25),      # State 0: Night city dark blue
        (255, 0, 128),     # State 1: Hot pink
        (0, 240, 200),     # State 2: Turquoise
        (180, 255, 0),     # State 3: Yellow-green
        (80, 0, 150)       # State 4: Purple haze
    ],
    6: [  # N=5, Autumn Leaves
        (25, 20, 15),      # State 0: Dark warm grey
        (255, 215, 0),     # State 1: Golden yellow
        (244, 164, 96),    # State 2: Sandy orange
        (210, 105, 30),    # State 3: Rust chocolate
        (139, 69, 19)      # State 4: Saddle brown
    ],
    7: [  # N=5, Graded Diffusion
        (10, 10, 10),      # State 0: Charcoal black
        (255, 255, 255),   # State 1: Pure white
        (191, 255, 0),     # State 2: Lime green
        (34, 139, 34),     # State 3: Forest green
        (0, 80, 0)         # State 4: Dark green shadow
    ],
    8: [  # N=6, Aurora Sky
        (5, 5, 15),        # State 0: Midnight black
        (0, 255, 150),     # State 1: Aurora green
        (0, 200, 255),     # State 2: Neon cyan
        (100, 100, 255),   # State 3: Electric blue
        (180, 50, 255),    # State 4: Aurora violet
        (80, 0, 120)       # State 5: Deep magenta
    ],
    9: [  # N=8, Rainbow Chaos
        (15, 15, 15),      # State 0: Dark gray
        (255, 0, 0),       # State 1: Vibrant red
        (255, 127, 0),     # State 2: Orange
        (255, 255, 0),     # State 3: Yellow
        (0, 255, 0),       # State 4: Green
        (0, 0, 255) ,      # State 5: Blue
        (75, 0, 130),      # State 6: Indigo
        (148, 0, 211)      # State 7: Purple
    ],
    10: [ # N=6, Ice Palace
        (10, 20, 25),      # State 0: Dark slate teal
        (255, 255, 255),   # State 1: Glacial white
        (127, 255, 212),   # State 2: Aquamarine
        (72, 209, 204),    # State 3: Ice turquoise
        (0, 128, 128),     # State 4: Glacial teal
        (25, 25, 112)      # State 5: Midnight blue
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
    output_dir = "loop_2/output"
    os.makedirs(output_dir, exist_ok=True)
    
    rules = [
        (1, rule1, 4),
        (2, rule2, 5),
        (3, rule3, 6),
        (4, rule4, 4),
        (5, rule5, 5),
        (6, rule6, 5),
        (7, rule7, 5),
        (8, rule8, 6),
        (9, rule9, 8),
        (10, rule10, 6)
    ]
    
    print("Starting Cellular Automata Simulations...")
    
    for idx, rule_func, N in rules:
        print(f"Simulating Rule {idx} (N={N} states)...")
        palette = PALETTES[idx]
        
        # 1. Single Seed Initialization
        single_seed = np.zeros(W, dtype=np.uint8)
        single_seed[W // 2] = 1
        
        history_single = simulate(rule_func, single_seed)
        palette_np = np.array(palette, dtype=np.uint8)
        
        img_single = Image.fromarray(palette_np[history_single])
        single_filename = os.path.join(output_dir, f"rule_{idx:02d}_single_seed.png")
        img_single.save(single_filename)
        print(f" Saved: {single_filename}")
        
        # 2. Random Initialization
        np.random.seed(42) # Reproducible randomness
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
