# Loop 19 Cellular Automata Rules: Necromantic Alchemical Transmutation & Soul-Weaving

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Necromantic Alchemical Transmutation & Soul-Weaving**.

These rules model magical systems, including leyline mana conduit grids, soul-binding resonances, ectoplasmic rot cascades, catalytic transmutations (lead to gold), explosive arcane feedback backlashes, phylactery expansion fields, necromantic skeleton reanimations, blood magic altar discharges, Philosopher's Stone crystallization, and entropic Abyssal devouring. Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates unique visual signatures reflecting their magical and alchemical dynamics.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Physical Expectation |
|---|---|---|---|---|---|
| **1** | [Mana Conduit and Dissipation](#rule-1-mana-conduit-and-dissipation) | 5 | Radius $r=1$ | Propagation of mana currents from stable leyline sources | Branching lines of active conduits decaying if disconnected |
| **2** | [Soul Binding and Resonant Weaving](#rule-2-soul-binding-and-resonant-weaving) | 5 | Radius $r=2$ | Propagation and collision of soul threads forming stable resonant nodes | Converging diagonal lines forming stable horizontal binding links |
| **3** | [Ectoplasmic Decay and Necrotic Miasma](#rule-3-ectoplasmic-decay-and-necrotic-miasma) | 5 | Radius $r=1$ | Necrotic miasma infection of flesh yielding stable bones and dissipating slime | Creeping contagion waves leaving skeletal bone stripes |
| **4** | [Alchemical Transmutation and Quicksilver Catalyst](#rule-4-alchemical-transmutation-and-quicksilver-catalyst) | 6 | Radius $r=1$ | Catalytic conversion of base metals into gold, with salt-overload explosion | Expanding gold domains separated by dross inclusions |
| **5** | [Arcane Feedback and Leyline Overload](#rule-5-arcane-feedback-and-leyline-overload) | 5 | Radius $r=1$ | Runaway energy accumulation sparking a destructive shockwave | Expanding shockwave circles leaving behind drained black voids |
| **6** | [Phylactery Aura and Lich Soul-Siphoning](#rule-6-phylactery-aura-and-lich-soul-siphoning) | 6 | Radius $r=1$ | Lich harbingers harvesting wandering souls to expand phylactery field | Expanding aura domains sending inward-moving energy pulses |
| **7** | [Bone Harvest and Reanimation](#rule-7-bone-harvest-and-reanimation) | 5 | Radius $r=1$ | Skeletons marching, crumbling on impact, and reanimating via pulse | Crisscrossing skeletons forming bone dots, swept by pulse lines |
| **8** | [Blood Altar Sacrifice and Runic Discharge](#rule-8-blood-altar-sacrifice-and-runic-discharge) | 6 | Radius $r=1$ | Altars pumping blood conduits into runes that trigger clearing novas | Rhythmic expanding rings of blood novas resetting the system |
| **9** | [Philosopher's Seed Crystallization](#rule-9-philosophers-seed-crystallization) | 5 | Radius $r=1$ | Fractal crystal growth seeded by sulfur and blocked by lead | Growth triangles splitting at promoters and stalling at inhibitors |
| **10** | [Void Corruption and Abyssal Decay](#rule-10-void-corruption-and-abyssal-decay) | 5 | Radius $r=1$ | Erosion of matter by abyssal core, with mana triggering explosions | Inward-eating dark cores expanding into explosive voids |

---

## Rule Definitions

### Rule 1: Mana Conduit and Dissipation
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Uninfused Aether (ground state).
  * State $1$: Leyline Source (stable, infinite energy source).
  * State $2$: Charging Conduit (transient charging state).
  * State $3$: Resonating Conduit (fully active conductor).
  * State $4$: Mana Resistance (decayed/blocking zone).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } L \in \{1, 2, 3\} \lor R \in \{1, 2, 3\} \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } L \in \{1, 3\} \lor R \in \{1, 3\} \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } L \in \{1, 3\} \lor R \in \{1, 3\} \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical/Physical Rationale:** Models the conduction of mana from sources through a self-healing conduit grid. Active conduits (3) require a continuous connection to an active flow (1, 2, or 3) from their immediate neighbors. If isolated, they collapse into mana resistance (4) before dissipating back to the ground state.
* **Expected Visual Behavior:** Stable vertical pillars of Leyline Sources (1) emitting diagonal streaks of Charging Conduits (2) that rapidly solidify into Resonating Conduits (3). If two paths clash or lose support, they instantly trigger a state 4 decay event, creating complex, segmented tree-like structures.

---

### Rule 2: Soul Binding and Resonant Weaving
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Inert Aether (vacuum).
  * State $1$: Soul Anchor (stable, static generator).
  * State $2$: Soul Thread (propagating wavefront).
  * State $3$: Resonant Soul Knot (stable connection).
  * State $4$: Fading Tether (decaying trace).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, and let $L_2 = S_t(x-2)$, $L_1 = S_t(x-1)$, $R_1 = S_t(x+1)$, and $R_2 = S_t(x+2)$.
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } L_1 \in \{1, 2, 3\} \lor R_1 \in \{1, 2, 3\} \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 2$:
    - If $(L_1 \in \{1, 2, 3\} \lor L_2 \in \{1, 2, 3\}) \land (R_1 \in \{1, 2, 3\} \lor R_2 \in \{1, 2, 3\})$:
      $$S_{t+1}(x) = 3$$
    - Else if $L_1 \in \{1, 2\} \lor R_1 \in \{1, 2\}$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 4$$
  - If $s = 0$:
    - If $L_1 = 2 \land R_1 = 2$:
      $$S_{t+1}(x) = 3$$
    - Else if $L_1 = 1 \lor R_1 = 1$:
      $$S_{t+1}(x) = 2$$
    - Else if $L_1 = 2 \land L_2 \in \{1, 2\} \land R_1 = 0$:
      $$S_{t+1}(x) = 2$$
    - Else if $R_1 = 2 \land R_2 \in \{1, 2\} \land L_1 = 0$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the creation and binding of soul threads. When two soul anchors (1) are placed on the grid, they launch waves of soul threads (2) in both directions. If these threads meet in the middle (collision point), they crystallize into a stable, resonant soul knot (3) that keeps the connection open. If the connection is broken, it decays into fading tethers (4).
* **Expected Visual Behavior:** Growing diagonal V-shapes of soul threads (2) extending from anchors (1). Where they intersect, horizontal bars of state 3 are formed. If the source of a thread is disrupted, the diagonal line instantly snaps, leaving a fading trail of state 4.

---

### Rule 3: Ectoplasmic Decay and Necrotic Miasma
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Empty Graveyard (vacuum).
  * State $1$: Living Flesh (susceptible tissue).
  * State $2$: Necrotic Miasma (active contagion).
  * State $3$: Ectoplasmic Slime (liquefied residue).
  * State $4$: Calcified Bones (resistant skeletal structures).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } (L = 2 \land R = 3) \lor (R = 2 \land L = 3) \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } L = 2 \lor R = 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } L = 1 \land R = 1 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } L = 2 \lor R = 2 \\
    4 & \text{otherwise}
    \end{cases}$$
* **Mathematical/Physical Rationale:** Models the spreading dynamics of a magical flesh-eating plague (Necrotic Miasma). Living flesh (1) is converted to miasma (2) upon contact. When miasma eats through a dense block of flesh (where both left and right neighbors are still flesh), the high-density biological containment calcifies the miasma into bone structures (4). Otherwise, the miasma degrades to ectoplasmic slime (3) and dissolves.
* **Expected Visual Behavior:** Expanding wave-fronts of miasma (2) chewing through a solid background of flesh (1). At the centers of massive flesh blocks, stable bone stripes (4) are left behind, forming skeleton-like patterns that remain stable unless re-infected by another wavefront.

---

### Rule 4: Alchemical Transmutation and Quicksilver Catalyst
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Base Lead ($Pb$, ground state).
  * State $1$: Alchemical Salt (reaction accelerant).
  * State $2$: Quicksilver Catalyst (transmutation engine).
  * State $3$: Noble Gold ($Au$, stable final product).
  * State $4$: Volatile Embers (combustible intermediate).
  * State $5$: Useless Dross (burnt ash).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 3$ or $s = 5$:
    $$S_{t+1}(x) = s$$
  - If $s = 4$:
    $$S_{t+1}(x) = 5$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } L = 1 \land R = 1 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } L = 2 \lor R = 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    - If $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 2$$
    - Else if $L = 1 \lor R = 1$:
      $$S_{t+1}(x) = 1$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models alchemical transmutation of base metals. Quicksilver catalyst (2) converts adjacent Lead (0) into more catalyst. Alchemical salt (1) accelerates the reaction. When quicksilver (2) consumes lead adjacent to salt, it transmutes into gold (3). However, if quicksilver is flanked by salt on both sides, the reaction over-saturates, causing a miniature explosion into volatile embers (4) which burn out into inert dross (5).
