import os
import numpy as np
from PIL import Image

# Setup output directory relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")
os.makedirs(output_dir, exist_ok=True)

# Color palettes (unique and vibrant for each rule)
PALETTES = {
    1: np.array([
        [15, 15, 35],     # 0: Deep blue (cold)
        [30, 80, 150],    # 1: Medium blue
        [40, 150, 180],   # 2: Cyan
        [50, 180, 120],   # 3: Green-blue
        [100, 200, 80],   # 4: Green
        [220, 200, 50],   # 5: Yellow-orange
        [240, 120, 30],   # 6: Bright orange
        [255, 30, 30]     # 7: Red-hot (hot)
    ], dtype=np.uint8),
    2: np.array([
        [20, 20, 25],     # 0: Dark charcoal
        [255, 160, 60],   # 1: Light orange (hot)
        [255, 60, 40],    # 2: Vibrant red-orange (hot)
        [100, 180, 255],  # 3: Soft light blue (cold)
        [40, 100, 230],   # 4: Medium blue (cold)
        [10, 30, 150]     # 5: Deep navy-blue (cold)
    ], dtype=np.uint8),
    3: np.array([
        [15, 15, 20],     # 0: Deep grey (quiescent)
        [90, 40, 120],    # 1: Dark purple (leftward 1)
        [140, 60, 180],   # 2: Medium purple (leftward 2)
        [210, 80, 255],   # 3: Bright violet-magenta (leftward 3)
        [80, 100, 30],    # 4: Dark olive-green (rightward 1)
        [120, 160, 40],   # 5: Medium green (rightward 2)
        [180, 230, 50],   # 6: Lime green-yellow (rightward 3)
        [80, 255, 255]    # 7: Electric cyan-white (vortex)
    ], dtype=np.uint8),
    4: np.array([
        [25, 10, 35],     # 0: Dark violet
        [110, 20, 90],    # 1: Deep pink
        [180, 30, 140],   # 2: Magenta
        [240, 50, 180],   # 3: Neon pink
        [255, 240, 50],   # 4: Bright neon yellow (discharge)
        [255, 255, 255]   # 5: Pure white (discharge)
    ], dtype=np.uint8),
    5: np.array([
        [20, 24, 30],     # 0: Deep dark slate
        [60, 150, 150],   # 1: Soft teal (leftward slow)
        [30, 220, 220],   # 2: Electric turquoise (leftward fast)
        [180, 130, 60],   # 3: Soft amber (rightward slow)
        [255, 100, 20],   # 4: Hot orange (rightward fast)
        [100, 10, 20]     # 5: Dark blood red (turbulent scars)
    ], dtype=np.uint8),
    6: np.array([
        [10, 10, 18],     # 0: Gas phase
        [20, 70, 90],     # 1: Dark oceanic teal
        [30, 130, 140],   # 2: Vibrant sea green
        [50, 190, 220],   # 3: Bright sky blue
        [200, 250, 255]   # 4: Ice blue/white
    ], dtype=np.uint8),
    7: np.array([
        [255, 230, 80],   # 0: Hot, Fresh (yellow)
        [255, 170, 60],   # 1: Hot, Med Fresh (pale orange)
        [230, 100, 40],   # 2: Hot, Med Salty (dark orange)
        [200, 50, 30],    # 3: Hot, Salty (red-orange)
        [120, 220, 200],  # 4: Cold, Fresh (pale aqua)
        [40, 170, 120],   # 5: Cold, Med Fresh (emerald green)
        [20, 100, 110],   # 6: Cold, Med Salty (deep teal)
        [30, 30, 100]     # 7: Cold, Salty (dark navy)
    ], dtype=np.uint8),
    8: np.array([
        [20, 50, 150],    # 0: Deep cobalt blue
        [40, 90, 220],    # 1: Royal blue
        [100, 160, 255],  # 2: Sky blue
        [160, 120, 10],   # 3: Deep gold
        [240, 210, 20],   # 4: Bright yellow
        [255, 245, 120],  # 5: Pale yellow
        [255, 20, 147],   # 6: Neon pink (wave)
        [255, 69, 0]      # 7: Electric orange (vortex)
    ], dtype=np.uint8),
    9: np.array([
        [15, 20, 30],     # 0: Dark night navy
        [80, 30, 100],    # 1: Deep purple
        [180, 40, 110],   # 2: Magenta-red
        [240, 90, 70],    # 3: Neon coral
        [50, 220, 90],    # 4: Neon green
        [200, 255, 210]   # 5: Bright white-green
    ], dtype=np.uint8),
    10: np.array([
        [25, 25, 25],     # 0: Very dark brown/grey (matrix)
        [210, 180, 140],  # 1: Light sand/beige
        [180, 130, 70],   # 2: Golden brown
        [160, 80, 50],    # 3: Terracotta/rust
        [120, 140, 90],   # 4: Pale olive
        [100, 130, 150],  # 5: Soft blue-grey
        [60, 100, 140],   # 6: Medium steel blue
        [10, 60, 180]     # 7: Intense water blue
    ], dtype=np.uint8)
}

