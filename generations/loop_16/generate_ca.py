import os
import numpy as np
from PIL import Image

# Output directory and grid size configuration
output_dir = "generations/loop_16/output"
os.makedirs(output_dir, exist_ok=True)
WIDTH = 800
STEPS = 800

def step_rule(rule_num, grid):
    W = len(grid)
    next_grid = np.zeros_like(grid)
    
    # We will use periodic boundary conditions
    # Pre-calculating neighbors for speed and clean indexing
    L1 = np.roll(grid, 1)
    R1 = np.roll(grid, -1)
    L2 = np.roll(grid, 2)
    R2 = np.roll(grid, -2)
    
    if rule_num == 1:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 2 and r1 == 1:
                    next_grid[x] = 3
                elif r1 == 4:
                    next_grid[x] = 1
                elif l1 == 4:
                    next_grid[x] = 2
                elif r1 == 1:
                    next_grid[x] = 1
                elif l1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 3 if l1 == 2 else 0
            elif s == 2:
                next_grid[x] = 3 if r1 == 1 else 0
            elif s == 3:
                next_grid[x] = 4
            elif s == 4:
                next_grid[x] = 0
                
    elif rule_num == 2:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 2:
                    next_grid[x] = 2
                elif r1 == 4:
                    next_grid[x] = 4
                elif l1 == 3:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 3 if (l1 == 2 or l1 == 3) else 1
            elif s == 2:
                next_grid[x] = 4 if r1 == 1 else 0
            elif s == 3:
                next_grid[x] = 1 if (r1 == 1 or r1 == 3) else 0
            elif s == 4:
                next_grid[x] = 0

    elif rule_num == 3:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 1 and r1 == 2:
                    next_grid[x] = 5
                elif l1 == 1:
                    next_grid[x] = 1
                elif r1 == 2:
                    next_grid[x] = 2
                elif l1 == 3 or r1 == 3:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 5 if r1 == 2 else 0
            elif s == 2:
                next_grid[x] = 5 if l1 == 1 else 0
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                next_grid[x] = 3
            elif s == 5:
                next_grid[x] = 4

    elif rule_num == 4:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            P_x = (1 if l1 == 1 else 0) + (1 if r1 == 1 else 0)
            if s == 1:
                next_grid[x] = 1
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 2
            elif s == 4:
                next_grid[x] = 0
            elif s == 0:
                if P_x >= 1 and (l1 in {2, 3} or r1 in {2, 3}):
                    next_grid[x] = 4
                elif P_x == 1:
                    next_grid[x] = 3
                elif l1 == 3 or r1 == 3:
                    next_grid[x] = 3
                elif l1 == 2 or r1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0

    elif rule_num == 5:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 1 and r1 == 3:
                    next_grid[x] = 2
                elif l1 == 1:
                    next_grid[x] = 1
                elif r1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 0
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 4 if l1 == 2 else 3
            elif s == 4:
                next_grid[x] = 4

    elif rule_num == 6:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 1:
                next_grid[x] = 4 if (l1 == 2 and r1 == 2) else 1
            elif s == 2:
                next_grid[x] = 2
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                next_grid[x] = 4
            elif s == 0:
                if l1 == 1 or r1 == 1:
                    next_grid[x] = 2
                elif l1 == 2 or r1 == 2:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0

    elif rule_num == 7:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 3 or r1 == 3:
                    next_grid[x] = 4
                elif l1 == 4:
                    next_grid[x] = 2
                elif r1 == 1:
                    next_grid[x] = 1
                elif l1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 0
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                next_grid[x] = 1

    elif rule_num == 8:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 1:
                if l1 == 1 and r1 == 1:
                    next_grid[x] = 4
                elif r1 == 4:
                    next_grid[x] = 2
                elif l1 == 4:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 1
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                next_grid[x] = 4
            elif s == 0:
                if r1 == 2:
                    next_grid[x] = 2
                elif l1 == 3:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0

    elif rule_num == 9:
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 1:
                next_grid[x] = 3
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 4
            elif s == 4:
                next_grid[x] = 1
            elif s == 0:
                if l1 == 1 or r1 == 1:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0

    elif rule_num == 10:
        for x in range(W):
            s = grid[x]
            l2, l1, r1, r2 = L2[x], L1[x], R1[x], R2[x]
            if s == 1:
                next_grid[x] = 1
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                next_grid[x] = 0
            elif s == 0:
                if l2 == 2 and l1 == 1:
                    next_grid[x] = 4
                elif r2 == 3 and r1 == 1:
                    next_grid[x] = 4
                elif l1 == 2:
                    next_grid[x] = 2
                elif r1 == 3:
                    next_grid[x] = 3
                elif l1 == 4:
                    next_grid[x] = 2
                elif r1 == 4:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0

    return next_grid

