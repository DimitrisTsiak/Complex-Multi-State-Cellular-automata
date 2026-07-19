import os
import numpy as np
from PIL import Image

# Output directory and grid size configuration
output_dir = "generations/loop_18/output"
os.makedirs(output_dir, exist_ok=True)
WIDTH = 800
STEPS = 800

def step_rule(rule_num, grid, t):
    W = len(grid)
    next_grid = np.zeros_like(grid)
    
    # Periodic boundary conditions pre-calculations
    L1 = np.roll(grid, 1)
    R1 = np.roll(grid, -1)
    L2 = np.roll(grid, 2)
    R2 = np.roll(grid, -2)
    
    if rule_num == 1:
        # Novikov Consistency Lock
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 1 and r1 == 2:
                    next_grid[x] = 4
                elif l1 == 4:
                    next_grid[x] = 1
                elif r1 == 4:
                    next_grid[x] = 2
                elif l1 == 1:
                    next_grid[x] = 1
                elif r1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 4 if (r1 == 2 or r1 == 4) else 0
            elif s == 2:
                next_grid[x] = 4 if (l1 == 1 or l1 == 4) else 0
            elif s == 3:
                next_grid[x] = 4
            elif s == 4:
                next_grid[x] = 0
                
    elif rule_num == 2:
        # Branching Timeline Merger
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 3 or r1 == 3:
                    next_grid[x] = 4
                elif l1 == 1 and r1 == 2:
                    next_grid[x] = 4
                elif l1 == 1 and r1 == 4:
                    next_grid[x] = 4
                elif l1 == 1:
                    next_grid[x] = 1
                elif r1 == 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 0
            elif s == 1:
                if r1 == 2:
                    next_grid[x] = 4
                elif r1 == 5:
                    next_grid[x] = 5
                else:
                    next_grid[x] = 1
            elif s == 2:
                if l1 == 1:
                    next_grid[x] = 4
                elif l1 == 5:
                    next_grid[x] = 5
                else:
                    next_grid[x] = 2
            elif s == 3:
                next_grid[x] = 5
            elif s == 4:
                next_grid[x] = 5 if (l1 == 5 or r1 == 5) else 4
            elif s == 5:
                next_grid[x] = 0

    elif rule_num == 3:
        # Bootstrap Paradox
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 1:
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
                next_grid[x] = 1 if r1 == 2 else 3
            elif s == 4:
                next_grid[x] = 2 if l1 == 1 else 4

    elif rule_num == 4:
        # Chronology Protection Blow-Up
        mask1 = (grid == 1).astype(np.int32)
        mask2 = (grid == 2).astype(np.int32)
        mask3 = (grid == 3).astype(np.int32)
        N1 = np.roll(mask1, 2) + np.roll(mask1, 1) + np.roll(mask1, -1) + np.roll(mask1, -2)
        N2 = np.roll(mask2, 2) + np.roll(mask2, 1) + np.roll(mask2, -1) + np.roll(mask2, -2)
        N3 = np.roll(mask3, 2) + np.roll(mask3, 1) + np.roll(mask3, -1) + np.roll(mask3, -2)
        for x in range(W):
            s = grid[x]
            n1, n2, n3 = N1[x], N2[x], N3[x]
            if s == 0:
                if n3 > 0:
                    next_grid[x] = 4
                elif n1 >= 3:
                    next_grid[x] = 2
                elif n1 in (1, 2):
                    next_grid[x] = 1
                else:
                    next_grid[x] = 0
            elif s == 1:
                if n3 > 0:
                    next_grid[x] = 4
                elif n2 >= 2:
                    next_grid[x] = 2
                else:
                    next_grid[x] = 1
            elif s == 2:
                if n3 > 0:
                    next_grid[x] = 4
                elif (n1 + n2) >= 4:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 2
            elif s == 3:
                next_grid[x] = 4
            elif s == 4:
                next_grid[x] = 0

    elif rule_num == 5:
        # Tachyonic Anti-Telephone
        for x in range(W):
            s = grid[x]
            l2, l1, r1, r2 = L2[x], L1[x], R1[x], R2[x]
            if s == 0:
                if r2 == 1:
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
                if l1 == 2:
                    next_grid[x] = 1
                elif r1 == 1 or r2 == 1:
                    next_grid[x] = 4
                else:
                    next_grid[x] = 3
            elif s == 4:
                next_grid[x] = 3

    elif rule_num == 6:
        # CTC Phase Coherence
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            
            def d(a, b):
                return min(abs(a - b), 4 - abs(a - b))
                
            if s in (1, 2, 3, 4):
                if l1 in (1, 2, 3, 4) and d(s, l1) > 1:
                    next_grid[x] = 0
                elif r1 in (1, 2, 3, 4) and d(s, r1) > 1:
                    next_grid[x] = 0
                else:
                    next_grid[x] = s
            elif s == 0:
                if l1 in (1, 2, 3, 4) and r1 == 0:
                    next_grid[x] = l1
                elif r1 in (1, 2, 3, 4) and l1 == 0:
                    next_grid[x] = r1
                elif l1 in (1, 2, 3, 4) and r1 in (1, 2, 3, 4):
                    if d(l1, r1) <= 1:
                        next_grid[x] = l1
                    else:
                        next_grid[x] = 0
                else:
                    next_grid[x] = 0

    elif rule_num == 7:
        # Temporal Friction and Chrono-decay
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
                elif l1 == 3 and t % 2 == 0:
                    next_grid[x] = 3
                elif l1 == 5 or r1 == 5:
                    next_grid[x] = 5
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 2 if (r1 in (2, 4)) else 0
            elif s == 2:
                next_grid[x] = 3 if (l1 in (1, 4)) else 0
            elif s == 3:
                if t % 2 == 0:
                    next_grid[x] = 4 if r1 == 4 else 0
                else:
                    next_grid[x] = 3
            elif s == 4:
                if l1 == 5 or r1 == 5 or (l1 == 3 and t % 2 == 0):
                    next_grid[x] = 5
                else:
                    next_grid[x] = 4
            elif s == 5:
                next_grid[x] = 0

    elif rule_num == 8:
        # Retrocausal Absorber Transaction
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 2:
                    next_grid[x] = 2
                elif r1 == 3:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 2 if r1 == 3 else 1
            elif s == 2:
                next_grid[x] = 0
            elif s == 3:
                next_grid[x] = 0
            elif s == 4:
                if l1 == 2:
                    next_grid[x] = 4
                elif t % 16 == 0:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 4

    elif rule_num == 9:
        # Grandfather Paradox (Timeline Splitting)
        for x in range(W):
            s = grid[x]
            l1, r1 = L1[x], R1[x]
            if s == 0:
                if l1 == 1:
                    next_grid[x] = 1
                elif r1 == 2:
                    next_grid[x] = 2
                elif l1 == 5 or r1 == 5:
                    next_grid[x] = 3
                else:
                    next_grid[x] = 0
            elif s == 1:
                next_grid[x] = 5 if r1 == 4 else 1
            elif s == 2:
                next_grid[x] = 5 if l1 == 4 else 2
            elif s == 3:
                if l1 == 5:
                    next_grid[x] = 2
                elif r1 == 5:
                    next_grid[x] = 1
                else:
                    next_grid[x] = 3
            elif s == 4:
                next_grid[x] = 0
            elif s == 5:
                next_grid[x] = 3

    elif rule_num == 10:
        # Chrono-Static Anchor Field
        mask1 = (grid == 1).astype(np.int32)
        N1 = mask1 + np.roll(mask1, 1) + np.roll(mask1, 2) + np.roll(mask1, -1) + np.roll(mask1, -2)
        for x in range(W):
            s = grid[x]
            n1 = N1[x]
            l2, l1, r1, r2 = L2[x], L1[x], R1[x], R2[x]
            
            if s == 1:
                next_grid[x] = 1
            elif s == 2:
                next_grid[x] = 2 if n1 > 0 else 0
            elif s == 3:
                next_grid[x] = 2 if n1 > 0 else 0
            elif s == 4:
                next_grid[x] = 2 if n1 > 0 else 0
            elif s == 0:
                if n1 > 0:
                    next_grid[x] = 2
                else:
                    if r1 == 3:
                        next_grid[x] = 3
                    elif l2 == 4:
                        next_grid[x] = 4
                    else:
                        next_grid[x] = 0
                        
    return next_grid

