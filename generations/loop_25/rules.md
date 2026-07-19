# Loop 25 Cellular Automata Rules: Self-Organized Criticality, Avalanches & Forest Fires

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Self-Organized Criticality, Avalanches & Forest Fires**.

These rules explore key concepts such as stochastic stress accumulation, trigger thresholds, toppling cascades, and forest fire spread with probabilistic ignitions or lightning strikes. Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time configurations of these systems simulate the emergence of self-organized critical behaviors, power-law cascade distributions, and stochastic wavefronts from localized, probabilistic updates.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Stochastic Sandpile Cascade](#rule-1-stochastic-sandpile-cascade) | 6 | Radius $r=1$ (with self) | Conservative height-based BTW toppling | Branching V-shaped avalanche cones |
| **2** | [Probabilistic Forest Fire](#rule-2-probabilistic-forest-fire) | 4 | Radius $r=1$ (no self) | Drossel-Schwabl forest fire with lightning | Twin fire fronts leaving burnt paths |
| **3** | [Directed Slope Avalanche](#rule-3-directed-slope-avalanche) | 5 | Asymmetric $r=2$ | Downhill energy flow with stochastic friction | Rightward-slanted avalanche tracks |
| **4** | [Seismic Slip Rupture](#rule-4-seismic-slip-rupture) | 8 | Radius $r=1$ (with self) | OFC earthquake fault strain transfer | Sudden wide diagonal slip reset waves |
| **5** | [Saturated Runoff Cascade](#rule-5-saturated-runoff-cascade) | 6 | Radius $r=1$ (no self) | Soil water saturation and runoff shedding | Runoff fronts wetting dry soil streams |
| **6** | [Aeolian Sandpile Cascade](#rule-6-aeolian-sandpile-cascade) | 6 | Radius $r=1$ (with self) | Wind-driven asymmetric sand toppling | Asymmetric right-tilted sand triangles |
| **7** | [Stochastic Multi-State Epidemic](#rule-7-stochastic-multi-state-epidemic) | 5 | Radius $r=1$ (no self) | Disease spread with immune decay | Chaotic, re-entering epidemic waves |
| **8** | [Stochastic Neuronal Avalanche](#rule-8-stochastic-neuronal-avalanche) | 6 | Radius $r=2$ (no self) | Synaptic noise and action potential firing | Power-law fractal active clusters |
| **9** | [Damped Granular Landslide](#rule-9-damped-granular-landslide) | 7 | Asymmetric $r=1$ | Landslide flow with energy dissipation | Dissipating downhill sliding chains |
| **10** | [Smoldering Forest Fire with Wind](#rule-10-smoldering-forest-fire-with-wind) | 7 | Asymmetric $r=2$ | Multi-level fuel, wind, and smoldering | Slanted fire fronts, flash explosions, hotspots |

---

## Rule Definitions

### Rule 1: Stochastic Sandpile Cascade
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * States $0, 1, 2, 3$: Stable sand heights (under capacity).
  * States $4, 5$: Super-critical sand heights (trigger toppling).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  Let $\xi_t(x) \sim \text{Bernoulli}(p_d)$ be an independent Bernoulli random variable representing the stochastic deposition of a sand grain with probability $p_d \in (0, 1)$.
  Let $T_t(x) = \mathbb{I}(S_t(x) \ge 4)$ be the toppling indicator function.
  The next state $S_{t+1}(x)$ is computed as:
  $$S_{t+1}(x) = \min\left(5, \max\left(0, S_t(x) + \xi_t(x) - 2 T_t(x) + T_t(x-1) + T_t(x+1)\right)\right)$$
* **Mathematical/Physical Rationale:** Models the classic Bak-Tang-Wiesenfeld sandpile on a 1D lattice. Stress (sand grains) accumulates slowly and stochastically. Once the height reaches the threshold of 4, the cell topples, shedding 2 grains (one to the left neighbor, one to the right neighbor). This is a conservative local redistribution that can push neighbors over the threshold, creating chain-reaction cascades.
* **Expected Visual Behavior:** Long, quiet periods of slow background color accumulation, interrupted by sudden, branching V-shaped cones of activity (avalanches) that cascade downward through the space-time grid.

---

### Rule 2: Probabilistic Forest Fire
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty ground (burnt/cleared).
  * State $1$: Sapling (young vegetation).
  * State $2$: Mature Tree (highly flammable fuel).
  * State $3$: Burning Tree (active fire front).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_g(x) \sim \text{Bernoulli}(p_g)$ represent sapling growth.
  Let $\xi_m(x) \sim \text{Bernoulli}(p_m)$ represent tree maturation.
  Let $\xi_l(x) \sim \text{Bernoulli}(p_l)$ represent a lightning strike.
  Let $\xi_{f, y}(x) \sim \text{Bernoulli}(p_f)$ represent fire spread from neighbor $y \in N(x)$.
  The next state $S_{t+1}(x)$ is:
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } \xi_g(x) = 1 \\ 0 & \text{otherwise} \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases} 2 & \text{if } \xi_m(x) = 1 \\ 1 & \text{otherwise} \end{cases}$$
  - If $s = 2$:
    Let the fire spread trigger be $F_t(x) = 1 - \prod_{y \in N(x)} \left(1 - \mathbb{I}(S_t(y) = 3) \cdot \xi_{f, y}(x)\right)$.
    $$S_{t+1}(x) = \begin{cases} 3 & \text{if } \xi_l(x) = 1 \text{ or } F_t(x) = 1 \\ 2 & \text{otherwise} \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** An adaptation of the Drossel-Schwabl forest fire model. Growth, maturation, and ignition are all stochastic. Fire spreads probabilistically from burning neighbors, allowing for firebreak gaps to occasionally stop the spread depending on fuel density.
* **Expected Visual Behavior:** Large patches of growing vegetation (states 1 and 2) that are suddenly struck by lightning, triggering twin fire fronts (state 3) traveling outwards in opposite directions, leaving behind empty black paths (state 0).

---

### Rule 3: Directed Slope Avalanche
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Stable ground (zero stress).
  * States $1, 2, 3$: Increasing stress accumulation.
  * State $4$: Avalanche flow (active kinetic state).
* **Neighborhood ($N(x)$):** Asymmetric radius $r=2$ looking uphill (to the left):
  $$N(x) = \{x-2, x-1, x\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_d(x) \sim \text{Bernoulli}(p_d)$ be the stochastic stress deposition.
  Let $\xi_p(x) \sim \text{Bernoulli}(p_p)$ be the propagation success (overcoming friction).
  Let $\xi_s(x) \sim \text{Bernoulli}(p_s)$ be a spontaneous gravity-driven failure trigger.
  - If $s \in \{0, 1, 2\}$:
    $$S_{t+1}(x) = s + \xi_d(x)$$
  - If $s = 3$:
    Let the uphill avalanche indicator be $A_t(x) = \mathbb{I}(S_t(x-1) = 4)$.
    $$S_{t+1}(x) = \begin{cases} 4 & \text{if } (A_t(x) = 1 \text{ and } \xi_p(x) = 1) \text{ or } \xi_s(x) = 1 \\ 3 & \text{otherwise} \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models downhill stress flow on a landslide-prone slope. Gravity creates a preferred direction (left-to-right). Uphill avalanches can trigger downslope failures, but the propagation is gated by stochastic friction ($\xi_p$). Spontaneous failures also occur due to gravity on highly stressed cells ($\xi_s$).
* **Expected Visual Behavior:** Rightward-slanted space-time tracks of state 4 that represent avalanches descending a slope. These tracks terminate randomly when they hit low-stress or high-friction regions.

---

### Rule 4: Seismic Slip Rupture
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State $0$: Relaxed fault.
  * States $1 \dots 6$: Elastic strain accumulation.
  * State $7$: Rupture threshold / Active slip.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_l(x) \sim \text{Bernoulli}(p_l)$ be the tectonic loading.
  Let $R_t(x) = \mathbb{I}(S_t(x-1) = 7) + \mathbb{I}(S_t(x+1) = 7)$ be the count of active rupture neighbors.
  - If $s = 7$:
    $$S_{t+1}(x) = 0$$
  - If $s < 7$:
    $$S_{t+1}(x) = \min\left(7, s + 2 R_t(x) + \xi_l(x)\right)$$
* **Mathematical/Physical Rationale:** Simulates the Olami-Feder-Christensen (OFC) earthquake model. Cells accumulate strain slowly through tectonic loading ($\xi_l$). When a cell reaches state 7, it slips, dropping its strain to 0 and transferring a large portion of it ($2$ units) to each neighbor. This can push neighbors past the threshold, initiating a cascade.
* **Expected Visual Behavior:** Long, uniform periods of strain increase (represented by progressive shifts in color/state), broken by sudden, instantaneous diagonal bands representing rupture waves that sweep across the lattice, resetting cells to state 0.

---

### Rule 5: Saturated Runoff Cascade
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Dry soil.
  * States $1, 2, 3, 4$: Partially saturated soil.
  * State $5$: Saturated / Surface runoff active.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_r(x) \sim \text{Bernoulli}(p_r)$ represent stochastic rainfall.
  Let $In_t(x) = \mathbb{I}(S_t(x-1) = 5) + \mathbb{I}(S_t(x+1) = 5)$ be the count of saturated neighbors.
  - If $s < 5$:
    $$S_{t+1}(x) = \min\left(5, s + \xi_r(x) + In_t(x)\right)$$
  - If $s = 5$:
    $$S_{t+1}(x) = \min\left(5, 3 + In_t(x)\right)$$
* **Mathematical/Physical Rationale:** Hydrological simulation of rainfall absorption and runoff. When soil saturates ($s=5$), it loses its capacity to hold water and sheds its excess water to neighboring cells. The saturated cell then drains down to state 3 (or higher if it receives runoff from its neighbors).
* **Expected Visual Behavior:** Random rainfall dots wetting the soil. As soon as a region becomes saturated, a runoff cascade triggers, sending wavefronts of water outward that wet dry soil, forming intricate stream-like networks in space-time.

---

### Rule 6: Aeolian Sandpile Cascade
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * States $0, 1, 2, 3$: Stable sand heights.
  * States $4, 5$: Super-critical heights (toppling).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_d(x) \sim \text{Bernoulli}(p_d)$ be the stochastic windblown sand deposition.
  Let $T_t(x) = \mathbb{I}(S_t(x) \ge 4)$ be the toppling indicator.
  The transition is defined as:
  $$S_{t+1}(x) = \min\left(5, \max\left(0, s + \xi_d(x) - 3 T_t(x) + 2 T_t(x-1) + T_t(x+1)\right)\right)$$
* **Mathematical/Physical Rationale:** Models wind-driven sand transport on a dune. Under a prevailing wind blowing left-to-right, a toppling cell at threshold $\ge 4$ sheds 3 grains of sand: 2 grains blow downwind to the right neighbor $x+1$, while only 1 grain is shed upwind to the left neighbor $x-1$.
* **Expected Visual Behavior:** Highly asymmetric, right-tilted triangular avalanche envelopes. The wavefronts on the right propagate faster and further, while the left boundaries remain relatively steep.

---

### Rule 7: Stochastic Multi-State Epidemic
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Susceptible ($S$).
  * State $1$: Infected ($I$, active spreader).
  * State $2$: Early Immune / Refractory ($R_1$).
  * State $3$: Late Immune / Refractory ($R_2$).
  * State $4$: Critical / Super-spreader ($C$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_s(x) \sim \text{Bernoulli}(p_s)$ be a spontaneous infection (external spark).
  Let $\xi_{i, y}(x) \sim \text{Bernoulli}(p_i)$ be the infection transmission from neighbor $y \in N(x)$.
  Let $\xi_c(x) \sim \text{Bernoulli}(p_c)$ be the progression to critical status.
  Let $\xi_r(x) \sim \text{Bernoulli}(p_r)$ be the loss of immunity.
  - If $s = 0$:
    Let $F_t(x) = 1 - \prod_{y \in N(x)} (1 - \mathbb{I}(S_t(y) \in \{1, 4\}) \cdot \xi_{i, y}(x))$.
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } \xi_s(x) = 1 \text{ or } F_t(x) = 1 \\ 0 & \text{otherwise} \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases} 4 & \text{if } \xi_c(x) = 1 \\ 2 & \text{otherwise} \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 2$$
  - If $s = 2$:
    $$S_{t+1}(x) = 3$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases} 0 & \text{if } \xi_r(x) = 1 \\ 3 & \text{otherwise} \end{cases}$$
* **Mathematical/Physical Rationale:** An epidemic model showing critical behavior. Infections spread stochastically from active (1) or critical (4) cases. Active cases may stochastically escalate to critical super-spreaders (4), causing a burst of infections. Recovery leads to a two-step immunity, after which immunity decays stochastically, returning the cell to the susceptible pool.
* **Expected Visual Behavior:** Traveling waves of infection followed by bands of immunity. Due to the stochastic loss of immunity, "holes" open in the immune shield, allowing waves to curl back and re-infect cleared areas, creating chaotic, self-sustaining epidemic cycles.

---

### Rule 8: Stochastic Neuronal Avalanche
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Quiescent / Rest state.
  * States $1, 2$: Sub-threshold excitation states.
  * State $3$: Action Potential / Firing state.
  * States $4, 5$: Refractory / Hyperpolarized states.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_n(x) \sim \text{Bernoulli}(p_n)$ represent stochastic synaptic noise.
  Let $F_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 3)$ be the number of active firing neighbors.
  - If $s \in \{0, 1, 2\}$:
    $$S_{t+1}(x) = \min\left(3, s + F_t(x) + \xi_n(x)\right)$$
  - If $s \in \{3, 4\}$:
    $$S_{t+1}(x) = s + 1$$
  - If $s = 5$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models criticality in neural networks. Neurons accumulate potential through local firing neighbors ($F_t$) and stochastic synaptic noise ($\xi_n$). Once they hit state 3, they fire, sending signals to neighbors within radius 2, followed by a deterministic hyperpolarized refractory period.
* **Expected Visual Behavior:** Power-law distributed bursts of neural firing (state 3) that cascade through the lattice. The space-time diagram displays fractal-like clusters of activity interspersed with silent periods.

---

### Rule 9: Damped Granular Landslide
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Empty / Relaxed ground.
  * States $1 \dots 5$: Energy levels.
  * State $6$: Active landslide / Kinetic flow.
* **Neighborhood ($N(x)$):** Asymmetric radius $r=1$ looking uphill (to the left):
  $$N(x) = \{x-1, x\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let $\xi_d(x) \sim \text{Bernoulli}(p_d)$ be the stochastic energy dissipation.
  Let $\xi_s(x) \sim \text{Bernoulli}(p_s)$ be a spontaneous trigger.
  - Let the incoming landslide energy be:
    $$G_t(x) = \mathbb{I}(S_t(x-1) = 6) \cdot \left(3 - \xi_d(x)\right)$$
  - If $s < 6$:
    $$S_{t+1}(x) = \min\left(6, s + G_t(x) + \xi_s(x)\right)$$
  - If $s = 6$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models landslide propagation on a granular slope. An active landslide (state 6) transfers 3 units of energy downhill. However, energy is lost due to friction, heat, and sound, modeled by a stochastic dissipation event ($\xi_d$) that reduces the transferred energy to 2. If a cell reaches state 6, it discharges completely.
* **Expected Visual Behavior:** Landslides propagate downhill (to the right). Due to stochastic energy dissipation, the landslide waves gradually lose energy and die out, resulting in a self-organized critical state with a power-law distribution of landslide sizes.

---

### Rule 10: Smoldering Forest Fire with Wind
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Burnt / Ash.
  * States $1, 2, 3$: Low, medium, and high density fuel.
  * State $4$: Smoldering fire.
  * State $5$: Flaming fire.
  * State $6$: Pyroclastic flash (explosive).
* **Neighborhood ($N(x)$):** Asymmetric radius $r=2$ favoring wind direction (left-to-right):
  $$N(x) = \{x-2, x-1, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$.
  Let the fire threat index $H_t(x)$ be defined as:
  $$H_t(x) = 2 \mathbb{I}(S_t(x-1) = 5) + \mathbb{I}(S_t(x+1) = 5) + 3 \mathbb{I}(S_t(x-2) = 6 \lor S_t(x-1) = 6) + \mathbb{I}(S_t(x-1) = 4)$$
  Let the ignition event be $\xi_{ign}(x) \sim \text{Bernoulli}\left(1 - (1 - p_f)^{H_t(x)}\right)$ where $p_f \in (0, 1)$ is the base spread rate.
  Let $\xi_r(x) \sim \text{Bernoulli}(p_r)$ be the fuel regeneration.
  Let $\xi_{flash}(x) \sim \text{Bernoulli}(p_{flash})$ be the explosive flash probability.
  Let $\xi_b(x) \sim \text{Bernoulli}(p_b)$ be the smolder burnout.
  - If $s \in \{0, 1, 2\}$:
    If $s = 0$ (and thus $\xi_{ign}(x) = 1$ is impossible due to lack of fuel):
      $$S_{t+1}(x) = S_t(x) + \xi_r(x)$$
    If $s \in \{1, 2\}$ and $\xi_{ign}(x) = 1$:
      - For $s = 2$: $S_{t+1}(x) = 5$ (flaming).
      - For $s = 1$: $S_{t+1}(x) = 4$ (smoldering).
    If $s \in \{1, 2\}$ and $\xi_{ign}(x) = 0$:
      $$S_{t+1}(x) = s + \xi_r(x)$$
  - If $s = 3$:
    If $\xi_{ign}(x) = 1$:
      $$S_{t+1}(x) = \begin{cases} 6 & \text{if } \xi_{flash}(x) = 1 \\ 5 & \text{otherwise} \end{cases}$$
    If $\xi_{ign}(x) = 0$:
      $$S_{t+1}(x) = 3$$
  - If $s = 4$ (smoldering):
    $$S_{t+1}(x) = \begin{cases} 5 & \text{if } H_t(x) \ge 2 \\ 0 & \text{else if } \xi_b(x) = 1 \\ 4 & \text{otherwise} \end{cases}$$
  - If $s \in \{5, 6\}$ (flaming / flash):
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** An advanced, highly detailed wildfire model. Wind blows left-to-right, causing fire to the left to have a much higher threat index. Fuel density dictates ignition results: low fuel (1) smolders (4), medium fuel (2) burns (5), and high fuel (3) can explode into a pyroclastic flash (6). A smoldering fire can flare up to flaming if the threat is high, or slowly burn out to ash.
* **Expected Visual Behavior:** Slanted fire fronts propagating rightward. High-density patches explode in bright flashes, spreading rapidly, while low-density patches smolder slowly, creating long-lived, dark-red hotspots that can reignite the forest if fuel matures.
