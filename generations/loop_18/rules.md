# Loop 18 Cellular Automata Rules: Retrocausal Time-Travel & Paradox Resolution

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Retrocausal Time-Travel & Paradox Resolution**. 

These rules model fundamental time-travel and retrocausality concepts, such as signals sent back in time (tachyonic signals, advanced waves), closed time-like curves (CTCs), branching timeline mergers, temporal paradoxes (grandfather and bootstrap paradoxes), and chronological protection mechanisms (Novikov self-consistency, Hawking's vacuum polarization blow-up, and chrono-static anchors). Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Physical Expectation |
|---|---|---|---|---|---|
| **1** | [Novikov Consistency Lock](#rule-1-novikov-consistency-lock) | 5 | Radius $r=1$ | Resolution of counter-propagating advanced and retarded waves via consistency nodes | Intersecting diagonals that pass through each other via localized lock dots |
| **2** | [Branching Timeline Merger](#rule-2-branching-timeline-merger) | 6 | Radius $r=1$ | Expansion of parallel histories forming a stable boundary interface | Expanding solid regions separated by vertical interfacial walls |
| **3** | [Bootstrap Paradox (Causal Loop)](#rule-3-bootstrap-paradox-causal-loop) | 5 | Radius $r=1$ | Self-sustaining causal loop where artifact triggers retro-signal and vice versa | Zig-zag diagonal oscillations between two static boundary columns |
| **4** | [Chronology Protection Blow-Up](#rule-4-chronology-protection-blow-up) | 5 | Radius $r=2$ | Vacuum polarization buildup leading to a singularity blast near CTCs | Branching structures that explode into large clearings |
| **5** | [Tachyonic Anti-Telephone](#rule-5-tachyonic-anti-telephone) | 5 | Radius $r=2$ | Superluminal retro-feedback inhibiting its own transmitter source | Rapidly oscillating vertical source lines emitting steep tachyon lines |
| **6** | [CTC Phase Coherence](#rule-6-ctc-phase-coherence) | 5 | Radius $r=1$ | Quantum phase alignment and destructive interference inside a CTC | Homogeneous color blocks separated by black decoherence gaps |
| **7** | [Temporal Friction and Chrono-decay](#rule-7-temporal-friction-and-chrono-decay) | 6 | Radius $r=1$ | Degradation and slowing of travelers with each timeline loop | Reflected lines that steepen (slow down) and explode upon collision |
| **8** | [Retrocausal Absorber Transaction](#rule-8-retrocausal-absorber-transaction) | 5 | Radius $r=1$ | Handshake transaction between advanced waves and retarded waves | Periodic V-shaped patterns formed between emitters and absorbers |
| **9** | [Grandfather Paradox (Timeline Splitting)](#rule-9-grandfather-paradox-timeline-splitting) | 6 | Radius $r=1$ | Branching of a timeline into parallel histories separated by a paradox horizon | Glider striking a block and triggering a new timeline color on its left |
| **10** | [Chrono-Static Anchor Field](#rule-10-chrono-static-anchor-field) | 5 | Radius $r=2$ | Shielding field around anchors that neutralizes retrocausal signals | Static pillars with protective halos that absorb incoming signals |

---

## Rule Definitions

### Rule 1: Novikov Consistency Lock
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Stable Timeline (Vacuum, ground state).
  * State $1$: Retarded Signal ($T_+$, forward-propagating wave, moves right).
  * State $2$: Advanced Signal ($T_-$, retrocausal wave, moves left).
  * State $3$: Paradox Contradiction (Instability state, resolved instantly).
  * State $4$: Novikov Consistency Lock (Localized spatial coherence shield).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  $$S_{t+1}(x) = \begin{cases}
  4 & \text{if } s = 0 \text{ and } l_1 = 1 \text{ and } r_1 = 2 \\
  1 & \text{else if } s = 0 \text{ and } l_1 = 4 \\
  2 & \text{else if } s = 0 \text{ and } r_1 = 4 \\
  1 & \text{else if } s = 0 \text{ and } l_1 = 1 \\
  2 & \text{else if } s = 0 \text{ and } r_1 = 2 \\
  0 & \text{else if } s = 0 \\
  4 & \text{if } s = 1 \text{ and } (r_1 = 2 \lor r_1 = 4) \\
  0 & \text{else if } s = 1 \\
  4 & \text{if } s = 2 \text{ and } (l_1 = 1 \lor l_1 = 4) \\
  0 & \text{else if } s = 2 \\
  4 & \text{if } s = 3 \\
  0 & \text{if } s = 4 \\
  \end{cases}$$
* **Mathematical Rationale:** This rule models two counter-propagating waves representing forward time (retarded, state 1) and backward time (advanced, state 2) signals. Instead of colliding and creating a grandfather-like inconsistency (which would yield a permanent paradox state 3), the Novikov Principle enforces self-consistency. When they meet, they form a consistency lock (state 4) that acts as a localized junction. In the next step, the lock decays back to vacuum while seamlessly re-emitting the two waves on their respective trajectories (state 1 to the right, state 2 to the left), resolving the temporal path without local contradiction.
* **Expected Visual Behavior:** Clean, intersecting diagonal lines of states 1 (slanted right) and 2 (slanted left). Where they cross, a single-dot lock (state 4) forms, producing a grid of crossing points that preserve the integrity of the paths.

---

### Rule 2: Branching Timeline Merger
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Unwritten Vacuum (Primordial timeline canvas).
  * State $1$: Timeline Alpha ($\alpha$-history, left-expanding).
  * State $2$: Timeline Beta ($\beta$-history, right-expanding).
  * State $3$: Branching Origin (Point of timeline divergence).
  * State $4$: Merger Zone (Temporal boundary interface).
  * State $5$: Timeline Decay (Entropy cleanup of mismatch).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } l_1 = 3 \text{ or } r_1 = 3 \\
    4 & \text{else if } l_1 = 1 \text{ and } r_1 = 2 \\
    4 & \text{else if } l_1 = 1 \text{ and } r_1 = 4 \\
    1 & \text{else if } l_1 = 1 \\
    2 & \text{else if } r_1 = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } r_1 = 2 \\
    5 & \text{else if } r_1 = 5 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } l_1 = 1 \\
    5 & \text{else if } l_1 = 5 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 5$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } l_1 = 5 \text{ or } r_1 = 5 \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 5$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** When two different timelines (1 and 2) collide, they do not annihilate immediately. Instead, they form a stable, static Merger Zone (state 4) that separates them. The branching event (state 3) serves as a source that decays and leaves behind a merger interface. If one of the timelines decays (state 5), the decay propagates along the interface, erasing the merger zone and restoring the unwritten vacuum.
* **Expected Visual Behavior:** Expanding solid regions of state 1 (left-to-right) and state 2 (right-to-left). When they meet, they lock and form a vertical border (state 4) that halts expansion. Branching origins (state 3) quickly decay to 5, leaving localized lines of interface that separate different domains.

---

### Rule 3: Bootstrap Paradox (Causal Loop)
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Flat Spacetime (Vacuum).
  * State $1$: The Causal Artifact (Physical object, moves right, speed 1).
  * State $2$: Retrocausal Information Signal (Advanced wave, moves left, speed 1).
  * State $3$: Loop Emitter (Stationary source that spawns the artifact when triggered).
  * State $4$: Future Receiver (Stationary sink that receives the artifact and transmits the retrocausal signal).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } l_1 = 1 \\
    2 & \text{else if } r_1 = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = 0$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } r_1 = 2 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } l_1 = 1 \\
    4 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** This rule demonstrates a closed causal cycle. An emitter (3) and a receiver (4) are positioned in space. If the emitter receives the retrocausal wave (2), it creates the artifact (1). When the artifact (1) propagates rightward and reaches the receiver (4), it triggers the receiver to emit a retrocausal signal (2) leftward. The retrocausal signal propagates back to the emitter, completing the loop. The loop has no beginning or end; the artifact's existence is entirely self-justified by the closed loop.
* **Expected Visual Behavior:** A standing rectangular grid pattern between fixed vertical lines (states 3 and 4). Right-slanting lines (state 1) alternate with left-slanting lines (state 2), creating a continuous zig-zag oscillation representing a stable causal loop.

---

### Rule 4: Chronology Protection Blow-Up
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Calm Vacuum.
  * State $1$: Closed Timelike Curve (CTC) Seed (Unstable time-loop node).
  * State $2$: Vacuum Polarization Accumulator (Energy builder).
  * State $3$: Chronological Protection Blast (Singularity explosion).
  * State $4$: Decaying Ash (Energy dissipation).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the state of cell $x$. Let $N_1, N_2, N_3$ be the counts of states 1, 2, and 3 respectively in the radius $2$ neighborhood of $x$ (excluding cell $x$ itself).
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_3 > 0 \\
    2 & \text{else if } N_1 \ge 3 \\
    1 & \text{else if } N_1 \in \{1, 2\} \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_3 > 0 \\
    2 & \text{else if } N_2 \ge 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } N_3 > 0 \\
    3 & \text{else if } (N_1 + N_2) \ge 4 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** The accumulation of time-machine nodes (state 1) induces a back-reaction in the vacuum. When the local density of CTC seeds is low, they spread. However, when the density of CTC seeds and polarized vacuum states (state 2) exceeds a threshold (total 4 or more in radius 2), it triggers a singularity blast (state 3). This blast clears all distortion in its neighborhood, restoring the vacuum (via state 4), conforming to Hawking's conjecture.
* **Expected Visual Behavior:** Branching, expanding structures of states 1 and 2 that suddenly hit a critical thickness and erupt into a bright, localized block of state 3 (blast). The blast then shrinks and leaves behind a cleared path of state 0, creating a self-limiting structure.

---

### Rule 5: Tachyonic Anti-Telephone
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quiet Vacuum.
  * State $1$: Tachyon Pulse (Superluminal signal, moves left at speed 2).
  * State $2$: Retarded Trigger (Subluminal signal, moves right at speed 1).
  * State $3$: Active Transmitter (Ready to fire).
  * State $4$: Inhibited Transmitter (Suppressed by retro-feedback).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the state of cell $x$, and let $l_2 = S_t(x-2)$, $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$, $r_2 = S_t(x+2)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } r_2 = 1 \\
    2 & \text{else if } l_1 = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = 0$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } l_1 = 2 \\
    4 & \text{else if } r_1 = 1 \text{ or } r_2 = 1 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 3$$
* **Mathematical Rationale:** A subluminal wave (2) moves right and hits an active transmitter (3), triggering a tachyon pulse (1) that moves left at speed 2. Because the tachyon travels superluminally, it arrives at the emitter's location in the past (represented spatially by propagating leftward and striking the emitter). Upon hitting the active transmitter (3), the tachyon inhibits it (state 4), making it unable to transmit. The transmitter then enters a refractory/inhibited state, resetting to active (3) on the next step. This models the classic grandfather paradox feedback loop: the signal shuts down the transmitter that sent it, causing a periodic oscillation.
* **Expected Visual Behavior:** Rapidly oscillating vertical lines of state 3 and 4 (the transmitter), triggered by diagonal lines of retarded waves (state 2) and emitting steep diagonal lines of tachyons (state 1, angle is half of state 2's angle due to speed 2).

---

### Rule 6: CTC Phase Coherence
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Decoherence (Vacuum/destructive interference).
  * States $1, 2, 3, 4$: Phase states ($\phi_0, \phi_1, \phi_2, \phi_3$, representing quantized phases).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  Let the phase distance function $d(a, b)$ for $a, b \in \{1, 2, 3, 4\}$ be:
  $$d(a, b) = \min(|a - b|, 4 - |a - b|)$$
  - If $s \in \{1, 2, 3, 4\}$:
    $$S_{t+1}(x) = \begin{cases}
    0 & \text{if } l_1 \in \{1, 2, 3, 4\} \text{ and } d(s, l_1) > 1 \\
    0 & \text{else if } r_1 \in \{1, 2, 3, 4\} \text{ and } d(s, r_1) > 1 \\
    s & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    l_1 & \text{if } l_1 \in \{1, 2, 3, 4\} \text{ and } r_1 = 0 \\
    r_1 & \text{else if } r_1 \in \{1, 2, 3, 4\} \text{ and } l_1 = 0 \\
    l_1 & \text{else if } l_1 \in \{1, 2, 3, 4\} \text{ and } r_1 \in \{1, 2, 3, 4\} \text{ and } d(l_1, r_1) \le 1 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** The state of a cell represents its quantum phase. To exist in a closed timelike curve, the boundary conditions require the phase to be self-consistent. If two adjacent cells have phases that differ by more than 1 unit, they interfere destructively and collapse to the ground state 0. If they are close (phase difference $\le 1$), they merge and align, representing constructive interference.
* **Expected Visual Behavior:** Clean, homogeneous patches of phase states (1, 2, 3, or 4) with sharp boundaries. When incompatible phases collide, they form black gaps of state 0, representing destructive interference, while compatible phases merge smoothly.

---

### Rule 7: Temporal Friction and Chrono-decay
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Vacuum.
  * State $1$: Fresh Traveler ($T_0$, speed 1, right-moving).
  * State $2$: Gen-1 Traveler ($T_1$, speed 1, left-moving).
  * State $3$: Gen-2 Traveler ($T_2$, speed 0.5, right-moving, moves only on even steps).
  * State $4$: Stationary Traveler ($T_3$, decayed, stationary).
  * State $5$: Annihilation Burst (Chrono-radiation).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } l_1 = 1 \text{ and } r_1 = 2 \\
    1 & \text{else if } l_1 = 1 \\
    2 & \text{else if } r_1 = 2 \\
    3 & \text{else if } l_1 = 3 \text{ and } t \pmod 2 = 0 \\
    5 & \text{else if } l_1 = 5 \text{ or } r_1 = 5 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } r_1 \in \{2, 4\} \text{ or } r_1 \text{ is a boundary} \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } l_1 \in \{1, 4\} \text{ or } l_1 \text{ is a boundary} \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } t \pmod 2 = 0 \text{ and } (r_1 = 4 \text{ or } r_1 \text{ is a boundary}) \\
    0 & \text{else if } t \pmod 2 = 0 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } l_1 = 5 \text{ or } r_1 = 5 \text{ or } (l_1 = 3 \text{ and } t \pmod 2 = 0) \\
    4 & \text{otherwise}
    \end{cases}$$
  - If $s = 5$:
    $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:** A traveling particle degrades due to temporal friction. Each reflection (representing a loop traversal) shifts its generation: $1 \to 2 \to 3 \to 4$. Its velocity decreases from 1 to 0.5 (moving on alternate steps) and then to 0. Once stationary (state 4), it becomes highly unstable and explodes into chrono-radiation (state 5) if struck by another particle, cleaning the temporal grid.
