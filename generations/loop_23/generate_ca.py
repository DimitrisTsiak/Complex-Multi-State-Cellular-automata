import os
import numpy as np
from PIL import Image

# Output directory
OUTPUT_DIR = "C:/programming/complex_cellular_automata/generations/loop_23/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# Transition Functions
# ---------------------------------------------------------

def step_rule_1(S):
    # Rule 1: Antigenic Drift Competition (6 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N_A = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_B = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    
    p_A = 1.0 - (1.0 - 0.60)**N_A
    p_B = 1.0 - (1.0 - 0.50)**N_B
    
    r_expose_A = np.random.rand(width) < p_A
    r_expose_B = np.random.rand(width) < p_B
    
    only_A = r_expose_A & ~r_expose_B
    only_B = r_expose_B & ~r_expose_A
    both_AB = r_expose_A & r_expose_B
    
    r_choice = np.random.rand(width)
    cond_to_1 = (only_A & (r_choice < 0.90)) | (only_B & (r_choice < 0.10)) | (both_AB & (r_choice < 0.50))
    cond_to_2 = (only_A & (r_choice >= 0.90)) | (only_B & (r_choice >= 0.10)) | (both_AB & (r_choice >= 0.50))
    
    # State 0 transitions
    is_zero = (S == 0)
    S_next[is_zero & cond_to_1] = 1
    S_next[is_zero & cond_to_2] = 2
    
    # State 1 transitions
    is_one = (S == 1)
    recover_A = np.random.rand(width) < 0.70
    S_next[is_one & recover_A] = 3
    
    # State 2 transitions
    is_two = (S == 2)
    recover_B = np.random.rand(width) < 0.70
    S_next[is_two & recover_B] = 4
    
    # State 3 transitions
    is_three = (S == 3)
    p_B_prime = 1.0 - 0.75**N_B
    infect_B_prime = np.random.rand(width) < p_B_prime
    decay_RA = np.random.rand(width) < 0.15
    
    r_choice_RA = np.random.rand(width)
    to_IA_from_RA = infect_B_prime & (r_choice_RA < 0.10)
    to_IB_from_RA = infect_B_prime & (r_choice_RA >= 0.10)
    to_S_from_RA = ~infect_B_prime & decay_RA
    
    S_next[is_three & to_IA_from_RA] = 1
    S_next[is_three & to_IB_from_RA] = 2
    S_next[is_three & to_S_from_RA] = 0
    
    # State 4 transitions
    is_four = (S == 4)
    p_A_prime = 1.0 - 0.70**N_A
    infect_A_prime = np.random.rand(width) < p_A_prime
    decay_RB = np.random.rand(width) < 0.15
    
    r_choice_RB = np.random.rand(width)
    to_IA_from_RB = infect_A_prime & (r_choice_RB < 0.90)
    to_IB_from_RB = infect_A_prime & (r_choice_RB >= 0.90)
    to_S_from_RB = ~infect_A_prime & decay_RB
    
    S_next[is_four & to_IA_from_RB] = 1
    S_next[is_four & to_IB_from_RB] = 2
    S_next[is_four & to_S_from_RB] = 0
    
    # State 5 transitions
    is_five = (S == 5)
    r_decay_R_AB = np.random.rand(width)
    to_RA_from_RAB = r_decay_R_AB < 0.05
    to_RB_from_RAB = (r_decay_R_AB >= 0.05) & (r_decay_R_AB < 0.10)
    
    S_next[is_five & to_RA_from_RAB] = 3
    S_next[is_five & to_RB_from_RAB] = 4
    
    return S_next

def step_rule_2(S):
    # Rule 2: Hyper-Mutational Cascade (Symmetric Error Catastrophe) (6 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N1 = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N2 = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N3 = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)
    
    p1 = 1.0 - (1.0 - 0.25)**N1
    p2 = 1.0 - (1.0 - 0.50)**N2
    p3 = 1.0 - (1.0 - 0.75)**N3
    
    P_inf = 1.0 - (1.0 - p1) * (1.0 - p2) * (1.0 - p3)
    is_infected = (S == 0) & (np.random.rand(width) < P_inf)
    
    # Select infecting strain
    sum_p = p1 + p2 + p3
    sum_p_safe = np.where(sum_p == 0, 1.0, sum_p)
    w1 = p1 / sum_p_safe
    w2 = p2 / sum_p_safe
    
    r_strain = np.random.rand(width)
    chosen_k = np.zeros(width, dtype=np.uint8)
    chosen_k[r_strain < w1] = 1
    chosen_k[(r_strain >= w1) & (r_strain < w1 + w2)] = 2
    chosen_k[r_strain >= w1 + w2] = 3
    
    # Mutational cascade
    r_mut = np.random.rand(width)
    mutate = r_mut < 0.20
    
    target_state = np.zeros(width, dtype=np.uint8)
    target_state[mutate] = np.minimum(chosen_k[mutate] + 1, 4)
    target_state[~mutate] = chosen_k[~mutate]
    
    # State 0 transitions
    S_next[is_infected] = target_state[is_infected]
    
    # State 1 transitions
    is_one = (S == 1)
    r_v1 = np.random.rand(width)
    to_v2 = r_v1 < 0.10
    to_d_from_v1 = (r_v1 >= 0.10) & (r_v1 < 0.20)
    S_next[is_one & to_v2] = 2
    S_next[is_one & to_d_from_v1] = 4
    
    # State 2 transitions
    is_two = (S == 2)
    r_v2 = np.random.rand(width)
    to_v3 = r_v2 < 0.15
    to_d_from_v2 = (r_v2 >= 0.15) & (r_v2 < 0.45)
    S_next[is_two & to_v3] = 3
    S_next[is_two & to_d_from_v2] = 4
    
    # State 3 transitions
    is_three = (S == 3)
    to_d_from_v3 = np.random.rand(width) < 0.70
    S_next[is_three & to_d_from_v3] = 4
    
    # State 4 transitions
    is_four = (S == 4)
    to_imm_from_d = np.random.rand(width) < 0.40
    S_next[is_four & to_imm_from_d] = 5
    
    # State 5 transitions
    is_five = (S == 5)
    to_healthy_from_r = np.random.rand(width) < 0.20
    S_next[is_five & to_healthy_from_r] = 0
    
    return S_next