# --- Update functions for each of the 10 rules ---

def step_rule1(S):
    # Clamped Advection-Diffusion
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    diff = S_right - S_left
    sgn = np.sign(diff).astype(int)
    return np.clip(S_left + sgn, 0, 7)

def step_rule2(S):
    # Buoyancy Convective Plumes
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    R_right = (S_right == 1) | (S_right == 2)
    K_left = (S_left == 3) | (S_left == 4) | (S_left == 5)
    
    cond1 = R_right & K_left
    cond2 = R_right & ~K_left
    cond3 = K_left & ~R_right & (S_left > 3)
    cond4 = K_left & ~R_right & (S_left == 3)
    cond5 = ~R_right & ~K_left & ((S == 1) | (S == 2))
    cond6 = ~R_right & ~K_left & ((S == 4) | (S == 5))
    
    val2 = np.maximum(1, S_right - 1)
    val3 = S_left - 1
    val5 = S - 1
    val6 = S - 1
    
    S_next = np.select(
        [cond1, cond2, cond3, cond4, cond5, cond6],
        [0, val2, val3, 0, val5, val6],
        default=0
    )
    return S_next

def step_rule3(S):
    # Rayleigh-Bénard Convective Cells
    V_lookup = np.array([0, -1, -2, -3, 1, 2, 3, 0])
    
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    V_left = V_lookup[S_left]
    V_right = V_lookup[S_right]
    
    # 1. Vortex core decay: S == 7 -> 0
    mask7 = (S == 7)
    
    # 2. Vortex ejection and flow collisions in quiescent cells: S == 0
    mask0 = (S == 0)
    cond0_both7 = mask0 & (S_right == 7) & (S_left == 7)
    cond0_right7 = mask0 & (S_right == 7) & ~cond0_both7
    cond0_left7 = mask0 & (S_left == 7) & ~cond0_both7 & ~cond0_right7
    cond0_shear = mask0 & (V_left > 0) & (V_right < 0) & ~cond0_both7 & ~cond0_right7 & ~cond0_left7
    cond0_right_flow = mask0 & (V_right < 0) & ~cond0_both7 & ~cond0_right7 & ~cond0_left7 & ~cond0_shear
    cond0_left_flow = mask0 & (V_left > 0) & ~cond0_both7 & ~cond0_right7 & ~cond0_left7 & ~cond0_shear & ~cond0_right_flow
    
    val0 = np.zeros_like(S)
    val0[cond0_both7] = 7
    val0[cond0_right7] = 3
    val0[cond0_left7] = 6
    val0[cond0_shear] = 7
    val0[cond0_right_flow] = np.where((S_right == 2) | (S_right == 3), S_right - 1, 0)[cond0_right_flow]
    val0[cond0_left_flow] = np.where((S_left == 5) | (S_left == 6), S_left - 1, 0)[cond0_left_flow]
    
    # 3. Flow propagation in active channels: S in {1, 2, 3} (leftward)
    mask_leftward = (S == 1) | (S == 2) | (S == 3)
    condL_r7 = mask_leftward & (S_right == 7)
    condL_shear = mask_leftward & (V_left > 0) & ~condL_r7
    condL_prop = mask_leftward & ~condL_r7 & ~condL_shear
    
    valL = np.zeros_like(S)
    valL[condL_r7] = 3
    valL[condL_shear] = 7
    
    u_L = np.where((S_right == 1) | (S_right == 2) | (S_right == 3), S_right, 0)
    valL_prop = np.where(u_L > 0, np.maximum(1, u_L - 1), np.where(S > 1, S - 1, 0))
    valL[condL_prop] = valL_prop[condL_prop]
    
    # 4. Rightward flow channels: S in {4, 5, 6} (rightward)
    mask_rightward = (S == 4) | (S == 5) | (S == 6)
    condR_l7 = mask_rightward & (S_left == 7)
    condR_shear = mask_rightward & (V_right < 0) & ~condR_l7
    condR_prop = mask_rightward & ~condR_l7 & ~condR_shear
    
    valR = np.zeros_like(S)
    valR[condR_l7] = 6
    valR[condR_shear] = 7
    
    u_R = np.where((S_left == 4) | (S_left == 5) | (S_left == 6), S_left, 0)
    valR_prop = np.where(u_R > 0, np.where(u_R > 4, u_R - 1, 0), np.where(S > 4, S - 1, 0))
    valR[condR_prop] = valR_prop[condR_prop]
    
    S_next = np.select(
        [mask7, mask0, mask_leftward, mask_rightward],
        [0, val0, valL, valR],
        default=0
    )
    return S_next

