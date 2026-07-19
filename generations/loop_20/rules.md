# Loop 20 Cellular Automata Rules: Non-Euclidean Wormholes & Spatial Folding

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Non-Euclidean Wormholes & Spatial Folding**.

These rules model spatial topologies, non-local shortcuts, coordinate folding, and multidimensional projections, such as dynamic portal teleportation, Klein bottle mirror folding, hypercube projections, Dijkstra shortest-path routing, extremum-coupled heat wormholes, Möbius boundary twists, variable metric gravitational lensing, chaotic portal percolation, 2D projected toroidal solitons, and quantum entanglement bridges. Each rule operates on a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates unique visual signatures reflecting their topological and geometrical motivations.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Topological Expectation |
|---|---|---|---|---|---|
| **1** | [Portal Pair Teleportation](#rule-1-portal-pair-teleportation) | 6 | Radius $r=1$ + Diametric link | Collision-based portal creation and non-local packet routing | V-shaped particle tracks crossing via central teleportation junctions |
| **2** | [Klein Bottle Spatial Folding](#rule-2-klein-bottle-spatial-folding) | 5 | Radius $r=1$ + Mirror link | Mirror-reflected coordinate teleportation with parity inversion | Waves reflecting off boundaries and emerging from the opposite side reversed |
| **3** | [Dynamic Hypercube Projection](#rule-3-dynamic-hypercube-projection) | 8 | Radius $r=1$ + XOR link | Hypercubic coordinate mapping with global-state rotation | Globally synchronized phase bands and chaotic fractal regions |
| **4** | [Metric Wormhole Routing](#rule-4-metric-wormhole-routing) | 6 | Radius $r=1$ + Non-local link | Dijkstra-like shortest path routing via metric wormholes | Particles skipping intermediate space only when it optimizes their path |
| **5** | [Non-Euclidean Thermal Wormhole](#rule-5-non-euclidean-thermal-wormhole) | 12 | Radius $r=1$ + Extremum coupling | Dynamic link between absolute maximum and minimum lattice states | Instantaneous energy transfer flattening peaks and bridging distant domains |
| **6** | [Möbius Boundary Twist](#rule-6-mobi-us-boundary-twist) | 6 | Radius $r=1$ with Möbius twist | Periodic boundary wrapping with state-shifting and parity twist | Checkerboard-like diagonal bands that alternate phase/color on wrapping |
| **7** | [Variable Metric Gravitational Lensing](#rule-7-variable-metric-gravitational-lensing) | 8 | Variable Radius | State-dependent neighborhood step size simulating spatial warping | Curved wave tracks that decelerate and lens near heavy mass cores |
| **8** | [Chaotic Portal Percolation](#rule-8-chaotic-portal-percolation) | 16 | Radius $r=1$ + Chaotic links | Intermittent portal opening based on a discretized Logistic map | Dense local patterns disrupted by sudden, non-local chaotic bursts |
| **9** | [2D Projected Toroidal Solitons](#rule-9-2d-projected-toroidal-solitons) | 8 | Sparse 2D (5-cell) projection | Projecting a 2D toroidal lattice update onto a 1D coordinate system | Parallel diagonal waves and periodic repeating patterns in 1D spacetime |
| **10** | [Quantum Entanglement Bridges](#rule-10-quantum-entanglement-bridges) | 4 | Radius $r=1$ + Mirror entanglement | Instantaneous state collapse of mirror-symmetric entangled cell pairs | Mirror-symmetric lines that vanish or flip state simultaneously |

---

## Rule Definitions

### Rule 1: Portal Pair Teleportation
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Quantum Vacuum ($|0\rangle$).
  * State $1$: Right-moving packet ($\psi_R$).
  * State $2$: Left-moving packet ($\psi_L$).
  * State $3$: Portal Mouth A ($P_A$).
  * State $4$: Portal Mouth B ($P_B$).
  * State $5$: Energized portal core / Transit ($T$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, and a non-local diametric partner coordinate $x^* = (x + W/2) \bmod W$, where $W$ is the lattice width:
  $$N_{local}(x) = \{x-1, x, x+1\}, \quad N_{nonlocal}(x) = \{x^*\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, and let $x^* = (x + W/2) \bmod W$.
  * **Portal Creation:**
    If $s = 0$, and a right-moving packet (1) and left-moving packet (2) collide ($S_t(x-1) = 1$ and $S_t(x+1) = 2$):
    - If $x < W/2$, then $S_{t+1}(x) = 3$ (Mouth A) and its partner $S_{t+1}(x^*) = 4$ (Mouth B).
  * **Portal Transition:**
    - If $s = 3$ (Mouth A):
      - If $S_t(x-1) = 1$ or $S_t(x+1) = 2$, it absorbs the particle and becomes $5$ (Energized).
      - Otherwise, it remains $3$.
    - If $s = 4$ (Mouth B):
      - If $S_t(x-1) = 1$ or $S_t(x+1) = 2$, it absorbs the particle and becomes $5$ (Energized).
      - Otherwise, it remains $4$.
    - If $s = 5$, it decays back to vacuum: $S_{t+1}(x) = 0$.
  * **Particle Propagation & Teleportation:**
    - If $s = 0$ (and no collision occurs):
      - **Teleported Emergence:**
        - If $S_t(x^*-1) = 1$ and $S_t(x^*) = 3$ (packet entered Mouth A at $x^*$, emerging from Mouth B at $x$): $S_{t+1}(x) = 1$.
        - If $S_t(x^*+1) = 2$ and $S_t(x^*) = 3$ (packet entered Mouth A at $x^*$, emerging from Mouth B at $x$): $S_{t+1}(x) = 2$.
        - If $S_t(x^*-1) = 1$ and $S_t(x^*) = 4$ (packet entered Mouth B at $x^*$, emerging from Mouth A at $x$): $S_{t+1}(x) = 1$.
        - If $S_t(x^*+1) = 2$ and $S_t(x^*) = 4$ (packet entered Mouth B at $x^*$, emerging from Mouth A at $x$): $S_{t+1}(x) = 2$.
      - **Local Propagation:**
        - If the cell is not receiving a teleported particle:
          - If $S_t(x-1) = 1$ and $S_t(x) \notin \{3, 4, 5\}$, then $S_{t+1}(x) = 1$.
          - If $S_t(x+1) = 2$ and $S_t(x) \notin \{3, 4, 5\}$, then $S_{t+1}(x) = 2$.
          - Otherwise, $S_{t+1}(x) = 0$.
* **Mathematical Rationale:**
  This rule models the Einstein-Rosen bridge where high local energy density (particle collisions) pinches spacetime to create a wormhole entrance ($P_A$) and exit ($P_B$) separated by a spatial distance of $W/2$. The packets carry momentum and, upon entering one throat, traverse the interior (energizing it) and emerge from the other mouth preserving their propagation direction.
* **Expected Visual Behavior:**
  Clean diagonal tracks corresponding to moving packets. When two packets collide, they spawn a pair of static horizontal portal lines. Subsequent packets striking these lines disappear and instantly reappear at the conjugate side of the lattice, creating symmetrical offset tracks.

---

### Rule 2: Klein Bottle Spatial Folding
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Spacetime vacuum.
  * State $1$: Right-moving particle ($P_R$).
  * State $2$: Left-moving particle ($P_L$).
  * State $3$: Fold Zone Core ($F_C$).
  * State $4$: Excited Fold Boundary ($F_B$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, and a mirror partner coordinate $x' = W - 1 - x$:
  $$N(x) = \{x-1, x, x+1, x'\}$$
* **Transition Function:**
  Let $s = S_t(x)$ and $x' = W - 1 - x$.
  - Fold zones are fixed regions: $S_t(x) = 3$ if $x \in \{0, 1, W-2, W-1\}$. They remain $3$ indefinitely.
  - If $s = 0$ (Vacuum):
    - **Teleportation through Fold:**
      - If $S_t(x'+1) = 1$ and $S_t(x') = 3$ (a right-mover entered the mirror fold): $S_{t+1}(x) = 2$ (emerges moving left).
      - If $S_t(x'-1) = 2$ and $S_t(x') = 3$ (a left-mover entered the mirror fold): $S_{t+1}(x) = 1$ (emerges moving right).
    - **Normal Propagation:**
      - If $S_t(x-1) = 1$ (and $S_t(x) \neq 3$): $S_{t+1}(x) = 1$.
      - If $S_t(x+1) = 2$ (and $S_t(x) \neq 3$): $S_{t+1}(x) = 2$.
      - Otherwise, $S_{t+1}(x) = 0$.
  - If $s = 1$ or $2$ (Particles):
    - If the next cell in its direction is a fold zone (e.g., $S_t(x+1) = 3$ for a right-mover), it vanishes: $S_{t+1}(x) = 0$.
    - Otherwise, normal propagation rules apply.
* **Mathematical Rationale:**
  A Klein bottle is a non-orientable surface where traversing a boundary inverts the coordinates and the chirality of the object. We discretize this by placing fold zones at the spatial boundaries. When a particle strikes the right boundary, it does not wrap around to $0$ as in a standard torus; instead, it teleports to the left side and has its direction of motion reversed ($1 \leftrightarrow 2$).
* **Expected Visual Behavior:**
  Waves propagating diagonally that, upon hitting the boundary, instantly emerge on the same or mirror side with flipped slope (direction), resulting in highly symmetric checkerboard reflection motifs.

---

### Rule 3: Dynamic Hypercube Projection
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, and a dynamically shifted coordinate $x_{hyper} = (x \oplus \theta_t) \bmod W$:
  $$N(x) = \{x-1, x, x+1, x_{hyper}\}$$
* **Transition Function:**
  Let $\theta_t$ be the global lattice orientation angle computed at each time step $t$:
  $$\theta_t = \left( \sum_{y=0}^{W-1} S_t(y) \right) \bmod 8$$
  For cell $x$, let $x_{hyper} = (x \oplus \theta_t) \bmod W$. The state updates as:
  $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x+1) + S_t(x) \cdot S_t(x_{hyper}) + 1 \right) \bmod 8$$
* **Mathematical Rationale:**
  This rule treats the 1D lattice as a projection of a higher-dimensional hypercube. The projection angle $\theta_t$ is dynamically coupled to the total integrated state of the lattice, rotating the hypercube. The bitwise XOR operation ($\oplus$) models the hypercubic coordinate routing, introducing a dynamic, non-local connection that shifts based on global feedback.
* **Expected Visual Behavior:**
  A mixture of local fractal growth and global synchronization. Sudden phase shifts (horizontal lines across the image) occur when $\theta_t$ changes value, reorganizing the spatial connections and leading to beautiful, complex interference lattices.

---

### Rule 4: Metric Wormhole Routing
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Spacetime vacuum.
  * State $1$: Right-seeking packet ($K_R$, heading to beacon).
  * State $2$: Left-seeking packet ($K_L$, heading away).
  * State $3$: Portal Entrance ($P_E$).
  * State $4$: Portal Exit ($P_X$).
  * State $5$: Gravitational Beacon ($B$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, with a fixed non-local link between $P_E$ and $P_X$.
* **Transition Function:**
  Let $x_E$ be the portal entrance at $W/4$, $x_X$ be the portal exit at $2W/3$, and $x_B$ be the beacon at $3W/4$.
  - Cells $x_E$, $x_X$, and $x_B$ have fixed states: $S_t(x_E) = 3$, $S_t(x_X) = 4$, and $S_t(x_B) = 5$ for all $t$.
  - For any other cell $x$:
    - If $s = 0$:
      - A right-seeking packet (1) arrives:
        - Via normal step: if $S_t(x-1) = 1$ and $x-1 \neq x_E$.
        - Via teleportation: if $S_t(x_E-1) = 1$ (the packet entered the portal entrance $x_E$ from the left) AND $x = x_X + 1$ (the packet emerges at the exit).
        - If either is true, $S_{t+1}(x) = 1$.
      - A left-seeking packet (2) arrives:
        - Via normal step: if $S_t(x+1) = 2$ and $x+1 \neq x_X$ (packets do not travel backward through the exit).
        - If true, $S_{t+1}(x) = 2$.
    - If $s \in \{1, 2\}$, it becomes $0$ in the next step (packets move forward).
* **Mathematical Rationale:**
  This rule models optimal routing on a metric space with non-trivial topology. The packets move according to the shortest path distance. Because the portal shortcut $x_E \to x_X$ offers a geodesic path that is shorter than the Euclidean walk (since $1 + |x_X - x_B| < |x_E - x_B|$), the right-moving packets route themselves through the wormhole.
* **Expected Visual Behavior:**
  Diagional tracks representing the packets. As packets reach $x_E$, they vanish, leaving a gap in the spacetime diagram, and instantly reappear at $x_X$, continuing their journey to the right. Packets moving left bypass the wormhole as it would route them backwards, demonstrating directional metric routing.

---

### Rule 5: Non-Euclidean Thermal Wormhole
* **States ($N$):** $12$ states ($0, 1, \dots, 11$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, plus a dynamic wormhole link between the absolute maximum and minimum state cells:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  At each step $t$, compute:
  $$x_{max} = \min \{ x \mid S_t(x) = \max_y S_t(y) \}$$
  $$x_{min} = \max \{ x \mid S_t(x) = \min_y S_t(y) \}$$
  For any cell $x$:
  - If $x \notin \{x_{max}, x_{min}\}$:
    $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x) + S_t(x+1) \right) \bmod 12$$
  - If $x = x_{max}$:
    $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x_{min}) + S_t(x+1) \right) \bmod 12$$
  - If $x = x_{min}$:
    $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x_{max}) + S_t(x+1) \right) \bmod 12$$
* **Mathematical Rationale:**
  This models a thermal feedback loop on a dynamically folding manifold. The two thermodynamic extremes of the lattice (highest and lowest energy states) puncture spacetime to form a wormhole. This allows instantaneous heat conduction between them, preventing thermal runaway and creating a self-regulating, non-local energy balancer.
* **Expected Visual Behavior:**
  Intricate, woven patterns with long-range correlations. Because the maximum and minimum states are continuously bridged, the image features sudden vertical strands and "jump" lines where high-energy nodes instantly neutralize or transfer their energy to cold regions.

---

### Rule 6: Möbius Boundary Twist
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including self, with a state-shifting boundary twist:
  $$N(x) = \{S_t(x-1), S_t(x), S_t(x+1)\}$$
  where boundary conditions are defined as:
  $$S_t(-1) = \left( S_t(W-1) + 3 \right) \bmod 6$$
  $$S_t(W) = \left( S_t(0) + 3 \right) \bmod 6$$
* **Transition Function:**
  $$S_{t+1}(x) = \left( S_t(x-1) \cdot S_t(x) + S_t(x) \cdot S_t(x+1) + 1 \right) \bmod 6$$
  where $S_t(-1)$ and $S_t(W)$ utilize the Möbius twist formulas above.
* **Mathematical Rationale:**
  This models a 1D lattice mapped onto the edge of a Möbius strip. When a spatial wave wraps around the boundary, it does not meet itself in phase; instead, its state value is shifted by $+3 \pmod 6$ (a half-rotation in the state space). This topology forces the system to undergo two full spatial traversals before returning to its original state.
* **Expected Visual Behavior:**
  Diagonal propagation lines that change color/phase upon crossing the left or right edges of the image. The pattern repeats with a phase shift, creating alternating light and dark bands and chevron-like geometric symmetries.

---

### Rule 7: Variable Metric Gravitational Lensing
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State $0$: Flat vacuum.
  * State $1, 2, 3$: Low, medium, high gravitational potential ($P$).
  * State $4$: Gravitational Singularity (static massive core).
  * State $5$: Right-propagating wavefront ($\gamma_R$).
  * State $6$: Left-propagating wavefront ($\gamma_L$).
  * State $7$: Gravitational radiation.
* **Neighborhood ($N(x)$):** Variable step size depending on local gravitational potential:
  $$d_L(x) = 1 + \left( S_t(x) \bmod 4 \right)$$
  $$d_R(x) = 1 + \left( S_t((x+1)\bmod W) \bmod 4 \right)$$
  $$N(x) = \{x - d_L(x), x, x + d_R(x)\}$$
* **Transition Function:**
  Let $x_L = (x - d_L(x)) \bmod W$ and $x_R = (x + d_R(x)) \bmod W$.
  - If $S_t(x) = 4$ (Singularity), it remains $4$.
  - Otherwise:
    $$S_{t+1}(x) = \left( S_t(x_L) + 2 \cdot S_t(x) + 3 \cdot S_t(x_R) \right) \bmod 8$$
* **Mathematical Rationale:**
  This rule implements Einsteinian general relativity on a discrete lattice by varying the local metric. The step size (distance) to the neighbors is a function of the local gravitational potential. High potential (near a singularity) contracts the coordinate steps, while flat vacuum has a step size of 1. This variable step size acts as gravitational lensing, refracting the paths of propagating waves.
* **Expected Visual Behavior:**
  Wavefronts moving through space that curve and bend as they approach the stationary singularity core (state 4). The path bends inward and speed alters, creating visual lensing envelopes and focusing lines around the core.

---

### Rule 8: Chaotic Portal Percolation
* **States ($N$):** $16$ states ($0, 1, \dots, 15$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, and a chaotic non-local partner $x^* = (x + S_t(x) \cdot 31) \bmod W$:
  $$N(x) = \{x-1, x, x+1, x^*\}$$
* **Transition Function:**
  - If $S_t(x) \ge 12$:
    $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x^*) + S_t(x+1) + 1 \right) \bmod 16$$
  - If $S_t(x) < 12$:
    $$S_{t+1}(x) = \left( S_t(x-1) + S_t(x) + S_t(x+1) \right) \bmod 16$$
* **Mathematical Rationale:**
  This models a dynamical system where portals open and close based on local state values. High states ($\ge 12$) act as unstable portal generators, linking the cell to a distant cell whose offset is proportional to the current state. This implements a form of topological percolation where the lattice connectivity network fluctuates dynamically.
* **Expected Visual Behavior:**
  A highly textured, chaotic background. When states spike above the threshold, non-local links are established, causing sudden "teleportation bursts" that appear as horizontal lines or localized explosions of state transfer across the grid.

---

### Rule 9: 2D Projected Toroidal Solitons
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
* **Neighborhood ($N(x)$):** Sparse non-local neighborhood projecting a 2D torus of size $L_1 \times L_2$ (where $W = L_1 \cdot L_2$, e.g., $40 \times 20$ for $W=800$):
  $$N(x) = \{x-1, x, x+1, (x - L_1) \bmod W, (x + L_1) \bmod W\}$$
* **Transition Function:**
  Let $L = S_t(x-1)$, $R = S_t(x+1)$, $U = S_t((x-40)\bmod W)$, and $D = S_t((x+40)\bmod W)$.
  $$S_{t+1}(x) = \left( (L + R + U + D + S_t(x)) \cdot 3 + 1 \right) \bmod 8$$
* **Mathematical Rationale:**
  We fold a higher-dimensional (2D) toroidal space onto a 1D line by mapping the coordinate $(u, v)$ to $x = u + v \cdot L_1$. The local 2D neighborhood (up, down, left, right) maps to non-local offsets of $\pm 1$ and $\pm L_1$ in 1D. This projectively simulates a 2D CA using a 1D formulation, demonstrating spatial folding and multidimensional projection.
* **Expected Visual Behavior:**
  Beautiful repeating diagonal wavefronts that align with the projection modulo ($40$). The 1D space-time diagram displays regular, periodic stripes and interference lattices that correspond to 2D waves crossing the boundaries of the projected torus.

---

### Rule 10: Quantum Entanglement Bridges
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Ground state.
  * State $1$: Entangled spin-up ($|\uparrow\rangle$).
  * State $2$: Entangled spin-down ($|\downarrow\rangle$).
  * State $3$: Disruption wavefront ($D$).
* **Neighborhood ($N(x)$):** Radius $r=1$ locally, and a mirror partner $x^* = W - 1 - x$:
  $$N(x) = \{x-1, x, x+1, x^*\}$$
* **Transition Function:**
  Let $x^* = W - 1 - x$.
  - **Entanglement Formation:**
    If $S_t(x) = 0$, and both neighbors are entangled ($S_t(x-1) \in \{1, 2\}$ and $S_t(x+1) \in \{1, 2\}$):
    $$S_{t+1}(x) = 1$$
  - **Disruption Wave Propagation:**
    - If $S_t(x) = 3$, it decays: $S_{t+1}(x) = 0$.
    - If $S_t(x) \neq 3$ and ($S_t(x-1) = 3$ or $S_t(x+1) = 3$): $S_{t+1}(x) = 3$.
  - **Entangled State Collapse:**
    - If $S_t(x) \in \{1, 2\}$ and it is hit by a disruption wave ($S_t(x-1) = 3$ or $S_t(x+1) = 3$):
      - Cell $x$ collapses: $S_{t+1}(x) = 0$.
    - If $S_t(x) \in \{1, 2\}$, and its partner $x^*$ was hit by a disruption wave at time $t$ (so $S_t(x^*-1) = 3$ or $S_t(x^*+1) = 3$):
      - If $S_t(x) = 1$ (spin up), it collapses to spin down: $S_{t+1}(x) = 2$.
      - If $S_t(x) = 2$ (spin down), it collapses to vacuum: $S_{t+1}(x) = 0$.
    - Otherwise, remains same: $S_{t+1}(x) = S_t(x)$.
* **Mathematical Rationale:**
  This rule models instantaneous, non-local quantum state collapse. Pairs of cells at $x$ and $W - 1 - x$ share an entangled state. When a classical disruption wave (State 3) measures/disturbs one cell, its state collapses, causing an instantaneous, non-local collapse and spin-flip at its entangled partner cell on the opposite side of the lattice, bypassing speed-of-light limits.
* **Expected Visual Behavior:**
  Highly symmetric, mirror-imaged patterns. The disruption waves (diagonal lines of state 3) propagate outward. When they hit entangled zones, the opposite side of the image reflects the collapse instantly, producing perfectly synchronized state changes across the vertical axis.