def step_rule_3(S):
    # Rule 3: Quorum-Sensing Pathogen Suppression (5 states)
    # Radius r = 2
    width = S.shape[0]
    S_L2 = np.roll(S, 2)
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    S_next = np.copy(S)
    
    N_A = ((S_L2 == 2).astype(int) + (S_L1 == 2).astype(int) + 
           (S_R1 == 2).astype(int) + (S_R2 == 2).astype(int))
    N_M = ((S_L2 == 3).astype(int) + (S_L1 == 3).astype(int) + 
           (S_R1 == 3).astype(int) + (S_R2 == 3).astype(int))
    
    # State 0 transitions
    p_inf = 1.0 - 0.50**N_A
    r_inf = np.random.rand(width)
    infected = r_inf < p_inf
    
    r_latent = np.random.rand(width)
    to_state_if_infected = np.where(r_latent < 0.80, 1, 2)
    
    P_recruit = 0.20 * N_A
    recruited = (~infected) & (N_A >= 2) & (np.random.rand(width) < P_recruit)
    
    is_zero = (S == 0)
    S_next[is_zero & infected] = to_state_if_infected[is_zero & infected]
    S_next[is_zero & recruited] = 3
    
    # State 1 transitions
    is_one = (S == 1)
    cleared_1 = (N_M >= 1) & (np.random.rand(width) < 0.75)
    p_activation = 0.10 + 0.05 * N_A
    activated = (~cleared_1) & (np.random.rand(width) < p_activation)
    S_next[is_one & cleared_1] = 0
    S_next[is_one & activated] = 2
    
    # State 2 transitions
    is_two = (S == 2)
    cleared_2 = (N_M >= 1) & (np.random.rand(width) < 0.85)
    decay_2 = (~cleared_2) & (np.random.rand(width) < 0.15)
    S_next[is_two & (cleared_2 | decay_2)] = 4
    
    # State 3 transitions
    is_three = (S == 3)
    exhaust_3 = np.random.rand(width) < 0.40
    S_next[is_three & exhaust_3] = 4
    
    # State 4 transitions
    is_four = (S == 4)
    regen_4 = np.random.rand(width) < 0.25
    S_next[is_four & regen_4] = 0
    
    return S_next

def step_rule_4(S):
    # Rule 4: Stochastic Phenotypic Switching (5 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N_C = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_P = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_K = (S_L1 == 4).astype(int) + (S_R1 == 4).astype(int)
    
    P_shock = 0.15 * (N_C + N_P)
    shock_occurs = np.random.rand(width) < P_shock
    
    # State 0 transitions
    p_C = 1.0 - 0.35**N_C
    p_P = 1.0 - 0.90**N_P
    P_inf = 1.0 - (1.0 - p_C) * (1.0 - p_P)
    
    is_zero = (S == 0)
    to_four_0 = is_zero & shock_occurs
    
    r_inf_0 = np.random.rand(width)
    infected_0 = is_zero & ~shock_occurs & (r_inf_0 < P_inf)
    r_choice_0 = np.random.rand(width)
    to_one_0 = infected_0 & (r_choice_0 < 0.90)
    to_two_0 = infected_0 & (r_choice_0 >= 0.90)
    
    S_next[to_four_0] = 4
    S_next[to_one_0] = 1
    S_next[to_two_0] = 2
    
    # State 1 transitions
    is_one = (S == 1)
    shock_or_neighbor_K = shock_occurs | (N_K >= 1)
    cleared_shock_1 = shock_or_neighbor_K & (np.random.rand(width) < 0.95)
    
    r_switch_1 = np.random.rand(width)
    switched_1 = ~cleared_shock_1 & (r_switch_1 < 0.08)
    
    r_rec_1 = np.random.rand(width)
    recovered_1 = ~cleared_shock_1 & ~switched_1 & (r_rec_1 < 0.15)
    
    S_next[is_one & cleared_shock_1] = 3
    S_next[is_one & switched_1] = 2
    S_next[is_one & recovered_1] = 3
    
    # State 2 transitions
    is_two = (S == 2)
    cleared_shock_2 = shock_or_neighbor_K & (np.random.rand(width) < 0.05)
    
    r_switch_2 = np.random.rand(width)
    switched_2 = ~cleared_shock_2 & (r_switch_2 < 0.12)
    
    r_rec_2 = np.random.rand(width)
    recovered_2 = ~cleared_shock_2 & ~switched_2 & (r_rec_2 < 0.02)
    
    S_next[is_two & cleared_shock_2] = 3
    S_next[is_two & switched_2] = 1
    S_next[is_two & recovered_2] = 3
    
    # State 3 transitions
    is_three = (S == 3)
    decay_3 = np.random.rand(width) < 0.15
    S_next[is_three & decay_3] = 0
    
    # State 4 transitions
    is_four = (S == 4)
    decay_4 = np.random.rand(width) < 0.80
    S_next[is_four & decay_4] = 0
    
    return S_next