* **Expected Visual Behavior:** Diagonal lines of state 1 and 2 that reflect. State 3 is represented by a steeper diagonal line (half speed). The stationary state 4 forms vertical lines, which explode into expanding cones of state 5 when hit, leading to rich, interactive patterns.

---

### Rule 8: Retrocausal Absorber Transaction
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Quantum Vacuum.
  * State $1$: Idle Emitter.
  * State $2$: Retarded Wave (Forward wave, moves right, speed 1).
  * State $3$: Advanced Wave (Backward wave, moves left, speed 1).
  * State $4$: Idle Absorber.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } l_1 = 2 \\
    3 & \text{else if } r_1 = 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } r_1 = 3 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = 0$$
  - If $s = 3$:
    $$S_{t+1}(x) = 0$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } l_1 = 2 \\
    3 & \text{else if } t \pmod{16} == 0 \\
    4 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** Models the transaction handshake of the absorber theory. A future absorber (4) emits a retrocausal advanced wave (3) traveling left. When the advanced wave reaches the emitter (1), it triggers the emission of a retarded wave (2) traveling right. The retarded wave eventually reaches the absorber (4), completing the handshake transaction. The emitter remains dark unless a handshake is established.
* **Expected Visual Behavior:** Static vertical lines of emitters (1) and absorbers (4). Periodically (every 16 steps), absorbers emit leftward-slanted lines of state 3. When they strike the emitter (1), they reflect as rightward-slanted lines of state 2, returning to the absorber. This forms clean, periodic "V" shapes aligned horizontally.

