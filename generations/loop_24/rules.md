# Loop 24 Cellular Automata Rules: Self-Organized Flocking & Active Matter Turbulence

This document contains 10 distinct, mathematically rigorous, and stochastic cellular automata (CA) rules focused on the domain of **Self-Organized Flocking & Active Matter Turbulence**. 

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The rules incorporate stochasticity (representing thermal or rotational noise) and simulate the phase transition between laminar alignment (coherent motion) and active turbulence (disordered scattering) using 1D projections of flocking dynamics.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Stochastic Vicsek-1D Flocking](#rule-1-stochastic-vicsek-1d-flocking) | 3 | Radius $r=1$ | Majority direction alignment with noise | Coherent flocking bands with collisions |
| **2** | [Multi-Angle Filament Alignment](#rule-2-multi-angle-filament-alignment) | 6 | Radius $r=2$ | Complex vector director alignment | Smooth orientation domains with thermal fluctuations |
| **3** | [Chiral Active Rotators (Kuramoto CA)](#rule-3-chiral-active-rotators-kuramoto-ca) | 8 | Radius $r=1$ (excl.) | Intrinsic chirality and phase coupling | Striated diagonal traveling phase waves |
| **4** | [Run-and-Tumble Active Matter (MIPS)](#rule-4-run-and-tumble-active-matter-mips) | 4 | Radius $r=1$ | Motion-advection and congestion-induced tumbling | Motility-Induced Phase Separation (MIPS) jam clusters |
| **5** | [Active Burgers Turbulence](#rule-5-active-burgers-turbulence) | 5 | Radius $r=1$ | Nonlinear advection and viscous diffusion | Sharp shock fronts and localized turbulent decay |
| **6** | [Stochastic Velocity-Modulated Flocking](#rule-6-stochastic-velocity-modulated-flocking) | 6 | Radius $r=2$ (excl.) | Density-dependent speed and alignment | Traffic jam oscillations and density wave transitions |
| **7** | [Active Nematic Defect Dynamics](#rule-7-active-nematic-defect-dynamics) | 3 | Radius $r=1$ | Orthogonal alignment and defect migration | Active defect walls moving along chaotic trajectories |
| **8** | [Chemotactic Predator-Prey Flocking](#rule-8-chemotactic-predator-prey-flocking) | 4 | Radius $r=2$ (excl.) | Trophic alignment and chemotactic gradients | Chasing wavefronts and localized wave-packet dynamics |
| **9** | [Active Matter Phase Transition](#rule-9-active-matter-phase-transition) | 6 | Radius $r=2$ | Density-gated phase transition (Gas to Liquid) | Scale-free fluctuations at critical density $\rho_c$ |
| **10** | [Active Emulsion Phase-Separation](#rule-10-active-emulsion-phase-separation) | 5 | Radius $r=2$ | Multi-species segregation and interface shear | Dynamic emulsions with pulsating turbulent boundaries |

---

## Rule Definitions

### Rule 1: Stochastic Vicsek-1D Flocking
* **Name & Domain Connection:** Standard 1D Vicsek flocking. Models how simple active particles align their velocities under the influence of stochastic rotational noise, projecting 2D flocking onto a 1D lattice.
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Quiescent / Empty.
  * State $1$: Left-moving particle ($L$).
  * State $2$: Right-moving particle ($R$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $N_L(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ be the count of Left-moving neighbors.
  Let $N_R(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ be the count of Right-moving neighbors.
  Let $N_{\text{active}}(x) = N_L(x) + N_R(x)$ be the total active count.
  
  If $N_{\text{active}}(x) = 0$, then $S_{t+1}(x) = 0$.
  If $N_{\text{active}}(x) > 0$, then:
  - With probability $1 - \eta$, the cell aligns with the local majority direction:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } N_L(x) > N_R(x) \\
    2 & \text{if } N_R(x) > N_L(x) \\
    \mathbf{B}(0.5) + 1 & \text{if } N_L(x) = N_R(x)
    \end{cases}$$
    where $\mathbf{B}(0.5)$ is a Bernoulli trial returning $0$ or $1$ with equal probability.
  - With probability $\eta$ (rotational noise), the cell scatters:
    $$S_{t+1}(x) \sim \text{Uniform}(\{0, 1, 2\})$$
* **Mathematical/Physical Rationale:** This rule represents a discretized, 1D projection of the Vicsek model. Alignment occurs when particles within the neighborhood agree on a majority direction, while the noise parameter $\eta$ acts as effective temperature, disrupting order.
* **Expected Visual Behavior:** For low noise $\eta < 0.1$, the system organizes into massive, coherent bands of Left or Right moving states. When opposing bands collide, they form temporary static boundaries before one dominates. High noise $\eta > 0.4$ leads to complete isotropic scattering.

---

### Rule 2: Multi-Angle Filament Alignment
* **Name & Domain Connection:** Active polar filaments (e.g., microtubules driven by motor proteins). Simulates local alignment of orientation angles in a 1D filament chain.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$) representing discrete orientation angles:
  $$\theta_k = \frac{2\pi k}{6} \quad \text{for } k \in \{0, 1, 2, 3, 4, 5\}$$
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  For each neighbor $y \in N(x)$, we define its orientation vector $\mathbf{v}(y) = (\cos \theta_{S_t(y)}, \sin \theta_{S_t(y)})$.
  We compute the local mean director vector:
  $$\mathbf{V}_{\text{mean}}(x) = \frac{1}{|N(x)|} \sum_{y \in N(x)} \mathbf{v}(y)$$
  Let $\theta_{\text{target}} = \text{atan2}(V_{\text{mean}, y}, V_{\text{mean}, x})$. If $\mathbf{V}_{\text{mean}} = \mathbf{0}$, $\theta_{\text{target}}$ is chosen uniformly from $[0, 2\pi)$.
  Let $k_{\text{target}}$ be the state that minimizes the angular distance:
  $$k_{\text{target}} = \arg\min_{k} \left| \text{mod}(\theta_k - \theta_{\text{target}} + \pi, 2\pi) - \pi \right|$$
  The state update is defined stochastically:
  - With probability $1 - \eta$:
    $$S_{t+1}(x) = k_{\text{target}}$$
  - With probability $\eta$ (Brownian rotational noise):
    $$S_{t+1}(x) = (S_t(x) + \xi) \pmod 6$$
    where $\xi \in \{-1, 0, 1\}$ with probabilities $\{0.25, 0.50, 0.25\}$ respectively.
* **Mathematical/Physical Rationale:** Active filaments align due to steric interactions and motor-driven forces. We calculate the true vector average of local orientations, project it back to the nearest discrete state, and add localized rotational diffusion (random walks in state space).
* **Expected Visual Behavior:** Clear domain boundaries where filaments are aligned. For low noise, the domains merge slowly (coarsening). For high noise, the boundaries wiggle erratically, simulating thermal fluctuations of active polymers.

---

### Rule 3: Chiral Active Rotators (Kuramoto CA)
* **Name & Domain Connection:** Active rotators and chiral flocking. Models cells that possess a natural torque (clockwise or counter-clockwise clock) but attempt to phase-synchronize with their neighbors.
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) representing phase angles:
  $$\phi_k = \frac{2\pi k}{8}$$
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let the intrinsic torque be $\omega = 1$. The phase alignment factor is computed via the complex mean:
  $$Z(x) = \sum_{y \in N(x)} e^{i \phi_{S_t(y)}} = R(x) e^{i \Phi_{\text{avg}}(x)}$$
  If $R(x) = 0$, then $\Phi_{\text{avg}}(x) = \phi_{S_t(x)}$. Let:
  $$k_{\text{align}} = \arg\min_{k} \left| \phi_k - \Phi_{\text{avg}}(x) \right|$$
  Let the alignment adjustment step be:
  $$\Delta = \text{sign}\left( \text{mod}(k_{\text{align}} - S_t(x) + 4, 8) - 4 \right) \in \{-1, 0, 1\}$$
  The transition is:
  - With probability $1 - \eta$:
    $$S_{t+1}(x) = (S_t(x) + 1 + \Delta) \pmod 8$$
  - With probability $\eta$ (turbulent scattering):
    $$S_{t+1}(x) \sim \text{Uniform}(\{0, 1, \dots, 7\})$$
* **Mathematical/Physical Rationale:** This combines a discrete phase-coupled oscillator model (Kuramoto) with a chiral driving torque $\omega = 1$. Synchronization forces neighboring cells to lock in phase, while rotational noise disrupts the coherence.
* **Expected Visual Behavior:** Striated diagonal bands representing traveling phase waves. As noise $\eta$ increases, phase defects (pinwheels or disclinations) form, showing wave breaks and turbulent scattering.

---

### Rule 4: Run-and-Tumble Active Matter (MIPS)
* **Name & Domain Connection:** Motility-Induced Phase Separation (MIPS). Simulates self-propelled particles that move deterministically ("run") but undergo sudden random reorientations ("tumble") when they collide or crowd together.
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty space (vacuum).
  * State $1$: Left-running particle ($L$).
  * State $2$: Right-running particle ($R$).
  * State $3$: Tumbling / Jammed particle ($T$).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $In_L(x) = \mathbb{I}(S_t(x+1) = 1)$ be a Left-running particle entering $x$.
  Let $In_R(x) = \mathbb{I}(S_t(x-1) = 2)$ be a Right-running particle entering $x$.
  
  If $S_t(x) = 0$ (quiescent):
  - If $In_L(x) = 1$ and $In_R(x) = 0$: $S_{t+1}(x) = 1$ with probability $0.9$, or $3$ (tumbles due to friction) with probability $0.1$.
  - If $In_R(x) = 1$ and $In_L(x) = 0$: $S_{t+1}(x) = 2$ with probability $0.9$, or $3$ (tumbles due to friction) with probability $0.1$.
  - If $In_L(x) = 1$ and $In_R(x) = 1$ (collision): $S_{t+1}(x) = 3$ with probability $0.8$, and $0$ (particles pass through or annihilate) with probability $0.2$.
  - If no incoming particles: $S_{t+1}(x) = 0$.
  
  If $S_t(x) = 1$ (Left-running):
  - If $S_t(x-1) \neq 0$ (blocked): it becomes $3$ with probability $0.8$, or remains $1$ with probability $0.2$.
  - If $S_t(x-1) = 0$ (free path): it leaves the cell, $S_{t+1}(x) = 0$.
  
  If $S_t(x) = 2$ (Right-running):
  - If $S_t(x+1) \neq 0$ (blocked): it becomes $3$ with probability $0.8$, or remains $2$ with probability $0.2$.
  - If $S_t(x+1) = 0$ (free path): it leaves the cell, $S_{t+1}(x) = 0$.
  
  If $S_t(x) = 3$ (Tumbling):
  - The particle has a probability $\gamma = 0.3$ of resolving its tumble: it becomes state $1$ or $2$ with probability $0.5$ each.
  - With probability $1 - \gamma = 0.7$, it remains stuck in state $3$ (slow diffusive jam).
* **Mathematical/Physical Rationale:** Active particles slow down in high-density regions due to steric clashes. This slow-down creates a feedback loop: slower speed leads to higher density, resulting in phase separation without any attractive forces.
* **Expected Visual Behavior:** Phase separation. Large, stable blocks of jammed states (3) act as liquid droplets, while the space between them is populated by dilute, fast-moving running particles (1 and 2).

---

### Rule 5: Active Burgers Turbulence
* **Name & Domain Connection:** Active fluid turbulence. A stochastic 1D projection of the Navier-Stokes velocity field under active driving (e.g., bacterial suspensions).
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Zero velocity ($u = 0$).
  * State $1$: Slow Left ($u = -1$).
  * State $2$: Fast Left ($u = -2$).
  * State $3$: Slow Right ($u = 1$).
  * State $4$: Fast Right ($u = 2$).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $U(s)$ be the velocity of state $s$: $U(0)=0, U(1)=-1, U(2)=-2, U(3)=1, U(4)=2$.
  We calculate advection $A_t(x)$ and viscous diffusion $D_t(x)$ terms:
  $$A_t(x) = U(S_t(x)) \cdot [U(S_t(x-1)) - U(S_t(x+1))]$$
  $$D_t(x) = U(S_t(x-1)) - 2U(S_t(x)) + U(S_t(x+1))$$
  The active driving value is:
  $$H_t(x) = U(S_t(x)) + 0.5 A_t(x) + 0.3 D_t(x)$$
  Let $k_{\text{target}}$ be the state in $\{0, 1, 2, 3, 4\}$ that minimizes $|U(k) - H_t(x)|$.
  - With probability $1 - \eta$:
    $$S_{t+1}(x) = k_{\text{target}}$$
  - With probability $\eta$ (turbulent noise):
    $$S_{t+1}(x) \sim \text{Uniform}(\{0, 1, 2, 3, 4\})$$
* **Mathematical/Physical Rationale:** Models the Burgers equation $\partial_t u + u \partial_x u = \nu \partial_{xx} u$ with stochastic noise. Active matter injects energy at the grid scale, creating nonlinear advective shocks.
* **Expected Visual Behavior:** Sharp shock waves where velocities compress into narrow bands (sloped lines in space-time). These shocks merge and dissipate, creating a turbulent cascade that is disrupted by noise.

---

### Rule 6: Stochastic Velocity-Modulated Flocking
* **Name & Domain Connection:** Density-dependent flocking (traffic flow of active matter). Modulates particle speed based on local crowding.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Vacant.
  * State $1$: Slow Left.
  * State $2$: Fast Left.
  * State $3$: Slow Right.
  * State $4$: Fast Right.
  * State $5$: Jammed/Stationary.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let the local density be $\rho(x) = \frac{1}{4} \sum_{y \in N(x)} \mathbb{I}(S_t(y) \neq 0)$.
  Let the velocity sum of the neighborhood be:
  $$V_{\text{sum}}(x) = \sum_{y \in N(x)} U(S_t(y))$$
  where $U(0)=0, U(1)=-1, U(2)=-2, U(3)=1, U(4)=2, U(5)=0$.
  
  If $\rho(x) > 0.75$ (overcrowded):
  - With probability $1 - \eta$, the cell jams: $S_{t+1}(x) = 5$.
  - With probability $\eta$, it scatters: $S_{t+1}(x) \sim \text{Uniform}(\{1, 3, 5\})$.
  
  If $\rho(x) \le 0.75$:
  - The target direction is Left if $V_{\text{sum}}(x) < 0$, Right if $V_{\text{sum}}(x) > 0$. If $V_{\text{sum}}(x) = 0$, target direction matches $S_t(x)$'s direction.
  - The target speed is determined by density:
    - If $\rho(x) < 0.3$ (dilute): Fast speed (state 2 or 4).
    - If $0.3 \le \rho(x) \le 0.75$ (moderate): Slow speed (state 1 or 3).
  - Let $k_{\text{target}}$ be the state matching the target direction and speed.
  - With probability $1 - \eta$: $S_{t+1}(x) = k_{\text{target}}$.
  - With probability $\eta$ (noise): $S_{t+1}(x) \sim \text{Uniform}(\{1, 2, 3, 4\})$.
* **Mathematical/Physical Rationale:** Active systems display self-regulation: flock velocity decreases as density increases due to steric hindrance. This rule models the coupling between alignment and density-regulated velocities.
* **Expected Visual Behavior:** High-density regions slow down and trigger localized jams (state 5), which propagate backward. This creates classical "stop-and-go" traffic waves.

---

### Rule 7: Active Nematic Defect Dynamics
* **Name & Domain Connection:** Active nematic liquid crystals. Models apolar active particles that align axially and exhibit self-propelled topological defects (walls).
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Isotropic (no alignment).
  * State $1$: Parallel alignment (horizontal along the 1D lattice).
  * State $2$: Perpendicular alignment (transverse to the lattice).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $N_1(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ and $N_2(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$.
  Let $Defect_t(x) = 1$ if $S_t(x-1) \neq S_t(x+1)$ and $S_t(x-1) \cdot S_t(x+1) \neq 0$ (defect interface).
  
  If $Defect_t(x) = 1$:
  - The active stress at the interface forces a state flip (defect propagation):
    - With probability $1 - \eta$: $S_{t+1}(x) = 3 - S_t(x)$.
    - With probability $\eta$: $S_{t+1}(x) = 0$.
  
  If $Defect_t(x) = 0$:
  - If $S_t(x) = 0$ (isotropic):
    - With probability $1 - \eta$, the cell aligns with the local majority if $N_1(x) \neq N_2(x)$:
      $$S_{t+1}(x) = \begin{cases} 1 & \text{if } N_1(x) > N_2(x) \\ 2 & \text{if } N_2(x) > N_1(x) \end{cases}$$
    - With probability $\eta$, it becomes a random state in $\{0, 1, 2\}$.
  - If $S_t(x) \in \{1, 2\}$ (aligned):
    - It remains in its state with probability $1 - \eta$.
    - With probability $\eta$ (thermal desorption), it decays: $S_{t+1}(x) = 0$.
* **Mathematical/Physical Rationale:** Active nematics do not have a vector polarity, but active stresses force interfaces between domains (defects) to glide. In 1D, defects are domain boundaries that move stochastically.
* **Expected Visual Behavior:** Clean, vertical-ish domain blocks of parallel (1) and perpendicular (2) alignment. The boundaries (defects) walk dynamically and annihilate when they meet, showing topological annihilation.

---

### Rule 8: Chemotactic Predator-Prey Flocking
* **Name & Domain Connection:** Chemotactic active matter. Simulates flocking particles (predators) that align with each other but are also strongly attracted to nutrient gradients (prey).
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty space.
  * State $1$: Nutrient (stationary source).
  * State $2$: Left-moving flocker.
  * State $3$: Right-moving flocker.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $G_L(x) = \mathbb{I}(S_t(x-1) = 1) + 2\mathbb{I}(S_t(x-2) = 1)$ be the left-side nutrient gradient.
  Let $G_R(x) = \mathbb{I}(S_t(x+1) = 1) + 2\mathbb{I}(S_t(x+2) = 1)$ be the right-side nutrient gradient.
  Let $P_L(x) = \sum_{y \in N(x), y < x} \mathbb{I}(S_t(y) \in \{2, 3\})$ and $P_R(x) = \sum_{y \in N(x), y > x} \mathbb{I}(S_t(y) \in \{2, 3\})$ be flocker counts.
  
  If $S_t(x) = 1$ (nutrient):
  - If a flocker is adjacent ($S_t(x-1) = 3$ or $S_t(x+1) = 2$), it is consumed: $S_{t+1}(x) = S_t(y)$ (the incoming flocker state) with probability $0.9$.
  - Otherwise, it remains with probability $0.98$, and decays to $0$ with probability $0.02$.
  
  If $S_t(x) = 0$ (empty):
  - If nutrients are present nearby:
    - If $G_L > G_R$, $S_{t+1}(x) = 2$ with probability $0.8$.
    - If $G_R > G_L$, $S_{t+1}(x) = 3$ with probability $0.8$.
  - If no nutrients, the cell aligns with neighbor flockers:
    - If $P_L > P_R$, $S_{t+1}(x) = 2$ with probability $0.6$.
    - If $P_R > P_L$, $S_{t+1}(x) = 3$ with probability $0.6$.
  - With probability $\eta$, a new nutrient spawns: $S_{t+1}(x) = 1$.
  
  If $S_t(x) \in \{2, 3\}$ (flocker):
  - It moves in its direction (cell becomes $0$ with probability $0.9$).
  - With probability $\eta$ (noise), it turns: $S_{t+1}(x) = 5 - S_t(x)$.
* **Mathematical/Physical Rationale:** Models active agents undergoing chemotaxis (moving towards higher concentrations of a chemical/nutrient field). This couples predator behavior with flocking dynamics.
* **Expected Visual Behavior:** Waves of flockers sweeping across the space-time grid, tracking and eating nutrient patches. This creates localized, dense pulses that leave clean vacuums behind them.

---

### Rule 9: Active Matter Phase Transition
* **Name & Domain Connection:** Vicsek-Schwabl phase transition. Simulates the second-order phase transition from an isotropic gas phase to a polar liquid flocking phase based on density.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Isotropic Gas (unpolarized, random).
  * State $1$: Weakly Polarized Left.
  * State $2$: Strongly Polarized Left.
  * State $3$: Weakly Polarized Right.
  * State $4$: Strongly Polarized Right.
  * State $5$: Jammed Solid.
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let the local density of active matter be:
  $$\rho_a(x) = \frac{1}{5} \sum_{y \in N(x)} \mathbb{I}(S_t(y) \neq 0)$$
  Let the critical density threshold be $\rho_c = 0.4$.
  
  - If $\rho_a(x) < \rho_c$:
    - The local region is in the Gas phase.
    - $S_{t+1}(x) = 0$ with probability $0.7$.
    - With probability $0.3$, it fluctuates to $1$ or $3$ (isotropic noise).
  - If $\rho_a(x) \ge \rho_c$:
    - The local region enters the Polar Liquid phase.
    - Let $N_L(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{1, 2\})$ and $N_R(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{3, 4\})$.
    - If density is extremely high ($\rho_a(x) > 0.8$), the cell jams: $S_{t+1}(x) = 5$ with probability $1 - \eta$.
    - Otherwise, alignment occurs:
      - If $N_L(x) > N_R(x)$:
        - With probability $1 - \eta$, the state becomes $2$ (strongly polarized).
        - With probability $\eta$ (noise), the state becomes $1$ or $0$.
      - If $N_R(x) > N_L(x)$:
        - With probability $1 - \eta$, the state becomes $4$ (strongly polarized).
        - With probability $\eta$ (noise), the state becomes $3$ or $0$.
      - If $N_L(x) = N_R(x)$, $S_{t+1}(x) = 0$.
* **Mathematical/Physical Rationale:** Active matter undergoes a phase transition when local density exceeds a critical value, enabling collective motion. Below this critical value, noise dominates and dissipates alignment.
* **Expected Visual Behavior:** Near $\rho_c$, we see scale-free fluctuations and fractal-like clusters of aligned states. Far below, we see noise. Far above, we see massive, stable laminar bands.

---

### Rule 10: Active Emulsion Phase-Separation
* **Name & Domain Connection:** Active emulsions and phase-separating mixtures. Models two distinct species of active particles that tend to segregate but generate active turbulent shear at their interfaces.
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Background passive fluid.
  * State $1$: Species A (Left-polarized).
  * State $2$: Species B (Right-polarized).
  * State $3$: Turbulent Interface state (shear zone).
  * State $4$: Jammed boundary wall.
* **Neighborhood ($N(x)$):** Radius $r=2$:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $N_A(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ and $N_B(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$.
  Let the total active density be $\rho_{\text{act}}(x) = \frac{1}{5}(N_A(x) + N_B(x))$.
  
  - If $N_A(x) > 0$ and $N_B(x) > 0$ (mixed zone):
    - Shear generates interface turbulence: with probability $0.6$, $S_{t+1}(x) = 3$.
    - With probability $0.3$, segregation dominates:
      - $S_{t+1}(x) = 1$ if $N_A > N_B$.
      - $S_{t+1}(x) = 2$ if $N_B > N_A$.
    - With probability $0.1$, the cell decays to $0$.
  - If $N_A(x) > 0$ and $N_B(x) = 0$ (Species A domain):
    - With probability $1 - \eta$, the cell aligns with A: $S_{t+1}(x) = 1$.
    - With probability $\eta$ (noise), it becomes $0$ or $3$.
  - If $N_B(x) > 0$ and $N_A(x) = 0$ (Species B domain):
    - With probability $1 - \eta$, the cell aligns with B: $S_{t+1}(x) = 2$.
    - With probability $\eta$ (noise), it becomes $0$ or $3$.
  - If $N_A(x) = 0$ and $N_B(x) = 0$ (empty background):
    - $S_{t+1}(x) = 0$ with probability $0.98$.
    - With probability $0.02$, it spontaneously fluctuates to $1$ or $2$.
* **Mathematical/Physical Rationale:** Active fluids containing different components can phase-separate (like oil and water). However, the active motion of the particles generates strong velocity shear at the interfaces, creating localized active turbulence that opposes complete separation.
* **Expected Visual Behavior:** Dynamic, pulsating domains of A (state 1) and B (state 2). Instead of freezing into static blocks, the interfaces (state 3) wiggle and split, maintaining a persistent active emulsion.
