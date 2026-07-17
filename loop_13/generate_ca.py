import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define Anchor Colors
ANCHORS = {
    1: [[10, 10, 30], [70, 130, 180], [255, 215, 0], [255, 140, 0]],
    2: [[5, 5, 15], [139, 0, 139], [255, 0, 127], [255, 255, 0]],
    3: [[0, 0, 10], [0, 128, 255], [255, 165, 0], [255, 255, 255]],
    4: [[5, 0, 10], [128, 0, 128], [255, 20, 147], [255, 215, 0]],
    5: [[10, 20, 15], [0, 128, 128], [0, 255, 255], [240, 255, 240]],
    6: [[15, 15, 15], [255, 69, 0], [255, 215, 0], [255, 255, 255]],
    7: [[5, 5, 20], [75, 0, 130], [255, 105, 180], [255, 223, 0]],
    8: [[10, 0, 0], [139, 0, 0], [218, 165, 32], [255, 250, 205]],
    9: [[0, 0, 0], [75, 0, 130], [186, 85, 211], [255, 255, 255]],
    10: [[20, 20, 20], [0, 191, 255], [0, 0, 255], [255, 99, 71], [255, 0, 0]]
}

def get_palette(rule_num, num_states):
    anchors = ANCHORS[rule_num]
    if num_states == 2:
        return np.array(anchors, dtype=np.uint8)
    xp = np.linspace(0, 1, len(anchors))
    x = np.linspace(0, 1, num_states)
    r = np.interp(x, xp, [c[0] for c in anchors])
    g = np.interp(x, xp, [c[1] for c in anchors])
    b = np.interp(x, xp, [c[2] for c in anchors])
    return np.stack([r, g, b], axis=-1).astype(np.uint8)

# Set random seed for reproducibility
np.random.seed(42)

# 3. Transition Rules
def rule_1(arr):
    # Quantum Area Spin Network (N=8)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    s_min = np.abs(left - right)
    s_max = np.minimum(7, left + right)
    s_target = (left + right - arr) % 8
    
    # Fluctuation mask: if left and right are 0
    fluct_mask = (left == 0) & (right == 0)
    
    new_arr = np.clip(s_target, s_min, s_max)
    new_arr[fluct_mask] = (arr[fluct_mask] + 1) % 8
    return new_arr

def rule_2(arr):
    # Ashtekar Connection Holonomy Flow (N=13)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (arr + (right - left)**2 + left * right) % 13

