# Loop 11 Cellular Automata Rules: Stochastic Behaviors & Markovian Processes

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Stochastic Behaviors & Markovian Processes**. 

Unlike deterministic systems, these rules integrate probabilistic updates, thermal fluctuations, decay dynamics, and stochastic particle walks. They operate on a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules highlights critical phase transitions, fluctuation-induced pattern formation, and non-equilibrium steady states.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Stochastic Majority (Ising Glauber)](#rule-1-stochastic-majority-ising-glauber) | 5 | Radius $r=1$ | Neighborhood majority vote with thermal noise | Dynamic domains with rough boundaries |
| **2** | [Stochastic Contact Process](#rule-2-stochastic-contact-process) | 2 | Radius $r=1$ (excl. self) | Probabilistic infection ($\lambda$) and recovery ($\mu$) | Spatially active fluctuating clusters |
| **3** | [Directed Percolation](#rule-3-directed-percolation) | 2 | Radius $r=1$ (excl. self) | Probabilistic active state propagation | Branching percolation trees |
| **4** | [Stochastic Excitable Media](#rule-4-stochastic-excitable-media) | 8 | Radius $r=1$ (excl. self) | Probabilistic threshold-based fire, deterministic recovery | Spiral fragments and wave decay |
| **5** | [Noisy Majority](#rule-5-noisy-majority) | 3 | Radius $r=1$ | Majority voting with flip error probability | Textured noise with fuzzy boundaries |
| **6** | [Markovian Diffusion](#rule-6-markovian-diffusion) | 10 | Radius $r=1$ (excl. self) | Probabilistic particle walk and absorption | Spreading Gaussian density profiles |
| **7** | [Nagel-Schreckenberg Traffic](#rule-7-nagel-schreckenberg-traffic) | 6 | Global (Lookahead) | Multi-state discrete traffic flow with random slowdowns | Moving congestion waves |
| **8** | [Stochastic Sandpile](#rule-8-stochastic-sandpile) | 16 | Radius $r=1$ | Toppling with random distribution direction | Asymmetrical, branching avalanche trails |
| **9** | [Metropolis Ising Model](#rule-9-metropolis-ising-model) | 2 | Radius $r=1$ (excl. self) | Energy-based spin flips under thermal bath | Coalescing magnetic domains |
| **10** | [Stochastic Chiral Growth](#rule-10-stochastic-chiral-growth) | 5 | Radius $r=1$ (excl. self) | Asymmetric growth probabilities | Chiral, tilted fractal trees |

---

## Rule Definitions

### Rule 1: Stochastic Majority (Ising Glauber)
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  For each state $i \in \{0, 1, 2, 3, 4\}$, let $C_i(x)$ be the number of cells in the neighborhood that have state $i$:
  $$C_i(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = i)$$
  The local majority state $M_{\text{maj}}(x)$ is defined as:
  $$M_{\text{maj}}(x) = \begin{cases}
  i & \text{if } C_i(x) \ge 2 \\
  0 & \text{otherwise}
  \end{cases}$$
  At each time step, the cell updates according to:
  $$S_{t+1}(x) = \begin{cases}
  M_{\text{maj}}(x) & \text{with probability } 0.88 \\
  \eta & \text{with probability } 0.12
  \end{cases}$$
  where $\eta$ is a random variable drawn from a uniform distribution over all possible states: $\eta \sim \text{Uniform}(\{0, 1, 2, 3, 4\})$.
* **Mathematical Rationale:**
  This rule models a discrete-state Ising model spin update (similar to Glauber dynamics) under thermal noise. The majority rule mimics the alignment of spins with their local magnetic field (energy minimization), while the stochastic perturbation (12% noise) simulates thermal fluctuations that prevent the system from instantly freezing into a global consensus.
* **Expected Visual Behavior:**
  Development of cohesive, dynamic domains with rough, fluctuating boundaries. Unlike deterministic majority rules that produce clean straight boundaries, the thermal noise keeps the boundaries active and prevents static equilibrium.

---

### Rule 2: Stochastic Contact Process
* **States ($N$):** $2$ states ($0, 1$). State $0$ is inactive (healthy/susceptible), and State $1$ is active (infected).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $A(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ be the count of active neighbors.
  - If $S_t(x) = 0$ (susceptible):
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{with probability } \lambda = 0.6 \text{ if } A(x) \ge 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 1$ (infected):
    $$S_{t+1}(x) = \begin{cases}
    0 & \text{with probability } \mu = 0.15 \text{ (recovery)} \\
    1 & \text{with probability } 1 - \mu = 0.85
    \end{cases}$$
* **Mathematical Rationale:**
  This is a discrete-time formulation of the classic Contact Process (also known as the Susceptible-Infected-Susceptible or SIS model). The epidemic propagates locally through contact with active neighbors with an infection probability $\lambda$, while active nodes recover independently at a constant rate $\mu$. The behavior depends heavily on the ratio $\lambda/\mu$ relative to the critical threshold of the contact process.
* **Expected Visual Behavior:**
  Spatially active, fluctuating clusters. Since $\lambda/\mu = 4.0$ is above the critical threshold for directed percolation in 1+1 dimensions, the infection is expected to persist in a dynamic non-equilibrium steady state rather than dying out.

---

### Rule 3: Directed Percolation
* **States ($N$):** $2$ states ($0, 1$). State $0$ is inactive, and State $1$ is active.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  The transition is governed by independent transmission trials from active neighbors. Let $p = 0.65$ be the transmission probability. The next state $S_{t+1}(x)$ is active if at least one transmission succeeds:
  $$P(S_{t+1}(x) = 1) = 1 - (1 - p \cdot S_t(x-1))(1 - p \cdot S_t(x+1))$$
  Explicitly:
  - If $S_t(x-1) = 0$ and $S_t(x+1) = 0$: $P(S_{t+1}(x) = 1) = 0$
  - If $S_t(x-1) = 1$ and $S_t(x+1) = 0$: $P(S_{t+1}(x) = 1) = 0.65$
  - If $S_t(x-1) = 0$ and $S_t(x+1) = 1$: $P(S_{t+1}(x) = 1) = 0.65$
  - If $S_t(x-1) = 1$ and $S_t(x+1) = 1$: $P(S_{t+1}(x) = 1) = 0.8775$
* **Mathematical Rationale:**
  Directed percolation (DP) represents a fundamental universality class in statistical mechanics. It describes the flow of fluid or information through a directed medium. The transition probability captures independent pathways of transmission, making it a classic model of phase transitions into an absorbing state (the all-zero state).
* **Expected Visual Behavior:**
  Branching percolation trees. From a single seed, the active state spreads outwards, forming fractal-like networks of active paths. If $p = 0.65$ is near the critical threshold, the branching structures exhibit power-law scaling and eventually either die out or percolate infinitely.

---

### Rule 4: Stochastic Excitable Media
* **States ($N$):** $8$ states ($0, 1, 2, 3, 4, 5, 6, 7$).
  - State $0$: Rest state (susceptible).
  - State $1$: Excited state (firing).
  - States $2, 3, 4, 5, 6, 7$: Refractory states (gradual decay/recovery).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $E(x) = \mathbb{I}(S_t(x-1) = 1) \lor \mathbb{I}(S_t(x+1) = 1)$ indicate if at least one neighbor is in the excited state.
  - If $S_t(x) = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{with probability } p_e = 0.7 \text{ if } E(x) \text{ is true} \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) \ge 1$:
    $$S_{t+1}(x) = (S_t(x) + 1) \pmod{8}$$
* **Mathematical Rationale:**
  This rule models excitable media (like cardiac tissue or neural networks) where excitation propagates stochastically. The recovery cycle is deterministic: once excited (state 1), a cell must progress through a sequence of refractory states ($2 \to 3 \to \dots \to 7$) before returning to the susceptible state 0.
* **Expected Visual Behavior:**
  Stochastic wavefronts and decaying spiral fragments. A single seed will propagate outwards as two wavefronts followed by a trailing refractory zone. The stochastic activation probability ($0.7$) causes wavefront fragmentation, leading to self-sustaining chaotic excitations.

---

### Rule 5: Noisy Majority
* **States ($N$):** $3$ states ($0, 1, 2$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  For each state $i \in \{0, 1, 2\}$, let $C_i(x)$ be the count of state $i$ in $N(x)$. The majority state $M_{\text{maj}}(x)$ is:
  $$M_{\text{maj}}(x) = \begin{cases}
  i & \text{if } C_i(x) \ge 2 \\
  0 & \text{otherwise}
  \end{cases}$$
  The state at the next time step is given by:
  $$S_{t+1}(x) = \begin{cases}
  M_{\text{maj}}(x) & \text{with probability } 0.95 \\
  \eta & \text{with probability } 0.05
  \end{cases}$$
  where $\eta \sim \text{Uniform}(\{0, 1, 2\})$.
* **Mathematical Rationale:**
  This is a three-state majority-voting model with low-intensity noise (5%). It belongs to the class of probabilistic cellular automata simulating opinion dynamics. The majority function represents local social pressure to conform, while the noise represents random individual non-conformism or error.
* **Expected Visual Behavior:**
  Textured, noisy domains with fuzzy, fluctuating boundaries. The 3 states form large clusters, but the low noise rate continuously generates small defects and keeps the boundaries in a constant state of micro-fluctuation.

---

### Rule 6: Markovian Diffusion
* **States ($N$):** $10$ states ($0, 1, \dots, 9$). State $0$ represents an empty state, and states $1$ to $9$ represent decaying particle density.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $r(x) \sim \text{Uniform}(0, 1)$ be a randomly drawn variable for cell $x$.
  The cell state updates as:
  $$S_{t+1}(x) = \begin{cases}
  (S_t(x-1) - 1) \pmod{10} & \text{if } r(x) < 0.33 \text{ and } S_t(x-1) > 0 \\
  (S_t(x+1) - 1) \pmod{10} & \text{if } r(x) > 0.66 \text{ and } S_t(x+1) > 0 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:**
  This rule models a Markovian random walk of density/particles with dissipation. At each step, a cell has a probability of receiving a decremented density value from its left neighbor (with probability 0.33) or right neighbor (with probability 0.33). The subtraction of 1 represents energy dissipation or particle absorption during movement.
* **Expected Visual Behavior:**
  Spreading Gaussian-like density profiles that slowly decay in amplitude. From a single high-value seed, the state spreads outward in a random-walk fashion, forming a symmetric, diffusing bell-curve texture that gradually fades to 0.

---

### Rule 7: Nagel-Schreckenberg Traffic
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  - State $0$: Empty road cell.
  - States $1, 2, 3, 4, 5$: A vehicle with velocity $v \in \{1, 2, 3, 4, 5\}$.
* **Neighborhood ($N(x)$):** Non-local / global lookahead.
* **Transition Function:**
  For a grid of length $L$, let $cars(t) = \{ x \in \{0, \dots, L-1\} \mid S_t(x) > 0 \}$ be the indices of cells containing vehicles.
  For each vehicle at position $x$:
  1. **Acceleration**: Let $v^{(1)}_t(x) = \min(S_t(x) + 1, 5)$.
  2. **Deceleration**: Let $next(x)$ be the position of the nearest vehicle ahead:
     $$next(x) = \arg\min_{y \in cars(t), y \neq x} \left( (y - x) \pmod L \right)$$
     The gap to the next vehicle is $g(x) = (next(x) - x - 1) \pmod L$. The velocity is limited by the gap:
     $$v^{(2)}_t(x) = \min(v^{(1)}_t(x), g(x))$$
  3. **Random Slowdown**: With probability $p_{\text{slow}} = 0.2$, if $v^{(2)}_t(x) > 1$, the velocity is reduced by 1:
     $$v^{(3)}_t(x) = \begin{cases}
     v^{(2)}_t(x) - 1 & \text{with probability } 0.2 \\
     v^{(2)}_t(x) & \text{with probability } 0.8
     \end{cases}$$
     *(Note: If $v^{(2)}_t(x) \le 1$, then $v^{(3)}_t(x) = v^{(2)}_t(x)$).*
  4. **Movement**: The vehicle moves to destination $x' = (x + v^{(3)}_t(x)) \pmod L$. The state at $x'$ becomes $v^{(3)}_t(x)$. All other cells remain or become empty ($0$).
* **Mathematical Rationale:**
  This is a discrete-time stochastic model for 1D highway traffic, first proposed by Nagel and Schreckenberg in 1992. It is a classic example of emergent collective behavior: the combination of deterministic gap-based slowdowns and stochastic random deceleration mimics human driver behavior, leading to spontaneous traffic jam formation.
* **Expected Visual Behavior:**
  Moving congestion waves. In the space-time diagram, cars move as diagonal lines. When density is high, backward-propagating waves of low speed (traffic jams) emerge spontaneously, showing negative-slope bands of lower velocity.

---

### Rule 8: Stochastic Sandpile
* **States ($N$):** $16$ states ($0, 1, \dots, 15$), representing grain height.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  At each step, a cell $x$ is unstable if $S_t(x) \ge 4$. Unstable cells topple, distributing 4 grains.
  Specifically, for each unstable cell $y$, we sample two independent Bernoulli variables representing directional targets:
  - $Target(L_y) = y - 1$ with probability $0.7$, and $y + 1$ with probability $0.3$.
  - $Target(R_y) = y + 1$ with probability $0.7$, and $y - 1$ with probability $0.3$.
  The update is the sum of self-retained grains ($S_t(x) - 2$ if $S_t(x) \ge 4$, otherwise $S_t(x)$) and the grains received from neighboring topples:
  $$S_{\text{new}}(x) = S_t(x) - 2 \cdot \mathbb{I}(S_t(x) \ge 4) + \sum_{y \in \{x-1, x+1\}} \mathbb{I}(S_t(y) \ge 4) \cdot \left[ \mathbb{I}(Target(L_y) = x) + \mathbb{I}(Target(R_y) = x) \right]$$
  Finally, the state is capped at 15:
  $$S_{t+1}(x) = \min(15, S_{\text{new}}(x))$$
* **Mathematical Rationale:**
  This is a stochastic variant of the Abelian Sandpile Model (Bak-Tang-Wiesenfeld model). While the classic model is deterministic and symmetric, this rule introduces stochastic asymmetry (a 70% chance to distribute grains in the preferred direction). This breaks the abelian group property and introduces directional flow, modeling downhill soil creep or wind-driven sand transport.
* **Expected Visual Behavior:**
  Asymmetric, branching avalanche trails. Sand piled at a single seed will topple and drift preferentially in one direction, creating skewed, fractal-like drainage basins and runoff patterns.

---

### Rule 9: Metropolis Ising Model
* **States ($N$):** $2$ states ($0, 1$), representing spins $\sigma \in \{-1, +1\}$.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $\sigma_t(x) = 2 \cdot S_t(x) - 1 \in \{-1, +1\}$ be the spin of cell $x$.
  The local energy change $\Delta E$ for flipping the spin $\sigma_t(x) \to -\sigma_t(x)$ is:
  $$\Delta E = 2 \cdot \sigma_t(x) \cdot (\sigma_t(x-1) + \sigma_t(x+1))$$
  Under the Metropolis-Hastings update rule, the spin flip is accepted with probability:
  $$P(\sigma_{t+1}(x) = -\sigma_t(x)) = \begin{cases}
  1 & \text{if } \Delta E \le 0 \\
  e^{-\Delta E / 1.8} & \text{if } \Delta E > 0
  \end{cases}$$
  Otherwise, the spin remains unchanged: $\sigma_{t+1}(x) = \sigma_t(x)$.
  Finally, the next state is mapped back: $S_{t+1}(x) = \frac{\sigma_{t+1}(x) + 1}{2}$.
* **Mathematical Rationale:**
  This rule implements a 1D Ising model using the Metropolis Monte Carlo algorithm. By updating all cells simultaneously, it acts as a probabilistic cellular automaton simulating ferromagnetic interactions at a finite temperature $T = 1.8$. The local energy change drives the system toward alignment (spins matching their neighbors), while the thermal bath allows occasional alignment-breaking flips.
* **Expected Visual Behavior:**
  Coalescing magnetic domains. The space-time progression shows the growth and merger of monochromatic regions (domains of spin $+1$ or $-1$). Because $T = 1.8$ is below the critical point of high-dimensional systems but finite in 1D, the domains show thermodynamic fluctuations and rough edges.

---

### Rule 10: Stochastic Chiral Growth
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$). State $0$ is the empty/growth-substrate state, and states $1, 2, 3, 4$ represent growing crystal segments.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  If $S_t(x) > 0$, the cell is already grown and remains unchanged: $S_{t+1}(x) = S_t(x)$.
  If $S_t(x) = 0$, we draw $r(x) \sim \text{Uniform}(0, 1)$. The transition is determined by neighbor growth:
  - If $S_t(x-1) > 0$ and $S_t(x+1) > 0$:
    $$S_{t+1}(x) = \begin{cases}
    (S_t(x-1) + 1) \pmod 5 & \text{if } r(x) < 0.25 \\
    (S_t(x+1) + 1) \pmod 5 & \text{if } 0.25 \le r(x) < 0.65 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x-1) > 0$ and $S_t(x+1) = 0$:
    $$S_{t+1}(x) = \begin{cases}
    (S_t(x-1) + 1) \pmod 5 & \text{if } r(x) < 0.25 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x-1) = 0$ and $S_t(x+1) > 0$:
    $$S_{t+1}(x) = \begin{cases}
    (S_t(x+1) + 1) \pmod 5 & \text{if } r(x) < 0.65 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x-1) = 0$ and $S_t(x+1) = 0$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:**
  This rule models chiral crystal growth or unidirectional polymerisation. The probability of colonization from the right neighbor ($0.65$) is significantly higher than from the left neighbor ($0.25$), introducing a spatial chirality (left-right asymmetry). The state increments modulo 5, adding periodic color bands to the growth front.
* **Expected Visual Behavior:**
  Chiral, tilted fractal trees. Growth from a single seed spreads asymmetric branches that tilt preferentially in one direction, producing a dynamic space-time pattern of slanted stripes and branch divisions.