def step_rule4(S):
    # Compressible Gas Shockwaves
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    E = (S_left >= 4).astype(int) + (S_right >= 4).astype(int)
    return np.where(S >= 4, 0, np.minimum(5, S + E))

def step_rule5(S):
    # Viscous Drag & Shear Flow
    V_lookup = np.array([0, -1, -2, 1, 2, 0])
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    V_curr = V_lookup[S]
    V_left = V_lookup[S_left]
    V_right = V_lookup[S_right]
    
    # 1. Turbulent shear trigger: |V_right - V_left| >= 3
    shear = np.abs(V_right - V_left)
    cond_turbulent = (shear >= 3)
    
    # 2. Turbulent dissipation: S == 5
    cond_dissipate = (S == 5) & ~cond_turbulent
    
    # 3. Viscous smoothing
    cond_viscous = ~cond_turbulent & ~cond_dissipate
    
    V_sum = V_left + V_curr + V_right
    V_avg = np.round(V_sum / 3.0).astype(int)
    
    S_viscous = np.select(
        [V_avg <= -2, V_avg == -1, V_avg == 0, V_avg == 1, V_avg >= 2],
        [2, 1, 0, 3, 4],
        default=0
    )
    
    S_next = np.select(
        [cond_turbulent, cond_dissipate, cond_viscous],
        [5, 0, S_viscous],
        default=0
    )
    return S_next

def step_rule6(S):
    # Surface Tension & Cohesion
    S_l2 = np.roll(S, 2)
    S_l1 = np.roll(S, 1)
    S_r1 = np.roll(S, -1)
    S_r2 = np.roll(S, -2)
    
    L = (S_l2 >= 1).astype(int) + (S_l1 >= 1).astype(int) + (S_r1 >= 1).astype(int) + (S_r2 >= 1).astype(int)
    
    # Gas phase
    S_gas_next = np.where(L >= 3, 1, 0)
    
    # Liquid phase
    S_liq_next = np.select(
        [L <= 1, L == 4],
        [S - 1, np.minimum(4, S + 1)],
        default=S
    )
    
    return np.where(S == 0, S_gas_next, S_liq_next)

def step_rule7(S):
    # Thermohaline Circulation
    T = S // 4
    S_salt = S % 4
    
    T_l2 = np.roll(T, 2)
    T_l1 = np.roll(T, 1)
    T_r1 = np.roll(T, -1)
    T_r2 = np.roll(T, -2)
    T_sum = T_l2 + T_l1 + T + T_r1 + T_r2
    T_next = np.where(T_sum >= 3, 1, 0)
    
    S_salt_left = np.roll(S_salt, 1)
    S_salt_right = np.roll(S_salt, -1)
    T_left = np.roll(T, 1)
    
    cond_advect = (T_left == 1) & (S_salt_left >= 2)
    
    S_salt_sum = S_salt_left + S_salt + S_salt_right
    S_salt_diffused = np.round(S_salt_sum / 3.0).astype(int)
    
    S_salt_next = np.where(cond_advect, S_salt_left, S_salt_diffused)
    
    return 4 * T_next + S_salt_next

