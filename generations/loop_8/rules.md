# Loop 8 Cellular Automata Rules: Quantum-Walk & Wave Interference

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Quantum-Walk & Wave Interference**. 

Unlike standard excitable or cyclic media, these rules model the dynamics of wave packets carrying **discrete phases** (representing sign or phase angle), **amplitudes**, and **chiral directions**. They simulate quantum phenomena such as superposition, constructive and destructive interference, wave packet dispersion, tunneling through barriers, and pilot-wave guidance.

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time diagrams of these rules will showcase interference fringes, wave-packet splitting, localized standing waves, and quantum scattering.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Discrete Hadamard Walk](#rule-1-discrete-hadamard-walk) | 9 | Radius $r=1$ | Discrete sign-preserving Hadamard coin | Spreading wave-packets with quantum interference fringes |
| **2** | [Quantum Tunneling & Scattering](#rule-2-quantum-tunneling--scattering) | 8 | Radius $r=2$ | Wave-splitting at semi-permeable barriers | Reflected & transmitted wave-packets crossing barriers |
| **3** | [Discrete Wave Equation](#rule-3-discrete-wave-equation) | 9 | Radius $r=1$ | Discretized displacement-velocity wave coupling | Circular wavefronts, reflections, and interference patterns |
| **4** | [Decohering Quantum Walk](#rule-4-decohering-quantum-walk) | 6 | Radius $r=1$ | Phase randomization via spatial noise | Transition from quantum interference to classical diffusion |
| **5** | [Bohmian Pilot-Wave CA](#rule-5-bohmian-pilot-wave-ca) | 6 | Radius $r=1$ | Guiding wave field with localized tracer particles | Wave-like patterns guiding localized diagonal gliders |
| **6** | [Discrete Nonlinear Schrödinger Envelope](#rule-6-discrete-nonlinear-schrödinger-envelope) | 5 | Radius $r=1$ | Dispersion vs. self-focusing amplitude threshold | Stable envelope solitons that survive collisions |
| **7** | [Fractional Chiral Edge States](#rule-7-fractional-chiral-edge-states) | 7 | Radius $r=1$ | Algebraic conservation of fractional charges | Directional charge packets with algebraic interference |
| **8** | [Beam Splitter Interferometer](#rule-8-beam-splitter-interometer) | 8 | Radius $r=1$ | Static waveguides, mirrors, and phase-shifters | Intersecting paths creating resonances and cancellations |
| **9** | [Schrödinger Wave-Packet Dispersion](#rule-9-schrödinger-wave-packet-dispersion) | 5 | Radius $r=1$ | Coupled real-imaginary Schrödinger update | Dispersive spreading of packets with spatial chirp |
| **10** | [Chiral Solitonic Rabi Oscillations](#rule-10-chiral-solitonic-rabi-oscillations) | 6 | Radius $r=1$ | Wave-packet absorption & stimulated emission | Periodic excitation and emission (Rabi cycles) |

---

## Rule Definitions

### Rule 1: Discrete Hadamard Walk
* **States ($N$):** $9$ states ($0, 1, \dots, 8$).
  States represent the wave amplitude vector $\begin{pmatrix} \psi_R \\ \psi_L \end{pmatrix}$ where $\psi_R, \psi_L \in \{-1, 0, 1\}$:
  * State $0$: $\begin{pmatrix} 0 \\ 0 \end{pmatrix}$ (vacuum)
  * State $1$: $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$ (right-mover $+$)
  * State $2$: $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$ (left-mover $+$)
  * State $3$: $\begin{pmatrix} -1 \\ 0 \end{pmatrix}$ (right-mover $-$)
  * State $4$: $\begin{pmatrix} 0 \\ -1 \end{pmatrix}$ (left-mover $-$)
  * State $5$: $\begin{pmatrix} 1 \\ 1 \end{pmatrix}$ (symmetric superposition $+/+$)
  * State $6$: $\begin{pmatrix} -1 \\ -1 \end{pmatrix}$ (symmetric superposition $-/-$)
  * State $7$: $\begin{pmatrix} 1 \\ -1 \end{pmatrix}$ (asymmetric superposition $+/-$)
  * State $8$: $\begin{pmatrix} -1 \\ 1 \end{pmatrix}$ (asymmetric superposition $-/+$)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let the component amplitudes of cell $y$ at time $t$ be $\psi_R(t, y)$ and $\psi_L(t, y)$.
  The incoming wave amplitudes at cell $x$ are:
  $$a = \psi_R(t, x-1) \quad (\text{entering from the left})$$
  $$b = \psi_L(t, x+1) \quad (\text{entering from the right})$$
  The updated amplitudes $\psi_R(t+1, x)$ and $\psi_L(t+1, x)$ are calculated via a discrete sign-preserving Hadamard coin:
  $$\psi_R(t+1, x) = \text{sgn}(a + b)$$
  $$\psi_L(t+1, x) = \text{sgn}(a - b)$$
  where $\text{sgn}(z) = 1$ if $z > 0$, $-1$ if $z < 0$, and $0$ if $z = 0$.
  The state $S_{t+1}(x)$ is the state corresponding to the resulting vector.
* **Mathematical Rationale:** This implements a discrete-time quantum walk (DTQW) using a discrete coin operator. By mapping the continuous unitary Hadamard coin to a discrete signum-based coin, we preserve phase-dependent superposition and destructive interference (cancellation when $a$ and $b$ have opposite signs) while keeping the state space strictly finite.
* **Expected Visual Behavior:** Under a single-seed start, a wave packet will split and propagate outward, creating distinct, nested wave-interference fringes. Colliding wave fronts will display clear phase-dependent cancellation.

---

### Rule 2: Quantum Tunneling & Scattering
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State $0$: Vacuum
  * State $1$: Right-mover $+$
  * State   $2$: Left-mover $+$
  * State   $3$: Right-mover $-$
  * State   $4$: Left-mover $-$
  * State $5$: Potential Barrier (static)
  * State $6$: High potential wall (fully reflective, static)
  * State $7$: Superposition state (both left and right movers, $+/+$)
* **Neighborhood ($N(x)$):** Radius $r=2$:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $\psi_R(y) = 1$ if $S(y) \in \{1, 7\}$, $-1$ if $S(y) = 3$, $0$ otherwise.
  Let $\psi_L(y) = 1$ if $S(y) \in \{2, 7\}$, $-1$ if $S(y) = 4$, $0$ otherwise.
  * If $S_t(x) \in \{5, 6\} \implies S_{t+1}(x) = S_t(x)$ (barriers are static).
  * If $S_t(x) \notin \{5, 6\}$, we calculate the incoming amplitudes:
    $$a = \begin{cases}
    -\psi_L(t, x) & \text{if } S_t(x-1) = 6 \quad (\text{reflection from wall}) \\
    \psi_R(t, x-2) - \psi_L(t, x) & \text{else if } S_t(x-1) = 5 \quad (\text{tunneling + partial reflection}) \\
    \psi_R(t, x-1) & \text{otherwise}
    \end{cases}$$
    $$b = \begin{cases}
    -\psi_R(t, x) & \text{if } S_t(x+1) = 6 \quad (\text{reflection from wall}) \\
    \psi_L(t, x+2) - \psi_R(t, x) & \text{else if } S_t(x+1) = 5 \quad (\text{tunneling + partial reflection}) \\
    \psi_L(t, x+1) & \text{otherwise}
    \end{cases}$$
    Let the final amplitudes be $a' = \text{clip}(a, -1, 1)$ and $b' = \text{clip}(b, -1, 1)$.
    The state $S_{t+1}(x)$ is:
    * State $1$ if $a'=1, b'=0$
    * State $3$ if $a'=-1, b'=0$
    * State $2$ if $a'=0, b'=1$
    * State $4$ if $a'=0, b'=-1$
    * State $7$ if $a'=1, b'=1$
    * State $0$ otherwise (destructive cancellation or vacuum).
* **Mathematical Rationale:** This model couples quantum-walk dynamics with potential barriers. High barrier walls reflect waves with a $\pi$ phase shift (amplitude negation), while low barriers act as semi-permeable interfaces that partition incoming energy into a transmitted wave and a reflected wave.
* **Expected Visual Behavior:** Waves moving across the space-time diagram that split when hitting static barriers, producing both reflected waves going backward and weaker transmitted waves continuing forward.

---

### Rule 3: Discrete Wave Equation
* **States ($N$):** $9$ states ($0, 1, \dots, 8$).
  States represent the displacement and velocity pair $(U, V)$ where $U, V \in \{-1, 0, 1\}$:
  * State $0$: $(0, 0)$
  * State $1$: $(1, 0)$
  * State $2$: $(-1, 0)$
  * State $3$: $(0, 1)$
  * State $4$: $(0, -1)$
  * State $5$: $(1, 1)$
  * State $6$: $(-1, -1)$
  * State $7$: $(1, -1)$
  * State $8$: $(-1, 1)$
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Extract $U_t(y)$ and $V_t(y)$ from the cell states.
  Compute the discrete spatial Laplacian of displacement:
  $$\Delta U_t(x) = U_t(x-1) - 2 U_t(x) + U_t(x+1)$$
  Update the velocity and displacement:
  $$V_{t+1}(x) = \text{clip}(V_t(x) + \Delta U_t(x), -1, 1)$$
  $$U_{t+1}(x) = \text{clip}(U_t(x) + V_{t+1}(x), -1, 1)$$
  where $\text{clip}(z, -1, 1) = \max(-1, \min(1, z))$.
  The state $S_{t+1}(x)$ is the state corresponding to the pair $(U_{t+1}(x), V_{t+1}(x))$.
* **Mathematical Rationale:** This rule is a direct Euler discretization of the classical second-order wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$. By representing both displacement and velocity as state variables, it simulates physical wave propagation, reflection off boundaries, and constructive/destructive superposition.
* **Expected Visual Behavior:** Expanding circular ripples originating from initial seeds. When two ripples intersect, they will show classic constructive reinforcement or destructive cancellation, creating checkerboard-like interference nodes.

---

### Rule 4: Decohering Quantum Walk
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Vacuum
  * State $1$: Coherent right-mover $+$
  * State $2$: Coherent left-mover $+$
  * State   $3$: Coherent right-mover $-$
  * State   $4$: Coherent left-mover $-$
  * State $5$: Decoherent noise (random walk, no phase info)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $R_{in} = 1$ if $S_t(x-1) = 1$, $-1$ if $S_t(x-1) = 3$, $0$ otherwise.
  Let $L_{in} = 1$ if $S_t(x+1) = 2$, $-1$ if $S_t(x+1) = 4$, $0$ otherwise.
  Let the local noise flag be $N_{flag} = \mathbb{I}(S_t(x-1) = 5) + \mathbb{I}(S_t(x+1) = 5) + \mathbb{I}(S_t(x) = 5)$.
  * If $N_{flag} \ge 1$ and ($R_{in} \neq 0$ or $L_{in} \neq 0$ or $S_t(x) = 5$):
    $$S_{t+1}(x) = 5 \quad (\text{decoheres into noise})$$
  * Else if $N_{flag} = 0$:
    * If $R_{in} \neq 0$ and $L_{in} \neq 0$:
      * If $R_{in} = L_{in} \implies S_{t+1}(x) = 1$ (if $R_{in}=1$) or $4$ (if $R_{in}=-1$).
      * If $R_{in} \neq L_{in} \implies S_{t+1}(x) = 0$ (destructive cancellation).
    * If $R_{in} \neq 0$ and $L_{in} = 0 \implies S_{t+1}(x) = 1$ (if $R_{in}=1$) or $3$ (if $R_{in}=-1$).
    * If $L_{in} \neq 0$ and $R_{in} = 0 \implies S_{t+1}(x) = 2$ (if $L_{in}=1$) or $4$ (if $L_{in}=-1$).
    * Otherwise, $S_{t+1}(x) = 0$.
* **Mathematical Rationale:** In quantum computing, environmental noise causes decoherence, destroying the phase relations necessary for quantum walks. Here, state 5 represents classical noise. Any coherent wave that comes into contact with state 5 has its phase randomized, transitioning from a quantum walk (which has speed $\propto t$) to a classical random walk (diffusion, speed $\propto \sqrt{t}$).
* **Expected Visual Behavior:** Clean, structured quantum-walk light cones that dissolve into messy, fuzzy, classical diffusion patterns as soon as they encounter noise blocks.

---

### Rule 5: Bohmian Pilot-Wave CA
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Vacuum
  * State $1$: Wave amplitude $+1$
  * State   $2$: Wave amplitude $-1$
  * State $3$: Particle alone (on vacuum)
  * State $4$: Particle riding on wave $+1$
  * State $5$: Particle riding on wave $-1$
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let the wave amplitude at cell $y$ be $\psi_t(y) = 1$ if $S_t(y) \in \{1, 4\}$, $-1$ if $S_t(y) \in \{2, 5\}$, $0$ otherwise.
  Let the particle presence at cell $y$ be $P_t(y) = 1$ if $S_t(y) \in \{3, 4, 5\}$, $0$ otherwise.
  1. **Wave Update**:
     $$\psi_{t+1}(x) = \text{sign}(\psi_t(x-1) + \psi_t(x+1))$$
  2. **Particle Update**:
     A particle at $x$ looks at the new wave magnitudes in its neighborhood: $M_L = |\psi_{t+1}(x-1)|$, $M_C = |\psi_{t+1}(x)|$, and $M_R = |\psi_{t+1}(x+1)|$.
     The particle moves to the neighbor with the maximum wave magnitude.
     Let $P_{new}(x)$ indicate if a particle landed on cell $x$ at $t+1$:
     $$P_{new}(x) = 1 \iff \text{any particle from } \{x-1, x, x+1\} \text{ moved to } x \text{ based on the maximum gradient rule}$$
  3. **Combine**:
     * If $P_{new}(x) = 0 \implies S_{t+1}(x) = 0$ (if $\psi_{t+1}(x) = 0$), $1$ (if $\psi_{t+1}(x) = 1$), $2$ (if $\psi_{t+1}(x) = -1$).
     * If $P_{new}(x) = 1 \implies S_{t+1}(x) = 3$ (if $\psi_{t+1}(x) = 0$), $4$ (if $\psi_{t+1}(x) = 1$), $5$ (if $\psi_{t+1}(x) = -1$).
* **Mathematical Rationale:** This rule models De Broglie-Bohm "pilot wave" mechanics. A continuous, linear wave field guides a localized particle. The wave propagates independently, while the particle acts as a tracer seeking regions of high wave density (constructive interference), creating a one-way dynamical coupling.
* **Expected Visual Behavior:** Broad wave-like envelopes filling the background, within which localized, sharp diagonal lines (particles) propagate. The particles will bend, reflect, or cluster near the crests of the wave envelopes.

---

### Rule 6: Discrete Nonlinear Schrödinger Envelope
* **States ($N$):** $5$ states ($0, 1, \dots, 4$).
  * State $0$: Quiescent (zero amplitude)
  * State $1$: Low amplitude
  * State $2$: Moderate amplitude
  * State $3$: High amplitude
  * State $4$: Soliton core (maximum amplitude)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $A_t(x) = S_t(x-1) + S_t(x+1)$ be the total neighbor amplitude.
  * If the cell state is low-energy ($S_t(x) \le 1$), it undergoes dispersion:
    $$S_{t+1}(x) = \text{round}(A_t(x) / 3)$$
  * If the cell state is high-energy ($S_t(x) \ge 2$), it self-focuses:
    $$S_{t+1}(x) = \begin{cases}
    \min(4, S_t(x) + 1) & \text{if } A_t(x) \ge 3 \\
    S_t(x) - 1 & \text{if } A_t(x) < 3
    \end{cases}$$
* **Mathematical Rationale:** This models the Nonlinear Schrödinger Equation (NLSE) which describes envelope solitons in nonlinear optics. At low amplitudes, linear dispersion dominates, causing the wave packet to diffuse. At high amplitudes, self-phase modulation focuses the energy, compensating for dispersion and forming a stable soliton.
* **Expected Visual Behavior:** Standard wave packets disperse into zero. However, starting with a sufficiently dense clump of high-amplitude states (e.g. state 3 or 4) creates a highly stable, non-dispersive soliton structure that propagates diagonally and passes through other solitons.

---

### Rule 7: Fractional Chiral Edge States
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Neutral (charge 0)
  * State $1$: Charge $+1/3$ (Right-moving)
  * State $2$: Charge $+2/3$ (Right-moving)
  * State $3$: Charge $+1$ (Right-moving)
  * State $4$: Charge $-1/3$ (Left-moving)
  * State $5$: Charge $-2/3$ (Left-moving)
  * State $6$: Charge $-1$ (Left-moving)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $q_R$ be the positive charge entering cell $x$ from the left neighbor $x-1$:
  $$q_R = \begin{cases} 1/3 & \text{if } S_t(x-1) = 1 \\ 2/3 & \text{if } S_t(x-1) = 2 \\ 1 & \text{if } S_t(x-1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  Let $q_L$ be the negative charge entering cell $x$ from the right neighbor $x+1$:
  $$q_L = \begin{cases} -1/3 & \text{if } S_t(x+1) = 4 \\ -2/3 & \text{if } S_t(x+1) = 5 \\ -1 & \text{if } S_t(x+1) = 6 \\ 0 & \text{otherwise} \end{cases}$$
  The net charge at cell $x$ is $Q = q_R + q_L$.
  The state $S_{t+1}(x)$ is determined by the sign and value of $Q$:
  * If $Q = 0 \implies S_{t+1}(x) = 0$
  * If $Q > 0$:
    * State $1$ if $Q \le 1/3$
    * State $2$ if $1/3 < Q \le 2/3$
    * State $3$ if $Q > 2/3$
  * If $Q < 0$:
    * State $4$ if $Q \ge -1/3$
    * State $5$ if $-2/3 \le Q < -1/3$
    * State $6$ if $Q < -2/3$
* **Mathematical Rationale:** In the fractional quantum Hall effect, edge states are chiral (unidirectional) and transport fractionalized charge. This rule implements an exact conservation law for fractional charges. When right-moving and left-moving fractional charge packets collide, they add algebraically, leading to either complete annihilation (if charge sums to 0) or partial cancellation.
* **Expected Visual Behavior:** Clean, sloped lines of varying intensity representing charges $+1/3, +2/3, 1$. Collisions will result in charge subtraction, creating thinner lines or empty space, illustrating algebraic interference.

---

### Rule 8: Beam Splitter Interferometer
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * State $0$: Vacuum
  * State $1$: Right-mover wave, phase $0$
  * State $2$: Right-mover wave, phase $\pi$
  * State $3$: Left-mover wave, phase $0$
  * State $4$: Left-mover wave, phase $\pi$
  * State $5$: Beam Splitter (static, semi-permeable)
  * State $6$: Mirror (static, fully reflective)
  * State $7$: Phase-Shifter (static, shifts phase of passing waves by $\pi$)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  * If $S_t(x) \in \{5, 6, 7\} \implies S_{t+1}(x) = S_t(x)$ (static components).
  * If $S_t(x) \notin \{5, 6, 7\}$, we calculate the incoming right-mover amplitude $a$ and left-mover amplitude $b$:
    $$a = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \\
    -1 & \text{if } S_t(x-1) = 2 \\
    -1 & \text{if } S_t(x-1) = 7 \text{ and } S_t(x-2) = 1 \quad (\text{phase-shift}) \\
    1 & \text{if } S_t(x-1) = 7 \text{ and } S_t(x-2) = 2 \quad (\text{phase-shift}) \\
    -1 & \text{if } S_t(x-1) = 6 \text{ and } S_t(x) = 3 \quad (\text{reflection}) \\
    1 & \text{if } S_t(x-1) = 6 \text{ and } S_t(x) = 4 \quad (\text{reflection}) \\
    0 & \text{otherwise}
    \end{cases}$$
    $$b = \begin{cases}
    1 & \text{if } S_t(x+1) = 3 \\
    -1 & \text{if } S_t(x+1) = 4 \\
    -1 & \text{if } S_t(x+1) = 7 \text{ and } S_t(x+2) = 3 \quad (\text{phase-shift}) \\
    1 & \text{if } S_t(x+1) = 7 \text{ and } S_t(x+2) = 4 \quad (\text{phase-shift}) \\
    -1 & \text{if } S_t(x+1) = 6 \text{ and } S_t(x) = 1 \quad (\text{reflection}) \\
    1 & \text{if } S_t(x+1) = 6 \text{ and } S_t(x) = 2 \quad (\text{reflection}) \\
    0 & \text{otherwise}
    \end{cases}$$
    Let the final state be determined by the sum:
    * If $a \neq 0$ and $b \neq 0$:
      * If $a = b \implies S_{t+1}(x) = 1$ (if $a=1$) or $2$ (if $a=-1$).
      * If $a = -b \implies S_{t+1}(x) = 0$ (destructive cancellation).
    * If $a \neq 0$ and $b = 0 \implies S_{t+1}(x) = 1$ (if $a=1$) or $2$ (if $a=-1$).
    * If $b \neq 0$ and $a = 0 \implies S_{t+1}(x) = 3$ (if $b=1$) or $4$ (if $b=-1$).
    * Otherwise, $S_{t+1}(x) = 0$.
* **Mathematical Rationale:** This rule allows the physical layout of optical interferometers (like Mach-Zehnder) on a 1D CA. Static cells represent waveguides, mirrors, and phase plates. Moving cells represent coherent wave packets. Destructive interference occurs when waves of opposite phase meet, canceling the wave amplitude.
* **Expected Visual Behavior:** Waves traveling along diagonal paths that reflect off mirrors, change color (phase) when passing through phase shifters, and cancel each other out when they intersect with opposing phases.

---

### Rule 9: Schrödinger Wave-Packet Dispersion
* **States ($N$):** $5$ states ($0, 1, \dots, 4$).
  States represent the complex wave function $\psi = R + i I$ where $R, I \in \{-1, 0, 1\}$:
  * State $0$: $(0, 0)$ (vacuum)
  * State $1$: $(1, 0)$ (real part $+1$)
  * State   $2$: $(-1, 0)$ (real part $-1$)
  * State $3$: $(0, 1)$ (imaginary part $+1$)
  * State $4$: $(0, -1)$ (imaginary part $-1$)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Extract $R_t(y)$ and $I_t(y)$ from the cell states.
  Calculate the discrete Laplacians:
  $$\Delta R_t(x) = R_t(x-1) - 2 R_t(x) + R_t(x+1)$$
  $$\Delta I_t(x) = I_t(x-1) - 2 I_t(x) + I_t(x+1)$$
  Compute the updated real and imaginary parts based on the Schrödinger relation $\frac{\partial \psi}{\partial t} = i \Delta \psi \implies \frac{\partial R}{\partial t} = -\Delta I, \frac{\partial I}{\partial t} = \Delta R$:
  $$R_{t+1}(x) = \text{clip}(R_t(x) - \Delta I_t(x), -1, 1)$$
  $$I_{t+1}(x) = \text{clip}(I_t(x) + \Delta R_t(x), -1, 1)$$
  The state $S_{t+1}(x)$ is determined by prioritizing the dominant component:
  * If $R_{t+1}(x) = I_{t+1}(x) = 0 \implies S_{t+1}(x) = 0$
  * If $|R_{t+1}(x)| \ge |I_{t+1}(x)| \implies S_{t+1}(x) = 1$ (if $R_{t+1}=1$) or $2$ (if $R_{t+1}=-1$).
  * If $|R_{t+1}(x)| < |I_{t+1}(x)| \implies S_{t+1}(x) = 3$ (if $I_{t+1}=1$) or $4$ (if $I_{t+1}=-1$).
* **Mathematical Rationale:** This implements a discretized free Schrödinger equation. The coupling between the real and imaginary components via the spatial Laplacian is what drives wave-packet dispersion. It mimics how quantum wave-packets spread and chirps in vacuum.
* **Expected Visual Behavior:** Starting from a concentrated wave packet, the wave will spread outward. The space-time diagram will show a characteristic fan-out structure with alternating real and imaginary states, visualizing the dispersion of a quantum particle.

---

### Rule 10: Chiral Solitonic Rabi Oscillations
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Atom ground state $|g\rangle$
  * State $1$: Atom excited state $|e\rangle$
  * State $2$: Right-moving wave (pump field $+$)
  * State $3$: Right-moving wave (pump field $-$)
  * State   $4$: Left-moving wave (pump field $+$)
  * State   $5$: Left-moving wave (pump field $-$)
* **Neighborhood ($N(x)$):** Radius $r=1$:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $W_R$ be the right-moving pump field coming from $x-1$:
  $$W_R = \begin{cases} 1 & \text{if } S_t(x-1) = 2 \\ -1 & \text{if } S_t(x-1) = 3 \\ 0 & \text{otherwise} \end{cases}$$
  Let $W_L$ be the left-moving pump field coming from $x+1$:
  $$W_L = \begin{cases} 1 & \text{if } S_t(x+1) = 4 \\ -1 & \text{if } S_t(x+1) = 5 \\ 0 & \text{otherwise} \end{cases}$$
  The cell state updates based on Rabi-like absorption and stimulated emission:
  * If $S_t(x) = 0$ (ground atom):
    * If $W_R \neq 0$ or $W_L \neq 0$: it absorbs the pump wave and transitions to excited state: $S_{t+1}(x) = 1$.
    * Otherwise, it remains ground state: $S_{t+1}(x) = 0$.
  * If $S_t(x) = 1$ (excited atom):
    * If $W_R \neq 0$: stimulated emission occurs. The atom returns to ground state, emitting an amplified wave packet with a phase flip: $S_{t+1}(x) = 3$ (right-mover $-$).
    * If $W_L \neq 0$: stimulated emission occurs: $S_{t+1}(x) = 5$ (left-mover $-$).
    * Otherwise, it spontaneously decays to ground state: $S_{t+1}(x) = 0$.
  * If $S_t(x) \in \{2, 3\}$ (right-mover in vacuum):
    * It continues propagating right: $S_{t+1}(x) = S_t(x-1)$ if $S_t(x-1) \in \{2, 3\}$, else $0$.
  * If $S_t(x) \in \{4, 5\}$ (left-mover in vacuum):
    * It continues propagating left: $S_{t+1}(x) = S_t(x+1)$ if $S_t(x+1) \in \{4, 5\}$, else $0$.
* **Mathematical Rationale:** This rules models Rabi oscillations from quantum optics. A coherent light field (pump field) interacts with two-level atoms. A ground-state atom absorbs the photon and excites. An excited-state atom is stimulated by a photon to decay and emit a phase-shifted photon.
* **Expected Visual Behavior:** Waves passing through an array of atoms will create a periodic absorption and emission trail. This produces vertical "excited" lines (state 1) and diagonal wave lines, creating a structured lattice pattern of energy exchange.
