# Loop 21 Cellular Automata Rules: Alien Linguistics, Hieroglyphic Syntax & Glyphs

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Alien Linguistics, Hieroglyphic Syntax & Glyphs**. 

These rules model structural linguistic constraints, self-assembling sentences or runes, syntax-driven information propagation, error-correction mechanisms, mirror-symmetrical palindrome growth, and contextual reconstruction of corrupted scripts. Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The space-time configurations of these systems simulate the emergence of syntax and grammar from local interactions.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Chomsky Syntactic Drift](#rule-1-chomsky-syntactic-drift) | 6 | Radius $r=1$ | Context-free grammar production tree expansion | Branching inverted-V shapes stabilizing into terminal pairs |
| **2** | [Semitic Triliteral Vocalization](#rule-2-semitic-triliteral-vocalization) | 6 | Radius $r=2$ | Dynamic vowels binding static consonants into words | Propagating waves freezing upon striking ordered consonant slots |
| **3** | [Dyck Language Nested Clause Symmetry](#rule-3-dyck-language-nested-clause-symmetry) | 5 | Radius $r=1$ | Parenthesis matching and nested clause resolution | Inward-contracting tension zones collapsing into stable harmonic bands |
| **4** | [Graphemic Rune Self-Assembly](#rule-4-graphemic-rune-self-assembly) | 5 | Radius $r=2$ | Symmetrical wing components binding to a central nucleus | Converging lines fusing into thick, stationary glyph cores |
| **5** | [Anisotropic Grammatical Waveguide](#rule-5-anisotropic-grammatical-waveguide) | 5 | Radius $r=1$ | Signal propagation guided strictly by NP-VP transitions | Wave packets propagating rightward along localized syntactic borders |
| **6** | [Phonotactic Vowel Epenthesis](#rule-6-phonotactic-vowel-epenthesis) | 4 | Radius $r=1$ | Insertion of vowels to break forbidden consonant clusters | Checkerboard-like syllable clusters resolving into uniform bands |
| **7** | [Syntactic Immune System](#rule-7-syntactic-immune-system) | 5 | Radius $r=1$ | Stranded modifiers triggering error-annihilation sweeps | Localized error nodes triggering outward-propagating clearing waves |
| **8** | [Case-Marking Concord Gravity](#rule-8-case-marking-concord-gravity) | 6 | Radius $r=1$ | Mobile case markers mediating noun-adjective agreement | Drifting particles converging to lock static elements into solid fields |
| **9** | [Graphemic Tense Tunneling](#rule-9-graphemic-tense-tunneling) | 5 | Radius $r=2$ | Tense conjugator wave bypassing nouns to conjugate verbs | Constant-velocity wave sweeping through static arrays, shifting states |
| **10** | [Orthographic Codex Reconstruction](#rule-10-orthographic-codex-reconstruction) | 5 | Radius $r=2$ | Contextual scribe agents repairing corrupted glyph cells | Moving scribe entities restoring noise patterns into ordered scripts |

---

## Rule Definitions

### Rule 1: Chomsky Syntactic Drift
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Empty Space / Silenced Medium ($[\emptyset]$).
  * State $1$: Non-terminal Sentence Symbol ($S$).
  * State $2$: Non-terminal Noun Phrase ($NP$).
  * State $3$: Non-terminal Verb Phrase ($VP$).
  * State $4$: Terminal Noun ($n$).
  * State $5$: Terminal Verb ($v$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  $$S_{t+1}(x) = \begin{cases}
  2 & \text{if } s = 0 \text{ and } S_t(x+1) = 1 \\
  3 & \text{if } s = 0 \text{ and } S_t(x-1) = 1 \\
  4 & \text{if } s = 2 \\
  5 & \text{if } s = 3 \\
  0 & \text{if } s = 1 \\
  s & \text{otherwise}
  \end{cases}$$
* **Mathematical/Physical Rationale:** Models a context-free grammar production tree ($S \to NP + VP$, $NP \to n$, $VP \to v$) mapped directly onto a 1D spatial lattice. The sentence symbol $S$ acts as an unstable state that splits into left and right sub-components ($NP$ and $VP$), which then crystallize into stable terminal words ($n$ and $v$).
* **Expected Visual Behavior:** Starting from a single seed of state $1$, the cell decays and spawns state $2$ on the left and state $3$ on the right, which then instantly freeze into states $4$ and $5$. The resulting space-time diagram features a V-shaped bifurcation branching outwards and leaving behind a stable, grammatically valid $n \dots v$ boundary.

---

### Rule 2: Semitic Triliteral Vocalization
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Empty Space / Silence ($[\emptyset]$).
  * State $1$: First Radical Consonant ($C_1$).
  * State $2$: Second Radical Consonant ($C_2$).
  * State $3$: Third Radical Consonant ($C_3$).
  * State $4$: Vowel Wave ($V$).
  * State $5$: Crystallized Semantic Word Glyph ($W$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 5$:
    $$S_{t+1}(x) = 5$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x+1) = 4 \text{ and } S_t(x+2) = 2 \text{ and } S_t(x+3) = 4 \text{ and } S_t(x+4) = 3 \\
    0 & \text{else if } S_t(x+1) = 0 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-2) = 1 \text{ and } S_t(x-1) = 4 \text{ and } S_t(x+1) = 4 \text{ and } S_t(x+2) = 3 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-4) = 1 \text{ and } S_t(x-3) = 4 \text{ and } S_t(x-2) = 2 \text{ and } S_t(x-1) = 4 \\
    0 & \text{else if } S_t(x-1) = 0 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } (S_t(x-1) = 1 \lor S_t(x-1) = 5) \text{ and } (S_t(x+1) = 2 \lor S_t(x+1) = 5) \\
    5 & \text{else if } (S_t(x-1) = 2 \lor S_t(x-1) = 5) \text{ and } (S_t(x+1) = 3 \lor S_t(x+1) = 5) \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \text{ and } S_{t+1}(x) \neq 5 \\
    3 & \text{if } S_t(x+1) = 3 \text{ and } S_{t+1}(x) \neq 5 \\
    4 & \text{if } S_t(x-1) = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical/Physical Rationale:** Inspired by Semitic languages' triliteral root system, where meaning is stored in stable consonant skeletons ($C_1-C_2-C_3$) and activated by interdigitated vowels ($V$). The consonants are static (or slide together), while vowels propagate as transient waves. When a vowel wave correctly nests within the consonants (creating $C_1-V-C_2-V-C_3$), the whole block binds into a permanent semantic word $W$ (state 5).
* **Expected Visual Behavior:** Moving vowel lines (diagonal stripes of state 4) collide with static or slowly moving consonant tracks. Upon achieving correct alignment, a solid vertical block of state 5 forms instantly, representing a written codex entry.

---

### Rule 3: Dyck Language Nested Clause Symmetry
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Empty Medium ($[\emptyset]$).
  * State $1$: Clause Opener ($[_{L}$).
  * State $2$: Clause Closer ($]_{R}$).
  * State $3$: Syntactic Link / Tension Field ($T$).
  * State $4$: Resolved Clause / Semantic Harmony ($H$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) \neq 2 \\
    2 & \text{else if } S_t(x+1) = 2 \text{ and } S_t(x-1) \neq 1 \\
    3 & \text{else if } (S_t(x-1) = 1 \lor S_t(x-1) = 3) \text{ and } (S_t(x+1) = 2 \lor S_t(x+1) = 3) \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x+1) = 2 \text{ or } S_t(x+1) = 4 \\
    3 & \text{else if } S_t(x+1) = 0 \text{ or } S_t(x+1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 1 \text{ or } S_t(x-1) = 4 \\
    3 & \text{else if } S_t(x-1) = 0 \text{ or } S_t(x-1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 4 \text{ and } S_t(x+1) = 4 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 4$$
* **Mathematical/Physical Rationale:** Models parenthesis matching (Dyck language) in a physical space. Clause boundaries migrate toward each other, projecting a tension field $T$ between them. When they meet, they resolve into a stable state of grammatical harmony $H$. The resolution propagates outward, resolving outer nested clauses sequentially.
* **Expected Visual Behavior:** Converging pairs of diagonal boundaries (states 1 and 2) enclosing a filled triangular space-time region of state 3. When the boundaries meet, a solid block of state 4 nucleates and expands outwards, neutralizing the tension.

---

### Rule 4: Graphemic Rune Self-Assembly
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unstructured Medium ($[\emptyset]$).
  * State $1$: Left-wing Rune Component ($G_L$).
  * State $2$: Right-wing Rune Component ($G_R$).
  * State $3$: Static Rune Nucleus ($K$).
  * State $4$: Crystallized Sacred Rune ($C$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 4$:
    $$S_{t+1}(x) = 4$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 2 \\
    3 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x+1) = 3 \text{ and } S_t(x+2) = 2 \\
    0 & \text{else if } S_t(x+1) = 0 \text{ or } S_t(x+1) = 1 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 3 \text{ and } S_t(x-2) = 1 \\
    0 & \text{else if } S_t(x-1) = 0 \text{ or } S_t(x-1) = 2 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x) \neq 3 \\
    2 & \text{if } S_t(x+1) = 2 \text{ and } S_t(x) \neq 3 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical/Physical Rationale:** Models the self-assembly of complex multi-part glyphs from mobile semantic building blocks. Left-wing components drift right, and right-wing components drift left. The nucleus acts as a catalytic template; it binds both wing elements simultaneously to form a stable 3-cell crystallized rune ($C$). Unbalanced or mismatched elements do not trigger assembly.
* **Expected Visual Behavior:** Diagonal lines of states 1 and 2 converge on stationary lines of state 3. If they arrive at the same time, the junction freezes into a thick 3-pixel wide vertical column of state 4.

---

### Rule 5: Anisotropic Grammatical Waveguide
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Unstructured Substrate.
  * State $1$: Noun Phrase Path ($NP$).
  * State $2$: Verb Phrase Path ($VP$).
  * State $3$: Active Meaning Signal / Semantic Wave ($\psi$).
  * State $4$: Refractory / Spent Pathway.
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } s = 1 \text{ and } S_t(x-1) = 3 \text{ and } S_t(x+1) = 2 \\
  3 & \text{else if } s = 2 \text{ and } S_t(x-1) = 3 \\
  4 & \text{else if } s = 3 \\
  0 & \text{else if } s = 4 \\
  1 & \text{else if } s = 0 \text{ and } S_t(x-1) = 1 \\
  2 & \text{else if } s = 0 \text{ and } S_t(x+1) = 2 \\
  s & \text{otherwise}
  \end{cases}$$
* **Mathematical/Physical Rationale:** Models the anisotropic transmission of information through a grammatically organized medium. A meaning signal $\psi$ is allowed to step forward only if it transitions across a noun-phrase to verb-phrase junction ($NP \to VP$), which serves as a semantic conduit. The transmission leaves behind a temporary refractory trail (state 4) that resets the local grammar.
* **Expected Visual Behavior:** Light-colored wave packets (state 3) traveling rightward along the boundary where state 1 (left) and state 2 (right) meet, followed immediately by a thin trailing line of state 4.

---

### Rule 6: Phonotactic Vowel Epenthesis
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Silence / Ambient Space ($[\emptyset]$).
  * State $1$: Consonant ($C$).
  * State $2$: Vowel ($V$).
  * State $3$: Syntactically Harmonized Syllable ($H$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 3$:
    $$S_{t+1}(x) = 3$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 1 \\
    3 & \text{else if } S_t(x-1) = 2 \lor S_t(x+1) = 2 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x-1) = 1 \text{ and } S_t(x+1) = 1 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 0$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Simulates phonotactic grammar constraints: three adjacent consonants ($C-C-C$) are forbidden due to alien physical speech limitations, triggering the insertion of a vowel (vowel epenthesis) in the center cell. A sequence of consonant-vowel-consonant ($C-V-C$) represents a stable, harmonic syllable, which crystallizes into state $3$.
* **Expected Visual Behavior:** Start with dense clusters of state 1. The cells at regular intervals morph into state 2, creating alternating checkerboard patterns of 1s and 2s that rapidly lock into static, solid blocks of state 3.

---

### Rule 7: Syntactic Immune System
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Corrected / Quiescent Space.
  * State $1$: Substantive Word ($S$).
  * State $2$: Modifying Word ($M$).
  * State $3$: Syntax Error Node ($E$).
  * State $4$: Correction Sweep Wave ($D$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 4 \text{ or } S_t(x+1) = 4 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x+1) \neq 1 \text{ and } S_t(x+1) \neq 3 \\
    4 & \text{else if } S_t(x-1) = 4 \text{ or } S_t(x+1) = 4 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 4$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } (S_t(x-1) = 4 \text{ and } S_t(x+1) \neq 0) \lor (S_t(x+1) = 4 \text{ and } S_t(x-1) \neq 0) \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical/Physical Rationale:** Models the preservation of lexical integrity. Modifiers ($M$, state 2) must precede Substantives ($S$, state 1). If a modifier is left dangling or is adjacent to another modifier, it triggers a syntax error (state 3). The error node collapses into an active correction wave (state 4) that moves outward, wiping out the entire ungrammatical clause back to silence (state 0) to allow for re-writing.
* **Expected Visual Behavior:** Small static regions of modifiers and nouns. Mismatches create glowing nodes (state 3) that burst into diagonal lines of state 4, which propagate and consume nearby structures, resetting them to state 0.

---

### Rule 8: Case-Marking Concord Gravity
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Unmarked Space.
  * State $1$: Noun Core ($N$).
  * State $2$: Adjective Core ($A$).
  * State $3$: Case Marker Alpha ($\alpha$, left-drifting).
  * State $4$: Case Marker Beta ($\beta$, right-drifting).
  * State $5$: Saturated Concord ($C$).
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x+1) = 3 \text{ and } S_t(x-1) \neq 4 \\
    4 & \text{else if } S_t(x-1) = 4 \text{ and } S_t(x+1) \neq 3 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x+1) = 3 \\
    1 & \text{otherwise}
    \end{cases}$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-1) = 4 \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x-1) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } S_t(x+1) = 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 5$:
    $$S_{t+1}(x) = 5$$
* **Mathematical/Physical Rationale:** Models grammatical agreement (concord) as an attractive field. Mobile case markers ($\alpha$ and $\beta$) drift in opposite directions along the lattice. When they collide with their matching lexical heads (Alpha with Nouns, Beta with Adjectives), they lock them into a stable agreed-upon state (Concord, state 5). Mismatched collisions result in markers passing through or decaying.
* **Expected Visual Behavior:** Drifting diagonal lines (states 3 and 4) that terminate abruptly when they strike stationary vertical columns (states 1 and 2), transforming the columns into stable, glowing concord regions (state 5).

---

### Rule 9: Graphemic Tense Tunneling
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Neutral Medium.
  * State $1$: Noun (Conduit barrier).
  * State $2$: Verb - Present Tense ($V_{pres}$).
  * State $3$: Verb - Past Tense ($V_{past}$).
  * State $4$: Tense Shift Wave ($\tau$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 4 \\
    4 & \text{else if } S_t(x-1) = 1 \text{ and } S_t(x-2) = 4 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1$:
    $$S_{t+1}(x) = 1$$
  - If $s = 2$:
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } S_t(x-1) = 4 \text{ or } (S_t(x-1) = 1 \text{ and } S_t(x-2) = 4) \\
    2 & \text{otherwise}
    \end{cases}$$
  - If $s = 3$:
    $$S_{t+1}(x) = 3$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
* **Mathematical/Physical Rationale:** Models the selective conjugation of verbs by a propagating grammatical tense particle ($\tau$, state 4). The particle moves rightward through the lattice. When it encounters a noun (state 1), it passes through it (tunnels) without altering the noun's state. When it hits a present tense verb (state 2), it conjugates it to past tense (state 3) and continues its rightward sweep.
* **Expected Visual Behavior:** A single diagonal wave (state 4) sweeping across a set of stationary vertical lines representing words. The noun lines (state 1) remain unchanged as the wave tunnels through them, while verb lines (state 2) shift color to state 3 after the wave passes.

---

### Rule 10: Orthographic Codex Reconstruction
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Empty Space.
  * State $1$: Correct Glyph A ($G_A$).
  * State $2$: Correct Glyph B ($G_B$).
  * State $3$: Corrupted Glyph / Noise ($\xi$).
  * State $4$: Scribe / Restorer ($R$).
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
* **Transition Function:**
  Let $s = S_t(x)$ be the current state of cell $x$.
  - If $s = 3$:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x-1) = 4 \text{ and } S_t(x-2) = 2 \\
    2 & \text{else if } S_t(x-1) = 4 \text{ and } S_t(x-2) = 1 \\
    1 & \text{else if } S_t(x+1) = 4 \text{ and } S_t(x+2) = 2 \\
    2 & \text{else if } S_t(x+1) = 4 \text{ and } S_t(x+2) = 1 \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 4$:
    $$S_{t+1}(x) = 0$$
  - If $s = 0$:
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x-1) = 4 \text{ and } S_t(x+1) = 3 \\
    4 & \text{else if } S_t(x+1) = 4 \text{ and } S_t(x-1) = 3 \\
    4 & \text{else if } S_t(x-1) = 3 \text{ and } S_t(x+1) \in \{1, 2\} \\
    0 & \text{otherwise}
    \end{cases}$$
  - If $s = 1 \text{ or } s = 2$:
    $$S_{t+1}(x) = s$$
* **Mathematical/Physical Rationale:** Models the self-healing preservation of a sacred alternating orthography ($A-B-A-B$). Corrupted text (state 3) decays unless a scribe (state 4) arrives. When a scribe is adjacent to a corrupted cell, it checks the context on the other side of itself; if it detects an alternating sequence violation, it rewrites the corruption to the matching state to complete the pattern.
* **Expected Visual Behavior:** Random noise cells (state 3) are targeted by dynamic scribe packets (state 4) that home in on them. Once a scribe reaches a corrupted block, it disappears and leaves behind a restored alternating pattern of state 1 and state 2, stabilizing the script.