PALETTES = {
    1: [
        [24, 24, 27],      # State 0: Vacuum (Dark charcoal)
        [56, 189, 248],    # State 1: Retarded Signal (Electric Blue)
        [244, 63, 94],     # State 2: Advanced Signal (Neon Pink/Magenta)
        [249, 115, 22],    # State 3: Paradox (High-energy Orange)
        [34, 197, 94]      # State 4: Consistency Lock (Vibrant Green)
    ],
    2: [
        [15, 23, 42],      # State 0: Primordial Vacuum (Deep black-blue)
        [59, 130, 246],    # State 1: Timeline Alpha (Cobalt Blue)
        [239, 68, 68],     # State 2: Timeline Beta (Crimson Red)
        [253, 224, 71],    # State 3: Branching Origin (Bright Yellow)
        [168, 85, 247],    # State 4: Merger Zone (Purple)
        [100, 116, 139]    # State 5: Timeline Decay (Slate Grey)
    ],
    3: [
        [15, 23, 30],      # State 0: Flat Spacetime (Very dark slate)
        [245, 158, 11],    # State 1: Causal Artifact (Golden Amber)
        [6, 182, 212],     # State 2: Retrocausal Signal (Neon Cyan)
        [217, 70, 239],    # State 3: Loop Emitter (Vibrant Magenta)
        [16, 185, 129]     # State 4: Future Receiver (Emerald Green)
    ],
    4: [
        [9, 9, 11],        # State 0: Calm Vacuum (Deep blue-black)
        [139, 92, 246],    # State 1: CTC Seed (Violet)
        [251, 146, 60],    # State 2: Vacuum Polarization (Pink-orange)
        [255, 255, 255],   # State 3: Singularity Blast (Pure White)
        [63, 63, 70]       # State 4: Decaying Ash (Dark brown-grey)
    ],
    5: [
        [20, 20, 23],      # State 0: Quiet Vacuum (Very dark grey)
        [225, 29, 72],     # State 1: Tachyon Pulse (Laser Crimson)
        [37, 99, 235],     # State 2: Retarded Trigger (Vivid Blue)
        [132, 204, 22],    # State 3: Active Transmitter (Bright Lime)
        [20, 83, 45]       # State 4: Inhibited Transmitter (Dark forest green)
    ],
    6: [
        [0, 0, 0],         # State 0: Decoherence Vacuum (Deep black)
        [6, 182, 212],     # State 1: Phase 0 (Cyan)
        [168, 85, 247],    # State 2: Phase 1 (Purple)
        [244, 63, 94],     # State 3: Phase 2 (Rose)
        [234, 179, 8]      # State 4: Phase 3 (Yellow)
    ],
    7: [
        [15, 23, 42],      # State 0: Vacuum (Slate black)
        [34, 197, 94],     # State 1: Fresh Traveler (Bright Green)
        [163, 230, 53],    # State 2: Gen-1 Traveler (Yellow-Green)
        [250, 204, 21],    # State 3: Gen-2 Traveler (Yellow)
        [194, 65, 12],     # State 4: Stationary Traveler (Dark Orange)
        [244, 63, 94]      # State 5: Annihilation Burst (Neon Crimson)
    ],
    8: [
        [11, 15, 26],      # State 0: Quantum Vacuum (Space blue)
        [71, 85, 105],     # State 1: Idle Emitter (Muted Blue)
        [14, 165, 233],    # State 2: Retarded Wave (Bright Sky Blue)
        [236, 72, 153],    # State 3: Advanced Wave (Hot Pink)
        [159, 18, 57]      # State 4: Idle Absorber (Muted Rose)
    ],
    9: [
        [10, 10, 14],      # State 0: Unwritten Void (Ink black)
        [2, 132, 199],     # State 1: Timeline A (Vivid Ocean Blue)
        [124, 58, 237],    # State 2: Timeline B (Vivid Violet)
        [249, 115, 22],    # State 3: Paradox Horizon (Bright Orange)
        [253, 224, 71],    # State 4: Time Traveler (Electric Yellow)
        [255, 255, 255]    # State 5: Paradox Excitation (White flash)
    ],
    10: [
        [15, 23, 30],      # State 0: Unshielded Spacetime (Very dark slate)
        [203, 213, 225],   # State 1: Temporal Anchor (Metallic Chrome)
        [16, 185, 129],    # State 2: Chrono-static Shield (Emerald Green)
        [99, 102, 241],    # State 3: Retrocausal Signal (Electric Indigo)
        [244, 63, 94]      # State 4: Tachyon Pulse (Electric Rose)
    ]
}

