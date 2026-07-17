import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define the 10 Rule Functions (with periodic boundary wrapping using np.roll)

def rule_1(arr):
    # States: 8
    # Neighborhood: r=2 excluding self
    next_s = (arr + 1) % 8
    count = (
        (np.roll(arr, 2) == next_s).astype(int) +
        (np.roll(arr, 1) == next_s).astype(int) +
        (np.roll(arr, -1) == next_s).astype(int) +
        (np.roll(arr, -2) == next_s).astype(int)
    )
    return np.where(count >= 2, next_s, arr)

def rule_2(arr):
    # States: 6. 0: quiescent, 1: excited, 2-5: refractory
    # Neighborhood: r=1 excluding self
    is_excited_neighbor = (
        (np.roll(arr, 1) == 1).astype(int) +
        (np.roll(arr, -1) == 1).astype(int)
    )
    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    new_arr[mask_zero] = np.where(is_excited_neighbor[mask_zero] == 1, 1, 0)
    
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 6
    return new_arr

def rule_3(arr):
    # States: 5
    # Neighborhood: r=2 (left-heavy: x-2, x-1, x+1)
    # Weights: w(-2)=1, w(-1)=2, w(1)=1
    next_s = (arr + 1) % 5
    c = (
        1 * (np.roll(arr, 2) == next_s).astype(int) +
        2 * (np.roll(arr, 1) == next_s).astype(int) +
        1 * (np.roll(arr, -1) == next_s).astype(int)
    )
    return np.where(c >= 2, next_s, arr)

def rule_4(arr):
    # States: 8. 0: quiescent, 1,2: excited, 3-7: refractory
    # Neighborhoods: Inner r=1, Outer r=3 (x-3, x-2, x+2, x+3)
    E = ((arr == 1) | (arr == 2)).astype(int)
    sum_in = np.roll(E, 1) + np.roll(E, -1)
    sum_out = np.roll(E, 3) + np.roll(E, 2) + np.roll(E, -2) + np.roll(E, -3)
    
    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    excite = (sum_in >= 1) | (sum_out >= 1)
    new_arr[mask_zero] = np.where(excite[mask_zero], 1, 0)
    
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 8
    return new_arr

def rule_5(arr):
    # States: 4
    # Neighborhood: r=2 excluding self
    next_s = (arr + 1) % 4
    inhibit_s = (arr + 2) % 4
    c_next = (
        (np.roll(arr, 2) == next_s).astype(int) +
        (np.roll(arr, 1) == next_s).astype(int) +
        (np.roll(arr, -1) == next_s).astype(int) +
        (np.roll(arr, -2) == next_s).astype(int)
    )
    c_inhibit = (
        (np.roll(arr, 2) == inhibit_s).astype(int) +
        (np.roll(arr, 1) == inhibit_s).astype(int) +
        (np.roll(arr, -1) == inhibit_s).astype(int) +
        (np.roll(arr, -2) == inhibit_s).astype(int)
    )
    return np.where((c_next >= 1) & (c_inhibit < 2), next_s, arr)

def rule_6(arr):
    # States: 10. 0: quiescent, 1: excited, 2-9: refractory
    # Neighborhood: r=2
    # V_t(x) = sum_{i=-2}^{2} (i+3)*S_t(x+i)
    # E_t(x) = count of excited (1) in x-2, x-1, x+1, x+2
    V = 1 * np.roll(arr, 2) + 2 * np.roll(arr, 1) + 3 * arr + 4 * np.roll(arr, -1) + 5 * np.roll(arr, -2)
    E = (
        (np.roll(arr, 2) == 1).astype(int) +
        (np.roll(arr, 1) == 1).astype(int) +
        (np.roll(arr, -1) == 1).astype(int) +
        (np.roll(arr, -2) == 1).astype(int)
    )
    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    v_mod = V % 7
    condition = (E >= 1) & ((v_mod == 1) | (v_mod == 3) | (v_mod == 5))
    new_arr[mask_zero] = np.where(condition[mask_zero], 1, 0)
    
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 10
    return new_arr

