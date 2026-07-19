# Loop 22 Cellular Automata Rules: Quantum Decoherence & Wavefunction Collapse

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Quantum Decoherence & Wavefunction Collapse**. 

These rules model quantum state superpositions, probabilistic collapse triggers (like the GRW dynamical collapse model), quantum tunneling through potential barriers, phase transitions under environmental measurement noise, the Quantum Zeno and Anti-Zeno effects, non-local Einstein-Podolsky-Rosen (EPR) entanglement, wave-particle duality with phase interference, thermal dissipation, gravity-induced collapse (Diosi-Penrose criterion), topological Majorana protection, and delayed-choice quantum erasers. Each rule is defined for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The updates are probabilistic, simulating quantum mechanical uncertainty.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Spontaneous Localization (GRW Collapse)](#rule-1-spontaneous-localization-grw-collapse) | 4 | Radius $r=1$ | Spontaneous localization triggers propagating collapse chains | Spreading coherent triangles suddenly collapsing into narrow classical lines |
| **2** | [Quantum Tunneling through Barriers](#rule-2-quantum-tunneling-through-barriers) | 4 | Radius $r=2$ | Probabilistic transmission and reflection at potential barriers | Diagonal particle paths splitting and reflecting at static barrier lines |
| **3** | [Environmental Decoherence Phase Transition](#rule-3-environmental-decoherence-phase-transition) | 3 | Radius $r=1$ | Localized noise fluctuations causing collapse of coherent phase | Transition from ordered coherent domains to disordered classical mixtures |
| **4** | [Quantum Zeno & Anti-Zeno Dynamics](#rule-4-quantum-zeno--anti-zeno-dynamics) | 4 | Radius $r=1$ | Measurement pulse frequency freezing or accelerating transitions | Dark, frozen Zeno trails and bright, excited Anti-Zeno bands |
| **5** | [EPR Entanglement and Causal Collapse](#rule-5-epr-entanglement-and-causal-collapse) | 6 | Radius $r=2$ | Retro-propagated collapse waves enforcing anti-correlated spins | Symmetrical paths collapsing into identical, opposite-colored tracks |
| **6** | [Quantum Wave Walk & Phase Interference](#rule-6-quantum-wave-walk--phase-interference) | 5 | Radius $r=1$ | Positive and negative wave amplitudes canceling or reinforcing | Intersecting waves canceling (destructive) or forming screen peaks |
| **7** | [Dissipative Decoherence in a Thermal Bath](#rule-7-dissipative-decoherence-in-a-thermal-bath) | 4 | Radius $r=1$ | Temperature-dependent energy dissipation into environmental bath | Coherent fields fragmented by thermal sparks, relaxing to ground state |
| **8** | [Penrose Gravitational Self-Energy Collapse](#rule-8-penrose-gravitational-self-energy-collapse) | 5 | Radius $r=1$ | Spacetime strain accumulating from superposition differences | Branching superpositions collapsing into asymmetric classical mass lines |
| **9** | [Topological Majorana Protection](#rule-9-topological-majorana-protection) | 5 | Radius $r=2$ | Qubits protected against local noise except paired poisoning | Resilient wire endpoints absorbing noise, failing only under dual hits |
| **10** | [Delayed-Choice Quantum Eraser](#rule-10-delayed-choice-quantum-eraser) | 5 | Radius $r=1$ | Erasing "which-way" markers to restore interference | Parallel paths merging into stable interference peaks after erasure |

---

## Rule Definitions

### Rule 1: Spontaneous Localization (GRW Collapse)
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Quantum vacuum / ground state ($|0\rangle$).
  * State $1$: Coherent, delocalized wave packet ($\psi$).
  * State $2$: Collapsed spin-up particle ($|\uparrow\rangle$).
  * State $3$: Collapsed spin-down particle ($|\downarrow\rangle$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    - The cell becomes excited by a neighboring wave packet:
      $$S_{t+1}(x) = \begin{cases}
      1 & \text{with probability } p_s \text{ if } (S_t(x-1) = 1 \text{ or } S_t(x+1) = 1) \text{ and } S_t(x-1), S_t(x+1) \notin \{2, 3\} \\
      0 & \text{otherwise}
      \end{cases}$$
  - If $s = 1$:
    - The cell can spontaneously collapse with rate $\lambda$:
      $$S_{t+1}(x) = \begin{cases}
      2 & \text{with probability } \lambda/2 \\
      3 & \text{with probability } \lambda/2
      \end{cases}$$
    - If no spontaneous collapse occurs (probability $1 - \lambda$), the cell checks for adjacent collapsed classical states to trigger an induced collapse chain (enforcing spatial wavefunction collapse):
      - If $S_t(x-1) = c \in \{2, 3\}$ and $S_t(x+1) \notin \{2, 3\}$:
        $$S_{t+1}(x) = \begin{cases}
        c & \text{with probability } p_c \\
        0 & \text{with probability } 1 - p_c
        \end{cases}$$
      - If $S_t(x+1) = c \in \{2, 3\}$ and $S_t(x-1) \notin \{2, 3\}$:
        $$S_{t+1}(x) = \begin{cases}
        c & \text{with probability } p_c \\
        0 & \text{with probability } 1 - p_c
        \end{cases}$$
      - If $S_t(x-1) = c_1 \in \{2, 3\}$ and $S_t(x+1) = c_2 \in \{2, 3\}$:
        $$S_{t+1}(x) = \begin{cases}
        c_1 & \text{with probability } p_c/2 \\
        c_2 & \text{with probability } p_c/2 \\
        0 & \text{with probability } 1 - p_c
        \end{cases}$$
      - If neither neighbor is in $\{2, 3\}$, the cell remains $1$: $S_{t+1}(x) = 1$.
  - If $s \in \{2, 3\}$:
    - The collapsed state slowly decays back to vacuum:
      $$S_{t+1}(x) = \begin{cases}
      0 & \text{with probability } \gamma \\
      s & \text{with probability } 1 - \gamma
      \end{cases}$$
* **Mathematical/Physical Rationale:** Models the Ghirardi-Rimini-Weber (GRW) dynamical collapse theory. Wavefunctions propagate coherently as spatial superpositions (state 1), but are subject to spontaneous, localized collapse events ($\lambda$). A single collapse seed triggers an extremely fast cascade: neighboring coherent waves collapse to the same eigenvalue ($2$ or $3$) or vanish ($0$) to represent conservation of total probability density ($|\psi|^2$).
* **Expected Visual Behavior:** Broad, spreading triangular regions of state 1 that suddenly crystallize into thin vertical lines of state 2 or 3, flanked immediately by empty space (state 0), representing localized particles.

---

### Rule 2: Quantum Tunneling through Barriers
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Free space ($[\emptyset]$).
  * State $1$: Right-moving wave packet ($|\psi_R\rangle$).
  * State $2$: Static potential barrier ($V$).
  * State $3$: Left-moving reflected wave packet ($|\psi_L\rangle$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 2$:
    $$S_{t+1}(x) = 2$$
  - If $s = 1$:
    - If $S_t(x+1) = 2$:
      $$S_{t+1}(x) = \begin{cases}
      3 & \text{with probability } 1 - p_{tunnel} \quad (\text{reflects}) \\
      0 & \text{with probability } p_{tunnel} \quad (\text{tunnels})
      \end{cases}$$
    - Else: $S_{t+1}(x) = 0$ (propagates forward).
  - If $s = 3$:
    - If $S_t(x-1) = 2$:
      $$S_{t+1}(x) = \begin{cases}
      1 & \text{with probability } 1 - p_{tunnel} \quad (\text{reflects}) \\
      0 & \text{with probability } p_{tunnel} \quad (\text{tunnels})
      \end{cases}$$
    - Else: $S_{t+1}(x) = 0$ (propagates forward).
  - If $s = 0$:
    - Define indicators for incoming particles:
      - $in_R = 1$ if ($S_t(x-1) = 1$ and $S_t(x) \neq 2$ and $S_t(x+1) \neq 2$), else $0$.
      - $tunnel_R = 1$ if ($S_t(x-2) = 1$ and $S_t(x-1) = 2$), else $0$.
      - $in_L = 1$ if ($S_t(x+1) = 3$ and $S_t(x) \neq 2$ and $S_t(x-1) \neq 2$), else $0$.
      - $tunnel_L = 1$ if ($S_t(x+2) = 3$ and $S_t(x+1) = 2$), else $0$.
    - The new state is resolved as:
      $$S_{t+1}(x) = \begin{cases}
      1 & \text{if } tunnel_R = 1 \text{ with probability } p_{tunnel} \\
      3 & \text{if } tunnel_L = 1 \text{ with probability } p_{tunnel} \\
      1 & \text{else if } in_R = 1 \text{ and } in_L = 0 \\
      3 & \text{else if } in_L = 1 \text{ and } in_R = 0 \\
      0 & \text{otherwise}
      \end{cases}$$
* **Mathematical/Physical Rationale:** Models the quantum mechanical tunneling of a particle through a potential barrier. A propagating wave packet moves deterministically in free space. Upon striking a barrier (state 2), the transition function resolves the wave's state probabilistically, reflecting it ($1 - p_{tunnel}$) or transmitting it past the barrier ($p_{tunnel}$).
* **Expected Visual Behavior:** Diagonal lines of state 1 (moving right) and state 3 (moving left) collide with a vertical static line of state 2. The incident line splits: a weaker diagonal line continues on the other side of the barrier (tunneling), while a brighter diagonal line propagates backward (reflection).

---

### Rule 3: Environmental Decoherence Phase Transition
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Classical ground state / dephased vacuum ($|0\rangle$).
  * State $1$: Coherent superposition state ($|+\rangle$).
  * State $2$: Environmental noise / measurement fluctuation ($\sigma_z$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 2$:
    - Noise decays back to the vacuum:
      $$S_{t+1}(x) = \begin{cases}
      0 & \text{with probability } p_{decay} \\
      2 & \text{with probability } 1 - p_{decay}
      \end{cases}$$
  - If $s = 0$:
    - Noise is generated spontaneously:
      $$S_{t+1}(x) = 2 \text{ with probability } \eta$$
    - If no noise is generated (probability $1 - \eta$), the cell can be excited by adjacent coherence:
      - If ($S_t(x-1) = 1$ or $S_t(x+1) = 1$) and neither is 2:
        $$S_{t+1}(x) = 1 \text{ with probability } p_{spread}$$
      - Otherwise, $S_{t+1}(x) = 0$.
  - If $s = 1$:
    - The cell dephases if exposed to noise:
      - If $S_t(x-1) = 2$ or $S_t(x+1) = 2$:
        $$S_{t+1}(x) = 0 \text{ with probability } p_{decoh}$$
      - Otherwise, the cell remains in state 1: $S_{t+1}(x) = 1$.
* **Mathematical/Physical Rationale:** Models the competition between coherence propagation ($p_{spread}$) and environmental dephasing ($p_{decoh}$). Noise is modeled as localized fluctuations ($\eta$) that disrupt the phase. When noise density exceeds a critical threshold $\eta_c$, the system undergoes a second-order phase transition from an ordered, coherent state (percolating state 1) to a disordered classical mixture (dominated by state 0 and transient noise).
* **Expected Visual Behavior:** At low noise $\eta$, large solid blocks of state 1 dominate the space-time grid. As $\eta$ increases, fractal-like boundaries form, and above the threshold $\eta_c$, coherence is completely suppressed, leaving only isolated, short-lived sparks of state 1.

---

### Rule 4: Quantum Zeno & Anti-Zeno Dynamics
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Unstable ground state ($|g\rangle$).
  * State $1$: Excited state ($|e\rangle$).
  * State $2$: Slow measurement pulse ($M_{slow}$).
  * State $3$: Fast measurement pulse ($M_{fast}$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s \in \{2, 3\}$:
    - Measurement pulses propagate as constant velocity waves:
      - State 2 moves rightward: $S_{t+1}(x) = 2$ if $S_t(x-1) = 2$, and $S_{t+1}(x) = 0$ otherwise.
      - State 3 moves leftward: $S_{t+1}(x) = 3$ if $S_t(x+1) = 3$, and $S_{t+1}(x) = 0$ otherwise.
  - If $s = 0$:
    - If a fast measurement pulse (3) is adjacent ($S_t(x-1) = 3$ or $S_t(x+1) = 3$):
      - The cell is measured projectively, freezing it in the ground state. It transitions to 1 with a very small Zeno probability:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{with probability } p_{zeno} \quad (p_{zeno} \ll p_{trans}) \\
        0 & \text{with probability } 1 - p_{zeno}
        \end{cases}$$
    - If a slow measurement pulse (2) is adjacent ($S_t(x-1) = 2$ or $S_t(x+1) = 2$):
      - The measurement stimulates transitions (Anti-Zeno):
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{with probability } p_{az} \quad (p_{az} > p_{trans}) \\
        0 & \text{with probability } 1 - p_{az}
        \end{cases}$$
    - If no measurement pulse is adjacent:
      - The cell undergoes standard natural transition to the excited state:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{with probability } p_{trans} \\
        0 & \text{with probability } 1 - p_{trans}
        \end{cases}$$
  - If $s = 1$:
    - The excited state naturally decays back to the ground state:
      $$S_{t+1}(x) = \begin{cases}
      0 & \text{with probability } p_{decay} \\
      1 & \text{with probability } 1 - p_{decay}
      \end{cases}$$
* **Mathematical/Physical Rationale:** In quantum mechanics, observing a system prevents it from changing (Zeno). Conversely, if the measurement interval matches the transition dynamics appropriately, it can accelerate decay (Anti-Zeno). This rule simulates this by modifying the excitation probability of state 0 based on the frequency (or speed/type) of passing measurement waves.
* **Expected Visual Behavior:** Background transitions of $0 \to 1 \to 0$ create a flickering pattern. When a fast measurement line (state 3) crosses, it leaves a dark, unexcited trail (Zeno freeze). When a slow measurement line (state 2) crosses, it leaves a bright, highly excited trail of state 1 (Anti-Zeno transition).

---

### Rule 5: EPR Entanglement and Causal Collapse
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Vacuum / unentangled space ($[\emptyset]$).
  * State $1$: Entangled pair source ($E$).
  * State $2$: Right-moving entangled particle ($e_R$).
  * State $3$: Left-moving entangled particle ($e_L$).
  * State $4$: Collapsed spin-up / Up-collapse wave ($|\uparrow\rangle$).
  * State $5$: Collapsed spin-down / Down-collapse wave ($|\downarrow\rangle$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$ (Source):
    - Periodically emits entangled pairs with probability $p_{emit}$:
      - If $S_t(x-1) = 0$ and $S_t(x+1) = 0$: $S_{t+1}(x-1) = 3$, $S_{t+1}(x+1) = 2$.
    - If it receives an Up-collapse wave (4) from the right ($S_t(x+1) = 4$):
      - It sends a Down-collapse wave (5) to the left: $S_{t+1}(x-1) = 5$.
    - If it receives a Down-collapse wave (5) from the right ($S_t(x+1) = 5$):
      - It sends an Up-collapse wave (4) to the left: $S_{t+1}(x-1) = 4$.
    - Same correlation applies for waves arriving from the left (relaying the opposite spin to the right).
    - Otherwise, $S_{t+1}(x) = 1$.
  - If $s = 2$ (Right-mover):
    - With probability $p_{meas}$ (spontaneous measurement fluctuation in space), it collapses:
      $$S_{t+1}(x) = \begin{cases}
      4 & \text{with probability } 0.5 \quad (\text{collapses to spin-up, sends Up wave left}) \\
      5 & \text{with probability } 0.5 \quad (\text{collapses to spin-down, sends Down wave left})
      \end{cases}$$
    - Otherwise, it propagates: if $S_t(x-1) = 2$, then $S_{t+1}(x) = 2$, and the old cell becomes 0.
  - If $s = 3$ (Left-mover):
    - It propagates: if $S_t(x+1) = 3$, then $S_{t+1}(x) = 3$, and the old cell becomes 0.
    - If it meets an incoming collapse wave from the source (say, state 4):
      - It instantly collapses to that state: $S_{t+1}(x) = 4$.
  - If $s \in \{4, 5\}$ (Collapse / wave states):
    - If it acts as a propagating collapse wave (moving towards the source):
      - State 4 moves left: $S_{t+1}(x) = 4$ if $S_t(x+1) = 4$.
      - State 5 moves left: $S_{t+1}(x) = 5$ if $S_t(x+1) = 5$.
    - If it is a stable collapsed particle (after correlation has been established):
      - Remains in state 4 or 5, decaying to 0 with a very small probability $\gamma$.
* **Mathematical/Physical Rationale:** To simulate the non-local correlation of EPR pairs in a local cellular automaton, the collapse of one particle (state 2) at a measurement site sends a retro-propagating collapse signal (state 4 or 5) back to the source (1). The source acts as a quantum relay, instantly sending the anti-correlated wave (5 or 4) to catch up with the other particle (3) and collapse it. This preserves the strict spin conservation ($S_{total} = 0$) across the entangled system.
* **Expected Visual Behavior:** The source is a central vertical line. Symmetrical diagonal lines (2 and 3) emerge from it. When one diagonal line randomly turns into a thick, colored line (4 or 5), a signal shoots back to the source, and a matching anti-correlated colored line emerges on the opposite side, creating perfectly symmetric, opposite-colored tracks.

---

### Rule 6: Quantum Wave Walk & Phase Interference
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum vacuum ($|0\rangle$).
  * State $1$: Positive wave amplitude ($|+\psi\rangle$).
  * State $2$: Negative wave amplitude ($|-\psi\rangle$).
  * State $3$: Collapsed classical particle ($P$).
  * State $4$: Measurement screen ($S$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 4$: $S_{t+1}(x) = 4$ (screen is static).
  - If $s = 3$:
    - The collapsed particle decays back to vacuum: $S_{t+1}(x) = 0$ with probability $p_{decay}$.
  - If $s = 1$ or $s = 2$:
    - Wave amplitudes propagate. A wave at $x$ splits and propagates to $x-1$ and $x+1$ at the next step.
    - If the wave is adjacent to a measurement screen (state 4):
      - It collapses into a classical particle (3) with probability $p_{collapse}$.
      - Otherwise, it decays to 0.
  - If $s = 0$:
    - We compute the net incoming amplitude from neighbors $x-1$ and $x+1$.
    - Let $A_{in}$ be the sum of incoming amplitudes.
      - Neighbor $x-1$ contributes $+1$ if $S_t(x-1) = 1$, and $-1$ if $S_t(x-1) = 2$.
      - Neighbor $x+1$ contributes $+1$ if $S_t(x+1) = 1$, and $-1$ if $S_t(x+1) = 2$.
    - The net amplitude is $A = A_{in}(x-1) + A_{in}(x+1)$.
    - The transition is determined by the interference:
      - If $A = +2$ (constructive positive): $S_{t+1}(x) = 1$ with probability $p_{prop}$.
      - If $A = -2$ (constructive negative): $S_{t+1}(x) = 2$ with probability $p_{prop}$.
      - If $A = 0$ (destructive interference): $S_{t+1}(x) = 0$ (the waves cancel out!).
      - If $A = +1$: $S_{t+1}(x) = 1$ with probability $p_{prop}/2$.
      - If $A = -1$: $S_{t+1}(x) = 2$ with probability $p_{prop}/2$.
* **Mathematical/Physical Rationale:** Models the superposition principle and wave-particle duality. Wave amplitudes can be positive or negative. When two waves of opposite signs meet, they interfere destructively, leading to complete cancellation ($A=0$). Same-sign waves interfere constructively, maintaining or reinforcing the wave propagation. Upon hitting the screen (state 4), the probability of collapsing to a particle (state 3) depends on the local wave intensity.
* **Expected Visual Behavior:** Intersecting diagonal paths of state 1 and 2. Where positive and negative paths cross, they vanish (destructive interference). Where identical phases cross, they continue strongly, eventually forming a spotty pattern of collapsed particles (state 3) on the measurement screen (state 4).

---

### Rule 7: Dissipative Decoherence in a Thermal Bath
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Coherent system state ($|\psi\rangle$).
  * State $1$: Dissipated bath state / thermal excitation ($|b\rangle$).
  * State $2$: Thermal bath fluctuation / heat source ($k_B T$).
  * State $3$: Fully decohered ground state ($|g\rangle$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 2$ (Thermal fluctuation):
    - Fluctuations are generated randomly in space with probability $\theta$ (representing bath temperature $T$).
    - They decay back to ground state with probability $p_{decay}$.
  - If $s = 0$ (Coherent state):
    - The coherent state is unstable under thermal noise. If $S_t(x-1) = 2$ or $S_t(x+1) = 2$:
      - The coherent state dissipates its phase energy into the bath:
        $$S_{t+1}(x) = 1 \text{ with probability } p_{diss} = e^{-\Delta E / T}$$
        where $T$ is modeled by the local fluctuation density, simplifying to a constant dissipation probability $p_{diss}$.
      - Otherwise, it remains coherent: $S_{t+1}(x) = 0$.
  - If $s = 1$ (Dissipated bath state):
    - The bath state quickly thermalizes and relaxes into the stable ground state:
      $$S_{t+1}(x) = \begin{cases}
      3 & \text{with probability } p_{relax} \\
      1 & \text{with probability } 1 - p_{relax}
      \end{cases}$$
  - If $s = 3$ (Ground state):
    - The ground state can be re-excited to the coherent state (0) by coherent driving:
      $$S_{t+1}(x) = 0 \text{ with probability } p_{drive}$$
    - Or it can be excited to a thermal bath state (1) by direct contact with noise:
      - If $S_t(x-1) = 2$ or $S_t(x+1) = 2$:
        $$S_{t+1}(x) = 1 \text{ with probability } p_{th\_ex}$$
* **Mathematical/Physical Rationale:** Models a quantum system undergoing dissipative decay. The coherent state (0) cannot survive in the presence of thermal fluctuations (2), which represent environmental degrees of freedom. Interaction triggers a transition to a dissipated state (1) before relaxing to the ground state (3), simulating the loss of quantum information to a thermal sink.
* **Expected Visual Behavior:** Solid regions of coherent state 0 are eaten away by noise particles (state 2), leaving behind a trail of state 1 which quickly settles into the dark background of state 3. High temperatures (high $\theta$) cause rapid, chaotic fragmentation, while low temperatures allow coherent domains to persist.

---

### Rule 8: Penrose Gravitational Self-Energy Collapse
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unperturbed flat spacetime ($|0\rangle$).
  * State $1$: Superposed mass state A ($|\psi_A\rangle$).
  * State $2$: Superposed mass state B ($|\psi_B\rangle$).
  * State $3$: Gravitational strain / self-energy ($E_G$).
  * State $4$: Collapsed classical mass ($M$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 4$ (Classical mass):
    - Stable state: $S_{t+1}(x) = 4$.
  - If $s = 3$ (Gravitational strain):
    - If no superposed states (1 or 2) are in the neighborhood, the strain relaxes to flat spacetime:
      $$S_{t+1}(x) = 0 \text{ with probability } p_{relax}$$
  - If $s = 0$ (Flat spacetime):
    - Spacetime gets curved by proximity to mass superpositions:
      - If $S_t(x-1) \in \{1, 2\}$ or $S_t(x+1) \in \{1, 2\}$:
        $$S_{t+1}(x) = 3 \text{ with probability } p_{strain}$$
  - If $s = 1$ or $s = 2$ (Superposition states):
    - The probability of collapse depends on the local gravitational strain $E_G$ (state 3) in the neighborhood.
    - Let $N_{strain}$ be the count of state 3 cells in $\{x-1, x, x+1\}$.
    - The collapse probability is $p_{collapse} = \alpha \cdot N_{strain}$, where $\alpha$ is the gravitational coupling constant.
    - At each step:
      - With probability $p_{collapse}$, the superposition collapses:
        - It collapses to classical mass (4) with probability $0.5$, or decays to vacuum (0) with probability $0.5$ (representing the mass localizing at the alternate superposition position).
      - If no collapse occurs, it maintains its superposition: $S_{t+1}(x) = s$.
* **Mathematical/Physical Rationale:** Penrose proposed that quantum superpositions of mass collapse due to the gravitational self-energy difference between the superposed states, which creates a "tension" in the fabric of spacetime. Here, state 1 and 2 represent the mass displacement. They generate gravitational strain (state 3). The accumulation of strain acts as a feedback mechanism that increases the probability of collapse to a localized classical mass (state 4).
* **Expected Visual Behavior:** Symmetrical branching structures of states 1 and 2 generating a surrounding halo of state 3. As the strain (3) accumulates, a sudden asymmetric collapse occurs: one branch terminates into vacuum (0) while the other crystallizes into a solid vertical line of classical mass (4).

---

### Rule 9: Topological Majorana Protection
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Trivial insulating vacuum.
  * State $1$: Topological phase boundary / wire ($T$).
  * State $2$: Protected Majorana bound state ($\gamma$).
  * State $3$: Local environmental noise / perturbation ($V_{noise}$).
  * State $4$: Decohered/Poisoned state ($D$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 3$ (Environmental noise):
    - Transient: $S_{t+1}(x) = 0$ with probability $p_{noise\_decay}$.
  - If $s = 4$ (Poisoned state):
    - Slowly recovers to vacuum: $S_{t+1}(x) = 0$ with probability $p_{recovery}$.
  - If $s = 1$ (Topological boundary):
    - Remains topological: $S_{t+1}(x) = 1$.
  - If $s = 2$ (Majorana mode):
    - Check for environmental noise in the neighborhood:
      - If there is noise (state 3) at $x-1$ or $x+1$, the mode is protected: the noise is absorbed, and the mode remains 2 (with probability $1 - p_{leak}$).
      - If noise (state 3) occurs simultaneously at both sides ($x-1$ and $x+1$) or is paired with another noise fluctuation, it can cause quasiparticle poisoning:
        $$S_{t+1}(x) = \begin{cases}
        4 & \text{with probability } p_{poison} \\
        2 & \text{with probability } 1 - p_{poison}
        \end{cases}$$
  - If $s = 0$ (Vacuum):
    - Spontaneous noise generation: $S_{t+1}(x) = 3$ with probability $\eta$.
    - If adjacent to a topological boundary (1) without noise, a Majorana mode can nucleate at the end of the wire:
      - If $S_t(x-1) = 1$ and $S_t(x-2) \neq 1$: $S_{t+1}(x) = 2$.
      - If $S_t(x+1) = 1$ and $S_t(x+2) \neq 1$: $S_{t+1}(x) = 2$.
* **Mathematical/Physical Rationale:** Majorana zero modes are topologically protected from local perturbations because their quantum information is stored non-locally. In this CA, a single noise source (state 3) touching the Majorana mode (state 2) is successfully absorbed or deflected due to topological protection. However, correlated noise or "quasiparticle poisoning" (noise on both sides of the boundary) breaks the protection, causing collapse into a poisoned, classical state (4).
* **Expected Visual Behavior:** Sizable vertical structures of state 1 (topological wire) capped with state 2 at the endpoints. Random noise sparks (state 3) continuously flash in the vacuum. When noise hits the endpoints (state 2), they remain stable. Only rarely, when multiple noise sparks hit the same endpoint simultaneously, does the endpoint flash into state 4, which then slowly decays back to 2.

---

### Rule 10: Delayed-Choice Quantum Eraser
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unmarked vacuum ($|0\rangle$).
  * State $1$: Photon path with "which-way" marker ($|\psi\rangle \otimes |w\rangle$).
  * State $2$: Photon path with erased marker ($|\psi\rangle$).
  * State $3$: Quantum eraser agent ($E$).
  * State $4$: Interference pattern peak ($I$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 3$ (Eraser) or $s = 4$ (Interference peak):
    - Static or slowly decaying structures: $S_{t+1}(x) = s$.
  - If $s = 1$ (Marked particle):
    - Propagates forward: if $S_t(x-1) = 1$ and $S_t(x) \neq 3$, then $S_{t+1}(x) = 1$.
    - If it hits the eraser (3): the marker is erased!
      $$S_{t+1}(x) = 2 \text{ with probability } p_{erase}$$
      $$S_{t+1}(x) = 0 \text{ with probability } 1 - p_{erase} \quad (\text{absorbed/scattered})$$
    - If it hits a detection boundary without eraser: it collapses classically to vacuum (0) without generating interference.
  - If $s = 2$ (Erased particle):
    - Propagates forward: if $S_t(x-1) = 2$, then $S_{t+1}(x) = 2$.
    - If two erased particles (2) collide at the same cell:
      - They undergo constructive interference, collapsing into a stable interference peak:
        $$S_{t+1}(x) = 4 \text{ with probability } p_{interf}$$
        $$S_{t+1}(x) = 0 \text{ with probability } 1 - p_{interf}$$
  - If $s = 0$ (Vacuum):
    - Becomes 1 if marked particle propagates into it: $S_{t+1}(x) = 1$ if $S_t(x-1) = 1$ and $S_t(x) \neq 3$.
    - Becomes 2 if erased particle propagates into it: $S_{t+1}(x) = 2$ if $S_t(x-1) = 2$.
* **Mathematical/Physical Rationale:** Models the recovery of quantum interference. If a particle has a "which-way" marker (state 1), its path is classical and it cannot interfere. However, passing through the eraser agent (state 3) removes this information, converting it to state 2. These erased particles are coherent wave packets that can interfere constructively upon collision (forming state 4), demonstrating that the presence or absence of "which-way" information determines the classical or quantum behavior.
* **Expected Visual Behavior:** Parallel diagonal paths of state 1 (marked paths). If they hit the screen directly, they disappear. However, if they pass through a block of state 3 (eraser), they turn into state 2. When these paths intersect, they form bright, stable vertical bands of state 4 (interference peaks).