def step_rule_5(S):
    # Rule 5: Viroid Hyperparasitism (6 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N_I = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_C = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_V = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)
    
    # State 0 transitions
    p_inf = 1.0 - (0.45**N_I) * (0.725**N_C)
    is_zero = (S == 0)
    infected_0 = is_zero & (np.random.rand(width) < p_inf)
    S_next[infected_0] = 1
    
    # State 1 transitions
    is_one = (S == 1)
    p_hyper = 1.0 - 0.40**(N_C + N_V)
    hyperinfected_1 = np.random.rand(width) < p_hyper
    
    r_choice_1 = np.random.rand(width)
    death_1 = ~hyperinfected_1 & (r_choice_1 < 0.10)
    recover_1 = ~hyperinfected_1 & (r_choice_1 >= 0.10) & (r_choice_1 < 0.20)
    
    S_next[is_one & hyperinfected_1] = 2
    S_next[is_one & death_1] = 4
    S_next[is_one & recover_1] = 5
    
    # State 2 transitions
    is_two = (S == 2)
    r_c = np.random.rand(width)
    suppress_2 = r_c < 0.35
    lysis_2 = (r_c >= 0.35) & (r_c < 0.55)
    S_next[is_two & suppress_2] = 3
    S_next[is_two & lysis_2] = 4
    
    # State 3 transitions
    is_three = (S == 3)
    recover_3 = np.random.rand(width) < 0.45
    S_next[is_three & recover_3] = 5
    
    # State 4 transitions
    is_four = (S == 4)
    regen_4 = np.random.rand(width) < 0.30
    S_next[is_four & regen_4] = 0
    
    # State 5 transitions
    is_five = (S == 5)
    decay_5 = np.random.rand(width) < 0.15
    S_next[is_five & decay_5] = 0
    
    return S_next

def step_rule_6(S):
    # Rule 6: Retroviral Integration and Oncogenic Drift (6 states)
    # Radius r = 2
    width = S.shape[0]
    S_L2 = np.roll(S, 2)
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    S_next = np.copy(S)
    
    N_IA = ((S_L2 == 1).astype(int) + (S_L1 == 1).astype(int) + 
            (S_R1 == 1).astype(int) + (S_R2 == 1).astype(int))
    N_T1 = ((S_L2 == 3).astype(int) + (S_L1 == 3).astype(int) + 
            (S_R1 == 3).astype(int) + (S_R2 == 3).astype(int))
    N_T2 = ((S_L2 == 4).astype(int) + (S_L1 == 4).astype(int) + 
            (S_R1 == 4).astype(int) + (S_R2 == 4).astype(int))
    
    p_inv_T2 = 1.0 - 0.55**N_T2
    p_inv_T1 = 1.0 - 0.85**N_T1
    p_inf = 1.0 - 0.65**N_IA
    
    # State 0 transitions
    is_zero = (S == 0)
    crushed = is_zero & (N_T2 >= 2) & (np.random.rand(width) < 0.40)
    inv_T2 = is_zero & ~crushed & (np.random.rand(width) < p_inv_T2)
    inv_T1 = is_zero & ~crushed & ~inv_T2 & (np.random.rand(width) < p_inv_T1)
    infected = is_zero & ~crushed & ~inv_T2 & ~inv_T1 & (np.random.rand(width) < p_inf)
    
    r_choice = np.random.rand(width)
    to_one = infected & (r_choice < 0.55)
    to_two = infected & (r_choice >= 0.55)
    
    S_next[crushed] = 5
    S_next[inv_T2] = 4
    S_next[inv_T1] = 3
    S_next[to_one] = 1
    S_next[to_two] = 2
    
    # State 1 transitions
    is_one = (S == 1)
    inv_T2_1 = is_one & (np.random.rand(width) < p_inv_T2)
    
    r_1 = np.random.rand(width)
    to_two_1 = is_one & ~inv_T2_1 & (r_1 < 0.15)
    to_three_1 = is_one & ~inv_T2_1 & (r_1 >= 0.15) & (r_1 < 0.20)
    to_five_1 = is_one & ~inv_T2_1 & (r_1 >= 0.20) & (r_1 < 0.45)
    
    S_next[inv_T2_1] = 4
    S_next[to_two_1] = 2
    S_next[to_three_1] = 3
    S_next[to_five_1] = 5
    
    # State 2 transitions
    is_two = (S == 2)
    inv_T2_2 = is_two & (np.random.rand(width) < p_inv_T2)
    
    r_2 = np.random.rand(width)
    to_one_2 = is_two & ~inv_T2_2 & (r_2 < 0.10)
    to_three_2 = is_two & ~inv_T2_2 & (r_2 >= 0.10) & (r_2 < 0.12)
    
    S_next[inv_T2_2] = 4
    S_next[to_one_2] = 1
    S_next[to_three_2] = 3
    
    # State 3 transitions
    is_three = (S == 3)
    r_3 = np.random.rand(width)
    to_four_3 = r_3 < 0.08
    to_five_3 = (r_3 >= 0.08) & (r_3 < 0.13)
    S_next[is_three & to_four_3] = 4
    S_next[is_three & to_five_3] = 5
    
    # State 4 transitions
    is_four = (S == 4)
    to_five_4 = np.random.rand(width) < 0.12
    S_next[is_four & to_five_4] = 5
    
    # State 5 transitions
    is_five = (S == 5)
    to_zero_5 = np.random.rand(width) < 0.35
    S_next[is_five & to_zero_5] = 0
    
    return S_next

