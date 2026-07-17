# Loop 16 Cellular Automata Rules: Quantum Electrodynamics

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Quantum Electrodynamics (QED)**.

These rules model fundamental quantum field interactions, vacuum behavior, and particle dynamics, such as virtual particle pair creation/annihilation, photon-electron scattering (Compton scattering), Feynman diagram vertices, Bremsstrahlung, vacuum polarization screening, Casimir pressure, Dirac sea hole excitations, Schwinger pair production, electron self-energy renormalization, and the Aharonov-Bohm phase shift. Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates unique visual signatures reflecting their quantum physical motivations.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Physical Expectation |
|---|---|---|---|---|---|
| **1** | [Vacuum Fluctuation and Pair Production](#rule-1-vacuum-fluctuation-and-pair-production) | 5 | Radius $r=1$ | Spontaneous excitation of vacuum into virtual electron-positron pairs | Oscillating tracks of pairs separating and annihilating into photons |
| **2** | [Compton Scattering](#rule-2-compton-scattering) | 5 | Radius $r=1$ | Momentum transfer from photon to resting electron | Photon reflection and electron recoil in opposite directions |
| **3** | [Feynman Vertex Coupling](#rule-3-feynman-vertex-coupling) | 6 | Radius $r=1$ | Electron-positron collision creating a virtual photon and outgoing photon pair | Collision nodes releasing isotropic outward-propagating photon waves |
| **4** | [Casimir Vacuum Suppression](#rule-4-casimir-vacuum-suppression) | 5 | Radius $r=1$ | Suppression of virtual photon modes inside narrow conducting plates | High virtual energy density outside plates creating pressure |
| **5** | [Bremsstrahlung Deceleration Radiation](#rule-5-bremsstrahlung-deceleration-radiation) | 5 | Radius $r=1$ | Deceleration of electron near heavy nucleus emitting a photon | Moving electron stops at nucleus, emitting a left-moving photon |
| **6** | [Vacuum Polarization Screening](#rule-6-vacuum-polarization-screening) | 5 | Radius $r=1$ | Bare charge attracting opposite virtual charges to screen its potential | Stable, layered screening structures around a central charge |
| **7** | [Dirac Sea Hole Excitation](#rule-7-dirac-sea-hole-excitation) | 5 | Radius $r=1$ | Photon exciting a negative-energy sea electron to conduction band | Co-propagating electron and positron hole moving in opposite directions |
| **8** | [Schwinger Field-Induced Pair Production](#rule-8-schwinger-field-induced-pair-production) | 5 | Radius $r=1$ | Decay of strong electric field into electron-positron pairs | Large field blocks decay into outward-propagating charge waves |
| **9** | [Self-Energy Dressed Electron](#rule-9-self-energy-dressed-electron) | 5 | Radius $r=1$ | Electron periodically emitting and reabsorbing virtual photons | Rhythmic breathing/pulsation of electron cloud core |
| **10** | [Aharonov-Bohm Phase Shift](#rule-10-aharonov-bohm-phase-shift) | 5 | Radius $r=2$ | Phase shift of electron bypassing a shielded magnetic flux tube | Electrons tunneling over barriers with a transient phase transition |

---

## Rule Definitions

### Rule 1: Vacuum Fluctuation and Pair Production
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum ($|0\rangle$, ground state).
  * State $1$: Virtual Electron ($e^-$, left-moving).
  * State $2$: Virtual Positron ($e^+$, right-moving).
  * State $3$: Virtual Photon ($\gamma$, collision/decay product).
  * State $4$: Vacuum Excitation (Fluctuation trigger).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } s = 0 \text{ and } S_t(x-1) = 2 \text{ and } S_t(x+1) = 1 \\
  1 & \text{else if } s = 0 \text{ and } S_t(x+1) = 4 \\
  2 & \text{else if } s = 0 \text{ and } S_t(x-1) = 4 \\
  1 & \text{else if } s = 0 \text{ and } S_t(x+1) = 1 \\
  2 & \text{else if } s = 0 \text{ and } S_t(x-1) = 2 \\
  0 & \text{else if } s = 0 \\
  3 & \text{if } s = 1 \text{ and } S_t(x-1) = 2 \\
  0 & \text{else if } s = 1 \\
  3 & \text{if } s = 2 \text{ and } S_t(x+1) = 1 \\
  0 & \text{else if } s = 2 \\
  4 & \text{if } s = 3 \\
  0 & \text{if } s = 4 \\
  \end{cases}$$
* **Mathematical Rationale:** This models the spontaneous creation of virtual particle-antiparticle pairs from vacuum fluctuations, in accordance with the Heisenberg uncertainty principle. A photon (3) decays into a vacuum excitation (4), which polarizes the vacuum, splitting into a left-moving electron (1) and a right-moving positron (2). When they encounter oppositely charged virtual particles, they annihilate back into a photon (3).
* **Expected Visual Behavior:** Clean, V-shaped patterns of separating tracks (states 1 and 2) that originate from localized excitation nodes (state 4). The tracks annihilate upon collision, producing brief photon flashes (state 3) before recycling.

---

### Rule 2: Compton Scattering
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum.
  * State $1$: Stationary Electron ($e^-_{rest}$).
  * State $2$: Right-propagating Photon ($\gamma_R$).
  * State $3$: Recoiling Electron ($e^-_{recoil}$, right-moving).
  * State $4$: Scattered Photon ($\gamma_L$, left-moving).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 2 \text{ and } S_t(x) \neq 1 \\
    4 & \text{else if } S_t(x+1) = 4 \\
    3 & \text{else if } S_t(x-1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x-1) = 2 \text{ or } S_t(x-1) = 3 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x+1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x+1) = 1 \text{ or } S_t(x+1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** Models the conservation of momentum during electron-photon collisions (Compton scattering). A photon (2) striking an electron (1) transfers its momentum: the photon scatters backward (4), and the electron recoils forward (3). If the recoiling electron (3) strikes another resting electron, momentum is transferred down the line (Newton's cradle effect), restoring the first electron to rest (1) and recoiling the next.
* **Expected Visual Behavior:** Rightward propagating diagonal lines of photons (state 2) striking stationary vertical lines (state 1). Upon impact, a photon is reflected as a leftward diagonal line (state 4), and the electron line shifts to the right (state 3) until it hits another stationary electron, cascading the momentum.

---

### Rule 3: Feynman Vertex Coupling
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Quantum Vacuum.
  * State $1$: Right-moving Electron ($e^-_{R}$).
  * State $2$: Left-moving Positron ($e^+_{L}$).
  * State $3$: Outgoing Photons ($\gamma_{out}$, isotropic expansion).
  * State $4$: Virtual Photon Intermediary ($\gamma_{virt}$).
  * State $5$: Vertex Core (High energy density).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 2 \\
    1 & \text{else if } S_t(x-1) = 1 \\
    2 & \text{else if } S_t(x+1) = 2 \\
    3 & \text{else if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 3$$
  - If $s = 5$:
    $$S_{t+1}(x) = 4$$
* **Mathematical Rationale:** Represents the fundamental vertex of QED ($e^+ e^- \gamma$ coupling). Incoming electron and positron fields collide to form a vertex node (5), representing the interaction point in a Feynman diagram. This vertex relaxes into a virtual photon state (4), which decays into two outgoing real photons (3) that disperse outward.
* **Expected Visual Behavior:** Two converging diagonal lines (states 1 and 2) that meet at a single point, triggering a stationary glowing node (state 5) that delays for 2 steps (transitioning to 4, then 3) before exploding into a pair of expanding, outward-propagating diagonal photon lines (state 3).

---

### Rule 4: Casimir Vacuum Suppression
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Free Space Vacuum.
  * State $1$: Conducting Plate (Static boundary).
  * State $2$: High-Frequency Virtual Photon ($\gamma_{high}$, decays rapidly).
  * State $3$: Low-Frequency Virtual Photon ($\gamma_{low}$, propagates).
  * State $4$: Casimir Pressure Zone.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $P(x) = \mathbb{I}(S_t(x-1) = 1) + \mathbb{I}(S_t(x+1) = 1)$ be the count of adjacent plate boundaries.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 2$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } P(x) \ge 1 \text{ and } (S_t(x-1) \in \{2, 3\} \lor S_t(x+1) \in \{2, 3\}) \\
    3 & \text{else if } P(x) = 1 \\
    3 & \text{else if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    2 & \text{else if } S_t(x-1) = 2 \lor S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models the Casimir effect, where conducting boundaries restrict the allowed wavelengths of virtual photons. In narrow cavities (width 1), $P(x) = 2$, which suppresses photon generation. In wider spaces or outside the plates ($P(x) = 1$), virtual photons are generated at the boundaries and propagate outward. When these photons hit the plates, they exert pressure (4). The asymmetry in pressure between the inside and outside of the plates drives the Casimir force.
* **Expected Visual Behavior:** Conducting plates (state 1) remain static. Inside a narrow cavity, the space remains dark (state 0) due to mode suppression. On the outer sides of the plates, virtual photons (states 3 and 2) propagate away, periodically striking the plates to create a glowing pressure boundary (state 4).

---

### Rule 5: Bremsstrahlung Deceleration Radiation
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum.
  * State $1$: Fast Electron ($e^-$, moves right).
  * State $2$: Bremsstrahlung Photon ($\gamma_{brems}$, moves left).
  * State $3$: Bare Nucleus ($Ze$, static charge center).
  * State $4$: Screened Nucleus ($Ze + e^-$, captured charge).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 3 \text{ (deceleration point)} \\
    1 & \text{else if } S_t(x-1) = 1 \\
    2 & \text{else if } S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = 0$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 2 \text{ (captures electron charge after photon emission)} \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 4$$
* **Mathematical Rationale:** Models Bremsstrahlung ("braking radiation") and charge capture. As a fast electron (1) approaches a heavy nucleus (3), it is decelerated by the electric field, emitting a photon (2) in the opposite direction. The nucleus then absorbs the electron's remaining kinetic energy, becoming a stable, screened nucleus (4).
* **Expected Visual Behavior:** A fast diagonal electron track (state 1) runs toward a static nuclear block (state 3). One step before contact, a reverse photon track (state 2) is emitted, and the nucleus permanently transitions to state 4, showing a screened state.

---

### Rule 6: Vacuum Polarization Screening
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unpolarized Vacuum.
  * State $1$: Bare Positive Charge ($Q^+$).
  * State $2$: Polarized Electron Cloud ($e^-_{pol}$).
  * State $3$: Polarized Positron Cloud ($e^+_{pol}$).
  * State $4$: Screened Charge Core.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 2 \text{ and } S_t(x+1) = 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = 2$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 4$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 1 \lor S_t(x+1) = 1 \\
    3 & \text{else if } S_t(x-1) = 2 \lor S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models the screening of a bare positive charge in QED by vacuum polarization. The strong electric field of the bare charge (1) attracts virtual electrons (2) to its immediate neighbors and repels virtual positrons (3) to the next shell. Once the charge is fully screened, it stabilizes into a shielded core (4), and the repelled positrons disperse back into the vacuum.
* **Expected Visual Behavior:** A single point charge (1) spontaneously recruits a flanking shell of state 2, which then collapses the core into state 4. A brief, fading outer ring of state 3 appears and disappears, leaving a stable three-cell screened charge configuration.

---

### Rule 7: Dirac Sea Hole Excitation
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Dirac Sea (Negative-energy ground state).
  * State $1$: Conduction Electron ($e^-$, positive energy, moves left).
  * State $2$: Positron Hole ($e^+$, empty negative-energy state, moves right).
  * State $3$: Incident Photon ($\gamma$).
  * State $4$: Excited Transition State.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 3 \lor S_t(x+1) = 3 \\
    2 & \text{else if } S_t(x-1) = 4 \\
    1 & \text{else if } S_t(x+1) = 1 \\
    2 & \text{else if } S_t(x-1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = 0$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 1$$
* **Mathematical Rationale:** Models Dirac's original formulation of the positron as a "hole" in a filled sea of negative energy states. An incoming photon (3) excites a sea state (0) into an intermediate transition state (4). This splits: the electron is lifted to the conduction band (1, moving left), leaving a vacant hole in the sea (2, moving right as a positron).
* **Expected Visual Behavior:** Incoming diagonal photon lines (state 3) hit the vacuum. Upon impact, they trigger a transition node (state 4) that immediately splits into a left-moving conduction electron (state 1) and a right-moving positron hole (state 2).

---

### Rule 8: Schwinger Field-Induced Pair Production
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum.
  * State $1$: Strong Electric Field ($E_{strong}$).
  * State $2$: Electron ($e^-$, moves left).
  * State $3$: Positron ($e^+$, moves right).
  * State $4$: Weakened Electric Field ($E_{weak}$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 1 \\
    2 & \text{else if } S_t(x+1) = 4 \\
    3 & \text{else if } S_t(x-1) = 4 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 4$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x+1) = 2 \\
    3 & \text{if } S_t(x-1) = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models the Schwinger effect, where a strong homogeneous electric field (1) is unstable and decays by producing electron-positron pairs. The interior of the field decays first into a weakened field (4). The boundaries of the field then decay, creating electrons (2) and positrons (3) that move outwards, shielding and neutralizing the external field.
* **Expected Visual Behavior:** Expanding blocks of strong electric fields (state 1) suddenly develop a weakened core (state 4) in their center. The outer boundaries then ignite, releasing left-moving electrons (state 2) and right-moving positrons (state 3) that propagate away into the vacuum.

---

### Rule 9: Self-Energy Dressed Electron
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum.
  * State $1$: Bare Electron ($e^-_0$).
  * State $2$: Cloud Photon ($\gamma_{cloud}$).
  * State $3$: Dressed Core ($e^-_{dressed}$).
  * State $4$: Reabsorbing Core.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = 3$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 4$:
    $$S_{t+1}(x) = 1$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 1 \lor S_t(x+1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models electron self-energy corrections in QED, where a physical electron is a "dressed" state undergoing continuous emission and reabsorption of virtual photons. A bare electron (1) emits a virtual photon cloud to its neighbors (2) while becoming a dressed core (3). The core then absorbs the cloud (transitioning to 4, which clears the cloud cells), returning to the bare state (1) to start the cycle anew.
* **Expected Visual Behavior:** A stationary electron cell that exhibits a periodic, rhythmic "breathing" or "pulsation" pattern. It alternates between a single localized state and a three-cell configuration with a bright core flanked by a pair of virtual photon clouds.

---

### Rule 10: Aharonov-Bohm Phase Shift
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Field-Free Vacuum.
  * State $1$: Shielded Magnetic Flux Tube ($B$, static solenoid).
  * State $2$: Right-propagating Electron (Phase $\theta_0$).
  * State $3$: Left-propagating Electron (Phase $\theta_1$).
  * State $4$: Phase-Shifted Electron ($\theta_0 + \Delta\theta$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-2) = 2 \text{ and } S_t(x-1) = 1 \\
    4 & \text{else if } S_t(x+2) = 3 \text{ and } S_t(x+1) = 1 \\
    2 & \text{else if } S_t(x-1) = 2 \\
    3 & \text{else if } S_t(x+1) = 3 \\
    2 & \text{else if } S_t(x-1) = 4 \\
    3 & \text{else if } S_t(x+1) = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models the Aharonov-Bohm effect, where a charged particle's phase is shifted by vector potentials even in regions of zero field. A right-moving (2) or left-moving (3) electron bypasses a shielded magnetic solenoid (1). In the 1D lattice, this is represented by the electron "tunneling" over the flux tube boundary. As it does so, its state changes to the phase-shifted representation (4), before resuming propagation with the modified phase.
* **Expected Visual Behavior:** Moving electron lines (states 2 and 3) traveling across the lattice. When they encounter a static solenoid barrier (state 1), they teleport/tunnel across it, flashing briefly as state 4 for one step, and then continuing their propagation as a phase-shifted wave.