def rule_3(arr):
    # Loop Quantum Cosmology Bounce (N=12)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # for arr == 0 (singularity)
    bounce_val = np.maximum(np.maximum(left, right), 3)
    # for arr > 0
    normal_val = np.maximum(0, (left + right) // 2 - 1)
    
    return np.where(arr == 0, bounce_val, normal_val)

def rule_4(arr):
    # Spinfoam Amplitude Sum-Over-Histories (N=6)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    parity = (left + arr + right) % 2
    constructive = (left + right) % 6
    return np.where(parity == 0, constructive, 0)

def rule_5(arr):
    # Semi-Classical Weave State Relaxation (N=8)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    d = np.abs(left - arr) + np.abs(right - arr)
    
    rough_val = (left + arr + right) // 3
    smooth_val = (arr + left - right + 1) % 8
    
    return np.where(d >= 3, rough_val, smooth_val)

def rule_6(arr):
    # Hamiltonian Constraint Vertex Excitation (N=5)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # Mask for arr == 0 (vacuum)
    mask_vac = (arr == 0)
    sum_neighbors = left + right
    vac_excited = np.where((sum_neighbors == 2) | (sum_neighbors == 4), 1, 0)
    
    # Mask for active excitations (1, 2, 3)
    mask_active = (arr >= 1) & (arr <= 3)
    
    # Conditions for active
    annihilate = (left >= 1) & (right >= 1)
    fluctuate = (left == 0) & (right == 0)
    propagate = ~annihilate & ~fluctuate
    
    active_val = np.zeros_like(arr)
    active_val = np.where(annihilate, arr - 1, active_val)
    active_val = np.where(fluctuate, (arr + 1) % 4, active_val)
    active_val = np.where(propagate, np.maximum(left, right), active_val)
    
    new_arr = np.zeros_like(arr)
    new_arr = np.where(mask_vac, vac_excited, new_arr)
    new_arr = np.where(mask_active, active_val, new_arr)
    # for arr == 4, it decays to 0, which is handled since default is 0
    return new_arr

def rule_7(arr):
    # Kodama State Phase Instability (N=12)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    delta = (right - left) % 12
    
    stable_val = (arr + 1) % 12
    unstable_val = (arr + 3 * delta + arr**2) % 12
    
    return np.where(delta == 0, stable_val, unstable_val)

def rule_8(arr):
    # Causal Dynamical Triangulations (N=8)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    tear = np.abs(left - right) > 3
    glue_val = (left + right) // 2
    branch_val = (arr + (left % 2) - (right % 2) + 8) % 8
    
    return np.where(tear, glue_val, branch_val)

def rule_9(arr):
    # Black Hole Horizon Pixelation (N=8)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    flux = left + right
    
    absorb_val = np.minimum(7, arr + 1)
    emit_val = np.maximum(0, arr - 1)
    
    # equilibrium
    eq_val = np.where(arr % 2 == 0, (arr + 1) % 8, arr - 1)
    
    new_arr = np.zeros_like(arr)
    new_arr = np.where(flux >= 8, absorb_val, new_arr)
    new_arr = np.where(flux < 4, emit_val, new_arr)
    new_arr = np.where((flux >= 4) & (flux < 8), eq_val, new_arr)
    return new_arr

def rule_10(arr):
    # Chiral Immirzi Asymmetry (N=5)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # mask for weak chiral (1, 3)
    mask_weak = (arr == 1) | (arr == 3)
    weak_val = np.where(right > left, right, left)
    
    # mask for strong chiral (2, 4)
    mask_strong = (arr == 2) | (arr == 4)
    strong_val = (arr + left - 2 * right + 5) % 5
    
    # mask for neutral (0)
    mask_neutral = (arr == 0)
    neutral_val = np.zeros_like(arr)
    neutral_val = np.where((left > right) & (left > 0), 1, neutral_val)
    neutral_val = np.where((right > left) & (right > 0), 3, neutral_val)
    
    new_arr = np.zeros_like(arr)
    new_arr = np.where(mask_weak, weak_val, new_arr)
    new_arr = np.where(mask_strong, strong_val, new_arr)
    new_arr = np.where(mask_neutral, neutral_val, new_arr)
    return new_arr

RULES = {
    1: (rule_1, 8),
    2: (rule_2, 13),
    3: (rule_3, 12),
    4: (rule_4, 6),
    5: (rule_5, 8),
    6: (rule_6, 5),
    7: (rule_7, 12),
    8: (rule_8, 8),
    9: (rule_9, 8),
    10: (rule_10, 5)
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        grid[0, W // 2] = num_states - 1
        if rule_num == 3: # LQC bounce needs a few seed points to keep running
            grid[0, W // 2 - 10] = 5
            grid[0, W // 2] = 11
            grid[0, W // 2 + 10] = 7
    elif init_type == "random":
        grid[0] = np.random.randint(0, num_states, size=W, dtype=np.int32)
        
    for t in range(H - 1):
        grid[t + 1] = rule_func(grid[t])
        
    palette = get_palette(rule_num, num_states)
    rgb_data = palette[grid]
    
    img = Image.fromarray(rgb_data)
    filename = f"rule_{rule_num:02d}_{init_type}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"Saved: {filepath}")

def main():
    for rule_num in sorted(RULES.keys()):
        for init_type in ["single_seed", "random"]:
            simulate_and_save(rule_num, init_type)
    print("Simulation complete.")

if __name__ == "__main__":
    main()