def step_rule_7(S):
    # Rule 7: Recombination-Driven Zoonotic Spillover (6 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N_A = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_B = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_AB = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)
    N_R = (S_L1 == 4).astype(int) + (S_R1 == 4).astype(int)
    
    p_A = 1.0 - 0.55**(N_A + 0.5 * N_AB)
    p_B = 1.0 - 0.55**(N_B + 0.5 * N_AB)
    p_R = 1.0 - 0.20**N_R
    
    expose_R = np.random.rand(width) < p_R
    expose_A = np.random.rand(width) < p_A
    expose_B = np.random.rand(width) < p_B
    
    is_zero = (S == 0)
    to_four_0 = is_zero & expose_R
    to_three_0 = is_zero & ~expose_R & (expose_A & expose_B)
    to_one_0 = is_zero & ~expose_R & (expose_A & ~expose_B)
    to_two_0 = is_zero & ~expose_R & (expose_B & ~expose_A)
    
    S_next[to_four_0] = 4
    S_next[to_three_0] = 3
    S_next[to_one_0] = 1
    S_next[to_two_0] = 2
    
    # State 1 transitions
    is_one = (S == 1)
    p_super_B = 1.0 - 0.55**(N_B + 0.5 * N_AB)
    super_B = np.random.rand(width) < p_super_B
    recovery_1 = ~super_B & (np.random.rand(width) < 0.20)
    S_next[is_one & super_B] = 3
    S_next[is_one & recovery_1] = 0
    
    # State 2 transitions
    is_two = (S == 2)
    p_super_A = 1.0 - 0.55**(N_A + 0.5 * N_AB)
    super_A = np.random.rand(width) < p_super_A
    recovery_2 = ~super_A & (np.random.rand(width) < 0.20)
    S_next[is_two & super_A] = 3
    S_next[is_two & recovery_2] = 0
    
    # State 3 transitions
    is_three = (S == 3)
    r_3 = np.random.rand(width)
    recomb_3 = r_3 < 0.25
    recovery_3 = (r_3 >= 0.25) & (r_3 < 0.35)
    S_next[is_three & recomb_3] = 4
    S_next[is_three & recovery_3] = 0
    
    # State 4 transitions
    is_four = (S == 4)
    r_4 = np.random.rand(width)
    lethal_4 = r_4 < 0.40
    recovery_4 = (r_4 >= 0.40) & (r_4 < 0.50)
    S_next[is_four & lethal_4] = 5
    S_next[is_four & recovery_4] = 0
    
    # State 5 transitions
    is_five = (S == 5)
    decay_5 = np.random.rand(width) < 0.25
    S_next[is_five & decay_5] = 0
    
    return S_next

