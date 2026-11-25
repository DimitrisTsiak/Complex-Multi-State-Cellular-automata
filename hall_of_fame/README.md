# Hall of Fame

The 30 rules from the showcase GIF, ported from their original loop scripts to the shared engine. Each port has the same dynamics, starting rows, cell data types and colours as its original. Only the source of randomness changed: the ports draw from the engine's seeded `rng` instead of `np.random`, so every image here can be regenerated exactly.

```bash
python -m ca_core run hall_of_fame                       # renders output/rule_01_*.png ... rule_30_*.png
python -m ca_core run hall_of_fame --width 1600 --steps 1600   # larger renders
```

The order follows `gif_showcase.py`; image `rule_NN` is entry NN below. The original showcase images are kept in [`../showcase/`](../showcase/).

## How faithful the ports are

- **Identical to the showcase image** (11): deterministic rules picked from a single seed. A normal run reproduces the original image pixel for pixel.
- **Same rule, new random start** (8): deterministic rules picked from a random start. Replaying the port from the original image's first row reproduces the original pixel for pixel. A normal run starts from a new random row, so the image differs in detail.
- **Same rule, new randomness** (11): stochastic rules. With the same random numbers as the original code, the port produces identical images (checked for both starts on three seeds). The engine's random numbers differ from the original's unseeded or global ones, so the image differs in detail.

Two picks needed small, behaviour-preserving changes: loop 20's rules 5 and 6 are vectorised versions of the original per-cell Python loops. Rules whose noise level depended on the start (loop 22 rule 7, loop 25 rules 1 and 8) carry that level as a hidden part of the state.

| # | Loop | Rule | Name | Showcase start | Hall-of-fame image |
|---|---|---|---|---|---|
| 01 | 1 | 4 | Staged Excitation Cascade | random | same rule, new random start |
| 02 | 2 | 2 | Parity-Gated Birth Generations | random | same rule, new random start |
| 03 | 2 | 4 | Chiral Drifting Generations | random | same rule, new random start |
| 04 | 2 | 7 | Totalistic-Sum Generations | single seed | identical to the showcase image |
| 05 | 3 | 8 | Anomalous Fractional Diffusion Wave | single seed | identical to the showcase image |
| 06 | 6 | 1 | Clamped Advection-Diffusion | random | same rule, new random start |
| 07 | 8 | 1 | Discrete Hadamard Walk | random | same rule, new random start |
| 08 | 8 | 2 | Quantum Tunneling & Scattering | random | same rule, new random start |
| 09 | 9 | 8 | Class Struggle and Elite Overproduction | single seed | identical to the showcase image |
| 10 | 10 | 8 | Arnold's Cat Map Lattice | single seed | identical to the showcase image |
| 11 | 11 | 3 | Directed Percolation | random | same rule, new randomness |
| 12 | 25 | 8 | Stochastic Neuronal Avalanche | random | same rule, new randomness |
| 13 | 11 | 5 | Noisy Majority | random | same rule, new randomness |
| 14 | 12 | 2 | Gravitational Wave Interferometer | single seed | identical to the showcase image |
| 15 | 12 | 4 | Gravitational Redshift (Time Dilation) | random | same rule, new randomness |
| 16 | 13 | 4 | Spinfoam Amplitude Sum-Over-Histories | random | same rule, new random start |
| 17 | 13 | 10 | Chiral Immirzi Asymmetry | single seed | identical to the showcase image |
| 18 | 14 | 3 | Calabi-Yau Dimension Compactification | single seed | identical to the showcase image |
| 19 | 14 | 7 | Holographic Boundary-to-Bulk Projection (AdS/CFT) | single seed | identical to the showcase image |
| 20 | 15 | 9 | Quantum-Coherent Extremophile | random | same rule, new random start |
| 21 | 17 | 9 | Symbiotic Subversion (Mutualistic Hijacking) | single seed | identical to the showcase image |
| 22 | 20 | 5 | Non-Euclidean Thermal Wormhole | single seed | identical to the showcase image |
| 23 | 20 | 6 | Möbius Boundary Twist | single seed | identical to the showcase image |
| 24 | 22 | 7 | Dissipative Decoherence in a Thermal Bath | single seed | same rule, new randomness |
| 25 | 23 | 7 | Recombination-Driven Zoonotic Spillover | single seed | same rule, new randomness |
| 26 | 23 | 5 | Viroid Hyperparasitism | random | same rule, new randomness |
| 27 | 24 | 1 | Stochastic Vicsek-1D Flocking | single seed | same rule, new randomness |
| 28 | 24 | 2 | Multi-Angle Filament Alignment | single seed | same rule, new randomness |
| 29 | 24 | 9 | Active Matter Phase Transition | single seed | same rule, new randomness |
| 30 | 25 | 1 | Stochastic Sandpile Cascade | single seed | same rule, new randomness |
