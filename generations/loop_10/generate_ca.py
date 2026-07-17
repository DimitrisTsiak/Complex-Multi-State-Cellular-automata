import os
import numpy as np
from PIL import Image

# 1. Setup output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Define Anchor Colors for vibrant, unique color palettes
ANCHORS = {
    1: [[10, 5, 20], [255, 20, 147], [255, 215, 0], [0, 255, 255]],       # Coupled Discrete Logistic Map: Deep Purple -> Hot Pink -> Gold -> Cyan
    2: [[5, 10, 25], [138, 43, 226], [255, 0, 255], [50, 205, 50], [255, 69, 0]], # Local Feistel: Dark Navy -> Purple -> Magenta -> Lime -> Orange-Red
    3: [[5, 20, 10], [0, 255, 127], [173, 255, 47], [255, 140, 0], [139, 0, 0]],   # Tent Map: Forest Green -> Mint -> Yellow-Green -> Orange -> Dark Red
    4: [[20, 0, 30], [230, 190, 255], [135, 206, 235], [0, 0, 255], [255, 250, 200]], # Hill Cipher: Dark Plum -> Lavender -> Sky Blue -> Blue -> White-Hot Gold
    5: [[15, 15, 20], [0, 240, 255], [180, 0, 255], [240, 255, 0]],       # Keccak-Inspired: Dark Charcoal -> Neon Teal -> Neon Purple -> Neon Yellow
    6: [[10, 10, 10], [180, 0, 0], [255, 69, 0], [255, 0, 255], [255, 215, 0]],    # Coupled Henon: Charcoal -> Red -> Orange -> Magenta -> Gold
    7: [[0, 20, 30], [34, 139, 34], [0, 255, 0], [0, 255, 255], [255, 255, 255]],  # Additive-Multiplicative: Dark Teal -> Forest Green -> Lime -> Cyan -> White
    8: [[5, 5, 30], [127, 0, 255], [255, 20, 147], [255, 127, 0], [255, 255, 150]],# Arnold's Cat: Dark Navy -> Violet -> Pink -> Tangerine -> Pale Yellow
    9: [[0, 0, 0], [100, 0, 0], [220, 20, 60], [255, 69, 0], [255, 215, 0], [255, 255, 240]], # SPN CA: Black -> Red -> Crimson -> Orange-Red -> Gold -> Warm White
    10: [[20, 10, 30], [57, 255, 20]]                                      # NLFSR CA: Dark Violet-Black vs Neon Lime Green
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

# 3. Define the 10 Rule Functions (with periodic boundary wrapping using np.roll)

def rule_1(arr):
    # States: 17
    # Neighborhood: r=1 including self
    # S_{t+1}(x) = [4 * S_t(x) * (17 - S_t(x)) + S_t(x-1) + S_t(x+1)] mod 17
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (4 * arr * (17 - arr) + left + right) % 17

# PRESENT S-box for Rule 2 and Rule 9
S_BOX = np.array([0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2], dtype=np.int32)

def rule_2(arr):
    # States: 16
    # Neighborhood: r=1 including self
    # S_{t+1}(x) = S_t(x-1) ^ S_box[S_t(x) ^ S_t(x+1)]
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    idx = arr ^ right
    return left ^ S_BOX[idx]

def rule_3(arr):
    # States: 32
    # Neighborhood: r=1 excluding self (but the formula uses self via T(s))
    # S_{t+1}(x) = [T(S_t(x)) + S_t(x-1) - S_t(x+1) + 32] mod 32
    # T(s) = 2*s if s < 16 else 2*(31 - s)
    t_val = np.where(arr < 16, 2 * arr, 2 * (31 - arr))
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (t_val + left - right) % 32

def rule_4(arr):
    # States: 26
    # Neighborhood: r=1 including self
    # S_{t+1}(x) = [S_t(x-1) + 2*S_t(x) + 3*S_t(x+1) + S_t(x)^3] mod 26
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (left + 2 * arr + 3 * right + arr**3) % 26

def rotl_3bit(u):
    # Bitwise left rotation of a 3-bit integer
    return ((u << 1) & 7) | (u >> 2)

def rule_5(arr):
    # States: 8 (3-bit vectors)
    # Neighborhood: r=1 including self
    # D_t(x) = S_t(x) ^ S_t(x-1) ^ rotl(S_t(x+1), 1)
    # S_{t+1}(x) = D_t(x) ^ ((~D_t(x-1)) & D_t(x+1))
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    
    # Linear diffusion step
    D = arr ^ left ^ rotl_3bit(right)
    
    # Non-linear mixing step
    D_left = np.roll(D, 1)
    D_right = np.roll(D, -1)
    return D ^ ((7 ^ D_left) & D_right)

def rule_6(arr):
    # States: 16
    # Neighborhood: r=1 including self
    # S_{t+1}(x) = [1 + 15*S_t(x)^2 + S_t(x-1) + 2*S_t(x+1)] mod 16
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (1 + 15 * (arr**2) + left + 2 * right) % 16

def rule_7(arr):
    # States: 13
    # Neighborhood: r=1 including self
    # S_{t+1}(x) = [S_t(x-1)*S_t(x+1) + S_t(x)^2 + 3] mod 13
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    return (left * right + arr**2 + 3) % 13

def rule_8(arr):
    # States: 16
    # Neighborhood: r=1 including self
    # X_t(x) = S_t(x) % 4, Y_t(x) = S_t(x) // 4
    # X_new(x) = [X_t(x) + Y_t(x) + S_t(x-1)] mod 4
    # Y_new(x) = [X_t(x) + 2*Y_t(x) + S_t(x+1)] mod 4
    # S_{t+1}(x) = X_new(x) + 4 * Y_new(x)
    left = np.roll(arr, 1)
    right = np.roll(arr, -1)
    X = arr % 4
    Y = arr // 4
    X_new = (X + Y + left) % 4
    Y_new = (X + 2 * Y + right) % 4
    return X_new + 4 * Y_new

# PRESENT P-box for Rule 9
P_BOX = np.array([0, 2, 8, 10, 1, 3, 9, 11, 4, 6, 12, 14, 5, 7, 13, 15], dtype=np.int32)

def rule_9(arr):
    # States: 16
    # Neighborhood: r=2 including self
    # M_t(x) = S_t(x-2) ^ S_t(x-1) ^ S_t(x) ^ S_t(x+1) ^ S_t(x+2)
    # V_t(x) = S_box[M_t(x)]
    # S_{t+1}(x) = P[V_t(x)]
    M = np.roll(arr, 2) ^ np.roll(arr, 1) ^ arr ^ np.roll(arr, -1) ^ np.roll(arr, -2)
    V = S_BOX[M]
    return P_BOX[V]

def rule_10(arr):
    # States: 2
    # Neighborhood: Asymmetric r=3 (x-3, x-2, x-1, x, x+1)
    # S_{t+1}(x) = S_t(x-3) ^ S_t(x-1) ^ S_t(x) ^ (S_t(x-2) & S_t(x+1))
    return np.roll(arr, 3) ^ np.roll(arr, 1) ^ arr ^ (np.roll(arr, 2) & np.roll(arr, -1))


# 4. Simulation Engine and Main Loop

RULES = {
    1: (rule_1, 17),
    2: (rule_2, 16),
    3: (rule_3, 32),
    4: (rule_4, 26),
    5: (rule_5, 8),
    6: (rule_6, 16),
    7: (rule_7, 13),
    8: (rule_8, 16),
    9: (rule_9, 16),
    10: (rule_10, 2),
}

def simulate_and_save(rule_num, init_type, W=800, H=800):
    rule_func, num_states = RULES[rule_num]
    
    # Initialize the space-time history grid
    grid = np.zeros((H, W), dtype=np.int32)
    
    if init_type == "single_seed":
        # Single-seed initialization: middle cell is set to 1, others to 0
        grid[0, W // 2] = 1
    elif init_type == "random":
        # Random initialization: all cells are independent random states in [0, N-1]
        grid[0] = np.random.randint(0, num_states, size=W, dtype=np.int32)
        
    # Simulate step-by-step
    for t in range(H - 1):
        grid[t + 1] = rule_func(grid[t])
        
    # Generate the palette programmatically from anchors
    palette = get_palette(rule_num, num_states)
    
    # Map the state grid (H, W) to RGB (H, W, 3)
    rgb_data = palette[grid]
    
    # Create PIL Image and save
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