* **Expected Visual Behavior:** Gold structures (3) grow outwards, surrounded by quicksilver reactions (2). Salt (1) lines propagate parallelly. Over-concentrations of salt trigger dark inclusions of dross (5) that act as insulators, blocking future transmutations and yielding complex stratified bands.

---

### Rule 5: Arcane Feedback and Leyline Overload
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Dead Aether (magic-dead zone, depleted).
  * State $1$: Ambient Mana (recharging/ground energy).
  * State $2$: Arcane Charge (accumulated spell energy).
  * State $3$: Feedback Spark (critical ignition state).
  * State $4$: Backlash Shockwave (exploding front).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 0$:
    $$S_{t+1}(x) = 1$$
  - If $s = 1$:
    - If $L = 4 \lor R = 4$:
      $$S_{t+1}(x) = 0$$
    - Else if $L = 3 \lor R = 3$:
      $$S_{t+1}(x) = 3$$
    - Else if $(L = 1 \land R = 1) \lor L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    - If $L = 4 \lor R = 4 \lor L = 3 \lor R = 3$:
      $$S_{t+1}(x) = 4$$
    - Else if $L = 2 \land R = 2$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 2$$
* **Mathematical/Physical Rationale:** Models the instability of high-level magic. Mana recharges (from 0 to 1) and accumulates into arcane charge (2). When two charge zones collide (both neighbors of a charged cell are charged), a feedback spark (3) is ignited. This spark explodes into a backlash shockwave (4) that expands, vaporizing all ambient mana and charge back into a dead aether state (0).
* **Expected Visual Behavior:** A cyclic-like generation pattern with expanding triangular cones representing shockwaves (4). Inside the cones is a black void of dead aether (0), which gradually heals back into charging zones (2), triggering further explosions and resulting in chaotic, fractal-like shockwave patterns.

