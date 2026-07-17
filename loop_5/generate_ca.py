import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define the 10 Rule Functions (with periodic boundary wrapping using np.roll)

def rule_1(arr):
    # States: 6.
    # 0: Quiescent Weak (Q_W), 1: Excited Weak (E_W), 2: Refractory Weak (R_W)
    # 3: Quiescent Potentiated (Q_P), 4: Excited Potentiated (E_P), 5: Refractory Potentiated (R_P)
    firing = (arr == 1) | (arr == 4)
    F = np.roll(firing, 1).astype(int) + np.roll(firing, -1).astype(int)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    new_arr[m0] = np.where(F[m0] == 2, 1, 0)
    # S_t(x) == 1
    m1 = (arr == 1)
    new_arr[m1] = np.where(F[m1] >= 1, 4, 2)
    # S_t(x) == 2
    new_arr[arr == 2] = 0
    # S_t(x) == 3
    m3 = (arr == 3)
    new_arr[m3] = np.where(F[m3] >= 1, 4, 0)
    # S_t(x) == 4
    new_arr[arr == 4] = 5
    # S_t(x) == 5
    new_arr[arr == 5] = 3
    
    return new_arr

def rule_2(arr):
    # States: 8.
    # Activity: a = S % 2 (0: Quiet, 1: Firing)
    # Weight: w = S // 2 (0 to 3)
    a_curr = arr % 2
    w_curr = arr // 2
    
    a_left = np.roll(a_curr, 1)
    a_right = np.roll(a_curr, -1)
    
    I = w_curr * (a_left + a_right)
    a_next = np.where((a_curr == 0) & (I >= 2), 1, 0)
    
    a_next_left = np.roll(a_next, 1)
    a_next_right = np.roll(a_next, -1)
    
    cond_ltp = (a_next == 1) & (a_left + a_right >= 1)
    cond_ltd = (a_curr == 1) & (a_next_left + a_next_right >= 1)
    
    w_next = np.copy(w_curr)
    w_next[cond_ltp] = np.minimum(3, w_curr[cond_ltp] + 1)
    w_next[cond_ltd] = np.maximum(0, w_curr[cond_ltd] - 1)
    
    return 2 * w_next + a_next

def rule_3(arr):
    # States: 4. 0: Quiescent, 1: Firing, 2: Refractory, 3: Hyperpolarized
    # Excitatory (E): x % 3 != 0
    # Inhibitory (I): x % 3 == 0
    n = len(arr)
    idx = np.arange(n)
    is_E = (idx % 3 != 0)
    is_I = (idx % 3 == 0)
    
    is_firing = (arr == 1)
    is_firing_E = is_firing & is_E
    is_firing_I = is_firing & is_I
    
    # Neighborhood sum (r=2 excluding self)
    def sum_r2(b):
        return (np.roll(b, 2) + np.roll(b, 1) + np.roll(b, -1) + np.roll(b, -2)).astype(int)
        
    E_count = sum_r2(is_firing_E)
    I_count = sum_r2(is_firing_I)
    A = E_count - 2 * I_count
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    new_arr[m0] = np.where(A[m0] >= 1, 1, 0)
    # S_t(x) == 1
    m1 = (arr == 1)
    new_arr[m1] = np.where(I_count[m1] >= 1, 3, 2)
    # S_t(x) == 2
    new_arr[arr == 2] = 0
    # S_t(x) == 3
    m3 = (arr == 3)
    new_arr[m3] = np.where(A[m3] >= 2, 1, 0)
    
    return new_arr

def rule_4(arr):
    # States: 8.
    # Neural Activity: n = S % 4 (0: Quiescent, 1: Firing, 2: Refractory P1, 3: Refractory P2)
    # Glial Modulation: g = S // 4 (0: Normal, 1: Potentiated)
    n_curr = arr % 4
    g_curr = arr // 4
    
    firing = (n_curr == 1)
    F = np.roll(firing, 1).astype(int) + np.roll(firing, -1).astype(int)
    
    # Neural state transition
    n_next = np.copy(n_curr)
    m0 = (n_curr == 0)
    cond_fire = ((g_curr == 0) & (F == 2)) | ((g_curr == 1) & (F >= 1))
    n_next[m0] = np.where(cond_fire[m0], 1, 0)
    
    n_next[n_curr == 1] = 2
    n_next[n_curr == 2] = 3
    n_next[n_curr == 3] = 0
    
    # Glial state transition
    g_next = np.copy(g_curr)
    cond_release = (n_curr == 1) & (F >= 1)
    cond_clear = (n_curr == 0) & (F == 0)
    
    g_next[cond_release] = 1
    g_next[cond_clear] = 0
    
    return 4 * g_next + n_next

