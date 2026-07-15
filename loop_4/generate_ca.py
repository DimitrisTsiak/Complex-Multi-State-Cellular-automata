import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Rule Transition Functions

def rule_1(arr):
    # Classical 1D Abelian Sandpile (N=4 states: 0, 1, 2, 3)
    # Neighborhood: r=1 including self
    # Topples if state >= 2
    tau = (arr >= 2).astype(np.int32)
    left = np.roll(tau, 1)
    right = np.roll(tau, -1)
    return arr - 2 * tau + left + right

def rule_2(arr):
    # Slope-Dependent Granular Slide (N=5 states: 0, 1, 2, 3, 4)
    # Neighborhood: r=1
    # Downhill flow from x to x+1 occurs if S_t(x) - S_t(x+1) >= 2
    flow_right = (arr - np.roll(arr, -1) >= 2).astype(np.int32)
    flow_from_left = np.roll(flow_right, 1)
    return arr - flow_right + flow_from_left

def rule_3(arr, t):
    # Reversible Odd-Even Segregation (N=3 states: 0, 1, 2)
    # Block Partition: even t uses {2k, 2k+1}, odd t uses {2k-1, 2k}
    # Left and right cells of a block swap values if L > R
    W = len(arr)
    if t % 2 == 0:
        left_idx = np.arange(0, W, 2)
        right_idx = np.arange(1, W, 2)
    else:
        left_idx = (np.arange(0, W, 2) - 1) % W
        right_idx = np.arange(0, W, 2)

    L_vals = arr[left_idx]
    R_vals = arr[right_idx]
    
    swap_mask = L_vals > R_vals
    
    new_arr = np.copy(arr)
    new_arr[left_idx[swap_mask]] = R_vals[swap_mask]
    new_arr[right_idx[swap_mask]] = L_vals[swap_mask]
    return new_arr

def rule_4(arr):
    # Granular Consolidation & Arching (N=4 states: 0, 1, 2, 3)
    # Neighborhood: r=1, gravity pulls to the right (+x)
    # 0 -> 1 if left is 1 (loose sand flows right)
    # 1 -> 0 if right is 0, -> 2 if right is 2 or 3 (loose sand compacts if supported)
    # 2 -> 1 if right is 0 (compacted sand becomes loose if support is lost)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.copy(arr)
    
    mask_0 = (arr == 0)
    new_arr[mask_0] = np.where(left[mask_0] == 1, 1, 0)
    
    mask_1 = (arr == 1)
    new_arr[mask_1] = np.where(right[mask_1] == 0, 0,
                               np.where((right[mask_1] == 2) | (right[mask_1] == 3), 2, 1))
                               
    mask_2 = (arr == 2)
    new_arr[mask_2] = np.where(right[mask_2] == 0, 1, 2)
    
    return new_arr

def rule_5(arr):
    # Dynamic-Threshold Sandpile (N=6 states: 0, 1, 2, 3, 4, 5)
    # Neighborhood: r=1
    # Topples if S(x) >= 4 or (S(x) == 3 and neighbor toppling >= 4)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    tau = np.zeros_like(arr, dtype=np.int32)
    tau[arr >= 4] = 1
    cond_3 = (arr == 3) & ((left >= 4) | (right >= 4))
    tau[cond_3] = 1
    
    left_tau = np.roll(tau, 1)
    right_tau = np.roll(tau, -1)
    return arr - 2 * tau + left_tau + right_tau

def rule_6(arr):
    # Wind-Blown Sand (Saltation & Creep) (N=3 states: 0, 1, 2)
    # Neighborhood: r=2, wind blows to the right (+x)
    # 0: empty, 1: light (saltates/jumps 2), 2: heavy (creeps/rolls 1)
    left1 = np.roll(arr, 1)
    left2 = np.roll(arr, 2)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)
    
    C1 = (left1 == 2) & (arr == 0)
    C2 = (left2 == 1) & (arr == 0) & (left1 != 2)
    C3 = (arr == 2) & (right1 == 0) & ~((left2 == 1) & (left1 != 2))
    C4 = (arr == 1) & (right2 == 0) & (right1 != 2)
    
    new_arr = np.copy(arr)
    new_arr[C3] = 0
    new_arr[C4] = 0
    new_arr[C1] = 2
    new_arr[C2] = 1
    return new_arr

