import os
import numpy as np
from PIL import Image

# 1. Setup output directory
output_dir = "generations/loop_20/output"
os.makedirs(output_dir, exist_ok=True)
WIDTH = 800
STEPS = 800

# 2. Define Anchor Colors for vibrant, unique color palettes
PALETTES = {
    1: [
        [15, 10, 22],      # State 0: Dark Void
        [255, 64, 129],    # State 1: Right-moving packet (Magenta/pink)
        [64, 196, 255],    # State 2: Left-moving packet (Cyan)
        [255, 235, 59],    # State 3: Portal Mouth A (Yellow)
        [255, 152, 0],     # State 4: Portal Mouth B (Orange)
        [224, 64, 251]     # State 5: Energized Core (Purple)
    ],
    2: [
        [20, 20, 30],      # State 0: Dark Navy
        [0, 230, 118],     # State 1: Spring Green
        [255, 87, 34],     # State 2: Deep Orange
        [124, 77, 255],    # State 3: Fold Zone Core (Deep Violet)
        [233, 30, 99]      # State 4: Boundary (Hot pink)
    ],
    3: [
        [10, 10, 15],      # State 0: Blackish-Indigo
        [33, 150, 243],    # State 1: Blue
        [0, 188, 212],     # State 2: Teal
        [139, 195, 74],    # State 3: Light Green
        [255, 235, 59],    # State 4: Yellow
        [255, 152, 0],     # State 5: Orange
        [244, 67, 54],     # State 6: Red
        [156, 39, 176]     # State 7: Purple
    ],
    4: [
        [18, 18, 24],      # State 0: Dark grey-black
        [0, 229, 255],     # State 1: Neon Cyan
        [255, 110, 64],    # State 2: Neon Orange
        [255, 255, 255],   # State 3: Entrance (White)
        [255, 215, 0],     # State 4: Exit (Gold)
        [224, 64, 251]     # State 5: Beacon (Neon Magenta)
    ],
    5: [
        [10, 10, 26],      # State 0
        [24, 30, 64],      # State 1
        [38, 50, 102],     # State 2
        [52, 70, 140],     # State 3
        [66, 90, 178],     # State 4
        [80, 110, 216],    # State 5
        [94, 130, 254],    # State 6
        [130, 100, 220],   # State 7
        [180, 60, 160],    # State 8
        [220, 40, 100],    # State 9
        [250, 90, 40],     # State 10
        [255, 220, 100]    # State 11
    ],
    6: [
        [20, 10, 20],      # State 0: Very dark plum
        [63, 81, 181],     # State 1: Indigo
        [0, 150, 136],     # State 2: Teal
        [139, 195, 74],    # State 3: Lime
        [255, 193, 7],     # State 4: Amber
        [233, 30, 99]      # State 5: Pink
    ],
    7: [
        [10, 10, 10],      # State 0: Pure black
        [55, 71, 79],      # State 1: Blue grey - weak gravity
        [90, 107, 124],    # State 2: Medium gravity
        [144, 164, 174],   # State 3: Strong gravity
        [255, 255, 255],   # State 4: White - Singularity
        [255, 82, 82],     # State 5: Vibrant red - photon R
        [83, 109, 254],    # State 6: Vibrant indigo - photon L
        [0, 230, 118]      # State 7: Vibrant green
    ],
    8: [
        [12, 10, 18], [28, 15, 36], [48, 20, 60], [70, 24, 86],
        [96, 28, 114], [124, 32, 140], [154, 38, 162], [182, 48, 176],
        [206, 68, 184], [224, 94, 190], [236, 124, 196], [244, 154, 204],
        [248, 184, 214], [250, 212, 226], [252, 236, 240], [255, 255, 255]
    ],
    9: [
        [13, 27, 42],      # State 0: Dark space blue
        [27, 38, 59],      # State 1: Slate blue
        [65, 90, 119],     # State 2: Medium blue
        [119, 141, 169],   # State 3: Light slate
        [224, 225, 221],   # State 4: Parchment white
        [252, 163, 17],    # State 5: Vibrant orange
        [229, 56, 56],     # State 6: Crimson red
        [20, 116, 111]     # State 7: Teal
    ],
    10: [
        [15, 15, 20],      # State 0: Dark charcoal
        [0, 229, 255],     # State 1: Cyan - spin up
        [255, 64, 129],    # State 2: Magenta - spin down
        [255, 235, 59]     # State 3: Bright yellow - disruption wave
    ]
}