def step_rule_8(S):
    # Rule 8: Epigenetic Vaccination Memory and Drift (6 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N1 = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N2 = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    
    p1 = 1.0 - 0.40**N1
    p2 = 1.0 - 0.40**N2
    
    expose_1 = np.random.rand(width) < p1
    expose_2 = np.random.rand(width) < p2
    
    only_1 = expose_1 & ~expose_2
    only_2 = expose_2 & ~expose_1
    both_12 = expose_1 & expose_2
    
    r_choice = np.random.rand(width)
    to_one_0 = only_1 | (both_12 & (r_choice < 0.50))
    to_two_0 = only_2 | (both_12 & (r_choice >= 0.50))
    
    # State 0 transitions
    is_zero = (S == 0)
    S_next[is_zero & to_one_0] = 1
    S_next[is_zero & to_two_0] = 2
    
    # State 1 transitions
    is_one = (S == 1)
    r_1 = np.random.rand(width)
    drift_1 = r_1 < 0.12
    clear_1 = (r_1 >= 0.12) & (r_1 < 0.60)
    S_next[is_one & drift_1] = 2
    S_next[is_one & clear_1] = 3
    
    # State 2 transitions
    is_two = (S == 2)
    r_2 = np.random.rand(width)
    drift_2 = r_2 < 0.12
    clear_2 = (r_2 >= 0.12) & (r_2 < 0.60)
    S_next[is_two & drift_2] = 1
    S_next[is_two & clear_2] = 4
    
    # State 3 transitions
    is_three = (S == 3)
    p_fail_3 = 1.0 - 0.65**N2
    infect_3 = np.random.rand(width) < p_fail_3
    
    p_upgrade_3 = 0.15 * N2
    upgrade_3 = ~infect_3 & (np.random.rand(width) < p_upgrade_3)
    
    decay_3 = ~infect_3 & ~upgrade_3 & (np.random.rand(width) < 0.10)
    
    S_next[is_three & infect_3] = 2
    S_next[is_three & upgrade_3] = 5
    S_next[is_three & decay_3] = 0
    
    # State 4 transitions
    is_four = (S == 4)
    p_fail_4 = 1.0 - 0.65**N1
    infect_4 = np.random.rand(width) < p_fail_4
    
    p_upgrade_4 = 0.15 * N1
    upgrade_4 = ~infect_4 & (np.random.rand(width) < p_upgrade_4)
    
    decay_4 = ~infect_4 & ~upgrade_4 & (np.random.rand(width) < 0.10)
    
    S_next[is_four & infect_4] = 1
    S_next[is_four & upgrade_4] = 5
    S_next[is_four & decay_4] = 0
    
    # State 5 transitions
    is_five = (S == 5)
    r_5 = np.random.rand(width)
    decay_to_3 = r_5 < 0.08
    decay_to_4 = (r_5 >= 0.08) & (r_5 < 0.16)
    S_next[is_five & decay_to_3] = 3
    S_next[is_five & decay_to_4] = 4
    
    return S_next

def step_rule_9(S):
    # Rule 9: Spatial Quarantining and Vector Transmission (5 states)
    # Radius r = 2
    width = S.shape[0]
    S_L2 = np.roll(S, 2)
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    S_next = np.copy(S)
    
    N_I = ((S_L2 == 1).astype(int) + (S_L1 == 1).astype(int) + 
           (S_R1 == 1).astype(int) + (S_R2 == 1).astype(int))
    N_Q = ((S_L2 == 2).astype(int) + (S_L1 == 2).astype(int) + 
           (S_R1 == 2).astype(int) + (S_R2 == 2).astype(int))
    N_V = ((S_L2 == 3).astype(int) + (S_L1 == 3).astype(int) + 
           (S_R1 == 3).astype(int) + (S_R2 == 3).astype(int))
    
    # State 0 transitions
    is_zero = (S == 0)
    quar_trigger = is_zero & ((N_I >= 1) | (N_V >= 1)) & (np.random.rand(width) < 0.35)
    
    p_inf = 1.0 - (0.60**N_I) * (0.30**N_V)
    infect_0 = is_zero & ~quar_trigger & (np.random.rand(width) < p_inf)
    
    # Vector shedding from neighbors (radius 1) into state 0
    N_I_r1 = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    p_shed = 1.0 - 0.85**N_I_r1
    shed_to_0 = is_zero & ~quar_trigger & ~infect_0 & (np.random.rand(width) < p_shed)
    
    S_next[quar_trigger] = 2
    S_next[infect_0] = 1
    S_next[shed_to_0] = 3
    
    # State 1 transitions
    is_one = (S == 1)
    recover_1 = np.random.rand(width) < 0.25
    S_next[is_one & recover_1] = 4
    
    # State 2 transitions
    is_two = (S == 2)
    decay_2 = np.random.rand(width) < 0.20
    S_next[is_two & decay_2] = 0
    
    # State 3 transitions
    is_three = (S == 3)
    die_3 = np.random.rand(width) < 0.65
    S_next[is_three & die_3] = 0
    
    # State 4 transitions
    is_four = (S == 4)
    p_reinf = 1.0 - 0.65**N_V
    reinf_4 = np.random.rand(width) < p_reinf
    recovery_4 = ~reinf_4 & (np.random.rand(width) < 0.30)
    S_next[is_four & reinf_4] = 1
    S_next[is_four & recovery_4] = 0
    
    return S_next

