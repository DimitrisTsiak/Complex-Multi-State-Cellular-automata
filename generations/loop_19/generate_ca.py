import os
import numpy as np
from PIL import Image

# Output directory and grid size configuration
output_dir = "generations/loop_19/output"
os.makedirs(output_dir, exist_ok=True)
WIDTH = 800
STEPS = 800

def step_rule(rule_num, grid):
    # Periodic boundary conditions pre-calculated using np.roll
    L1 = np.roll(grid, 1)
    R1 = np.roll(grid, -1)
    L2 = np.roll(grid, 2)
    R2 = np.roll(grid, -2)
    
    next_grid = np.zeros_like(grid)
    
    if rule_num == 1:
        # State 0: Uninfused Aether
        # State 1: Leyline Source
        # State 2: Charging Conduit
        # State 3: Resonating Conduit
        # State 4: Mana Resistance
        
        in_123_L = (L1 == 1) | (L1 == 2) | (L1 == 3)
        in_123_R = (R1 == 1) | (R1 == 2) | (R1 == 3)
        in_13_L = (L1 == 1) | (L1 == 3)
        in_13_R = (R1 == 1) | (R1 == 3)

        next_grid[grid == 1] = 1
        
        mask_3 = (grid == 3)
        cond_3 = in_123_L | in_123_R
        next_grid[mask_3 & cond_3] = 3
        next_grid[mask_3 & ~cond_3] = 4

        mask_2 = (grid == 2)
        cond_2 = in_13_L | in_13_R
        next_grid[mask_2 & cond_2] = 3
        next_grid[mask_2 & ~cond_2] = 4

        mask_0 = (grid == 0)
        cond_0 = in_13_L | in_13_R
        next_grid[mask_0 & cond_0] = 2

    elif rule_num == 2:
        # State 0: Inert Aether
        # State 1: Soul Anchor
        # State 2: Soul Thread
        # State 3: Resonant Soul Knot
        # State 4: Fading Tether
        
        in_123_L1 = (L1 == 1) | (L1 == 2) | (L1 == 3)
        in_123_R1 = (R1 == 1) | (R1 == 2) | (R1 == 3)
        in_123_L2 = (L2 == 1) | (L2 == 2) | (L2 == 3)
        in_123_R2 = (R2 == 1) | (R2 == 2) | (R2 == 3)
        
        next_grid[grid == 1] = 1

        mask_3 = (grid == 3)
        cond_3 = in_123_L1 | in_123_R1
        next_grid[mask_3 & cond_3] = 3
        next_grid[mask_3 & ~cond_3] = 4

        mask_2 = (grid == 2)
        cond_2_to_3 = (in_123_L1 | in_123_L2) & (in_123_R1 | in_123_R2)
        in_12_L1 = (L1 == 1) | (L1 == 2)
        in_12_R1 = (R1 == 1) | (R1 == 2)
        cond_2_to_2 = in_12_L1 | in_12_R1
        next_grid[mask_2 & cond_2_to_3] = 3
        next_grid[mask_2 & ~cond_2_to_3 & cond_2_to_2] = 2
        next_grid[mask_2 & ~cond_2_to_3 & ~cond_2_to_2] = 4

        mask_0 = (grid == 0)
        cond_0_to_3 = (L1 == 2) & (R1 == 2)
        cond_0_to_2a = (L1 == 1) | (R1 == 1)
        in_12_L2 = (L2 == 1) | (L2 == 2)
        in_12_R2 = (R2 == 1) | (R2 == 2)
        cond_0_to_2b = (L1 == 2) & in_12_L2 & (R1 == 0)
        cond_0_to_2c = (R1 == 2) & in_12_R2 & (L1 == 0)
        cond_0_to_2 = cond_0_to_2a | cond_0_to_2b | cond_0_to_2c

        next_grid[mask_0 & cond_0_to_3] = 3
        next_grid[mask_0 & ~cond_0_to_3 & cond_0_to_2] = 2

    elif rule_num == 3:
        # State 0: Empty Graveyard
        # State 1: Living Flesh
        # State 2: Necrotic Miasma
        # State 3: Ectoplasmic Slime
        # State 4: Calcified Bones
        
        mask_0 = (grid == 0)
        cond_0 = ((L1 == 2) & (R1 == 3)) | ((R1 == 2) & (L1 == 3))
        next_grid[mask_0 & cond_0] = 2

        mask_1 = (grid == 1)
        cond_1 = (L1 == 2) | (R1 == 2)
        next_grid[mask_1 & cond_1] = 2
        next_grid[mask_1 & ~cond_1] = 1

        mask_2 = (grid == 2)
        cond_2 = (L1 == 1) & (R1 == 1)
        next_grid[mask_2 & cond_2] = 4
        next_grid[mask_2 & ~cond_2] = 3

        mask_4 = (grid == 4)
        cond_4 = (L1 == 2) | (R1 == 2)
        next_grid[mask_4 & cond_4] = 2
        next_grid[mask_4 & ~cond_4] = 4

    elif rule_num == 4:
        # State 0: Base Lead
        # State 1: Alchemical Salt
        # State 2: Quicksilver Catalyst
        # State 3: Noble Gold
        # State 4: Volatile Embers
        # State 5: Useless Dross
        
        next_grid[grid == 3] = 3
        next_grid[grid == 5] = 5
        next_grid[grid == 4] = 5

        mask_2 = (grid == 2)
        cond_2 = (L1 == 1) & (R1 == 1)
        next_grid[mask_2 & cond_2] = 4
        next_grid[mask_2 & ~cond_2] = 3

        mask_1 = (grid == 1)
        cond_1 = (L1 == 2) | (R1 == 2)
        next_grid[mask_1 & cond_1] = 2
        next_grid[mask_1 & ~cond_1] = 1

        mask_0 = (grid == 0)
        cond_0_to_2 = (L1 == 2) | (R1 == 2)
        cond_0_to_1 = (L1 == 1) | (R1 == 1)
        next_grid[mask_0 & cond_0_to_2] = 2
        next_grid[mask_0 & ~cond_0_to_2 & cond_0_to_1] = 1

    elif rule_num == 5:
        # State 0: Dead Aether
        # State 1: Ambient Mana
        # State 2: Arcane Charge
        # State 3: Feedback Spark
        # State 4: Backlash Shockwave
        
        next_grid[grid == 3] = 4
        next_grid[grid == 0] = 1

        mask_1 = (grid == 1)
        cond_1_to_0 = (L1 == 4) | (R1 == 4)
        cond_1_to_3 = (L1 == 3) | (R1 == 3)
        cond_1_to_2 = ((L1 == 1) & (R1 == 1)) | (L1 == 2) | (R1 == 2)
        next_grid[mask_1 & cond_1_to_0] = 0
        next_grid[mask_1 & ~cond_1_to_0 & cond_1_to_3] = 3
        next_grid[mask_1 & ~cond_1_to_0 & ~cond_1_to_3 & cond_1_to_2] = 2
        next_grid[mask_1 & ~cond_1_to_0 & ~cond_1_to_3 & ~cond_1_to_2] = 1

        mask_2 = (grid == 2)
        cond_2_to_4 = (L1 == 4) | (R1 == 4) | (L1 == 3) | (R1 == 3)
        cond_2_to_3 = (L1 == 2) & (R1 == 2)
        next_grid[mask_2 & cond_2_to_4] = 4
        next_grid[mask_2 & ~cond_2_to_4 & cond_2_to_3] = 3
        next_grid[mask_2 & ~cond_2_to_4 & ~cond_2_to_3] = 2

    elif rule_num == 6:
        # State 0: Wild Forest
        # State 1: Wandering Soul
        # State 2: Phylactery Core
        # State 3: Necrotic Aura
        # State 4: Lich Harbinger
        # State 5: Siphoned Essence
        
        next_grid[grid == 2] = 2

        mask_3 = (grid == 3)
        cond_3 = (L1 == 5) | (R1 == 5)
        next_grid[mask_3 & cond_3] = 5
        next_grid[mask_3 & ~cond_3] = 3

        next_grid[grid == 5] = 3

        mask_4 = (grid == 4)
        cond_4 = (L1 == 1) | (R1 == 1)
        next_grid[mask_4 & cond_4] = 5
        next_grid[mask_4 & ~cond_4] = 3

        mask_1 = (grid == 1)
        cond_1 = (L1 == 4) | (R1 == 4)
        next_grid[mask_1 & cond_1] = 5
        next_grid[mask_1 & ~cond_1] = 1

        mask_0 = (grid == 0)
        cond_0_to_4 = ((L1 == 3) & ((R1 == 1) | (R1 == 0))) | ((R1 == 3) & ((L1 == 1) | (L1 == 0)))
        cond_0_to_5 = ((L1 == 5) & (R1 == 3)) | ((R1 == 5) & (L1 == 3))
        next_grid[mask_0 & cond_0_to_4] = 4
        next_grid[mask_0 & ~cond_0_to_4 & cond_0_to_5] = 5

    elif rule_num == 7:
        # State 0: Dark Soil
        # State 1: Dead Bones
        # State 2: Right-Marching Skeleton
        # State 3: Left-Marching Skeleton
        # State 4: Necromantic Pulse
        
        mask_1 = (grid == 1)
        cond_1_to_2 = (L1 == 4)
        cond_1_to_3 = (R1 == 4)
        next_grid[mask_1 & cond_1_to_2] = 2
        next_grid[mask_1 & ~cond_1_to_2 & cond_1_to_3] = 3
        next_grid[mask_1 & ~cond_1_to_2 & ~cond_1_to_3] = 1

        mask_2 = (grid == 2)
        cond_2 = (R1 == 3) | (R1 == 1) | (R1 == 4)
        next_grid[mask_2 & cond_2] = 1

        mask_3 = (grid == 3)
        cond_3 = (L1 == 2) | (L1 == 1) | (L1 == 4)
        next_grid[mask_3 & cond_3] = 1

        mask_0 = (grid == 0)
        cond_0_to_4 = (L1 == 4) | (R1 == 4)
        cond_0_to_1 = (L1 == 2) & (R1 == 3)
        cond_0_to_2 = (L1 == 2)
        cond_0_to_3 = (R1 == 3)
        next_grid[mask_0 & cond_0_to_4] = 4
        next_grid[mask_0 & ~cond_0_to_4 & cond_0_to_1] = 1
        next_grid[mask_0 & ~cond_0_to_4 & ~cond_0_to_1 & cond_0_to_2] = 2
        next_grid[mask_0 & ~cond_0_to_4 & ~cond_0_to_1 & ~cond_0_to_2 & cond_0_to_3] = 3

    elif rule_num == 8:
        # State 0: Stone Floor
        # State 1: Sacrificial Altar
        # State 2: Flowing Blood
        # State 3: Runic Circle
        # State 4: Saturated Rune
        # State 5: Blood Nova
        
        mask_1 = (grid == 1)
        cond_1_to_0 = (L1 == 5) | (R1 == 5)
        next_grid[mask_1 & ~cond_1_to_0] = 1

        next_grid[grid == 4] = 5

        mask_3 = (grid == 3)
        cond_3 = (L1 == 2) | (R1 == 2)
        next_grid[mask_3 & cond_3] = 4
        next_grid[mask_3 & ~cond_3] = 3

        mask_2 = (grid == 2)
        cond_2 = (L1 == 5) | (R1 == 5)
        next_grid[mask_2 & cond_2] = 5

        mask_0 = (grid == 0)
        cond_0_to_5 = (L1 == 5) | (R1 == 5)
        cond_0_to_2 = (L1 == 1) | (R1 == 1) | (L1 == 2) | (R1 == 2)
        next_grid[mask_0 & cond_0_to_5] = 5
        next_grid[mask_0 & ~cond_0_to_5 & cond_0_to_2] = 2

    elif rule_num == 9:
        # State 0: Liquid Mercury
        # State 1: Stone Crystal Core
        # State 2: Crystallization Seed
        # State 3: Sulfur Impurity
        # State 4: Lead Impurity
        
        next_grid[grid == 1] = 1
        next_grid[grid == 4] = 4

        mask_3 = (grid == 3)
        cond_3 = (L1 == 2) | (R1 == 2)
        next_grid[mask_3 & cond_3] = 2
        next_grid[mask_3 & ~cond_3] = 3

        mask_2 = (grid == 2)
        cond_2 = (L1 == 4) | (R1 == 4)
        next_grid[mask_2 & cond_2] = 4
        next_grid[mask_2 & ~cond_2] = 1

        mask_0 = (grid == 0)
        cond_0_to_1 = (L1 == 2) & (R1 == 2)
        cond_0_to_2 = (L1 == 2) | (R1 == 2)
        next_grid[mask_0 & cond_0_to_1] = 1
        next_grid[mask_0 & ~cond_0_to_1 & cond_0_to_2] = 2

    elif rule_num == 10:
        # State 0: Stable Matter
        # State 1: Mana-infused Matter
        # State 2: Abyssal Core
        # State 3: Ravenous Void
        # State 4: Decaying Ectoplasm
        
        next_grid[grid == 2] = 2
        next_grid[grid == 4] = 2
        next_grid[grid == 3] = 4

        mask_1 = (grid == 1)
        cond_1 = (L1 == 2) | (L1 == 3) | (R1 == 2) | (R1 == 3)
        next_grid[mask_1 & cond_1] = 3
        next_grid[mask_1 & ~cond_1] = 1

        mask_0 = (grid == 0)
        cond_0 = (L1 == 3) | (R1 == 3) | ((L1 == 2) & (R1 == 2))
        next_grid[mask_0 & cond_0] = 3

    return next_grid