def rule_7(arr):
    # States: 6
    # Neighborhood: r=2 excluding self
    s1 = (arr + 1) % 6
    s2 = (arr + 2) % 6
    c1 = (
        (np.roll(arr, 2) == s1).astype(int) +
        (np.roll(arr, 1) == s1).astype(int) +
        (np.roll(arr, -1) == s1).astype(int) +
        (np.roll(arr, -2) == s1).astype(int)
    )
    c2 = (
        (np.roll(arr, 2) == s2).astype(int) +
        (np.roll(arr, 1) == s2).astype(int) +
        (np.roll(arr, -1) == s2).astype(int) +
        (np.roll(arr, -2) == s2).astype(int)
    )
    new_arr = np.copy(arr)
    mask_double = (c2 >= 2) & (c1 < 2)
    mask_single = (~mask_double) & (c1 >= 1)
    new_arr[mask_double] = s2[mask_double]
    new_arr[mask_single] = s1[mask_single]
    return new_arr

def rule_8(arr):
    # States: 12. 0: quiescent, 1: excited, 2-11: refractory
    # Neighborhood: r=2 excluding self
    is_ref = ((arr >= 2) & (arr <= 11)).astype(int)
    R = (
        np.roll(is_ref, 2) +
        np.roll(is_ref, 1) +
        np.roll(is_ref, -1) +
        np.roll(is_ref, -2)
    )
    is_exc = (arr == 1).astype(int)
    E = (
        np.roll(is_exc, 2) +
        np.roll(is_exc, 1) +
        np.roll(is_exc, -1) +
        np.roll(is_exc, -2)
    )
    threshold = np.where(R <= 1, 1, 2)
    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    excite = (E >= threshold)
    new_arr[mask_zero] = np.where(excite[mask_zero], 1, 0)
    
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 12
    return new_arr

def rule_9(arr):
    # States: 7. 0: quiescent, 1: excited, 2-6: refractory
    # Neighborhood: r=1 excluding self
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    S = left + right
    new_arr = np.copy(arr)
    mask_zero = (arr == 0)
    condition = ((S % 2) != 0) & (S > 0)
    new_arr[mask_zero] = np.where(condition[mask_zero], 1, 0)
    
    mask_active = (arr >= 1)
    new_arr[mask_active] = (arr[mask_active] + 1) % 7
    return new_arr

def rule_10(arr):
    # States: 8
    # Neighborhoods: N1 (r=1 excluding self), N2 (r=2 excluding self)
    next_s = (arr + 1) % 8
    c1 = (
        (np.roll(arr, 1) == next_s).astype(int) +
        (np.roll(arr, -1) == next_s).astype(int)
    )
    c2 = (
        (np.roll(arr, 2) == next_s).astype(int) +
        (np.roll(arr, 1) == next_s).astype(int) +
        (np.roll(arr, -1) == next_s).astype(int) +
        (np.roll(arr, -2) == next_s).astype(int)
    )
    new_arr = np.copy(arr)
    is_even = (arr % 2 == 0)
    is_odd = ~is_even
    mask_even_trigger = is_even & (c1 >= 1)
    mask_odd_trigger = is_odd & (c2 >= 2)
    new_arr[mask_even_trigger] = next_s[mask_even_trigger]
    new_arr[mask_odd_trigger] = next_s[mask_odd_trigger]
    return new_arr


# 3. Unique Vibrant Color Palettes for each rule