def rule_7(arr):
    # Frictional Arrest (Granular Jamming) (N=3 states: 0, 1, 2)
    # Neighborhood: r=2 favoring left: {x-2, x-1, x, x+1}
    # 0: empty, 1: flowing sand (moving right), 2: jammed/solid sand
    left1 = np.roll(arr, 1)
    left2 = np.roll(arr, 2)
    right1 = np.roll(arr, -1)
    
    C1 = (arr == 1) & ((left1 == 1) | (right1 == 1))
    C2 = (arr == 2) & (right1 == 0)
    C3 = (arr == 0) & (left1 == 1) & (left2 != 1)
    C4 = (arr == 1) & (right1 == 0) & (left1 != 1)
    
    new_arr = np.copy(arr)
    new_arr[C1] = 2
    new_arr[C2] = 1
    new_arr[C3] = 1
    new_arr[C4] = 0
    return new_arr

def rule_8(arr):
    # Friction-Induced Dissipation (N=4 states: 0, 1, 2, 3)
    # Neighborhood: r=1. Empty space (0) absorbs sand grains permanently.
    tau = (arr >= 2).astype(np.int32)
    is_gt_0 = (arr >= 1).astype(np.int32)
    
    # flow_from_left is flow from x-1 to x (which is to the right)
    # phi(x-1 -> x) = \tau_t(x-1) * I(S_t(x) >= 1)
    flow_from_left = np.roll(tau, 1) * is_gt_0
    
    # flow_from_right is flow from x+1 to x (which is to the left)
    # phi(x+1 -> x) = \tau_t(x+1) * I(S_t(x) >= 1)
    flow_from_right = np.roll(tau, -1) * is_gt_0
    
    return arr - 2 * tau + flow_from_left + flow_from_right

def rule_9(arr):
    # Momentum-Driven Snow Avalanche (N=4 states: 0, 1, 2, 3)
    # Neighborhood: r=2, gravity flows to the right (+x)
    # 0: empty, 1: stable snow, 2: unstable snow, 3: active avalanche
    left1 = np.roll(arr, 1)
    left2 = np.roll(arr, 2)
    right1 = np.roll(arr, -1)
    
    C_to_3 = (left1 == 3) & ((arr == 0) | (arr == 2) | ((arr == 1) & (left2 == 3)))
    C_to_0 = (arr == 3) & ((right1 == 0) | (right1 == 2) | ((right1 == 1) & (left1 == 3)))
    C_to_1 = (arr == 3) & ~C_to_0
    
    new_arr = np.copy(arr)
    new_arr[C_to_0] = 0
    new_arr[C_to_1] = 1
    new_arr[C_to_3] = 3
    return new_arr

def rule_10(arr, t):
    # Granular Percolation (Reverse Grading) (N=4 states: 0, 1, 2, 3)
    # Block Partition: even t uses {2k, 2k+1}, odd t uses {2k-1, 2k}
    # 0: empty, 3: large, 2: medium, 1: small
    # (L, R) -> (R, L) if L >= 1 and R >= 1 and L < R (small particles sift down)
    # (L, R) -> (0, L) if L >= 1 and R == 0 (particles fall into empty space)
    W = len(arr)
    if t % 2 == 0:
        left_idx = np.arange(0, W, 2)
        right_idx = np.arange(1, W, 2)
    else:
        left_idx = (np.arange(0, W, 2) - 1) % W
        right_idx = np.arange(0, W, 2)

    L_vals = arr[left_idx]
    R_vals = arr[right_idx]
    
    swap_mask = ((L_vals >= 1) & (R_vals >= 1) & (L_vals < R_vals)) | ((L_vals >= 1) & (R_vals == 0))
    
    new_arr = np.copy(arr)
    new_arr[left_idx[swap_mask]] = R_vals[swap_mask]
    new_arr[right_idx[swap_mask]] = L_vals[swap_mask]
    return new_arr

# 3. Unique Vibrant Color Palettes (RGB)