def get_single_seed_grid(rule_num, W):
    grid = np.zeros(W, dtype=np.int32)
    center = W // 2
    if rule_num == 1:
        # Colliding signals
        grid[center - 80] = 1
        grid[center + 80] = 2
    elif rule_num == 2:
        # Branching origin and expanding domains
        grid[center] = 3
        grid[center - 100] = 1
        grid[center + 100] = 2
    elif rule_num == 3:
        # Emitter and Receiver with a starting artifact
        grid[center - 120] = 3
        grid[center + 120] = 4
        grid[center - 119] = 1
    elif rule_num == 4:
        # Small cluster of CTC seeds
        grid[center - 2] = 1
        grid[center] = 1
        grid[center + 2] = 1
    elif rule_num == 5:
        # Active transmitter and incoming trigger
        grid[center] = 3
        grid[center - 200] = 2
    elif rule_num == 6:
        # Coexistence of phases
        grid[center - 100:center] = 1
        grid[center:center + 100] = 3
    elif rule_num == 7:
        # Fresh traveler and a stationary block
        grid[center - 150] = 1
        grid[center + 50] = 4
    elif rule_num == 8:
        # Emitter and Absorber
        grid[center - 100] = 1
        grid[center + 100] = 4
    elif rule_num == 9:
        # Split half A and half B, with a traveler crossing
        grid[:center] = 1
        grid[center:] = 2
        grid[center + 120] = 4
    elif rule_num == 10:
        # Anchor in the middle, signals arriving from left and right
        grid[center] = 1
        grid[center - 250] = 4  # Tachyon moving right
        grid[center + 250] = 3  # Retrocausal signal moving left
    return grid

