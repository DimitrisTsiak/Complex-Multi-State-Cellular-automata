import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define Anchor Colors
ANCHORS = {
    1: [[10, 10, 20], [34, 139, 34], [255, 215, 0], [255, 69, 0], [139, 0, 0]],
    2: [[0, 0, 0], [57, 255, 20]],
    3: [[5, 5, 25], [0, 191, 255]],
    4: [[15, 0, 30], [255, 0, 255], [255, 127, 0], [255, 255, 0]],
    5: [[10, 15, 20], [0, 255, 255], [255, 255, 255]],
    6: [[5, 5, 5], [160, 82, 45], [218, 165, 32], [255, 250, 205]],
    7: [[20, 20, 20], [255, 0, 0], [255, 165, 0], [255, 255, 0], [0, 255, 0]],
    8: [[0, 0, 0], [135, 206, 235], [255, 69, 0], [255, 255, 255]],
    9: [[10, 10, 10], [0, 240, 255]],
    10: [[15, 5, 5], [255, 99, 71], [255, 215, 0], [144, 238, 144]]
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
    # Stochastic Majority: Vote with noise
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    stacked = np.stack([left, arr, right], axis=0)
    maj = np.zeros_like(arr)
    for i in range(5):
        c = np.sum(stacked == i, axis=0)
        maj = np.where(c >= 2, i, maj)
    r = np.random.random(arr.shape)
    rand_val = np.random.randint(0, 5, size=arr.shape)
    return np.where(r < 0.88, maj, rand_val)

def rule_2(arr):
    # Stochastic Contact Process: Active=1 infects neighbors, Active recovers to 0
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    has_active_neighbor = (left == 1) | (right == 1)
    
    new_arr = arr.copy()
    # Infection: 0 -> 1 with prob 0.6 if has active neighbor
    infect_mask = (arr == 0) & has_active_neighbor & (np.random.random(arr.shape) < 0.6)
    new_arr[infect_mask] = 1
    # Recovery: 1 -> 0 with prob 0.15
    recover_mask = (arr == 1) & (np.random.random(arr.shape) < 0.15)
    new_arr[recover_mask] = 0
    return new_arr

def rule_3(arr):
    # Directed Percolation: 1 propagates to neighbor with prob 0.65
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    r_left = np.random.random(arr.shape) < 0.65
    r_right = np.random.random(arr.shape) < 0.65
    
    prop = (left == 1) & r_left | (right == 1) & r_right
    return prop.astype(np.int32)

def rule_4(arr):
    # Stochastic Excitable Media
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    excited = ((left == 1) | (right == 1)).astype(int)
    
    new_arr = arr.copy()
    # 0 -> 1 (excite) with prob 0.7 if neighbor excited
    mask_zero = (arr == 0)
    excite_prob = np.random.random(arr.shape) < 0.7
    new_arr[mask_zero] = np.where(excited[mask_zero] & excite_prob[mask_zero], 1, 0)
    
    # Active states decay
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 8
    return new_arr

def rule_5(arr):
    # Noisy Majority (N=3)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    stacked = np.stack([left, arr, right], axis=0)
    maj = np.zeros_like(arr)
    for i in range(3):
        c = np.sum(stacked == i, axis=0)
        maj = np.where(c >= 2, i, maj)
    r = np.random.random(arr.shape)
    return np.where(r < 0.95, maj, np.random.randint(0, 3, size=arr.shape))

def rule_6(arr):
    # Markovian Diffusion N=10
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # Probability to step left, right, or stay
    r = np.random.random(arr.shape)
    new_arr = arr.copy()
    
    # Move some density
    move_left = (r < 0.33) & (left > 0)
    move_right = (r > 0.66) & (right > 0)
    
    new_arr = np.where(move_left, (left - 1) % 10, new_arr)
    new_arr = np.where(move_right, (right - 1) % 10, new_arr)
    return new_arr

def rule_7(arr):
    # Traffic Nagel-Schreckenberg (simplified)
    # State represents velocity (0=empty, 1..5 = speed)
    # Cars move, accelerate, slow down, and randomly decelerate
    new_arr = np.zeros_like(arr)
    cars = (arr > 0)
    
    # Acceleration
    v = np.where(cars, np.minimum(arr + 1, 5), 0)
    
    # Slow down due to gap (lookahead)
    # We find next car index
    indices = np.where(cars)[0]
    if len(indices) > 1:
        gaps = np.roll(indices, -1) - indices
        gaps = np.where(gaps < 0, gaps + len(arr), gaps) - 1
        
        # update v based on gaps
        v_cars = v[indices]
        v_cars = np.minimum(v_cars, gaps)
        v[indices] = v_cars
        
    # Random deceleration
    r = np.random.random(arr.shape)
    v = np.where(cars & (v > 1) & (r < 0.2), v - 1, v)
    
    # Move cars
    for idx in np.where(cars)[0]:
        speed = int(v[idx])
        dest = (idx + speed) % len(arr)
        new_arr[dest] = speed
    return new_arr

def rule_8(arr):
    # Stochastic Sandpile
    # If state >= 4, topple: distribute 2 grains randomly left or right, 2 locally
    new_arr = arr.copy()
    topple_mask = arr >= 4
    
    # subtract 4 from toppling cells
    new_arr[topple_mask] -= 4
    
    # distribute grains
    indices = np.where(topple_mask)[0]
    for idx in indices:
        # left grain: 70% left, 30% right
        dest_l = (idx - 1) % len(arr) if np.random.random() < 0.7 else (idx + 1) % len(arr)
        # right grain: 70% right, 30% left
        dest_r = (idx + 1) % len(arr) if np.random.random() < 0.7 else (idx - 1) % len(arr)
        
        new_arr[dest_l] += 1
        new_arr[dest_r] += 1
        new_arr[idx] += 2 # keep 2 locally
        
    return np.minimum(new_arr, 15)

def rule_9(arr):
    # Metropolis Ising Model N=2 (0, 1 maps to spin -1, 1)
    spins = np.where(arr == 1, 1, -1)
    left = np.roll(spins, 1)
    right = np.roll(spins, -1)
    
    # Energy change: dE = 2 * spin * (left + right)
    dE = 2 * spins * (left + right)
    
    # Flip if dE <= 0, or with Boltzmann probability if dE > 0
    # Temperature T = 1.8
    r = np.random.random(arr.shape)
    flip = (dE <= 0) | (r < np.exp(-dE / 1.8))
    
    new_spins = np.where(flip, -spins, spins)
    return np.where(new_spins == 1, 1, 0)

def rule_10(arr):
    # Stochastic Chiral Growth
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # Growth probability is higher to the right
    r = np.random.random(arr.shape)
    new_arr = arr.copy()
    
    mask_zero = arr == 0
    grow_right = (right > 0) & (r < 0.65)
    grow_left = (left > 0) & (r < 0.25)
    
    new_arr[mask_zero & grow_right] = ((right[mask_zero & grow_right] + 1) % 5)
    new_arr[mask_zero & grow_left] = ((left[mask_zero & grow_left] + 1) % 5)
    
    return new_arr

RULES = {
    1: (rule_1, 5),
    2: (rule_2, 2),
    3: (rule_3, 2),
    4: (rule_4, 8),
    5: (rule_5, 3),
    6: (rule_6, 10),
    7: (rule_7, 6),
    8: (rule_8, 16),
    9: (rule_9, 2),
    10: (rule_10, 5)
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        grid[0, W // 2] = 1 if num_states > 2 else 1
        if rule_num == 8: # Sandpile needs high density at center
            grid[0, W // 2] = 15
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