def rule_5(arr):
    # States: 6. 0: Quiescent, 1: Firing, 2: Refractory, 3: Quiescent Habituated, 4: Firing Habituated, 5: Refractory Habituated
    firing = (arr == 1) | (arr == 4)
    F = (
        np.roll(firing, 2) +
        np.roll(firing, 1) +
        np.roll(firing, -1) +
        np.roll(firing, -2)
    ).astype(int)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    new_arr[m0] = np.where(F[m0] >= 1, 1, 0)
    # S_t(x) == 1
    new_arr[arr == 1] = 2
    # S_t(x) == 2
    new_arr[arr == 2] = 3
    # S_t(x) == 3
    m3 = (arr == 3)
    new_arr[m3] = np.where(F[m3] >= 3, 4, 0)
    # S_t(x) == 4
    new_arr[arr == 4] = 5
    # S_t(x) == 5
    new_arr[arr == 5] = 3
    
    return new_arr

def rule_6(arr):
    # States: 5. 0: Depleted Q, 1: Partially Charged Q, 2: Fully Charged Q, 3: Firing, 4: Refractory
    firing = (arr == 3)
    F = np.roll(firing, 1).astype(int) + np.roll(firing, -1).astype(int)
    
    new_arr = np.copy(arr)
    # S_t(x) == 2
    m2 = (arr == 2)
    new_arr[m2] = np.where(F[m2] >= 1, 3, 2)
    # S_t(x) == 1
    m1 = (arr == 1)
    new_arr[m1] = np.where(F[m1] == 2, 3, 2)
    # S_t(x) == 0
    new_arr[arr == 0] = 1
    # S_t(x) == 3
    new_arr[arr == 3] = 4
    # S_t(x) == 4
    new_arr[arr == 4] = 0
    
    return new_arr

def rule_7(arr):
    # States: 7. 0: Quiescent, 1: Coincidence Hub, 2-5: Delay line, 6: Firing Terminal
    firing = (arr == 6)
    I = np.roll(firing, 2).astype(int) + np.roll(firing, 1).astype(int) + np.roll(firing, -1).astype(int)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    new_arr[m0] = np.where(I[m0] >= 2, 1, 0)
    # 1 <= S_t(x) <= 5
    m_delay = (arr >= 1) & (arr <= 5)
    new_arr[m_delay] = arr[m_delay] + 1
    # S_t(x) == 6
    new_arr[arr == 6] = 0
    
    return new_arr

def rule_8(arr):
    # States: 6. 0: Quiescent, 1: Normal Firing, 2: Normal Refractory, 3: Gas Emission, 4: Potentiated Firing, 5: Potentiated Refractory
    firing = (arr == 1) | (arr == 4)
    gas = (arr == 3)
    
    def sum_r2(b):
        return (np.roll(b, 2) + np.roll(b, 1) + np.roll(b, -1) + np.roll(b, -2)).astype(int)
        
    F = sum_r2(firing)
    G = sum_r2(gas)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    cond_pot = (G >= 1) & (F >= 1)
    cond_norm = (G == 0) & (F >= 2)
    new_arr[m0] = np.where(cond_pot[m0], 4, np.where(cond_norm[m0], 1, 0))
    # S_t(x) == 1
    new_arr[arr == 1] = 2
    # S_t(x) == 2
    new_arr[arr == 2] = 0
    # S_t(x) == 4
    new_arr[arr == 4] = 3
    # S_t(x) == 3
    new_arr[arr == 3] = 5
    # S_t(x) == 5
    new_arr[arr == 5] = 0
    
    return new_arr