PALETTES = {
    1: [
        [10, 10, 25],     # 0: deep black-indigo
        [30, 120, 255],   # 1: medium blue
        [255, 0, 128],    # 2: vibrant magenta
        [255, 235, 0]     # 3: neon yellow
    ],
    2: [
        [15, 15, 20],     # 0: dark charcoal
        [180, 90, 20],    # 1: warm copper
        [255, 150, 0],    # 2: gold/orange
        [255, 220, 50],   # 3: bright yellow
        [255, 255, 180]   # 4: brilliant white-yellow
    ],
    3: [
        [15, 5, 25],      # 0: deep violet-black
        [0, 230, 200],    # 1: vibrant teal/cyan
        [255, 60, 0]      # 2: neon orange-red
    ],
    4: [
        [5, 10, 30],      # 0: midnight blue
        [50, 255, 50],    # 1: neon green (loose sand)
        [230, 50, 250],   # 2: bright pink-purple (compacted sand)
        [180, 30, 50]     # 3: dark red-gray (solid rock barrier)
    ],
    5: [
        [5, 25, 10],      # 0: deep forest green
        [10, 120, 60],    # 1: emerald green
        [100, 240, 20],   # 2: bright lime green
        [0, 255, 240],    # 3: cyan
        [255, 110, 0],    # 4: vibrant orange
        [255, 20, 147]    # 5: hot pink
    ],
    6: [
        [10, 10, 15],     # 0: dark space
        [0, 191, 255],    # 1: electric sky blue (light sand)
        [255, 215, 0]     # 2: gold-yellow (heavy sand)
    ],
    7: [
        [20, 25, 30],     # 0: dark slate-gray
        [57, 255, 20],    # 1: neon lime green (flowing sand)
        [220, 20, 60]     # 2: crimson red (jammed/solid sand)
    ],
    8: [
        [10, 15, 45],     # 0: deep navy blue
        [150, 100, 255],  # 1: light purple
        [0, 200, 255],    # 2: electric blue
        [255, 100, 80]    # 3: neon coral
    ],
    9: [
        [15, 0, 30],      # 0: dark purple
        [200, 230, 255],  # 1: pale blue-white (stable snowpack)
        [0, 80, 220],     # 2: deep blue (unstable snowpack)
        [255, 69, 0]      # 3: neon orange-red (active avalanche)
    ],
    10: [
        [5, 5, 5],        # 0: deep black
        [75, 0, 130],     # 1: indigo (small particles)
        [255, 20, 147],   # 2: hot pink (medium particles)
        [173, 255, 47]    # 3: neon yellow-green (large particles)
    ]
}

# 4. Simulation Configs & Execution

RULES = {
    1: (rule_1, 4),
    2: (rule_2, 5),
    3: (rule_3, 3),
    4: (rule_4, 4),
    5: (rule_5, 6),
    6: (rule_6, 3),
    7: (rule_7, 3),
    8: (rule_8, 4),
    9: (rule_9, 4),
    10: (rule_10, 4)
}

# Values to initialize for a single seed to trigger correct rule dynamics
SEED_VALUES = {
    1: 3,  # Classical Sandpile (threshold is 2, 3 will topple)
    2: 4,  # Slope-Dependent Slide (threshold is 2, 4 will slide)
    3: 2,  # Segregation (heavy particle, will move)
    4: 1,  # Consolidation (1 is loose sand, which will flow)
    5: 5,  # Dynamic Sandpile (threshold is 4, 5 will topple)
    6: 1,  # Wind-Blown Sand (1 is light sand, which saltates)
    7: 1,  # Granular Jamming (1 is flowing sand, which flows)
    8: 3,  # Dissipation (threshold is 2, 3 will topple)
    9: 3,  # Snow Avalanche (3 is active avalanche, which slides)
    10: 3  # Granular Percolation (3 is large particle, will move)
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    
    # Initialize the space-time history grid
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        # Single-seed initialization: middle cell is set to rule-specific active seed value
        seed_val = SEED_VALUES[rule_num]
        grid[0, W // 2] = seed_val
    elif init_type == "random":
        # Random initialization: all cells are independent random states in [0, N-1]
        grid[0] = np.random.randint(0, num_states, size=W, dtype=np.int32)
        
    # Simulate step-by-step
    for t in range(H - 1):
        if rule_num in [3, 10]:
            grid[t + 1] = rule_func(grid[t], t)
        else:
            grid[t + 1] = rule_func(grid[t])
            
    # Map the state grid (H, W) to RGB (H, W, 3) using rule palette
    palette = np.array(PALETTES[rule_num], dtype=np.uint8)
    rgb_data = palette[grid]
    
    # Create PIL Image and save
    img = Image.fromarray(rgb_data)
    filename = f"rule_{rule_num}_{init_type}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"Saved: {filepath}")

def main():
    # Run simulation for all rules and initializations
    for rule_num in sorted(RULES.keys()):
        for init_type in ["single_seed", "random"]:
            simulate_and_save(rule_num, init_type)
    print("Simulation complete. All 20 files generated.")

if __name__ == "__main__":
    main()
