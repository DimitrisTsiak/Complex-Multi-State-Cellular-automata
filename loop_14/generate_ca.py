import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define Vibrant Palettes for each rule
PALETTES = {
    1: np.array([
        [15, 15, 25],      # 0: Vacuum
        [30, 144, 255],    # 1: Boson B1 (Light blue)
        [0, 255, 255],     # 2: Boson B2 (Cyan)
        [255, 20, 147],    # 3: Fermion F1 (Pink/magenta)
        [147, 112, 219],   # 4: Fermion F2 (Purple)
        [255, 215, 0]      # 5: Bound State S (Gold)
    ], dtype=np.uint8),

    2: np.array([
        [10, 5, 20],       # 0: Bulk
        [0, 255, 127],     # 1: Left open endpoint (Neon green)
        [50, 205, 50],     # 2: Right open endpoint (Bright green)
        [255, 127, 80],    # 3: Open string body (Coral)
        [138, 43, 226],    # 4: Left closed mode (Violet)
        [75, 0, 130],      # 5: Right closed mode (Indigo)
        [255, 20, 147],    # 6: Knot (Hot pink)
        [255, 191, 0]      # 7: D-brane (Amber)
    ], dtype=np.uint8),

    3: np.array([
        [10, 15, 25],      # 0
        [75, 0, 130],      # 1
        [128, 0, 128],     # 2
        [0, 0, 139],       # 3
        [0, 0, 255],       # 4
        [30, 144, 255],    # 5
        [0, 128, 128],     # 6
        [0, 128, 0],       # 7
        [154, 205, 50],    # 8
        [255, 255, 0],     # 9
        [255, 165, 0],     # 10
        [255, 0, 0]        # 11
    ], dtype=np.uint8),

    4: np.array([
        [5, 5, 5],         # 0
        [0, 191, 255],     # 1
        [0, 255, 255],     # 2
        [144, 238, 144],   # 3
        [255, 215, 0],     # 4
        [255, 140, 0],     # 5
        [255, 69, 0],      # 6
        [255, 99, 71]      # 7
    ], dtype=np.uint8),

    5: np.array([
        [70, 30, 30],      # 0: Unstable vacuum (Pale red)
        [255, 69, 0],      # 1: Decaying tachyon (Orange-red)
        [0, 100, 80],      # 2: Stable vacuum (Forest green)
        [0, 191, 255],     # 3: Open string excitation (Sky blue)
        [255, 215, 0]      # 4: Kink/defect (Gold)
    ], dtype=np.uint8),

    6: np.array([
        [10, 10, 30],      # 0
        [65, 105, 225],    # 1
        [72, 209, 204],    # 2
        [46, 139, 87],     # 3
        [255, 20, 147],    # 4
        [153, 50, 204],    # 5
        [255, 99, 71],     # 6
        [240, 240, 240]    # 7
    ], dtype=np.uint8),

    7: np.array([
        [15, 15, 15],      # 0
        [32, 178, 170],    # 1
        [0, 139, 139],     # 2
        [144, 238, 144],   # 3
        [50, 205, 50],     # 4
        [34, 139, 34],     # 5
        [255, 165, 0],     # 6
        [255, 127, 80],    # 7
        [255, 99, 71],     # 8
        [255, 215, 0]      # 9
    ], dtype=np.uint8),

    8: np.array([
        [10, 10, 20],      # 0: Quantum foam
        [255, 69, 0],      # 1: Clockwise boundary (Orange)
        [255, 223, 0],     # 2: Counter-clockwise (Yellow)
        [0, 255, 255],     # 3: String connection (Cyan)
        [147, 112, 219],   # 4: Junction (Royal purple)
        [255, 255, 255]    # 5: Singularity (White)
    ], dtype=np.uint8),

    9: np.array([
        [10, 10, 30],      # 0: Bulk spacetime
        [220, 20, 60],     # 1: D-brane A (Red)
        [30, 144, 255],    # 2: D-brane B (Blue)
        [0, 255, 0],       # 3: Endpoint (Neon green)
        [144, 238, 144],   # 4: Body (Soft green)
        [255, 255, 200]    # 5: Collision plasma (White-hot)
    ], dtype=np.uint8),

    10: np.array([
        [20, 20, 20],      # 0: Flat vacuum
        [0, 255, 0],       # 1: Particle flavor 1 (Green)
        [173, 255, 47],    # 2: Particle flavor 2 (Lime-yellow)
        [0, 250, 154],     # 3: Particle flavor 3 (Spring green)
        [255, 140, 0],     # 4: Horizon 1 (Orange)
        [255, 0, 255],     # 5: Horizon 2 (Magenta)
        [220, 20, 60],     # 6: Horizon 3 (Crimson)
        [200, 220, 255]    # 7: Singularity core (Blue-white)
    ], dtype=np.uint8)
}