---

### Rule 9: Grandfather Paradox (Timeline Splitting)
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Unwritten Void.
  * State $1$: Timeline A (Possibility where traveler is born).
  * State $2$: Timeline B (Possibility where traveler is unborn).
  * State $3$: Paradox Horizon (The branching domain wall).
  * State $4$: Time Traveler (Left-moving glider, speed 1).
  * State $5$: Paradox Excitation (Local collision site).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } l_1 = 1 \\
    2 & \text{else if } r_1 = 2 \\
    3 & \text{else if } l_1 = 5 \text{ or } r_1 = 5 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } r_1 = 4 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } l_1 = 4 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } l_1 = 5 \\
    1 & \text{else if } r_1 = 5 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 5$:
    $$S_{t+1}(x) = 3$$
* **Mathematical Rationale:** A time traveler (4) travels left. When they collide with a timeline (1 or 2), they create a paradox excitation (5) because their presence alters the conditions of their own birth. The paradox resolves by splitting the space into Timeline A (1) and Timeline B (2), separated by a stable boundary called the Paradox Horizon (3). This prevents a global contradiction by localizing the split.
* **Expected Visual Behavior:** A left-moving diagonal line (state 4) striking a solid block of state 1. On impact, a vertical line (state 3) is generated, with state 1 on its right and a newly generated block of state 2 on its left, showing a clear spatial division of the two histories.

