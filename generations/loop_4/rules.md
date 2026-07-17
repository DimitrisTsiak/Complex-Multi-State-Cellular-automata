# Loop 4 Cellular Automata Rules: Granular Flows, Sandpiles & Gravity

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Granular Flows, Sandpiles & Gravity**. 

Unlike the cyclic and generation-based systems of Loops 1 & 2, this domain models physical features of granular media, such as conservation of mass (particle counts), repose thresholds (slopes), frictional arrest (jamming), kinetic energy transfer, aeolian saltation, and gravity-induced size segregation.

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The rules are mathematically distinct from previous loops, introducing conservative formulations and partitioned (block-based) updates.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Classical 1D Abelian Sandpile](#rule-1-classical-1d-abelian-sandpile) | 4 | Radius $r=1$ | Height-threshold conservative diffusion | Avalanche triangles and SOC fractal structures |
| **2** | [Slope-Dependent Granular Slide](#rule-2-slope-dependent-granular-slide) | 5 | Radius $r=1$ | Asymmetric slope-triggered transport | Terraced slopes sliding downhill |
| **3** | [Reversible Odd-Even Segregation](#rule-3-reversible-odd-even-segregation) | 3 | Block Partition | Phase sorting under gravity | Density-sorted layered columns |
| **4** | [Granular Consolidation & Arching](#rule-4-granular-consolidation--arching) | 4 | Radius $r=1$ | Support-based sand compaction | Jammed sand columns resisting gravity flow |
| **5** | [Dynamic-Threshold Sandpile](#rule-5-dynamic-threshold-sandpile) | 6 | Radius $r=1$ | Neighbor-triggered avalanche threshold | Sudden catastrophic slope failures |
| **6** | [Wind-Blown Sand (Saltation & Creep)](#rule-6-wind-blown-sand-saltation--creep) | 3 | Radius $r=2$ | Multi-speed wind-driven transport | Aeolian sorting and ripple formation |
| **7** | [Frictional Arrest (Granular Jamming)](#rule-7-frictional-arrest-granular-jamming) | 3 | Radius $r=2$ | High-density flow jamming | Clogging waves propagating backwards |
| **8** | [Friction-Induced Dissipation](#rule-8-friction-induced-dissipation) | 4 | Radius $r=1$ | Porous substrate absorption | Rapid edge decay of sandpiles |
| **9** | [Momentum-Driven Snow Avalanche](#rule-9-momentum-driven-snow-avalanche) | 4 | Radius $r=2$ | Momentum-dependent barrier shearing | Dynamic snowpacks releasing runout zones |
| **10** | [Granular Percolation (Reverse Grading)](#rule-10-granular-percolation-reverse-grading) | 4 | Block Partition | Size segregation via kinetic sieving | Large grains rising to the top (left) |

---

## Rule Definitions

### Rule 1: Classical 1D Abelian Sandpile
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $\tau_t(x)$ be the indicator representing whether a cell is unstable and topples:
  $$\tau_t(x) = \mathbb{I}(S_t(x) \ge 2)$$
  The transition is defined by the mass conservation equation:
  $$S_{t+1}(x) = S_t(x) - 2\tau_t(x) + \tau_t(x-1) + \tau_t(x+1)$$
* **Mathematical Rationale:** This is the classic 1D Bak-Tang-Wiesenfeld sandpile model. A cell containing 2 or more grains is unstable and distributes 1 grain to each neighbor, losing 2 grains. The state space is closed: if $S_t(x) \le 1$, it receives at most 2 grains (ending at $\le 3$). If $S_t(x) \ge 2$, it loses 2 and receives at most 2 (ending at $S_t(x) \le 3$).
* **Expected Visual Behavior:** Avalanche propagation that generates stable triangular formations and fractal-like structures, exhibiting self-organized criticality (SOC).

---

### Rule 2: Slope-Dependent Granular Slide
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$), representing sand heights.
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Gravity pulls to the right ($+x$). Define the downhill mass outflow from cell $x$ to $x+1$ as:
  $$\phi(x \to x+1) = \mathbb{I}(S_t(x) - S_t(x+1) \ge 2)$$
  The transition function is:
  $$S_{t+1}(x) = S_t(x) - \phi(x \to x+1) + \phi(x-1 \to x)$$
* **Mathematical Rationale:** This rule models the angle of repose. Sand grains only slide downhill if the height difference (slope) is at least 2. Mass is strictly conserved across updates. The states are bounded because a cell at height 4 cannot receive mass (as the neighbor would need to be $\ge 6$), and a cell at height 0 cannot lose mass.
* **Expected Visual Behavior:** Sloping sand formations sliding downhill, leaving behind stable step-like terraces separated by active sliding fronts.

---

### Rule 3: Reversible Odd-Even Segregation
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Empty space (air).
  * State $1$: Light particles (fine sand).
  * State $2$: Heavy particles (coarse rock).
* **Neighborhood ($N(x)$):** A partitioned block neighborhood.
  At even steps $t$, cells are grouped into blocks $B_k = \{2k, 2k+1\}$.
  At odd steps $t$, cells are grouped into blocks $B_k = \{2k-1, 2k\}$.
* **Transition Function:**
  Let $\{L, R\}$ denote the left and right cells of a block. The block update is:
  $$(S_{t+1}(L), S_{t+1}(R)) = \begin{cases}
  (0, 1) & \text{if } (S_t(L), S_t(R)) = (1, 0) \\
  (0, 2) & \text{if } (S_t(L), S_t(R)) = (2, 0) \\
  (1, 2) & \text{if } (S_t(L), S_t(R)) = (2, 1) \\
  (S_t(L), S_t(R)) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** By partitioning updates, we guarantee 100% particle conservation and avoid collision conflicts. Gravity pulls particles rightward. Heavy particles (2) are denser and displace light particles (1) and empty space (0), while light particles displace empty space.
* **Expected Visual Behavior:** Rapid phase segregation where heavy rocks settle at the bottom (right), light sand forms a layer above them, and empty space rises to the top (left).

---

### Rule 4: Granular Consolidation & Arching
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty space.
  * State $1$: Loose sand (unstable).
  * State $2$: Compacted sand (stable).
  * State $3$: Solid rock barrier (immobile).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Gravity pulls to the right ($+x$).
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } S_t(x-1) = 1 \\
  0 & \text{if } S_t(x) = 1 \text{ and } S_t(x+1) = 0 \\
  2 & \text{if } S_t(x) = 1 \text{ and } S_t(x+1) \in \{2, 3\} \\
  1 & \text{if } S_t(x) = 2 \text{ and } S_t(x+1) = 0 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Loose sand (1) flows into empty spaces. Compacted sand (2) is supported and remains immobile. If loose sand hits a support (2 or 3) on its right, it compacts (1 $\to$ 2). If compacted sand loses support on its right, it becomes loose (2 $\to$ 1) and begins to flow. Sand count is conserved.
* **Expected Visual Behavior:** Columns of sand falling through voids and jamming when they hit barriers, forming solid arches or columns that resist gravity until their foundation is disturbed.

---

### Rule 5: Dynamic-Threshold Sandpile
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  A cell $x$ is sensitized by neighboring avalanches. Define the dynamic toppling indicator $\tau_t(x)$ as:
  $$\tau_t(x) = \begin{cases}
  1 & \text{if } S_t(x) \ge 4 \\
  1 & \text{if } S_t(x) = 3 \text{ and } (S_t(x-1) \ge 4 \text{ or } S_t(x+1) \ge 4) \\
  0 & \text{otherwise}
  \end{cases}$$
  The transition function is:
  $$S_{t+1}(x) = S_t(x) - 2\tau_t(x) + \tau_t(x-1) + \tau_t(x+1)$$
* **Mathematical Rationale:** Models vibrational triggering. A cell with height 3 is meta-stable. It does not topple under static conditions, but if a neighbor is actively toppling ($\ge 4$), the vibrational energy lowers the static friction threshold, forcing the cell to topple.
* **Expected Visual Behavior:** Catastrophic avalanche cascades that sweep across the lattice, destabilizing and flattening meta-stable sloped regions.

---

### Rule 6: Wind-Blown Sand (Saltation & Creep)
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Empty space.
  * State $1$: Light sand (saltates/jumps).
  * State $2$: Heavy sand (creeps/rolls).
* **Neighborhood ($N(x)$):** Radius $r=2$.
* **Transition Function:**
  Wind blows sand to the right ($+x$). Heavy sand creeps 1 cell. Light sand saltates 2 cells.
  $$S_{t+1}(x) = \begin{cases}
  2 & \text{if } S_t(x-1) = 2 \text{ and } S_t(x) = 0 \\
  1 & \text{if } S_t(x-2) = 1 \text{ and } S_t(x) = 0 \text{ and } S_t(x-1) \neq 2 \\
  0 & \text{if } S_t(x) = 2 \text{ and } S_t(x+1) = 0 \text{ and not } (S_t(x-2) = 1 \text{ and } S_t(x-1) \neq 2) \\
  0 & \text{if } S_t(x) = 1 \text{ and } S_t(x+2) = 0 \text{ and } S_t(x+1) \neq 2 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Models aerodynamic drag sorting. The transition guards prevent collisions (e.g. preventing a saltating grain and a creeping grain from occupying the same cell) and maintain exact particle conservation.
* **Expected Visual Behavior:** Aeolian sorting patterns where light sand rapidly migrates ahead, leaving behind slow-moving heavy sand ripples.

---

### Rule 7: Frictional Arrest (Granular Jamming)
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Empty space.
  * State $1$: Flowing sand (moving right).
  * State $2$: Jammed/Solid sand (immobile).
* **Neighborhood ($N(x)$):** Radius $r=2$ favoring the left:
  $$N(x) = \{x-2, x-1, x, x+1\}$$
* **Transition Function:**
  - Sand (1) flows right into empty space (0).
  - Two adjacent flowing particles (1) jam and freeze into state 2.
  - Jammed cells (2) melt back to flowing (1) if there is empty space to their right.
  $$S_{t+1}(x) = \begin{cases}
  2 & \text{if } S_t(x) = 1 \text{ and } (S_t(x-1) = 1 \text{ or } S_t(x+1) = 1) \\
  1 & \text{if } S_t(x) = 2 \text{ and } S_t(x+1) = 0 \\
  1 & \text{if } S_t(x) = 0 \text{ and } S_t(x-1) = 1 \text{ and } S_t(x-2) \neq 1 \\
  0 & \text{if } S_t(x) = 1 \text{ and } S_t(x+1) = 0 \text{ and } S_t(x-1) \neq 1 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Models silo and chute clogging. When particles flow too close together, frictional force bridges lock them. De-jamming propagates backwards from the free boundary.
* **Expected Visual Behavior:** Alternating phases of flow and arrest, visible as jamming waves that travel upstream (leftward) against the direction of physical flow.

---

### Rule 8: Friction-Induced Dissipation
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $\tau_t(x) = \mathbb{I}(S_t(x) \ge 2)$ be the toppling indicator. Define local flows:
  $$\phi(x \to x-1) = \tau_t(x) \cdot \mathbb{I}(S_t(x-1) \ge 1)$$
  $$\phi(x \to x+1) = \tau_t(x) \cdot \mathbb{I}(S_t(x+1) \ge 1)$$
  The transition function is:
  $$S_{t+1}(x) = S_t(x) - 2\tau_t(x) + \phi(x-1 \to x) + \phi(x+1 \to x)$$
* **Mathematical Rationale:** Models flow over a porous substrate. Empty space ($0$) represents deep pores that absorb sand grains permanently. A toppling cell only successfully transfers grains to neighbors that already contain sand ($\ge 1$).
* **Expected Visual Behavior:** Sandpiles that decay rapidly at their boundaries as grains fall into pores, while the saturated core of the sandpile continues to show standard diffusion.

---

### Rule 9: Momentum-Driven Snow Avalanche
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty space.
  * State $1$: Stable snowpack.
  * State $2$: Unstable snowpack.
  * State $3$: Active sliding avalanche.
* **Neighborhood ($N(x)$):** Radius $r=2$.
* **Transition Function:**
  Gravity flows to the right ($+x$). An active avalanche (3) shears through empty (0) or unstable (2) space, but requires momentum (two adjacent avalanche cells) to shear through stable snow (1).
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } S_t(x-1) = 3 \text{ and } S_t(x) \in \{0, 2\} \\
  3 & \text{if } S_t(x-1) = 3 \text{ and } S_t(x) = 1 \text{ and } S_t(x-2) = 3 \\
  0 & \text{if } S_t(x) = 3 \text{ and } S_t(x+1) \in \{0, 2\} \\
  0 & \text{if } S_t(x) = 3 \text{ and } S_t(x+1) = 1 \text{ and } S_t(x-1) = 3 \\
  1 & \text{if } S_t(x) = 3 \text{ and } \text{otherwise} \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Models snowpack mechanical failure. A single sliding cell stops when hitting stable snow. However, a thick, moving avalanche front has the kinetic energy to erode and trigger stable snow, turning it into sliding mass.
* **Expected Visual Behavior:** Dynamic flow fronts that expand in unstable zones, cut through stable barriers if they have enough momentum, and leave deposition scars (1) when they run out of energy.

---

### Rule 10: Granular Percolation (Reverse Grading)
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty space.
  * State $3$: Large particles (coarse).
  * State $2$: Medium particles.
  * State $1$: Small particles (fine).
* **Neighborhood ($N(x)$):** A partitioned block neighborhood.
  At even steps $t$, cells are grouped into blocks $B_k = \{2k, 2k+1\}$.
  At odd steps $t$, cells are grouped into blocks $B_k = \{2k-1, 2k\}$.
* **Transition Function:**
  Within each block $\{L, R\}$ (where $L$ is the left/top cell and $R$ is the right/bottom cell):
  $$(S_{t+1}(L), S_{t+1}(R)) = \begin{cases}
  (R, L) & \text{if } L \ge 1 \text{ and } R \ge 1 \text{ and } L < R \\
  (0, L) & \text{if } L \ge 1 \text{ and } R = 0 \\
  (S_t(L), S_t(R)) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Models kinetic sieving. When granular materials are sheared, small particles (1) fall through the gaps of larger particles (2 and 3) to the bottom (right), which forces the larger particles to rise to the top (left). Empty space (0) always rises.
* **Expected Visual Behavior:** Size segregation where a mixed state sorts itself into layered bands: coarse grains on top (left), medium in the middle, and fine grains at the bottom (right).