---

### Rule 6: Phylactery Aura and Lich Soul-Siphoning
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Wild Forest (empty ground).
  * State $1$: Wandering Soul (static nutrient).
  * State $2$: Phylactery Core (static source at center).
  * State $3$: Necrotic Aura (sustained field).
  * State $4$: Lich Harbinger (boundary guardian).
  * State $5$: Siphoned Essence (returning energy pulse).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 2$:
    $$S_{t+1}(x) = 2$$
  - If $s = 3$:
    - If $L = 5 \lor R = 5$:
      $$S_{t+1}(x) = 5$$
    - Else:
      $$S_{t+1}(x) = 3$$
  - If $s = 5$:
    - If $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 3$$
  - If $s = 4$:
    - If $L = 1 \lor R = 1$:
      $$S_{t+1}(x) = 5$$
    - Else:
      $$S_{t+1}(x) = 3$$
  - If $s = 1$:
    - If $L = 4 \lor R = 4$:
      $$S_{t+1}(x) = 5$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 0$:
    - If $L = 3 \land R = 1$:
      $$S_{t+1}(x) = 4$$
    - Else if $R = 3 \land L = 1$:
      $$S_{t+1}(x) = 4$$
    - Else if $L = 3 \land R = 0$:
      $$S_{t+1}(x) = 4$$
    - Else if $R = 3 \land L = 0$:
      $$S_{t+1}(x) = 4$$
    - Else if $L = 5 \land R = 3$:
      $$S_{t+1}(x) = 5$$
    - Else if $R = 5 \land L = 3$:
      $$S_{t+1}(x) = 5$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the life support loop of a Lich. The Lich Harbinger (4) patrols the boundary of the Necrotic Aura (3). If the Lich encounters a Wandering Soul (1), it consumes it, creating a pulse of Siphoned Essence (5) that travels backward through the aura to the core (2). When it reaches the core, the essence converts into stable aura (3), permanently expanding the phylactery's domain.
* **Expected Visual Behavior:** Slowly expanding colored blocks of Necrotic Aura (3) centered on the Phylactery (2). The borders are traced by Lich Harbingers (4). When the border intersects a soul (1), a bright diagonal line of Siphoned Essence (5) races back to the center of the aura, leaving a wider, stable domain.

---

### Rule 7: Bone Harvest and Reanimation
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Dark Soil (ground state).
  * State $1$: Dead Bones (stationary resource).
  * State $2$: Right-Marching Skeleton.
  * State $3$: Left-Marching Skeleton.
  * State $4$: Necromantic Pulse (fast-moving wave).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 1$:
    - If $L = 4$:
      $$S_{t+1}(x) = 2$$
    - Else if $R = 4$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    - If $R \in \{3, 1, 4\}$:
      $$S_{t+1}(x) = 1$$
    - Else:
      $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    - If $L \in \{2, 1, 4\}$:
      $$S_{t+1}(x) = 1$$
    - Else:
      $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    - If $L = 4 \lor R = 4$:
      $$S_{t+1}(x) = 4$$
    - Else if $L = 2 \land R = 3$:
      $$S_{t+1}(x) = 1$$
    - Else if $L = 2$:
      $$S_{t+1}(x) = 2$$
    - Else if $R = 3$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the reanimation cycle of skeletal armies. Skeletons (2 and 3) march across the battlefield. When they collide with each other, with pulses, or with existing piles of bones (1), they crumble to the ground as inactive bones (1). When a necromantic pulse (4) sweeps across, it reanimates any inactive bones, sending them marching in the direction of the pulse.
