import os
import numpy as np
from PIL import Image

def save_image(grid, colors, filepath):
    # Map the grid of states to RGB colors
    color_grid = colors[grid].astype(np.uint8)
    img = Image.fromarray(color_grid)
    img.save(filepath)

def main():
    output_dir = "generations/loop_22/output"
    os.makedirs(output_dir, exist_ok=True)
    
    steps = 800
    width = 800
    
    # ----------------------------------------------------
    # RULE 1: Spontaneous Localization (GRW Collapse)
    # N = 4. 0: vacuum, 1: coherent, 2: spin-up, 3: spin-down
    # ----------------------------------------------------
    print("Simulating Rule 1...")
    colors_1 = np.array([
        [10, 15, 30],      # 0: dark slate blue
        [0, 255, 255],     # 1: neon cyan
        [255, 0, 100],     # 2: neon red/pink
        [200, 0, 255]      # 3: neon purple/magenta
    ], dtype=np.uint8)
    
    lambda_val = 0.008
    p_s = 0.7
    p_c = 0.95
    gamma = 0.02
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        if init_type == "single_seed":
            grid[0, 380:420] = 1
            grid[0, 400] = 2
        else:
            r = np.random.random(width)
            grid[0] = np.where(r < 0.7, 0,
                               np.where(r < 0.95, 1,
                                        np.where(r < 0.975, 2, 3)))
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            
            # Decay of collapsed states
            mask_decay = (S == 2) | (S == 3)
            r_decay = np.random.random(width)
            S_next[mask_decay] = np.where(r_decay[mask_decay] < gamma, 0, S[mask_decay])
            
            # Spontaneous collapse of 1
            mask_1 = S == 1
            r_collapse = np.random.random(width)
            collapse_to_2 = mask_1 & (r_collapse < lambda_val / 2)
            collapse_to_3 = mask_1 & (r_collapse >= lambda_val / 2) & (r_collapse < lambda_val)
            S_next[collapse_to_2] = 2
            S_next[collapse_to_3] = 3
            
            # Induced collapse for remaining 1s
            mask_induced = mask_1 & (r_collapse >= lambda_val)
            if np.any(mask_induced):
                left_S = np.roll(S, 1)
                right_S = np.roll(S, -1)
                
                left_is_c = (left_S == 2) | (left_S == 3)
                right_is_c = (right_S == 2) | (right_S == 3)
                
                c1 = mask_induced & left_is_c & ~right_is_c
                if np.any(c1):
                    r_ind = np.random.random(width)
                    S_next[c1] = np.where(r_ind[c1] < p_c, left_S[c1], 0)
                    
                c2 = mask_induced & right_is_c & ~left_is_c
                if np.any(c2):
                    r_ind = np.random.random(width)
                    S_next[c2] = np.where(r_ind[c2] < p_c, right_S[c2], 0)
                    
                c3 = mask_induced & left_is_c & right_is_c
                if np.any(c3):
                    r_ind = np.random.random(width)
                    S_next[c3] = np.where(r_ind[c3] < p_c / 2, left_S[c3],
                                         np.where(r_ind[c3] < p_c, right_S[c3], 0))
            
            # Excitation of 0
            mask_0 = S == 0
            if np.any(mask_0):
                left_S = np.roll(S, 1)
                right_S = np.roll(S, -1)
                neighbor_has_1 = (left_S == 1) | (right_S == 1)
                neighbor_has_c = (left_S == 2) | (left_S == 3) | (right_S == 2) | (right_S == 3)
                
                excite_cond = mask_0 & neighbor_has_1 & ~neighbor_has_c
                if np.any(excite_cond):
                    r_excite = np.random.random(width)
                    S_next[excite_cond] = np.where(r_excite[excite_cond] < p_s, 1, 0)
            
            grid[t+1] = S_next
            
        save_image(grid, colors_1, f"{output_dir}/rule_01_{init_type}.png")

    # ----------------------------------------------------
    # RULE 2: Quantum Tunneling through Barriers
    # N = 4. 0: free space, 1: right-mover, 2: barrier, 3: left-mover
    # ----------------------------------------------------
    print("Simulating Rule 2...")
    colors_2 = np.array([
        [5, 15, 10],       # 0: very dark green-black
        [0, 191, 255],     # 1: neon light blue (right-mover)
        [180, 180, 180],   # 2: static barrier (grey)
        [255, 127, 0]      # 3: neon orange (left-mover)
    ], dtype=np.uint8)
    
    p_tunnel = 0.25
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        
        # Define static barrier columns
        barriers = [250, 400, 550] if init_type == "single_seed" else [100, 200, 300, 400, 500, 600, 700]
        for col in barriers:
            grid[:, col] = 2
            
        if init_type == "single_seed":
            # Initial moving particles
            grid[0, 50] = 1
            grid[0, 750] = 3
        else:
            # Random initial moving particles in non-barrier columns
            r = np.random.random(width)
            non_barriers = [c for c in range(width) if c not in barriers]
            for col in non_barriers:
                if r[col] < 0.04:
                    grid[0, col] = 1
                elif r[col] < 0.08:
                    grid[0, col] = 3
                    
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            
            # Enforce static barriers
            for col in barriers:
                S_next[col] = 2
                
            # Random decision array
            R = np.random.random(width)
            
            left_1 = np.roll(S, 1)
            right_1 = np.roll(S, -1)
            left_2 = np.roll(S, 2)
            right_2 = np.roll(S, -2)
            
            # Handle state 1 (right-mover)
            mask_1 = S == 1
            if np.any(mask_1):
                near_barrier = (right_1 == 2)
                S_next[mask_1 & near_barrier] = np.where(R[mask_1 & near_barrier] < p_tunnel, 0, 3)
                S_next[mask_1 & ~near_barrier] = 0
                
            # Handle state 3 (left-mover)
            mask_3 = S == 3
            if np.any(mask_3):
                near_barrier = (left_1 == 2)
                S_next[mask_3 & near_barrier] = np.where(R[mask_3 & near_barrier] < p_tunnel, 0, 1)
                S_next[mask_3 & ~near_barrier] = 0
                
            # Handle state 0
            mask_0 = S == 0
            if np.any(mask_0):
                tunnel_R = (left_2 == 1) & (left_1 == 2)
                tunnel_L = (right_2 == 3) & (right_1 == 2)
                in_R = (left_1 == 1) & (S != 2) & (right_1 != 2)
                in_L = (right_1 == 3) & (S != 2) & (left_1 != 2)
                
                val = np.zeros(width, dtype=int)
                cond_in_R = in_R & ~in_L
                cond_in_L = in_L & ~in_R
                val[cond_in_R] = 1
                val[cond_in_L] = 3
                
                cond_tunnel_R = tunnel_R & (np.roll(R, 2) < p_tunnel)
                val[cond_tunnel_R] = 1
                cond_tunnel_L = tunnel_L & (np.roll(R, -2) < p_tunnel)
                val[cond_tunnel_L] = 3
                
                S_next[mask_0] = val[mask_0]
                
            # Periodic injection for single seed to make a beautiful diagram
            if init_type == "single_seed":
                if t % 80 == 0:
                    S_next[50] = 1
                    S_next[750] = 3
                    
            grid[t+1] = S_next
            
        save_image(grid, colors_2, f"{output_dir}/rule_02_{init_type}.png")

    # ----------------------------------------------------
    # RULE 3: Environmental Decoherence Phase Transition
    # N = 3. 0: dephased ground, 1: coherent, 2: noise
    # ----------------------------------------------------
    print("Simulating Rule 3...")
    colors_3 = np.array([
        [15, 5, 20],       # 0: dark purple-black
        [57, 255, 20],     # 1: neon green
        [255, 36, 0]       # 2: neon red (noise)
    ], dtype=np.uint8)
    
    p_decay = 0.25
    p_spread = 0.92
    p_decoh = 0.85
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        eta = 0.002 if init_type == "single_seed" else 0.015
        
        if init_type == "single_seed":
            grid[0, 395:405] = 1
        else:
            r = np.random.random(width)
            grid[0] = np.where(r < 0.6, 0, np.where(r < 0.9, 1, 2))
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            
            # Decay of noise (state 2)
            mask_2 = S == 2
            r_decay = np.random.random(width)
            S_next[mask_2] = np.where(r_decay[mask_2] < p_decay, 0, 2)
            
            # Dephasing of coherence (state 1)
            mask_1 = S == 1
            near_noise = (left_S == 2) | (right_S == 2)
            r_decoh = np.random.random(width)
            S_next[mask_1 & near_noise] = np.where(r_decoh[mask_1 & near_noise] < p_decoh, 0, 1)
            
            # State 0 updates: noise generation & coherence spreading
            mask_0 = S == 0
            r_noise = np.random.random(width)
            r_spread = np.random.random(width)
            
            noise_gen = mask_0 & (r_noise < eta)
            S_next[noise_gen] = 2
            
            spread_cond = mask_0 & ~noise_gen & ((left_S == 1) | (right_S == 1)) & (left_S != 2) & (right_S != 2)
            S_next[spread_cond] = np.where(r_spread[spread_cond] < p_spread, 1, 0)
            
            grid[t+1] = S_next
            
        save_image(grid, colors_3, f"{output_dir}/rule_03_{init_type}.png")

    # ----------------------------------------------------
    # RULE 4: Quantum Zeno & Anti-Zeno Dynamics
    # N = 4. 0: ground, 1: excited, 2: slow pulse, 3: fast pulse
    # ----------------------------------------------------
    print("Simulating Rule 4...")
    colors_4 = np.array([
        [10, 10, 25],      # 0: deep space blue
        [255, 255, 0],     # 1: electric yellow (excited)
        [0, 255, 200],     # 2: slow pulse (light blue)
        [255, 0, 150]      # 3: fast pulse (hot pink)
    ], dtype=np.uint8)
    
    p_trans = 0.08
    p_decay = 0.15
    p_zeno = 0.003
    p_az = 0.75
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        if init_type == "single_seed":
            pass # starts from empty background with periodic injections
        else:
            r = np.random.random(width)
            grid[0] = np.where(r < 0.8, 0, np.where(r < 0.95, 1, np.where(r < 0.975, 2, 3)))
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            
            incoming_2 = left_S == 2
            incoming_3 = right_S == 3
            
            # Resolve pulse propagation conflicts
            conflict = incoming_2 & incoming_3
            r_conflict = np.random.random(width)
            S_next[conflict] = np.where(r_conflict[conflict] < 0.5, 2, 3)
            
            only_2 = incoming_2 & ~incoming_3
            S_next[only_2] = 2
            
            only_3 = incoming_3 & ~incoming_2
            S_next[only_3] = 3
            
            no_pulse = ~incoming_2 & ~incoming_3
            
            # Decay of excited state (state 1)
            mask_1 = S == 1
            r_decay = np.random.random(width)
            S_next[mask_1 & no_pulse] = np.where(r_decay[mask_1 & no_pulse] < p_decay, 0, 1)
            
            # Transition of ground state (state 0)
            mask_0 = S == 0
            if np.any(mask_0 & no_pulse):
                r_trans = np.random.random(width)
                fast_adj = (left_S == 3) | (right_S == 3)
                slow_adj = (left_S == 2) | (right_S == 2)
                
                zeno_cond = mask_0 & no_pulse & fast_adj
                S_next[zeno_cond] = np.where(r_trans[zeno_cond] < p_zeno, 1, 0)
                
                az_cond = mask_0 & no_pulse & slow_adj & ~fast_adj
                S_next[az_cond] = np.where(r_trans[az_cond] < p_az, 1, 0)
                
                std_cond = mask_0 & no_pulse & ~fast_adj & ~slow_adj
                S_next[std_cond] = np.where(r_trans[std_cond] < p_trans, 1, 0)
                
            # Periodic injection of pulses
            if init_type == "single_seed":
                if t % 100 == 0:
                    S_next[10] = 2
                    S_next[780] = 3
            else:
                # Randomly spawn new pulses at boundaries to maintain density
                if np.random.random() < 0.05:
                    S_next[0] = 2
                if np.random.random() < 0.05:
                    S_next[width-1] = 3
                    
            grid[t+1] = S_next
            
        save_image(grid, colors_4, f"{output_dir}/rule_04_{init_type}.png")

    # ----------------------------------------------------
    # RULE 5: EPR Entanglement and Causal Collapse
    # N = 6. 0: vacuum, 1: source, 2: R-mover, 3: L-mover, 4: Up-collapse, 5: Down-collapse
    # ----------------------------------------------------
    print("Simulating Rule 5...")
    colors_5 = np.array([
        [5, 5, 5],         # 0: pitch black
        [255, 255, 255],   # 1: bright white (source)
        [0, 255, 255],     # 2: cyan (right-mover)
        [0, 100, 255],     # 3: blue (left-mover)
        [255, 69, 0],      # 4: neon orange (spin-up)
        [50, 205, 50]      # 5: neon green (spin-down)
    ], dtype=np.uint8)
    
    p_meas = 0.015
    gamma_r5 = 0.004
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        stable = np.zeros(width, dtype=bool)
        
        sources = [400] if init_type == "single_seed" else [100, 200, 300, 400, 500, 600, 700]
        for src in sources:
            grid[0, src] = 1
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            stable_next = stable.copy()
            
            # Decays of stable collapse states (4 and 5)
            r_decay = np.random.random(width)
            decay_mask = stable & (r_decay < gamma_r5)
            S_next[decay_mask] = 0
            stable_next[decay_mask] = False
            
            # Right-mover propagation and collapse
            mask_2 = S == 2
            for x in np.where(mask_2)[0]:
                r = np.random.random()
                if r < p_meas:
                    # Collapse!
                    spin = 4 if np.random.random() < 0.5 else 5
                    S_next[x] = spin
                    stable_next[x] = True
                    # Start wave to the left
                    S_next[(x - 1) % width] = spin
                    stable_next[(x - 1) % width] = False
                else:
                    S_next[x] = 0
                    S_next[(x + 1) % width] = 2
                    stable_next[(x + 1) % width] = False
                    
            # Left-mover propagation and collapse detection
            mask_3 = S == 3
            for x in np.where(mask_3)[0]:
                wave_val = 0
                for offset in [1, 2]:
                    neighbor_state = S[(x + offset) % width]
                    neighbor_stable = stable[(x + offset) % width]
                    if neighbor_state in [4, 5] and not neighbor_stable:
                        wave_val = neighbor_state
                        break
                        
                if wave_val > 0:
                    S_next[x] = wave_val
                    stable_next[x] = True
                else:
                    S_next[x] = 0
                    S_next[(x - 1) % width] = 3
                    stable_next[(x - 1) % width] = False
                    
            # Propagating collapse waves moving left
            mask_wave = ~stable & ((S == 4) | (S == 5))
            for x in np.where(mask_wave)[0]:
                spin = S[x]
                S_next[x] = 0
                dest1 = (x - 1) % width
                dest2 = (x - 2) % width
                if dest2 not in sources and dest1 not in sources:
                    S_next[dest2] = spin
                    stable_next[dest2] = False
                    
            # Source updates and wave relaying
            for src in sources:
                wave_right = 0
                for offset in [1, 2]:
                    neighbor_state = S[(src + offset) % width]
                    neighbor_stable = stable[(src + offset) % width]
                    if neighbor_state in [4, 5] and not neighbor_stable:
                        wave_right = neighbor_state
                        break
                        
                wave_left = 0
                for offset in [-1, -2]:
                    neighbor_state = S[(src + offset) % width]
                    neighbor_stable = stable[(src + offset) % width]
                    if neighbor_state in [4, 5] and not neighbor_stable:
                        wave_left = neighbor_state
                        break
                        
                if wave_right > 0:
                    opp_spin = 5 if wave_right == 4 else 4
                    S_next[(src - 1) % width] = opp_spin
                    stable_next[(src - 1) % width] = False
                    S_next[(src - 2) % width] = opp_spin
                    stable_next[(src - 2) % width] = False
                elif wave_left > 0:
                    opp_spin = 5 if wave_left == 4 else 4
                    S_next[(src + 1) % width] = opp_spin
                    stable_next[(src + 1) % width] = False
                    S_next[(src + 2) % width] = opp_spin
                    stable_next[(src + 2) % width] = False
                else:
                    S_next[src] = 1
                    stable_next[src] = False
                    
            # Periodically emit new pairs
            emit_period = 150 if init_type == "single_seed" else 80
            if t % emit_period == 0:
                for src in sources:
                    if S_next[(src - 1) % width] == 0 and S_next[(src + 1) % width] == 0:
                        S_next[(src - 1) % width] = 3
                        S_next[(src + 1) % width] = 2
                        stable_next[(src - 1) % width] = False
                        stable_next[(src + 1) % width] = False
                        
            grid[t+1] = S_next
            stable = stable_next
            
        save_image(grid, colors_5, f"{output_dir}/rule_05_{init_type}.png")

    # ----------------------------------------------------
    # RULE 6: Quantum Wave Walk & Phase Interference
    # N = 5. 0: vacuum, 1: +, 2: -, 3: collapsed particle, 4: screen
    # ----------------------------------------------------
    print("Simulating Rule 6...")
    colors_6 = np.array([
        [12, 10, 36],      # 0: dark indigo
        [0, 245, 212],     # 1: cyan (positive amplitude)
        [241, 95, 255],    # 2: violet/pink (negative amplitude)
        [255, 228, 0],     # 3: electric yellow (collapsed particle)
        [112, 128, 144]    # 4: slate grey (screen)
    ], dtype=np.uint8)
    
    p_decay = 0.015
    p_collapse = 0.7
    p_prop = 0.95
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        
        screens = [150, 650] if init_type == "single_seed" else [100, 200, 300, 400, 500, 600, 700]
        for s_col in screens:
            grid[:, s_col] = 4
            
        if init_type == "single_seed":
            grid[0, 399] = 1
            grid[0, 401] = 2
        else:
            r = np.random.random(width)
            non_screens = [c for c in range(width) if c not in screens]
            for col in non_screens:
                if r[col] < 0.05:
                    grid[0, col] = 1
                elif r[col] < 0.10:
                    grid[0, col] = 2
                    
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            
            for s_col in screens:
                S_next[s_col] = 4
                
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            near_screen = (left_S == 4) | (right_S == 4)
            
            # Decay of collapsed particles (3)
            mask_3 = S == 3
            r_decay = np.random.random(width)
            S_next[mask_3] = np.where(r_decay[mask_3] < p_decay, 0, 3)
            
            # Wave collapse near screen
            mask_wave_near = ((S == 1) | (S == 2)) & near_screen
            if np.any(mask_wave_near):
                r_coll = np.random.random(width)
                S_next[mask_wave_near] = np.where(r_coll[mask_wave_near] < p_collapse, 3, 0)
                
            # Wave propagation & interference
            mask_update = (S != 4) & ~mask_3 & ~mask_wave_near
            if np.any(mask_update):
                left_contrib = np.where(left_S == 1, 1, np.where(left_S == 2, -1, 0))
                right_contrib = np.where(right_S == 1, 1, np.where(right_S == 2, -1, 0))
                A = left_contrib + right_contrib
                
                r_prop = np.random.random(width)
                val = np.zeros(width, dtype=int)
                
                val[A == 2] = np.where(r_prop[A == 2] < p_prop, 1, 0)
                val[A == -2] = np.where(r_prop[A == -2] < p_prop, 2, 0)
                val[A == 1] = np.where(r_prop[A == 1] < p_prop / 2, 1, 0)
                val[A == -1] = np.where(r_prop[A == -1] < p_prop / 2, 2, 0)
                
                S_next[mask_update] = val[mask_update]
                
            # Periodic wave injection in center
            if init_type == "single_seed":
                if t % 25 == 0:
                    S_next[398] = 1
                    S_next[402] = 2
                    
            grid[t+1] = S_next
            
        save_image(grid, colors_6, f"{output_dir}/rule_06_{init_type}.png")

    # ----------------------------------------------------
    # RULE 7: Dissipative Decoherence in a Thermal Bath
    # N = 4. 0: coherent, 1: dissipated, 2: noise, 3: ground
    # ----------------------------------------------------
    print("Simulating Rule 7...")
    colors_7 = np.array([
        [0, 100, 200],     # 0: deep blue (coherent)
        [255, 50, 50],     # 1: neon red (dissipated)
        [255, 215, 0],     # 2: golden yellow (thermal noise)
        [20, 20, 20]       # 3: dark grey/black (ground state)
    ], dtype=np.uint8)
    
    p_decay = 0.35
    p_diss = 0.75
    p_relax = 0.12
    p_drive = 0.04
    p_th_ex = 0.22
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        theta = 0.003 if init_type == "single_seed" else 0.03
        
        if init_type == "single_seed":
            grid[0] = 3
            grid[0, 250:550] = 0
        else:
            r = np.random.random(width)
            grid[0] = np.where(r < 0.4, 0, np.where(r < 0.8, 3, np.where(r < 0.9, 1, 2)))
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            
            # Spontaneous noise generation
            r_noise = np.random.random(width)
            noise_mask = (S != 2) & (r_noise < theta)
            
            # State 2 decay
            mask_2 = S == 2
            r_decay = np.random.random(width)
            S_next[mask_2] = np.where(r_decay[mask_2] < p_decay, 3, 2)
            
            # State 1 relaxation
            mask_1 = S == 1
            r_relax = np.random.random(width)
            S_next[mask_1] = np.where(r_relax[mask_1] < p_relax, 3, 1)
            
            # State 0 dissipation
            mask_0 = S == 0
            near_noise = (left_S == 2) | (right_S == 2)
            r_diss = np.random.random(width)
            S_next[mask_0 & near_noise] = np.where(r_diss[mask_0 & near_noise] < p_diss, 1, 0)
            
            # State 3 transitions
            mask_3 = S == 3
            if np.any(mask_3):
                r_drive = np.random.random(width)
                r_ex = np.random.random(width)
                near_noise_3 = (left_S == 2) | (right_S == 2)
                
                th_ex_cond = mask_3 & near_noise_3
                S_next[th_ex_cond] = np.where(r_ex[th_ex_cond] < p_th_ex, 1,
                                              np.where(r_drive[th_ex_cond] < p_drive, 0, 3))
                
                std_drive_cond = mask_3 & ~near_noise_3
                S_next[std_drive_cond] = np.where(r_drive[std_drive_cond] < p_drive, 0, 3)
                
            S_next[noise_mask] = 2
            grid[t+1] = S_next
            
        save_image(grid, colors_7, f"{output_dir}/rule_07_{init_type}.png")

    # ----------------------------------------------------
    # RULE 8: Penrose Gravitational Self-Energy Collapse
    # N = 5. 0: flat space, 1: mass A, 2: mass B, 3: strain, 4: classical mass
    # ----------------------------------------------------
    print("Simulating Rule 8...")
    colors_8 = np.array([
        [10, 12, 18],      # 0: deep space background
        [0, 255, 128],     # 1: neon emerald green (mass A)
        [0, 128, 255],     # 2: neon teal (mass B)
        [180, 0, 255],     # 3: electric purple (gravitational strain)
        [255, 230, 0]      # 4: bright yellow (classical mass)
    ], dtype=np.uint8)
    
    alpha = 0.28
    p_strain = 0.75
    p_relax = 0.08
    p_branch = 0.05
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        if init_type == "single_seed":
            grid[0, 396] = 1
            grid[0, 404] = 2
        else:
            r = np.random.random(width)
            grid[0] = np.where(r < 0.95, 0, np.where(r < 0.975, 1, 2))
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            
            # State 3 relaxation
            mask_3 = S == 3
            near_mass = (left_S == 1) | (left_S == 2) | (S == 1) | (S == 2) | (right_S == 1) | (right_S == 2)
            r_relax = np.random.random(width)
            S_next[mask_3 & ~near_mass] = np.where(r_relax[mask_3 & ~near_mass] < p_relax, 0, 3)
            
            # Superposition states A & B (1 & 2)
            mask_super = (S == 1) | (S == 2)
            r_coll = np.random.random(width)
            
            strain_count = (left_S == 3).astype(int) + (S == 3).astype(int) + (right_S == 3).astype(int)
            p_collapse = np.minimum(1.0, alpha * strain_count)
            
            for x in np.where(mask_super)[0]:
                s_val = S[x]
                p_c = p_collapse[x]
                if r_coll[x] < p_c:
                    S_next[x] = 4 if np.random.random() < 0.5 else 0
                else:
                    xl = (x - 1) % width
                    if S[xl] == 0:
                        if np.random.random() < p_branch:
                            S_next[xl] = s_val
                    xr = (x + 1) % width
                    if S[xr] == 0:
                        if np.random.random() < p_branch:
                            S_next[xr] = s_val
                            
            # State 0 strain generation
            mask_0 = S == 0
            if np.any(mask_0):
                r_strain = np.random.random(width)
                near_super = (left_S == 1) | (left_S == 2) | (right_S == 1) | (right_S == 2)
                cond_strain = mask_0 & near_super
                still_0 = S_next[cond_strain] == 0
                S_next[cond_strain] = np.where(still_0, np.where(r_strain[cond_strain] < p_strain, 3, 0), S_next[cond_strain])
                
            grid[t+1] = S_next
            
        save_image(grid, colors_8, f"{output_dir}/rule_08_{init_type}.png")

    # ----------------------------------------------------
    # RULE 9: Topological Majorana Protection
    # N = 5. 0: vacuum, 1: wire, 2: Majorana mode, 3: noise, 4: poisoned
    # ----------------------------------------------------
    print("Simulating Rule 9...")
    colors_9 = np.array([
        [25, 25, 30],      # 0: charcoal grey
        [218, 165, 32],    # 1: golden wire
        [0, 255, 255],     # 2: electric cyan (Majorana mode)
        [255, 0, 255],     # 3: neon magenta (noise)
        [220, 20, 60]      # 4: crimson (poisoned state)
    ], dtype=np.uint8)
    
    p_noise_decay = 0.55
    p_recovery = 0.08
    p_leak = 0.04
    p_poison = 0.85
    eta_noise = 0.015
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        
        # Static wire configuration
        if init_type == "single_seed":
            wires = [(200, 250), (380, 420), (550, 600)]
        else:
            wires = [(80, 120), (180, 220), (280, 320), (380, 420), (480, 520), (580, 620), (680, 720)]
            
        for start, end in wires:
            grid[:, start:end+1] = 1
            
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            
            # Enforce static wires
            for start, end in wires:
                S_next[start:end+1] = 1
                
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            left_2 = np.roll(S, 2)
            right_2 = np.roll(S, -2)
            
            # Noise decay
            mask_3 = S == 3
            r_decay = np.random.random(width)
            S_next[mask_3] = np.where(r_decay[mask_3] < p_noise_decay, 0, 3)
            
            # Recovery of poisoned mode
            mask_4 = S == 4
            r_rec = np.random.random(width)
            S_next[mask_4] = np.where(r_rec[mask_4] < p_recovery, 0, 4)
            
            # Majorana mode updates
            mask_2 = S == 2
            if np.any(mask_2):
                r_mode = np.random.random(width)
                noise_left1 = left_S == 3
                noise_left2 = left_2 == 3
                noise_right1 = right_S == 3
                noise_right2 = right_2 == 3
                
                noise_count = (noise_left1.astype(int) + noise_left2.astype(int) +
                               noise_right1.astype(int) + noise_right2.astype(int))
                noise_both = noise_left1 & noise_right1
                
                poison_cond = mask_2 & (noise_both | (noise_count >= 2))
                S_next[poison_cond] = np.where(r_mode[poison_cond] < p_poison, 4, 2)
                
                leak_cond = mask_2 & ~poison_cond & ((left_S == 3) | (right_S == 3))
                S_next[leak_cond] = np.where(r_mode[leak_cond] < p_leak, 4, 2)
                
            # Noise absorption by Majorana mode
            if np.any(mask_3):
                near_mode = (left_S == 2) | (right_S == 2)
                r_absorb = np.random.random(width)
                absorb_mask = mask_3 & near_mode
                still_3 = S_next == 3
                absorb_cond = absorb_mask & still_3
                if np.any(absorb_cond):
                    S_next[absorb_cond] = np.where(r_absorb[absorb_cond] < 0.96, 0, 3)
                
            # Spontaneous noise & Majorana nucleation
            mask_0 = S == 0
            if np.any(mask_0):
                r_noise = np.random.random(width)
                noise_gen = mask_0 & (r_noise < eta_noise)
                S_next[noise_gen] = 3
                
                wire_end_left = (left_S == 1) & (left_2 != 1)
                wire_end_right = (right_S == 1) & (right_2 != 1)
                nuc_cond = mask_0 & ~noise_gen & (wire_end_left | wire_end_right)
                S_next[nuc_cond] = 2
                
            grid[t+1] = S_next
            
        save_image(grid, colors_9, f"{output_dir}/rule_09_{init_type}.png")

    # ----------------------------------------------------
    # RULE 10: Delayed-Choice Quantum Eraser
    # N = 5. 0: vacuum, 1: marked path, 2: erased path, 3: eraser, 4: peak
    # ----------------------------------------------------
    print("Simulating Rule 10...")
    colors_10 = np.array([
        [15, 10, 25],      # 0: very dark violet
        [50, 205, 50],     # 1: lime green (marked path)
        [30, 144, 255],    # 2: sky blue (erased path)
        [255, 140, 0],     # 3: bright orange (eraser)
        [255, 20, 147]     # 4: hot pink (interference peak)
    ], dtype=np.uint8)
    
    p_erase = 0.88
    p_interf = 0.92
    p_decay_r10 = 0.015
    
    for init_type in ["single_seed", "random"]:
        grid = np.zeros((steps, width), dtype=np.int32)
        
        # Eraser regions
        eraser_cols = [(280, 320), (480, 520)] if init_type == "single_seed" else [(150, 180), (350, 380), (550, 580)]
        for start, end in eraser_cols:
            grid[:, start:end+1] = 3
            
        if init_type == "single_seed":
            grid[0, 100] = 1
            grid[0, 700] = 1
        else:
            r = np.random.random(width)
            for col in range(width):
                is_eraser = any(start <= col <= end for start, end in eraser_cols)
                if not is_eraser and r[col] < 0.05:
                    grid[0, col] = 1
                    
        for t in range(steps - 1):
            S = grid[t]
            S_next = S.copy()
            
            # Enforce static erasers
            for start, end in eraser_cols:
                S_next[start:end+1] = 3
                
            left_S = np.roll(S, 1)
            right_S = np.roll(S, -1)
            left_2 = np.roll(S, 2)
            right_2 = np.roll(S, -2)
            
            # Peak decay
            mask_4 = S == 4
            r_decay = np.random.random(width)
            S_next[mask_4] = np.where(r_decay[mask_4] < p_decay_r10, 0, 4)
            
            # Vacuum updates
            mask_0 = S == 0
            if np.any(mask_0):
                r_interf = np.random.random(width)
                r_erase = np.random.random(width)
                
                # Collision of state 2 from left and right
                coll_2 = (left_S == 2) & (right_S == 2)
                cond_coll = mask_0 & coll_2
                S_next[cond_coll] = np.where(r_interf[cond_coll] < p_interf, 4, 0)
                
                # Propagation of state 2
                prop_2 = (left_S == 2) | (right_S == 2)
                cond_prop2 = mask_0 & ~coll_2 & prop_2
                S_next[cond_prop2] = 2
                
                # Emerge as 2 from eraser
                emerge_left = (left_S == 3) & (left_2 == 1)
                emerge_right = (right_S == 3) & (right_2 == 1)
                cond_emerge = mask_0 & ~coll_2 & ~prop_2 & (emerge_left | emerge_right)
                S_next[cond_emerge] = np.where(r_erase[cond_emerge] < p_erase, 2, 0)
                
                # Standard propagation of state 1
                prop_1 = (left_S == 1) | (right_S == 1)
                cond_prop1 = mask_0 & ~coll_2 & ~prop_2 & ~cond_emerge & prop_1
                S_next[cond_prop1] = 1
                
            # Periodic injection for single seed
            if init_type == "single_seed":
                if t % 140 == 0:
                    S_next[100] = 1
                    S_next[700] = 1
                    
            grid[t+1] = S_next
            
        save_image(grid, colors_10, f"{output_dir}/rule_10_{init_type}.png")
        
    print("All simulations completed successfully!")

if __name__ == "__main__":
    main()