# 3. Transition Rules
def rule_1(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    left_b = (left == 1) | (left == 2)
    right_b = (right == 1) | (right == 2)
    nb = left_b.astype(np.int32) + right_b.astype(np.int32)
    
    left_f = (left == 3) | (left == 4)
    right_f = (right == 3) | (right == 4)
    nf = left_f.astype(np.int32) + right_f.astype(np.int32)
    
    new_arr = np.zeros_like(arr)
    
    # State 0 updates
    cond0 = (arr == 0)
    val0 = np.zeros_like(arr)
    cond0_5 = (nb >= 1) & (nf >= 1)
    cond0_1 = (nb >= 2) & ~cond0_5
    cond0_3 = (nf >= 2) & ~cond0_5 & ~cond0_1
    val0[cond0_5] = 5
    val0[cond0_1] = 1
    val0[cond0_3] = 3
    
    # State 1, 2 updates (Boson)
    is_b = (arr == 1) | (arr == 2)
    val_b = arr.copy()
    cond_susy_b = (nf > nb)
    val_b[cond_susy_b] = arr[cond_susy_b] + 2
    cond_excite_b = (~cond_susy_b) & (arr == 1) & (left == 1) & (right == 1)
    val_b[cond_excite_b] = 2
    cond_decay_b = (~cond_susy_b) & (~cond_excite_b) & (arr == 2)
    val_b[cond_decay_b] = 0
    
    # State 3, 4 updates (Fermion)
    is_f = (arr == 3) | (arr == 4)
    val_f = arr.copy()
    cond_susy_f = (nb > nf)
    val_f[cond_susy_f] = arr[cond_susy_f] - 2
    cond_pauli = (~cond_susy_f) & ((left == arr) | (right == arr))
    val_f[cond_pauli] = 0
    
    # State 5 updates (Bound State)
    mask5 = (arr == 5)
    val5 = np.where(left % 2 == 0, 1, 3)
    
    new_arr[cond0] = val0[cond0]
    new_arr[is_b] = val_b[is_b]
    new_arr[is_f] = val_f[is_f]
    new_arr[mask5] = val5[mask5]
    
    return new_arr

def rule_2(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    cond_7 = (arr == 7)
    cond_6 = (arr == 6)
    cond_from_6_right = (right == 6) & ~cond_7 & ~cond_6
    cond_from_6_left = (left == 6) & ~cond_7 & ~cond_6 & ~cond_from_6_right
    
    # State 0 updates
    cond_0 = (arr == 0) & ~cond_from_6_right & ~cond_from_6_left
    collision = (left == 5) & (right == 4)
    prop_right_closed = (left == 5) & ~collision
    prop_left_closed = (right == 4) & ~collision
    open_body_prop = ((left == 3) & (right == 2)) | ((right == 3) & (left == 1))
    
    val_0 = np.zeros_like(arr)
    val_0 = np.where(collision, 6, val_0)
    val_0 = np.where(prop_right_closed, 5, val_0)
    val_0 = np.where(prop_left_closed, 4, val_0)
    val_0 = np.where(open_body_prop & ~collision & ~prop_right_closed & ~prop_left_closed, 3, val_0)
    
    # State 1 updates
    cond_1 = (arr == 1) & ~cond_from_6_right & ~cond_from_6_left
    val_1 = np.where(left == 7, 2, np.where(right == 3, 3, 0))
    
    # State 2 updates
    cond_2 = (arr == 2) & ~cond_from_6_right & ~cond_from_6_left
    val_2 = np.where(right == 7, 1, np.where(left == 3, 3, 0))
    
    # State 3 updates
    cond_3 = (arr == 3) & ~cond_from_6_right & ~cond_from_6_left
    val_3 = np.where(((left == 1) | (left == 3)) & ((right == 2) | (right == 3)), 3, 0)
    
    # State 4 updates
    cond_4 = (arr == 4) & ~cond_from_6_right & ~cond_from_6_left
    val_4 = np.where((right == 4) | (right == 0), right, 0)
    
    # State 5 updates
    cond_5 = (arr == 5) & ~cond_from_6_right & ~cond_from_6_left
    val_5 = np.where((left == 5) | (left == 0), left, 0)
    
    new_arr = np.zeros_like(arr)
    new_arr[cond_7] = 7
    new_arr[cond_6] = 3
    new_arr[cond_from_6_right] = 1
    new_arr[cond_from_6_left] = 2
    new_arr[cond_0] = val_0[cond_0]
    new_arr[cond_1] = val_1[cond_1]
    new_arr[cond_2] = val_2[cond_2]
    new_arr[cond_3] = val_3[cond_3]
    new_arr[cond_4] = val_4[cond_4]
    new_arr[cond_5] = val_5[cond_5]
    
    return new_arr

def rule_3(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    e_L, i_L = left // 3, left % 3
    e_x, i_x = arr // 3, arr % 3
    e_R, i_R = right // 3, right % 3
    
    i_next = (i_L + i_x + i_R) % 3
    
    e_next_0 = (e_L + e_R) % 4
    
    e_next_1 = np.zeros_like(arr)
    cond_ex_not_0 = (e_x != 0)
    e_next_1[cond_ex_not_0] = (e_x[cond_ex_not_0] + 1) % 4
    cond_ex_0_trigger = (e_x == 0) & ((e_L == 1) | (e_R == 1))
    e_next_1[cond_ex_0_trigger] = 1
    
    e_next_2 = (e_x**2 + e_L * e_R) % 4
    
    e_next = np.zeros_like(arr)
    e_next = np.where(i_next == 0, e_next_0, e_next)
    e_next = np.where(i_next == 1, e_next_1, e_next)
    e_next = np.where(i_next == 2, e_next_2, e_next)
    
    return 3 * e_next + i_next

def rule_4(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    p_L, w_L = left // 2, left % 2
    p_x, w_x = arr // 2, arr % 2
    p_R, w_R = right // 2, right % 2
    
    W_local = w_L + w_x + w_R
    
    p_small = (w_L + w_R) % 4
    w_small = ((p_L + p_x + p_R) % 2).astype(np.int32)
    
    p_large = (p_L + p_x + p_R) % 4
    w_large = (w_L + w_R) % 2
    
    p_next = np.where(W_local >= 2, p_small, p_large)
    w_next = np.where(W_local >= 2, w_small, w_large)
    
    return 2 * p_next + w_next

def rule_5(arr):
    left2 = np.roll(arr, 2)
    left1 = np.roll(arr, 1)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)
    
    is_decay_active = (arr == 1) | (arr == 2) | (arr == 4)
    left1_decay = (left1 == 1) | (left1 == 2) | (left1 == 4)
    left2_decay = (left2 == 1) | (left2 == 2) | (left2 == 4)
    right1_decay = (right1 == 1) | (right1 == 2) | (right1 == 4)
    right2_decay = (right2 == 1) | (right2 == 2) | (right2 == 4)
    
    decay_sum = (is_decay_active.astype(np.int32) + 
                 left1_decay.astype(np.int32) + 
                 left2_decay.astype(np.int32) + 
                 right1_decay.astype(np.int32) + 
                 right2_decay.astype(np.int32))
    
    val_0 = np.where(decay_sum >= 1, 1, 0)
    
    val_3 = np.where((left1 == 2) | (right1 == 2), 2, 
                     np.where((left1 == 3) & (right1 != 3), 3, 0))
    
    val_4 = np.where(left1 == 2, 2, 4)
    
    cond_become_4 = (left1 == 4) & (left2 == 2) & (arr == 0)
    
    new_arr = np.zeros_like(arr)
    new_arr = np.where(arr == 0, val_0, new_arr)
    new_arr = np.where(arr == 1, 2, new_arr)
    new_arr = np.where(arr == 2, 2, new_arr)
    new_arr = np.where(arr == 3, val_3, new_arr)
    new_arr = np.where(arr == 4, val_4, new_arr)
    new_arr = np.where(cond_become_4, 4, new_arr)
    
    return new_arr

def rule_6(arr):
    left2 = np.roll(arr, 2)
    left1 = np.roll(arr, 1)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)
    
    C = (arr >= 4).astype(np.int32)
    C_L = (left1 >= 4).astype(np.int32)
    C_R = (right1 >= 4).astype(np.int32)
    E = C_L + C + C_R
    
    u_L2 = left2 % 4
    u_L1 = left1 % 4
    u_R1 = right1 % 4
    u_R2 = right2 % 4
    val_weak = (u_L2 + u_L1 + u_R1 + u_R2) % 4
    
    v_x = arr % 4
    v_L = left1 % 4
    v_R = right1 % 4
    val_strong = 4 + (v_x**2 + v_L * v_R) % 4
    
    return np.where(E <= 1, val_weak, val_strong)

def rule_7(arr):
    left2 = np.roll(arr, 2)
    left1 = np.roll(arr, 1)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)
    
    val_boundary = (3 * arr + left2 * right2) % 10
    val_bulk = (left1 + right1 + left2 + right2) % 10
    
    indices = np.arange(len(arr))
    is_even = (indices % 2 == 0)
    
    return np.where(is_even, val_boundary, val_bulk)

def rule_8(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    in_R = (left == 1) | (left == 4)
    in_L = (right == 2) | (right == 4)
    
    new_arr = np.zeros_like(arr)
    
    mask0 = (arr == 0)
    mask1 = (arr == 1)
    mask2 = (arr == 2)
    mask3 = (arr == 3)
    mask4 = (arr == 4)
    mask5 = (arr == 5)
    
    val0 = np.zeros_like(arr)
    val0 = np.where(in_R & in_L, 4, val0)
    val0 = np.where(in_R & ~in_L, 1, val0)
    val0 = np.where(~in_R & in_L, 2, val0)
    
    val1 = np.where(right == 2, 3, np.where(in_R, 1, 0))
    val2 = np.where(left == 1, 3, np.where(in_L, 2, 0))
    val3 = np.where((left == 4) & (right == 4), 5, 3)
    
    new_arr[mask0] = val0[mask0]
    new_arr[mask1] = val1[mask1]
    new_arr[mask2] = val2[mask2]
    new_arr[mask3] = val3[mask3]
    # States 4 and 5 become 0
    
    return new_arr

def rule_9(arr):
    left2 = np.roll(arr, 2)
    left1 = np.roll(arr, 1)
    right1 = np.roll(arr, -1)
    right2 = np.roll(arr, -2)
    
    cond_5 = ((arr == 1) & (right1 == 2)) | ((arr == 2) & (left1 == 1))
    cond_1 = (~cond_5) & ((left1 == 1) | (left2 == 5))
    cond_2 = (~cond_5) & ((right1 == 2) | (right2 == 5))
    
    cond_3 = (~cond_5) & (~cond_1) & (~cond_2) & (
        (left1 == 5) | (right1 == 5) | 
        ((arr == 1) & (left1 == 3)) | 
        ((arr == 2) & (right1 == 3))
    )
    
    cond_4 = (~cond_5) & (~cond_1) & (~cond_2) & (~cond_3) & (
        (arr == 5) | 
        ((arr == 4) & ((left1 == 3) | (left1 == 4)) & ((right1 == 3) | (right1 == 4))) | 
        ((arr == 3) & ((right1 == 1) | (left1 == 2)))
    )
    
    new_arr = np.zeros_like(arr)
    new_arr[cond_5] = 5
    new_arr[cond_1] = 1
    new_arr[cond_2] = 2
    new_arr[cond_3] = 3
    new_arr[cond_4] = 4
    
    return new_arr

def rule_10(arr):
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    def get_h(y):
        return np.where(y >= 4, y - 4, y % 3)
        
    h_x = get_h(arr)
    h_L = get_h(left)
    h_R = get_h(right)
    
    h_new = (h_x + h_L * h_R + 1) % 3
    
    new_arr = np.zeros_like(arr)
    
    mask7 = (arr == 7)
    new_arr[mask7] = 7
    
    is_hor = (arr >= 4) & (arr <= 6)
    val_hor = np.where((left == 0) & (h_new == 0), 0, 4 + h_new)
    new_arr[is_hor] = val_hor[is_hor]
    
    is_part = (arr >= 1) & (arr <= 3)
    right_is_hor = (right >= 4) & (right <= 6)
    val_part = np.where(right_is_hor, 4 + (arr + right) % 3, 
                        np.where((left >= 1) & (left <= 3), left, 0))
    new_arr[is_part] = val_part[is_part]
    
    is_vac = (arr == 0)
    hawking_emit = (right == 6)
    left_is_part = (left >= 1) & (left <= 3)
    val_vac = np.where(left_is_part, left, np.where(hawking_emit, 1, 0))
    new_arr[is_vac] = val_vac[is_vac]
    
    return new_arr

RULES = {
    1: (rule_1, 6),
    2: (rule_2, 8),
    3: (rule_3, 12),
    4: (rule_4, 8),
    5: (rule_5, 5),
    6: (rule_6, 8),
    7: (rule_7, 10),
    8: (rule_8, 6),
    9: (rule_9, 6),
    10: (rule_10, 8)
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        if rule_num == 1:
            grid[0, W // 2 - 2] = 1
            grid[0, W // 2 - 1] = 3
            grid[0, W // 2] = 5
            grid[0, W // 2 + 1] = 3
            grid[0, W // 2 + 2] = 1
        elif rule_num == 2:
            grid[0, 10] = 7
            grid[0, W - 10] = 7
            grid[0, W // 2 - 5] = 5
            grid[0, W // 2 + 5] = 4
        elif rule_num == 3:
            grid[0, W // 2 - 10] = 5
            grid[0, W // 2] = 11
            grid[0, W // 2 + 10] = 8
        elif rule_num == 4:
            grid[0, W // 2 - 5] = 3
            grid[0, W // 2] = 7
            grid[0, W // 2 + 5] = 5
        elif rule_num == 5:
            grid[0, W // 2] = 1
            grid[0, W // 2 - 100] = 2
            grid[0, W // 2 + 100] = 2
        elif rule_num == 6:
            grid[0, W // 2 - 10 : W // 2 + 10] = 5
        elif rule_num == 7:
            grid[0, W // 2] = 9
            grid[0, W // 2 - 20] = 7
            grid[0, W // 2 + 20] = 8
        elif rule_num == 8:
            grid[0, W // 2] = 4
            grid[0, W // 4] = 4
            grid[0, 3 * W // 4] = 4
        elif rule_num == 9:
            grid[0, W // 4] = 1
            grid[0, 3 * W // 4] = 2
        elif rule_num == 10:
            grid[0, W // 2 : W - 50] = np.random.randint(4, 7, size=(W - 50 - W // 2))
            grid[0, W - 50] = 7
            grid[0, W // 4] = 1
            grid[0, W // 4 - 20] = 2
            grid[0, W // 4 - 40] = 3
        else:
            grid[0, W // 2] = num_states - 1
            
    elif init_type == "random":
        if rule_num == 5:
            # Tachyon Condensation needs a mostly vacuum grid to see bubble growth
            grid[0] = np.where(np.random.rand(W) < 0.98, 0, np.random.randint(1, num_states, size=W))
        elif rule_num == 10:
            # Fuzzball horizon is more interesting if horizon block is initialized
            # but we can also do pure random. Let's make pure random, but keep some 7s at boundaries
            grid[0] = np.random.randint(0, num_states, size=W, dtype=np.int32)
        else:
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
    # Set random seed for reproducibility
    np.random.seed(42)
    
    for rule_num in sorted(RULES.keys()):
        for init_type in ["single_seed", "random"]:
            simulate_and_save(rule_num, init_type)
    print("Simulation complete.")

if __name__ == "__main__":
    main()