def step_rule_10(S):
    # Rule 10: Antagonistic Co-evolutionary Arms Race (7 states)
    # Radius r = 1
    width = S.shape[0]
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    N_V1 = (S_L1 == 1).astype(int) + (S_R1 == 1).astype(int)
    N_V2 = (S_L1 == 2).astype(int) + (S_R1 == 2).astype(int)
    N_V3 = (S_L1 == 3).astype(int) + (S_R1 == 3).astype(int)
    
    p1 = 1.0 - 0.50**N_V1
    p2 = 1.0 - 0.50**N_V2
    p3 = 1.0 - 0.50**N_V3
    
    expose_V1 = np.random.rand(width) < p1
    expose_V2 = np.random.rand(width) < p2
    expose_V3 = np.random.rand(width) < p3
    
    # Exposure combinations for state 0 and picking infected strain
    comb = (expose_V1.astype(int) * 4) + (expose_V2.astype(int) * 2) + expose_V3.astype(int)
    
    r_choice_0 = np.random.rand(width)
    chosen_V = np.zeros(width, dtype=np.uint8)
    chosen_V[comb == 4] = 1
    chosen_V[comb == 2] = 2
    chosen_V[comb == 1] = 3
    chosen_V[comb == 6] = np.where(r_choice_0[comb == 6] < 0.50, 1, 2)
    chosen_V[comb == 5] = np.where(r_choice_0[comb == 5] < 0.50, 1, 3)
    chosen_V[comb == 3] = np.where(r_choice_0[comb == 3] < 0.50, 2, 3)
    
    r_three = r_choice_0[comb == 7]
    chosen_V[comb == 7] = np.where(r_three < 1/3, 1, np.where(r_three < 2/3, 2, 3))
    
    # Immune priming if not infected
    has_pathogen = (N_V1 >= 1) | (N_V2 >= 1) | (N_V3 >= 1)
    not_infected = (comb == 0)
    prime_0 = is_zero = (S == 0) & not_infected & has_pathogen & (np.random.rand(width) < 0.25)
    
    r_prime = np.random.rand(width)
    prime_state = np.where(r_prime < 1/3, 4, np.where(r_prime < 2/3, 5, 6))
    
    # State 0 transitions
    is_zero = (S == 0)
    S_next[is_zero & (comb > 0)] = chosen_V[is_zero & (comb > 0)]
    S_next[is_zero & prime_0] = prime_state[is_zero & prime_0]
    
    # State 1 transitions
    is_one = (S == 1)
    r_v1 = np.random.rand(width)
    to_v2_from_v1 = r_v1 < 0.08
    to_v3_from_v1 = (r_v1 >= 0.08) & (r_v1 < 0.16)
    clear_v1 = (r_v1 >= 0.16) & (r_v1 < 0.56)
    S_next[is_one & to_v2_from_v1] = 2
    S_next[is_one & to_v3_from_v1] = 3
    S_next[is_one & clear_v1] = 4
    
    # State 2 transitions
    is_two = (S == 2)
    r_v2 = np.random.rand(width)
    to_v1_from_v2 = r_v2 < 0.08
    to_v3_from_v2 = (r_v2 >= 0.08) & (r_v2 < 0.16)
    clear_v2 = (r_v2 >= 0.16) & (r_v2 < 0.56)
    S_next[is_two & to_v1_from_v2] = 1
    S_next[is_two & to_v3_from_v2] = 3
    S_next[is_two & clear_v2] = 5
    
    # State 3 transitions
    is_three = (S == 3)
    r_v3 = np.random.rand(width)
    to_v1_from_v3 = r_v3 < 0.08
    to_v2_from_v3 = (r_v3 >= 0.08) & (r_v3 < 0.16)
    clear_v3 = (r_v3 >= 0.16) & (r_v3 < 0.56)
    S_next[is_three & to_v1_from_v3] = 1
    S_next[is_three & to_v2_from_v3] = 2
    S_next[is_three & clear_v3] = 6
    
    # State 4 transitions
    expose_V2_4 = np.random.rand(width) < (1.0 - 0.50**N_V2)
    expose_V3_4 = np.random.rand(width) < (1.0 - 0.50**N_V3)
    infect_4 = expose_V2_4 | expose_V3_4
    
    r_choice_4 = np.random.rand(width)
    to_V_from_4 = np.zeros(width, dtype=np.uint8)
    to_V_from_4[expose_V2_4 & ~expose_V3_4] = 2
    to_V_from_4[expose_V3_4 & ~expose_V2_4] = 3
    to_V_from_4[expose_V2_4 & expose_V3_4] = np.where(r_choice_4[expose_V2_4 & expose_V3_4] < 0.50, 2, 3)
    
    is_four = (S == 4)
    r_other_4 = np.random.rand(width)
    drift_to_5_from_4 = ~infect_4 & (r_other_4 < 0.04)
    drift_to_6_from_4 = ~infect_4 & (r_other_4 >= 0.04) & (r_other_4 < 0.08)
    decay_from_4 = ~infect_4 & (r_other_4 >= 0.08) & (r_other_4 < 0.16)
    
    S_next[is_four & infect_4] = to_V_from_4[is_four & infect_4]
    S_next[is_four & drift_to_5_from_4] = 5
    S_next[is_four & drift_to_6_from_4] = 6
    S_next[is_four & decay_from_4] = 0
    
    # State 5 transitions
    expose_V1_5 = np.random.rand(width) < (1.0 - 0.50**N_V1)
    expose_V3_5 = np.random.rand(width) < (1.0 - 0.50**N_V3)
    infect_5 = expose_V1_5 | expose_V3_5
    
    r_choice_5 = np.random.rand(width)
    to_V_from_5 = np.zeros(width, dtype=np.uint8)
    to_V_from_5[expose_V1_5 & ~expose_V3_5] = 1
    to_V_from_5[expose_V3_5 & ~expose_V1_5] = 3
    to_V_from_5[expose_V1_5 & expose_V3_5] = np.where(r_choice_5[expose_V1_5 & expose_V3_5] < 0.50, 1, 3)
    
    is_five = (S == 5)
    r_other_5 = np.random.rand(width)
    drift_to_4_from_5 = ~infect_5 & (r_other_5 < 0.04)
    drift_to_6_from_5 = ~infect_5 & (r_other_5 >= 0.04) & (r_other_5 < 0.08)
    decay_from_5 = ~infect_5 & (r_other_5 >= 0.08) & (r_other_5 < 0.16)
    
    S_next[is_five & infect_5] = to_V_from_5[is_five & infect_5]
    S_next[is_five & drift_to_4_from_5] = 4
    S_next[is_five & drift_to_6_from_5] = 6
    S_next[is_five & decay_from_5] = 0
    
    # State 6 transitions
    expose_V1_6 = np.random.rand(width) < (1.0 - 0.50**N_V1)
    expose_V2_6 = np.random.rand(width) < (1.0 - 0.50**N_V2)
    infect_6 = expose_V1_6 | expose_V2_6
    
    r_choice_6 = np.random.rand(width)
    to_V_from_6 = np.zeros(width, dtype=np.uint8)
    to_V_from_6[expose_V1_6 & ~expose_V2_6] = 1
    to_V_from_6[expose_V2_6 & ~expose_V1_6] = 2
    to_V_from_6[expose_V1_6 & expose_V2_6] = np.where(r_choice_6[expose_V1_6 & expose_V2_6] < 0.50, 1, 2)
    
    is_six = (S == 6)
    r_other_6 = np.random.rand(width)
    drift_to_4_from_6 = ~infect_6 & (r_other_6 < 0.04)
    drift_to_5_from_6 = ~infect_6 & (r_other_6 >= 0.04) & (r_other_6 < 0.08)
    decay_from_6 = ~infect_6 & (r_other_6 >= 0.08) & (r_other_6 < 0.16)
    
    S_next[is_six & infect_6] = to_V_from_6[is_six & infect_6]
    S_next[is_six & drift_to_4_from_6] = 4
    S_next[is_six & drift_to_5_from_6] = 5
    S_next[is_six & decay_from_6] = 0
    
    return S_next

