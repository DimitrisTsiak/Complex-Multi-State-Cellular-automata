# Loop 14 Cellular Automata Rules: String Theory

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **String Theory**.

Unlike the classical physical systems or stochastic processes modeled in previous loops, the rules in this loop utilize concepts from string theory, such as supersymmetry, open/closed string worldsheets, D-branes, Calabi-Yau compactification, T-duality, S-duality, tachyon condensation, boundary-to-bulk holographic projections (AdS/CFT), loop quantum gravity, and fuzzball black holes. These rules operate on a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates complex, multidimensional, and dual geometric behaviors.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Boson-Fermion Supersymmetric Pairing](#rule-1-boson-fermion-supersymmetric-pairing) | 6 | Radius $r=1$ | Supersymmetric pairing, Pauli exclusion, and superpartner decay | Self-regulating patterns of propagating waves and stable boundaries |
| **2** | [Open and Closed String Worldsheet Dynamics](#rule-2-open-and-closed-string-worldsheet-dynamics) | 8 | Radius $r=1$ | Free closed string propagation and D-brane open string reflections | Colliding closed strings creating transient open string segments |
| **3** | [Calabi-Yau Dimension Compactification](#rule-3-calabi-yau-dimension-compactification) | 12 | Radius $r=1$ | Modular compactified coordinate flow dictating external spacetime dynamics | Heterogeneous domains of linear diffusion, excitable waves, and chaos |
| **4** | [T-Duality and Winding-Momentum Exchange](#rule-4-t-duality-and-winding-momentum-exchange) | 8 | Radius $r=1$ | Density-dependent duality toggle swapping momentum and winding modes | Self-regulating domains transitioning between stable and wave-like states |
| **5** | [Tachyon Condensation and Vacuum Decay](#rule-5-tachyon-condensation-and-vacuum-decay) | 5 | Radius $r=2$ | Bubble expansion of stable vacuum and topological kink creation | Expanding stable domains with stable vertical boundaries |
| **6** | [S-Duality Strong-Weak Coupling Duality](#rule-6-s-duality-strong-weak-coupling-duality) | 8 | Radius $r=1, 2$ | Dynamic coupling regime toggle mapping weak fields to strong solitons | Coexisting domains of linear wave interference and discrete solitons |
| **7** | [Holographic Boundary-to-Bulk Projection (AdS/CFT)](#rule-7-holographic-boundary-to-bulk-projection-adscft) | 10 | Radius $r=1, 2$ | Autonomous boundary CFT projecting into a holographic gravity bulk | Alternating grid showing boundary chaos driving bulk wave envelopes |
| **8** | [Conformal Worldsheet Loop Dynamics](#rule-8-conformal-worldsheet-loop-dynamics) | 6 | Radius $r=1$ | Conformal loop expansion, junction creation, and singularity evaporation | Geometric diamond structures representing string loop histories |
| **9** | [D-Brane Collision and Open String Creation](#rule-9-d-brane-collision-and-open-string-creation) | 6 | Radius $r=1$ | Collision of moving D-brane defects creating stretching open strings | Converging walls colliding to spawn growing segments of string bodies |
| **10** | [Fuzzball Horizon Information Scrambler](#rule-10-fuzzball-horizon-information-scrambler) | 8 | Radius $r=1$ | Particle absorption and chaotic horizon scrambling with evaporation | Infalling particles absorbed by a flickering, radiating horizon zone |

---

## Rule Definitions

### Rule 1: Boson-Fermion Supersymmetric Pairing
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Spacetime vacuum $|0\rangle$.
  * State $1$: Boson mode $B_1$ (low energy).
  * State $2$: Boson mode $B_2$ (high energy).
  * State $3$: Fermion mode $F_1$ (low energy).
  * State $4$: Fermion mode $F_2$ (high energy).
  * State $5$: Supersymmetric Bound State / Partner Pair $S$.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $N_B(x) = \sum_{y \in \{x-1, x+1\}} \mathbb{I}(S_t(y) \in \{1, 2\})$ be the number of active bosonic neighbors.
  Let $N_F(x) = \sum_{y \in \{x-1, x+1\}} \mathbb{I}(S_t(y) \in \{3, 4\})$ be the number of active fermionic neighbors.
  
  * **If $S_t(x) = 0$ (Vacuum):**
    - If there is at least one boson neighbor and one fermion neighbor, they pair up:
      If $N_B(x) \ge 1$ and $N_F(x) \ge 1$, then $S_{t+1}(x) = 5$.
    - Else, if boson neighbors dominate, a low-energy boson is created:
      If $N_B(x) \ge 2$, then $S_{t+1}(x) = 1$.
    - Else, if fermion neighbors dominate, a low-energy fermion is created:
      If $N_F(x) \ge 2$, then $S_{t+1}(x) = 3$.
    - Otherwise, remains vacuum: $S_{t+1}(x) = 0$.
  * **If $S_t(x) \in \{1, 2\}$ (Boson):**
    - Under a local supersymmetry transformation $Q$, the excess of neighboring fermions converts the boson into its partner fermion:
      If $N_F(x) > N_B(x)$, then $S_{t+1}(x) = S_t(x) + 2$.
    - Else, if $S_t(x) = 1$ and it is stimulated by adjacent bosons, it excites:
      If $S_t(x-1) = 1$ and $S_t(x+1) = 1$, then $S_{t+1}(x) = 2$.
    - Else, if $S_t(x) = 2$, it decays back to vacuum: $S_{t+1}(x) = 0$.
    - Otherwise, remains same: $S_{t+1}(x) = S_t(x)$.
  * **If $S_t(x) \in \{3, 4\}$ (Fermion):**
    - Under a local supersymmetry transformation $\bar{Q}$, the excess of neighboring bosons converts the fermion into its partner boson:
      If $N_B(x) > N_F(x)$, then $S_{t+1}(x) = S_t(x) - 2$.
    - Pauli Exclusion Principle: Two identical adjacent fermions cannot occupy the same state space. If adjacent to an identical fermion, they annihilate to vacuum:
      If $S_t(x-1) = S_t(x)$ or $S_t(x+1) = S_t(x)$, then $S_{t+1}(x) = 0$.
    - Otherwise, remains same: $S_{t+1}(x) = S_t(x)$.
  * **If $S_t(x) = 5$ (Supersymmetric Bound State):**
    - The bound state decays into its constituent particles based on local spatial parity:
      If $S_t(x-1) \pmod 2 \equiv 0$, it decays to a low-energy boson: $S_{t+1}(x) = 1$.
      Else, it decays to a low-energy fermion: $S_{t+1}(x) = 3$.
* **Mathematical Rationale:**
  Supersymmetry (SUSY) relates bosons (integer spin) and fermions (half-integer spin) via supercharge generators $Q$ and $\bar{Q}$. This rule models a discrete version of this pairing: the local density of fermions or bosons acts as the supercharge operator prompting state conversion. Additionally, it implements the Pauli Exclusion Principle for fermionic states, preventing identical fermions from clustering, and models the formation/decay of boson-fermion bound states.
* **Expected Visual Behavior:**
  A balanced, self-regulating space-time diagram where bosonic propagation waves are dynamically checked by fermionic exclusion zones. The supersymmetric bound states (state 5) act as slow-moving localized defects or boundaries, leading to rich, structured, and non-trivial patterns.

---

### Rule 2: Open and Closed String Worldsheet Dynamics
* **States ($N$):** $8$ states ($0, 1, 2, 3, 4, 5, 6, 7$).
  * State $0$: Empty spacetime bulk.
  * State $1$: Left-moving open string endpoint.
  * State $2$: Right-moving open string endpoint.
  * State $3$: Open string body.
  * State $4$: Left-moving closed string mode.
  * State $5$: Right-moving closed string mode.
  * State $6$: Closed string intersection/knot.
  * State $7$: D-brane (Dirichlet boundary).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  - If $S_t(x) = 7$ (D-brane), it remains static:
    $$S_{t+1}(x) = 7$$
  - If $S_t(x) = 0$ (Vacuum):
    - Collision of closed strings: If $S_t(x-1) = 5$ and $S_t(x+1) = 4$, they collide:
      $$S_{t+1}(x) = 6$$
    - Propagation of closed strings:
      If only $S_t(x-1) = 5$: $S_{t+1}(x) = 5$.
      If only $S_t(x+1) = 4$: $S_{t+1}(x) = 4$.
    - Open string body propagation:
      If $S_t(x-1) = 3$ and $S_t(x+1) = 2$: $S_{t+1}(x) = 3$.
      If $S_t(x+1) = 3$ and $S_t(x-1) = 1$: $S_{t+1}(x) = 3$.
    - Otherwise, remains vacuum: $S_{t+1}(x) = 0$.
  - If $S_t(x) = 1$ (Left-moving endpoint):
    - Reflection: If $S_t(x-1) = 7$, then $S_{t+1}(x) = 2$.
    - Propagation: If $S_t(x-1) \neq 7$, it propagates left:
      $$S_{t+1}(x) = \begin{cases} 3 & \text{if } S_t(x+1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  - If $S_t(x) = 2$ (Right-moving endpoint):
    - Reflection: If $S_t(x+1) = 7$, then $S_{t+1}(x) = 1$.
    - Propagation: If $S_t(x+1) \neq 7$, it propagates right:
      $$S_{t+1}(x) = \begin{cases} 3 & \text{if } S_t(x-1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  - If $S_t(x) = 3$ (Open string body):
    - It must be supported by endpoints:
      $$S_{t+1}(x) = \begin{cases} 3 & \text{if } (S_t(x-1) \in \{1, 3\} \text{ and } S_t(x+1) \in \{2, 3\}) \\ 0 & \text{otherwise} \end{cases}$$
  - If $S_t(x) = 4$ (Left-moving closed string mode):
    - It propagates left: $S_{t+1}(x) = S_t(x+1)$ (if $S_t(x+1) = 4$ or $0$, else decays to $0$).
  - If $S_t(x) = 5$ (Right-moving closed string mode):
    - It propagates right: $S_{t+1}(x) = S_t(x-1)$ (if $S_t(x-1) = 5$ or $0$, else decays to $0$).
  - If $S_t(x) = 6$ (Closed string intersection):
    - The high-mass knot decays, splitting into a pair of open string endpoints that stretch an open string body:
      $$S_{t+1}(x) = 3, \quad S_{t+1}(x-1) = 1, \quad S_{t+1}(x+1) = 2$$
* **Mathematical Rationale:**
  In string theory, open strings have endpoints that end on D-branes (Dirichlet boundaries), while closed strings have no endpoints and propagate freely through spacetime. This rule captures these distinct boundary conditions: closed strings propagate freely, while open strings are bound by endpoints that reflect when hitting a D-brane. A collision of closed strings creates a localized high-energy state (a knot), which decays back into open string segments, reflecting the stringy interactions that couple open and closed sectors.
* **Expected Visual Behavior:**
  Clear diagonal tracks representing left- and right-moving closed strings. Open strings form segment tracks that bounce back and forth between static D-brane walls. Collisions of closed strings create localized "explosions" that transition into expanding open string segments.

---

### Rule 3: Calabi-Yau Dimension Compactification
* **States ($N$):** $12$ states ($0, 1, \dots, 11$). We represent each state $s$ as a tuple of external spacetime field $e \in \{0, 1, 2, 3\}$ and internal compactified coordinate $i \in \{0, 1, 2\}$:
  $$s = 3 \cdot e + i$$
  where $e = \lfloor s/3 \rfloor$ and $i = s \pmod 3$.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  First, unpack the states of the neighborhood into $(e_L, i_L)$, $(e_x, i_x)$, and $(e_R, i_R)$.
  
  1. **Internal Compact Dimension Evolution:**
     The internal space coordinates evolve under a local minimization of gradient energy (a discrete modular Laplace-like flow):
     $$i_{t+1}(x) = (i_L + i_x + i_R) \pmod 3$$
  
  2. **External Spacetime Field Evolution:**
     The update of the external field state is determined by the updated internal compactified configuration $i_{t+1}(x)$:
     - **If $i_{t+1}(x) = 0$ (Flat internal geometry):** The external state behaves like a linear wave diffusion:
       $$e_{t+1}(x) = (e_L + e_R) \pmod 4$$
     - **If $i_{t+1}(x) = 1$ (Positively curved internal geometry):** The external state behaves like an excitable medium with state decay:
       $$e_{t+1}(x) = \begin{cases}
       (e_x + 1) \pmod 4 & \text{if } e_x \neq 0 \\
       1 & \text{if } e_x = 0 \text{ and } (e_L = 1 \text{ or } e_R = 1) \\
       0 & \text{otherwise}
       \end{cases}$$
     - **If $i_{t+1}(x) = 2$ (Negative curvature / Singularity):** The external state undergoes highly non-linear chaotic scattering:
       $$e_{t+1}(x) = (e_x^2 + e_L \cdot e_R) \pmod 4$$
  
  Combine the updated coordinates:
  $$S_{t+1}(x) = 3 \cdot e_{t+1}(x) + i_{t+1}(x)$$
* **Mathematical Rationale:**
  In string theory, spacetime is 10-dimensional, where 6 dimensions are compactified into a tiny Calabi-Yau manifold. The shape and topology of the Calabi-Yau manifold at each point of external space dictate the effective physics (equations of motion, coupling strengths) in the external 4D spacetime. This rule models this by pairing each cell with an internal state $i$ and an external state $e$. The internal geometry evolves dynamically, and its value acts as a local "metric" that decides which physical transition rule (linear diffusion, excitable decay, or chaotic scattering) governs the external field $e$.
* **Expected Visual Behavior:**
  A highly heterogeneous space-time pattern. In areas where the internal state settles to $0$, we see smooth linear wave interference. Where the internal state becomes $1$, excitable pulses and spiral-like wave fronts emerge. Near internal singularities ($i = 2$), the external field becomes turbulent and chaotic, illustrating how compactified dimensions dynamically govern external physics.

---

### Rule 4: T-Duality and Winding-Momentum Exchange
* **States ($N$):** $8$ states ($0, 1, \dots, 7$). We represent the state as a pair $(p, w)$ where:
  - $p \in \{0, 1, 2, 3\}$ represents the momentum mode of the string.
  - $w \in \{0, 1\}$ represents the winding number of the string.
  State $s = 2 \cdot p + w$, where $p = \lfloor s/2 \rfloor$ and $w = s \pmod 2$.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let the local winding density determine the effective compactification radius $R$.
  Let $W_{\text{local}}(x) = w_{x-1} + w_x + w_{x+1}$ be the number of wound strings in the neighborhood.
  
  - **If $W_{\text{local}}(x) \ge 2$ (Small radius regime $R \to 0$):**
    Under T-duality, winding modes and momentum modes are exchanged. The transition rules swap the roles of $p$ and $w$:
    $$p_{t+1}(x) = (w_{x-1} + w_{x+1}) \pmod 4$$
    $$w_{t+1}(x) = \mathbb{I}\left( (p_{x-1} + p_x + p_{x+1}) \pmod 2 \equiv 1 \right)$$
  - **If $W_{\text{local}}(x) < 2$ (Large radius regime $R \to \infty$):**
    The system follows standard field theory dynamics, where momentum dominates and winding modes are frozen or slowly diffuse:
    $$p_{t+1}(x) = (p_{x-1} + p_x + p_{x+1}) \pmod 4$$
    $$w_{t+1}(x) = (w_{x-1} + w_{x+1}) \pmod 2$$
  
  Combine the dual components:
  $$S_{t+1}(x) = 2 \cdot p_{t+1}(x) + w_{t+1}(x)$$
* **Mathematical Rationale:**
  T-duality is a stringy symmetry which asserts that a string compactified on a circle of radius $R$ is physically equivalent to a string compactified on a circle of radius $R' = \alpha'/R$ with momentum modes $p$ and winding modes $w$ interchanged. When winding states cluster locally (representing a tiny compactification radius where winding is energy-favorable), T-duality maps this to a dual large-radius description. The CA models this by dynamically switching the transition function, exchanging the algebraic roles of $p$ and $w$ when the local winding density crosses a threshold.
* **Expected Visual Behavior:**
  Regions of high winding density self-regulate, rapidly converting winding states into expanding momentum waves. Conversely, regions of low winding display stable, localized momentum oscillations. The space-time diagram displays a dynamic balancing act with dual textures transitioning into one another.

---

### Rule 5: Tachyon Condensation and Vacuum Decay
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unstable vacuum (Tachyon field at potential maximum, D-brane active).
  * State $1$: Decaying tachyon (rolling down the potential).
  * State $2$: Stable closed string vacuum (potential minimum, D-brane annihilated).
  * State $3$: Open string excitation on the brane.
  * State $4$: Topological defect (stable tachyon kink/vortex).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  - **If $S_t(x) = 0$ (Unstable vacuum):**
    - The decay is triggered by adjacent decaying or stable vacuum cells, or by topological kinks:
      If $\sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{1, 2, 4\}) \ge 1$, then $S_{t+1}(x) = 1$ (decay begins).
      Otherwise, remains $0$.
  - **If $S_t(x) = 1$ (Decaying state):**
    - The field rolls down to the stable minimum:
      $$S_{t+1}(x) = 2$$
  - **If $S_t(x) = 2$ (Stable vacuum):**
    - The D-brane has disappeared here; the closed string vacuum is completely stable:
      $$S_{t+1}(x) = 2$$
  - **If $S_t(x) = 3$ (Open string excitation):**
    - If any neighbor within $r=1$ has decayed to stable vacuum, the open string has no brane to end on and is radiated away (annihilated):
      If $S_t(x-1) = 2$ or $S_t(x+1) = 2$, then $S_{t+1}(x) = 2$.
      Otherwise, the open string propagates as a simple translation:
      $$S_{t+1}(x) = \begin{cases} 3 & \text{if } S_t(x-1) = 3 \text{ and } S_t(x+1) \neq 3 \\ 0 & \text{otherwise} \end{cases}$$
  - **If $S_t(x) = 4$ (Topological defect / Kink):**
    - The defect is stable unless it is surrounded by stable vacuum on both sides, which causes it to dissolve:
      If $S_t(x-1) = 2$ and $S_t(x+1) = 2$, then $S_{t+1}(x) = 2$.
      Else, it shifts dynamically to resolve boundary pressure:
      If $S_t(x-1) = 2$ and $S_t(x+1) = 0$, then $S_{t+1}(x) = 2$ and $S_{t+1}(x+1) = 4$.
      Otherwise, it remains stable: $S_{t+1}(x) = 4$.
* **Mathematical Rationale:**
  Tachyon condensation describes the decay of unstable D-branes. The tachyon field has a negative mass-squared at the origin (state $0$), representing the unstable configuration. As it rolls down to the minimum (state $2$), the D-brane annihilates. Since open strings must end on D-branes, they cannot exist in the stable vacuum (state 2) and are destroyed. At the boundary where different regions roll in opposite directions, stable topological defects (kinks, state $4$) are created.
* **Expected Visual Behavior:**
  From a homogeneous state $0$ with a few seeds of decay, we observe expanding bubbles of stable vacuum (state $2$). Open string excitations (state $3$) are swept away. Where the expanding bubbles collide, stable topological kinks (state $4$) form, appearing as sharp, persistent vertical lines in the space-time diagram.

---

### Rule 6: S-Duality Strong-Weak Coupling Duality
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  We divide the states into two sectors:
  - Weakly coupled sector: States $\{0, 1, 2, 3\}$ (linear, wave-like field modes).
  - Strongly coupled sector: States $\{4, 5, 6, 7\}$ (highly nonlinear, localized soliton modes).
* **Neighborhood ($N(x)$):** Radius $r=2$ for the weak coupling interactions, and $r=1$ for the strong coupling interactions.
* **Transition Function:**
  Let $C(x) = \mathbb{I}(S_t(x) \ge 4)$ be the coupling type (0: weak, 1: strong).
  Let $E_x = C(x-1) + C(x) + C(x+1)$ be the local coupling environment.
  
  - **If $E_x \le 1$ (Weak Coupling Regime):**
    The field modes interact weakly and propagate as linear waves using the larger neighborhood ($r=2$):
    Let $u(y) = S_t(y) \pmod 4$.
    $$S_{t+1}(x) = (u(x-2) + u(x-1) + u(x+1) + u(x+2)) \pmod 4$$
  
  - **If $E_x \ge 2$ (Strong Coupling Regime):**
    Under S-duality ($g \leftrightarrow 1/g$), the strongly coupled field maps to a dual weakly coupled theory of solitons. The update becomes a localized ($r=1$), highly non-linear mapping:
    Let $v(y) = S_t(y) - 4$ if $S_t(y) \ge 4$ else $S_t(y)$.
    $$S_{t+1}(x) = 4 + \left[ (v(x))^2 + v(x-1) \cdot v(x+1) \right] \pmod 4$$
* **Mathematical Rationale:**
  S-duality is a fundamental symmetry in string theory (and some quantum field theories) that relates a theory at strong coupling $g$ to a dual theory at weak coupling $1/g$. Under S-duality, elementary particles that are light and weakly interacting become heavy and strongly interacting, while heavy, non-perturbative topological solitons (monopoles) become light, weakly interacting fundamental particles. This CA implements S-duality by dynamically toggling between a linear wave propagation rule ($r=2$) and a non-linear quadratic mapping ($r=1$) based on the local coupling density $E_x$.
* **Expected Visual Behavior:**
  Distinct spatial domains representing the two phases. In weak-coupling domains (states 0-3), we see smooth, overlapping wave interference patterns. In strong-coupling domains (states 4-7), the dynamics collapse into highly localized, sharp soliton-like particles that move and collide elastically, demonstrating the particle-soliton duality.

---

### Rule 7: Holographic Boundary-to-Bulk Projection (AdS/CFT)
* **States ($N$):** $10$ states ($0, 1, \dots, 9$).
  We partition the 1D lattice into:
  - Boundary cells: Cells at even indices ($x \equiv 0 \pmod 2$), representing the Conformal Field Theory (CFT) boundary.
  - Bulk cells: Cells at odd indices ($x \equiv 1 \pmod 2$), representing the Anti-de Sitter (AdS) gravity bulk.
* **Neighborhood ($N(x)$):** Radius $r=1$ for boundary cells, and $r=2$ for bulk cells.
* **Transition Function:**
  The transition function depends on the spatial index of the cell $x$:
  
  - **If $x$ is a Boundary Cell ($x \equiv 0 \pmod 2$):**
    The boundary evolves autonomously as a short-range, non-linear chaotic system (CFT dynamics), ignoring the bulk:
    $$S_{t+1}(x) = \left[ 3 \cdot S_t(x) + S_t(x-2) \cdot S_t(x+2) \right] \pmod{10}$$
    *(Note: $x-2$ and $x+2$ are the adjacent boundary cells)*.
  
  - **If $x$ is a Bulk Cell ($x \equiv 1 \pmod 2$):**
    The bulk state represents gravitational field modes that are holographically projected from the boundary, while propagating through the bulk:
    $$S_{t+1}(x) = \left[ S_t(x-1) + S_t(x+1) + S_t(x-2) + S_t(x+2) \right] \pmod{10}$$
    *(Note: $x-1$ and $x+1$ are the adjacent boundary cells; $x-2$ and $x+2$ are the adjacent bulk cells)*.
* **Mathematical Rationale:**
  The AdS/CFT correspondence (holographic principle) states that a quantum gravity theory in a bulk ($d+1$)-dimensional AdS space is exactly dual to a conformal field theory (CFT) living on the $d$-dimensional boundary. This CA models this holographic relation: the boundary cells (even indices) evolve independently under chaotic CFT dynamics, while the bulk cells (odd indices) represent the bulk space whose states are driven by the boundary configurations (holographic projection) combined with local bulk diffusion.
* **Expected Visual Behavior:**
  An alternating, grid-like pattern. The boundary cells display rapid, high-entropy chaotic patterns, while the bulk cells display smoother, low-frequency wave envelopes that lag behind the boundary, illustrating how the chaotic boundary "holographically projects" structured information into the bulk.

---

### Rule 8: Conformal Worldsheet Loop Dynamics
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Quantum foam (inactive spacetime).
  * State $1$: Clockwise moving loop boundary.
  * State $2$: Counter-clockwise moving loop boundary.
  * State $3$: String segment (stable connection).
  * State $4$: Junction (vertex of three strings).
  * State $5$: Singularity (collapsed loop).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  - **If $S_t(x) = 0$ (Quantum Foam):**
    - Loop boundaries can expand into vacuum:
      If $S_t(x-1) = 1$ and $S_t(x+1) = 2$ (loop boundaries colliding), they merge to form a junction: $S_{t+1}(x) = 4$.
      Else, if $S_t(x-1) = 1$: $S_{t+1}(x) = 1$.
      Else, if $S_t(x+1) = 2$: $S_{t+1}(x) = 2$.
      Otherwise, remains $0$.
  - **If $S_t(x) = 1$ (Clockwise Boundary):**
    - If it meets a counter-clockwise boundary ($S_t(x+1) = 2$), they annihilate and leave a connection: $S_{t+1}(x) = 3$.
    - Otherwise, it continues moving right: $S_{t+1}(x) = S_t(x-1)$.
  - **If $S_t(x) = 2$ (Counter-Clockwise Boundary):**
    - If it meets a clockwise boundary ($S_t(x-1) = 1$), they annihilate: $S_{t+1}(x) = 3$.
    - Otherwise, it continues moving left: $S_{t+1}(x) = S_t(x+1)$.
  - **If $S_t(x) = 3$ (String Segment):**
    - If flanked by two junctions, it collapses:
      If $S_t(x-1) = 4$ and $S_t(x+1) = 4$, then $S_{t+1}(x) = 5$.
      Otherwise, remains stable: $S_{t+1}(x) = 3$.
  - **If $S_t(x) = 4$ (Junction):**
    - It decays by emitting loop boundaries in both directions:
      $$S_{t+1}(x) = 0 \text{ and } S_{t+1}(x-1) = 2, S_{t+1}(x+1) = 1$$
  - **If $S_t(x) = 5$ (Singularity):**
    - It evaporates into quantum foam:
      $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:**
  A string tracing out a worldsheet in spacetime has local conformal symmetry. This CA models the discrete equivalent of loops: they expand, collide, form vertices/junctions, and occasionally pinch off to form singularities that evaporate. The dynamics are local and symmetric, reflecting the topological nature of loop interactions.
* **Expected Visual Behavior:**
  Expanding and contracting diamond structures representing the space-time trace of interacting string loops. Junctions (state 4) and singularities (state 5) appear as point-like vertices where loops split, merge, or evaporate.

---

### Rule 9: D-Brane Collision and Open String Creation
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Bulk spacetime.
  * State $1$: D-brane A (right-moving wall).
  * State $2$: D-brane B (left-moving wall).
  * State $3$: Open string endpoint (attached to a brane).
  * State $4$: Open string body.
  * State $5$: Collision plasma (high energy).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  - **If $S_t(x) = 1$ (D-brane A):**
    - If it collides with B: If $S_t(x+1) = 2$, then $S_{t+1}(x) = 5$.
    - Otherwise, it propagates right:
      $$S_{t+1}(x) = \begin{cases} 1 & \text{if } S_t(x-1) = 1 \text{ or } S_t(x-1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  - **If $S_t(x) = 2$ (D-brane B):**
    - If it collides with A: If $S_t(x-1) = 1$, then $S_{t+1}(x) = 5$.
    - Otherwise, it propagates left:
      $$S_{t+1}(x) = \begin{cases} 2 & \text{if } S_t(x+1) = 2 \text{ or } S_t(x+1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  - **If $S_t(x) = 5$ (Collision Plasma):**
    - It decays, causing the D-branes to bounce and creating a stretching open string between them:
      $$S_{t+1}(x) = 4, \quad S_{t+1}(x-1) = 3, \quad S_{t+1}(x+1) = 3$$
  - **If $S_t(x) = 3$ (Open String Endpoint):**
    - It must stay attached to a D-brane:
      - If adjacent to D-brane A ($S_t(x+1) = 1$) or D-brane B ($S_t(x-1) = 2$), it moves with it.
      - If D-brane A has moved to the right (so $S_t(x-1) = 4$ and $S_t(x+1) = 1$): $S_{t+1}(x) = 4$, and the endpoint moves to $x+1$.
      - If D-brane B has moved to the left: $S_{t+1}(x) = 4$, and the endpoint moves to $x-1$.
      - Otherwise, if the D-brane is gone, the endpoint decays: $S_{t+1}(x) = 0$.
  - **If $S_t(x) = 4$ (Open String Body):**
    - It stretches to fill the space between endpoints:
      If $S_t(x-1) \in \{3, 4\}$ and $S_t(x+1) \in \{3, 4\}$, it remains: $S_{t+1}(x) = 4$.
      Otherwise, it decays: $S_{t+1}(x) = 0$.
* **Mathematical Rationale:**
  D-branes are dynamical objects in string theory where open strings can end. When two D-branes collide, they do not simply pass through each other; they interact strongly, creating a high-energy density that decays by stretching open strings between the separating branes. This CA models the kinematics of D-brane walls in a discrete spacetime, demonstrating the topological necessity of open string creation when branes intersect and separate.
* **Expected Visual Behavior:**
  Two solid diagonal lines (representing D-branes) moving toward each other. Upon collision, they create a bright state-5 vertex, which then splits into two diverging branes with a growing shaded region (state 4) bound by endpoints (state 3) stretching between them.

---

### Rule 10: Fuzzball Horizon Information Scrambler
* **States ($N$):** $8$ states ($0, 1, 2, 3, 4, 5, 6, 7$).
  * State $0$: Flat vacuum (outside the horizon).
  * States $1, 2, 3$: Infalling particle flavors.
  * States $4, 5, 6$: Horizon microstates (fuzzball stringy states).
  * State $7$: Singularity core (inner boundary).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  - **If $S_t(x) = 0$ (Vacuum):**
    - Particles propagate rightward toward the horizon:
      If $S_t(x-1) \in \{1, 2, 3\}$, then $S_{t+1}(x) = S_t(x-1)$.
      Otherwise, remains $0$.
  - **If $S_t(x) \in \{1, 2, 3\}$ (Infalling Particle):**
    - If the cell to the right is a horizon state ($S_t(x+1) \in \{4, 5, 6\}$), the particle is absorbed and scrambles the horizon state:
      $$S_{t+1}(x) = 4 + \left[ S_t(x) + S_t(x+1) \right] \pmod 3$$
    - Otherwise, it continues moving right: $S_{t+1}(x) = S_t(x-1)$ (or $0$ if empty behind).
  - **If $S_t(x) \in \{4, 5, 6\}$ (Horizon State):**
    - The horizon states perform highly chaotic stringy microstate permutations to simulate information scrambling:
      Let $h_x = S_t(x) - 4 \in \{0, 1, 2\}$.
      Let $h_L = S_t(x-1) - 4$ if $S_t(x-1) \ge 4$ else $S_t(x-1) \pmod 3$.
      Let $h_R = S_t(x+1) - 4$ if $S_t(x+1) \ge 4$ else $S_t(x+1) \pmod 3$.
      
      We compute the scrambled next state:
      $$h_{new} = \left( h_x + h_L \cdot h_R + 1 \right) \pmod 3$$
      The cell remains a horizon state: $S_{t+1}(x) = 4 + h_{new}$.
      
      - Hawking Radiation: Occasionally, a horizon cell on the outer boundary (where $S_t(x-1) = 0$) evaporates and emits a scrambled particle back into the vacuum:
        If $S_t(x-1) = 0$ and $h_{new} = 0$, the cell evaporates: $S_{t+1}(x) = 0$ and emits a particle to the left: $S_{t+1}(x-1) = 1$.
  - **If $S_t(x) = 7$ (Singularity Core):**
    - It remains stable:
      $$S_{t+1}(x) = 7$$
* **Mathematical Rationale:**
  In string theory, the "fuzzball" proposal replaces the classical black hole singularity and horizon with a hot, dense ball of interacting fundamental strings. Information falling into a fuzzball is not lost at a singularity; instead, it is absorbed by the stringy microstates and scrambled across the horizon surface, eventually being re-radiated via Hawking radiation. This CA models this by having particle states (1-3) fall into a horizon region (4-6), where their information is scrambled using a non-linear chaotic mapping. The horizon boundary slowly emits particles back into the vacuum, representing unitary black hole evaporation.
* **Expected Visual Behavior:**
  Particles moving from left to right. When they hit the horizon (a thick block of states 4-6), they are absorbed. The horizon region displays a highly active, chaotic flickering texture (information scrambling). Occasionally, particles are ejected from the left edge of the horizon and propagate back to the left (Hawking radiation).