def get_random_grid(rule_num, W):
    num_states = len(PALETTES[rule_num])
    
    if rule_num == 1:
        p = [0.94, 0.03, 0.03, 0.00, 0.00]
    elif rule_num == 2:
        p = [0.95, 0.02, 0.02, 0.01, 0.00, 0.00]
    elif rule_num == 3:
        # Periodic emitters and receivers, randomly scattered artifacts
        grid = np.zeros(W, dtype=np.int32)
        grid[::60] = 3
        grid[30::60] = 4
        for x in range(W):
            if grid[x] == 0 and np.random.rand() < 0.04:
                grid[x] = np.random.choice([1, 2])
        return grid
    elif rule_num == 4:
        p = [0.97, 0.03, 0.00, 0.00, 0.00]
    elif rule_num == 5:
        # Scatter transmitters and triggers
        grid = np.zeros(W, dtype=np.int32)
        for x in range(W):
            r = np.random.rand()
            if r < 0.02:
                grid[x] = 3
            elif r < 0.05:
                grid[x] = 2
        return grid
    elif rule_num == 6:
        p = [0.2, 0.2, 0.2, 0.2, 0.2]
    elif rule_num == 7:
        p = [0.96, 0.02, 0.00, 0.00, 0.02, 0.00]
    elif rule_num == 8:
        # Fixed emitters and absorbers
        grid = np.zeros(W, dtype=np.int32)
        grid[::80] = 1
        grid[40::80] = 4
        return grid
    elif rule_num == 9:
        # Branching regions
        grid = np.random.choice([1, 2], size=W, p=[0.5, 0.5])
        # Randomly inject travelers
        for x in range(W):
            if np.random.rand() < 0.01:
                grid[x] = 4
        return grid
    elif rule_num == 10:
        # Randomly placed anchors and signals
        grid = np.zeros(W, dtype=np.int32)
        for x in range(W):
            r = np.random.rand()
            if r < 0.01:
                grid[x] = 1
            elif r < 0.04:
                grid[x] = 3
            elif r < 0.06:
                grid[x] = 4
        return grid
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
        grid = step_rule(rule_num, grid, t)
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
