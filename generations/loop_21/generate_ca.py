import os
import numpy as np
from PIL import Image

# Output directory
OUTPUT_DIR = "C:/programming/complex_cellular_automata/generations/loop_21/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# Transition Functions
# ---------------------------------------------------------

def step_rule_1(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    is_zero = (S == 0)
    cond_2 = is_zero & (S_R1 == 1)
    cond_3 = is_zero & ~cond_2 & (S_L1 == 1)
    
    S_next[cond_2] = 2
    S_next[cond_3] = 3
    S_next[S == 2] = 4
    S_next[S == 3] = 5
    S_next[S == 1] = 0
    return S_next

def step_rule_2(S):
    S_L1 = np.roll(S, 1)
    S_L2 = np.roll(S, 2)
    S_L3 = np.roll(S, 3)
    S_L4 = np.roll(S, 4)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    S_R3 = np.roll(S, -3)
    S_R4 = np.roll(S, -4)
    
    S_next = np.copy(S)
    
    cond_1_to_5 = (S == 1) & (S_R1 == 4) & (S_R2 == 2) & (S_R3 == 4) & (S_R4 == 3)
    cond_2_to_5 = (S == 2) & (S_L2 == 1) & (S_L1 == 4) & (S_R1 == 4) & (S_R2 == 3)
    cond_3_to_5 = (S == 3) & (S_L4 == 1) & (S_L3 == 4) & (S_L2 == 2) & (S_L1 == 4)
    cond_4_to_5 = (S == 4) & (
        (((S_L1 == 1) | (S_L1 == 5)) & ((S_R1 == 2) | (S_R1 == 5))) |
        (((S_L1 == 2) | (S_L1 == 5)) & ((S_R1 == 3) | (S_R1 == 5)))
    )
    
    # State 1
    S_next[cond_1_to_5] = 5
    S_next[(S == 1) & ~cond_1_to_5 & (S_R1 == 0)] = 0
    
    # State 2
    S_next[cond_2_to_5] = 5
    
    # State 3
    S_next[cond_3_to_5] = 5
    S_next[(S == 3) & ~cond_3_to_5 & (S_L1 == 0)] = 0
    
    # State 4
    S_next[cond_4_to_5] = 5
    S_next[(S == 4) & ~cond_4_to_5] = 0
    
    # State 0
    is_zero = (S == 0)
    cond_0_to_1 = is_zero & (S_L1 == 1) & ~np.roll(cond_1_to_5, 1)
    cond_0_to_3 = is_zero & ~cond_0_to_1 & (S_R1 == 3) & ~np.roll(cond_3_to_5, -1)
    cond_0_to_4 = is_zero & ~cond_0_to_1 & ~cond_0_to_3 & (S_L1 == 4) & ~np.roll(cond_4_to_5, 1)
    
    S_next[cond_0_to_1] = 1
    S_next[cond_0_to_3] = 3
    S_next[cond_0_to_4] = 4
    S_next[is_zero & ~cond_0_to_1 & ~cond_0_to_3 & ~cond_0_to_4] = 0
    
    # State 5 remains 5
    S_next[S == 5] = 5
    
    return S_next

def step_rule_3(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_1 = is_zero & (S_L1 == 1) & (S_R1 != 2)
    cond_0_to_2 = is_zero & ~cond_0_to_1 & (S_R1 == 2) & (S_L1 != 1)
    cond_0_to_3 = is_zero & ~cond_0_to_1 & ~cond_0_to_2 & (
        ((S_L1 == 1) | (S_L1 == 3)) & ((S_R1 == 2) | (S_R1 == 3))
    )
    
    S_next[cond_0_to_1] = 1
    S_next[cond_0_to_2] = 2
    S_next[cond_0_to_3] = 3
    S_next[is_zero & ~cond_0_to_1 & ~cond_0_to_2 & ~cond_0_to_3] = 0
    
    # s = 1 case
    is_one = (S == 1)
    cond_1_to_4 = is_one & ((S_R1 == 2) | (S_R1 == 4))
    cond_1_to_3 = is_one & ~cond_1_to_4 & ((S_R1 == 0) | (S_R1 == 1))
    
    S_next[cond_1_to_4] = 4
    S_next[cond_1_to_3] = 3
    S_next[is_one & ~cond_1_to_4 & ~cond_1_to_3] = 0
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_4 = is_two & ((S_L1 == 1) | (S_L1 == 4))
    cond_2_to_3 = is_two & ~cond_2_to_4 & ((S_L1 == 0) | (S_L1 == 2))
    
    S_next[cond_2_to_4] = 4
    S_next[cond_2_to_3] = 3
    S_next[is_two & ~cond_2_to_4 & ~cond_2_to_3] = 0
    
    # s = 3 case
    is_three = (S == 3)
    cond_3_to_4 = is_three & (S_L1 == 4) & (S_R1 == 4)
    S_next[is_three & cond_3_to_4] = 4
    S_next[is_three & ~cond_3_to_4] = 3
    
    # s = 4 case
    S_next[S == 4] = 4
    
    return S_next

def step_rule_4(S):
    S_L1 = np.roll(S, 1)
    S_L2 = np.roll(S, 2)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    
    S_next = np.copy(S)
    
    # s = 3 case
    is_three = (S == 3)
    cond_3_to_4 = is_three & (S_L1 == 1) & (S_R1 == 2)
    S_next[cond_3_to_4] = 4
    S_next[is_three & ~cond_3_to_4] = 3
    
    # s = 1 case
    is_one = (S == 1)
    cond_1_to_4 = is_one & (S_R1 == 3) & (S_R2 == 2)
    cond_1_to_0 = is_one & ~cond_1_to_4 & ((S_R1 == 0) | (S_R1 == 1))
    S_next[cond_1_to_4] = 4
    S_next[cond_1_to_0] = 0
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_4 = is_two & (S_L1 == 3) & (S_L2 == 1)
    cond_2_to_0 = is_two & ~cond_2_to_4 & ((S_L1 == 0) | (S_L1 == 2))
    S_next[cond_2_to_4] = 4
    S_next[cond_2_to_0] = 0
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_1 = is_zero & (S_L1 == 1)
    cond_0_to_2 = is_zero & ~cond_0_to_1 & (S_R1 == 2)
    S_next[cond_0_to_1] = 1
    S_next[cond_0_to_2] = 2
    S_next[is_zero & ~cond_0_to_1 & ~cond_0_to_2] = 0
    
    # s = 4 case
    S_next[S == 4] = 4
    
    return S_next

def step_rule_5(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    cond_s1_to_3 = (S == 1) & (S_L1 == 3) & (S_R1 == 2)
    cond_s2_to_3 = (S == 2) & (S_L1 == 3)
    cond_s3_to_4 = (S == 3)
    cond_s4_to_0 = (S == 4)
    cond_s0_to_1 = (S == 0) & (S_L1 == 1)
    cond_s0_to_2 = (S == 0) & ~cond_s0_to_1 & (S_R1 == 2)
    
    S_next[cond_s1_to_3] = 3
    S_next[cond_s2_to_3] = 3
    S_next[cond_s3_to_4] = 4
    S_next[cond_s4_to_0] = 0
    S_next[cond_s0_to_1] = 1
    S_next[cond_s0_to_2] = 2
    
    return S_next

def step_rule_6(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    # s = 1 case
    is_one = (S == 1)
    cond_1_to_2 = is_one & (S_L1 == 1) & (S_R1 == 1)
    cond_1_to_3 = is_one & ~cond_1_to_2 & ((S_L1 == 2) | (S_R1 == 2))
    S_next[cond_1_to_2] = 2
    S_next[cond_1_to_3] = 3
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_3 = is_two & (S_L1 == 1) & (S_R1 == 1)
    S_next[cond_2_to_3] = 3
    
    # s = 3 and 0 remain unchanged
    return S_next

def step_rule_7(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    # s = 1 case
    is_one = (S == 1)
    cond_1_to_4 = is_one & ((S_L1 == 4) | (S_R1 == 4))
    S_next[cond_1_to_4] = 4
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_3 = is_two & (S_R1 != 1) & (S_R1 != 3)
    cond_2_to_4 = is_two & ~cond_2_to_3 & ((S_L1 == 4) | (S_R1 == 4))
    S_next[cond_2_to_3] = 3
    S_next[cond_2_to_4] = 4
    
    # s = 3 case
    is_three = (S == 3)
    S_next[is_three] = 4
    
    # s = 4 case
    is_four = (S == 4)
    S_next[is_four] = 0
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_4 = is_zero & (
        ((S_L1 == 4) & (S_R1 != 0)) |
        ((S_R1 == 4) & (S_L1 != 0))
    )
    S_next[cond_0_to_4] = 4
    S_next[is_zero & ~cond_0_to_4] = 0
    
    return S_next

def step_rule_8(S):
    S_L1 = np.roll(S, 1)
    S_R1 = np.roll(S, -1)
    S_next = np.copy(S)
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_3 = is_zero & (S_R1 == 3) & (S_L1 != 4)
    cond_0_to_4 = is_zero & ~cond_0_to_3 & (S_L1 == 4) & (S_R1 != 3)
    S_next[cond_0_to_3] = 3
    S_next[cond_0_to_4] = 4
    S_next[is_zero & ~cond_0_to_3 & ~cond_0_to_4] = 0
    
    # s = 1 case
    is_one = (S == 1)
    cond_1_to_5 = is_one & (S_R1 == 3)
    S_next[cond_1_to_5] = 5
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_5 = is_two & (S_L1 == 4)
    S_next[cond_2_to_5] = 5
    
    # s = 3 case
    is_three = (S == 3)
    cond_3_to_5 = is_three & (S_L1 == 1)
    S_next[cond_3_to_5] = 5
    S_next[is_three & ~cond_3_to_5] = 0
    
    # s = 4 case
    is_four = (S == 4)
    cond_4_to_5 = is_four & (S_R1 == 2)
    S_next[cond_4_to_5] = 5
    S_next[is_four & ~cond_4_to_5] = 0
    
    # s = 5 remains 5
    S_next[S == 5] = 5
    
    return S_next

def step_rule_9(S):
    S_L1 = np.roll(S, 1)
    S_L2 = np.roll(S, 2)
    S_next = np.copy(S)
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_4_a = is_zero & (S_L1 == 4)
    cond_0_to_4_b = is_zero & ~cond_0_to_4_a & (S_L1 == 1) & (S_L2 == 4)
    S_next[cond_0_to_4_a | cond_0_to_4_b] = 4
    S_next[is_zero & ~cond_0_to_4_a & ~cond_0_to_4_b] = 0
    
    # s = 1 remains 1
    
    # s = 2 case
    is_two = (S == 2)
    cond_2_to_3 = is_two & ((S_L1 == 4) | ((S_L1 == 1) & (S_L2 == 4)))
    S_next[cond_2_to_3] = 3
    
    # s = 3 remains 3
    
    # s = 4 case
    is_four = (S == 4)
    S_next[is_four] = 0
    
    return S_next

def step_rule_10(S):
    S_L1 = np.roll(S, 1)
    S_L2 = np.roll(S, 2)
    S_R1 = np.roll(S, -1)
    S_R2 = np.roll(S, -2)
    
    S_next = np.copy(S)
    
    # s = 3 case
    is_three = (S == 3)
    cond_3_to_1_l = is_three & (S_L1 == 4) & (S_L2 == 2)
    cond_3_to_2_l = is_three & ~cond_3_to_1_l & (S_L1 == 4) & (S_L2 == 1)
    cond_3_to_1_r = is_three & ~cond_3_to_1_l & ~cond_3_to_2_l & (S_R1 == 4) & (S_R2 == 2)
    cond_3_to_2_r = is_three & ~cond_3_to_1_l & ~cond_3_to_2_l & ~cond_3_to_1_r & (S_R1 == 4) & (S_R2 == 1)
    
    S_next[cond_3_to_1_l | cond_3_to_1_r] = 1
    S_next[cond_3_to_2_l | cond_3_to_2_r] = 2
    S_next[is_three & ~cond_3_to_1_l & ~cond_3_to_2_l & ~cond_3_to_1_r & ~cond_3_to_2_r] = 0
    
    # s = 4 case
    is_four = (S == 4)
    S_next[is_four] = 0
    
    # s = 0 case
    is_zero = (S == 0)
    cond_0_to_4_a = is_zero & (S_L1 == 4) & (S_R1 == 3)
    cond_0_to_4_b = is_zero & ~cond_0_to_4_a & (S_R1 == 4) & (S_L1 == 3)
    cond_0_to_4_c = is_zero & ~cond_0_to_4_a & ~cond_0_to_4_b & (S_L1 == 3) & ((S_R1 == 1) | (S_R1 == 2))
    
    S_next[cond_0_to_4_a | cond_0_to_4_b | cond_0_to_4_c] = 4
    S_next[is_zero & ~cond_0_to_4_a & ~cond_0_to_4_b & ~cond_0_to_4_c] = 0
    
    # s = 1 or 2 remain unchanged
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
# Color Palettes
# ---------------------------------------------------------

COLOR_PALETTES = {
    1: {
        0: (15, 15, 26),      # Dark purple-blue background
        1: (255, 0, 127),     # Neon Pink
        2: (57, 255, 20),     # Neon Green
        3: (0, 229, 255),     # Neon Cyan
        4: (255, 215, 0),     # Gold
        5: (255, 87, 34)      # Neon Orange
    },
    2: {
        0: (13, 13, 13),      # Very dark grey/black
        1: (255, 63, 63),     # Vibrant Red
        2: (63, 63, 255),     # Vibrant Blue
        3: (63, 255, 63),     # Vibrant Green
        4: (255, 255, 63),    # Vibrant Yellow
        5: (255, 63, 255)     # Vibrant Magenta
    },
    3: {
        0: (18, 14, 22),      # Dark violet background
        1: (255, 159, 0),     # Neon Orange
        2: (0, 255, 159),     # Neon Spring Green
        3: (77, 77, 255),     # Deep Blue
        4: (224, 224, 224)    # Glowing Silver
    },
    4: {
        0: (16, 16, 24),      # Dark slate background
        1: (255, 42, 109),    # Neon Pink/Red
        2: (5, 217, 232),     # Neon Cyan
        3: (245, 166, 35),    # Warm Amber
        4: (255, 255, 255)    # Bright White
    },
    5: {
        0: (10, 14, 23),      # Dark space blue background
        1: (0, 230, 118),     # Bright Green
        2: (41, 121, 255),    # Electric Blue
        3: (255, 234, 0),     # Bright Yellow
        4: (213, 0, 249)      # Neon Purple
    },
    6: {
        0: (12, 12, 15),      # Dark night background
        1: (0, 245, 255),     # Bright Turquoise
        2: (255, 102, 0),     # Vibrant Orange
        3: (255, 0, 255)      # Bright Magenta
    },
    7: {
        0: (20, 0, 12),       # Dark burgundy background
        1: (0, 229, 255),     # Cyan
        2: (255, 234, 0),     # Yellow
        3: (255, 23, 68),     # Vibrant Red
        4: (224, 64, 251)     # Vibrant Purple
    },
    8: {
        0: (14, 18, 16),      # Dark forest background
        1: (178, 255, 89),    # Lime Green
        2: (255, 64, 129),    # Bright Rose
        3: (0, 229, 255),     # Neon Light Blue
        4: (255, 255, 0),     # Yellow
        5: (224, 64, 251)     # Neon Violet
    },
    9: {
        0: (21, 16, 26),      # Dark mauve background
        1: (255, 143, 0),     # Amber
        2: (0, 176, 255),     # Light Blue
        3: (0, 230, 118),     # Green
        4: (255, 61, 0)       # Red-Orange
    },
    10: {
        0: (11, 14, 20),      # Dark cyan-grey background
        1: (0, 229, 255),     # Cyan
        2: (255, 61, 0),      # Red-Orange
        3: (158, 158, 158),    # Grey Noise
        4: (118, 255, 3)      # Vibrant Chartreuse
    }
}

# ---------------------------------------------------------
# Initializations
# ---------------------------------------------------------

def initialize_grid(rule_idx, width, init_type):
    grid = np.zeros(width, dtype=np.uint8)
    
    if init_type == "single_seed":
        if rule_idx == 1:
            grid[width // 2] = 1
        elif rule_idx == 2:
            grid[400] = 2
            grid[250] = 1
            grid[550] = 3
            for x in [50, 120, 180, 220, 300, 350, 420, 480]:
                grid[x] = 4
        elif rule_idx == 3:
            for x in [150, 250, 350]:
                grid[x] = 1
            for x in [450, 550, 650]:
                grid[x] = 2
        elif rule_idx == 4:
            grid[400] = 3
            for x in [100, 250, 350]:
                grid[x] = 1
            for x in [450, 550, 700]:
                grid[x] = 2
        elif rule_idx == 5:
            # Alternating segments of 1 and 2
            grid[0:200] = 1
            grid[200:400] = 2
            grid[400:600] = 1
            grid[600:800] = 2
            grid[199] = 3
            grid[599] = 3
        elif rule_idx == 6:
            # Consonant blocks of different lengths to trigger epenthesis
            # 3 consonants at 100
            grid[100:103] = 1
            # 5 consonants at 200
            grid[200:205] = 1
            # 7 consonants at 350
            grid[350:357] = 1
            # 11 consonants at 500
            grid[500:511] = 1
            # 15 consonants at 650
            grid[650:665] = 1
        elif rule_idx == 7:
            # Correct pairing is 2 followed by 1 (M S)
            for x in [100, 200, 300, 500, 600, 700]:
                grid[x] = 2
                grid[x+1] = 1
            # Error node triggers sweeping wave
            grid[400] = 2  # Lone modifier (no substantive to its right)
        elif rule_idx == 8:
            for x in [150, 350, 550]:
                grid[x] = 1  # Noun Cores
            for x in [250, 450, 650]:
                grid[x] = 2  # Adjective Cores
            for x in [180, 380, 580]:
                grid[x] = 3  # Left-drifting marker Alpha
            for x in [220, 420, 620]:
                grid[x] = 4  # Right-drifting marker Beta
        elif rule_idx == 9:
            for x in [200, 350, 500, 650]:
                grid[x] = 1  # Nouns
            for x in [250, 400, 550, 700]:
                grid[x] = 2  # Verbs
            grid[50] = 4      # Tense Shift Wave
        elif rule_idx == 10:
            # Alternating script segments with noise and scribe
            # Segment 1
            grid[200:204:2] = 1
            grid[201:204:2] = 2
            grid[204] = 3  # noise
            grid[205] = 2
            grid[206] = 1
            grid[198] = 4  # scribe
            
            # Segment 2
            grid[500:504:2] = 2
            grid[501:504:2] = 1
            grid[504] = 3  # noise
            grid[505] = 1
            grid[506] = 2
            grid[508] = 4  # scribe
            
    else:  # random initialization
        if rule_idx == 1:
            grid = np.random.choice([0, 1], size=width, p=[0.98, 0.02])
        elif rule_idx == 2:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.93, 0.015, 0.015, 0.015, 0.025])
        elif rule_idx == 3:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.95, 0.025, 0.025])
        elif rule_idx == 4:
            grid = np.random.choice([0, 1, 2, 3], size=width, p=[0.94, 0.025, 0.025, 0.01])
        elif rule_idx == 5:
            # Generate binary blocks of 1 and 2, and some 3s
            base = np.random.choice([1, 2], size=width, p=[0.5, 0.5])
            # Smooth blocks
            for _ in range(5):
                base = np.where(np.roll(base, 1) == base, base, np.roll(base, -1))
            grid = base.astype(np.uint8)
            # Inject some 3s (wave packets) at boundaries
            boundaries = (grid != np.roll(grid, -1))
            # Pick a few boundaries randomly
            rand_boundary = np.random.rand(width) < 0.2
            grid[boundaries & rand_boundary] = 3
        elif rule_idx == 6:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.15, 0.80, 0.05])
        elif rule_idx == 7:
            grid = np.random.choice([0, 1, 2], size=width, p=[0.85, 0.10, 0.05])
        elif rule_idx == 8:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.90, 0.03, 0.03, 0.02, 0.02])
        elif rule_idx == 9:
            grid = np.random.choice([0, 1, 2, 4], size=width, p=[0.90, 0.04, 0.04, 0.02])
        elif rule_idx == 10:
            grid = np.random.choice([0, 1, 2, 3, 4], size=width, p=[0.70, 0.12, 0.12, 0.04, 0.02])
            
    return grid

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
