# Loop 2 Cellular Automata Rules: Multi-state Generations & Outer-Totalistic

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Multi-state Generations & Outer-Totalistic Media**. 

In this domain, cells transition through $N$ states: $\{0, 1, \dots, N-1\}$. State $0$ is the quiescent (dead) state, State $1$ is the active (alive) state, and states $2 \dots N-1$ are refractory (decaying) states. 

A key defining characteristic of this domain is that active cells (State 1) can survive (remain in State 1) under specific local conditions, unlike simple excitable media where active cells always decay immediately. Transition functions are outer-totalistic, depending on the cell's current state and total counts (or sums) of neighbor states.

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Standard Generations Baseline](#rule-1-standard-generations-baseline) | 4 | Radius $r=2$ | Baseline outer-totalistic birth/survival | Clean propagating hulls and gliders |
| **2** | [Parity-Gated Birth Generations](#rule-2-parity-gated-birth-generations) | 5 | Radius $r=2$ | Odd-active parity birth trigger | Sierpinski-like fractals in wave envelopes |
| **3** | [Refractory-Feedback Generations](#rule-3-refractory-feedback-generations) | 6 | Radius $r=2$ | Active density delays refractory decay | Persistent walls and breathing scars |
| **4** | [Chiral Drifting Generations](#rule-4-chiral-drifting-generations) | 4 | Asymmetric $r=3$ | Weighted left-heavy asymmetric neighborhood | Unidirectional drifting gliders and waves |
| **5** | [Dual-Threshold Density Generations](#rule-5-dual-threshold-density-generations) | 5 | Radius $r=3$ | Non-monotonic double-band birth/survival | Interference-rich textured crystal structures |
| **6** | [Refractory-Inhibited Birth Generations](#rule-6-refractory-inhibited-birth-generations) | 5 | Radius $r=2$ | Refractory count inhibits birth trigger | Self-limiting wavefronts and breathing particles |
| **7** | [Totalistic-Sum Generations](#rule-7-totalistic-sum-generations) | 5 | Radius $r=2$ (incl. self) | Transitions based on total state sum | Graded wavefronts and soft gradient colors |
| **8** | [Velocity-Modulated Range-Shifting](#rule-8-velocity-modulated-range-shifting) | 6 | Variable $r=1, 2$ | Refractory-density modulated neighborhood | Compression and expansion shockwave fronts |
| **9** | [Chaotic-Gate Generations](#rule-9-chaotic-gate-generations) | 8 | Radius $r=2$ | Spatial state-hash gating birth | Highly textured, dendritic, and turbulent growth |
| **10** | [Mutual-Exclusion Generations](#rule-10-mutual-exclusion-generations) | 6 | Radius $r=2$ | State-2 decay density gates birth/survival | Intricate self-pruning crystal growth and gliders |

---

## Rule Definitions

### Rule 1: Standard Generations Baseline
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Quiescent.
  * State $1$: Active (Alive).
  * States $2, 3$: Decaying (Refractory).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $A_t(x)$ be the count of active neighbors:
  $$A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) = 2 \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{1, 2\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin \{1, 2\} \\
  (S_t(x) + 1) \pmod 4 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** This establishes a baseline 1D Generations rule. It specifies birth under moderate density ($A=2$), survival under low-to-moderate density ($A \in \{1, 2\}$), and a simple 2-step decay cycle.
* **Expected Visual Behavior:** Clean, propagating diagonal lines, stable hull structures, and simple gliders.

### Rule 2: Parity-Gated Birth Generations
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quiescent.
  * State $1$: Active.
  * States $2, 3, 4$: Decaying.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$.
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) \in \{1, 3\} \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{1, 2\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin \{1, 2\} \\
  (S_t(x) + 1) \pmod 5 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** Coupling a parity rule (which generates Sierpinski-like fractals in dead space) with survival constraints and a longer 3-step refractory period to prevent uncontrolled growth.
* **Expected Visual Behavior:** Sierpinski triangles embedded within localized propagating envelopes, exhibiting periodic collapses and regenerations.

### Rule 3: Refractory-Feedback Generations
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Quiescent.
  * State $1$: Active.
  * States $2, 3, 4, 5$: Decaying.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself.
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$.
  * For quiescent and active cells:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) \in \{2, 3\} \\
    1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) = 2 \\
    2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \neq 2
    \end{cases}$$
  * For decaying cells ($S_t(x) \ge 2$):
    $$S_{t+1}(x) = \begin{cases}
    S_t(x) & \text{if } A_t(x) \ge 3 \\
    (S_t(x) + 1) \pmod 6 & \text{if } A_t(x) < 3
    \end{cases}$$
* **Mathematical Rationale:** We break the "unconditional decay" rule of standard Generations. If a decaying cell has a high density of active neighbors ($A_t(x) \ge 3$), it "resists" decay and remains in its current refractory state. This introduces local memory and feedback.
* **Expected Visual Behavior:** Stationary, breathing "scars" and persistent walls of refractory cells that block or shape propagating fronts.

### Rule 4: Chiral Drifting Generations
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
* **Neighborhood ($N_{asym}(x)$):** Asymmetric radius $r=3$ favoring the left side:
  $$N_{asym}(x) = \{x-3, x-2, x-1, x+1\}$$
  With spatial weights: $w(-1) = 2$, $w(-2) = 1$, $w(-3) = 1$, and $w(1) = 1$.
* **Transition Function:**
  Let the weighted sum of active neighbors be:
  $$W_t(x) = \sum_{y \in N_{asym}(x)} w(y - x) \cdot \mathbb{I}(S_t(y) = 1)$$
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } W_t(x) \in \{2, 3\} \\
  1 & \text{if } S_t(x) = 1 \text{ and } W_t(x) \in \{1, 2, 3\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } W_t(x) \notin \{1, 2, 3\} \\
  (S_t(x) + 1) \pmod 4 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** Spatial asymmetry in the neighborhood weights breaks chiral symmetry. The left-heavy weight distribution forces active waves and gliders to propagate preferentially in one direction.
* **Expected Visual Behavior:** Drifting waves and sloped space-time structures. The entire diagram will exhibit a dominant diagonal flow direction.

### Rule 5: Dual-Threshold Density Generations
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
* **Neighborhood ($N(x)$):** Radius $r=3$ excluding the cell itself:
  $$N(x) = \{x-3, x-2, x-1, x+1, x+2, x+3\}$$
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$.
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) \in \{2, 4\} \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{2, 3, 5\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin \{2, 3, 5\} \\
  (S_t(x) + 1) \pmod 5 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** Non-monotonic (double-banded) birth and survival sets create complex resonance. The system cannot stabilize into simple uniform blocks because intermediate or high densities trigger birth or death non-linearly.
* **Expected Visual Behavior:** Complex high-frequency interference patterns with nested chaotic bands.

### Rule 6: Refractory-Inhibited Birth Generations
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself.
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ (active neighbors).
  Let $R_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \ge 2)$ (refractory/decaying neighbors).
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) = 2 \text{ and } R_t(x) \le 1 \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{1, 2\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin \{1, 2\} \\
  (S_t(x) + 1) \pmod 5 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** In many physical systems, recovering regions release inhibitory chemicals. Here, if the neighborhood has too many refractory cells ($R_t(x) \ge 2$), it inhibits birth, restricting growth to clean, un-decayed regions.
* **Expected Visual Behavior:** Self-limiting wave boundaries, leading to localized breathing patterns and discrete, self-assembled gliders rather than chaotic overgrowth.

### Rule 7: Totalistic-Sum Generations
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
* **Neighborhood ($N_{all}(x)$):** Radius $r=2$ including the cell itself:
  $$N_{all}(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let the arithmetic sum of neighbor states be:
  $$K_t(x) = \sum_{y \in N_{all}(x)} S_t(y)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } K_t(x) \in \{3, 4, 5, 6\} \\
  1 & \text{if } S_t(x) = 1 \text{ and } K_t(x) \in \{4, 5, 6, 7\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } K_t(x) \notin \{4, 5, 6, 7\} \\
  (S_t(x) + 1) \pmod 5 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** In standard Generations, only state 1 affects the transition. Here, we sum the actual state values. Because refractory states (2, 3, 4) have higher numeric values, they exert a stronger totalistic influence, driving smoother transitions.
* **Expected Visual Behavior:** Graded wavefronts and soft textures. The space-time diagram will display color gradients rather than sharp boundaries, resembling reaction-diffusion waves.

### Rule 8: Velocity-Modulated Range-Shifting
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
* **Neighborhoods ($N_1(x), N_2(x)$):**
  * Narrow: $N_1(x) = \{x-1, x+1\}$ (radius 1)
  * Wide: $N_2(x) = \{x-2, x-1, x+1, x+2\}$ (radius 2)
* **Transition Function:**
  Let $R_t(x) = \sum_{y \in N_1(x)} \mathbb{I}(S_t(y) \ge 2)$ be the local refractory count.
  Select the active neighborhood $N_{use}(x)$ and conditions:
  * If $R_t(x) \ge 1$: Use $N_{use}(x) = N_2(x)$, and the birth/survival sets are $B = S = \{2, 3\}$.
  * If $R_t(x) = 0$: Use $N_{use}(x) = N_1(x)$, and the birth/survival sets are $B = S = \{1\}$.
  Let $A_t(x) = \sum_{y \in N_{use}(x)} \mathbb{I}(S_t(y) = 1)$.
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) \in B \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in S \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin S \\
  (S_t(x) + 1) \pmod 6 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** By making the neighborhood size and threshold state-dependent, propagation speed shifts. Waves traveling through clean space propagate locally and rapidly, whereas waves encountering refractory trails slow down and require wider support.
* **Expected Visual Behavior:** Periodic compression and expansion of wavefronts, creating shockwaves and expansion zones in the space-time diagram.

### Rule 9: Chaotic-Gate Generations
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$.
  Let the local state hash $V_t(x)$ be:
  $$V_t(x) = \sum_{i=-2}^{2} (i+3) \cdot S_t(x+i)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) = 2 \text{ and } (V_t(x) \pmod 3 \neq 0) \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{1, 2\} \\
  2 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \notin \{1, 2\} \\
  (S_t(x) + 1) \pmod 8 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** Gating the birth transition with a local spatial hash breaks structural symmetry and injects deterministic chaos, producing spatial patterns that resemble randomized media.
* **Expected Visual Behavior:** Highly textured, dendritic, and turbulent growth patterns with complex, fuzzy wave envelopes.

### Rule 10: Mutual-Exclusion Generations
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $A_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ (active neighbors).
  Let $D_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ (decaying-1 neighbors).
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) = 2 \text{ and } (D_t(x) \pmod 2 = 0) \\
  1 & \text{if } S_t(x) = 1 \text{ and } A_t(x) \in \{1, 2\} \text{ and } D_t(x) \le 1 \\
  2 & \text{if } S_t(x) = 1 \text{ and } \text{otherwise} \\
  (S_t(x) + 1) \pmod 6 & \text{if } S_t(x) \ge 2
  \end{cases}$$
* **Mathematical Rationale:** Both birth and survival are gated by the local density of state 2 (the immediate post-active state). State 2 cells represent immediate exhaustion of resource or localized toxicity, which halts propagation if not distributed evenly.
* **Expected Visual Behavior:** Highly intricate, self-pruning structures. Gliders that periodically change shape or state, and localized, crystal-like growth.
