import os
import numpy as np
from PIL import Image

# Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Custom highly vibrant, biologically-inspired color palettes for each rule
PALETTES = {
    1: np.array([[15, 20, 30], [0, 255, 255], [255, 140, 0], [160, 82, 45], [238, 130, 238]], dtype=np.uint8),
    2: np.array([[5, 15, 40], [173, 255, 47], [255, 20, 147], [255, 255, 0], [20, 20, 20]], dtype=np.uint8),
    3: np.array([[10, 5, 25], [100, 200, 255], [255, 50, 50], [50, 50, 255], [255, 255, 255], [200, 100, 0]], dtype=np.uint8),
    4: np.array([[30, 25, 25], [218, 165, 32], [47, 79, 79], [50, 205, 50], [255, 69, 0]], dtype=np.uint8),
    5: np.array([[0, 15, 20], [0, 255, 127], [0, 191, 255], [255, 223, 0], [255, 0, 255]], dtype=np.uint8),
    6: np.array([[5, 5, 10], [255, 215, 0], [112, 128, 144], [224, 255, 255], [255, 0, 60], [57, 255, 20]], dtype=np.uint8),
    7: np.array([[25, 25, 30], [184, 115, 51], [138, 43, 226], [72, 61, 139], [0, 255, 255]], dtype=np.uint8),
    8: np.array([[20, 40, 20], [255, 165, 0], [255, 0, 127], [0, 206, 209], [245, 245, 220]], dtype=np.uint8),
    9: np.array([[10, 10, 35], [0, 255, 204], [75, 0, 130], [255, 69, 0], [230, 230, 250]], dtype=np.uint8),
    10: np.array([[20, 20, 20], [0, 191, 255], [57, 255, 20], [255, 215, 0], [70, 130, 180], [220, 20, 60]], dtype=np.uint8)
}