def step_rule8(S):
    # Kelvin-Helmholtz Instability
    V_lookup = np.array([-1, -2, -3, 1, 2, 3, 0, 0])
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    V_left = V_lookup[S_left]
    V_right = V_lookup[S_right]
    
    mask_decay = (S == 6) | (S == 7)
    S_decay = np.where(S == 7, 6, 0)
    
    mask_flow = ~mask_decay
    delta_V = np.abs(V_right - V_left)
    
    cond_vortex = mask_flow & (delta_V >= 5)
    cond_wave = mask_flow & (delta_V >= 3) & (delta_V < 5)
    cond_laminar = mask_flow & (delta_V < 3)
    
    R_in_L = (S_right == 0) | (S_right == 1) | (S_right == 2)
    L_in_R = (S_left == 3) | (S_left == 4) | (S_left == 5)
    
    cond_lam_r = cond_laminar & R_in_L & ~L_in_R
    cond_lam_l = cond_laminar & L_in_R & ~R_in_L
    cond_lam_both = cond_laminar & R_in_L & L_in_R
    cond_lam_none = cond_laminar & ~R_in_L & ~L_in_R
    
    S_next = np.zeros_like(S)
    S_next[mask_decay] = S_decay[mask_decay]
    S_next[cond_vortex] = 7
    S_next[cond_wave] = 6
    S_next[cond_lam_r] = S_right[cond_lam_r]
    S_next[cond_lam_l] = S_left[cond_lam_l]
    S_next[cond_lam_both] = 6
    S_next[cond_lam_none] = S[cond_lam_none]
    
    return S_next

def step_rule9(S):
    # Evaporative Convection (Marangoni)
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    M = np.maximum(S_left, S_right)
    
    cond1 = (S < M)
    cond2 = (S > M)
    cond3 = (S == M) & (S > 0)
    
    val1 = np.maximum(S, M - 1)
    val2 = np.maximum(0, S - 2)
    val3 = S - 1
    
    return np.select(
        [cond1, cond2, cond3],
        [val1, val2, val3],
        default=0
    )

def step_rule10(S):
    # Porous Darcy Gravity Currents
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    F_l_c = ((S_left >= 3) & (S_left > S)).astype(int)
    F_r_c = ((S_right >= 3) & (S_right > S)).astype(int)
    
    F_c_l = ((S >= 3) & (S > S_left)).astype(int)
    F_c_r = ((S >= 3) & (S > S_right)).astype(int)
    
    Gain = F_l_c + F_r_c
    Loss = F_c_l + F_c_r
    
    return np.clip(S + Gain - Loss, 0, 7)

# Map rule numbers to their respective step functions
RULE_FUNCTIONS = {
    1: step_rule1,
    2: step_rule2,
    3: step_rule3,
    4: step_rule4,
    5: step_rule5,
    6: step_rule6,
    7: step_rule7,
    8: step_rule8,
    9: step_rule9,
    10: step_rule10
}

def run_simulation(rule_num, init_type, W=800, T=800):
    palette = PALETTES[rule_num]
    N = len(palette)
    step_fn = RULE_FUNCTIONS[rule_num]
    
    # Initialize grid
    if init_type == "single_seed":
        grid = np.zeros(W, dtype=int)
        grid[W // 2] = N - 1
    elif init_type == "random":
        grid = np.random.randint(0, N, size=W)
    else:
        raise ValueError("Invalid init_type")
        
    history = np.empty((T, W), dtype=int)
    history[0] = grid
    
    for t in range(1, T):
        grid = step_fn(grid)
        history[t] = grid
        
    # Map history grid to RGB colors
    rgb_image = palette[history]
    
    # Save as 800x800 PNG
    img = Image.fromarray(rgb_image)
    filename = os.path.join(output_dir, f"rule_{rule_num:02d}_{init_type}.png")
    img.save(filename)
    print(f"Saved: {filename}")

if __name__ == "__main__":
    print("Starting simulation for 10 rules...")
    for rule in range(1, 11):
        print(f"Simulating Rule {rule}...")
        run_simulation(rule, "single_seed")
        run_simulation(rule, "random")
    print("All simulations finished successfully!")
