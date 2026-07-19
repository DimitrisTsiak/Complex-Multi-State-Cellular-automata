import os
import numpy as np
from PIL import Image

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return np.array([int(hex_str[i:i+2], 16) for i in (0, 2, 4)], dtype=np.uint8)

# Define palettes for each rule
palettes = {
    1: np.array([hex_to_rgb('#0a0915'), hex_to_rgb('#00d2ff'), hex_to_rgb('#ff007f'), hex_to_rgb('#ffff00'), hex_to_rgb('#39ff14')]),
    2: np.array([hex_to_rgb('#03161c'), hex_to_rgb('#2ecc71'), hex_to_rgb('#ff6600'), hex_to_rgb('#9b59b6'), hex_to_rgb('#ff3333')]),
    3: np.array([hex_to_rgb('#111111'), hex_to_rgb('#00ffff'), hex_to_rgb('#ff69b4'), hex_to_rgb('#ffd700'), hex_to_rgb('#dc143c')]),
    4: np.array([hex_to_rgb('#000000'), hex_to_rgb('#ff6f61'), hex_to_rgb('#aef359'), hex_to_rgb('#7b1fa2'), hex_to_rgb('#1565c0'), hex_to_rgb('#78909c')]),
    5: np.array([hex_to_rgb('#1a0f0f'), hex_to_rgb('#00ff66'), hex_to_rgb('#00bfff'), hex_to_rgb('#ff4500'), hex_to_rgb('#ffd700')]),
    6: np.array([hex_to_rgb('#181818'), hex_to_rgb('#b39ddb'), hex_to_rgb('#00e5ff'), hex_to_rgb('#ff6d00'), hex_to_rgb('#7f0000')]),
    7: np.array([hex_to_rgb('#1e272c'), hex_to_rgb('#81d4fa'), hex_to_rgb('#ffcc80'), hex_to_rgb('#0d47a1'), hex_to_rgb('#b71c1c')]),
    8: np.array([hex_to_rgb('#050505'), hex_to_rgb('#ff007f'), hex_to_rgb('#00ff88'), hex_to_rgb('#ffff33'), hex_to_rgb('#0e3a1f')]),
    9: np.array([hex_to_rgb('#1c2833'), hex_to_rgb('#33ccff'), hex_to_rgb('#cc33ff'), hex_to_rgb('#ccff33'), hex_to_rgb('#ff9933'), hex_to_rgb('#0f0f0f')]),
    10: np.array([hex_to_rgb('#120a2a'), hex_to_rgb('#d4ac0d'), hex_to_rgb('#e67e22'), hex_to_rgb('#c0392b')])
}

