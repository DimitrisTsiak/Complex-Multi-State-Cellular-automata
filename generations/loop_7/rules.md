# Loop 7 Cellular Automata Rules: Biological Growth & Chiral Asymmetry

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Biological Growth & Chiral Asymmetry**. 

In this domain, cells transition through $N$ states: $\{0, 1, \dots, N-1\}$. The rules model biological processes such as hormone flow, stem cell division, lateral inhibition, vascularization, filament assembly, and biofilm expansion. Crucially, they incorporate **chiral asymmetry** (breaking reflection symmetry) so that growth and differentiation propagate with a directional bias (typically left-to-right or via asymmetric branching).

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Polar Auxin & Apical Dominance](#rule-1-polar-auxin--apical-dominance) | 5 | Left-side $r=2$ | Unidirectional auxin transport + spacing inhibition | Spaced, propagating apical tip lines |
| **2** | [Anchored Apical Growth](#rule-2-anchored-apical-growth) | 5 | Radius $r=1$ | Asymmetric growth tip and promoter interaction | Solid structural anchor trailing a moving tip |
| **3** | [Chiral Turing Branching](#rule-3-chiral-turing-branching) | 5 | Mixed: $r=1$ symm., $r=3$ left-only | Short-range activator + left-biased inhibitor | Asymmetric periodic branching stripes |
| **4** | [Sinuous Helical Circumnutation](#rule-4-sinuous-helical-circumnutation) | 6 | Dual-range $r=3$ | State-dependent trail-length chirality swap | Sinuous, zig-zag space-time trails |
| **5** | [Asymmetric Stem Cell Niche](#rule-5-asymmetric-stem-cell-niche) | 6 | Radius $r=1$ | Niche-anchored division + contact-inhibited death | Steady differentiated flow with periodic clearing |
| **6** | [Vascular Lumen Formation](#rule-6-vascular-lumen-formation) | 5 | Radius $r=1$ | Polar tip growth + core-tissue apoptosis | Hollow double-walled tube structures |
| **7** | [Morphogenetic French Flag Wave](#rule-7-morphogenetic-french-flag-wave) | 7 | Left-only $r=1$ | Left-to-right morphogen flow + multi-stage differentiation | Propagating tri-color striped bands |
| **8** | [Polar Filament Dynamic Instability](#rule-8-polar-filament-dynamic-instability) | 6 | Radius $r=2$ | Asymmetric plus/minus growth + uncapped catastrophe | Rapid growth interrupted by collapse waves |
| **9** | [Chiral Biofilm Shear Expansion](#rule-9-chiral-biofilm-shear-expansion) | 6 | Radius $r=2$ | Nutrient depletion + asymmetric sliding shear | Asymmetric biofilm profiles with necrotic cores |
| **10** | [Asymmetric Mycelial Branching](#rule-10-asymmetric-mycelial-branching) | 6 | Radius $r=2$ | Apical extension right + lateral branching left | Growing ring-like structures that decay from within |

---

## Rule Definitions

### Rule 1: Polar Auxin & Apical Dominance
*   **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
    *   State $0$: Quiescent / Undifferentiated matrix.
    *   State $1$: Meristem / Growth Tip (Apical cell).
    *   State $2$: High Auxin (Growth promoter hormone).
    *   State $3$: Stem / Stalk (Differentiated stable structure).
    *   State $4$: Low Auxin (Refractory state).
*   **Neighborhood ($N(x)$):** Left-side asymmetric neighborhood of radius $r=2$:
    $$N(x) = \{x-2, x-1\}$$
*   **Transition Function:**
    Let $s = S_t(x)$ be the current cell state.
    *   If $s = 3$, it remains stable:
        $$S_{t+1}(x) = 3$$
    *   If $s = 1$, it differentiates to stem:
        $$S_{t+1}(x) = 3$$
    *   If $s = 2$, it degrades to low auxin:
        $$S_{t+1}(x) = 4$$
    *   If $s = 4$, it decays to quiescent:
        $$S_{t+1}(x) = 0$$
    *   If $s = 0$, it is excited based on hormone flow and lateral inhibition:
        $$S_{t+1}(x) = \begin{cases} 
        1 & \text{if } S_t(x-1) = 2 \text{ and } S_t(x-2) \neq 1 \\ 
        2 & \text{else if } S_t(x-1) \in \{1, 2\} \\
        0 & \text{otherwise} 
        \end{cases}$$
*   **Mathematical Rationale:** Chirality is embedded because the transition only reads states from the left ($x-1$ and $x-2$), forcing a unidirectional flow of auxin to the right. Apical dominance is modeled by the inhibition: if a Meristem ($1$) is at $x-2$, the cell at $x$ cannot become a Meristem ($1$), it becomes High Auxin ($2$) instead, which pushes the next Meristem further to the right. This generates a spaced sequence of growth tips.
*   **Expected Visual Behavior:** Regularly spaced, parallel lines of growing tips propagating diagonally to the right, separated by bands of auxin signals and quiescent space.

### Rule 2: Anchored Apical Growth
*   **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
    *   State $0$: Quiescent / Undifferentiated soil.
    *   State $1$: Active Growth Tip.
    *   State $2$: Chiral Promoter (anchoring signal).
    *   State $3$: Sheath / Mature Stem (Permanent absorbing state).
    *   State $4$: Inhibitor / Decay.
*   **Neighborhood ($N(x)$):** Radius $r=1$:
    $$N(x) = \{x-1, x+1\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    *   If $s = 3$, it remains stable:
        $$S_{t+1}(x) = 3$$
    *   If $s = 1$, it matures:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } S_t(x-1) = 2 \\
        4 & \text{otherwise}
        \end{cases}$$
    *   If $s = 2$, it differentiates to sheath:
        $$S_{t+1}(x) = 3$$
    *   If $s = 4$, it decays:
        $$S_{t+1}(x) = 0$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) \neq 4 \\
        2 & \text{else if } S_t(x+1) = 1 \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** A tip ($1$) at $x$ causes its right neighbor ($x+1$) to become a tip ($1$), and its left neighbor ($x-1$) to become a promoter ($2$). The promoter ($2$) then matures into a permanent sheath ($3$). If the tip has a promoter on its left, it matures into a sheath, anchoring it. Otherwise, it turns to inhibitor ($4$). This rule breaks reflection symmetry: growth is directed to the right ($S_t(x-1)=1 \to S_{t+1}(x)=1$), while the anchoring signal is sent to the left ($S_t(x+1)=1 \to S_{t+1}(x)=2$).
*   **Expected Visual Behavior:** A solid, growing triangular sheath of permanent stem cells (state 3) on the left, capped by an active, diagonally moving growth tip (state 1) on the right.

### Rule 3: Chiral Turing Branching
*   **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
    *   State $0$: Substrate / Quiescent.
    *   State $1$: Activator (high growth activity).
    *   State $2$: Inhibitor (suppressive hormone).
    *   State $3$: Differentiated Tissue (Permanent absorbing state).
    *   State $4$: Depleted / Refractory.
*   **Neighborhoods ($N_A(x), N_I(x)$):**
    *   Activator neighborhood (symmetric, range 1): $N_A(x) = \{x-1, x+1\}$
    *   Inhibitor neighborhood (chiral, left-side range 3): $N_I(x) = \{x-3, x-2, x-1\}$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $a_t(x) = \sum_{y \in N_A(x)} \mathbb{I}(S_t(y) = 1)$ be the activator count.
    Let $i_t(x) = \sum_{y \in N_I(x)} \mathbb{I}(S_t(y) = 2)$ be the inhibitor count.
    *   If $s = 3$, it remains stable:
        $$S_{t+1}(x) = 3$$
    *   If $s = 4$, it decays:
        $$S_{t+1}(x) = 0$$
    *   If $s = 2$, it decays:
        $$S_{t+1}(x) = 4$$
    *   If $s = 1$, it matures:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } a_t(x) \ge 1 \\
        4 & \text{otherwise}
        \end{cases}$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } a_t(x) \ge 1 \text{ and } i_t(x) = 0 \\
        2 & \text{else if } S_t(x-1) = 1 \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** Activator ($1$) diffuses symmetrically, but the inhibitor ($2$) is transported asymmetrically (swept to the right, meaning cell $x$ only reads the inhibitor levels of its left neighbors $N_I(x)$). This chiral transport creates a periodic Turing pattern that is skewed to the right. The tissue differentiates into a permanent structure ($3$) trailing the active wave.
*   **Expected Visual Behavior:** Propagating waves of activator that periodically branch or split at regular intervals dictated by the inhibitor range, leaving behind a patterned differentiated structure (state 3) on the left.

### Rule 4: Sinuous Helical Circumnutation
*   **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
    *   State $0$: Quiescent space.
    *   State $1$: Right-growing Tip.
    *   State $2$: Left-growing Tip.
    *   State $3$: Right-to-Left Transition.
    *   State $4$: Left-to-Right Transition.
    *   State $5$: Permanent Stem.
*   **Neighborhoods ($N_L(x), N_R(x)$):**
    *   Left-trail neighborhood: $N_L(x) = \{x-3, x-2, x-1\}$
    *   Right-trail neighborhood: $N_R(x) = \{x+1, x+2, x+3\}$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $C_L(x) = \sum_{y \in N_L(x)} \mathbb{I}(S_t(y) = 5)$ be the count of stems on the left.
    Let $C_R(x) = \sum_{y \in N_R(x)} \mathbb{I}(S_t(y) = 5)$ be the count of stems on the right.
    *   If $s = 5$, it remains stable:
        $$S_{t+1}(x) = 5$$
    *   If $s \in \{3, 4\}$, it becomes stem:
        $$S_{t+1}(x) = 5$$
    *   If $s = 1$:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } C_L(x) \ge 2 \\
        5 & \text{otherwise}
        \end{cases}$$
    *   If $s = 2$:
        $$S_{t+1}(x) = \begin{cases}
        4 & \text{if } C_R(x) \ge 2 \\
        5 & \text{otherwise}
        \end{cases}$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ and } C_L(x-1) < 2 \\
        2 & \text{else if } S_t(x+1) = 2 \text{ and } C_R(x+1) < 2 \\
        2 & \text{else if } S_t(x+1) = 3 \\
        1 & \text{else if } S_t(x-1) = 4 \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** The growth tip moves in one direction ($1$ moves right, $2$ moves left), depositing permanent stem cells ($5$) behind it. It tracks the length of its stem trail. When the trail length reaches the threshold ($\ge 2$ stems in the trailing neighborhood), the tip undergoes a transition ($3$ or $4$) that swaps its growth chirality, causing it to grow in the opposite direction.
*   **Expected Visual Behavior:** A single growth front that oscillates left and right, leaving behind a solid stem and tracing a beautiful, regular zig-zag pattern (sinuous/helical path) in the space-time diagram.

### Rule 5: Asymmetric Stem Cell Niche
*   **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
    *   State $0$: Quiescent / Empty space.
    *   State $1$: Stem Cell (active divider).
    *   State $2$: Niche Signal (permanent anchor).
    *   State $3$: Progenitor Cell (transit amplifying).
    *   State $4$: Differentiated Tissue.
    *   State $5$: Senescent Cell (refractory).
*   **Neighborhood ($N(x)$):** Radius $r=1$:
    $$N(x) = \{x-1, x+1\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $d_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 4)$ be the count of differentiated neighbors.
    *   If $s = 2$, it remains stable:
        $$S_{t+1}(x) = 2$$
    *   If $s = 1$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 2 \\
        3 & \text{otherwise}
        \end{cases}$$
    *   If $s = 3$, it becomes differentiated:
        $$S_{t+1}(x) = 4$$
    *   If $s = 4$:
        $$S_{t+1}(x) = \begin{cases}
        5 & \text{if } d_t(x) = 2 \text{ (contact inhibition due to overcrowding)} \\
        4 & \text{otherwise}
        \end{cases}$$
    *   If $s = 5$, it decays:
        $$S_{t+1}(x) = 0$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } S_t(x-1) = 3 \\
        3 & \text{else if } S_t(x-1) = 1 \text{ and } S_t(x-2) = 2 \text{ (asymmetric division)} \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** The stem cell ($1$) divides asymmetrically, producing a progenitor ($3$) only to its right because the niche ($2$) is on its left. The progenitor ($3$) migrates right and matures to tissue ($4$). Overcrowding of tissue ($4$) triggers contact inhibition, turning it to senescent ($5$) and then clearing space ($0$), leading to dynamic tissue self-renewal.
*   **Expected Visual Behavior:** A fixed niche point on the left generating a continuous rightward stream of differentiated cells (state 4). Overcrowding causes periodic waves of apoptosis (state 5 and 0), creating a striped pattern of tissue segments that periodically collapse and regenerate.

### Rule 6: Vascular Lumen Formation
*   **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
    *   State $0$: Quiescent / Lumen (empty interior).
    *   State $1$: Proliferating Tip (active growth front).
    *   State $2$: Endothelial Wall (differentiated tissue).
    *   State $3$: Apoptotic Trigger (hollowing process).
    *   State $4$: Refractory/Decaying.
*   **Neighborhood ($N(x)$):** Radius $r=1$:
    $$N(x) = \{x-1, x+1\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $w_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ be the count of wall neighbors.
    *   If $s = 1$:
        $$S_{t+1}(x) = \begin{cases}
        2 & \text{if } S_t(x+1) \neq 0 \text{ (contact-inhibited tip)} \\
        1 & \text{otherwise}
        \end{cases}$$
    *   If $s = 2$:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } w_t(x) = 2 \text{ (core tissue apoptosis to hollow the vessel)} \\
        2 & \text{otherwise}
        \end{cases}$$
    *   If $s = 3$, it decays to refractory:
        $$S_{t+1}(x) = 4$$
    *   If $s = 4$, it becomes lumen:
        $$S_{t+1}(x) = 0$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 0 \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** A tip cell ($1$) grows to the right. When it meets a barrier, it differentiates to wall cells ($2$). To form a hollow vessel (lumen), the internal cells of the tissue (surrounded by walls on both sides, $w_t=2$) undergo programmed cell death (apoptosis, $2 \to 3 \to 4 \to 0$). Chirality is expressed by the growth direction of the tip (always to the right).
*   **Expected Visual Behavior:** A hollow double-walled tube (two parallel lines of state 2) propagating diagonally in space-time, with a growing tip (state 1) at the front and a hollow core (state 0) cleared by apoptosis (states 3 and 4) in the center.

### Rule 7: Morphogenetic French Flag Wave
*   **States ($N$):** $7$ states ($0, 1, 2, 3, 4, 5, 6$).
    *   State $0$: Undifferentiated ectoderm.
    *   State $1$: Apical Organizer (stable morphogen source).
    *   State $2$: Morphogen Concentration High.
    *   State $3$: Morphogen Concentration Medium.
    *   State $4$: Mesoderm (differentiated type 1).
    *   State $5$: Endoderm (differentiated type 2).
    *   State $6$: Neural crest (differentiated type 3).
*   **Neighborhood ($N(x)$):** Left-only asymmetric neighborhood of radius $r=1$:
    $$N(x) = \{x-1\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    *   If $s = 1$, it remains stable:
        $$S_{t+1}(x) = 1$$
    *   If $s \in \{4, 5, 6\}$, the differentiated state is permanent:
        $$S_{t+1}(x) = s$$
    *   If $s = 2$, it decays to medium:
        $$S_{t+1}(x) = 3$$
    *   If $s = 3$, it differentiates based on the upstream neighbor:
        $$S_{t+1}(x) = \begin{cases}
        4 & \text{if } S_t(x-1) \in \{2, 3\} \\
        5 & \text{else if } S_t(x-1) = 4 \\
        6 & \text{else if } S_t(x-1) = 5 \\
        0 & \text{otherwise}
        \end{cases}$$
    *   If $s = 0$, it absorbs morphogen from the left:
        $$S_{t+1}(x) = \begin{cases}
        2 & \text{if } S_t(x-1) \in \{1, 2\} \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** Morphogen flows from left to right. The cell differentiates based on the state of its left neighbor when it receives the medium morphogen ($3$). This creates sequential, chirally asymmetric stripes of tissue types ($4$, then $5$, then $6$) moving rightwards from the organizer ($1$).
*   **Expected Visual Behavior:** Concentric, tri-color bands of differentiated tissue (states 4, 5, 6) that grow and expand to the right of a fixed organizer (state 1).

### Rule 8: Polar Filament Dynamic Instability
*   **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
    *   State $0$: Free Monomer pool.
    *   State $1$: Plus-End (fast growing tip).
    *   State $2$: Minus-End (slow growing/anchored tip).
    *   State $3$: Stable Filament Core.
    *   State $4$: Catastrophe (depolymerization wave).
    *   State $5$: Refractory Monomer.
*   **Neighborhood ($N(x)$):** Radius $r=2$:
    $$N(x) = \{x-2, x-1, x+1, x+2\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    *   If $s \in \{1, 2\}$, it becomes stable core:
        $$S_{t+1}(x) = 3$$
    *   If $s = 4$, it becomes refractory:
        $$S_{t+1}(x) = 5$$
    *   If $s = 5$, it becomes free monomer:
        $$S_{t+1}(x) = 0$$
    *   If $s = 3$:
        $$S_{t+1}(x) = \begin{cases}
        4 & \text{if } S_t(x-1) = 4 \text{ or } S_t(x+1) = 4 \text{ (catastrophe propagation)} \\
        4 & \text{else if } S_t(x-1) = 0 \text{ and } S_t(x+1) = 0 \text{ (isolated core degrades)} \\
        3 & \text{otherwise}
        \end{cases}$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ (rapid growth at plus end to the right)} \\
        2 & \text{else if } S_t(x+1) = 2 \text{ and } S_t(x+2) = 3 \text{ (slow anchored growth at minus end)} \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** The filament grows asymmetrically: rapid plus-end growth to the right ($1$ cell/step), and anchored minus-end growth to the left only if supported by the core. Loss of capping tips leads to catastrophic depolymerization ($4$) propagating through the core.
*   **Expected Visual Behavior:** Diagonal growth of stable core (state 3) which is periodically interrupted by catastrophic depolymerization waves (state 4), causing segments of the filament to dissolve back to monomers.

### Rule 9: Chiral Biofilm Shear Expansion
*   **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
    *   State $0$: Nutrients (quiescent substrate).
    *   State $1$: Expanding Edge (growth front).
    *   State $2$: Active Biofilm Interior.
    *   State $3$: Starved Interior.
    *   State $4$: Sliding Shear (chiral slide).
    *   State $5$: Depleted Necrotic Matrix.
*   **Neighborhood ($N(x)$):** Radius $r=2$:
    $$N(x) = \{x-2, x-1, x+1, x+2\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $n_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 0)$ be the local nutrient count.
    *   If $s \in \{1, 4\}$, it becomes active interior:
        $$S_{t+1}(x) = 2$$
    *   If $s = 2$:
        $$S_{t+1}(x) = \begin{cases}
        3 & \text{if } n_t(x) = 0 \text{ (nutrients depleted)} \\
        2 & \text{otherwise}
        \end{cases}$$
    *   If $s = 3$, it becomes necrotic:
        $$S_{t+1}(x) = 5$$
    *   If $s = 5$, it remains stable:
        $$S_{t+1}(x) = 5$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ (expansion to the right)} \\
        4 & \text{else if } S_t(x+1) = 1 \text{ and } S_t(x+2) \neq 0 \text{ (chiral shear to the left)} \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** Biofilm grows into nutrient-rich space ($0$). Growth is chiral: expansion to the right is fast (state 1), while expansion to the left is slow and goes through a shear phase (state 4) only if anchored. Depletion of local nutrients leads to necrotic core formation ($5$).
*   **Expected Visual Behavior:** Asymmetrical expansion patterns where the right edge is sharp and fast-growing, while the left edge is fuzzy and slow-growing. The center of the biofilm decays into a permanent necrotic zone (state 5).

### Rule 10: Asymmetric Mycelial Branching
*   **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
    *   State $0$: Nutrient-rich substrate.
    *   State $1$: Primary Hyphal Tip (grows right).
    *   State $2$: Sub-apical branching hub.
    *   State $3$: Mature hypha (active transport).
    *   State $4$: Senescent hypha (decaying).
    *   State $5$: Necrotic empty space.
*   **Neighborhood ($N(x)$):** Radius $r=2$:
    $$N(x) = \{x-2, x-1, x+1, x+2\}$$
*   **Transition Function:**
    Let $s = S_t(x)$.
    Let $T_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ be the active tip count.
    *   If $s = 1$, it becomes sub-apical:
        $$S_{t+1}(x) = 2$$
    *   If $s = 2$, it becomes mature:
        $$S_{t+1}(x) = 3$$
    *   If $s = 3$:
        $$S_{t+1}(x) = \begin{cases}
        4 & \text{if } T_t(x) = 0 \text{ (senesces when disconnected from active tips)} \\
        3 & \text{otherwise}
        \end{cases}$$
    *   If $s = 4$, it becomes necrotic:
        $$S_{t+1}(x) = 5$$
    *   If $s = 5$, it remains stable:
        $$S_{t+1}(x) = 5$$
    *   If $s = 0$:
        $$S_{t+1}(x) = \begin{cases}
        1 & \text{if } S_t(x-1) = 1 \text{ (main hyphal growth right)} \\
        1 & \text{else if } S_t(x+1) = 2 \text{ and } S_t(x+2) = 3 \text{ (asymmetric lateral branch left)} \\
        0 & \text{otherwise}
        \end{cases}$$
*   **Mathematical Rationale:** Main hypha grows to the right (state 1). Sub-apical hubs (2) sprout lateral branches to the left (state 1) only if supported by mature hyphae (3). Disconnected mature hyphae undergo senescence (4) and necrosis (5), mimicking the expansion of ring-like mycelial colonies.
*   **Expected Visual Behavior:** A growing tree-like branching network in space-time that extends primarily to the right, with secondary branches growing to the left, and a decaying center that clears out behind the growth front.