def step_rule(rule_num, grid):
    W = len(grid)
    next_grid = np.zeros_like(grid)
    
    # Pre-calculating neighbors with periodic wrapping
    L1 = np.roll(grid, 1)
    R1 = np.roll(grid, -1)
    
    if rule_num == 1:
        # Portal Pair Teleportation
        # x_star = (x + W/2) mod W
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            x_star = (x + W // 2) % W
            
            if s == 0:
                # Check collision:
                if l1 == 1 and r1 == 2:
                    next_grid[x] = 3 if x < W // 2 else 4
                else:
                    # Check teleported emergence from left to right:
                    idx_L = (x - 1) % W
                    star_L = (idx_L + W // 2) % W
                    l_star = grid[(star_L - 1) % W]
                    
                    # Check teleported emergence from right to left:
                    idx_R = (x + 1) % W
                    star_R = (idx_R + W // 2) % W
                    r_star = grid[(star_R + 1) % W]
                    
                    if grid[star_L] in [3, 4] and l_star == 1:
                        next_grid[x] = 1
                    elif grid[star_R] in [3, 4] and r_star == 2:
                        next_grid[x] = 2
                    else:
                        # Normal local propagation:
                        if l1 == 1 and grid[x] not in [3, 4, 5]:
                            next_grid[x] = 1
                        elif r1 == 2 and grid[x] not in [3, 4, 5]:
                            next_grid[x] = 2
                        else:
                            next_grid[x] = 0
            elif s == 3: # Mouth A
                next_grid[x] = 5 if (l1 == 1 or r1 == 2) else 3
            elif s == 4: # Mouth B
                next_grid[x] = 5 if (l1 == 1 or r1 == 2) else 4
            elif s == 5: # Energized Mouth
                next_grid[x] = 0 # decays
            elif s in [1, 2]:
                # Handled by default zero unless they stay (particles don't stay)
                pass
                
    elif rule_num == 2:
        # Klein Bottle Mirror Folding
        # Fold zones are fixed at boundaries
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            xp = W - 1 - x
            
            if x in [0, 1, W-2, W-1]:
                next_grid[x] = 3
            else:
                if s == 0:
                    # Check mirror teleportation
                    if grid[xp] == 3 and grid[(xp - 1) % W] == 1:
                        next_grid[x] = 2
                    elif grid[xp] == 3 and grid[(xp + 1) % W] == 2:
                        next_grid[x] = 1
                    else:
                        if l1 == 1 and grid[x] != 3:
                            next_grid[x] = 1
                        elif r1 == 2 and grid[x] != 3:
                            next_grid[x] = 2
                        else:
                            next_grid[x] = 0
                elif s in [1, 2]:
                    pass # moving particles vanish from current cell
                    
    elif rule_num == 3:
        # Dynamic Hypercube Projection
        theta = int(np.sum(grid) % 8)
        # Vectorized implementation
        x_hyper = (np.arange(W) ^ theta) % W
        next_grid = (L1 + R1 + grid * grid[x_hyper] + 1) % 8
        
    elif rule_num == 4:
        # Metric Wormhole Routing
        xE = W // 4
        xX = (2 * W) // 3
        xB = (3 * W) // 4
        for x in range(W):
            if x == xE:
                next_grid[x] = 3
            elif x == xX:
                next_grid[x] = 4
            elif x == xB:
                next_grid[x] = 5
            else:
                s = grid[x]
                if s == 0:
                    # Arrives via normal step:
                    if grid[(x-1)%W] == 1 and ((x-1)%W) != xE:
                        next_grid[x] = 1
                    # Teleports to exit:
                    elif x == (xX + 1) % W and grid[(xE-1)%W] == 1:
                        next_grid[x] = 1
                    # Left-mover propagation:
                    elif grid[(x+1)%W] == 2 and ((x+1)%W) != xX:
                        next_grid[x] = 2
                elif s in [1, 2]:
                    pass # vanishes
                    
    elif rule_num == 5:
        # Non-Euclidean Thermal Wormhole
        max_val = np.max(grid)
        min_val = np.min(grid)
        # Unique choice of indexes to make it deterministic
        x_max = np.where(grid == max_val)[0][0]
        x_min = np.where(grid == min_val)[0][-1]
        
        for x in range(W):
            if x == x_max:
                next_grid[x] = (grid[(x-1)%W] + grid[x_min] + grid[(x+1)%W]) % 12
            elif x == x_min:
                next_grid[x] = (grid[(x-1)%W] + grid[x_max] + grid[(x+1)%W]) % 12
            else:
                next_grid[x] = (grid[(x-1)%W] + grid[x] + grid[(x+1)%W]) % 12
                
    elif rule_num == 6:
        # Möbius Boundary Twist
        for x in range(W):
            l1 = (grid[W-1] + 3) % 6 if x == 0 else L1[x]
            r1 = (grid[0] + 3) % 6 if x == W-1 else R1[x]
            next_grid[x] = (l1 * grid[x] + grid[x] * r1 + 1) % 6
            
    elif rule_num == 7:
        # Variable Metric Gravitational Lensing
        d_L = 1 + (grid % 4)
        d_R = 1 + (np.roll(grid, -1) % 4)
        for x in range(W):
            if grid[x] == 4:
                next_grid[x] = 4
            else:
                xl = (x - d_L[x]) % W
                xr = (x + d_R[x]) % W
                next_grid[x] = (grid[xl] + 2 * grid[x] + 3 * grid[xr]) % 8
                
    elif rule_num == 8:
        # Chaotic Portal Percolation
        for x in range(W):
            s = grid[x]
            if s >= 12:
                x_star = (x + s * 31) % W
                next_grid[x] = (grid[(x-1)%W] + grid[x_star] + grid[(x+1)%W] + 1) % 16
            else:
                next_grid[x] = (grid[(x-1)%W] + grid[x] + grid[(x+1)%W]) % 16
                
    elif rule_num == 9:
        # 2D Projected Toroidal Solitons
        # L1 = 40, L2 = 20
        for x in range(W):
            u, v = x % 40, x // 40
            L = grid[((u - 1) % 40) + v * 40]
            R = grid[((u + 1) % 40) + v * 40]
            U = grid[u + ((v - 1) % 20) * 40]
            D = grid[u + ((v + 1) % 20) * 40]
            next_grid[x] = ((L + R + U + D + grid[x]) * 3 + 1) % 8
            
    elif rule_num == 10:
        # Quantum Entanglement Bridges
        for x in range(W):
            s = grid[x]
            x_star = W - 1 - x
            
            if s == 3:
                next_grid[x] = 0
            elif grid[(x-1)%W] == 3 or grid[(x+1)%W] == 3:
                next_grid[x] = 3
            else:
                if s == 0 and grid[(x-1)%W] in [1, 2] and grid[(x+1)%W] in [1, 2]:
                    next_grid[x] = 1
                elif s in [1, 2]:
                    # Check partner
                    if grid[(x_star-1)%W] == 3 or grid[(x_star+1)%W] == 3:
                        if s == 1:
                            next_grid[x] = 2
                        else:
                            next_grid[x] = 0
                    else:
                        next_grid[x] = s
                else:
                    next_grid[x] = s
                    
    return next_grid

def get_single_seed_grid(rule_num, W):
    grid = np.zeros(W, dtype=np.int32)
    center = W // 2
    if rule_num == 1:
        # Place two portals at 200 and 600
        grid[200] = 3
        grid[600] = 4
        # Add moving packets
        grid[100] = 1
        grid[500] = 1
        grid[300] = 2
        grid[700] = 2
    elif rule_num == 2:
        # Fold zones are fixed at boundaries, add packets moving toward them
        grid[200] = 1
        grid[600] = 2
    elif rule_num == 3:
        grid[center] = 1
    elif rule_num == 4:
        # Add several packets traveling towards entrance (W//4 = 200)
        grid[50] = 1
        grid[100] = 1
        grid[150] = 1
        grid[180] = 1
    elif rule_num == 5:
        # Heat spike in the center
        grid[center-5 : center+5] = 11
    elif rule_num == 6:
        # Initial seed
        grid[center] = 3
        grid[center+1] = 4
    elif rule_num == 7:
        # Singularity in the middle
        grid[center] = 4
        # Curvature around it
        for idx in range(1, 20):
            val = max(1, 4 - idx // 5)
            grid[center - idx] = val
            grid[center + idx] = val
        # Add photons moving inward
        grid[center - 150] = 5
        grid[center + 150] = 6
    elif rule_num == 8:
        grid[center] = 15
    elif rule_num == 9:
        grid[380:420] = np.random.randint(1, 8, size=40)
    elif rule_num == 10:
        # Entangled block in the center, and disruption wave on the left and right
        grid[300:500] = 1
        grid[150] = 3
        grid[650] = 3
    return grid

def get_random_grid(rule_num, W):
    num_states = len(PALETTES[rule_num])
    
    if rule_num == 1:
        # Mostly vacuum with some packets
        p = [0.96, 0.02, 0.02, 0.00, 0.00, 0.00]
    elif rule_num == 2:
        # Boundary folds are set in step_rule, other space is vacuum with packets
        p = [0.96, 0.02, 0.02, 0.00, 0.00]
    elif rule_num == 3:
        p = [0.15, 0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1]
    elif rule_num == 4:
        # Portals are fixed in step_rule
        p = [0.97, 0.02, 0.01, 0.00, 0.00, 0.00]
    elif rule_num == 5:
        p = [0.2, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1]
    elif rule_num == 6:
        p = [0.25, 0.15, 0.15, 0.15, 0.15, 0.15]
    elif rule_num == 7:
        # Initialize three singularities
        grid = np.zeros(W, dtype=np.int32)
        grid[200] = 4
        grid[400] = 4
        grid[600] = 4
        # Add random potential and photons
        for x in range(W):
            if grid[x] != 4:
                grid[x] = np.random.choice([0, 1, 2, 5, 6], p=[0.85, 0.05, 0.04, 0.03, 0.03])
        return grid
    elif rule_num == 8:
        p = [0.95] + [0.05 / 15] * 15
    elif rule_num == 9:
        p = [0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    elif rule_num == 10:
        # Random blocks of entanglement
        grid = np.zeros(W, dtype=np.int32)
        for _ in range(5):
            w = np.random.randint(20, 60)
            start = np.random.randint(0, W - w)
            grid[start : start + w] = 1
        # Add disruption waves
        grid[np.random.randint(0, W, size=4)] = 3
        return grid
        
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