# Color Palettes with vibrant/neon tones on dark backgrounds
PALETTES = {
    1: [
        [10, 10, 24],      # State 0: Uninfused Aether (Dark navy)
        [0, 240, 255],     # State 1: Leyline Source (Neon cyan)
        [180, 50, 255],    # State 2: Charging Conduit (Vibrant purple)
        [255, 230, 0],     # State 3: Resonating Conduit (Neon gold)
        [180, 20, 50]      # State 4: Mana Resistance (Deep crimson)
    ],
    2: [
        [16, 8, 30],       # State 0: Inert Aether (Dark violet)
        [255, 0, 128],     # State 1: Soul Anchor (Neon pink)
        [0, 191, 255],     # State 2: Soul Thread (Electric blue)
        [220, 255, 255],   # State 3: Resonant Soul Knot (Brilliant white-cyan)
        [100, 80, 120]     # State 4: Fading Tether (Dim purple-grey)
    ],
    3: [
        [8, 18, 12],       # State 0: Empty Graveyard (Dark forest green-black)
        [240, 128, 128],   # State 1: Living Flesh (Coral pink)
        [57, 255, 20],     # State 2: Necrotic Miasma (Toxic neon green)
        [190, 255, 0],     # State 3: Ectoplasmic Slime (Slime yellow-green)
        [245, 245, 240]    # State 4: Calcified Bones (Skeletal white)
    ],
    4: [
        [25, 28, 36],      # State 0: Base Lead (Dark slate grey)
        [220, 225, 235],   # State 1: Alchemical Salt (Silver white)
        [0, 255, 200],     # State 2: Quicksilver Catalyst (Neon turquoise)
        [255, 215, 0],     # State 3: Noble Gold (Gold)
        [255, 69, 0],      # State 4: Volatile Embers (Neon orange-red)
        [90, 90, 95]       # State 5: Useless Dross (Charcoal ash)
    ],
    5: [
        [5, 5, 8],         # State 0: Dead Aether (Void black)
        [99, 102, 241],    # State 1: Ambient Mana (Deep electric blue)
        [236, 72, 153],    # State 2: Arcane Charge (Neon pink)
        [255, 255, 200],   # State 3: Feedback Spark (Yellowish white)
        [249, 115, 22]     # State 4: Backlash Shockwave (Neon orange)
    ],
    6: [
        [10, 24, 15],      # State 0: Wild Forest (Dark forest green)
        [100, 200, 255],   # State 1: Wandering Soul (Soft blue)
        [255, 0, 255],     # State 2: Phylactery Core (Neon magenta)
        [50, 205, 50],     # State 3: Necrotic Aura (Neon lime green)
        [255, 50, 50],     # State 4: Lich Harbinger (Neon red)
        [255, 255, 100]    # State 5: Siphoned Essence (Bright yellow)
    ],
    7: [
        [20, 15, 12],      # State 0: Dark Soil (Dark brownish black)
        [220, 215, 200],   # State 1: Dead Bones (Bone white)
        [0, 191, 255],     # State 2: Right-Marching Skeleton (Electric cyan)
        [255, 0, 180],     # State 3: Left-Marching Skeleton (Neon pink)
        [50, 255, 50]      # State 4: Necromantic Pulse (Vibrant lime green)
    ],
    8: [
        [28, 28, 30],      # State 0: Stone Floor (Charcoal)
        [150, 0, 20],      # State 1: Sacrificial Altar (Blood crimson)
        [255, 0, 50],      # State 2: Flowing Blood (Bright red)
        [0, 128, 128],     # State 3: Runic Circle (Dark teal)
        [0, 255, 255],     # State 4: Saturated Rune (Cyan)
        [255, 255, 150]    # State 5: Blood Nova (Electric pale yellow)
    ],
    9: [
        [20, 30, 45],      # State 0: Liquid Mercury (Dark metallic blue)
        [218, 165, 32],    # State 1: Stone Crystal Core (Gold)
        [255, 127, 80],    # State 2: Crystallization Seed (Coral orange)
        [255, 255, 0],     # State 3: Sulfur Impurity (Bright yellow)
        [112, 128, 144]    # State 4: Lead Impurity (Slate grey)
    ],
    10: [
        [25, 15, 45],      # State 0: Stable Matter (Deep space purple)
        [0, 255, 255],     # State 1: Mana-infused Matter (Electric cyan)
        [15, 15, 20],      # State 2: Abyssal Core (Near pitch black)
        [230, 0, 255],     # State 3: Ravenous Void (Vibrant neon magenta)
        [152, 251, 152]    # State 4: Decaying Ectoplasm (Pale green)
    ]
}