STEP_FUNCTIONS = {
    1: step_rule_1,
    2: step_rule_2,
    3: step_rule_3,
    4: step_rule_4,
    5: step_rule_5,
    6: step_rule_6,
    7: step_rule_7,
    8: step_rule_8,
    9: step_rule_9,
    10: step_rule_10
}

# ---------------------------------------------------------
# Color Palettes (N distinct vibrant colors on dark backgrounds)
# ---------------------------------------------------------

COLOR_PALETTES = {
    1: {
        0: (10, 10, 20),      # Dark blue-grey background
        1: (255, 0, 100),     # Neon Pink (I_A)
        2: (0, 255, 255),     # Neon Cyan (I_B)
        3: (100, 50, 200),    # Medium Purple (R_A)
        4: (0, 150, 150),     # Teal (R_B)
        5: (255, 255, 100)    # Pale Yellow (R_AB)
    },
    2: {
        0: (15, 15, 15),      # Near Black
        1: (50, 205, 50),     # Lime Green (V_1)
        2: (255, 165, 0),     # Orange (V_2)
        3: (255, 0, 0),       # Red (V_3)
        4: (128, 128, 128),   # Grey (D)
        5: (30, 144, 255)     # Dodger Blue (R)
    },
    3: {
        0: (20, 10, 30),      # Dark Violet
        1: (255, 255, 0),     # Yellow (I_L)
        2: (255, 20, 147),    # Deep Pink (I_A)
        3: (0, 250, 154),     # Medium Spring Green (M)
        4: (139, 69, 19)      # Saddle Brown (E)
    },
    4: {
        0: (10, 20, 20),      # Dark Slate
        1: (255, 69, 0),      # Red-Orange (I_C)
        2: (0, 255, 127),     # Spring Green (I_P)
        3: (75, 0, 130),      # Indigo (R)
        4: (255, 255, 255)    # White (K)
    },
    5: {
        0: (12, 12, 24),      # Midnight Blue
        1: (220, 20, 60),     # Crimson (I)
        2: (127, 255, 0),     # Chartreuse (C)
        3: (0, 191, 255),     # Deep Sky Blue (V)
        4: (70, 130, 180),    # Steel Blue (D)
        5: (230, 230, 250)    # Lavender (R)
    },
    6: {
        0: (25, 20, 20),      # Dark Brownish-Grey
        1: (255, 0, 255),     # Magenta (I_A)
        2: (138, 43, 226),    # Blue-Violet (I_L)
        3: (255, 140, 0),     # Dark Orange (T_1)
        4: (255, 215, 0),     # Gold (T_2)
        5: (0, 0, 0)          # Black (D)
    },
    7: {
        0: (10, 25, 15),      # Dark Teal-Green
        1: (240, 128, 128),   # Light Coral (I_A)
        2: (135, 206, 250),   # Light Sky Blue (I_B)
        3: (186, 85, 211),    # Medium Orchid (I_AB)
        4: (255, 23, 68),     # Vibrant Red (I_R)
        5: (47, 79, 79)       # Dark Slate Grey (D)
    },
    8: {
        0: (20, 20, 25),      # Dark Grey
        1: (255, 20, 147),    # Deep Pink (V_1)
        2: (30, 144, 255),    # Dodger Blue (V_2)
        3: (255, 105, 180),   # Hot Pink (M_1)
        4: (95, 158, 160),    # Cadet Blue (M_2)
        5: (0, 255, 0)        # Green (M_12)
    },
    9: {
        0: (24, 20, 30),      # Dark Eggplant
        1: (255, 127, 80),    # Coral (I)
        2: (112, 128, 144),   # Slate Grey (Q)
        3: (255, 215, 0),     # Gold (V)
        4: (147, 112, 219)    # Medium Purple (E)
    },
    10: {
        0: (15, 15, 25),      # Dark Space Blue
        1: (255, 0, 0),       # Red (V_1)
        2: (0, 255, 0) ,      # Green (V_2)
        3: (0, 0, 255),       # Blue (V_3)
        4: (255, 165, 0),     # Orange (I_1)
        5: (0, 255, 255),     # Cyan (I_2)
        6: (255, 0, 255)      # Magenta (I_3)
    }
}

