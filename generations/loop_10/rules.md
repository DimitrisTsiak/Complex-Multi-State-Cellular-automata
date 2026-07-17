# Loop 10 Cellular Automata Rules: Cryptographic Scramblers & Chaotic Maps

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Cryptographic Scramblers & Chaotic Maps**. 

Unlike the physical systems modeled in Loop 1 (Excitable & Cyclic Media) and Loop 2 (Generations & Outer-Totalistic Media), which rely on threshold-based propagation and state-decay cycles, the rules in this loop utilize algebraic structures, discrete chaotic maps, and cryptographic primitives. These rules operate on a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time progression of these rules generates high-entropy, chaotic patterns and exhibits a strong cryptographic avalanche effect (where a single-bit change in the initial seed rapidly diffuses to randomize the entire system).

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual/Cryptographic Expectation |
|---|---|---|---|---|---|
| **1** | [Coupled Discrete Logistic Map](#rule-1-coupled-discrete-logistic-map) | 17 | Radius $r=1$ | Discretized quadratic map with spatial coupling | High-frequency chaotic fluctuations; rapid seed expansion |
| **2** | [Local Feistel Nibble Scrambler](#rule-2-local-feistel-nibble-scrambler) | 16 | Radius $r=1$ | Feistel round structure with 4-bit S-box | Highly scrambled space-time texture; avoids fixed points |
| **3** | [Spatially Coupled Tent Map Lattice](#rule-3-spatially-coupled-tent-map-lattice) | 32 | Radius $r=1$ (excl. self) | Discretized tent map with derivative coupling | Shearing wave chaos; high sensitivity to boundaries |
| **4** | [Modular Hill Cipher CA](#rule-4-modular-hill-cipher-ca) | 26 | Radius $r=1$ | Linear matrix multiplication + cubic substitution | Rapid linear diffusion gated by cubic non-linearity |
| **5** | [Keccak-Inspired $\theta$-$\chi$ CA](#rule-5-keccak-inspired-theta-chi-ca) | 8 | Radius $r=1$ | 3-bit linear diffusion ($\theta$) + non-linear mix ($\chi$) | Dense, hash-like space-time signature; high degree-2 mixing |
| **6** | [Coupled Discrete Henon Map](#rule-6-coupled-discrete-henon-map) | 16 | Radius $r=1$ | Quadratic fold + asymmetric linear shear | Strange-attractor-like filament structures |
| **7** | [Quadratic Additive-Multiplicative CA](#rule-7-quadratic-additive-multiplicative-ca) | 13 | Radius $r=1$ | Prime field product coupling + quadratic self-map | Rapid multiplication-driven value blowup and fragmentation |
| **8** | [Arnold's Cat Map Lattice](#rule-8-arnolds-cat-map-lattice) | 16 | Radius $r=1$ | Toral automorphism on split coordinates | Strong diagonal shears reflecting chaotic eigenvectors |
| **9** | [Substitution-Permutation Network CA](#rule-9-substitution-permutation-network-ca) | 16 | Radius $r=2$ | 5-cell diffusion + PRESENT S-box + bit-P-box | Complete structureless pseudo-random noise; full avalanche |
| **10** | [Non-Linear Feedback Shift Register CA](#rule-10-non-linear-feedback-shift-register-ca) | 2 | Asymmetric $r=3$ | Linear taps with quadratic product feedback | Highly complex binary pseudorandom keystream pattern |

---

## Rule Definitions

### Rule 1: Coupled Discrete Logistic Map
* **States ($N$):** $17$ states ($0, 1, \dots, 16$). Choosing a prime number of states prevents division/modulo degeneracies and ensures algebraic completeness.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  The transition combines a local quadratic map (modeling the fully chaotic regime of the logistic map, $\mu=4$) with linear spatial coupling:
  $$S_{t+1}(x) = \left[ 4 \cdot S_t(x) \cdot (17 - S_t(x)) + S_t(x-1) + S_t(x+1) \right] \pmod{17}$$
  *(Note: Since $17 \equiv 0 \pmod{17}$, this simplifies algebraically to $[-4 S_t(x)^2 + S_t(x-1) + S_t(x+1)] \pmod{17}$).*
* **Mathematical Rationale:** The continuous logistic map $x_{n+1} = 4x_n(1-x_n)$ is a classic generator of chaos. Discretizing it over the finite field $\mathbb{F}_{17}$ and coupling each cell to its nearest neighbors creates a Coupled Map Lattice (CML). The quadratic term folds the state space, while the neighbor terms diffuse the values.
* **Expected Visual Behavior:** High-entropy chaotic patterns. A single point perturbation will spread diagonally at the maximum speed of $1$ cell per time step, producing an expanding wedge of deterministic noise.

---

### Rule 2: Local Feistel Nibble Scrambler
* **States ($N$):** $16$ states ($0, 1, \dots, 15$), representing 4-bit nibbles.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $\oplus$ denote the bitwise XOR operator. Let $S_{\text{box}}$ be the non-linear 4-bit permutation from the PRESENT block cipher:
  $$S_{\text{box}} = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]$$
  The update rule mimics a round of a Feistel cipher:
  $$S_{t+1}(x) = S_t(x-1) \oplus S_{\text{box}}[S_t(x) \oplus S_t(x+1)]$$
* **Mathematical Rationale:** A Feistel structure guarantees bijective properties and ensures information is scrambled through S-box substitution (confusion) and XOR mixing (diffusion). Because the S-box is non-linear, it breaks any potential linear relations. The offset input ($x-1$ vs $x+1$) creates directional flow.
* **Expected Visual Behavior:** A highly scrambled, blocky texture. Because $S_{\text{box}}[0] = 0xC \neq 0$, the all-zero state is not stable; the rule will generate dynamic patterns even from a completely blank grid.

---

### Rule 3: Spatially Coupled Tent Map Lattice
* **States ($N$):** $32$ states ($0, 1, \dots, 31$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $T(s)$ be the discretized tent map:
  $$T(s) = \begin{cases} 
  2s & \text{if } s < 16 \\ 
  2(31 - s) & \text{if } s \ge 16 
  \end{cases}$$
  The transition couples the local tent map with spatial derivative-like differences:
  $$S_{t+1}(x) = \left[ T(S_t(x)) + S_t(x-1) - S_t(x+1) + 32 \right] \pmod{32}$$
* **Mathematical Rationale:** The tent map is a piecewise linear map with a constant Lyapunov exponent of $\ln(2) > 0$. The difference term $S_t(x-1) - S_t(x+1)$ acts as a spatial first derivative, causing localized shears that sweep through the system and amplify tiny numerical fluctuations.
* **Expected Visual Behavior:** Sharp, jagged boundaries and shearing wave structures. The space-time diagram displays asymmetric diagonal flows due to the directional subtraction in the coupling term.

---

### Rule 4: Modular Hill Cipher CA
* **States ($N$):** $26$ states ($0, 1, \dots, 25$). Modulo 26 maps directly to alphabet-based cryptography (classic Hill cipher).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  The transition combines a linear weighted sum (a row from an invertible Hill cipher matrix) with a non-linear cubic term to prevent linear cryptanalysis:
  $$S_{t+1}(x) = \left[ S_t(x-1) + 2 \cdot S_t(x) + 3 \cdot S_t(x+1) + S_t(x)^3 \right] \pmod{26}$$
* **Mathematical Rationale:** The coefficients $[1, 2, 3]$ are chosen to represent a robust linear diffusion vector. The addition of the cubic term $S_t(x)^3 \pmod{26}$ introduces cryptographic confusion, preventing the pattern from collapsing into simple linear overlays or superpositions.
* **Expected Visual Behavior:** Rapidly spreading, highly structured wave envelopes. Small seeds expand into complex geometric patterns that feature localized crystalline interference zones.

---

### Rule 5: Keccak-Inspired $\theta$-$\chi$ CA
* **States ($N$):** $8$ states ($0, 1, \dots, 7$). Each state is represented as a 3-bit binary vector $(b_2, b_1, b_0)_2$.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  This rule is a two-step process modeled directly on the Keccak (SHA-3) round function.
  Let $\oplus$ be bitwise XOR, $\&$ be bitwise AND, and $\sim$ be bitwise NOT (defined on 3-bit states as $\sim u = 7 \oplus u$).
  Let $\text{rotl}(u, 1)$ be the bitwise left rotation of a 3-bit integer: $\text{rotl}((b_2, b_1, b_0)_2, 1) = (b_1, b_0, b_2)_2$.
  1. Compute the linear diffusion step $\theta$ for all cells:
     $$D_t(x) = S_t(x) \oplus S_t(x-1) \oplus \text{rotl}(S_t(x+1), 1)$$
  2. Compute the non-linear mixing step $\chi$ to get the next state:
     $$S_{t+1}(x) = D_t(x) \oplus \left( (\sim D_t(x-1)) \& D_t(x+1) \right)$$
* **Mathematical Rationale:** Keccak's cryptographic strength is built on combining the linear diffusion of $\theta$ (which spreads differences across bits and coordinates) and the non-linear mapping of $\chi$ (which provides local algebraic mixing of degree 2). This rule translates those exact principles to a 1D spatial lattice.
* **Expected Visual Behavior:** Fine-grained, hash-like space-time diagrams. The combination of bit-shifts, XORs, and local AND gates produces highly complex, noise-like structures that leave no visible geometric artifacts.

---

### Rule 6: Coupled Discrete Henon Map
* **States ($N$):** $16$ states ($0, 1, \dots, 15$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  A discretized, coupled version of the classical 2D Henon map ($x_{t+1} = 1 - a x_t^2 + y_t$, $y_{t+1} = b x_t$):
  $$S_{t+1}(x) = \left[ 1 + 15 \cdot S_t(x)^2 + S_t(x-1) + 2 \cdot S_t(x+1) \right] \pmod{16}$$
  *(Note: Since $15 \equiv -1 \pmod{16}$, the quadratic term represents $-S_t(x)^2$).*
* **Mathematical Rationale:** The Henon map generates chaos by stretching the state space along one dimension and folding it back along another. Here, the quadratic term $-S_t(x)^2$ handles the folding, while the linear neighborhood terms ($S_t(x-1) + 2 S_t(x+1)$) handle the spatial stretching and shearing.
* **Expected Visual Behavior:** Morphing, fractal-like filaments that drift across the space-time grid. The asymmetrical weights in the neighbor terms ($1$ and $2$) force the chaotic attractors to drift preferentially to one side.

---

### Rule 7: Quadratic Additive-Multiplicative CA
* **States ($N$):** $13$ states ($0, 1, \dots, 12$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  $$S_{t+1}(x) = \left[ S_t(x-1) \cdot S_t(x+1) + S_t(x)^2 + 3 \right] \pmod{13}$$
* **Mathematical Rationale:** Operating on the prime field $\mathbb{F}_{13}$, this rule blends additive self-coupling (via the quadratic term $S_t(x)^2$) and multiplicative neighbor coupling ($S_t(x-1) \cdot S_t(x+1)$). The addition of the constant $+3$ acts as a background driver, preventing the grid from settling into inactive zero-states.
* **Expected Visual Behavior:** Instantaneous value explosion and fragmentation. Because multiplication in a prime field behaves like a pseudo-random permutation, any localized seed immediately shatters into a high-frequency, noisy state distribution.

---

### Rule 8: Arnold's Cat Map Lattice
* **States ($N$):** $16$ states ($0, 1, \dots, 15$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  We split the cell state $S_t(x)$ into two 2-bit coordinates $X_t(x) = S_t(x) \pmod 4$ and $Y_t(x) = \lfloor S_t(x)/4 \rfloor$.
  We then apply the classic Arnold's Cat Map matrix to the coordinates, coupled with spatial inputs:
  $$X_{\text{new}}(x) = \left( X_t(x) + Y_t(x) + S_t(x-1) \right) \pmod 4$$
  $$Y_{\text{new}}(x) = \left( X_t(x) + 2 \cdot Y_t(x) + S_t(x+1) \right) \pmod 4$$
  Finally, we recombine the coordinates into the next state:
  $$S_{t+1}(x) = X_{\text{new}}(x) + 4 \cdot Y_{\text{new}}(x)$$
* **Mathematical Rationale:** Arnold's Cat Map is a classic toral automorphism that is hyperbolic and chaotic everywhere. Splitting the state space into 2D coordinates and updating them using the cat map matrix $\begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$ provides local stretching. Coupling the coordinate updates with spatial neighbors extends this chaotic stretching to the lattice.
* **Expected Visual Behavior:** Strongly sheared, diagonal space-time bands. The slope of these bands corresponds to the eigenvectors of the cat map matrix, showing a visual representation of chaotic flow lines.

---

### Rule 9: Substitution-Permutation Network CA
* **States ($N$):** $16$ states ($0, 1, \dots, 15$), representing 4-bit values.
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $\oplus$ denote the bitwise XOR operator.
  1. Combine the neighborhood states linearly using XOR:
     $$M_t(x) = S_t(x-2) \oplus S_t(x-1) \oplus S_t(x) \oplus S_t(x+1) \oplus S_t(x+2)$$
  2. Apply S-box substitution (using the 4-bit PRESENT S-box):
     $$V_t(x) = S_{\text{box}}[M_t(x)]$$
  3. Apply bit-level permutation (P-box) to obtain the next state:
     $$S_{t+1}(x) = P[V_t(x)]$$
     Where the P-box permutation table is:
     $$P = [0, 2, 8, 10, 1, 3, 9, 11, 4, 6, 12, 14, 5, 7, 13, 15]$$
     *(Note: This P-box maps a 4-bit coordinate $(b_3, b_2, b_1, b_0)_2 \to (b_1, b_3, b_0, b_2)_2$).*
* **Mathematical Rationale:** This rule is a direct, parallel implementation of a Substitution-Permutation Network (SPN) cipher round. The 5-cell XOR sum provides linear diffusion, the S-box provides non-linear confusion, and the P-box shuffles the bits to ensure that single-bit changes propagate across different bit positions in subsequent rounds.
* **Expected Visual Behavior:** Pure, structureless pseudo-random noise. It exhibits the strongest avalanche effect of all designed rules; a single-state perturbation in a uniform grid will propagate as a perfect triangular cone filled with high-entropy random values.

---

### Rule 10: Non-Linear Feedback Shift Register CA
* **States ($N$):** $2$ states ($0, 1$).
* **Neighborhood ($N(x)$):** Asymmetric radius $r=3$:
  $$N(x) = \{x-3, x-2, x-1, x, x+1\}$$
* **Transition Function:**
  Let $\oplus$ denote the XOR operator (addition modulo 2) and $\cdot$ denote the AND operator (multiplication modulo 2):
  $$S_{t+1}(x) = S_t(x-3) \oplus S_t(x-1) \oplus S_t(x) \oplus \left( S_t(x-2) \cdot S_t(x+1) \right)$$
* **Mathematical Rationale:** Non-Linear Feedback Shift Registers (NLFSRs) are widely used in stream ciphers (e.g., Grain, Trivium) to generate pseudo-random keystreams. The linear taps ($x-3$, $x-1$, $x$) ensure a long sequence period, while the quadratic term ($S_t(x-2) \cdot S_t(x+1)$) prevents algebraic attacks by raising the algebraic degree of the feedback function.
* **Expected Visual Behavior:** Extremely complex, non-linear binary patterns. While similar in setup to Wolfram's Rule 30, the inclusion of the non-linear neighbor product breaks standard symmetries and creates unique, highly irregular spatial structures.