def get_single_seed_grid(rule_num, W):
    grid = np.zeros(W, dtype=np.int32)
    
    if rule_num == 1:
        grid[W // 3] = 1
        grid[2 * W // 3] = 1
        grid[W // 3 + 2] = 2
        grid[2 * W // 3 - 2] = 2
    elif rule_num == 2:
        grid[250] = 1
        grid[550] = 1
        grid[252] = 2
        grid[548] = 2
    elif rule_num == 3:
        grid.fill(1)
        grid[W // 2] = 2
    elif rule_num == 4:
        grid[200:210] = 1
        grid[400] = 2
        grid[590:600] = 1
    elif rule_num == 5:
        grid.fill(1)
        grid[W // 2 - 20: W // 2 + 20] = 2
        grid[W // 2] = 3
    elif rule_num == 6:
        grid[W // 2] = 2
        grid[150] = 1
        grid[280] = 1
        grid[520] = 1
        grid[680] = 1
        grid[W // 2 - 4] = 4
        grid[W // 2 + 4] = 4
    elif rule_num == 7:
        grid[300] = 1
        grid[500] = 1
        grid[100] = 2
        grid[700] = 3
        grid[W // 2] = 4
    elif rule_num == 8:
        grid[W // 2] = 1
        grid[200] = 3
        grid[600] = 3
    elif rule_num == 9:
        grid[W // 2] = 2
        grid[300] = 3
        grid[500] = 3
        grid[200:210] = 4
        grid[600:610] = 4
    elif rule_num == 10:
        grid[W // 2] = 2
        grid[150:250] = 1
        grid[550:650] = 1
        
    return grid

def get_random_grid(rule_num, W):
    num_states = len(PALETTES[rule_num])
    
    if rule_num == 1:
        p = [0.93, 0.01, 0.02, 0.02, 0.02]
    elif rule_num == 2:
        p = [0.94, 0.01, 0.03, 0.01, 0.01]
    elif rule_num == 3:
        p = [0.10, 0.85, 0.03, 0.01, 0.01]
    elif rule_num == 4:
        p = [0.90, 0.06, 0.03, 0.00, 0.01, 0.00]
    elif rule_num == 5:
        p = [0.05, 0.70, 0.23, 0.02, 0.00]
    elif rule_num == 6:
        p = [0.92, 0.05, 0.002, 0.02, 0.008, 0.00]
    elif rule_num == 7:
        p = [0.85, 0.08, 0.03, 0.03, 0.01]
    elif rule_num == 8:
        grid = np.zeros(W, dtype=np.int32)
        altar_indices = np.random.choice(W, size=10, replace=False)
        grid[altar_indices] = 1
        rune_indices = np.random.choice(W, size=15, replace=False)
        rune_indices = rune_indices[grid[rune_indices] == 0]
        grid[rune_indices] = 3
        blood_indices = np.random.choice(W, size=15, replace=False)
        blood_indices = blood_indices[grid[blood_indices] == 0]
        grid[blood_indices] = 2
        return grid
    elif rule_num == 9:
        p = [0.90, 0.00, 0.02, 0.05, 0.03]
    elif rule_num == 10:
        p = [0.70, 0.25, 0.01, 0.03, 0.01]
    else:
        p = [1.0] + [0.0] * (num_states - 1)
        
    p = np.array(p)
    p = p / p.sum()
    return np.random.choice(num_states, size=W, p=p)

def run_simulation(rule_num, init_type, width=800, steps=800):
    if init_type == "single_seed":
        grid = get_single_seed_grid(rule_num, width)
    else:
        grid = get_random_grid(rule_num, width)
        
    history = np.zeros((steps, width), dtype=np.int32)
    history[0] = grid
    
    for t in range(1, steps):
        grid = step_rule(rule_num, grid)
        history[t] = grid
        
    return history

def save_as_png(history, rule_num, init_type, output_path):
    palette = np.array(PALETTES[rule_num], dtype=np.uint8)
    img_data = palette[history]
    img = Image.fromarray(img_data, mode="RGB")
    img.save(output_path)
    print(f"Saved: {output_path}")

def main():
    np.random.seed(42)
    
    for r in range(1, 11):
        for init in ["single_seed", "random"]:
            filename = f"rule_{r:02d}_{init}.png"
            filepath = os.path.join(output_dir, filename)
            
            history = run_simulation(r, init, WIDTH, STEPS)
            save_as_png(history, r, init, filepath)

if __name__ == "__main__":
    main()