# Color Palettes (RGB)
PALETTES = {
    1: [
        [15, 15, 27],      # State 0: Ground/Vacuum (Dark blue-black)
        [255, 0, 127],     # State 1: Virtual Electron (Vibrant pink)
        [0, 240, 255],     # State 2: Virtual Positron (Vibrant cyan)
        [255, 255, 0],     # State 3: Virtual Photon (Bright yellow)
        [255, 255, 255]    # State 4: Vacuum Excitation (Pure white)
    ],
    2: [
        [18, 10, 33],      # State 0: Vacuum (Dark violet)
        [57, 255, 20],     # State 1: Stationary Electron (Neon green)
        [255, 49, 184],    # State 2: Right Photon (Neon pink)
        [255, 153, 51],    # State 3: Recoiling Electron (Neon orange)
        [0, 255, 255]      # State 4: Scattered Photon (Electric cyan)
    ],
    3: [
        [8, 12, 24],       # State 0: Vacuum (Deep navy)
        [59, 130, 246],    # State 1: Right Electron (Vibrant blue)
        [239, 68, 68],     # State 2: Left Positron (Vibrant red)
        [16, 185, 129],    # State 3: Outgoing Photon (Emerald green)
        [245, 158, 11],    # State 4: Virtual Photon (Bright amber)
        [255, 255, 255]    # State 5: Vertex Core (Pure white)
    ],
    4: [
        [26, 26, 36],      # State 0: Vacuum (Charcoal grey-blue)
        [148, 163, 184],   # State 1: Conducting Plate (Slate/silver metal)
        [236, 72, 153],    # State 2: HF Virtual Photon (Hot pink)
        [59, 130, 246],    # State 3: LF Virtual Photon (Vibrant blue)
        [234, 179, 8]      # State 4: Casimir Pressure Zone (Yellow-gold)
    ],
    5: [
        [10, 14, 23],      # State 0: Vacuum (Midnight blue)
        [6, 182, 212],     # State 1: Fast Electron (Neon cyan)
        [244, 63, 94],     # State 2: Bremsstrahlung Photon (Rose red)
        [168, 85, 247],    # State 3: Bare Nucleus (Bright purple)
        [16, 185, 129]     # State 4: Screened Nucleus (Vibrant green)
    ],
    6: [
        [24, 24, 27],      # State 0: Vacuum (Dark zinc)
        [239, 68, 68],     # State 1: Bare Positive Charge (Vibrant red)
        [59, 130, 246],    # State 2: Polarized Electron Cloud (Vibrant blue)
        [244, 63, 94],     # State 3: Polarized Positron Cloud (Rose pink)
        [251, 191, 36]     # State 4: Screened Charge Core (Warm amber)
    ],
    7: [
        [11, 19, 43],      # State 0: Dirac Sea (Deep dark space blue)
        [57, 255, 20],     # State 1: Conduction Electron (Neon green)
        [255, 0, 127],     # State 2: Positron Hole (Vibrant magenta-pink)
        [255, 255, 255],   # State 3: Incident Photon (Bright white)
        [255, 234, 0]      # State 4: Excited Transition (Neon yellow)
    ],
    8: [
        [30, 27, 75],      # State 0: Vacuum (Deep indigo)
        [244, 63, 94],     # State 1: Strong Electric Field (Electric crimson)
        [6, 182, 212],     # State 2: Electron (Bright turquoise)
        [16, 185, 129],    # State 3: Positron (Bright mint)
        [99, 102, 241]     # State 4: Weakened Electric Field (Indigo-violet)
    ],
    9: [
        [15, 23, 42],      # State 0: Vacuum (Slate blue-black)
        [56, 189, 248],    # State 1: Bare Electron (Light sky blue)
        [168, 85, 247],    # State 2: Cloud Photon (Bright amethyst)
        [244, 63, 94],     # State 3: Dressed Core (Bright coral red)
        [251, 113, 133]    # State 4: Reabsorbing Core (Soft pink)
    ],
    10: [
        [30, 30, 36],      # State 0: Vacuum (Very dark grey)
        [226, 232, 240],   # State 1: Shielded Magnetic Flux Tube (Silver-white)
        [249, 115, 22],    # State 2: Right Electron (Neon orange)
        [6, 182, 212],     # State 3: Left Electron (Neon cyan)
        [168, 85, 247]     # State 4: Phase-Shifted Electron (Bright purple)
    ]
}

def get_single_seed_grid(rule_num, W):
    grid = np.zeros(W, dtype=np.int32)
    center = W // 2
    if rule_num == 1:
        grid[center] = 4
    elif rule_num == 2:
        grid[400] = 1
        grid[550] = 1
        grid[250] = 2
    elif rule_num == 3:
        grid[300] = 1
        grid[500] = 2
    elif rule_num == 4:
        grid[200] = 1
        grid[202] = 1
        grid[350] = 1
        grid[450] = 1
        grid[600] = 1
    elif rule_num == 5:
        grid[500] = 3
        grid[200] = 1
    elif rule_num == 6:
        grid[400] = 1
    elif rule_num == 7:
        grid[400] = 3
    elif rule_num == 8:
        grid[350:451] = 1
    elif rule_num == 9:
        grid[400] = 1
    elif rule_num == 10:
        grid[400] = 1
        grid[200] = 2
        grid[600] = 3
    return grid

def get_random_grid(rule_num, W):
    num_states = len(PALETTES[rule_num])
    
    if rule_num == 1:
        p = [0.95, 0.0125, 0.0125, 0.0125, 0.0125]
    elif rule_num == 2:
        p = [0.94, 0.03, 0.015, 0.005, 0.01]
    elif rule_num == 3:
        p = [0.95, 0.01, 0.01, 0.01, 0.01, 0.01]
    elif rule_num == 4:
        p = [0.96, 0.01, 0.01, 0.01, 0.01]
    elif rule_num == 5:
        p = [0.96, 0.02, 0.01, 0.01, 0.00]
    elif rule_num == 6:
        p = [0.98, 0.01, 0.005, 0.005, 0.00]
    elif rule_num == 7:
        p = [0.96, 0.01, 0.01, 0.02, 0.00]
    elif rule_num == 8:
        grid = np.zeros(W, dtype=np.int32)
        num_blocks = np.random.randint(3, 8)
        for _ in range(num_blocks):
            block_width = np.random.randint(15, 50)
            start_idx = np.random.randint(0, W - block_width)
            grid[start_idx:start_idx + block_width] = 1
        return grid
    elif rule_num == 9:
        p = [0.98, 0.02, 0.00, 0.00, 0.00]
    elif rule_num == 10:
        p = [0.96, 0.005, 0.015, 0.015, 0.005]
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