* **Expected Visual Behavior:** Grid-like diagonal intersections of right- and left-marching skeletons. The intersections leave stationary dots of state 1. When a fast-moving pulse (4) passes through, these dots are instantly converted back into diagonal marching lines, forming complex, self-perpetuating interference webs.

---

### Rule 8: Blood Altar Sacrifice and Runic Discharge
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Stone Floor (inert).
  * State $1$: Sacrificial Altar (pulse generator).
  * State $2$: Flowing Blood (conduit, propagates).
  * State $3$: Runic Circle (absorbing receiver).
  * State $4$: Saturated Rune (fully charged).
  * State $5$: Blood Nova (expanding shockwave).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 1$:
    - If $L = 5 \lor R = 5$:
      $$S_{t+1}(x) = 0$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 5$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 5$$
  - If $s = 3$:
    - If $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 4$$
    - Else:
      $$S_{t+1}(x) = 3$$
  - If $s = 2$:
    - If $L = 5 \lor R = 5$:
      $$S_{t+1}(x) = 5$$
    - Else:
      $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    - If $L = 5 \lor R = 5$:
      $$S_{t+1}(x) = 5$$
    - Else if $L = 1 \lor R = 1$:
      $$S_{t+1}(x) = 2$$
    - Else if $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models blood magic rituals. The Sacrificial Altar (1) pumps out Flowing Blood (2). When the blood reaches a Runic Circle (3), the rune absorbs it, saturating (4) and immediately discharging a massive Blood Nova (5). The nova propagates as a wave, vaporizing the blood conduits and resetting the altar back to normal stone floor (0), establishing a cyclical burst engine.
* **Expected Visual Behavior:** Alternating expansion rings. The altar sends out diagonal streaks of blood (2) that strike stationary circles (3). Upon impact, a fast expanding wave of state 5 explodes outwards, clearing all conduits and shutting down the altar, which must then wait for external recharge, resulting in a breathing visual rhythm.

---

### Rule 9: Philosopher's Seed Crystallization
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Liquid Mercury (background medium).
  * State $1$: Stone Crystal Core (stable gold).
  * State $2$: Crystallization Seed (growth tip).
  * State $3$: Sulfur Impurity (growth promoter).
  * State $4$: Lead Impurity (growth inhibitor).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 1$ or $s = 4$:
    $$S_{t+1}(x) = s$$
  - If $s = 3$:
    - If $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 3$$
  - If $s = 2$:
    - If $L = 4 \lor R = 4$:
      $$S_{t+1}(x) = 4$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 0$:
    - If $L = 2 \land R = 2$:
      $$S_{t+1}(x) = 1$$
    - Else if $L = 2 \lor R = 2$:
      $$S_{t+1}(x) = 2$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the crystal growth of the Philosopher's Stone. The seed (2) expands into mercury (0), leaving a core of gold (1). If it hits sulfur (3), it triggers a secondary growth front, causing branching. If it hits lead (4), it stalls the crystallization tip, freezing it into an inert state.
* **Expected Visual Behavior:** Clean triangular shapes representing crystal facets. The edges are outlined in bright seeds (2). Pockets of lead (4) truncate the triangles, carving flat boundaries into the growth. Sulfur spots (3) generate branching shoots, creating nested fractal triangles.

---

### Rule 10: Void Corruption and Abyssal Decay
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Stable Matter (inert substrate).
  * State $1$: Mana-infused Matter (high-energy reactant).
  * State $2$: Abyssal Core (stable, collapsed vacuum).
  * State $3$: Ravenous Void (highly active decay front).
  * State $4$: Decaying Ectoplasm (unstable transient).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state, $L = S_t(x-1)$, and $R = S_t(x+1)$.
  - If $s = 2$:
    $$S_{t+1}(x) = 2$$
  - If $s = 4$:
    $$S_{t+1}(x) = 2$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 1$:
    - If $L \in \{2, 3\} \lor R \in \{2, 3\}$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 1$$
  - If $s = 0$:
    - If $L = 3 \land R = 3$:
      $$S_{t+1}(x) = 3$$
    - Else if $L = 2 \land R = 2$:
      $$S_{t+1}(x) = 3$$
    - Else if $L = 3 \lor R = 3$:
      $$S_{t+1}(x) = 3$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the entropic expansion of the Abyssal Void. The Abyssal Core (2) slowly eats away stable matter (0) by converting it to Ravenous Void (3) at the boundary. When it touches Mana-infused Matter (1), the high concentration of magical energy triggers a local collapse, rapidly expanding the active void before it decays to ectoplasm (4) and finally condenses into core (2).
* **Expected Visual Behavior:** Dark vertical stripes of Abyssal Core (2) with glowing margins of Ravenous Void (3). Pockets of Mana-infused Matter (1) appear as bright fields that instantly dissolve upon contact with the void, creating dynamic, erratic erosion patterns and complex webbed textures.
