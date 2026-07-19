import os
import numpy as np
from PIL import Image

def create_output_dir():
    os.makedirs("generations/loop_25/output", exist_ok=True)

# Define color palettes (RGB list of lists)
PALETTES = {
    1: [
        [15, 15, 20],      # 0: Dark background
        [40, 50, 90],      # 1: Dark Slate Blue
        [0, 180, 180],     # 2: Teal/Cyan
        [50, 220, 100],    # 3: Bright Green
        [255, 220, 0],     # 4: Neon Yellow
        [255, 60, 60]      # 5: Neon Red/Orange
    ],
    2: [
        [10, 10, 10],      # 0: Pitch Black (burnt)
        [34, 139, 34],     # 1: Sapling Green-Brown
        [0, 255, 100],     # 2: Vibrant Emerald Green (mature)
        [255, 69, 0]       # 3: Electric Orange-Red (burning)
    ],
    3: [
        [20, 24, 30],      # 0: Deep Slate Gray
        [75, 0, 130],      # 1: Dull Indigo
        [186, 85, 211],    # 2: Magenta/Purple
        [138, 43, 226],    # 3: Bright Violet
        [0, 230, 255]      # 4: Electric Cyan/Blue (avalanche)
    ],
    4: [
        [5, 5, 10],        # 0: Dark Obsidian
        [60, 20, 60],      # 1: Deep Plum
        [120, 10, 40],     # 2: Deep Crimson
        [180, 40, 20],     # 3: Red-Orange
        [220, 100, 10],    # 4: Amber
        [240, 180, 20],    # 5: Gold
        [200, 240, 30],    # 6: Yellow-Green
        [0, 255, 255]      # 7: Bright Electric White/Cyan
    ],
    5: [
        [25, 20, 15],      # 0: Dark Warm Brown
        [70, 50, 30],      # 1: Medium Brown
        [100, 100, 50],    # 2: Olive
        [0, 120, 140],     # 3: Damp Teal
        [0, 180, 240],     # 4: Bright Ocean Blue
        [100, 255, 255]    # 5: Neon Sky Blue/White (saturated runoff)
    ],
    6: [
        [10, 15, 30],      # 0: Deep Midnight Blue
        [48, 25, 100],     # 1: Indigo
        [100, 40, 160],    # 2: Medium Purple
        [220, 50, 150],    # 3: Hot Pink
        [255, 120, 0],     # 4: Neon Orange
        [255, 255, 50]     # 5: Lemon Yellow
    ],
    7: [
        [12, 12, 12],      # 0: Pitch Black (susceptible)
        [57, 255, 20],     # 1: Neon Lime Green (infected)
        [0, 0, 180],       # 2: Dark Royal Blue (early immune)
        [0, 100, 255],     # 3: Medium Blue (late immune)
        [255, 0, 255]      # 4: Hot Purple/Magenta (critical)
    ],
    8: [
        [18, 18, 18],      # 0: Dark Charcoal
        [10, 60, 30],      # 1: Deep Forest Green
        [100, 180, 100],   # 2: Pale Green
        [255, 255, 150],   # 3: Neon White-Yellow (firing)
        [80, 0, 120],      # 4: Deep Violet (refractory 1)
        [30, 45, 60]       # 5: Deep Blue-Gray (refractory 2)
    ],
    9: [
        [25, 30, 35],      # 0: Slate Gray
        [80, 60, 20],      # 1: Dark Ochre
        [140, 100, 30],    # 2: Brownish Yellow
        [220, 120, 20],    # 3: Vibrant Orange
        [240, 60, 20],     # 4: Vermilion
        [255, 0, 180],     # 5: Bright Magenta
        [200, 255, 255]    # 6: Neon Cyan/White (landslide flow)
    ],
    10: [
        [15, 15, 15],      # 0: Dark Gray/Black (burnt)
        [34, 50, 34],      # 1: Deep Mud Green (low density fuel)
        [34, 120, 34],     # 2: Forest Green (medium density fuel)
        [120, 180, 40],    # 3: Bright Olive Green (high density fuel)
        [180, 30, 0],      # 4: Smoldering Red (smoldering)
        [255, 160, 0],     # 5: Bright Flaming Yellow-Orange (flaming)
        [230, 200, 255]    # 6: Electric Purple-White (pyroclastic flash)
    ]
}

# ----------------- Transition functions for each rule -----------------