---

### Rule 10: Chrono-Static Anchor Field
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unshielded Spacetime.
  * State $1$: Temporal Anchor (Static source).
  * State $2$: Chrono-static Shield (Protected area).
  * State $3$: Retrocausal Signal (Moves left, speed 1).
  * State $4$: Tachyon Pulse (Moves right, speed 2).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$, and let $N_1$ be the count of state 1 in the radius 2 neighborhood of $x$ (including cell $x$).
  Let $l_2 = S_t(x-2)$, $l_1 = S_t(x-1)$, $r_1 = S_t(x+1)$, $r_2 = S_t(x+2)$.
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_1 > 0 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_1 > 0 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_1 > 0 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } N_1 > 0 \\
    3 & \text{else if } r_1 = 3 \\
    4 & \text{else if } l_2 = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:** A temporal anchor (1) acts as an indestructible boundary condition. It projects a chrono-static shield (2) in its radius 2 neighborhood. Any retrocausal signal (3) or tachyon pulse (4) that enters this shield is immediately converted to a shield state (2), preventing it from passing through or changing the state of the anchor's region. This represents an absolute local history protector.
* **Expected Visual Behavior:** Fixed vertical pillars of state 1 surrounded by a green halo of state 2. Diagonal lines representing signals (states 3 and 4) approach the pillars but disappear upon touching the green shield, leaving the central anchor undisturbed.
