# Cellular Automata Review Report: Biological Growth & Chiral Asymmetry (Loop 7)

This report reviews the 20 space-time diagrams generated in [loop_7/output/](file:///C:/programming/complex_cellular_automata/loop_7/output/) based on the 10 rules defined in [loop_7/rules.md](file:///C:/programming/complex_cellular_automata/loop_7/rules.md). Each rule is evaluated under two initial conditions: a **Single-Seed** (in the center) and a **Random** configuration.

---

## Executive Summary
The cellular automata rules in Loop 7 model biological growth processes (such as apical dominance, stem cell division, vascularization, and biofilm expansion) with an emphasis on **chiral asymmetry** (unidirectional or biased propagation). 

Through visual inspection of the space-time diagrams, the rules exhibit behaviors ranging from static frozen states (Class 1/2) to periodic propagating waves and complex boundary dynamics (Class 2/3 hybrids). The top 3 winner rules were selected based on their **visual complexity, structural emergent properties, and aesthetic appeal**:
1. **Rule 7: Morphogenetic French Flag Wave** (Winner) — Dynamic morphogen waves propagating within stable corridors.
2. **Rule 5: Asymmetric Stem Cell Niche** (Runner-up) — Striated, self-renewing tissue structures governed by contact inhibition.
3. **Rule 6: Vascular Lumen Formation** (Third Place) — Hollow channel development via localized apoptosis.

---

## Rule-by-Rule Visual Analysis

The following table summarizes the visual characteristics, classification, and aesthetic scores of all 10 rules.

| Rule # | Name | States ($N$) | Visual Complexity | Class | Aesthetic Score (1-10) | Key Visual Pattern |
|:---:|---|:---:|:---:|:---:|:---:|---|
| **1** | [Polar Auxin & Apical Dominance](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_01_random.png) | 5 | Low-Medium | 2 | 5/10 | Unidirectional wedge (single) and simple vertical stripes (random). |
| **2** | [Anchored Apical Growth](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_02_random.png) | 5 | Low | 2 | 4/10 | Sparse diagonal and vertical lines; mostly empty space. |
| **3** | [Chiral Turing Branching](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_03_random.png) | 5 | Low | 2 | 3/10 | Simple inverted V-shape (single) and thin vertical lines (random). |
| **4** | [Sinuous Helical Circumnutation](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_04_random.png) | 6 | Low | 1 | 2/10 | Aborts growth immediately; freezes into static vertical lines. |
| **5** | [Asymmetric Stem Cell Niche](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_05_random.png) | 6 | High | 2 | 8/10 | Highly organized, clean, striated green/black vertical bands. |
| **6** | [Vascular Lumen Formation](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_06_random.png) | 5 | Medium-High | 2 | 7/10 | Grid of hollow channels (lumens) and red walls. |
| **7** | [Morphogenetic French Flag Wave](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_07_random.png) | 7 | Outstanding | 2/3 | 10/10 | Propagating wave texture trapped in stable multi-colored corridors. |
| **8** | [Polar Filament Dynamic Instability](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_08_random.png) | 6 | Low | 1 | 3/10 | Fails to show catastrophes in single; freezes into a solid purple block. |
| **9** | [Chiral Biofilm Shear Expansion](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_09_random.png) | 6 | Low-Medium | 2 | 4/10 | Solid, flat olive-green wedge with lime edges; lacks internal texture. |
| **10** | [Asymmetric Mycelial Branching](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_10_random.png) | 6 | Low-Medium | 2 | 4/10 | Solid dark brown wedge with yellow borders; flat interior. |

---

## Detailed Analysis of Top 3 Winners

### 🥇 Winner: Rule 7 — Morphogenetic French Flag Wave
* **File Links:** [rule_07_single.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_07_single.png) | [rule_07_random.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_07_random.png)
* **Biological Mechanism:** Models morphogen flow (pink/orchid) from a fixed organizer (white) that drives multi-stage differentiation (dodger blue, tomato red, lime green).
* **Space-Time Diagram Analysis:**
  * *Single-Seed:* The single seed grows to the right, generating a repeating wave of morphogens (states 2 and 3) that propagates at a speed of 1 cell/step. The resulting space-time diagram shows a highly regular, diagonal pink/orchid striped pattern. Interestingly, because of the specific timing of the propagation wave, cells do not reach the threshold to stabilize into states 4, 5, or 6, but instead stay in a perpetual propagating cycle.
  * *Random Initial Conditions:* When initialized randomly, the stable differentiated states (4, 5, 6) present in the initial configuration remain frozen, forming solid vertical columns. The morphogen waves (2 and 3) propagate in the spaces (quiescent corridors) between these columns. They are blocked when they collide with stable cells, resulting in a beautiful visual of **dynamic wave propagation trapped inside static corridors**.
* **Aesthetics & Order vs. Chaos:** This rule is visually stunning. The file size of `rule_07_random.png` (106 KB) is 15–20 times larger than the other images, reflecting its high texture density and visual details. The contrast between the neon pink/orchid waves, the dark gray-blue background, and the solid blue/red/green columns produces a striking, high-frequency textile-like pattern.

### 🥈 Runner-up: Rule 5 — Asymmetric Stem Cell Niche
* **File Links:** [rule_05_single.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_05_single.png) | [rule_05_random.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_05_random.png)
* **Biological Mechanism:** Models an anchored stem cell niche (red-orange/gold) dividing asymmetrically to produce progenitor cells (blue), which migrate right, differentiate to tissue (green), and undergo contact-inhibited apoptosis (gray/black) under overcrowding.
* **Space-Time Diagram Analysis:**
  * *Single-Seed:* It forms a central vertical anchor (the niche) and a diagonal growing wedge to the right. Inside this wedge, a perfect grid of green (state 4) and black (state 0) vertical stripes emerges. This is because cells in the middle of a growing tissue segment become surrounded by other tissue cells, triggering apoptosis (turning 5, then 0), which leaves behind isolated, stable single-cell green columns.
  * *Random Initial Conditions:* The random starting grid is quickly cleaned up by contact inhibition, which acts as a spatial filter. The diagram resolves into extremely clean, regular, and evenly spaced vertical green/black stripes with small yellow/red highlights near the top.
* **Aesthetics & Order vs. Chaos:** The rule represents high-contrast, cyberpunk-themed order. The electric cyan/green lines on the pitch-black background look like a digital circuit board or a stylized barcode. It has excellent visual balance and mathematical precision.

### 🥉 Third Place: Rule 6 — Vascular Lumen Formation
* **File Links:** [rule_06_single.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_06_single.png) | [rule_06_random.png](file:///C:/programming/complex_cellular_automata/loop_7/output/rule_06_random.png)
* **Biological Mechanism:** Simulates vascularization, where a proliferating tip (bright red) grows right, leaving behind walls (dark red). When a wall cell is surrounded on both sides by other walls, it undergoes apoptosis (orange trigger, then dark gray, then black lumen) to hollow out the vessel.
* **Space-Time Diagram Analysis:**
  * *Single-Seed:* The single seed grows to the right, forming a diagonal wedge. Inside the wedge, a repeating wall-lumen-wall-lumen pattern develops. The interior is not completely hollowed out but resolves into alternating dark red vertical wall lines and black hollow channels.
  * *Random Initial Conditions:* It forms a dense, striated comb-like structure of vertical red wall lines and black lumens. 
* **Aesthetics & Order vs. Chaos:** The color palette (Vascular Blood) uses rich crimson, orange, and gray tones on black. The resulting space-time diagrams look organic, resembling muscular fibers, capillary networks, or comb structures. It perfectly demonstrates how local rules of contact-inhibition and apoptosis can form regular vascular structures.

---

## Symmetry-Breaking and Chirality
A key focus of this domain is **chiral asymmetry**. In all three winner rules, chirality is beautifully visualized:
* In **Rule 7**, the morphogen wave only propagates to the right, creating a unilateral diagonal texture.
* In **Rule 5**, the niche is anchored on the left and divisions are pushed exclusively to the right, creating a highly asymmetric wedge shape in the single-seed diagram.
* In **Rule 6**, vascular tips grow exclusively to the right, creating a distinct rightward-slanted growth front.

Rules that failed to manifest this chirality in an interesting way (e.g. Rules 4 and 8) quickly froze or aborted growth due to feedback loops that killed the active growth tips.

---

## Conclusion
The Loop 7 cellular automata simulations demonstrate the power of asymmetric local rules in creating organized global patterns. **Rule 7** stands out as the clear winner due to its outstanding visual texture and the complex interaction of static boundaries and dynamic morphogen waves. **Rule 5** and **Rule 6** are excellent runners-up, showcasing how biological mechanisms like contact inhibition and apoptosis can act as self-organizing spatial filters to create clean, striated, and functional space-time structures.