def run_rule_1(width, steps, init_type):
    # Stochastic Sandpile Cascade
    # N=6
    S = np.zeros(width, dtype=np.int32)
    p_d = 0.02
    
    if init_type == "single_seed":
        # Stable background (mix of 2 and 3)
        S = np.random.choice([2, 3], size=width, p=[0.5, 0.5])
        S[width // 2] = 5
        p_d = 0.005  # lower deposition for cleaner seed avalanches
    else:
        # Random initial configuration
        S = np.random.choice([0, 1, 2, 3], size=width, p=[0.1, 0.2, 0.4, 0.3])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi = np.random.binomial(1, p_d, size=width)
        T = (S >= 4).astype(np.int32)
        T_left = np.roll(T, 1)
        T_right = np.roll(T, -1)
        S = np.clip(S + xi - 2 * T + T_left + T_right, 0, 5)
        history[t + 1] = S
    
    return history

def run_rule_2(width, steps, init_type):
    # Probabilistic Forest Fire
    # N=4
    # State 0: empty, 1: sapling, 2: mature, 3: burning
    S = np.zeros(width, dtype=np.int32)
    p_g = 0.03
    p_m = 0.02
    p_l = 0.001
    p_f = 0.8
    
    if init_type == "single_seed":
        # All mature trees, center burning
        S.fill(2)
        S[width // 2] = 3
        # In single seed, minimize lightning so only the seed propagates
        p_l = 0.0
        p_g = 0.005
        p_m = 0.005
    else:
        S = np.random.choice([0, 1, 2], size=width, p=[0.4, 0.3, 0.3])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_g = np.random.binomial(1, p_g, size=width)
        xi_m = np.random.binomial(1, p_m, size=width)
        xi_l = np.random.binomial(1, p_l, size=width)
        
        # Fire spread from left and right neighbors stochastically
        fire_left = (np.roll(S, 1) == 3) & (np.random.binomial(1, p_f, size=width) == 1)
        fire_right = (np.roll(S, -1) == 3) & (np.random.binomial(1, p_f, size=width) == 1)
        F = fire_left | fire_right

        S_next = S.copy()
        # s == 0
        mask_0 = (S == 0)
        S_next[mask_0] = np.where(xi_g[mask_0] == 1, 1, 0)
        # s == 1
        mask_1 = (S == 1)
        S_next[mask_1] = np.where(xi_m[mask_1] == 1, 2, 1)
        # s == 2
        mask_2 = (S == 2)
        S_next[mask_2] = np.where((xi_l[mask_2] == 1) | F[mask_2], 3, 2)
        # s == 3
        mask_3 = (S == 3)
        S_next[mask_3] = 0

        S = S_next
        history[t + 1] = S
        
    return history

def run_rule_3(width, steps, init_type):
    # Directed Slope Avalanche
    # N=5. 0: stable, 1..3: stress, 4: avalanche flow
    S = np.zeros(width, dtype=np.int32)
    p_d = 0.15
    p_p = 0.9
    p_s = 0.002
    
    if init_type == "single_seed":
        # Maximum stress, center avalanche
        S.fill(3)
        S[width // 2] = 4
        p_d = 0.0
        p_s = 0.0
    else:
        S = np.random.choice([0, 1, 2, 3], size=width, p=[0.2, 0.3, 0.3, 0.2])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_d = np.random.binomial(1, p_d, size=width)
        xi_p = np.random.binomial(1, p_p, size=width)
        xi_s = np.random.binomial(1, p_s, size=width)
        
        # Look uphill (to the left)
        A = (np.roll(S, 1) == 4).astype(np.int32)

        S_next = S.copy()
        # s <= 2
        mask_less = (S <= 2)
        S_next[mask_less] = S[mask_less] + xi_d[mask_less]
        # s == 3
        mask_3 = (S == 3)
        trigger = ((A == 1) & (xi_p == 1)) | (xi_s == 1)
        S_next[mask_3] = np.where(trigger[mask_3], 4, 3)
        # s == 4
        mask_4 = (S == 4)
        S_next[mask_4] = 0

        S = S_next
        history[t + 1] = S
        
    return history

def run_rule_4(width, steps, init_type):
    # Seismic Slip Rupture
    # N=8
    S = np.zeros(width, dtype=np.int32)
    p_l = 0.08
    
    if init_type == "single_seed":
        # High strain, center rupture
        S.fill(6)
        S[width // 2] = 7
        p_l = 0.01
    else:
        S = np.random.randint(0, 7, size=width)

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_l = np.random.binomial(1, p_l, size=width)
        R = (np.roll(S, 1) == 7).astype(np.int32) + (np.roll(S, -1) == 7).astype(np.int32)

        S_next = S.copy()
        mask_7 = (S == 7)
        mask_less = (S < 7)
        S_next[mask_7] = 0
        S_next[mask_less] = np.minimum(7, S[mask_less] + 2 * R[mask_less] + xi_l[mask_less])

        S = S_next
        history[t + 1] = S

    return history

def run_rule_5(width, steps, init_type):
    # Saturated Runoff Cascade
    # N=6
    S = np.zeros(width, dtype=np.int32)
    p_r = 0.08
    
    if init_type == "single_seed":
        # Near saturated, center saturated
        S.fill(4)
        S[width // 2] = 5
        p_r = 0.002
    else:
        S = np.random.randint(0, 4, size=width)

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_r = np.random.binomial(1, p_r, size=width)
        In = (np.roll(S, 1) == 5).astype(np.int32) + (np.roll(S, -1) == 5).astype(np.int32)

        S_next = S.copy()
        mask_less = (S < 5)
        mask_5 = (S == 5)
        
        S_next[mask_less] = np.minimum(5, S[mask_less] + xi_r[mask_less] + In[mask_less])
        S_next[mask_5] = np.minimum(5, 3 + In[mask_5])

        S = S_next
        history[t + 1] = S

    return history

def run_rule_6(width, steps, init_type):
    # Aeolian Sandpile Cascade
    # N=6
    S = np.zeros(width, dtype=np.int32)
    p_d = 0.03
    
    if init_type == "single_seed":
        S.fill(3)
        S[width // 2] = 5
        p_d = 0.002
    else:
        S = np.random.choice([0, 1, 2, 3], size=width, p=[0.1, 0.2, 0.4, 0.3])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_d = np.random.binomial(1, p_d, size=width)
        T = (S >= 4).astype(np.int32)
        T_left = np.roll(T, 1)
        T_right = np.roll(T, -1)
        
        # 3 grains shed: 2 to right, 1 to left
        S = np.clip(S + xi_d - 3 * T + 2 * T_left + T_right, 0, 5)
        history[t + 1] = S

    return history

def run_rule_7(width, steps, init_type):
    # Stochastic Multi-State Epidemic
    # N=5
    S = np.zeros(width, dtype=np.int32)
    p_s = 0.001
    p_i = 0.6
    p_c = 0.1
    p_r = 0.05
    
    if init_type == "single_seed":
        # Susceptible, center critical spreader
        S.fill(0)
        S[width // 2] = 4
        p_s = 0.0
        p_i = 0.95
        p_r = 0.02
    else:
        S = np.random.choice([0, 1, 4], size=width, p=[0.98, 0.015, 0.005])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_s = np.random.binomial(1, p_s, size=width)
        xi_c = np.random.binomial(1, p_c, size=width)
        xi_r = np.random.binomial(1, p_r, size=width)

        inf_left = (np.roll(S, 1) == 1) | (np.roll(S, 1) == 4)
        inf_right = (np.roll(S, -1) == 1) | (np.roll(S, -1) == 4)
        trans_left = inf_left & (np.random.binomial(1, p_i, size=width) == 1)
        trans_right = inf_right & (np.random.binomial(1, p_i, size=width) == 1)
        F = trans_left | trans_right

        S_next = S.copy()
        
        # s == 0
        mask_0 = (S == 0)
        S_next[mask_0] = np.where((xi_s[mask_0] == 1) | F[mask_0], 1, 0)
        
        # s == 1
        mask_1 = (S == 1)
        S_next[mask_1] = np.where(xi_c[mask_1] == 1, 4, 2)
        
        # s == 4
        mask_4 = (S == 4)
        S_next[mask_4] = 2
        
        # s == 2
        mask_2 = (S == 2)
        S_next[mask_2] = 3
        
        # s == 3
        mask_3 = (S == 3)
        S_next[mask_3] = np.where(xi_r[mask_3] == 1, 0, 3)

        S = S_next
        history[t + 1] = S

    return history

def run_rule_8(width, steps, init_type):
    # Stochastic Neuronal Avalanche
    # N=6
    S = np.zeros(width, dtype=np.int32)
    p_n = 0.03
    
    if init_type == "single_seed":
        S.fill(2) # subthreshold excitation
        S[width // 2] = 3
        p_n = 0.001
    else:
        S = np.random.choice([0, 1, 2], size=width, p=[0.4, 0.4, 0.2])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_n = np.random.binomial(1, p_n, size=width)
        # Radius 2 excluding self
        F = (np.roll(S, 2) == 3).astype(np.int32) + \
            (np.roll(S, 1) == 3).astype(np.int32) + \
            (np.roll(S, -1) == 3).astype(np.int32) + \
            (np.roll(S, -2) == 3).astype(np.int32)

        S_next = S.copy()
        mask_exc = (S <= 2)
        S_next[mask_exc] = np.minimum(3, S[mask_exc] + F[mask_exc] + xi_n[mask_exc])
        
        mask_ref = (S == 3) | (S == 4)
        S_next[mask_ref] = S[mask_ref] + 1
        
        mask_5 = (S == 5)
        S_next[mask_5] = 0

        S = S_next
        history[t + 1] = S

    return history

def run_rule_9(width, steps, init_type):
    # Damped Granular Landslide
    # N=7
    S = np.zeros(width, dtype=np.int32)
    p_s = 0.02
    p_d = 0.3
    
    if init_type == "single_seed":
        S.fill(5)
        S[width // 2] = 6
        p_s = 0.0
        p_d = 0.2
    else:
        S = np.random.choice([0, 1, 2, 3, 4, 5], size=width, p=[0.1, 0.1, 0.2, 0.2, 0.2, 0.2])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        xi_d = np.random.binomial(1, p_d, size=width)
        xi_s = np.random.binomial(1, p_s, size=width)
        
        G = (np.roll(S, 1) == 6).astype(np.int32) * (3 - xi_d)

        S_next = S.copy()
        mask_less = (S < 6)
        mask_6 = (S == 6)
        
        S_next[mask_less] = np.minimum(6, S[mask_less] + G[mask_less] + xi_s[mask_less])
        S_next[mask_6] = 0

        S = S_next
        history[t + 1] = S

    return history

def run_rule_10(width, steps, init_type):
    # Smoldering Forest Fire with Wind
    # N=7
    S = np.zeros(width, dtype=np.int32)
    p_f = 0.5
    p_r = 0.02
    p_flash = 0.2
    p_b = 0.1
    
    if init_type == "single_seed":
        # Random fuel, center flaming
        S = np.random.choice([1, 2, 3], size=width, p=[0.3, 0.4, 0.3])
        S[width // 2] = 5
        p_r = 0.0
        p_f = 0.75
        p_flash = 0.4
        p_b = 0.05
    else:
        S = np.random.choice([0, 1, 2, 3, 4, 5], size=width, p=[0.3, 0.2, 0.2, 0.25, 0.03, 0.02])

    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = S

    for t in range(steps - 1):
        H = 2 * (np.roll(S, 1) == 5).astype(np.int32) + \
            (np.roll(S, -1) == 5).astype(np.int32) + \
            3 * ((np.roll(S, 2) == 6) | (np.roll(S, 1) == 6)).astype(np.int32) + \
            (np.roll(S, 1) == 4).astype(np.int32)
        
        # Stochastic ignition: p_ign = 1 - (1-p_f)^H
        p_ign = 1.0 - (1.0 - p_f) ** H
        xi_ign = np.random.rand(width) < p_ign

        xi_r = np.random.binomial(1, p_r, size=width)
        xi_flash = np.random.binomial(1, p_flash, size=width)
        xi_b = np.random.binomial(1, p_b, size=width)

        S_next = S.copy()

        # s == 0
        mask_0 = (S == 0)
        S_next[mask_0] = S[mask_0] + xi_r[mask_0]

        # s in {1, 2}
        mask_1_2 = (S == 1) | (S == 2)
        ign_mask = mask_1_2 & xi_ign
        no_ign_mask = mask_1_2 & ~xi_ign

        S_next[ign_mask] = np.where(S[ign_mask] == 2, 5, 4)
        S_next[no_ign_mask] = S[no_ign_mask] + xi_r[no_ign_mask]

        # s == 3
        mask_3 = (S == 3)
        ign_mask_3 = mask_3 & xi_ign
        S_next[ign_mask_3] = np.where(xi_flash[ign_mask_3] == 1, 6, 5)

        # s == 4
        mask_4 = (S == 4)
        flare_up = mask_4 & (H >= 2)
        burn_out = mask_4 & (H < 2) & (xi_b == 1)
        keep_smolder = mask_4 & (H < 2) & (xi_b == 0)

        S_next[flare_up] = 5
        S_next[burn_out] = 0
        S_next[keep_smolder] = 4

        # s in {5, 6}
        mask_5_6 = (S == 5) | (S == 6)
        S_next[mask_5_6] = 0

        S = S_next
        history[t + 1] = S

    return history


# Dictionary mapping rule number to its simulation function
RULES = {
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
    create_output_dir()
    width = 800
    steps = 800

    for rule_num, run_func in RULES.items():
        palette = PALETTES[rule_num]
        rule_str = f"rule_{rule_num:02d}"
        
        for init_type in ["single_seed", "random"]:
            print(f"Simulating {rule_str} ({init_type})...")
            history = run_func(width, steps, init_type)
            
            # Map state history to RGB image
            palette_arr = np.array(palette, dtype=np.uint8)
            rgb_data = palette_arr[history] # shape (800, 800, 3)
            
            img = Image.fromarray(rgb_data)
            out_filename = f"generations/loop_25/output/{rule_str}_{init_type}.png"
            img.save(out_filename)
            print(f"Saved {out_filename}")

if __name__ == "__main__":
    main()
