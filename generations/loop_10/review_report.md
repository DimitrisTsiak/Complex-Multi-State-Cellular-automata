# Loop 10 Cellular Automata Review: Cryptographic Scramblers & Chaotic Maps

This report presents a visual, aesthetic, and mathematical analysis of the 20 space-time diagrams generated in `loop_10/output/`. These rules operate on algebraic structures, discrete chaotic maps, and cryptographic primitives, resulting in patterns that range from highly ordered fractals to pure pseudo-random noise.

---

## Individual Rule Analysis

### Rule 1: Coupled Discrete Logistic Map
* **States ($N$):** 17
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A symmetrical triangular wedge expanding at 1 cell/step (forming a $45^\circ$ boundary). The interior is filled with highly dense, multi-colored noise, but features a sharp vertical line of symmetry down the center and faint chevron-like structures near the apex.
* **Random-Seed Visuals:** A uniform, high-entropy, fine-grained noise texture without any visible macroscopic structures.
* **Order vs. Chaos:** High chaos. The quadratic folding of the logistic map ($4S(17-S)$) over $\mathbb{F}_{17}$ dominates the system, causing rapid diffusion of the seed into deterministic noise.
* **Aesthetics:** Vibrant and high-contrast, utilizing the Deep Purple $\to$ Hot Pink $\to$ Gold $\to$ Cyan palette. The single-seed wedge stands out cleanly against the black background.

### Rule 2: Local Feistel Nibble Scrambler
* **States ($N$):** 16 (4-bit nibbles)
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** An asymmetric wedge. Crucially, because the PRESENT S-box does not map $0 \to 0$ ($S_{\text{box}}[0] = 0xC$), the background is not empty but alternates between state $0$ and state $12$ at each step, creating green and dark navy horizontal stripes. The interior is a highly scrambled, blocky texture.
* **Random-Seed Visuals:** A homogeneous, fine-grained texture dominated by purple, magenta, and green, showing no spatial correlation.
* **Order vs. Chaos:** Deep chaos with a strong avalanche effect. The non-linear S-box substitution completely scrambles linear relations, and the Feistel layout creates asymmetric information flow.
* **Aesthetics:** The striped background contrasted with the dense purple/green interior creates a distinct retro-digital aesthetic, though it is slightly blocky and noisy.

### Rule 3: Spatially Coupled Tent Map Lattice
* **States ($N$):** 32
* **Neighborhood:** $r=1$ (excluding self in derivative, but includes self in tent map)
* **Single-Seed Visuals:** An asymmetric triangular wedge with a black background. The interior is filled with green-yellow-red noise, but is noticeably sheared, showing subtle diagonal stripes and wave structures running down-right.
* **Random-Seed Visuals:** High-entropy green-yellow speckled texture, slightly more structured than Rule 1 due to the derivative coupling.
* **Order vs. Chaos:** Chaotic. The tent map's positive Lyapunov exponent amplifies numerical fluctuations, while the spatial derivative term ($S(x-1) - S(x+1)$) drives the shearing waves.
* **Aesthetics:** Excellent contrast and a warm, organic color profile (Forest Green $\to$ Mint $\to$ Yellow-Green $\to$ Orange $\to$ Dark Red). The shearing waves give it a dynamic feel.

### Rule 4: Modular Hill Cipher CA
* **States ($N$):** 26
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A symmetrical triangular wedge. The apex features beautiful, highly ordered crystalline nested triangles. As we move down, these structures gradually break down and dissolve into a dense blue-and-white scrambled noise.
* **Random-Seed Visuals:** A uniform blue-white speckled texture representing global chaos.
* **Order vs. Chaos:** Transition from order to chaos. The linear coefficients $[1, 2, 3]$ initially dictate structured wave diffusion (order), but the non-linear cubic term $S_t(x)^3 \pmod{26}$ slowly accumulates differences until it triggers complete non-linear confusion (chaos).
* **Aesthetics:** Highly appealing. The Lavender $\to$ Sky Blue $\to$ Blue $\to$ White-Hot Gold palette is clean, and the transition from crystalline geometry to noise is visually fascinating.

