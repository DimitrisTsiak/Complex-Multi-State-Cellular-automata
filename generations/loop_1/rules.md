# Loop 1 Cellular Automata Rules: Multi-state Cyclic & Excitable Media

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Multi-state Cyclic and Excitable Media**. 

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules (where the horizontal axis represents space $x$ and the vertical axis represents time $t$) will generate visual structures ranging from rigid soliton pulses to turbulent chaotic mixtures.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Standard Cyclic Vortex](#rule-1-standard-cyclic-vortex) | 8 | Radius $r=2$ | Classic threshold cyclic CCA | Solid spiral-like domain bands |
| **2** | [Excitable Soliton Wave](#rule-2-excitable-soliton-wave) | 6 | Radius $r=1$ | Exact-excitation threshold excitable media | Soliton-like moving pulses |
| **3** | [Asymmetric Chiral Wave](#rule-3-asymmetric-chiral-wave) | 5 | Asymmetric $r=2$ | Directionally-weighted cyclic excitation | Sloped, drifting space-time waves |
| **4** | [Staged Excitation Cascade](#rule-4-staged-excitation-cascade) | 8 | Dual-range $r=1, 3$ | Nested multi-stage excitation | Concentric, multi-layered envelopes |
| **5** | [Cyclic Domination with Back-Inhibition](#rule-5-cyclic-domination-with-back-inhibition) | 4 | Radius $r=2$ | Predator-inhibited prey transition | Localized breathing structures and gliders |
| **6** | [Deterministic Chaos Excitable Media](#rule-6-deterministic-chaos-excitable-media) | 10 | Radius $r=2$ | Hashed pseudo-random excitation threshold | Turbulent, dendritic, and noisy waves |
| **7** | [Cyclic Double-Jump](#rule-7-cyclic-double-jump) | 6 | Radius $r=2$ | Multi-state skip logic based on density | Multi-frequency phase-locking and interference |
| **8** | [Heartbeat Excitation](#rule-8-heartbeat-excitation) | 12 | Radius $r=2$ | Refractory-dependent variable threshold | Self-organizing pacemakers and wave breaks |
| **9** | [Parity-Filtered Excitation](#rule-9-parity-filtered-excitation) | 7 | Radius $r=1$ | Algebraic parity filter on quiescent trigger | Sierpinski-like fractals within wave envelopes |
| **10** | [Velocity-Modulated Cyclic Wave](#rule-10-velocity-modulated-cyclic-wave) | 8 | Variable $r=1, 2$ | State-dependent neighborhood range | Compression-expansion wavefronts (shockwaves) |

---

## Rule Definitions

### Rule 1: Standard Cyclic Vortex
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $\mathbb{I}$ be the indicator function. The cell state advances to the next state modulo 8 if the number of neighbors in the next state is at least the threshold $T = 2$:
  $$S_{t+1}(x) = \begin{cases} 
  (S_t(x) + 1) \pmod 8 & \text{if } \sum_{y \in N(x)} \mathbb{I}(S_t(y) = (S_t(x) + 1) \pmod 8) \ge 2 \\ 
  S_t(x) & \text{otherwise} 
  \end{cases}$$
* **Mathematical Rationale:** This is the baseline 1D cyclic cellular automaton. A cell is only "eaten" by the next state if there is sufficient local pressure (at least 2 neighbors).
* **Expected Visual Behavior:** Spiral-like domain boundaries, periodic block patterns, and stable wavefronts that lock into constant velocity.

### Rule 2: Excitable Soliton Wave
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Quiescent (rest state).
  * State $1$: Excited.
  * States $2, 3, 4, 5$: Refractory (recovering states).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  * If a cell is quiescent ($S_t(x) = 0$), it becomes excited ($1$) if and only if **exactly one** of its neighbors is excited:
    $$S_{t+1}(x) = 1 \iff S_t(x) = 0 \text{ and } \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1) = 1$$
  * If a cell is already excited or refractory ($S_t(x) \ge 1$), it decays deterministically back to quiescent state:
    $$S_{t+1}(x) = \begin{cases}
    (S_t(x) + 1) \pmod 6 & \text{if } S_t(x) \ge 1 \text{ and } S_t(x) < 5 \\
    0 & \text{if } S_t(x) = 5
    \end{cases}$$
* **Mathematical Rationale:** The exact-excitation rule ($\text{count} = 1$) prevents excitation from spreading if it is overcrowded. This mimics the physical properties of solitons where opposing waves do not merge into a single massive wave but instead annihilate or pass through each other.
* **Expected Visual Behavior:** Highly stable, thin moving pulses (solitons) that travel diagonally. When two pulses collide, they can annihilate each other or pass through depending on the refractory trail.

### Rule 3: Asymmetric Chiral Wave
* **States ($N$):** $5$ states ($0, 1, \dots, 4$).
* **Neighborhood ($N(x)$):** Asymmetric radius $r=2$ favoring the left side:
  $$N(x) = \{x-2, x-1, x+1\}$$
  With weights $w(-2) = 1$, $w(-1) = 2$, and $w(1) = 1$.
* **Transition Function:**
  Let the weighted next-state neighbor count be:
  $$C_t(x) = \sum_{y \in N(x)} w(y - x) \cdot \mathbb{I}(S_t(y) = (S_t(x) + 1) \pmod 5)$$
  $$S_{t+1}(x) = \begin{cases}
  (S_t(x) + 1) \pmod 5 & \text{if } C_t(x) \ge 2 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Introducing spatial asymmetry in the neighborhood weights breaks chiral symmetry. The left-heavy weight distribution forces waves to propagate preferentially in one direction.
* **Expected Visual Behavior:** Drifting waves and sloped space-time structures. The entire diagram will exhibit a dominant diagonal flow direction.

### Rule 4: Staged Excitation Cascade
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State $0$: Quiescent.
  * States $1, 2$: Excited (Stage 1 and Stage 2).
  * States $3, 4, 5, 6, 7$: Refractory.
* **Neighborhoods ($N_{in}(x), N_{out}(x)$):**
  * Inner neighborhood: $N_{in}(x) = \{x-1, x+1\}$
  * Outer neighborhood: $N_{out}(x) = \{x-3, x-2, x+2, x+3\}$
* **Transition Function:**
  Let $E_t(y) = \mathbb{I}(S_t(y) \in \{1, 2\})$ represent whether a neighbor is excited.
  * If a cell is quiescent ($S_t(x) = 0$), it excites to state $1$ if there is at least one excited cell in either the inner or outer neighborhood:
    $$S_{t+1}(x) = 1 \iff S_t(x) = 0 \text{ and } \left( \sum_{y \in N_{in}(x)} E_t(y) \ge 1 \text{ or } \sum_{y \in N_{out}(x)} E_t(y) \ge 1 \right)$$
  * If a cell is active ($S_t(x) \ge 1$), it transitions to the next state:
    $$S_{t+1}(x) = \begin{cases}
    S_t(x) + 1 & \text{if } 1 \le S_t(x) < 7 \\
    0 & \text{if } S_t(x) = 7
    \end{cases}$$
* **Mathematical Rationale:** The division of excitation into two states (Stage 1 and 2) combined with a dual-range neighborhood check allows for multi-scale wave propagation. The outer neighborhood acts as a long-range jump mechanism, while the inner neighborhood preserves local continuity.
* **Expected Visual Behavior:** Nested, multi-layered wave envelopes. Large waves with smaller internal ripples, creating complex nested geometric shapes.

### Rule 5: Cyclic Domination with Back-Inhibition
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $c_{next}$ be the number of neighbors in state $(S_t(x) + 1) \pmod 4$:
  $$c_{next} = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = (S_t(x) + 1) \pmod 4)$$
  Let $c_{inhibit}$ be the number of neighbors in state $(S_t(x) + 2) \pmod 4$:
  $$c_{inhibit} = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = (S_t(x) + 2) \pmod 4)$$
  The transition is:
  $$S_{t+1}(x) = \begin{cases}
  (S_t(x) + 1) \pmod 4 & \text{if } c_{next} \ge 1 \text{ and } c_{inhibit} < 2 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** In a cyclic ecosystem (like Rock-Paper-Scissors), state $s$ is eaten by state $s+1$. However, we introduce back-inhibition: if state $s+2$ (the predator of $s+1$) is sufficiently present in the neighborhood, it inhibits the ability of $s+1$ to dominate $s$.
* **Expected Visual Behavior:** Localized, breathing structures (gliders or stationary oscillators) rather than continuous spreading waves. The back-inhibition blocks uniform propagation, creating localized complexity.

### Rule 6: Deterministic Chaos Excitable Media
* **States ($N$):** $10$ states ($0, 1, \dots, 9$).
  * State $0$: Quiescent.
  * State $1$: Excited.
  * States $2 \dots 9$: Refractory.
* **Neighborhood ($N_{all}(x), N_{exc}(x)$):** Radius $r=2$.
  * Full neighborhood (including self): $N_{all}(x) = \{x-2, x-1, x, x+1, x+2\}$
  * Excited neighborhood (excluding self): $N_{exc}(x) = \{x-2, x-1, x+1, x+2\}$
* **Transition Function:**
  Let a deterministic hash value $V_t(x)$ be computed as:
  $$V_t(x) = \sum_{i=-2}^{2} (i+3) \cdot S_t(x+i)$$
  Let $E_t(x) = \sum_{y \in N_{exc}(x)} \mathbb{I}(S_t(y) = 1)$.
  * A quiescent cell excites only if there is at least one excited neighbor and the local hash satisfies a modulo condition:
    $$S_{t+1}(x) = 1 \iff S_t(x) = 0 \text{ and } (V_t(x) \pmod 7 \in \{1, 3, 5\}) \text{ and } E_t(x) \ge 1$$
  * Active states decay deterministically:
    $$S_{t+1}(x) = (S_t(x) + 1) \pmod{10} \quad (\text{for } S_t(x) \ge 1)$$
* **Mathematical Rationale:** By gating the excitable trigger with a spatial hash function, we introduce pseudo-random deterministic noise. This represents spatial heterogeneity or turbulence in the medium.
* **Expected Visual Behavior:** Dendritic, highly textured, and turbulent patterns. The wavefronts will look "fuzzy" or chaotic, yet will respect the macro-scale refractory periods.

### Rule 7: Cyclic Double-Jump
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $c_1$ and $c_2$ represent counts of next-state and next-next-state neighbors:
  $$c_1 = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = (S_t(x) + 1) \pmod 6)$$
  $$c_2 = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = (S_t(x) + 2) \pmod 6)$$
  The transition is:
  $$S_{t+1}(x) = \begin{cases}
  (S_t(x) + 2) \pmod 6 & \text{if } c_2 \ge 2 \text{ and } c_1 < 2 \\
  (S_t(x) + 1) \pmod 6 & \text{else if } c_1 \ge 1 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Normally, cyclic automata only allow $s \to s+1$. Here, if the $s+2$ state is highly concentrated and $s+1$ is sparse, the cell undergoes a "double-jump" directly to $s+2$.
* **Expected Visual Behavior:** Multi-frequency wave interference. Waves can overtake one another, leading to phase-mixing and complex boundaries where waves of different velocities collide.

### Rule 8: Heartbeat Excitation
* **States ($N$):** $12$ states ($0, 1, \dots, 11$).
  * State $0$: Quiescent.
  * State $1$: Excited.
  * States $2 \dots 11$: Refractory.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $R_t(x)$ be the number of refractory cells in the neighborhood:
  $$R_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{2, 3, \dots, 11\})$$
  Let $E_t(x)$ be the number of excited cells in the neighborhood:
  $$E_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$$
  The excitation threshold $T(R_t(x))$ is state-dependent:
  $$T(R_t(x)) = \begin{cases} 1 & \text{if } R_t(x) \le 1 \\ 2 & \text{if } R_t(x) \ge 2 \end{cases}$$
  The transition is:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } E_t(x) \ge T(R_t(x)) \\
  (S_t(x) + 1) \pmod{12} & \text{if } S_t(x) \ge 1
  \end{cases}$$
* **Mathematical Rationale:** This rule models local tissue fatigue. If the neighborhood has many refractory cells, the current cell requires more excited inputs to fire. This mimics cardiac re-entry and localized blockages.
* **Expected Visual Behavior:** Self-organizing pacemaker centers and wave breaks. Instead of continuous stripes, we expect to see waves that fragment and form localized spiral-like sources.

### Rule 9: Parity-Filtered Excitation
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Quiescent.
  * State $1$: Excited.
  * States $2 \dots 6$: Refractory.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $Sum_t(x) = S_t(x-1) + S_t(x+1)$.
  * A quiescent cell excites if the sum of neighbor states is odd and non-zero:
    $$S_{t+1}(x) = 1 \iff S_t(x) = 0 \text{ and } (Sum_t(x) \pmod 2 \neq 0) \text{ and } Sum_t(x) > 0$$
  * Refractory decay is standard:
    $$S_{t+1}(x) = (S_t(x) + 1) \pmod 7 \quad (\text{for } S_t(x) \ge 1)$$
* **Mathematical Rationale:** This rule couples algebraic (parity-based) cellular automata (like Wolfram's Rule 90) with an excitable refractory cycle. The excitation is gated by parity rather than simple threshold summation.
* **Expected Visual Behavior:** Fractal-like patterns (e.g., Sierpinski triangles) embedded inside large-scale excitable wave envelopes. It creates a beautiful hybrid of discrete algebraic patterns and smooth physical wave structures.

### Rule 10: Velocity-Modulated Cyclic Wave
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
* **Neighborhoods ($N_1(x), N_2(x)$):**
  * Radius 1: $N_1(x) = \{x-1, x+1\}$
  * Radius 2: $N_2(x) = \{x-2, x-1, x+1, x+2\}$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $c_1$ and $c_2$ represent counts of next-state neighbors in the respective neighborhoods:
  $$c_1 = \sum_{y \in N_1(x)} \mathbb{I}(S_t(y) = (s+1) \pmod 8)$$
  $$c_2 = \sum_{y \in N_2(x)} \mathbb{I}(S_t(y) = (s+1) \pmod 8)$$
  The transition is:
  $$S_{t+1}(x) = \begin{cases}
  (s+1) \pmod 8 & \text{if } s \text{ is even and } c_1 \ge 1 \\
  (s+1) \pmod 8 & \text{if } s \text{ is odd and } c_2 \ge 2 \\
  s & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** By making the neighborhood size state-dependent, different phases of the cycle propagate at different speeds. Even states propagate locally and rapidly (threshold 1 at radius 1), whereas odd states propagate slower and require wider support (threshold 2 at radius 2).
* **Expected Visual Behavior:** Periodic compression and expansion of wavefronts. This leads to the formation of high-density shockwave fronts and low-density expansion zones in the space-time diagram.
