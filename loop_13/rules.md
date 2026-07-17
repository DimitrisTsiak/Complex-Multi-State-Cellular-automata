# Loop 13 Cellular Automata Rules: Loop Quantum Gravity

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Loop Quantum Gravity (LQG)**. 

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The rules translate core quantum gravitational concepts—such as spin networks, quantized area and volume, the Hamiltonian constraint, and spinfoam amplitudes—into discrete dynamical updates, generating complex space-time structures at the discrete Planck scale.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Physical Expectation |
|---|---|---|---|---|---|
| **1** | [Quantum Area Spin Network](#rule-1-quantum-area-spin-network) | 8 | Radius $r=1$ (excl. self) | Clebsch-Gordan spin coupling under triangle inequalities | Smooth diagonal spin network domains |
| **2** | [Ashtekar Connection Holonomy Flow](#rule-2-ashtekar-connection-holonomy-flow) | 13 | Radius $r=1$ | Modular non-abelian connection curvature dynamics | High-entropy turbulent gauge field noise |
| **3** | [Loop Quantum Cosmology Bounce](#rule-3-loop-quantum-cosmology-bounce) | 12 | Radius $r=1$ | Quantum gravity pressure-induced singularity avoidance | Periodic local expansion and contraction cycles |
| **4** | [Spinfoam Amplitude Sum-Over-Histories](#rule-4-spinfoam-amplitude-sum-over-histories) | 6 | Radius $r=1$ | Parity-gated path integral constructive interference | Branching, fractal-like active spin histories |
| **5** | [Semi-Classical Weave State Relaxation](#rule-5-semi-classical-weave-state-relaxation) | 8 | Radius $r=1$ | Geometry smoothing coupled to sub-Planckian noise | Homogeneous domains bordered by quantum fluctuations |
| **6** | [Hamiltonian Constraint Vertex Excitation](#rule-6-hamiltonian-constraint-vertex-excitation) | 5 | Radius $r=1$ | Wheeler-DeWitt vertex creation, decay, and propagation | Glider-like traveling particle excitations |
| **7** | [Kodama State Phase Instability](#rule-7-kodama-state-phase-instability) | 12 | Radius $r=1$ | Chern-Simons coupling gradient amplification | Uniform phase sweep broken by chaotic wave fronts |
| **8** | [Causal Dynamical Triangulations](#rule-8-causal-dynamical-triangulations) | 8 | Radius $r=1$ | Manifold boundary interpolation with coordinate branching | Fractal, self-similar dimension branching trees |
| **9** | [Black Hole Horizon Pixelation](#rule-9-black-hole-horizon-pixelation) | 8 | Radius $r=1$ (excl. self) | Bekenstein-Hawking spin flux absorption and emission | Clustered matter zones alongside decay regions |
| **10** | [Chiral Immirzi Asymmetry](#rule-10-chiral-immirzi-asymmetry) | 5 | Radius $r=1$ | Parity-violating drift of left/right configurations | Tilted wave patterns exhibiting directional bias |

---

## Rule Definitions

### Rule 1: Quantum Area Spin Network
* **States ($N$):** $8$ states ($0, 1, \dots, 7$). State $s$ represents the quantized spin $j = s/2 \in \{0, 1/2, 1, 3/2, 2, 5/2, 3, 7/2\}$.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $S_{min} = |S_t(x-1) - S_t(x+1)|$ and $S_{max} = \min(7, S_t(x-1) + S_t(x+1))$ represent the Clebsch-Gordan spin coupling bounds.
  Let the target state be:
  $$S_{target} = \left[ S_t(x-1) + S_t(x+1) - S_t(x) \right] \pmod 8$$
  The transition is defined by:
  * If $S_t(x-1) = S_t(x+1) = 0$ (isolated vacuum state):
    $$S_{t+1}(x) = [S_t(x) + 1] \pmod 8$$
  * Otherwise, project $S_{target}$ into the valid interval $[S_{min}, S_{max}]$:
    $$S_{t+1}(x) = \max\left(S_{min}, \min\left(S_{max}, S_{target}\right)\right)$$
* **Mathematical Rationale:**
  In Loop Quantum Gravity, space is represented by spin networks—graphs whose edges are labeled by $SU(2)$ representations (spins $j$). When two edges meet at a vertex, the spins must satisfy the triangle inequality (Clebsch-Gordan recoupling conditions). This rule models the dynamic evolution of spins under these coupling constraints. The target state propagates the phase difference, while the projection ensures the local spin configuration remains a valid, coupled $SU(2)$ state.
* **Expected Visual Behavior:**
  A network of crystalline structures. The triangle inequalities constrain the gradient of states, creating smooth diagonal lines and bounded color domains representing coherent spin network configurations.

---

### Rule 2: Ashtekar Connection Holonomy Flow
* **States ($N$):** $13$ states ($0, 1, \dots, 12$). Choosing a prime number of states ensures algebraic field properties ($\mathbb{F}_{13}$) and prevents division/modulo degeneracies.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  $$S_{t+1}(x) = \left[ S_t(x) + (S_t(x+1) - S_t(x-1))^2 + S_t(x-1) \cdot S_t(x+1) \right] \pmod{13}$$
* **Mathematical Rationale:**
  Ashtekar variables formulate gravity as a gauge theory where the connection $A_a^i$ and conjugate triad $E_i^a$ are the fundamental fields. The curvature $F = dA + A \wedge A$ represents the magnetic field of the connection. In this rule, the squared difference term $(S_t(x+1) - S_t(x-1))^2$ models the spatial derivative squared (related to the discrete curvature contribution), and the product term $S_t(x-1) \cdot S_t(x+1)$ models the non-abelian self-interaction ($A \wedge A$).
* **Expected Visual Behavior:**
  Chaotic and highly dynamic textures with high-entropy mixing. Small perturbations expand rapidly at the speed of light (1 cell per step), producing complex, turbulent patterns reflecting non-abelian gauge field dynamics.

---

### Rule 3: Loop Quantum Cosmology Bounce
* **States ($N$):** $12$ states ($0, 1, \dots, 11$). State $0$ represents the physical singularity (zero volume/density limit).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  * If $S_t(x) = 0$ (singularity boundary):
    $$S_{t+1}(x) = \max(S_t(x-1), S_t(x+1), 3)$$
  * If $S_t(x) > 0$:
    $$S_{t+1}(x) = \max\left(0, \lfloor \frac{S_t(x-1) + S_t(x+1)}{2} \rfloor - 1\right)$$
* **Mathematical Rationale:**
  In Loop Quantum Cosmology (LQC), quantum geometry effects create a repulsive force at Planck densities, replacing the classical Big Bang singularity with a Big Bounce. This CA models local volumes contracting under gravitational attraction (decaying state values) until they hit $S_t(x) = 0$. At this singularity limit, quantum gravity pressure triggers a bounce to a minimum volume ($\ge 3$), driving localized re-inflation.
* **Expected Visual Behavior:**
  Rhythmic, periodic oscillations. Regions contract to zero, producing dark spots that immediately explode into bright, expanding cones of high-state values, showing a visual representation of local cyclic cosmology.

---

### Rule 4: Spinfoam Amplitude Sum-Over-Histories
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let the local parity condition $P(x)$ be defined as:
  $$P(x) = (S_t(x-1) + S_t(x) + S_t(x+1)) \pmod 2$$
  * If $P(x) = 0$ (admissible configuration / constructive interference):
    $$S_{t+1}(x) = [ S_t(x-1) + S_t(x+1) ] \pmod 6$$
  * If $P(x) = 1$ (inadmissible configuration / destructive interference):
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:**
  Spinfoams define the path integral formulation of LQG. The transition amplitudes are given by the sum-over-histories of spin networks, weighted by vertex amplitudes (such as the 10j symbol). The amplitude is non-zero (constructive interference) only when certain parity conditions on the spins are met. This rule mimics this quantum interference: when the local spin sum is even (even parity), the amplitudes interfere constructively and propagate; when it is odd, the amplitude vanishes, resetting the cell to the vacuum state ($0$).
* **Expected Visual Behavior:**
  Fractal-like branching structures interspersed with large black regions of suppressed states. The dynamics exhibit self-organizing criticality, creating complex geometric networks that propagate only along parity-coherent paths.

---

### Rule 5: Semi-Classical Weave State Relaxation
* **States ($N$):** $8$ states ($0, 1, \dots, 7$), representing local area quanta.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $D(x) = |S_t(x-1) - S_t(x)| + |S_t(x+1) - S_t(x)|$ represent the local spatial gradient (discrete curvature).
  * If $D(x) \ge 3$ (highly curved / rough geometry):
    $$S_{t+1}(x) = \lfloor \frac{S_t(x-1) + S_t(x) + S_t(x+1)}{3} \rfloor$$
  * If $D(x) < 3$ (smooth / flat geometry):
    $$S_{t+1}(x) = \left[ S_t(x) + S_t(x-1) - S_t(x+1) + 1 \right] \pmod 8$$
* **Mathematical Rationale:**
  Weave states are semi-classical states that approximate smooth geometry at macroscopic scales while remaining highly discrete at the Planck scale. This rule models a relaxation process: if the local geometry is rough, it dampens via diffusion to simulate minimization of curvature. However, if the geometry becomes too smooth, quantum gravity fluctuations are triggered to prevent it from collapsing to a classical continuum, maintaining the discrete quantum foam structure.
* **Expected Visual Behavior:**
  Interlocking patches of smooth, uniform colors (the semi-classical weave) bordered by active, high-frequency boundaries of quantum noise, creating a visual balance between classicality and quantum chaos.

---

### Rule 6: Hamiltonian Constraint Vertex Excitation
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unexcited vacuum state.
  * States $1, 2, 3$: Excitation levels of the spin network nodes.
  * State $4$: Virtual unstable state.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  * If $S_t(x) = 0$ (vacuum):
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } S_t(x-1) + S_t(x+1) \in \{2, 4\} \\ 0 & \text{otherwise} \end{cases}$$
  * If $S_t(x) \in \{1, 2, 3\}$ (active excitation):
    * If $S_t(x-1) \ge 1$ and $S_t(x+1) \ge 1$:
      $$S_{t+1}(x) = S_t(x) - 1 \quad \text{(local annihilation/decay)}$$
    * If $S_t(x-1) = 0$ and $S_t(x+1) = 0$:
      $$S_{t+1}(x) = (S_t(x) + 1) \pmod 4 \quad \text{(quantum fluctuation)}$$
    * Otherwise (one neighbor excited, one vacuum):
      $$S_{t+1}(x) = \max(S_t(x-1), S_t(x+1)) \quad \text{(propagation)}$$
  * If $S_t(x) = 4$ (unstable virtual excitation):
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:**
  In loop quantum gravity, physical states must satisfy the Hamiltonian constraint $H\Psi = 0$. The Hamiltonian operator acts locally on the vertices of spin networks, creating new edges, changing spins, or annihilating existing links. This rule models these operations: vacuum cells get excited if their neighbors supply sufficient energy; existing excitations propagate if asymmetrical, but annihilate each other if they collide.
* **Expected Visual Behavior:**
  Complex particle-like behaviors (gliders) traveling through the vacuum, occasionally colliding to annihilate each other or form new stable configurations, resembling a discrete quantum field theory on a spin network.

---

### Rule 7: Kodama State Phase Instability
* **States ($N$):** $12$ states ($0, 1, \dots, 11$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let the local modular phase difference be:
  $$\Delta(x) = (S_t(x+1) - S_t(x-1)) \pmod{12}$$
  * If $\Delta(x) = 0$ (perfect phase alignment):
    $$S_{t+1}(x) = (S_t(x) + 1) \pmod{12}$$
  * If $\Delta(x) \neq 0$ (phase gradient present):
    $$S_{t+1}(x) = \left[ S_t(x) + 3 \cdot \Delta(x) + S_t(x)^2 \right] \pmod{12}$$
* **Mathematical Rationale:**
  The Kodama state is a wavefunction that solves all quantum gravity constraints with a positive cosmological constant. It is defined as $\Psi_{Kodama}(A) \sim e^{i \frac{3}{\hbar \Lambda} Y_{CS}(A)}$, where $Y_{CS}$ is the Chern-Simons action of the Ashtekar connection. While exact, the Kodama state is physically unstable under small perturbations, leading to unbounded fluctuations. This rule models this behavior: if neighbors are in phase, the cell undergoes stable, uniform rotation; a tiny phase difference $\Delta(x) \neq 0$ triggers the non-linear Chern-Simons term, causing the system to explode into local chaos.
* **Expected Visual Behavior:**
  Uniform, sweeping color bands (stable Kodama sectors) that are suddenly disrupted by jagged, highly chaotic waves originating from any local defect or mismatch.

---

### Rule 8: Causal Dynamical Triangulations
* **States ($N$):** $8$ states ($0, 1, \dots, 7$), representing coordination numbers or local geometry indices.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  * If $|S_t(x-1) - S_t(x+1)| > 3$ (geometric tear):
    $$S_{t+1}(x) = \lfloor \frac{S_t(x-1) + S_t(x+1)}{2} \rfloor$$
  * Otherwise (manifold continuity maintained):
    $$S_{t+1}(x) = \left[ S_t(x) + (S_t(x-1) \pmod 2) - (S_t(x+1) \pmod 2) + 8 \right] \pmod 8$$
* **Mathematical Rationale:**
  Causal Dynamical Triangulations (CDT) is a path integral approach where quantum geometry is assembled from simplicial pieces under strict causality constraints. At macroscopic scales, the triangulation behaves like a smooth manifold, but at Planck scales, it is a fractal branching structure of spatial slices. This rule enforces this structure: if neighbor states differ too much, a "geometric tear" is threatened, forcing the cell to interpolate (smoothing constraint). If the region is stable, the cell undergoes coordinate branching (parity-driven fluctuations).
* **Expected Visual Behavior:**
  Fractal, self-similar tree structures that bifurcate and merge. The smoothing condition creates cohesive boundaries, while the branching condition generates intricate, high-frequency patterns.

---

### Rule 9: Black Hole Horizon Pixelation
* **States ($N$):** $8$ states ($0, 1, \dots, 7$). State $s$ represents the spin $j = s/2$ of an individual horizon pixel.
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $S_{flux} = S_t(x-1) + S_t(x+1)$ be the neighboring energy flux.
  * If $S_{flux} \ge 8$ (matter absorption):
    $$S_{t+1}(x) = \min(7, S_t(x) + 1)$$
  * If $S_{flux} < 4$ (Hawking radiation emission):
    $$S_{t+1}(x) = \max(0, S_t(x) - 1)$$
  * If $4 \le S_{flux} < 8$ (thermal equilibrium):
    $$S_{t+1}(x) = \begin{cases} (S_t(x) + 1) \pmod 8 & \text{if } S_t(x) \text{ is even} \\ S_t(x) - 1 & \text{otherwise} \end{cases}$$
* **Mathematical Rationale:**
  In LQG, a black hole horizon is modeled as a surface punctured by spin network edges. The area of the horizon is quantized, and the entropy is proportional to the number of microstates. This rule models the thermodynamic evolution of the horizon: high external flux increases the local spin (absorbing matter and growing the black hole's area), low external flux causes the spins to decay (Hawking radiation), and moderate flux maintains thermal equilibrium with local phase oscillations.
* **Expected Visual Behavior:**
  Coalescing domains of high spins representing absorbed matter clumps, bordered by oscillating, pixelated zones of equilibrium and decaying regions of radiation.

---

### Rule 10: Chiral Immirzi Asymmetry
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Symmetric/achiral geometry.
  * States $1, 2$: Left-handed chiral excitations (weak, strong).
  * States $3, 4$: Right-handed chiral excitations (weak, strong).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $L = S_t(x-1)$ and $R = S_t(x+1)$.
  * If $S_t(x) \in \{1, 3\}$ (weak chiral states):
    $$S_{t+1}(x) = \begin{cases} R & \text{if } R > L \\ L & \text{otherwise} \end{cases}$$
  * If $S_t(x) \in \{2, 4\}$ (strong chiral states):
    $$S_{t+1}(x) = \left[ S_t(x) + L - 2 \cdot R + 5 \right] \pmod 5$$
  * If $S_t(x) = 0$ (neutral):
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } L > R \text{ and } L > 0 \\
    3 & \text{if } R > L \text{ and } R > 0 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:**
  The Barbero-Immirzi parameter $\gamma$ is a scaling factor in LQG that sets the area quantum. When gravity couples to fermions, the Immirzi parameter induces a parity-violating chiral interaction. This CA models the spatial dynamics of this chiral asymmetry: weak states are swept by neighbor dominance, while strong states act as active sources, projecting their chirality with a directional bias (left vs right parity drift).
* **Expected Visual Behavior:**
  Asymmetric, tilted wavefronts drifting across the grid. The parity-violating coupling creates a strong directional bias, where one chirality dominates and pushes against the other, resulting in tilted stripes and domain boundaries.