# Define rule transition functions
def rule_1(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    
    new_arr[is_3] = 3
    
    decay_2 = is_2 & ((left == 3) | (right == 3))
    new_arr[decay_2] = 3
    new_arr[is_2 & ~decay_2] = 2
    
    new_arr[is_1] = 2
    
    cond_1 = ((left == 1) & (right == 4)) | ((left == 4) & (right == 1))
    new_arr[is_0 & cond_1] = 1
    
    cond_4 = ((left == 4) | (right == 4)) & ~cond_1
    new_arr[is_0 & cond_4] = 4
    
    return new_arr

def rule_2(arr):
    def get_count(k):
        is_k = (arr == k).astype(np.int32)
        return np.roll(is_k, 1) + is_k + np.roll(is_k, -1)
    
    N1 = get_count(1)
    N2 = get_count(2)
    N3 = get_count(3)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    
    new_arr[is_4] = 4
    new_arr[is_3] = 2
    
    cond_2_4 = is_2 & (N3 >= 2)
    cond_2_2 = is_2 & (N3 == 1)
    new_arr[cond_2_4] = 4
    new_arr[cond_2_2] = 2
    
    cond_1_3 = is_1 & (N2 >= 1)
    new_arr[cond_1_3] = 3
    new_arr[is_1 & ~cond_1_3] = 1
    
    cond_0_2 = is_0 & (N2 >= 1) & (N1 >= 1)
    cond_0_1 = is_0 & ~cond_0_2 & (N1 >= 2)
    new_arr[cond_0_2] = 2
    new_arr[cond_0_1] = 1
    
    return new_arr

def rule_3(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    
    new_arr[is_2 | is_3 | is_4] = 5
    
    cond_1_2 = is_1 & (left == 2)
    cond_1_3 = is_1 & ~cond_1_2 & (right == 3)
    new_arr[cond_1_2] = 2
    new_arr[cond_1_3] = 3
    new_arr[is_1 & ~cond_1_2 & ~cond_1_3] = 5
    
    cond_0_4 = is_0 & (left == 2) & (right == 3)
    cond_0_2 = is_0 & ~cond_0_4 & (left == 2)
    cond_0_3 = is_0 & ~cond_0_4 & ~cond_0_2 & (right == 3)
    cond_0_1 = is_0 & ~cond_0_4 & ~cond_0_2 & ~cond_0_3 & ((left == 4) | (right == 4))
    
    new_arr[cond_0_4] = 4
    new_arr[cond_0_2] = 2
    new_arr[cond_0_3] = 3
    new_arr[cond_0_1] = 1
    
    return new_arr

def rule_4(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    def get_count_excl(k):
        return (left == k).astype(np.int32) + (right == k).astype(np.int32)
        
    N2 = get_count_excl(2)
    N3 = get_count_excl(3)
    N4 = get_count_excl(4)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    
    new_arr[is_0 & (N4 >= 1)] = 2
    
    cond_1_4 = is_1 & (N3 >= 1)
    new_arr[cond_1_4] = 4
    new_arr[is_1 & ~cond_1_4] = 1
    
    cond_2_3 = is_2 & (N4 >= 1)
    new_arr[cond_2_3] = 3
    new_arr[is_2 & ~cond_2_3] = 2
    
    cond_3_4 = is_3 & (N4 >= 1)
    new_arr[cond_3_4] = 4
    
    cond_4_1 = is_4 & (N2 + N3 == 0)
    new_arr[cond_4_1] = 1
    new_arr[is_4 & ~cond_4_1] = 4
    
    return new_arr

def rule_5(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    
    cond_3_3 = is_3 & ((left == 4) | (right == 4))
    new_arr[cond_3_3] = 3
    new_arr[is_3 & ~cond_3_3] = 4
    
    new_arr[is_2 & (left == 1)] = 4
    new_arr[is_1 & (right == 2)] = 4
    
    cond_0_3 = is_0 & (left == 1) & (right == 2)
    cond_0_1 = is_0 & ~cond_0_3 & (left == 4) & (right == 4)
    cond_0_4 = is_0 & ~cond_0_3 & ~cond_0_1 & (left == 4)
    
    new_arr[cond_0_3] = 3
    new_arr[cond_0_1] = 1
    new_arr[cond_0_4] = 4
    
    return new_arr

def rule_6(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    is_5 = (arr == 5)
    
    new_arr[is_3] = 3
    new_arr[is_5] = 3
    
    new_arr[is_4 & (left == 2)] = 1
    
    cond_2_1 = is_2 & (right == 4)
    cond_2_5 = is_2 & ~cond_2_1 & (left == 5)
    new_arr[cond_2_1] = 1
    new_arr[cond_2_5] = 5
    new_arr[is_2 & ~cond_2_1 & ~cond_2_5] = 2
    
    new_arr[is_1 & (right == 2)] = 5
    
    cond_0_1 = is_0 & (left == 1)
    cond_0_4_a = is_0 & ~cond_0_1 & (right == 4)
    cond_0_4_b = is_0 & ~cond_0_1 & ~cond_0_4_a & (right == 3)
    
    new_arr[cond_0_1] = 1
    new_arr[cond_0_4_a | cond_0_4_b] = 4
    
    return new_arr

def rule_7(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    def get_count(k):
        is_k = (arr == k).astype(np.int32)
        return np.roll(is_k, 1) + is_k + np.roll(is_k, -1)
        
    N1 = get_count(1)
    N2 = get_count(2)
    N4 = get_count(4)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    
    new_arr[is_3] = 3
    new_arr[is_4] = 2
    
    cond_2_4 = is_2 & ((left == 4) | (right == 4))
    cond_2_3 = is_2 & ~cond_2_4 & (N1 == 0)
    new_arr[cond_2_4] = 4
    new_arr[cond_2_3] = 3
    new_arr[is_2 & ~cond_2_4 & ~cond_2_3] = 2
    
    cond_1_2 = is_1 & ((N2 >= 1) | (N4 >= 1))
    new_arr[cond_1_2] = 2
    new_arr[is_1 & ~cond_1_2] = 1
    
    new_arr[is_0 & (N4 >= 2)] = 1
    
    return new_arr

def rule_8(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_3 = (arr == 3)
    
    cond_3_4 = is_3 & ((left == 1) | (right == 1))
    new_arr[cond_3_4] = 4
    new_arr[is_3 & ~cond_3_4] = 3
    
    cond_2_4 = is_2 & ((left == 3) | (right == 3))
    new_arr[cond_2_4] = 4
    new_arr[is_2 & ~cond_2_4] = 2
    
    cond_1_4 = is_1 & ((left == 2) | (right == 2))
    new_arr[cond_1_4] = 4
    new_arr[is_1 & ~cond_1_4] = 1
    
    cond_0_3_pair = is_0 & (((left == 1) & (right == 2)) | ((left == 2) & (right == 1)))
    cond_0_1_pair = is_0 & ~cond_0_3_pair & (((left == 2) & (right == 3)) | ((left == 3) & (right == 2)))
    cond_0_2_pair = is_0 & ~cond_0_3_pair & ~cond_0_1_pair & (((left == 3) & (right == 1)) | ((left == 1) & (right == 3)))
    
    cond_0_1_single = is_0 & ~cond_0_3_pair & ~cond_0_1_pair & ~cond_0_2_pair & ((left == 1) | (right == 1))
    cond_0_2_single = is_0 & ~cond_0_3_pair & ~cond_0_1_pair & ~cond_0_2_pair & ~cond_0_1_single & ((left == 2) | (right == 2))
    cond_0_3_single = is_0 & ~cond_0_3_pair & ~cond_0_1_pair & ~cond_0_2_pair & ~cond_0_1_single & ~cond_0_2_single & ((left == 3) | (right == 3))
    
    new_arr[cond_0_3_pair] = 3
    new_arr[cond_0_1_pair] = 1
    new_arr[cond_0_2_pair] = 2
    new_arr[cond_0_1_single] = 1
    new_arr[cond_0_2_single] = 2
    new_arr[cond_0_3_single] = 3
    
    return new_arr

def rule_9(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_1 = (arr == 1)
    is_2 = (arr == 2)
    is_4 = (arr == 4)
    
    new_arr[is_4] = 1
    
    cond_2_1 = is_2 & (((left == 1) & (right != 1)) | ((right == 1) & (left != 1)))
    cond_2_0 = is_2 & ~cond_2_1 & ((left == 3) | (right == 3))
    cond_2_2 = is_2 & ~cond_2_1 & ~cond_2_0
    
    new_arr[cond_2_1] = 1
    new_arr[cond_2_2] = 2
    
    cond_1_0 = is_1 & ((left == 3) | (right == 3))
    new_arr[is_1 & ~cond_1_0] = 2
    
    cond_0_1 = is_0 & (((left == 1) & (right == 2)) | ((left == 2) & (right == 1)))
    cond_0_4 = is_0 & ~cond_0_1 & ((left == 3) | (right == 3))
    
    new_arr[cond_0_1] = 1
    new_arr[cond_0_4] = 4
    
    return new_arr

def rule_10(arr):
    left_1 = np.roll(arr, 1)
    left_2 = np.roll(arr, 2)
    right_1 = np.roll(arr, -1)
    right_2 = np.roll(arr, -2)
    
    new_arr = np.zeros_like(arr)
    is_0 = (arr == 0)
    is_3 = (arr == 3)
    is_4 = (arr == 4)
    is_5 = (arr == 5)
    
    new_arr[is_5] = 5
    
    cond_4_5 = is_4 & (left_1 == 4) & (right_1 == 4)
    new_arr[cond_4_5] = 5
    new_arr[is_4 & ~cond_4_5] = 4
    
    new_arr[is_3] = 4
    
    G = (left_1 == 2) | (left_2 == 2)
    C = (right_1 == 1) | (right_2 == 1)
    
    cond_0_3 = is_0 & G & C
    cond_0_2 = is_0 & ~cond_0_3 & G
    cond_0_1 = is_0 & ~cond_0_3 & ~cond_0_2 & C
    
    new_arr[cond_0_3] = 3
    new_arr[cond_0_2] = 2
    new_arr[cond_0_1] = 1
    
    return new_arr

RULES = {
    1: (rule_1, 5),
    2: (rule_2, 5),
    3: (rule_3, 6),
    4: (rule_4, 5),
    5: (rule_5, 5),
    6: (rule_6, 6),
    7: (rule_7, 5),
    8: (rule_8, 5),
    9: (rule_9, 5),
    10: (rule_10, 6)
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        if rule_num == 1:
            grid[0, W // 2] = 1
            for k in range(1, W // 4):
                grid[0, W // 2 - 2 * k] = 4
                grid[0, W // 2 + 2 * k] = 4
        elif rule_num == 2:
            grid[0, :] = 1
            grid[0, W // 2] = 3
        elif rule_num == 3:
            grid[0, W // 2 - 10] = 2
            grid[0, W // 2 + 10] = 3
        elif rule_num == 4:
            grid[0, :] = 2
            grid[0, W // 2] = 4
        elif rule_num == 5:
            grid[0, W // 2] = 3
            grid[0, W // 2 - 10] = 4
        elif rule_num == 6:
            grid[0, W // 2 - 200] = 1
            grid[0, W // 2 - 100] = 2
            grid[0, W // 2] = 2
            grid[0, W // 2 + 100] = 2
        elif rule_num == 7:
            grid[0, :] = 1
            grid[0, W // 2] = 2
            grid[0, W // 2 - 1] = 4
            grid[0, W // 2 + 1] = 4
        elif rule_num == 8:
            grid[0, W // 2 - 20] = 1
            grid[0, W // 2] = 2
            grid[0, W // 2 + 20] = 3
        elif rule_num == 9:
            grid[0, W // 2] = 3
        elif rule_num == 10:
            grid[0, W // 2 - 100] = 2
            grid[0, W // 2 + 100] = 1
    elif init_type == "random":
        grid[0] = np.random.randint(0, num_states, size=W, dtype=np.int32)
        
    for t in range(H - 1):
        grid[t + 1] = rule_func(grid[t])
        
    palette = PALETTES[rule_num]
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
    print("Simulation complete successfully.")

if __name__ == "__main__":
    main()
