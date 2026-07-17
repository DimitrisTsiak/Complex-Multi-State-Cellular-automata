# Loop 3 Cellular Automata Rules: Reaction-Diffusion & Chemical Waves

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Reaction-Diffusion & Chemical Waves**. 

In this domain, cellular automata model physical chemistry phenomena where multiple interacting variables (such as activators and inhibitors, or temperatures and fuels) undergo local diffusion and non-linear chemical reactions. Unlike previous loops, these rules partition the discrete cell state $S_t(x)$ into decoupled chemical components (e.g., activator concentration and inhibitor density) or directly implement spatial operators like the discrete Laplacian to capture classic continuous partial differential equation (PDE) dynamics.

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Discrete Gray-Scott Activator-Inhibitor](#rule-1-discrete-gray-scott-activator-inhibitor) | 8 | Radius $r=1, 2$ | Dual-range activator-inhibitor coupling | Self-replicating spots and wave fronts |
| **2** | [FitzHugh-Nagumo Excitable Wave](#rule-2-fitzhugh-nagumo-excitable-wave) | 6 | Radius $r=1, 2$ | Threshold excitation gated by recovery sum | Clean excitable waves and spiral fragments |
| **3** | [Autocatalytic Reversible Brusselator](#rule-3-autocatalytic-reversible-brusselator) | 8 | Radius $r=1, 3$ | Autocatalytic $2X+Y \to 3X$ substrate depletion | Rhythmic oscillations and breathing wave fronts |
| **4** | [Chiral Oregonator (BZ with Flow)](#rule-4-chiral-oregonator-bz-with-flow) | 9 | Asymmetric $r=2$, $r=1$ | Asymmetric-advection BZ reaction kinetics | Unidirectionally drifting chemical wave trains |
| **5** | [Turing Patterning Sandpile](#rule-5-turing-patterning-sandpile) | 6 | Radius $r=1, 3$ | Curvature-activated long-range inhibition | Self-organizing periodic Turing stripes |
| **6** | [Precipitation-Dissolution (Liesegang Rings)](#rule-6-precipitation-dissolution-liesegang-rings) | 7 | Radius $r=1$ | Immobility reaction with local redissolution | Periodic precipitate bands separated by gaps |
| **7** | [Thermally-Coupled Combustion Wave](#rule-7-thermally-coupled-combustion-wave) | 8 | Radius $r=1$ (incl. self) | Temperature diffusion with fuel consumption | Expanding fire fronts and collision annihilation |
| **8** | [Anomalous Fractional Diffusion Wave](#rule-8-anomalous-fractional-diffusion-wave) | 7 | Radius $r=1, 3$ | Levy-flight super-diffusion and saturation | Non-local jumps and nested wave hierarchies |
| **9** | [Solute-Inhibited Crystallization](#rule-9-solute-inhibited-crystallization) | 8 | Radius $r=1$ | Melting boundary solidification and rejection | Dendritic branching and solute-rich channels |
| **10** | [Stefan Gradient-Stifled Cross-Diffusion](#rule-10-stefan-gradient-stifled-cross-diffusion) | 6 | Radius $r=1$ | Gradient-gated phase interface barrier | Step-like flat plateaus and sharp wave edges |

---

## Rule Definitions

### Rule 1: Discrete Gray-Scott Activator-Inhibitor
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * Activator concentration $u \in \{0, 1, 2, 3\}$, decoded as: $u_t(x) = S_t(x) \pmod 4$.
  * Inhibitor concentration $v \in \{0, 1\}$, decoded as: $v_t(x) = \lfloor S_t(x) / 4 \rfloor$.
* **Neighborhood ($N_1(x), N_2(x)$):**
  * Inner neighborhood (radius 1): $N_1(x) = \{x-1, x, x+1\}$
  * Outer neighborhood (radius 2): $N_2(x) = \{x-2, x-1, x, x+1, x+2\}$
* **Transition Function:**
  Let the local activator sum be:
  $$A_{local}(x) = \sum_{y \in N_1(x)} u_t(y)$$
  Let the local inhibitor sum be:
  $$I_{local}(x) = \sum_{y \in N_2(x)} v_t(y)$$
  The next activator state $u_{t+1}(x)$ is defined as:
  $$u_{t+1}(x) = \begin{cases}
  \max(0, u_t(x) - 1) & \text{if } I_{local}(x) \ge 2 \\
  \min(3, u_t(x) + 1) & \text{else if } I_{local}(x) < 2 \text{ and } A_{local}(x) \ge 3 \\
  u_t(x) & \text{otherwise}
  \end{cases}$$
  The next inhibitor state $v_{t+1}(x)$ is defined as:
  $$v_{t+1}(x) = \begin{cases}
  1 & \text{if } u_t(x) = 3 \\
  0 & \text{else if } u_t(x) = 0 \\
  v_t(x) & \text{otherwise}
  \end{cases}$$
  The combined state is:
  $$S_{t+1}(x) = u_{t+1}(x) + 4 \cdot v_{t+1}(x)$$
* **Mathematical Rationale:** Mimics the classic Gray-Scott activator-inhibitor system. Activator $u$ undergoes autocatalytic growth ($u \to u+1$) when local activator concentration is high ($A_{local} \ge 3$) and inhibitor is low ($I_{local} < 2$). Peak activator density triggers inhibitor production ($v = 1$), which diffuses over a wider range ($r=2$) and suppresses the activator.
* **Expected Visual Behavior:** Self-replicating active spots, expanding wavefronts, and Turing-like stable structures that periodically split.

### Rule 2: FitzHugh-Nagumo Excitable Wave
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * Activator voltage $a \in \{0, 1, 2\}$, decoded as: $a_t(x) = S_t(x) \pmod 3$.
  * Recovery inhibitor $w \in \{0, 1\}$, decoded as: $w_t(x) = \lfloor S_t(x) / 3 \rfloor$.
* **Neighborhood ($N_1(x), N_2(x)$):**
  * Activator diffusion neighborhood (radius 1 excluding self): $N_1(x) = \{x-1, x+1\}$
  * Inhibitor diffusion neighborhood (radius 2 excluding self): $N_2(x) = \{x-2, x-1, x+1, x+2\}$
* **Transition Function:**
  Let the surrounding activator activity be:
  $$A_{diff}(x) = \sum_{y \in N_1(x)} a_t(y)$$
  Let the surrounding inhibitor activity be:
  $$W_{diff}(x) = \sum_{y \in N_2(x)} w_t(y)$$
  The next activator state $a_{t+1}(x)$ is defined as:
  $$a_{t+1}(x) = \begin{cases}
  1 & \text{if } a_t(x) = 0 \text{ and } w_t(x) = 0 \text{ and } A_{diff}(x) \ge 2 \\
  2 & \text{if } a_t(x) = 1 \text{ and } W_{diff}(x) \le 1 \\
  0 & \text{if } a_t(x) = 1 \text{ and } W_{diff}(x) \ge 2 \\
  0 & \text{if } a_t(x) = 2
  \end{cases}$$
  The next inhibitor state $w_{t+1}(x)$ is defined as:
  $$w_{t+1}(x) = \begin{cases}
  1 & \text{if } a_t(x) = 2 \\
  0 & \text{if } a_t(x) = 0 \text{ and } W_{diff}(x) \le 1 \\
  w_t(x) & \text{otherwise}
  \end{cases}$$
  The combined state is:
  $$S_{t+1}(x) = a_{t+1}(x) + 3 \cdot w_{t+1}(x)$$
* **Mathematical Rationale:** Discretizes the FitzHugh-Nagumo model where the excitation threshold depends on the recovery variable $w$. High local inhibitor presence ($W_{diff} \ge 2$) blocks rising excitation (holding it at $a=0$ or reverting $a=1 \to 0$). Once excitation peaks ($a=2$), it activates the inhibitor ($w=1$), which remains active until local inhibitor density falls, ensuring a refractory trail.
* **Expected Visual Behavior:** Propagating wave fronts with a distinct refractory tail. Wave collisions result in mutual annihilation, and local blocks generate spiral-like structures.

### Rule 3: Autocatalytic Reversible Brusselator
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * Activator species $X \in \{0, 1, 2, 3\}$, decoded as: $X_t(x) = S_t(x) \pmod 4$.
  * Substrate species $Y \in \{0, 1\}$, decoded as: $Y_t(x) = \lfloor S_t(x) / 4 \rfloor$.
* **Neighborhood ($N_1(x), N_3(x)$):**
  * Activator neighborhood (radius 1 excluding self): $N_1(x) = \{x-1, x+1\}$
  * Substrate neighborhood (radius 3 excluding self): $N_3(x) = \{x-3, x-2, x-1, x+1, x+2, x+3\}$
* **Transition Function:**
  Let the local activator sum be:
  $$X_{sum}(x) = \sum_{y \in N_1(x)} X_t(y)$$
  Let the local substrate sum be:
  $$Y_{sum}(x) = \sum_{y \in N_3(x)} Y_t(y)$$
  The next substrate $Y_{t+1}(x)$ is:
  $$Y_{t+1}(x) = \begin{cases}
  1 & \text{if } Y_t(x) = 0 \text{ and } Y_{sum}(x) \le 2 \\
  0 & \text{if } Y_t(x) = 1 \text{ and } X_t(x) \ge 2 \\
  Y_t(x) & \text{otherwise}
  \end{cases}$$
  The next activator $X_{t+1}(x)$ is:
  $$X_{t+1}(x) = \begin{cases}
  \min(3, X_t(x) + 1) & \text{if } Y_t(x) = 1 \text{ and } (X_t(x) \ge 1 \text{ or } X_{sum}(x) \ge 2) \\
  \max(0, X_t(x) - 1) & \text{if } Y_t(x) = 0 \\
  X_t(x) & \text{otherwise}
  \end{cases}$$
  The combined state is:
  $$S_{t+1}(x) = X_{t+1}(x) + 4 \cdot Y_{t+1}(x)$$
* **Mathematical Rationale:** Implements the autocatalytic reaction loop $2X + Y \to 3X$ from the Brusselator. Substrate $Y$ acts as chemical fuel, diffusing quickly at long-range ($r=3$), and is consumed when activator concentration is high. The activator grows only in the presence of substrate fuel, decaying when fuel is depleted.
* **Expected Visual Behavior:** Periodic chemical oscillations, breathing structures, and wave envelopes with alternating phase structures.

### Rule 4: Chiral Oregonator (BZ with Flow)
* **States ($N$):** $9$ states ($0, 1, \dots, 8$).
  * Bromous acid (Activator) $A \in \{0, 1, 2\}$, decoded as: $A_t(x) = S_t(x) \pmod 3$.
  * Catalyst (Inhibitor) $C \in \{0, 1, 2\}$, decoded as: $C_t(x) = \lfloor S_t(x) / 3 \rfloor$.
* **Neighborhood ($N_{chiral}(x), N_1(x)$):**
  * Left-biased asymmetric neighborhood (radius 2): $N_{chiral}(x) = \{x-2, x-1, x+1\}$
  * Symmetric catalyst neighborhood (radius 1): $N_1(x) = \{x-1, x, x+1\}$
* **Transition Function:**
  Let the weighted asymmetric activator sum be:
  $$A_{chiral}(x) = A_t(x-2) + 2 \cdot A_t(x-1) + A_t(x+1)$$
  The next activator state $A_{t+1}(x)$ is:
  $$A_{t+1}(x) = \begin{cases}
  1 & \text{if } A_t(x) = 0 \text{ and } C_t(x) = 0 \text{ and } A_{chiral}(x) \ge 2 \\
  2 & \text{if } A_t(x) = 1 \text{ and } C_t(x) \le 1 \\
  \max(0, A_t(x) - 1) & \text{if } A_t(x) \ge 1 \text{ and } C_t(x) = 2 \\
  1 & \text{if } A_t(x) = 2 \text{ and } C_t(x) \le 1 \\
  A_t(x) & \text{otherwise}
  \end{cases}$$
  The next catalyst state $C_{t+1}(x)$ is:
  $$C_{t+1}(x) = \begin{cases}
  \min(2, C_t(x) + 1) & \text{if } A_t(x) = 2 \\
  \max(0, C_t(x) - 1) & \text{if } A_t(x) = 0 \\
  C_t(x) & \text{otherwise}
  \end{cases}$$
  The combined state is:
  $$S_{t+1}(x) = A_{t+1}(x) + 3 \cdot C_{t+1}(x)$$
* **Mathematical Rationale:** Models the Belousov-Zhabotinsky reaction using Oregonator kinetics. The left-heavy asymmetric neighborhood $N_{chiral}$ introduces directionality, simulating advective fluid flow or active stirring, which tilts the wave propagation path.
* **Expected Visual Behavior:** Asymmetric, drifting chemical wave trains moving steadily in one direction.

### Rule 5: Turing Patterning Sandpile
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
* **Neighborhood ($N_1(x), N_{outer}(x)$):**
  * Inner neighborhood (radius 1 excluding self): $N_1(x) = \{x-1, x+1\}$
  * Outer neighborhood (radius 3 excluding inner): $N_{outer}(x) = \{x-3, x-2, x+2, x+3\}$
* **Transition Function:**
  Let the discrete Laplacian (local curvature) of the state be:
  $$L_t(x) = S_t(x-1) - 2 S_t(x) + S_t(x+1)$$
  Let the outer inhibitor sum be:
  $$I_t(x) = \sum_{y \in N_{outer}(x)} S_t(y)$$
  The state change $\Delta S_t(x)$ is:
  $$\Delta S_t(x) = \begin{cases}
  1 & \text{if } L_t(x) \ge 1 \text{ and } I_t(x) \le 6 \\
  -1 & \text{if } L_t(x) \le -1 \text{ or } I_t(x) \ge 10 \\
  0 & \text{otherwise}
  \end{cases}$$
  The next state is clamped to the range $[0, 5]$:
  $$S_{t+1}(x) = \max(0, \min(5, S_t(x) + \Delta S_t(x)))$$
* **Mathematical Rationale:** Turing instability relies on local activation and long-range inhibition. Here, local curvature (discrete Laplacian $L_t \ge 1$, showing neighbor concentrations are higher) acts as the activation mechanism, while high concentration in the outer shell ($I_t \ge 10$) triggers decay, replicating discrete Turing patterning.
* **Expected Visual Behavior:** Self-organizing periodic stripes (Turing patterns) that stabilize into static or slowly breathing vertical bands in space-time.

### Rule 6: Precipitation-Dissolution (Liesegang Rings)
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State 0: Quiescent/empty.
  * States 1, 2: Soluble Reactant A (low and high concentration).
  * States 3, 4: Soluble Reactant B (low and high concentration).
  * States 5, 6: Immobile Precipitate (low and high density).
* **Neighborhood ($N_{side}(x)$):** Radius 1 excluding self: $N_{side}(x) = \{x-1, x+1\}$.
* **Transition Function:**
  Let $A_{count}(x) = \sum_{y \in N_{side}(x)} \mathbb{I}(S_t(y) \in \{1, 2\})$ (neighboring Reactant A).
  Let $B_{count}(x) = \sum_{y \in N_{side}(x)} \mathbb{I}(S_t(y) \in \{3, 4\})$ (neighboring Reactant B).
  
  For $S_t(x) = 0$ (empty):
  $$S_{t+1}(x) = \begin{cases}
  5 & \text{if } A_{count}(x) \ge 1 \text{ and } B_{count}(x) \ge 1 \\
  1 & \text{if } A_{count}(x) \ge 1 \text{ and } B_{count}(x) = 0 \\
  3 & \text{if } B_{count}(x) \ge 1 \text{ and } A_{count}(x) = 0 \\
  0 & \text{otherwise}
  \end{cases}$$
  
  For $S_t(x) \in \{1, 2\}$ (Reactant A):
  $$S_{t+1}(x) = \begin{cases}
  5 & \text{if } B_{count}(x) \ge 1 \\
  2 & \text{else if } A_{count}(x) \ge 2 \\
  0 & \text{else if } A_{count}(x) = 0 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
  
  For $S_t(x) \in \{3, 4\}$ (Reactant B):
  $$S_{t+1}(x) = \begin{cases}
  5 & \text{if } A_{count}(x) \ge 1 \\
  4 & \text{else if } B_{count}(x) \ge 2 \\
  0 & \text{else if } B_{count}(x) = 0 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
  
  For $S_t(x) \in \{5, 6\}$ (Precipitate):
  $$S_{t+1}(x) = \begin{cases}
  6 & \text{if } S_t(x) = 5 \text{ and } A_{count}(x) \ge 1 \text{ and } B_{count}(x) \ge 1 \\
  1 & \text{if } S_t(x) = 5 \text{ and } A_{count}(x) \ge 2 \text{ and } B_{count}(x) = 0 \\
  3 & \text{if } S_t(x) = 5 \text{ and } B_{count}(x) \ge 2 \text{ and } A_{count}(x) = 0 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** When diffusing reactants A and B meet, they react to form precipitate $P$ ($S_t \in \{5, 6\}$), which is immobile. High local concentrations of A or B without the other cause slow dissolution of $P$ back into the mobile phase, capturing periodic Liesegang ring formation.
* **Expected Visual Behavior:** Clear, periodic bands of immobile precipitate separated by gaps of empty space, forming Liesegang-like patterns.

### Rule 7: Thermally-Coupled Combustion Wave
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * Temperature $T \in \{0, 1, 2, 3\}$, decoded as: $T_t(x) = S_t(x) \pmod 4$.
  * Fuel present $F \in \{0, 1\}$, decoded as: $F_t(x) = \lfloor S_t(x) / 4 \rfloor$.
* **Neighborhood ($N_{all}(x)$):** Radius 1 including self: $N_{all}(x) = \{x-1, x, x+1\}$.
* **Transition Function:**
  Let the local average temperature be:
  $$T_{local}(x) = \frac{1}{3} \sum_{y \in N_{all}(x)} T_t(y)$$
  The next temperature $T_{t+1}(x)$ and fuel $F_{t+1}(x)$ are:
  * If fuel is present ($F_t(x) = 1$):
    - Combustion trigger: if $T_t(x) \ge 1$ or $\max_{y \in N_{all}(x)} T_t(y) \ge 2$:
      $$T_{t+1}(x) = 3, \quad F_{t+1}(x) = 0$$
    - Otherwise (below ignition temperature):
      $$T_{t+1}(x) = \lfloor T_{local}(x) \rfloor, \quad F_{t+1}(x) = 1$$
  * If fuel is exhausted ($F_t(x) = 0$):
    - Cool down and diffusion:
      $$T_{t+1}(x) = \max(0, \lfloor T_{local}(x) \rfloor - 1), \quad F_{t+1}(x) = 0$$
  The combined state is:
  $$S_{t+1}(x) = T_{t+1}(x) + 4 \cdot F_{t+1}(x)$$
* **Mathematical Rationale:** Simulates an exothermic reaction wave. Fuel $F$ combined with heat $T$ triggers combustion, raising local temperature to maximum ($T=3$) and consuming fuel ($F=0$). Heat diffuses to adjacent cells, while burned-out cells gradually cool down to 0, forming a non-recoverable refractory zone.
* **Expected Visual Behavior:** Rapidly propagating thermal fronts. Colliding wavefronts annihilate due to the exhaustion of fuel behind them, leaving dark quiescent trails.

### Rule 8: Anomalous Fractional Diffusion Wave
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
* **Neighborhood ($N_1(x), N_3(x)$):**
  * Short-range neighborhood (radius 1): $N_1(x) = \{x-1, x+1\}$
  * Long-range neighborhood (radius 3): $N_3(x) = \{x-3, x+3\}$
* **Transition Function:**
  Let the active neighbor counts (state $\ge 1$) be:
  $$C_1(x) = \sum_{y \in N_1(x)} \mathbb{I}(S_t(y) \ge 1)$$
  $$C_3(x) = \sum_{y \in N_3(x)} \mathbb{I}(S_t(y) \ge 1)$$
  The effective fractional diffusion density $D_t(x)$ is:
  $$D_t(x) = 2 \cdot C_1(x) + C_3(x)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } D_t(x) \in \{2, 3\} \\
  S_t(x) + 1 & \text{if } S_t(x) \ge 1 \text{ and } S_t(x) < 4 \\
  (S_t(x) + 1) \pmod 7 & \text{if } S_t(x) \ge 4 \\
  0 & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Combines local (radius 1) and long-range (radius 3) neighbors in the activation function. This models anomalous fractional diffusion (super-diffusion), where chemical transport can bypass intermediate regions via Levy flights.
* **Expected Visual Behavior:** Branching wave structures and non-local "islands" of excitation that form ahead of the main propagating front, generating complex nested patterns.

### Rule 9: Solute-Inhibited Crystallization
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State 0: Pure liquid.
  * States 1, 2, 3: Solute-enriched liquid (freezing inhibitor).
  * States 4, 5, 6, 7: Solid/crystalline phase.
* **Neighborhood ($N_{side}(x)$):** Radius 1 excluding self: $N_{side}(x) = \{x-1, x+1\}$.
* **Transition Function:**
  Let the solid neighbor count be:
  $$Solid_{count}(x) = \sum_{y \in N_{side}(x)} \mathbb{I}(S_t(y) \ge 4)$$
  
  For liquid states ($S_t(x) < 4$):
  * Solidification: if $Solid_{count}(x) \ge 1$:
    - If $S_t(x) = 0$: solidifies, $S_{t+1}(x) = 4$.
    - If $S_t(x) \in \{1, 2, 3\}$: solidifies only if $S_t(x) + Solid_{count}(x) \le 3$. If it solidifies, $S_{t+1}(x) = 4$.
  * Solute rejection: if the cell remains liquid but has a solid neighbor:
    $$S_{t+1}(x) = \min(3, S_t(x) + 1)$$
  * Otherwise, it remains unchanged.
  
  For solid states ($S_t(x) \ge 4$):
  * Annealing (crystallization maturation):
    $$S_{t+1}(x) = \begin{cases}
    S_t(x) + 1 & \text{if } S_t(x) < 7 \\
    7 & \text{if } S_t(x) = 7
    \end{cases}$$
* **Mathematical Rationale:** Models crystallization from a liquid melt. Solidification rejects solute into adjacent liquid, raising its solute concentration ($S \in \{1, 2, 3\}$). High solute acts as a local freezing inhibitor, requiring a higher density of solid neighbors to overcome the chemical barrier.
* **Expected Visual Behavior:** Dendritic, tree-like growth structures with rough crystallization fronts and pockets of trapped liquid phase.

### Rule 10: Stefan Gradient-Stifled Cross-Diffusion
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
* **Neighborhood ($N_{side}(x)$):** Radius 1 excluding self: $N_{side}(x) = \{x-1, x+1\}$.
* **Transition Function:**
  Let the local state gradient of neighbor $y$ be:
  $$G_t(y) = |S_t(y+1) - S_t(y-1)|$$
  Let the gradient-stifled diffusion flux into cell $x$ be:
  $$Flux_t(x) = \sum_{y \in N_{side}(x)} S_t(y) \cdot \mathbb{I}(G_t(y) \le 1)$$
  The next state $S_{t+1}(x)$ is:
  $$S_{t+1}(x) = \begin{cases}
  \min(5, S_t(x) + 1) & \text{if } S_t(x) \le 2 \text{ and } Flux_t(x) \ge 3 \\
  \max(0, S_t(x) - 1) & \text{if } S_t(x) \ge 3 \text{ and } Flux_t(x) \le 1 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Models cross-diffusion across phase boundaries (Stefan problem). In high-gradient regions ($G_t > 1$), diffusion is shut down, representing a sharp phase interface barrier. Low-gradient regions ($G_t \le 1$) allow normal diffusion, resulting in phase separation.
* **Expected Visual Behavior:** Step-like shock waves, flat concentration plateaus, and exceptionally sharp phase boundaries.