def step_rule_1(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    C_I = (S_left == 2).astype(int) + (S_right == 2).astype(int)
    C_V = (S_left == 3).astype(int) + (S_right == 3).astype(int)
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    S_next[mask_0] = np.where((C_V[mask_0] >= 1) | (C_I[mask_0] == 2), 1, 0)
    
    mask_1 = (S == 1)
    S_next[mask_1] = np.where((C_I[mask_1] + C_V[mask_1] >= 1), 2, 0)
    
    mask_2 = (S == 2)
    S_next[mask_2] = np.where((C_I[mask_2] >= 1) & (C_V[mask_2] >= 1), 3, 4)
    
    mask_4 = (S == 4)
    S_next[mask_4] = np.where(C_V[mask_4] == 0, 0, 4)
    
    return S_next

def step_rule_2(S):
    S_left1 = np.roll(S, 1)
    S_left2 = np.roll(S, 2)
    S_right1 = np.roll(S, -1)
    S_right2 = np.roll(S, -2)
    
    V_L = (S_left1 == 3) | (S_left2 == 3)
    V_R = (S_right1 == 3) | (S_right2 == 3)
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    cond_1_for_0 = (S_left1 == 3) | (S_right1 == 3)
    cond_2_for_0 = ((S_left1 == 2) & (S_left2 != 3) & V_R) | ((S_right1 == 2) & (S_right2 != 3) & V_L)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where(cond_2_for_0, 2, val_for_0)
    val_for_0 = np.where(cond_1_for_0, 1, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = np.where(V_L[mask_1] | V_R[mask_1], 2, 1)
    
    mask_2 = (S == 2)
    cond_1_for_2 = (S_left1 == 3) | (S_right1 == 3)
    S_next[mask_2] = np.where(cond_1_for_2[mask_2], 4, 0)
    
    mask_4 = (S == 4)
    S_next[mask_4] = 0
    
    return S_next

def step_rule_3(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    cond_c = (S_left == 4) & (S_right == 3)
    cond_b = (S_right == 2)
    cond_a = (S_left == 1)
    val_for_0 = np.where(cond_c, 4, val_for_0)
    val_for_0 = np.where(cond_b, 2, val_for_0)
    val_for_0 = np.where(cond_a, 1, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = np.where(S_right[mask_1] == 3, 4, 0)
    
    mask_2 = (S == 2)
    S_next[mask_2] = np.where(S_left[mask_2] == 3, 4, 0)
    
    return S_next

def step_rule_4(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    N_1 = (S_left == 1).astype(int) + (S_right == 1).astype(int)
    N_2 = (S_left == 2).astype(int) + (S_right == 2).astype(int)
    N_3 = (S_left == 3).astype(int) + (S_right == 3).astype(int)
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    cond_2_for_0 = (N_2 >= 1)
    cond_1_for_0 = (N_1 >= 1)
    cond_3_for_0 = (N_3 >= 1) | ((N_1 >= 1) & (N_2 >= 1))
    val_for_0 = np.where(cond_2_for_0, 2, val_for_0)
    val_for_0 = np.where(cond_1_for_0, 1, val_for_0)
    val_for_0 = np.where(cond_3_for_0, 3, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = 4
    
    mask_2 = (S == 2)
    S_next[mask_2] = np.where(N_1[mask_2] >= 1, 3, 5)
    
    mask_3 = (S == 3)
    S_next[mask_3] = 5
    
    mask_4 = (S == 4)
    S_next[mask_4] = np.where(N_3[mask_4] >= 1, 3, 0)
    
    mask_5 = (S == 5)
    S_next[mask_5] = 0
    
    return S_next

def step_rule_5(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    N_I = (S_left == 1).astype(int) + (S_right == 1).astype(int)
    N_D = (S_left == 2).astype(int) + (S_right == 2).astype(int)
    N_T = (S_left == 3).astype(int) + (S_right == 3).astype(int)
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    cond_4_for_0 = (N_D >= 1) & (N_I == 0)
    cond_1_for_0 = ((N_I >= 1) & (N_D == 0)) | (N_T >= 1)
    val_for_0 = np.where(cond_4_for_0, 4, val_for_0)
    val_for_0 = np.where(cond_1_for_0, 1, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = np.where((N_D[mask_1] >= 1) & (N_I[mask_1] == 0), 4, 1)
    
    mask_2 = (S == 2)
    S_next[mask_2] = np.where(N_I[mask_2] >= 2, 3, 2)
    
    mask_4 = (S == 4)
    S_next[mask_4] = np.where(N_T[mask_4] >= 2, 1, 4)
    
    return S_next

def step_rule_6(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    N_active = (S_left == 3).astype(int) + (S_right == 3).astype(int)
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where(S_left == 2, 2, val_for_0)
    val_for_0 = np.where(N_active >= 1, 1, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    cond_activation = (S_left == 2) | (S_right == 2) | (N_active >= 1)
    S_next[mask_1] = np.where(cond_activation[mask_1], 3, 1)
    
    mask_2 = (S == 2)
    S_next[mask_2] = 0
    
    mask_3 = (S == 3)
    S_next[mask_3] = 4
    
    mask_4 = (S == 4)
    S_next[mask_4] = 0
    
    return S_next

def step_rule_7(S):
    S_left1 = np.roll(S, 1)
    S_left2 = np.roll(S, 2)
    S_right1 = np.roll(S, -1)
    S_right2 = np.roll(S, -2)
    
    W_L = ((S_left1 == 1).astype(int) + (S_left2 == 1).astype(int) + 
           (S_right1 == 1).astype(int) + (S_right2 == 1).astype(int) +
           2 * ((S_left1 == 3).astype(int) + (S_left2 == 3).astype(int) + 
                (S_right1 == 3).astype(int) + (S_right2 == 3).astype(int)))
    
    W_R = ((S_left1 == 2).astype(int) + (S_left2 == 2).astype(int) + 
           (S_right1 == 2).astype(int) + (S_right2 == 2).astype(int) +
           2 * ((S_left1 == 4).astype(int) + (S_left2 == 4).astype(int) + 
                (S_right1 == 4).astype(int) + (S_right2 == 4).astype(int)))
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where(W_R > W_L + 1, 2, val_for_0)
    val_for_0 = np.where(W_L > W_R + 1, 1, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    val_for_1 = np.ones_like(S)
    val_for_1 = np.where(W_R > W_L, 0, val_for_1)
    val_for_1 = np.where(W_L > W_R + 2, 3, val_for_1)
    S_next[mask_1] = val_for_1[mask_1]
    
    mask_2 = (S == 2)
    val_for_2 = np.full_like(S, 2)
    val_for_2 = np.where(W_L > W_R, 0, val_for_2)
    val_for_2 = np.where(W_R > W_L + 2, 4, val_for_2)
    S_next[mask_2] = val_for_2[mask_2]
    
    mask_3 = (S == 3)
    S_next[mask_3] = np.where(W_R[mask_3] > W_L[mask_3] + 4, 1, 3)
    
    mask_4 = (S == 4)
    S_next[mask_4] = np.where(W_L[mask_4] > W_R[mask_4] + 4, 2, 4)
    
    return S_next

def step_rule_8(S):
    S_left = np.roll(S, 1)
    S_right = np.roll(S, -1)
    
    N_P = (S_left == 1).astype(int) + (S_right == 1).astype(int)
    N_H = (S_left == 3).astype(int) + (S_right == 3).astype(int)
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where(N_H >= 1, 1, val_for_0)
    val_for_0 = np.where(N_P >= 1, 2, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = 0
    
    mask_2 = (S == 2)
    cond_activation = (N_H >= 1) | (S_left == 2) | (S_right == 2)
    S_next[mask_2] = np.where(cond_activation[mask_2], 3, 2)
    
    mask_3 = (S == 3)
    S_next[mask_3] = 4
    
    mask_4 = (S == 4)
    S_next[mask_4] = np.where(N_P[mask_4] >= 2, 2, 0)
    
    return S_next

def step_rule_9(S):
    S_left1 = np.roll(S, 1)
    S_left2 = np.roll(S, 2)
    S_right1 = np.roll(S, -1)
    S_right2 = np.roll(S, -2)
    
    N_S = ((S_left1 == 1).astype(int) + (S_left2 == 1).astype(int) + 
           (S_right1 == 1).astype(int) + (S_right2 == 1).astype(int))
    
    N_P = ((S_left1 == 2).astype(int) + (S_left2 == 2).astype(int) + 
           (S_right1 == 2).astype(int) + (S_right2 == 2).astype(int))
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    val_for_0 = np.zeros_like(S)
    val_for_0 = np.where((N_S >= 1) & (N_P == 0), 1, val_for_0)
    val_for_0 = np.where((N_P >= 2) & (N_S < 1), 2, val_for_0)
    S_next[mask_0] = val_for_0[mask_0]
    
    mask_1 = (S == 1)
    S_next[mask_1] = np.where(N_S[mask_1] >= 3, 3, 1)
    
    mask_2 = (S == 2)
    S_next[mask_2] = np.where(N_S[mask_2] >= 2, 1, 5)
    
    mask_3 = (S == 3)
    S_next[mask_3] = 4
    
    mask_4 = (S == 4)
    S_next[mask_4] = 5
    
    mask_5 = (S == 5)
    S_next[mask_5] = np.where(N_S[mask_5] >= 1, 0, 5)
    
    return S_next

def step_rule_10(S):
    S_left1 = np.roll(S, 1)
    S_left2 = np.roll(S, 2)
    S_right1 = np.roll(S, -1)
    S_right2 = np.roll(S, -2)
    
    N_A = ((S_left1 == 2).astype(int) + (S_left2 == 2).astype(int) + 
           (S_right1 == 2).astype(int) + (S_right2 == 2).astype(int))
    
    N_D = ((S_left1 == 3).astype(int) + (S_left2 == 3).astype(int) + 
           (S_right1 == 3).astype(int) + (S_right2 == 3).astype(int))
    
    N_total = N_A + 2 * N_D
    
    S_next = np.copy(S)
    
    mask_0 = (S == 0)
    S_next[mask_0] = np.where(N_total[mask_0] >= 3, 1, 0)
    
    mask_1 = (S == 1)
    val_for_1 = np.ones_like(S)
    val_for_1 = np.where(N_total <= 1, 0, val_for_1)
    val_for_1 = np.where(N_total >= 4, 2, val_for_1)
    S_next[mask_1] = val_for_1[mask_1]
    
    mask_2 = (S == 2)
    val_for_2 = np.full_like(S, 2)
    val_for_2 = np.where(N_total == 0, 1, val_for_2)
    cond_to_3 = (N_D >= 2) | ((N_A >= 3) & (N_D >= 1))
    val_for_2 = np.where(cond_to_3, 3, val_for_2)
    S_next[mask_2] = val_for_2[mask_2]
    
    return S_next

def step_rule(rule_idx, S):
    if rule_idx == 1: return step_rule_1(S)
    elif rule_idx == 2: return step_rule_2(S)
    elif rule_idx == 3: return step_rule_3(S)
    elif rule_idx == 4: return step_rule_4(S)
    elif rule_idx == 5: return step_rule_5(S)
    elif rule_idx == 6: return step_rule_6(S)
    elif rule_idx == 7: return step_rule_7(S)
    elif rule_idx == 8: return step_rule_8(S)
    elif rule_idx == 9: return step_rule_9(S)
    elif rule_idx == 10: return step_rule_10(S)
    else: raise ValueError(f"Unknown rule {rule_idx}")

def initialize_grid(rule_idx, init_type, width=800):
    grid = np.zeros(width, dtype=np.uint8)
    
    if init_type == "random":
        if rule_idx == 1:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.85, 0.05, 0.05, 0.01, 0.04]).astype(np.uint8)
        elif rule_idx == 2:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.90, 0.04, 0.04, 0.01, 0.01]).astype(np.uint8)
        elif rule_idx == 3:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.94, 0.02, 0.02, 0.01, 0.01]).astype(np.uint8)
        elif rule_idx == 4:
            grid = np.random.choice([0, 1, 2, 3, 4, 5], size=width, p=[0.92, 0.04, 0.04, 0.00, 0.00, 0.00]).astype(np.uint8)
        elif rule_idx == 5:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.80, 0.12, 0.08, 0.00, 0.00]).astype(np.uint8)
        elif rule_idx == 6:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.95, 0.045, 0.005, 0.00, 0.00]).astype(np.uint8)
        elif rule_idx == 7:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.40, 0.20, 0.20, 0.10, 0.10]).astype(np.uint8)
        elif rule_idx == 8:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.88, 0.02, 0.08, 0.02, 0.00]).astype(np.uint8)
        elif rule_idx == 9:
            grid = np.random.choice([0, 1, 2, 3, 4, 5], size=width, p=[0.85, 0.10, 0.05, 0.00, 0.00, 0.00]).astype(np.uint8)
        elif rule_idx == 10:
            grid = np.random.choice([0, 1, 2, 3], size=width, p=[0.80, 0.10, 0.08, 0.02]).astype(np.uint8)
            
    elif init_type == "single_seed":
        if rule_idx == 1:
            grid[200] = 3
            grid[400] = 3
            grid[600] = 3
            grid[198] = 2
            grid[202] = 2
            grid[398] = 2
            grid[402] = 2
            grid[598] = 2
            grid[602] = 2
        elif rule_idx == 2:
            grid[200] = 3
            grid[400] = 3
            grid[600] = 3
            grid[197] = 2
            grid[203] = 2
            grid[397] = 2
            grid[403] = 2
            grid[597] = 2
            grid[603] = 2
            grid[198] = 1
            grid[202] = 1
            grid[398] = 1
            grid[402] = 1
            grid[598] = 1
            grid[602] = 1
        elif rule_idx == 3:
            grid[400] = 3
            grid[100] = 1
            grid[200] = 1
            grid[300] = 1
            grid[500] = 2
            grid[600] = 2
            grid[700] = 2
        elif rule_idx == 4:
            grid[200] = 1
            grid[600] = 1
            grid[400] = 2
        elif rule_idx == 5:
            grid[380:420] = 2
            grid[378] = 1
            grid[379] = 1
            grid[421] = 1
            grid[422] = 1
        elif rule_idx == 6:
            for i in range(50, 750, 40):
                grid[i] = 1
            grid[10] = 2
        elif rule_idx == 7:
            grid[200:220] = 3
            grid[580:600] = 4
            grid[220:300] = 1
            grid[500:580] = 2
        elif rule_idx == 8:
            grid[195:205] = 2
            grid[395:405] = 2
            grid[595:605] = 2
            grid[200] = 3
            grid[400] = 3
            grid[600] = 3
        elif rule_idx == 9:
            grid[199:202] = 1
            grid[398:403] = 1
            grid[596:605] = 1
            grid[100] = 2
            grid[700] = 2
        elif rule_idx == 10:
            grid[390:410] = 3
            grid[385:390] = 1
            grid[410:415] = 1
            
    return grid

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    width = 800
    height = 800
    
    for rule_idx in range(1, 11):
        print(f"Simulating Rule {rule_idx}...")
        palette = palettes[rule_idx]
        
        for init_type in ["single_seed", "random"]:
            if init_type == "random":
                np.random.seed(42 + rule_idx)
                
            S = initialize_grid(rule_idx, init_type, width)
            history = np.zeros((height, width), dtype=np.uint8)
            history[0] = S
            
            for t in range(1, height):
                S = step_rule(rule_idx, S)
                history[t] = S
                
            # Map state history to RGB image using index mapping
            rgb_img = palette[history]
            
            # Save the image using Pillow (PIL)
            img = Image.fromarray(rgb_img, 'RGB')
            filename = f"rule_{rule_idx:02d}_{init_type}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            print(f"Saved {filename}")

if __name__ == "__main__":
    main()