### Rule 5: Keccak-Inspired $\theta$-$\chi$ CA
* **States ($N$):** 8 (3-bit vectors)
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A highly asymmetric wedge. The right boundary propagates at 2 cells/step (flat slope), while the left boundary propagates at 1 cell/step (steep slope). The right boundary wraps around the periodic grid, intersecting the left boundary. The interior is a completely homogeneous, fine-grained teal-purple noise.
* **Random-Seed Visuals:** Uniform, structureless neon teal-purple noise.
* **Order vs. Chaos:** High chaos. The combination of Keccak's $\theta$ step (linear diffusion) and $\chi$ step (non-linear degree-2 mapping) ensures that any structure is instantly pulverized into pseudo-random noise.
* **Aesthetics:** Distinctly modern/cyberpunk due to the Neon Teal $\to$ Neon Purple $\to$ Neon Yellow palette, though it lacks macroscopic patterns.

### Rule 6: Coupled Discrete Henon Map
* **States ($N$):** 16
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A breathtakingly unique, asymmetric structure. The left boundary is a **perfectly vertical line**, while the right boundary propagates at 2 cells/step, wrapping around the screen. The interior is filled with stunning, nested square-like and diagonal fractal filaments in red, orange, and magenta. The background alternates between states 1 and 3, appearing as a dark red texture.
* **Random-Seed Visuals:** High-entropy pink-orange-red scrambled texture.
* **Order vs. Chaos:** Highly complex. A perfect balance of quadratic folding and asymmetric neighbor coupling allows stable, self-canceling wave boundaries (creating the vertical wall) alongside chaotic interior filaments.
* **Aesthetics:** Outstanding. The Charcoal $\to$ Red $\to$ Orange $\to$ Magenta $\to$ Gold palette fits the Henon attractor theme perfectly. The visual variety of the nested shapes is mesmerizing.

### Rule 7: Quadratic Additive-Multiplicative CA
* **States ($N$):** 13
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A symmetrical triangular wedge. The background alternates between states 1 and 5 (green stripes). The interior is filled with a vibrant green, cyan, and white pattern. It has a sharp vertical line of symmetry and exhibits nested chevron structures that repeat.
* **Random-Seed Visuals:** Uniform green-cyan noise.
* **Order vs. Chaos:** Chaotic. The multiplication of neighbors ($S(x-1) \cdot S(x+1)$) behaves like a pseudo-random permutation over $\mathbb{F}_{13}$, shattering the seed, while the quadratic self-coupling maintains some localized symmetrical features.
* **Aesthetics:** Very clean and bright. The Dark Teal $\to$ Lime $\to$ Cyan $\to$ White palette is refreshing, and the horizontal background stripes provide excellent framing.

### Rule 8: Arnold's Cat Map Lattice
* **States ($N$):** 16
* **Neighborhood:** $r=1$ (including self)
* **Single-Seed Visuals:** A beautiful, highly structured triangular wedge against a black background. The interior features a striking combination of strongly sheared, diagonal bands (leaning down-right) and **large, empty triangular gaps** (Sierpinski-like fractal holes) of varying scales.
* **Random-Seed Visuals:** Detailed pink-violet-orange noise with faint diagonal shearing textures.
* **Order vs. Chaos:** Emergent complexity. The splitting of state space into 2D coordinates and updating via the Cat Map matrix creates chaotic sheared bands along the matrix eigenvectors. The spatial coupling allows these sheared bands to form macroscopic fractal-like voids.
* **Aesthetics:** Visually stunning. The combination of empty black triangular voids and detailed, colorful sheared textures (Navy $\to$ Violet $\to$ Pink $\to$ Tangerine $\to$ Pale Yellow) is highly artistic and complex.

### Rule 9: Substitution-Permutation Network CA
* **States ($N$):** 16 (4-bit values)
* **Neighborhood:** $r=2$ (including self)
* **Single-Seed Visuals:** A highly ordered, clean fractal pattern with horizontal stripes and Sierpinski-like triangles in yellow and dark red. The background alternates between states 0 and 5.
* **Random-Seed Visuals:** A completely uniform, structureless, high-entropy noise texture.
* **Order vs. Chaos:** A fascinating case of **algebraic state space collapse**. While designed to be a cryptographic scrambler (using a PRESENT-like SPN round), the single-seed initialization of state 1 ($0001_2$) restricts the cell states to a low-entropy linear/symmetric subspace where the S-box behaves linearly, producing a clean fractal. However, the random seed successfully breaks this subspace trap, producing pure, high-entropy pseudo-random noise.
* **Aesthetics:** Visually clean and highly geometric. The Crimson $\to$ Orange-Red $\to$ Gold palette gives the nested triangles a glowing, flame-like appearance.

