# Loop 15 Cellular Automata Rules: Extraterrestrial Life

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Extraterrestrial Life**. 

These rules model hypothetical alien metabolic pathways, strange biochemistries (silicon-based, cryogenic, magnetotactic, radiosynthetic), space-faring constructor swarms, and quantum-coherent sub-Kelvin organisms. Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates unique visual signatures reflecting their alien biological motivations.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Biological Expectation |
|---|---|---|---|---|---|
| **1** | [Silicon Crystalline Replication](#rule-1-silicon-crystalline-replication) | 5 | Radius $r=1$ | Silicon crystal growth driven by silane carrier diffusion | Expanding crystalline facets with stable quartz cores |
| **2** | [Methanogenic Titan Chemoton](#rule-2-methanogenic-titan-chemoton) | 5 | Radius $r=1$ | Membrane assembly, nutrient absorption, and decay in liquid methane | Cellular membrane walls separating core and waste |
| **3** | [Jovian Magnetotactic Plasma Filaments](#rule-3-jovian-magnetotactic-plasma-filaments) | 6 | Radius $r=1$ | Counter-propagating plasma currents creating magnetic pinches | Directional current gliders and localized pinch nodes |
| **4** | [Radiotrophic Panspermia Spores](#rule-4-radiotrophic-panspermia-spores) | 5 | Radius $r=1$ (excl. self) | Spore germination via radiation-catalyzed soil minerals | Expanding wavefronts leaving dormant spores behind |
| **5** | [Superfluid Vortex Organisms](#rule-5-superfluid-vortex-organisms) | 5 | Radius $r=1$ | Annihilation and dipole binding of quantized superfluid vortices | Moving vortex dipoles and localized annihilation pulses |
| **6** | [Dysonian Astro-engineering Swarms](#rule-6-dysonian-astro-engineering-swarms) | 6 | Radius $r=1$ | Solar sail spores and constructor drones building mirror arrays | Unidirectional drift, asteroid consumption, and collector growth |
| **7** | [Subterranean Metallophilic Xenolith](#rule-7-subterranean-metallophilic-xenolith) | 5 | Radius $r=1$ | Mycelial growth along metal veins triggered by electrical pulses | Dendritic patterns with periodic electrical discharges |
| **8** | [Hypercyclic Xenovirus](#rule-8-hypercyclic-xenovirus) | 5 | Radius $r=1$ | Three-strain cyclic parasitism and host cell lysis | Dynamic rotating wavefronts and cyclic oscillations |
| **9** | [Quantum-Coherent Extremophile](#rule-9-quantum-coherent-extremophile) | 5 | Radius $r=1$ | Energy transport via entanglement swapping and decoherence | Highly synchronized, checkerboard-like quantum state domains |
| **10** | [Radiosynthetic Cherenkov Shield](#rule-10-radiosynthetic-cherenkov-shield) | 6 | Radius $r=2$ | Cherenkov energy harvesting and biomineralized lead shielding | Tiered shielding enclosures protecting core spores |

---

## Rule Definitions

### Rule 1: Silicon Crystalline Replication
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Amorphous Silica ($SiO_2$, inert background matrix).
  * State $1$: Growth Front (Active crystallization tip).
  * State $2$: Quartz Lattice (Stable crystal structure).
  * State $3$: Metamict Quartz (Degraded/damaged crystal).
  * State $4$: Silane Transporter (Diffusible silicon carrier).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } s = 2 \text{ and } (S_t(x-1) = 3 \lor S_t(x+1) = 3) \\
  2 & \text{if } s = 2 \text{ and not above} \\
  3 & \text{if } s = 3 \\
  2 & \text{if } s = 1 \\
  0 & \text{if } s = 4 \\
  1 & \text{if } s = 0 \text{ and } \left( (S_t(x-1) = 1 \land S_t(x+1) = 4) \lor (S_t(x-1) = 4 \land S_t(x+1) = 1) \right) \\
  4 & \text{if } s = 0 \text{ and } (S_t(x-1) = 4 \lor S_t(x+1) = 4) \text{ and not the condition for state } 1 \\
  0 & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** This models silicon-based life in a high-temperature crust. The growth front (1) advances by consuming the diffusing silane carrier (4) and transforming silica (0) into quartz lattice (2). Over time, radiation causes stable quartz (2) to degrade to metamict (3) if it is adjacent to metamict cells, modeling a crystalline infection/decay process.
* **Expected Visual Behavior:** Growing solid triangles of state 2 bordered by thin growth tips (state 1). The cores of these crystals gradually transform into state 3 from the center outwards, showing a weathered rock texture.

---

### Rule 2: Methanogenic Titan Chemoton
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Liquid Methane Solvent (Inert background).
  * State $1$: Acetylene Nutrient (Soluble hydrocarbons).
  * State $2$: Polymeric Membrane (Protective lipid-like barrier).
  * State $3$: Metabolic Core (Catalytic active site).
  * State $4$: Carbon Soot Waste (Insoluble polymer).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $N_k(x) = \sum_{y \in \{x-1, x, x+1\}} \mathbb{I}(S_t(y) = k)$ be the number of cells in neighborhood $N(x)$ at state $k$.
  - If $S_t(x) = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_2(x) \ge 1 \text{ and } N_1(x) \ge 1 \\
    1 & \text{else if } N_1(x) \ge 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 1$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } N_2(x) \ge 1 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_3(x) \ge 2 \\
    2 & \text{else if } N_3(x) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 3$:
    $$S_{t+1}(x) = 2$$
  - If $S_t(x) = 4$:
    $$S_{t+1}(x) = 4$$
* **Mathematical Rationale:** Models the Ganti Chemoton template adapted to liquid methane at $90\text{ K}$. It couples membrane formation (2) with metabolic activity (3). The membrane grows when in contact with acetylene nutrient (1). Over-accumulation of metabolic cores causes the membrane to degrade into insoluble carbon soot (4), representing the metabolic waste limits of cryogenic life.
* **Expected Visual Behavior:** Cell-like compartments of state 3 enclosed by thin boundaries of state 2, which gradually leave behind static lines of state 4 (carbon soot) as the system evolves.

---

### Rule 3: Jovian Magnetotactic Plasma Filaments
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Ambient Plasma (Ground state/vacuum).
  * State $1$: Ionized Channel (Excited conducting path).
  * State $2$: Positive Current Filament ($I^+$, right-moving).
  * State $3$: Negative Current Filament ($I^-$, left-moving).
  * State $4$: Magnetic Pinch Node (High-energy collision site).
  * State $5$: Discharged Plasma (Refractory state).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 2 \text{ and } S_t(x+1) = 3 \\
    2 & \text{else if } S_t(x-1) = 2 \\
    3 & \text{else if } S_t(x+1) = 3 \\
    1 & \text{else if } S_t(x-1) = 4 \lor S_t(x+1) = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 2 \\
    3 & \text{else if } S_t(x+1) = 3 \\
    5 & \text{otherwise}
    \end{cases}$$
  - If $s \in \{2, 3, 4\}$:
    $$S_{t+1}(x) = 5$$
  - If $s = 5$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** Models plasma-based organisms in gas giant atmospheres. The organisms consist of self-propagating currents. $I^+$ (state 2) conducts to the right, and $I^-$ (state 3) conducts to the left. A head-on collision creates a high-energy magnetic pinch (4), which ionizes neighboring regions (creating state 1) and enables new currents to flow, mimicking reproduction.
* **Expected Visual Behavior:** Clean diagonal lines of current propagating in opposite directions. The intersection points generate localized "explosions" (state 4) that branch out into new current pairs, creating self-sustaining networks of electrical loops.

---

### Rule 4: Radiotrophic Panspermia Spores
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Inert Regolith (Empty background matrix).
  * State $1$: Dormant Spore (Highly resistant state).
  * State $2$: Unweathered Minerals (Stable food resource).
  * State $3$: Radiated Minerals (Activated nutrient).
  * State $4$: Vegetative Hyphae (Active growing state).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $N_k(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = k)$ be the number of neighbors of cell $x$ in state $k$.
  - If $S_t(x) = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_4(x) \ge 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_3(x) \ge 1 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } N_4(x) \ge 1 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_4(x) \ge 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 4$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } N_2(x) + N_3(x) = 0 \\
    4 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models radiotrophic alien fungi spreading across airless planetary bodies. Spores (1) remain dormant until stellar cosmic rays activate adjacent unweathered minerals (2) into radiated minerals (3). Active hyphae (4) feed on this radiation and weather regolith into minerals, but revert to dormant spores (1) when resources are exhausted, preventing starvation.
* **Expected Visual Behavior:** Expanding, nested V-shaped structures. The outer edges are active hyphae (4) that convert the background into nutrients, while the interior collapses back into a stable trail of dormant spores (1).

---

### Rule 5: Superfluid Vortex Organisms
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Superfluid Ground State (Inert fluid).
  * State $1$: Clockwise Vortex ($v_+$).
  * State $2$: Counter-Clockwise Vortex ($v_-$).
  * State $3$: Bound Vortex Dipole (Metabolic cell core).
  * State $4$: Thermal Acoustic Phonon (Decaying signal).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 2 \\
    1 & \text{else if } S_t(x-1) = 4 \text{ and } S_t(x+1) = 4 \\
    4 & \text{else if } S_t(x-1) = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x-1) = 4 \lor S_t(x+1) = 4 \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** Models hypothetical sub-Kelvin life in liquid helium pools or neutron star crusts. Organisms are composed of quantized topological defects (vortices). Clockwise (1) and counter-clockwise (2) vortices drift; if they meet, they annihilate into thermal phonons (4). However, if aligned correctly, they bind into stable dipoles (3) that can survive and reproduce by capturing energy from passing thermal waves.
* **Expected Visual Behavior:** Highly dynamic particle-like tracks. States 1 and 2 move diagonally and annihilate upon contact, generating expanding rings of state 4. The stable state 3 acts as stationary blocks that light up when waves pass.

---

### Rule 6: Dysonian Astro-engineering Swarms
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Vacuum (Empty space).
  * State $1$: Pioneer Spore (Solar-sailing probe, right-moving).
  * State $2$: Asteroid Core (Silicate-metal substrate).
  * State $3$: Collector Mirror (Reflective dysonian element).
  * State $4$: Laser Beam (Energy delivery system, left-moving).
  * State $5$: Constructor Drone (Active builder node).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \\
    4 & \text{else if } S_t(x+1) = 4 \\
    4 & \text{else if } S_t(x+1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x+1) = 4 \\
    5 & \text{else if } S_t(x-1) = 5 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 3$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 5$:
    $$S_{t+1}(x) = 3$$
* **Mathematical Rationale:** Models space-dwelling post-biological swarms constructed to harvest stellar energy. Pioneer spores (1) sail rightward until they strike an asteroid (2), which spawns constructor drones (5) to digest the asteroid and build solar collectors (3). The collectors emit high-energy lasers (4) leftward. If a laser strikes another asteroid, it vaporizes it into a new wave of pioneer spores, creating a self-sustaining stellar-engineering feedback loop.
* **Expected Visual Behavior:** Beautiful asymmetrical drift. Moving particles of state 1 (spores) propagate to the right. When they hit asteroid blocks (state 2), they build permanent collector blocks (state 3) that shoot laser beams (state 4) to the left, seeding new waves.

---

### Rule 7: Subterranean Metallophilic Xenolith
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Basalt Rock (Inert crust).
  * State $1$: Iron Ore Vein (Nutrient).
  * State $2$: Lithotrophic Mycelium (Active consumer).
  * State $3$: Fossil Trail (Exhausted node).
  * State $4$: Charge Pulse (Electrical coordinator).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $N_k(x) = \sum_{y \in \{x-1, x, x+1\}} \mathbb{I}(S_t(y) = k)$ be the neighbor count.
  - If $S_t(x) = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } N_4(x) \ge 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_2(x) \ge 1 \lor N_4(x) \ge 1 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 4 \lor S_t(x+1) = 4 \\
    3 & \text{else if } N_1(x) = 0 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $S_t(x) = 3$:
    $$S_{t+1}(x) = 3$$
  - If $S_t(x) = 4$:
    $$S_{t+1}(x) = 2$$
* **Mathematical Rationale:** Models inorganic subterranean organisms that grow inside rocky planetary shells. They feed on iron ore veins (1). Electrical charge pulses (4) travel along the conductive mycelium (2) to coordinate nutrient intake. If two pulses collide, they generate localized lightning arcs that fracture basalt (0), exposing new iron veins (1) and allowing the organism to continue spreading.
* **Expected Visual Behavior:** Branching, root-like structures (state 2) that consume background streaks of state 1. Dynamic points of state 4 run up and down the structures, creating new vein networks upon collision.

---

### Rule 8: Hypercyclic Xenovirus
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Uninfected Host (Inert cellular matrix).
  * State $1$: Viral Strain A ($V_A$, catalyzed by B).
  * State $2$: Viral Strain B ($V_B$, catalyzed by C).
  * State $3$: Viral Strain C ($V_C$, catalyzed by A).
  * State $4$: Lytic Host Cell (Ruptured/decaying state).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } (S_t(x-1) = 1 \land S_t(x+1) = 2) \lor (S_t(x-1) = 2 \land S_t(x+1) = 1) \\
    1 & \text{else if } (S_t(x-1) = 2 \land S_t(x+1) = 3) \lor (S_t(x-1) = 3 \land S_t(x+1) = 2) \\
    2 & \text{else if } (S_t(x-1) = 3 \land S_t(x+1) = 1) \lor (S_t(x-1) = 1 \land S_t(x+1) = 3) \\
    1 & \text{else if } S_t(x-1) = 1 \lor S_t(x+1) = 1 \\
    2 & \text{else if } S_t(x-1) = 2 \lor S_t(x+1) = 2 \\
    3 & \text{else if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 2 \lor S_t(x+1) = 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 1 \lor S_t(x+1) = 1 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** Models an alien virus with a tripartite genetic structure that utilizes a hypercyclic parasitism loop. Each strain is stable on its own but is catalyzed into rapid, host-killing replication (state 4) when exposed to its catalytic companion (A is catalyzed by B, B by C, C by A). The host cell ruptures and clears back to state 0, allowing host tissue regrowth and further infection cycles.
* **Expected Visual Behavior:** Spiral-like or wave-like patterns with three distinct colored phases chasing each other. The interface between strains creates thin black bands of ruptured cells (state 4), preventing complete host wipeout.

---

### Rule 9: Quantum-Coherent Extremophile
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Ground Classical State (De-cohered environment).
  * State $1$: Coherent Superposition ($|\psi\rangle$).
  * State $2$: Entangled Connection ($|\Phi^+\rangle$).
  * State $3$: Thermal Noise Pump (Decohering generator).
  * State $4$: Intermediate Coherence Loader.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 2 \\
    1 & \text{else if } S_t(x-1) = 2 \text{ and } S_t(x+1) = 1 \\
    4 & \text{else if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    0 & \text{if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } (S_t(x-1) = 1 \land S_t(x+1) \neq 1) \lor (S_t(x+1) = 1 \land S_t(x-1) \neq 1) \\
    0 & \text{else if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 1$$
* **Mathematical Rationale:** Models cryogenic organisms that exploit quantum coherence for high-efficiency energy transmission. Quantum states (1 and 2) propagate across the lattice using entanglement swaps. However, contact with environmental thermal noise (3) collapses the wavefunction back to the ground classical state (0). The noise pump (3) also acts as an activation source, loading nearby cells (4) to initiate coherence.
* **Expected Visual Behavior:** Highly synchronized, geometric checkerboard-like patterns. Domains of coherence (state 1 and 2) are periodically fragmented and reset by thermal noise collapses, creating a breathing crystalline texture.

---

### Rule 10: Radiosynthetic Cherenkov Shield
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Exposed Regolith (Inert background).
  * State $1$: Cherenkov Photon Wave (Energy carrier, left-moving).
  * State $2$: Gamma Radiation Ray (Excitation carrier, right-moving).
  * State $3$: Active Radiotrophic Mycelium (Metabolic structure).
  * State $4$: Lead Biomineral Shield (Highly resistant wall).
  * State $5$: Reproductive Spore Core (Protected center).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    - Let $G = \mathbb{I}(S_t(x-1) = 2 \lor S_t(x-2) = 2)$ and $C = \mathbb{I}(S_t(x+1) = 1 \lor S_t(x+2) = 1)$.
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } G = 1 \text{ and } C = 1 \\
    2 & \text{else if } G = 1 \\
    1 & \text{else if } C = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s \in \{1, 2\}$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-1) = 4 \text{ and } S_t(x+1) = 4 \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 5$:
    $$S_{t+1}(x) = 5$$
* **Mathematical Rationale:** Models organisms that grow in extremely high radiation environments (e.g. close-in orbiting exoplanets or reactor walls). They harvest energy where incoming gamma rays (2) and self-emitted Cherenkov photons (1) intersect. Metabolic cells (3) build heavy-metal lead shields (4) to protect their reproductive spore cores (5), which only form in cells completely insulated from the external radiation field.
* **Expected Visual Behavior:** Robust, nested structures. Outer bands of moving radiation fields build static shield enclosures (state 4) that encapsulate stable green spores (state 5) in their center, resisting subsequent radiation waves.