def rule_9(arr):
    # States: 6. 0: Normal Q, 1: Sensitized Q, 2: Desensitized Q, 3: Firing, 4: Normal Refractory, 5: Deep Refractory
    firing = (arr == 3)
    
    def sum_r2(b):
        return (np.roll(b, 2) + np.roll(b, 1) + np.roll(b, -1) + np.roll(b, -2)).astype(int)
        
    F = sum_r2(firing)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    m0 = (arr == 0)
    new_arr[m0] = np.where(F[m0] >= 2, 3, np.where(F[m0] == 0, 1, 0))
    # S_t(x) == 1
    m1 = (arr == 1)
    new_arr[m1] = np.where(F[m1] >= 1, 3, 1)
    # S_t(x) == 2
    m2 = (arr == 2)
    new_arr[m2] = np.where(F[m2] >= 4, 3, np.where(F[m2] == 0, 0, 2))
    # S_t(x) == 3
    m3 = (arr == 3)
    new_arr[m3] = np.where(F[m3] >= 3, 5, 4)
    # S_t(x) == 4
    new_arr[arr == 4] = 0
    # S_t(x) == 5
    new_arr[arr == 5] = 2
    
    return new_arr

def rule_10(arr):
    # States: 7. 0: Exhausted Q, 1: Charged Q, 2: Hyper-Charged Q, 3: Firing from Charged, 4: Firing from Hyper-Charged, 5: Refractory Low, 6: Refractory High
    firing = (arr == 3) | (arr == 4)
    F = np.roll(firing, 1).astype(int) + np.roll(firing, -1).astype(int)
    
    new_arr = np.copy(arr)
    # S_t(x) == 0
    new_arr[arr == 0] = 1
    # S_t(x) == 1
    m1 = (arr == 1)
    new_arr[m1] = np.where(F[m1] >= 1, 3, 2)
    # S_t(x) == 2
    m2 = (arr == 2)
    new_arr[m2] = np.where(F[m2] >= 1, 4, 2)
    # S_t(x) == 3
    new_arr[arr == 3] = 5
    # S_t(x) == 4
    new_arr[arr == 4] = 6
    # S_t(x) == 5
    new_arr[arr == 5] = 0
    # S_t(x) == 6
    new_arr[arr == 6] = 1
    
    return new_arr