### Rule 10: Non-Linear Feedback Shift Register CA
* **States ($N$):** 2 (Binary)
* **Neighborhood:** Asymmetric $r=3$ ($x-3, x-2, x-1, x, x+1$)
* **Single-Seed Visuals:** A highly asymmetric binary wedge. The left boundary is a **perfectly vertical line** at the center, while the right boundary propagates at a speed of exactly 3 cells/step (flat slope), wrapping around the screen. The interior is filled with an extremely detailed, non-linear binary noise pattern of neon green on a dark violet background.
* **Random-Seed Visuals:** Uniform, fine-grained neon green-on-violet binary noise.
* **Order vs. Chaos:** Pure chaos with unidirectional flow. Because the update rule only depends on cells at index $x+1$ and to its left ($x, x-1, x-2, x-3$), information is mathematically forbidden from propagating to the left of the seed, ensuring the vertical left boundary. The rightmost active cell is pulled right by 3 cells per step.
* **Aesthetics:** Stark, high-contrast digital look. The Neon Lime Green on Dark Violet-Black is clean and evokes a classic matrix/terminal aesthetic.

---

## Top 3 Winner Rules

After analyzing all 20 space-time diagrams, the following three rules are selected as the winners based on their visual complexity, aesthetic appeal, and unique mathematical behaviors:

### 🏆 1st Place: Rule 6 (Coupled Discrete Henon Map)
* **Visual Appeal:** 10/10
* **Mathematical Sophistication:** 10/10
* **Justification:** Rule 6 is the standout winner due to its extraordinary combination of nested, strange-attractor-like filaments and the **vertical boundary phenomenon** on its left side. Mathematically, the leftward propagation is blocked because when the perturbation reaches index $W/2-3$, its difference from the background is always $\pm 8 \pmod{16}$. When multiplied by the neighbor coefficient of $2$, this difference becomes $16 \equiv 0 \pmod{16}$, canceling its effect on the next cell to the left. This creates a perfectly stable vertical wall on the left, while the right side propagates chaotically at 2 cells/step. The resulting asymmetric, nested square and diagonal patterns are visually gorgeous and mathematically brilliant.

### 🥈 2nd Place: Rule 8 (Arnold's Cat Map Lattice)
* **Visual Appeal:** 9.5/10
* **Mathematical Sophistication:** 9/10
* **Justification:** Rule 8 achieves a stunning visual balance between order and chaos. The space-time diagram features large, macroscopic triangular voids (fractal order) embedded within a highly detailed, sheared texture (chaos). The diagonal slants in the texture directly reflect the eigenvectors of the Arnold's Cat Map matrix. This rule demonstrates how local toral automorphisms can be coupled across a lattice to generate beautiful, large-scale structures that are visually engaging and highlight the underlying mathematical eigenvectors.

### 🥉 3rd Place: Rule 9 (Substitution-Permutation Network CA)
* **Visual Appeal:** 9/10
* **Mathematical Sophistication:** 8.5/10
* **Justification:** Rule 9 is selected because of the fascinating **discrepancy between its design expectation and visual reality**. Designed as a cryptographically secure SPN scrambler, it was expected to produce structureless noise from a single seed. Instead, the single seed collapses the state space into a low-entropy subspace, producing a highly ordered, gorgeous yellow-and-red Sierpinski fractal. In contrast, the random-seed diagram is pure, homogeneous noise. This dramatic bifurcation of behavior depending on the initial entropy makes it a compelling study in algebraic dynamics and one of the most visually striking patterns in the set.

---

## Honorable Mention: Rule 10 (NLFSR CA)
Rule 10 deserves an honorable mention for its strict **unidirectional propagation**. The rule mathematically guarantees that the leftmost active cell remains fixed at the seed position (forming a vertical boundary), while the rightmost boundary sweeps right at exactly 3 cells/step. This creates a highly asymmetric wedge of binary keystream noise that is visually clean and mathematically pure.