# ---------------------------------------------------------
# Initializations
# ---------------------------------------------------------

def initialize_grid(rule_idx, width, init_type):
    grid = np.zeros(width, dtype=np.uint8)
    
    if init_type == "single_seed":
        if rule_idx == 1:
            grid[380:400] = 1
            grid[400:420] = 2
        elif rule_idx == 2:
            grid[395:405] = 1
        elif rule_idx == 3:
            grid[390:410] = 1
            grid[400] = 2
        elif rule_idx == 4:
            grid[390:400] = 1
            grid[400:410] = 2
        elif rule_idx == 5:
            grid[390:410] = 1
            grid[400] = 2
        elif rule_idx == 6:
            # Random mix of IA (1) and IL (2) in the center, and a single tumor cell (3)
            center_mix = np.random.choice([1, 2], size=40, p=[0.55, 0.45])
            grid[380:420] = center_mix
            grid[400] = 3
        elif rule_idx == 7:
            grid[370:395] = 1
            grid[405:430] = 2
        elif rule_idx == 8:
            grid[350] = 1
            grid[450] = 2
        elif rule_idx == 9:
            grid[400] = 1
        elif rule_idx == 10:
            grid[380:420] = np.random.choice([1, 2, 3, 4, 5, 6], size=40)
            
    else:  # random initialization
        if rule_idx == 1:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.90, 0.05, 0.05])
        elif rule_idx == 2:
            grid = np.random.choice([0, 1, 2, 3], size=width, p=[0.95, 0.03, 0.015, 0.005])
        elif rule_idx == 3:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.90, 0.08, 0.02])
        elif rule_idx == 4:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.90, 0.08, 0.02])
        elif rule_idx == 5:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.85, 0.10, 0.05])
        elif rule_idx == 6:
            grid = np.random.choice([0, 1, 2, 3], size=width, p=[0.90, 0.06, 0.03, 0.01])
        elif rule_idx == 7:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.90, 0.05, 0.05])
        elif rule_idx == 8:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.80, 0.05, 0.05, 0.05, 0.05])
        elif rule_idx == 9:
            grid = np.random.choice([0, 1], size=width, p=[0.95, 0.05])
        elif rule_idx == 10:
            grid = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=width, p=[0.70, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
            
    return grid.astype(np.uint8)

# ---------------------------------------------------------
# Simulation Runner
# ---------------------------------------------------------

def simulate_ca(rule_idx, init_type, steps=800, width=800):
    grid = initialize_grid(rule_idx, width, init_type)
    step_fn = STEP_FUNCTIONS[rule_idx]
    
    history = np.zeros((steps, width), dtype=np.uint8)
    history[0] = grid
    
    current = np.copy(grid)
    for t in range(1, steps):
        current = step_fn(current)
        history[t] = current
        
    return history

def save_history_as_image(history, rule_idx, filepath):
    palette = COLOR_PALETTES[rule_idx]
    height, width = history.shape
    img_data = np.zeros((height, width, 3), dtype=np.uint8)
    for state_val, color in palette.items():
        img_data[history == state_val] = color
        
    img = Image.fromarray(img_data)
    img.save(filepath)

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------

if __name__ == "__main__":
    for r in range(1, 11):
        for init in ["single_seed", "random"]:
            filename = f"rule_{r:02d}_{init}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            print(f"Simulating rule {r:02d} ({init})...")
            history = simulate_ca(r, init)
            save_history_as_image(history, r, filepath)
            print(f"Saved {filepath}")
    print("Done simulating all rules.")