# 3. Hand-crafted vibrant color palettes representing neural dynamics
PALETTES = {
    1: [
        [15, 10, 25],      # 0: Quiescent Weak (Deep charcoal)
        [0, 102, 255],     # 1: Excited Weak (Electric blue)
        [70, 90, 120],     # 2: Refractory Weak (Muted blue-grey)
        [100, 70, 10],     # 3: Quiescent Potentiated (Dark gold)
        [255, 204, 0],     # 4: Excited Potentiated (Bright gold)
        [255, 102, 0],     # 5: Refractory Potentiated (Orange)
    ],
    2: [
        [10, 20, 15],      # 0: a=0, w=0 (Dark green-black)
        [200, 255, 220],   # 1: a=1, w=0 (Light mint)
        [10, 80, 80],      # 2: a=0, w=1 (Teal)
        [0, 230, 230],     # 3: a=1, w=1 (Bright cyan)
        [10, 30, 100],     # 4: a=0, w=2 (Dark blue)
        [50, 100, 255],    # 5: a=1, w=2 (Royal blue)
        [60, 10, 100],     # 6: a=0, w=3 (Dark violet)
        [255, 0, 200],     # 7: a=1, w=3 (Vibrant magenta)
    ],
    3: [
        [5, 10, 30],       # 0: Quiescent (Navy blue)
        [255, 0, 51],      # 1: Firing (Neon crimson)
        [128, 0, 192],     # 2: Refractory (Royal purple)
        [0, 80, 40],       # 3: Hyperpolarized (Forest green)
    ],
    4: [
        [10, 10, 12],      # 0: n=0, g=0 (Almost black)
        [173, 255, 47],    # 1: n=1, g=0 (Neon green)
        [46, 139, 87],     # 2: n=2, g=0 (Muted green)
        [47, 79, 79],      # 3: n=3, g=0 (Dark slate)
        [139, 69, 19],     # 4: n=0, g=1 (Copper/Orange)
        [255, 69, 0],      # 5: n=1, g=1 (Bright orange-red)
        [255, 20, 147],    # 6: n=2, g=1 (Hot pink)
        [148, 0, 211],     # 7: n=3, g=1 (Dark purple)
    ],
    5: [
        [10, 15, 30],      # 0: Quiescent (Dark blue-black)
        [0, 255, 255],     # 1: Firing (Vibrant cyan)
        [0, 139, 139],     # 2: Refractory (Muted teal)
        [75, 0, 130],      # 3: Quiescent Habituated (Indigo)
        [255, 20, 147],    # 4: Firing Habituated (Neon pink)
        [139, 0, 139],     # 5: Refractory Habituated (Purple-magenta)
    ],
    6: [
        [40, 40, 50],      # 0: Depleted Quiescent (Dark grey)
        [100, 110, 140],   # 1: Partially Charged (Slate blue)
        [200, 200, 230],   # 2: Fully Charged (Lavender)
        [255, 99, 71],     # 3: Firing (Tomato orange)
        [150, 0, 0],       # 4: Refractory (Deep red)
    ],
    7: [
        [8, 8, 24],        # 0: Quiescent (Deep night blue)
        [255, 215, 0],     # 1: Coincidence Hub (Bright gold)
        [255, 140, 0],     # 2: Delay 1 (Orange)
        [255, 99, 71],     # 3: Delay 2 (Tomato)
        [220, 20, 60],     # 4: Delay 3 (Crimson)
        [255, 20, 147],    # 5: Delay 4 (Hot pink)
        [255, 255, 255],   # 6: Firing Terminal (Pure white)
    ],
    8: [
        [20, 20, 20],      # 0: Quiescent (Very dark grey)
        [50, 255, 50],     # 1: Normal Firing (Lime green)
        [0, 100, 0],       # 2: Normal Refractory (Dark forest)
        [0, 200, 255],     # 3: Gas Emission (Retrograde gas cyan)
        [255, 0, 255],     # 4: Potentiated Firing (Bright magenta)
        [75, 0, 130],      # 5: Potentiated Refractory (Indigo)
    ],
    9: [
        [40, 0, 10],       # 0: Normal Quiescent (Burgundy)
        [255, 100, 150],   # 1: Sensitized (Bright rose)
        [60, 40, 20],      # 2: Desensitized (Brown)
        [255, 255, 0],     # 3: Firing (Neon yellow)
        [200, 100, 0],     # 4: Normal Refractory (Muted orange)
        [120, 30, 0],      # 5: Deep Refractory (Rust)
    ],
    10: [
        [80, 80, 80],      # 0: Exhausted (Muted grey)
        [0, 200, 100],     # 1: Charged (Emerald green)
        [100, 255, 180],   # 2: Hyper-Charged (Neon mint)
        [160, 32, 240],    # 3: Firing from Charged (Electric purple)
        [255, 255, 150],   # 4: Firing from Hyper-Charged (Light gold)
        [50, 0, 70],       # 5: Refractory Low (Dark purple)
        [180, 150, 220],   # 6: Refractory High (Light lavender)
    ],
}


# 4. Simulation Engine and Main Loop

RULES = {
    1: (rule_1, 6),
    2: (rule_2, 8),
    3: (rule_3, 4),
    4: (rule_4, 8),
    5: (rule_5, 6),
    6: (rule_6, 5),
    7: (rule_7, 7),
    8: (rule_8, 6),
    9: (rule_9, 6),
    10: (rule_10, 7),
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    
    # Initialize the grid
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        # Hand-crafted initializations to showcase rule dynamics without immediate decay
        if rule_num == 1:
            grid[0] = 3
            grid[0, W // 2] = 4
        elif rule_num == 2:
            grid[0] = 4
            grid[0, W // 2] = 5
        elif rule_num == 3:
            seed_idx = W // 2
            if seed_idx % 3 == 0:
                seed_idx += 1
            grid[0] = 0
            grid[0, seed_idx] = 1
        elif rule_num == 4:
            grid[0] = 4
            grid[0, W // 2] = 5
        elif rule_num == 5:
            grid[0] = 0
            grid[0, W // 2] = 1
        elif rule_num == 6:
            grid[0] = 2
            grid[0, W // 2] = 3
        elif rule_num == 7:
            grid[0] = 0
            grid[0, W // 2 - 1] = 6
            grid[0, W // 2 + 1] = 6
        elif rule_num == 8:
            grid[0] = 0
            grid[0, W // 2 - 1] = 3
            grid[0, W // 2] = 4
            grid[0, W // 2 + 1] = 4
        elif rule_num == 9:
            grid[0] = 1
            grid[0, W // 2] = 3
        elif rule_num == 10:
            grid[0] = 1
            grid[0, W // 2] = 3
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
