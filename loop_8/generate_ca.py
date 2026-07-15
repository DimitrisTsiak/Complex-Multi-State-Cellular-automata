import os
import numpy as np
from PIL import Image

def main():
    # Make sure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    W = 800
    T = 800
    
    # Define palettes for each rule
    # Palettes are lists of RGB tuples mapping from state 0 to N-1
    palettes = {
        1: [
            (10, 10, 20),     # 0: Vacuum (dark navy)
            (0, 220, 255),    # 1: Right-mover + (cyan)
            (255, 0, 128),    # 2: Left-mover + (pink)
            (0, 100, 255),    # 3: Right-mover - (blue)
            (255, 0, 0),      # 4: Left-mover - (red)
            (255, 200, 0),    # 5: Superposition +/+ (yellow)
            (128, 0, 255),    # 6: Superposition -/- (purple)
            (0, 255, 128),    # 7: Superposition +/- (green)
            (255, 128, 0)     # 8: Superposition -/+ (orange)
        ],
        2: [
            (15, 10, 15),     # 0: Vacuum (dark purple)
            (0, 255, 100),    # 1: Right-mover + (emerald)
            (0, 150, 255),    # 2: Left-mover + (sky blue)
            (100, 255, 0),    # 3: Right-mover - (lime)
            (0, 50, 200),     # 4: Left-mover - (deep blue)
            (120, 120, 120),  # 5: Potential barrier (gray)
            (220, 220, 220),  # 6: High potential wall (white-gray)
            (255, 255, 0)     # 7: Superposition (yellow)
        ],
        3: [
            (5, 5, 5),        # 0: (0,0) (black)
            (0, 255, 255),    # 1: (1,0) (cyan)
            (0, 128, 255),    # 2: (-1,0) (blue)
            (255, 0, 255),    # 3: (0,1) (magenta)
            (255, 0, 128),    # 4: (0,-1) (rose)
            (255, 255, 0),    # 5: (1,1) (yellow)
            (128, 0, 255),    # 6: (-1,-1) (purple)
            (255, 128, 0),    # 7: (1,-1) (orange)
            (0, 255, 0)       # 8: (-1,1) (green)
        ],
        4: [
            (10, 10, 10),     # 0: Vacuum (black)
            (0, 255, 200),    # 1: Coherent right + (mint)
            (200, 0, 255),    # 2: Coherent left + (purple)
            (0, 150, 255),    # 3: Coherent right - (blue)
            (255, 0, 100),    # 4: Coherent left - (hot pink)
            (255, 100, 0)     # 5: Noise (orange)
        ],
        5: [
            (20, 10, 30),     # 0: Vacuum (dark indigo)
            (0, 128, 255),    # 1: Wave +1 (blue)
            (255, 0, 128),    # 2: Wave -1 (magenta)
            (255, 255, 255),  # 3: Particle alone (white)
            (0, 255, 255),    # 4: Particle on wave +1 (cyan)
            (255, 255, 0)     # 5: Particle on wave -1 (yellow)
        ],
        6: [
            (10, 15, 20),     # 0: Quiescent (dark teal)
            (50, 100, 150),   # 1: Low amplitude (slate blue)
            (0, 200, 100),    # 2: Moderate amplitude (emerald green)
            (255, 165, 0),    # 3: High amplitude (orange)
            (255, 0, 0)       # 4: Soliton core (red)
        ],
        7: [
            (15, 15, 15),     # 0: Neutral (black)
            (100, 200, 255),  # 1: Charge +1/3 (light blue)
            (50, 150, 255),   # 2: Charge +2/3 (medium blue)
            (0, 80, 255),     # 3: Charge +1 (deep blue)
            (255, 200, 100),  # 4: Charge -1/3 (peach)
            (255, 150, 50),   # 5: Charge -2/3 (orange)
            (255, 80, 0)      # 6: Charge -1 (red-orange)
        ],
        8: [
            (10, 10, 15),     # 0: Vacuum (dark navy)
            (0, 255, 128),    # 1: Right 0 (spring green)
            (0, 255, 255),    # 2: Right pi (cyan)
            (255, 0, 255),    # 3: Left 0 (magenta)
            (255, 128, 0),    # 4: Left pi (orange)
            (255, 255, 255),  # 5: Beam splitter (white)
            (128, 128, 128),  # 6: Mirror (gray)
            (255, 255, 0)     # 7: Phase shifter (yellow)
        ],
        9: [
            (5, 10, 15),      # 0: Vacuum (dark)
            (255, 0, 100),    # 1: Real +1 (rose)
            (0, 200, 255),    # 2: Real -1 (cyan)
            (255, 200, 0),    # 3: Imag +1 (yellow)
            (150, 50, 255)    # 4: Imag -1 (violet)
        ],
        10: [
            (10, 10, 10),     # 0: Ground atom (dark gray)
            (255, 0, 0),      # 1: Excited atom (bright red)
            (0, 255, 0),      # 2: Right-mover + (green)
            (0, 255, 255),    # 3: Right-mover - (cyan)
            (255, 0, 255),    # 4: Left-mover + (magenta)
            (255, 255, 0)     # 5: Left-mover - (yellow)
        ]
    }
    
    # Define the transition steps for each rule
    def step_rule1(S):
        # Hadamard Walk
        psi_R = np.zeros(W, dtype=np.int8)
        psi_L = np.zeros(W, dtype=np.int8)
        
        psi_R[S == 1] = 1
        psi_R[S == 3] = -1
        psi_R[S == 5] = 1
        psi_R[S == 6] = -1
        psi_R[S == 7] = 1
        psi_R[S == 8] = -1
        
        psi_L[S == 2] = 1
        psi_L[S == 4] = -1
        psi_L[S == 5] = 1
        psi_L[S == 6] = -1
        psi_L[S == 7] = -1
        psi_L[S == 8] = 1
        
        a = np.roll(psi_R, 1)
        b = np.roll(psi_L, -1)
        
        R_new = np.sign(a + b)
        L_new = np.sign(a - b)
        
        S_new = np.zeros(W, dtype=np.int8)
        S_new[(R_new == 1) & (L_new == 0)] = 1
        S_new[(R_new == 0) & (L_new == 1)] = 2
        S_new[(R_new == -1) & (L_new == 0)] = 3
        S_new[(R_new == 0) & (L_new == -1)] = 4
        S_new[(R_new == 1) & (L_new == 1)] = 5
        S_new[(R_new == -1) & (L_new == -1)] = 6
        S_new[(R_new == 1) & (L_new == -1)] = 7
        S_new[(R_new == -1) & (L_new == 1)] = 8
        return S_new

    def step_rule2(S):
        # Tunneling
        psi_R = np.zeros(W, dtype=np.int8)
        psi_R[(S == 1) | (S == 7)] = 1
        psi_R[S == 3] = -1
        
        psi_L = np.zeros(W, dtype=np.int8)
        psi_L[(S == 2) | (S == 7)] = 1
        psi_L[S == 4] = -1
        
        S_left = np.roll(S, 1)
        cond_6 = (S_left == 6)
        cond_5 = (S_left == 5)
        cond_other = ~(cond_6 | cond_5)
        
        a = np.zeros(W, dtype=np.int8)
        a[cond_6] = -psi_L[cond_6]
        a[cond_5] = np.roll(psi_R, 2)[cond_5] - psi_L[cond_5]
        a[cond_other] = np.roll(psi_R, 1)[cond_other]
        
        S_right = np.roll(S, -1)
        cond_6_b = (S_right == 6)
        cond_5_b = (S_right == 5)
        cond_other_b = ~(cond_6_b | cond_5_b)
        
        b = np.zeros(W, dtype=np.int8)
        b[cond_6_b] = -psi_R[cond_6_b]
        b[cond_5_b] = np.roll(psi_L, -2)[cond_5_b] - psi_R[cond_5_b]
        b[cond_other_b] = np.roll(psi_L, -1)[cond_other_b]
        
        a_prime = np.clip(a, -1, 1)
        b_prime = np.clip(b, -1, 1)
        
        S_new = np.zeros(W, dtype=np.int8)
        static_mask = (S == 5) | (S == 6)
        S_new[static_mask] = S[static_mask]
        
        non_static = ~static_mask
        S_ns = np.zeros(W, dtype=np.int8)
        S_ns[(a_prime == 1) & (b_prime == 0)] = 1
        S_ns[(a_prime == -1) & (b_prime == 0)] = 3
        S_ns[(a_prime == 0) & (b_prime == 1)] = 2
        S_ns[(a_prime == 0) & (b_prime == -1)] = 4
        S_ns[(a_prime == 1) & (b_prime == 1)] = 7
        
        S_new[non_static] = S_ns[non_static]
        return S_new

    def step_rule3(S):
        # Wave Equation
        U = np.zeros(W, dtype=np.int8)
        V = np.zeros(W, dtype=np.int8)
        
        U[S == 1] = 1
        U[S == 2] = -1
        U[S == 5] = 1
        U[S == 6] = -1
        U[S == 7] = 1
        U[S == 8] = -1
        
        V[S == 3] = 1
        V[S == 4] = -1
        V[S == 5] = 1
        V[S == 6] = -1
        V[S == 7] = -1
        V[S == 8] = 1
        
        Delta_U = np.roll(U, 1) - 2 * U + np.roll(U, -1)
        V_new = np.clip(V + Delta_U, -1, 1)
        U_new = np.clip(U + V_new, -1, 1)
        
        S_new = np.zeros(W, dtype=np.int8)
        S_new[(U_new == 1) & (V_new == 0)] = 1
        S_new[(U_new == -1) & (V_new == 0)] = 2
        S_new[(U_new == 0) & (V_new == 1)] = 3
        S_new[(U_new == 0) & (V_new == -1)] = 4
        S_new[(U_new == 1) & (V_new == 1)] = 5
        S_new[(U_new == -1) & (V_new == -1)] = 6
        S_new[(U_new == 1) & (V_new == -1)] = 7
        S_new[(U_new == -1) & (V_new == 1)] = 8
        return S_new

    def step_rule4(S):
        # Decoherence
        R_in = np.zeros(W, dtype=np.int8)
        S_left = np.roll(S, 1)
        R_in[S_left == 1] = 1
        R_in[S_left == 3] = -1
        
        L_in = np.zeros(W, dtype=np.int8)
        S_right = np.roll(S, -1)
        L_in[S_right == 2] = 1
        L_in[S_right == 4] = -1
        
        N_flag = (S_left == 5) | (S_right == 5) | (S == 5)
        
        S_new = np.zeros(W, dtype=np.int8)
        
        cond_decohere = N_flag & ((R_in != 0) | (L_in != 0) | (S == 5))
        S_new[cond_decohere] = 5
        
        coherent = ~N_flag
        case_both = coherent & (R_in != 0) & (L_in != 0)
        S_new[case_both & (R_in == L_in) & (R_in == 1)] = 1
        S_new[case_both & (R_in == L_in) & (R_in == -1)] = 4
        
        case_R = coherent & (R_in != 0) & (L_in == 0)
        S_new[case_R & (R_in == 1)] = 1
        S_new[case_R & (R_in == -1)] = 3
        
        case_L = coherent & (L_in != 0) & (R_in == 0)
        S_new[case_L & (L_in == 1)] = 2
        S_new[case_L & (L_in == -1)] = 4
        return S_new

    def step_rule5(S):
        # Bohmian
        psi_t = np.zeros(W, dtype=np.int8)
        psi_t[(S == 1) | (S == 4)] = 1
        psi_t[(S == 2) | (S == 5)] = -1
        
        psi_new = np.sign(np.roll(psi_t, 1) + np.roll(psi_t, -1))
        P_t = (S == 3) | (S == 4) | (S == 5)
        
        P_new = np.zeros(W, dtype=np.int8)
        active_p = np.where(P_t)[0]
        for y in active_p:
            M_L = abs(psi_new[(y - 1) % W])
            M_C = abs(psi_new[y])
            M_R = abs(psi_new[(y + 1) % W])
            max_val = max(M_L, M_C, M_R)
            if M_C == max_val:
                dest = y
            elif M_R == max_val:
                dest = (y + 1) % W
            else:
                dest = (y - 1) % W
            P_new[dest] = 1
            
        S_new = np.zeros(W, dtype=np.int8)
        cond_no_p = (P_new == 0)
        S_new[cond_no_p & (psi_new == 1)] = 1
        S_new[cond_no_p & (psi_new == -1)] = 2
        
        cond_p = (P_new == 1)
        S_new[cond_p & (psi_new == 0)] = 3
        S_new[cond_p & (psi_new == 1)] = 4
        S_new[cond_p & (psi_new == -1)] = 5
        return S_new

    def step_rule6(S):
        # NLSE
        A = np.roll(S, 1) + np.roll(S, -1)
        S_new = np.zeros(W, dtype=np.int8)
        
        low_energy = (S <= 1)
        high_energy = (S >= 2)
        
        S_new[low_energy] = np.floor(A[low_energy] / 3.0 + 0.5).astype(np.int8)
        
        S_new[high_energy & (A >= 3)] = np.minimum(4, S[high_energy & (A >= 3)] + 1)
        S_new[high_energy & (A < 3)] = S[high_energy & (A < 3)] - 1
        return S_new

    def step_rule7(S):
        # Fractional Edge States
        q_R = np.zeros(W, dtype=np.int8)
        S_left = np.roll(S, 1)
        q_R[S_left == 1] = 1
        q_R[S_left == 2] = 2
        q_R[S_left == 3] = 3
        
        q_L = np.zeros(W, dtype=np.int8)
        S_right = np.roll(S, -1)
        q_L[S_right == 4] = -1
        q_L[S_right == 5] = -2
        q_L[S_right == 6] = -3
        
        Q = q_R + q_L
        
        S_new = np.zeros(W, dtype=np.int8)
        S_new[(Q > 0) & (Q == 1)] = 1
        S_new[(Q > 0) & (Q == 2)] = 2
        S_new[(Q > 0) & (Q >= 3)] = 3
        
        S_new[(Q < 0) & (Q == -1)] = 4
        S_new[(Q < 0) & (Q == -2)] = 5
        S_new[(Q < 0) & (Q <= -3)] = 6
        return S_new

    def step_rule8(S):
        # Beam Splitter
        a = np.zeros(W, dtype=np.int8)
        b = np.zeros(W, dtype=np.int8)
        
        S_left = np.roll(S, 1)
        S_left2 = np.roll(S, 2)
        S_right = np.roll(S, -1)
        S_right2 = np.roll(S, -2)
        
        cond_a_1 = (S_left == 1)
        cond_a_2 = (S_left == 2)
        cond_a_3 = (S_left == 7) & (S_left2 == 1)
        cond_a_4 = (S_left == 7) & (S_left2 == 2)
        cond_a_5 = (S_left == 6) & (S == 3)
        cond_a_6 = (S_left == 6) & (S == 4)
        
        a[cond_a_1] = 1
        a[cond_a_2] = -1
        a[cond_a_3] = -1
        a[cond_a_4] = 1
        a[cond_a_5] = -1
        a[cond_a_6] = 1
        
        cond_b_1 = (S_right == 3)
        cond_b_2 = (S_right == 4)
        cond_b_3 = (S_right == 7) & (S_right2 == 3)
        cond_b_4 = (S_right == 7) & (S_right2 == 4)
        cond_b_5 = (S_right == 6) & (S == 1)
        cond_b_6 = (S_right == 6) & (S == 2)
        
        b[cond_b_1] = 1
        b[cond_b_2] = -1
        b[cond_b_3] = -1
        b[cond_b_4] = 1
        b[cond_b_5] = -1
        b[cond_b_6] = 1
        
        S_new = np.zeros(W, dtype=np.int8)
        static_mask = (S == 5) | (S == 6) | (S == 7)
        S_new[static_mask] = S[static_mask]
        
        non_static = ~static_mask
        S_ns = np.zeros(W, dtype=np.int8)
        
        cond_both = (a != 0) & (b != 0)
        S_ns[cond_both & (a == b) & (a == 1)] = 1
        S_ns[cond_both & (a == b) & (a == -1)] = 2
        
        cond_a_only = (a != 0) & (b == 0)
        S_ns[cond_a_only & (a == 1)] = 1
        S_ns[cond_a_only & (a == -1)] = 2
        
        cond_b_only = (b != 0) & (a == 0)
        S_ns[cond_b_only & (b == 1)] = 3
        S_ns[cond_b_only & (b == -1)] = 4
        
        S_new[non_static] = S_ns[non_static]
        return S_new

    def step_rule9(S):
        # Schrödinger
        R = np.zeros(W, dtype=np.int8)
        I = np.zeros(W, dtype=np.int8)
        
        R[S == 1] = 1
        R[S == 2] = -1
        I[S == 3] = 1
        I[S == 4] = -1
        
        Delta_R = np.roll(R, 1) - 2 * R + np.roll(R, -1)
        Delta_I = np.roll(I, 1) - 2 * I + np.roll(I, -1)
        
        R_new = np.clip(R - Delta_I, -1, 1)
        I_new = np.clip(I + Delta_R, -1, 1)
        
        S_new = np.zeros(W, dtype=np.int8)
        cond_r_dom = np.abs(R_new) >= np.abs(I_new)
        cond_i_dom = np.abs(R_new) < np.abs(I_new)
        
        S_new[cond_r_dom & (R_new == 1)] = 1
        S_new[cond_r_dom & (R_new == -1)] = 2
        S_new[cond_i_dom & (I_new == 1)] = 3
        S_new[cond_i_dom & (I_new == -1)] = 4
        return S_new

    def step_rule10(S):
        # Rabi
        W_R = np.zeros(W, dtype=np.int8)
        S_left = np.roll(S, 1)
        W_R[S_left == 2] = 1
        W_R[S_left == 3] = -1
        
        W_L = np.zeros(W, dtype=np.int8)
        S_right = np.roll(S, -1)
        W_L[S_right == 4] = 1
        W_L[S_right == 5] = -1
        
        S_new = np.zeros(W, dtype=np.int8)
        
        cond_0 = (S == 0)
        S_new[cond_0 & ((W_R != 0) | (W_L != 0))] = 1
        
        cond_1 = (S == 1)
        S_new[cond_1 & (W_R != 0)] = 3
        S_new[cond_1 & (W_R == 0) & (W_L != 0)] = 5
        
        cond_23 = (S == 2) | (S == 3)
        cond_23_prop = cond_23 & ((S_left == 2) | (S_left == 3))
        S_new[cond_23_prop] = S_left[cond_23_prop]
        
        cond_45 = (S == 4) | (S == 5)
        cond_45_prop = cond_45 & ((S_right == 4) | (S_right == 5))
        S_new[cond_45_prop] = S_right[cond_45_prop]
        return S_new

    rules = {
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

    # Execute simulation and save results
    for r_idx in range(1, 11):
        step_func = rules[r_idx]
        palette = palettes[r_idx]
        N_states = len(palette)
        
        for init_type in ['single', 'random']:
            S = np.zeros(W, dtype=np.int8)
            
            # Setup initial state
            if init_type == 'single':
                if r_idx == 1:
                    S[W // 2] = 5
                elif r_idx == 2:
                    S[W // 4] = 1
                    S[W // 2 - 1 : W // 2 + 2] = 5
                    S[3 * W // 4 - 1 : 3 * W // 4 + 2] = 6
                elif r_idx == 3:
                    S[W // 2] = 1
                elif r_idx == 4:
                    S[W // 4] = 1
                    S[3 * W // 4] = 2
                    S[W // 2 : W // 2 + 30] = 5
                elif r_idx == 5:
                    S[W // 2 - 20 : W // 2 + 21] = 1
                    S[W // 2] = 4
                elif r_idx == 6:
                    S[W // 2] = 4
                    S[W // 2 - 1] = 3
                    S[W // 2 + 1] = 3
                    S[W // 2 - 2] = 2
                    S[W // 2 + 2] = 2
                elif r_idx == 7:
                    S[W // 4] = 3
                    S[W // 2] = 1
                    S[3 * W // 4] = 5
                elif r_idx == 8:
                    S[W // 8] = 6
                    S[W // 2] = 7
                    S[3 * W // 4] = 6
                    S[W // 4] = 1
                elif r_idx == 9:
                    S[W // 2] = 1
                elif r_idx == 10:
                    S[:200] = 2
                    S[600:] = 4
            else:
                # Random initialization
                np.random.seed(42 + r_idx)  # Deterministic seed for reproducible beauty
                if r_idx == 2:
                    # Place a few barriers/walls, and rest waves
                    probs = [0.80, 0.08, 0.02, 0.02, 0.02, 0.03, 0.02, 0.01]
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
                elif r_idx == 4:
                    # Place some noise and some coherent states
                    probs = [0.80, 0.04, 0.04, 0.04, 0.04, 0.04]
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
                elif r_idx == 5:
                    # Place wave and particle states
                    probs = [0.85, 0.05, 0.05, 0.02, 0.02, 0.01]
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
                elif r_idx == 8:
                    # Place mirrors, phase shifters, beam splitters, and waves
                    probs = [0.80, 0.04, 0.04, 0.04, 0.04, 0.01, 0.02, 0.01]
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
                elif r_idx == 10:
                    # Rabi has state 0 as background, 1 as excited, 2-5 as waves
                    probs = [0.70, 0.10, 0.05, 0.05, 0.05, 0.05]
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
                else:
                    # Generic random with high vacuum probability
                    probs = [0.85] + [0.15 / (N_states - 1)] * (N_states - 1)
                    S = np.random.choice(np.arange(N_states), size=W, p=probs).astype(np.int8)
            
            # Run simulation
            history = np.zeros((T, W), dtype=np.int8)
            history[0] = S
            
            for t in range(1, T):
                S = step_func(S)
                history[t] = S
                
            # Map to RGB
            rgb_data = np.zeros((T, W, 3), dtype=np.uint8)
            for state_val, color in enumerate(palette):
                mask = (history == state_val)
                rgb_data[mask] = color
                
            # Save as PNG
            img = Image.fromarray(rgb_data, 'RGB')
            filename = f"rule{r_idx}_{init_type}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath)
            print(f"Saved {filename} to {filepath}")

    print("All 20 CA simulation PNGs generated successfully.")

if __name__ == '__main__':
    main()
