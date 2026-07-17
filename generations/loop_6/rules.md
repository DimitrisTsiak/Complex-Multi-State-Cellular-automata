# Loop 6 Cellular Automata Rules: Fluid & Convective Systems

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Fluid & Convective Systems**. 

In this domain, cells represent discretized fluid elements, and the state values $S_t(x) \in \{0, 1, \dots, N-1\}$ encode physical properties such as temperature, pressure, concentration, velocity, or density. Unlike the cyclic threshold models of Loop 1 or the simple birth/survival-decay generations models of Loop 2, these transition functions are derived from discretized transport equations, advection-diffusion-reaction dynamics, buoyancy-driven displacement, and momentum transfer with non-linear thresholds.

Each rule is designed for a 1D lattice of width $W$ with periodic boundary conditions, where the state of cell $x$ at time step $t$ is denoted by $S_t(x)$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Physical Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Clamped Advection-Diffusion](#rule-1-clamped-advection-diffusion) | 8 | Radius $r=1$ | Directional advection with gradient-based diffusion | Skewed, thermal diffusion plumes |
| **2** | [Buoyancy Convective Plumes](#rule-2-buoyancy-convective-plumes) | 6 | Radius $r=1$ | Density-driven asymmetric flows & collision annihilation | Colliding and neutralizing plumes |
| **3** | [Rayleigh-Bénard Convective Cells](#rule-3-rayleigh-benard-convective-cells) | 8 | Radius $r=1$ | Velocity fields, shear instability, and rotational roll ejection | Periodic circulating convective cells |
| **4** | [Compressible Gas Shockwaves](#rule-4-compressible-gas-shockwaves) | 6 | Radius $r=1$ | Accumulative pressure build-up and explosive discharge | Intersecting high-pressure shock lines |
| **5** | [Viscous Drag & Shear Flow](#rule-5-viscous-drag-shear-flow) | 6 | Radius $r=1$ (incl. self) | Momentum diffusion & shear-triggered turbulence | Viscously smoothed regions split by turbulent scars |
| **6** | [Surface Tension & Cohesion](#rule-6-surface-tension-cohesion) | 5 | Radius $r=2$ | Phase condensation, cohesion, & evaporation | Cohesive fluid droplets separating gas voids |
| **7** | [Thermohaline Circulation](#rule-7-thermohaline-circulation) | 8 | Dual $r=1, 2$ | Double-diffusive convection (different heat & salt scales) | Intricate, multi-layered fingering structures |
| **8** | [Kelvin-Helmholtz Instability](#rule-8-kelvin-helmholtz-instability) | 8 | Radius $r=1$ | Opposing velocity shear forming roll-up vortices | Rolling vortex trains along shear interfaces |
| **9** | [Evaporative Convection (Marangoni)](#rule-9-evaporative-convection-marangoni) | 6 | Radius $r=1$ | Surfactant spreading from low to high surface tension | Spreading chemical fronts with peak evaporation |
| **10** | [Porous Darcy Gravity Currents](#rule-10-porous-darcy-gravity-currents) | 8 | Radius $r=1$ | Pressure-gradient flow with capillary trapping threshold | Trapped residual plumes and segmented drainage |

---

## Rule Definitions

### Rule 1: Clamped Advection-Diffusion
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) representing local temperature (0 is cold, 7 is hot).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $\text{sgn}(u)$ be the sign function:
  $$\text{sgn}(u) = \begin{cases} 1 & \text{if } u > 0 \\ -1 & \text{if } u < 0 \\ 0 & \text{if } u = 0 \end{cases}$$
  The state at the next step is advected from the left (representing a left-to-right velocity field) and modified by the local diffusion gradient:
  $$S_{t+1}(x) = \max\left(0, \min\left(7, S_t(x-1) + \text{sgn}\left(S_t(x+1) - S_t(x-1)\right)\right)\right)$$
* **Mathematical Rationale:** This rule discretizes the 1D advection-diffusion equation. The advective term shifts the state rightward ($S_t(x-1)$), while the diffusion term adjusts the state based on the local spatial derivative $(S_t(x+1) - S_t(x-1))$ to smooth out gradients. The clamping ensures that temperature respects thermodynamic bounds instead of wrapping around cyclicly.
* **Expected Visual Behavior:** Skewed, thermal diffusion plumes that drift rightward, forming smooth gradient boundaries with stable internal fields.

### Rule 2: Buoyancy Convective Plumes
* **States ($N$):** $6$ states ($0, 1, \dots, 5$) representing fluid density.
  * State $0$: Neutral background fluid.
  * States $1, 2$: Hot rising fluid (buoyant, advects leftward).
  * States $3, 4, 5$: Cold sinking fluid (dense, advects rightward).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself.
* **Transition Function:**
  Define indicator functions for hot and cold plumes in neighboring cells:
  $$R_t(y) = \mathbb{I}\left(S_t(y) \in \{1, 2\}\right) \quad (\text{hot plume})$$
  $$K_t(y) = \mathbb{I}\left(S_t(y) \in \{3, 4, 5\}\right) \quad (\text{cold plume})$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  0 & \text{if } R_t(x+1) = 1 \text{ and } K_t(x-1) = 1 \quad (\text{collision neutralization}) \\
  \max\left(1, S_t(x+1) - 1\right) & \text{else if } R_t(x+1) = 1 \text{ and } K_t(x-1) = 0 \quad (\text{hot flow left}) \\
  S_t(x-1) - 1 & \text{else if } K_t(x-1) = 1 \text{ and } R_t(x+1) = 0 \text{ and } S_t(x-1) > 3 \quad (\text{cold flow right}) \\
  0 & \text{else if } K_t(x-1) = 1 \text{ and } R_t(x+1) = 0 \text{ and } S_t(x-1) = 3 \quad (\text{cold flow right, fully decayed}) \\
  S_t(x) - 1 & \text{else if } S_t(x) \in \{1, 2\} \quad (\text{hot thermal dissipation}) \\
  S_t(x) - 1 & \text{else if } S_t(x) \in \{4, 5\} \quad (\text{cold thermal dissipation}) \\
  0 & \text{otherwise } (S_t(x) \in \{0, 3\})
  \end{cases}$$
* **Mathematical Rationale:** Models two opposing convective buoyancy streams: hot rising fluid moving left, and cold sinking fluid moving right. When they meet, they neutralize to the background temperature ($0$). When they flow through space, they lose energy (decay by 1), and static plumes dissolve into the background.
* **Expected Visual Behavior:** Dynamic, colliding plumes that form complex vertical intersection patterns and annihilate on impact, creating transient, self-limiting convection cells.

### Rule 3: Rayleigh-Bénard Convective Cells
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) encoding local fluid velocity.
  * State $0$: Quiescent.
  * States $1, 2, 3$: Leftward flowing fluid with speed $1, 2, 3$ respectively.
  * States $4, 5, 6$: Rightward flowing fluid with speed $1, 2, 3$ respectively.
  * State $7$: Turbulent vortex core.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself.
* **Transition Function:**
  Let the velocity $V(s)$ of state $s$ be:
  $$V(0) = 0, \quad V(1)=-1, V(2)=-2, V(3)=-3, \quad V(4)=1, V(5)=2, V(6)=3, \quad V(7)=0$$
  The transition is defined by the following cases:
  1. **Vortex core decay:** If $S_t(x) = 7$, then $S_{t+1}(x) = 0$.
  2. **Vortex ejection and flow collisions in quiescent cells:** If $S_t(x) = 0$:
     * If $S_t(x+1) = 7$ and $S_t(x-1) = 7$: $S_{t+1}(x) = 7$.
     * Else if $S_t(x+1) = 7$: $S_{t+1}(x) = 3$ (eject leftward).
     * Else if $S_t(x-1) = 7$: $S_{t+1}(x) = 6$ (eject rightward).
     * Else if $V(S_t(x-1)) > 0$ and $V(S_t(x+1)) < 0$: $S_{t+1}(x) = 7$ (shear collision).
     * Else if $V(S_t(x+1)) < 0$: $S_{t+1}(x) = S_t(x+1) - 1$ if $S_t(x+1) \in \{2, 3\}$ else $0$.
     * Else if $V(S_t(x-1)) > 0$: $S_{t+1}(x) = S_t(x-1) - 1$ if $S_t(x-1) \in \{5, 6\}$ else $0$.
     * Else: $S_{t+1}(x) = 0$.
  3. **Flow propagation in active channels:** If $S_t(x) \in \{1, 2, 3\}$ (leftward):
     * If $S_t(x+1) = 7$: $S_{t+1}(x) = 3$.
     * Else if $V(S_t(x-1)) > 0$: $S_{t+1}(x) = 7$ (shear collision).
     * Else: Let $u = S_t(x+1)$ if $S_t(x+1) \in \{1, 2, 3\}$ else $0$. If $u > 0$, $S_{t+1}(x) = \max(1, u-1)$; else $S_{t+1}(x) = S_t(x)-1$ if $S_t(x) > 1$ else $0$.
  4. **Rightward flow channels:** If $S_t(x) \in \{4, 5, 6\}$ (rightward):
     * If $S_t(x-1) = 7$: $S_{t+1}(x) = 6$.
     * Else if $V(S_t(x+1)) < 0$: $S_{t+1}(x) = 7$ (shear collision).
     * Else: Let $u = S_t(x-1)$ if $S_t(x-1) \in \{4, 5, 6\}$ else $0$. If $u > 0$: $S_{t+1}(x) = u-1$ if $u > 4$ else $0$; else $S_{t+1}(x) = S_t(x)-1$ if $S_t(x) > 4$ else $0$.
* **Mathematical Rationale:** Models Rayleigh-Bénard roll dynamics. Opposing velocity flows that collide face-to-face create a shear vortex core (7). Vortex cores are unstable and decay by ejecting new fluid streams in opposite directions, creating circular roll loops.
* **Expected Visual Behavior:** Alternating bands of leftward and rightward velocity streams bounded by vortex cores. This generates self-sustaining cellular structures resembling convective rolls.

### Rule 4: Compressible Gas Shockwaves
* **States ($N$):** $6$ states ($0, 1, \dots, 5$) representing pressure/density.
  * States $0, 1, 2, 3$: Low-to-moderate pressure.
  * States $4, 5$: High pressure (discharge states).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $E_t(x)$ be the number of discharging neighbors:
  $$E_t(x) = \sum_{y \in N(x)} \mathbb{I}\left(S_t(y) \ge 4\right)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  0 & \text{if } S_t(x) \ge 4 \quad (\text{discharge collapse}) \\
  \min\left(5, S_t(x) + E_t(x)\right) & \text{if } S_t(x) < 4 \quad (\text{pressure accumulation})
  \end{cases}$$
* **Mathematical Rationale:** Simulates acoustic waves that compress and steepen into shockwaves. Moderate pressure areas accumulate incoming acoustic energy from active discharges. When local pressure exceeds the limit ($\ge 4$), it releases it in a single explosive step (discharge), propagating the pressure wave outward to its neighbors.
* **Expected Visual Behavior:** Clean intersecting diagonal lines of pressure propagation. When two waves collide, they superimpose, triggering localized secondary discharges and creating complex grid-like shock pattern interfaces.

### Rule 5: Viscous Drag & Shear Flow
* **States ($N$):** $6$ states ($0, 1, \dots, 5$) representing fluid velocity.
  * State $0$: Stationary.
  * State $1$: Slow leftward velocity ($V = -1$).
  * State $2$: Fast leftward velocity ($V = -2$).
  * State $3$: Slow rightward velocity ($V = 1$).
  * State $4$: Fast rightward velocity ($V = 2$).
  * State $5$: Turbulent shear zone ($V = 0$).
* **Neighborhood ($N_{all}(x)$):** Radius $r=1$ including the cell itself:
  $$N_{all}(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  First, map neighbor states to their velocity values:
  $$V_t(y) = \begin{cases}
  -2 & \text{if } S_t(y) = 2 \\
  -1 & \text{if } S_t(y) = 1 \\
  0 & \text{if } S_t(y) \in \{0, 5\} \\
  1 & \text{if } S_t(y) = 3 \\
  2 & \text{if } S_t(y) = 4
  \end{cases}$$
  The transition is defined as:
  1. **Turbulent shear trigger:** If the shear $|V_t(x+1) - V_t(x-1)| \ge 3$, then:
     $$S_{t+1}(x) = 5$$
  2. **Turbulent dissipation:** Else if $S_t(x) = 5$, then:
     $$S_{t+1}(x) = 0$$
  3. **Viscous smoothing (momentum average):** Otherwise:
     Compute the average local velocity:
     $$V_{avg} = \text{round}\left( \frac{V_t(x-1) + V_t(x) + V_t(x+1)}{3} \right)$$
     And map back to the state:
     $$S_{t+1}(x) = \begin{cases}
     2 & \text{if } V_{avg} \le -2 \\
     1 & \text{if } V_{avg} = -1 \\
     0 & \text{if } V_{avg} = 0 \\
     3 & \text{if } V_{avg} = 1 \\
     4 & \text{if } V_{avg} \ge 2
     \end{cases}$$
* **Mathematical Rationale:** Simulates momentum transport with a shear-induced transition to turbulence. Viscosity smooths out velocity differences through local averaging. However, if the spatial velocity gradient (shear) is too steep ($|\Delta V| \ge 3$), the interface undergoes transition to a turbulent state (5), which has zero net velocity and dissipates energy in the next step.
* **Expected Visual Behavior:** Large regions of smooth laminar flow that gradually slow down due to viscosity, punctuated by dark, stationary "turbulent scars" where opposing flows clash.

### Rule 6: Surface Tension & Cohesion
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$) representing fluid phases.
  * State $0$: Gas phase.
  * States $1, 2, 3, 4$: Liquid phases of increasing concentration and cohesion.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $L_t(x)$ be the number of liquid neighbors:
  $$L_t(x) = \sum_{y \in N(x)} \mathbb{I}\left(S_t(y) \ge 1\right)$$
  The transition is defined as:
  * **Gas Phase ($S_t(x) = 0$):** Condensation occurs if liquid density is high:
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } L_t(x) \ge 3 \\ 0 & \text{otherwise} \end{cases}$$
  * **Liquid Phase ($S_t(x) \ge 1$):**
    $$S_{t+1}(x) = \begin{cases}
    S_t(x) - 1 & \text{if } L_t(x) \le 1 \quad (\text{evaporation/dispersion}) \\
    \min(4, S_t(x) + 1) & \text{if } L_t(x) = 4 \quad (\text{cohesive condensation}) \\
    S_t(x) & \text{otherwise } (L_t(x) \in \{2, 3\})
    \end{cases}$$
* **Mathematical Rationale:** Models the balance between cohesive surface tension forces and evaporative dispersion. Liquid cells pull together, increasing local concentration when surrounded by liquid ($L_t=4$). Isolated liquid cells ($L_t \le 1$) evaporate due to lack of cohesive support. Gas cells condense (nucleate) under high liquid pressure.
* **Expected Visual Behavior:** Clean phase-separated boundaries. The system self-organizes into stable fluid droplets (high-concentration lines) separated by gas voids, resisting dispersion.

### Rule 7: Thermohaline Circulation
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) representing a binary combination of Temperature and Salinity.
  * Temperature: $T \in \{0, 1\}$ where $0$ is Hot (buoyant) and $1$ is Cold (dense).
  * Salinity: $S^{salt} \in \{0, 1, 2, 3\}$ from Fresh (buoyant) to Very Salty (dense).
  * State value: $S_t(x) = 4 \cdot T_t(x) + S^{salt}_t(x)$.
* **Neighborhoods:**
  * Temperature neighborhood: $N_2(x) = \{x-2, x-1, x, x+1, x+2\}$ (radius 2, rapid thermal diffusion).
  * Salinity neighborhood: $N_1(x) = \{x-1, x, x+1\}$ (radius 1, slow salt diffusion/convective advection).
* **Transition Function:**
  Extract components: $T_t(y) = \lfloor S_t(y)/4 \rfloor$ and $S^{salt}_t(y) = S_t(y) \pmod 4$.
  1. **Temperature diffusion (rapid):**
     $$T_{t+1}(x) = \begin{cases} 1 & \text{if } \sum_{y=x-2}^{x+2} T_t(y) \ge 3 \\ 0 & \text{otherwise} \end{cases}$$
  2. **Salinity transport (slow diffusion + gravity flow):**
     * If the left neighbor is cold and salty ($T_t(x-1) = 1$ and $S^{salt}_t(x-1) \ge 2$), it convective-sinks and advects salt rightward:
       $$S^{salt}_{t+1}(x) = S^{salt}_t(x-1)$$
     * Otherwise, salinity undergoes local diffusion:
       $$S^{salt}_{t+1}(x) = \text{round}\left( \frac{S^{salt}_t(x-1) + S^{salt}_t(x) + S^{salt}_t(x+1)}{3} \right)$$
  3. **Recombination:**
     $$S_{t+1}(x) = 4 \cdot T_{t+1}(x) + S^{salt}_{t+1}(x)$$
* **Mathematical Rationale:** Models double-diffusive convection (salt fingering). Since heat diffuses much faster than salt, salinity gradients persist longer. When a cold, highly saline fluid mass forms, it becomes dense and advects downwards (represented in 1D as moving rightward), carrying salinity with it.
* **Expected Visual Behavior:** Intricate, multi-layered vertical fingering structures. The different spatial scales of thermal and salinity diffusion create fine-grained periodic instabilities.

### Rule 8: Kelvin-Helmholtz Instability
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) encoding interface shear and velocities.
  * States $0, 1, 2$: Leftward flowing fluid with velocities $V = -1, -2, -3$ respectively.
  * States $3, 4, 5$: Rightward flowing fluid with velocities $V = 1, 2, 3$ respectively.
  * State $6$: Interface wave ($V = 0$).
  * State $7$: Vortex roll-up ($V = 0$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself.
* **Transition Function:**
  Define velocity $V(s)$ for state $s$:
  $$V(s) = \begin{cases}
  -1 - s & \text{if } s \in \{0, 1, 2\} \\
  s - 2 & \text{if } s \in \{3, 4, 5\} \\
  0 & \text{if } s \in \{6, 7\}
  \end{cases}$$
  The transition is defined as:
  1. **Wave/Vortex decay:** If $S_t(x) \in \{6, 7\}$, then:
     $$S_{t+1}(x) = \begin{cases} 6 & \text{if } S_t(x) = 7 \quad (\text{vortex relaxes to wave}) \\ 0 & \text{if } S_t(x) = 6 \quad (\text{wave relaxes to flow}) \end{cases}$$
  2. **Instability trigger and flow propagation:** If $S_t(x) \notin \{6, 7\}$, compute the shear:
     $$\Delta V_t(x) = |V(S_t(x+1)) - V(S_t(x-1))|$$
     * If $\Delta V_t(x) \ge 5$: $S_{t+1}(x) = 7$ (vortex roll-up).
     * Else if $\Delta V_t(x) \ge 3$: $S_{t+1}(x) = 6$ (wave instability).
     * Else (laminar flow propagation):
       * If $S_t(x+1) \in \{0, 1, 2\}$ and $S_t(x-1) \notin \{3, 4, 5\}$: $S_{t+1}(x) = S_t(x+1)$.
       * If $S_t(x-1) \in \{3, 4, 5\}$ and $S_t(x+1) \notin \{0, 1, 2\}$: $S_{t+1}(x) = S_t(x-1)$.
       * If both: $S_{t+1}(x) = 6$ (collision shear).
       * Otherwise: $S_{t+1}(x) = S_t(x)$.
* **Mathematical Rationale:** Models the transition of a sheared interface between opposing fluid layers. When the velocity difference across the interface is high, it triggers Kelvin-Helmholtz instability, rolling the cell into a vortex (7). The vortices then relax and dissipate back into standard flows.
* **Expected Visual Behavior:** Alternating rolling structures along the boundaries of left-propagating and right-propagating flows, resembling a classic vortex train.

### Rule 9: Evaporative Convection (Marangoni)
* **States ($N$):** $6$ states ($0, 1, \dots, 5$) representing surfactant concentration on a fluid surface.
  * State $0$: Pure fluid (high surface tension).
  * States $1, \dots, 5$: Surfactant concentration (increasing concentration, lower surface tension).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself.
* **Transition Function:**
  Let $M_t(x) = \max\left(S_t(x-1), S_t(x+1)\right)$ be the maximum neighbor concentration.
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  \max\left(S_t(x), M_t(x) - 1\right) & \text{if } S_t(x) < M_t(x) \quad (\text{marangoni spreading}) \\
  \max\left(0, S_t(x) - 2\right) & \text{if } S_t(x) > M_t(x) \quad (\text{peak discharge & evaporation}) \\
  S_t(x) - 1 & \text{if } S_t(x) = M_t(x) \text{ and } S_t(x) > 0 \quad (\text{standard evaporation}) \\
  0 & \text{otherwise } (S_t(x) = 0 \text{ and } M_t(x) = 0)
  \end{cases}$$
* **Mathematical Rationale:** The Marangoni effect drives fluid flow from regions of low surface tension (high concentration) to high surface tension (low concentration). This causes surfactant to spread outward. Peak concentration cells drop rapidly (decaying by 2) as they spread their mass in both directions and evaporate.
* **Expected Visual Behavior:** Spreading waves of surfactant that widen and thin out over time, leaving behind triangular-shaped space-time dilution plumes that eventually evaporate completely.

### Rule 10: Porous Darcy Gravity Currents
* **States ($N$):** $8$ states ($0, 1, \dots, 7$) representing the fluid column height in a porous matrix.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Define the directional flow from cell $y$ to cell $x$, gated by a capillary trapping threshold ($S \ge 3$):
  $$F_t(y \to x) = \begin{cases}
  1 & \text{if } S_t(y) \ge 3 \text{ and } S_t(y) > S_t(x) \\
  0 & \text{otherwise}
  \end{cases}$$
  Compute the fluid gain and loss at cell $x$:
  $$\text{Gain}_t(x) = F_t(x-1 \to x) + F_t(x+1 \to x)$$
  $$\text{Loss}_t(x) = F_t(x \to x-1) + F_t(x \to x+1)$$
  The new state height is:
  $$S_{t+1}(x) = \max\left(0, \min\left(7, S_t(x) + \text{Gain}_t(x) - \text{Loss}_t(x)\right)\right)$$
* **Mathematical Rationale:** Models gravity-driven drainage through a porous medium governed by Darcy's law, where flow velocity is proportional to the fluid height (pressure) gradient. The threshold ($S \ge 3$) models capillary trapping forces: if the fluid column is too thin ($S < 3$), surface tension forces within the pores exceed gravity, trapping the fluid in place.
* **Expected Visual Behavior:** Drainage patterns that smooth out high columns but stop abruptly when they hit the capillary threshold, leaving behind stable, trapped residual columns (cliffs) rather than flattening completely.
