import os
import numpy as np
from PIL import Image

def run_ca_rule_1(init_type, X=800, T=800):
    # Rule 1: Wheeler's Loop (Matter-Geometry Coupling)
    S = np.zeros(X, dtype=np.int32)
    
    if init_type == "single_seed":
        S[X//2] = 7  # Matter = 1, Potential = 3 (1 + 2*3 = 7)
        S[X//2 - 1] = 5 # Matter = 1, Potential = 2 (1 + 2*2 = 5)
        S[X//2 + 1] = 5 # Matter = 1, Potential = 2
    else:
        # Random matter with 15% probability, random potential 0..3
        M = (np.random.rand(X) < 0.15).astype(np.int32)
        G = np.random.randint(0, 4, size=X, dtype=np.int32)
        S = M + 2 * G
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        M = S % 2
        G = S // 2
        
        S_L = np.roll(S, 1)
        S_R = np.roll(S, -1)
        Phi = G
        Phi_L = np.roll(G, 1)
        Phi_R = np.roll(G, -1)
        
        # L(y) = I(Phi(y-1) > Phi(y) and Phi(y-1) >= Phi(y+1))
        # R(y) = I(Phi(y+1) > Phi(y) and Phi(y+1) > Phi(y-1))
        L = (Phi_L > Phi) & (Phi_L >= Phi_R)
        R = (Phi_R > Phi) & (Phi_R > Phi_L)
        Stay = 1 - L.astype(np.int32) - R.astype(np.int32)
        
        M_L = np.roll(M, 1) * np.roll(R, 1)
        M_R = np.roll(M, -1) * np.roll(L, -1)
        M_S = M * Stay
        M_next = np.minimum(1, M_L + M_R + M_S)
        
        G_sum = Phi_L + G + Phi_R
        G_next = np.minimum(3, (G_sum // 3) + M_next)
        
        S = M_next + 2 * G_next
        grid[t] = S
        
    palette = np.array([
        [10, 10, 15],     # M=0, G=0 (dark)
        [255, 50, 50],    # M=1, G=0 (red)
        [40, 20, 80],     # M=0, G=1 (dark indigo)
        [230, 50, 180],   # M=1, G=1 (violet-pink)
        [30, 80, 180],    # M=0, G=2 (blue)
        [50, 200, 255],   # M=1, G=2 (neon blue)
        [100, 180, 255],  # M=0, G=3 (light blue)
        [255, 240, 150]   # M=1, G=3 (gold)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_2(init_type, X=800, T=800):
    # Rule 2: Gravitational Wave Interferometer
    S = np.zeros(X, dtype=np.int32)
    
    # Place static deflectors at X//4 and 3*X//4
    lenses = [X//4, 3 * X // 4]
    
    if init_type == "single_seed":
        # Wave packet in the center
        for dx in range(-5, 6):
            S[X//2 + dx] = 1 # u_curr = 1, u_prev = 0
    else:
        # Random wave states (0..8) with 95% prob, lenses with 5% prob
        S = np.random.randint(0, 9, size=X, dtype=np.int32)
        lens_mask = np.random.rand(X) < 0.05
        S[lens_mask] = 9
        
    for l in lenses:
        S[l] = 9
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        mask_9 = (S == 9)
        u_curr = S % 3
        u_prev = S // 3
        
        W = np.where(S < 9, u_curr, 0)
        W_L = np.roll(W, 1)
        W_R = np.roll(W, -1)
        
        u_next = (W_L + W_R - u_prev + 3) % 3
        S_next = u_next + 3 * u_curr
        S_next[mask_9] = 9
        S = S_next
        grid[t] = S
        
    palette = np.array([
        [15, 15, 25],      # 0
        [0, 80, 100],      # 1 (dark teal)
        [0, 180, 140],     # 2 (green teal)
        [40, 30, 90],      # 3 (dark violet)
        [120, 40, 180],    # 4 (purple)
        [220, 60, 200],    # 5 (magenta)
        [180, 80, 0],      # 6 (burnt orange)
        [240, 150, 0],     # 7 (bright orange)
        [255, 220, 50],     # 8 (bright yellow)
        [255, 255, 255]    # 9 (white lens)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_3(init_type, X=800, T=800):
    # Rule 3: Event Horizon and Singularity
    S = np.zeros(X, dtype=np.int32)
    
    if init_type == "single_seed":
        # High-density core in the center to cause collapse
        S[X//2] = 4
        S[X//2 - 1] = 4
        S[X//2 + 1] = 4
        # Add some low density background matter
        bg = np.random.rand(X) < 0.10
        S[bg & (S == 0)] = 1
    else:
        # Random matter states 0..4 (no initial singularity 5)
        S = np.random.randint(0, 5, size=X, dtype=np.int32)
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        S_L = np.roll(S, 1)
        S_R = np.roll(S, -1)
        
        m1 = (S == 5)
        m2 = (~m1) & (S_L == 5) & (S_R == 5)
        m3 = (~m1) & (~m2) & (S_L == 5)
        m4 = (~m1) & (~m2) & (S_R == 5)
        m_other = ~(m1 | m2 | m3 | m4)
        
        S_next = np.copy(S)
        S_next[m1] = 5
        S_next[m2] = 5
        S_next[m3] = 0
        S_next[m4] = 0
        
        Total = S_L + S + S_R
        m5 = m_other & (Total >= 8)
        S_next[m5] = 5
        
        m_no_collapse = m_other & (Total < 8)
        cond_max = (S >= S_L) & (S >= S_R) & ~((S == S_L) & (S == S_R))
        cond_min = (S < S_L) & (S < S_R)
        
        inc = (S_L > 0).astype(np.int32) + (S_R > 0).astype(np.int32)
        val_max = np.minimum(4, S + inc)
        val_min = np.maximum(0, S - 1)
        
        m_max = m_no_collapse & cond_max
        m_min = m_no_collapse & cond_min
        
        S_next[m_max] = val_max[m_max]
        S_next[m_min] = val_min[m_min]
        
        S = S_next
        grid[t] = S
        
    palette = np.array([
        [5, 5, 5],        # 0 (black vacuum)
        [120, 20, 10],    # 1 (dark brick red)
        [200, 50, 20],    # 2 (orange-red)
        [255, 100, 30],   # 3 (bright orange)
        [255, 200, 50],   # 4 (gold-yellow)
        [180, 0, 255]     # 5 (neon purple singularity)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_4(init_type, X=800, T=800):
    # Rule 4: Gravitational Redshift (Time Dilation)
    S = np.zeros(X, dtype=np.int32)
    
    # Define potential wells
    Phi = np.zeros(X, dtype=np.int32)
    Phi[X//3 : X//3 + 40] = 3
    Phi[2*X//3 : 2*X//3 + 40] = 3
    
    if init_type == "single_seed":
        # Regular pulse of signals
        P = np.zeros(X, dtype=np.int32)
        P[np.arange(X) % 20 < 5] = 1
    else:
        P = (np.random.rand(X) < 0.50).astype(np.int32)
        Phi = np.random.randint(0, 4, size=X, dtype=np.int32)
        
    S = P + 2 * Phi
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        P = S % 2
        Phi = S // 2
        
        P_update = 1.0 - 0.25 * Phi
        r = np.random.rand(X)
        
        P_next = np.copy(P)
        update_mask = (r < P_update)
        P_next[update_mask] = np.roll(P, 1)[update_mask]
        
        S = P_next + 2 * Phi
        grid[t] = S
        
    palette = np.array([
        [10, 10, 12],     # P=0, Phi=0 (black)
        [50, 255, 100],   # P=1, Phi=0 (green)
        [10, 50, 60],     # P=0, Phi=1 (dark blue-green)
        [0, 230, 230],    # P=1, Phi=1 (cyan)
        [15, 30, 90],     # P=0, Phi=2 (dark blue)
        [50, 120, 255],   # P=1, Phi=2 (bright blue)
        [50, 15, 80],     # P=0, Phi=3 (dark purple)
        [255, 50, 150]    # P=1, Phi=3 (hot pink)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_5(init_type, X=800, T=800):
    # Rule 5: Frame Dragging (Lense-Thirring CA)
    S = np.zeros(X, dtype=np.int32)
    
    # Spinning masses
    S[X//3] = 4  # Clockwise (drag right)
    S[2*X//3] = 5 # Counterclockwise (drag left)
    
    if init_type == "single_seed":
        # Launch left/right moving particles as regular beams
        for x in range(X):
            if S[x] >= 3:
                continue
            if x < X//2 and x % 40 == 0:
                S[x] = 2  # Right-mover
            elif x > X//2 and x % 40 == 0:
                S[x] = 1  # Left-mover
    else:
        # Randomly initialize cells (keep static spinning masses)
        mask = (S < 3)
        r = np.random.rand(X)
        rand_states = np.zeros(X, dtype=np.int32)
        rand_states[r < 0.08] = 1 # Left-mover
        rand_states[(r >= 0.08) & (r < 0.16)] = 2 # Right-mover
        S[mask] = rand_states[mask]
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        is_4 = (S == 4)
        is_5 = (S == 5)
        
        D_R = (np.roll(is_4, 1) | is_4 | np.roll(is_4, -1))
        D_L = (np.roll(is_5, 1) | is_5 | np.roll(is_5, -1))
        
        is_1 = (S == 1)
        is_2 = (S == 2)
        
        RecvR = np.roll(is_2 & ~D_L, 1)
        RecvL = np.roll(is_1 & ~D_R, -1)
        
        StayR = is_2 & D_L
        StayL = is_1 & D_R
        
        S_next = np.zeros_like(S)
        mask_massive = (S >= 3)
        S_next[mask_massive] = S[mask_massive]
        
        mask_empty_or_matter = ~mask_massive
        cond_1 = RecvL | StayL
        cond_2 = RecvR | StayR
        
        S_next[mask_empty_or_matter & cond_1] = 1
        S_next[mask_empty_or_matter & cond_2] = 2
        
        S = S_next
        grid[t] = S
        
    palette = np.array([
        [12, 12, 16],     # 0 (space)
        [255, 80, 80],    # 1 (left-mover - red)
        [80, 255, 80],    # 2 (right-mover - green)
        [60, 100, 255],   # 3 (static mass - blue)
        [255, 180, 0],    # 4 (clockwise - orange)
        [255, 0, 180]     # 5 (counterclockwise - pink)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_6(init_type, X=800, T=800):
    # Rule 6: Schwarzschild Geodesics (Radial Fall)
    S = np.zeros(X, dtype=np.int32)
    
    # Black Hole structure in the center
    S[X//2] = 6  # Singularity
    S[X//2 - 25 : X//2 + 26] = 5  # Interior
    S[X//2] = 6  # Restore singularity
    S[X//2 - 26] = 4  # Horizon L
    S[X//2 + 26] = 4  # Horizon R
    
    if init_type == "single_seed":
        # Fast particles in regular spacing
        for pos in [50, 100, 150, 200, 250, 300]:
            S[pos] = 3  # Right fast
            S[X - pos] = 2  # Left fast
    else:
        # Random fast particles outside black hole
        bh_mask = (np.arange(X) >= X//2 - 26) & (np.arange(X) <= X//2 + 26)
        r = np.random.rand(X)
        rand_states = np.zeros(X, dtype=np.int32)
        rand_states[r < 0.05] = 2 # Left fast
        rand_states[(r >= 0.05) & (r < 0.10)] = 3 # Right fast
        S[~bh_mask] = rand_states[~bh_mask]
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        S_next = np.copy(S)
        S_L = np.roll(S, 1)
        S_R = np.roll(S, -1)
        
        # We can implement using logical arrays for speed
        mask_update = (S < 4)
        
        in_R = (S_L == 3)
        in_L = (S_R == 2)
        
        # S == 0 case:
        m_0 = (S == 0) & mask_update
        c_R_only = in_R & ~in_L
        c_L_only = in_L & ~in_R
        c_both = in_R & in_L
        
        S_next[m_0 & c_R_only] = np.where(S_R[m_0 & c_R_only] >= 4, 1, 3)
        S_next[m_0 & c_L_only] = np.where(S_L[m_0 & c_L_only] >= 4, 1, 2)
        S_next[m_0 & c_both] = 1
        
        # S == 3 case:
        m_3 = (S == 3) & mask_update
        S_next[m_3] = np.where(S_R[m_3] >= 4, 1, 0)
        
        # S == 2 case:
        m_2 = (S == 2) & mask_update
        S_next[m_2] = np.where(S_L[m_2] >= 4, 1, 0)
        
        # S == 1 case:
        m_1 = (S == 1) & mask_update
        S_next[m_1] = 0
        
        S = S_next
        grid[t] = S
        
    palette = np.array([
        [10, 10, 14],     # 0 (space)
        [255, 230, 50],   # 1 (slow - yellow)
        [0, 255, 220],    # 2 (left fast - cyan)
        [255, 50, 180],   # 3 (right fast - neon pink)
        [220, 160, 40],   # 4 (horizon - gold)
        [30, 40, 60],     # 5 (interior - dark blue-grey)
        [255, 255, 255]   # 6 (singularity - white)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_7(init_type, X=800, T=800):
    # Rule 7: FLRW Expansion & Redshift (Cosmological CA)
    S = np.zeros(X, dtype=np.int32)
    
    if init_type == "single_seed":
        # Launch right-movers and left-movers of max energy
        for pos in [20, 80, 140, 200]:
            S[pos] = 7  # Right-mover, energy 3
            S[X - pos] = 3 # Left-mover, energy 3
    else:
        r = np.random.rand(X)
        S[r < 0.05] = 7
        S[(r >= 0.05) & (r < 0.10)] = 3
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        S_L = np.roll(S, 1)
        S_R = np.roll(S, -1)
        
        r_R = np.random.rand(X)
        r_L = np.random.rand(X)
        
        cond_R = (S_L >= 4)
        W_inR = S_L % 4
        decay_R = (r_R >= 0.85)
        W_inR_next = np.where(decay_R, np.maximum(0, W_inR - 1), W_inR)
        
        cond_L = (S_R > 0) & (S_R < 4)
        W_inL = S_R
        decay_L = (r_L >= 0.85)
        W_inL_next = np.where(decay_L, np.maximum(0, W_inL - 1), W_inL)
        
        S = np.where(cond_R, W_inR_next + 4, np.where(cond_L, W_inL_next, 0))
        grid[t] = S
        
    palette = np.array([
        [5, 5, 10],       # 0 (black vacuum)
        [120, 20, 40],    # 1 (crimson, energy 1 left-mover)
        [200, 40, 50],    # 2 (red, energy 2 left-mover)
        [255, 70, 70],    # 3 (bright red, energy 3 left-mover)
        [20, 30, 45],     # 4 (faded blue, energy 0 right-mover)
        [0, 100, 150],    # 5 (dark cyan, energy 1 right-mover)
        [0, 160, 255],    # 6 (bright blue, energy 2 right-mover)
        [180, 230, 255]   # 7 (electric blue, energy 3 right-mover)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_8(init_type, X=800, T=800):
    # Rule 8: Gravitational Collapse (Jeans Instability)
    S = np.zeros(X, dtype=np.int32)
    
    if init_type == "single_seed":
        # Smooth density dome
        x_indices = np.arange(X)
        dist = np.abs(x_indices - X//2)
        S = np.maximum(0, 8 - dist // 10)
    else:
        S = np.random.randint(0, 5, size=X, dtype=np.int32)
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        M = np.where(S == 11, 11, S)
        
        M_R1 = np.roll(M, -1)
        M_R2 = np.roll(M, -2)
        M_L1 = np.roll(M, 1)
        M_L2 = np.roll(M, 2)
        
        F_net = (M_R1 + 0.25 * M_R2) - (M_L1 + 0.25 * M_L2)
        
        is_mid = (S > 0) & (S < 11)
        OutR = (F_net > 2) & is_mid
        OutL = (F_net < -2) & is_mid
        
        OutR_int = OutR.astype(np.int32)
        OutL_int = OutL.astype(np.int32)
        
        S_new = S - OutR_int - OutL_int + np.roll(OutR_int, 1) + np.roll(OutL_int, -1)
        S = np.where(S == 11, 11, np.clip(S_new, 0, 11))
        grid[t] = S
        
    palette = np.array([
        [10, 10, 20],     # 0
        [30, 15, 60],     # 1
        [50, 20, 100],    # 2
        [80, 25, 140],    # 3
        [120, 30, 160],   # 4
        [160, 35, 160],   # 5
        [200, 40, 140],   # 6
        [220, 50, 100],   # 7
        [240, 70, 70],    # 8
        [255, 100, 50],   # 9
        [255, 150, 50],   # 10
        [255, 255, 200]   # 11 (dense yellow core)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_9(init_type, X=800, T=800):
    # Rule 9: Causal Light Cones (Penrose Horizon CA)
    Tilt = np.zeros(X, dtype=np.int32)
    Tilt[X//2 :] = 1  # Tilted region on the right
    
    if init_type == "single_seed":
        Sig = np.zeros(X, dtype=np.int32)
        Sig[X//4] = 3
        Sig[3*X//4] = 3
    else:
        Sig = np.random.randint(0, 4, size=X, dtype=np.int32)
        
    S = Sig + 4 * Tilt
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        Sig = S % 4
        Tilt = S // 4
        
        Sig_L = np.roll(Sig, 1)
        Tilt_L = np.roll(Tilt, 1)
        Sig_R = np.roll(Sig, -1)
        
        Sig_inR = np.where(Tilt_L == 0, Sig_L, 0)
        Sig_inL = Sig_R
        
        Sig_next = np.where(Tilt == 1, Sig_inL, np.maximum(Sig_inR, Sig_inL))
        S = Sig_next + 4 * Tilt
        grid[t] = S
        
    palette = np.array([
        [5, 5, 8],        # Sig=0, Tilt=0 (black)
        [20, 40, 120],    # Sig=1, Tilt=0 (deep blue)
        [40, 90, 200],    # Sig=2, Tilt=0 (medium blue)
        [0, 230, 255],    # Sig=3, Tilt=0 (cyan)
        [40, 10, 60],     # Sig=0, Tilt=1 (deep purple)
        [100, 30, 140],   # Sig=1, Tilt=1 (medium purple)
        [180, 50, 180],   # Sig=2, Tilt=1 (magenta)
        [255, 180, 0]     # Sig=3, Tilt=1 (yellow-orange)
    ], dtype=np.uint8)
    
    return palette[grid]

def run_ca_rule_10(init_type, X=800, T=800):
    # Rule 10: Einstein-Rosen Bridge (Wormhole CA)
    S = np.zeros(X, dtype=np.int32)
    
    x_A = X // 3
    x_B = 2 * X // 3
    S[x_A] = 4  # Mouth A
    S[x_B] = 5  # Mouth B
    S[0] = 6    # Left static boundary
    S[X - 1] = 6 # Right static boundary
    
    if init_type == "single_seed":
        # Launch particles
        S[X//6] = 2  # Right-mover from left
        S[X//2] = 2  # Right-mover from center
        S[5*X//6] = 1 # Left-mover from right
    else:
        # Random particles (keep mouths and boundaries static)
        mask = (S == 0)
        r = np.random.rand(X)
        rand_states = np.zeros(X, dtype=np.int32)
        rand_states[r < 0.05] = 1  # Left-mover
        rand_states[(r >= 0.05) & (r < 0.10)] = 2  # Right-mover
        S[mask] = rand_states[mask]
        
    grid = np.zeros((T, X), dtype=np.int32)
    grid[0] = S
    
    for t in range(1, T):
        S_L = np.roll(S, 1)
        S_R = np.roll(S, -1)
        
        in_R = (S_L == 2)
        in_L = (S_R == 1)
        
        # Wormhole connectivity overrides:
        in_L[x_A - 1] = (S[(x_B + 1) % X] == 1)
        in_R[x_A + 1] = (S[(x_B - 1) % X] == 2)
        in_L[x_B - 1] = (S[(x_A + 1) % X] == 1)
        in_R[x_B + 1] = (S[(x_A - 1) % X] == 2)
        
        S_next = np.zeros_like(S)
        mask_static = (S >= 4)
        S_next[mask_static] = S[mask_static]
        
        mask_update = ~mask_static
        cond_2 = in_R & ~in_L
        cond_1 = in_L & ~in_R
        cond_3 = in_R & in_L
        
        S_next[mask_update & cond_2] = 2
        S_next[mask_update & cond_1] = 1
        S_next[mask_update & cond_3] = 3
        
        S = S_next
        grid[t] = S
        
    palette = np.array([
        [8, 8, 12],       # 0 (space)
        [50, 255, 50],    # 1 (left-mover - green)
        [255, 50, 255],   # 2 (right-mover - magenta)
        [255, 255, 0],    # 3 (collision - yellow)
        [0, 240, 255],    # 4 (Mouth A - cyan)
        [255, 120, 0],    # 5 (Mouth B - orange)
        [60, 60, 60],     # 6 (boundary)
        [70, 70, 70],     # 7
        [80, 80, 80],     # 8
        [90, 90, 90]      # 9
    ], dtype=np.uint8)
    
    return palette[grid]

def main():
    output_dir = "generations/loop_12/output"
    os.makedirs(output_dir, exist_ok=True)
    
    rules = {
        1: run_ca_rule_1,
        2: run_ca_rule_2,
        3: run_ca_rule_3,
        4: run_ca_rule_4,
        5: run_ca_rule_5,
        6: run_ca_rule_6,
        7: run_ca_rule_7,
        8: run_ca_rule_8,
        9: run_ca_rule_9,
        10: run_ca_rule_10
    }
    
    for rule_num, sim_func in rules.items():
        for init_type in ["single_seed", "random"]:
            filename = f"rule_{rule_num:02d}_{init_type}.png"
            filepath = os.path.join(output_dir, filename)
            print(f"Simulating Rule {rule_num} ({init_type})...")
            img_data = sim_func(init_type)
            img = Image.fromarray(img_data)
            img.save(filepath)
            print(f"Saved {filepath} (Resolution: {img.size[0]}x{img.size[1]})")

if __name__ == "__main__":
    main()