PALETTES = {
    1: [
        [10, 10, 30],     # 0: deep indigo
        [0, 50, 150],     # 1: dark blue
        [0, 120, 200],    # 2: blue
        [0, 200, 200],    # 3: cyan
        [0, 230, 150],    # 4: teal-green
        [150, 230, 50],   # 5: lime
        [230, 150, 50],   # 6: orange
        [230, 50, 150],   # 7: pink-magenta
    ],
    2: [
        [15, 15, 20],     # 0: quiescent (black-blue)
        [255, 255, 200],  # 1: excited (neon pale yellow)
        [255, 50, 50],    # 2: bright red
        [200, 0, 120],    # 3: rose
        [120, 0, 180],    # 4: purple
        [50, 0, 120],     # 5: dark blue-purple
    ],
    3: [
        [20, 30, 20],     # 0: dark forest green
        [0, 150, 80],     # 1: emerald green
        [0, 220, 100],    # 2: neon green
        [200, 250, 50],   # 3: bright lime yellow
        [250, 180, 0],    # 4: bright orange-gold
    ],
    4: [
        [10, 5, 5],       # 0: almost black
        [255, 255, 255],  # 1: white-hot
        [255, 230, 0],    # 2: bright yellow
        [255, 140, 0],    # 3: orange
        [230, 50, 0],     # 4: red
        [160, 0, 80],     # 5: crimson
        [90, 0, 120],     # 6: plum purple
        [30, 0, 60],      # 7: deep violet
    ],
    5: [
        [10, 10, 20],     # 0: dark night
        [0, 255, 240],    # 1: neon cyan
        [255, 0, 128],    # 2: neon pink
        [240, 255, 0],    # 3: neon yellow
    ],
    6: [
        [5, 5, 10],       # 0: very dark indigo
        [255, 0, 255],    # 1: bright magenta
        [0, 255, 255],    # 2: bright cyan
        [0, 255, 128],    # 3: neon green-blue
        [128, 255, 0],    # 4: bright lime
        [255, 255, 0],    # 5: neon yellow
        [255, 128, 0],    # 6: neon orange
        [255, 0, 128],    # 7: bright pink
        [128, 0, 255],    # 8: purple
        [64, 0, 128],     # 9: dark violet
    ],
    7: [
        [10, 25, 40],     # 0: deep ocean blue
        [20, 80, 120],    # 1: steel blue
        [30, 150, 180],   # 2: teal
        [100, 220, 200],  # 3: light sea green
        [240, 180, 120],  # 4: peach/coral
        [250, 120, 90],   # 5: bright salmon
    ],
    8: [
        [15, 15, 15],     # 0: dark gray
        [255, 0, 50],     # 1: bright red
        [255, 100, 100],  # 2: light red/pink
        [255, 180, 50],   # 3: orange-gold
        [220, 220, 50],   # 4: yellow-green
        [50, 220, 100],   # 5: lime green
        [0, 200, 180],    # 6: turquoise
        [0, 150, 220],    # 7: light blue
        [0, 80, 200],     # 8: royal blue
        [80, 0, 180],     # 9: indigo
        [120, 0, 120],    # 10: purple
        [60, 10, 60],     # 11: dark magenta
    ],
    9: [
        [20, 10, 5],      # 0: dark chocolate
        [255, 220, 150],  # 1: bright pale gold
        [230, 170, 80],   # 2: warm gold
        [200, 120, 40],   # 3: copper
        [160, 80, 20],    # 4: bronze
        [110, 50, 10],    # 5: dark copper
        [60, 25, 5],      # 6: deep brown
    ],
    10: [
        [20, 10, 30],     # 0: deep purple-black
        [80, 20, 100],    # 1: violet
        [150, 30, 120],   # 2: magenta
        [220, 40, 80],    # 3: hot pink
        [255, 80, 40],    # 4: neon orange-red
        [255, 150, 30],   # 5: bright orange
        [255, 210, 50],   # 6: gold
        [255, 255, 180],  # 7: pale yellow-white
    ],
}


# 4. Simulation Engine and Main Loop

RULES = {
    1: (rule_1, 8),
    2: (rule_2, 6),
    3: (rule_3, 5),
    4: (rule_4, 8),
    5: (rule_5, 4),
    6: (rule_6, 10),
    7: (rule_7, 6),
    8: (rule_8, 12),
    9: (rule_9, 7),
    10: (rule_10, 8),
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    
    # Initialize the grid
    grid = np.zeros((H, W), dtype=np.int32)
    if init_type == "single_seed":
        grid[0, W // 2] = 1
    elif init_type == "random":
        grid[0] = np.random.randint(0, num_states, size=W)
        
    # Simulate
    for t in range(H - 1):
        grid[t + 1] = rule_func(grid[t])
        
    # Convert grid to RGB using palette
    palette = PALETTES[rule_num]
    palette_arr = np.array(palette, dtype=np.uint8)
    rgb_data = palette_arr[grid]
    
    # Save to PNG
    img = Image.fromarray(rgb_data)
    filename = f"rule_{rule_num:02d}_{init_type}.png"
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
