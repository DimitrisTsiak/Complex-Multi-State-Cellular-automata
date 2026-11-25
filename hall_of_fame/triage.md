# Triage: hall_of_fame

Automatic quality gate written by `python -m ca_core triage` from the images in `output/`. Re-run it after any change. It is a guide for the reviewer, not a verdict on beauty.

**Gate:** 24 pass, 6 need review, 0 need rework

| Rule | Name | single_seed | random | Gate |
|---|---|---|---|---|
| 01 | Loop 1 Rule 4: Staged Excitation Cascade | FAIL dead: single colour from row 141/800 | WARN periodic: repeats every 8 rows from row 26/800 | REVIEW |
| 02 | Loop 2 Rule 2: Parity-Gated Birth Generations | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 03 | Loop 2 Rule 4: Chiral Drifting Generations | WARN translating: rigid pattern moving +1 cells per 1 rows from row 2/800 | PASS dynamic: aperiodic and structured | PASS |
| 04 | Loop 2 Rule 7: Totalistic-Sum Generations | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 05 | Loop 3 Rule 8: Anomalous Fractional Diffusion Wave | WARN periodic: repeats every 8 rows from row 597/800 | PASS dynamic: aperiodic and structured | PASS |
| 06 | Loop 6 Rule 1: Clamped Advection-Diffusion | WARN translating: rigid pattern moving -1 cells per 1 rows from row 6/800 | WARN translating: rigid pattern moving -1 cells per 1 rows from row 6/800 | REVIEW |
| 07 | Loop 8 Rule 1: Discrete Hadamard Walk | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 08 | Loop 8 Rule 2: Quantum Tunneling & Scattering | WARN near-static: only ~2.0 cells change per row | PASS dynamic: aperiodic and structured | PASS |
| 09 | Loop 9 Rule 8: Class Struggle and Elite Overproduction | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 10 | Loop 10 Rule 8: Arnold's Cat Map Lattice | PASS dynamic: aperiodic and structured | WARN noise: close to random noise (compression 1.00) | PASS |
| 11 | Loop 11 Rule 3: Directed Percolation | FAIL dead: single colour from row 13/800 | PASS dynamic: aperiodic and structured | PASS |
| 12 | Loop 25 Rule 8: Stochastic Neuronal Avalanche | WARN near-static: only ~3.1 cells change per row | PASS dynamic: aperiodic and structured | PASS |
| 13 | Loop 11 Rule 5: Noisy Majority | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 14 | Loop 12 Rule 2: Gravitational Wave Interferometer | PASS dynamic: aperiodic and structured | WARN noise: close to random noise (compression 0.91) | PASS |
| 15 | Loop 12 Rule 4: Gravitational Redshift (Time Dilation) | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 16 | Loop 13 Rule 4: Spinfoam Amplitude Sum-Over-Histories | FAIL dead: single colour from row 1/800 | PASS dynamic: aperiodic and structured | PASS |
| 17 | Loop 13 Rule 10: Chiral Immirzi Asymmetry | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 18 | Loop 14 Rule 3: Calabi-Yau Dimension Compactification | WARN noise: close to random noise (compression 0.91) | WARN noise: close to random noise (compression 0.96) | REVIEW |
| 19 | Loop 14 Rule 7: Holographic Boundary-to-Bulk Projection (AdS/CFT) | PASS dynamic: aperiodic and structured | WARN noise: close to random noise (compression 0.98) | PASS |
| 20 | Loop 15 Rule 9: Quantum-Coherent Extremophile | FAIL frozen: static from row 3/800 | PASS dynamic: aperiodic and structured | PASS |
| 21 | Loop 17 Rule 9: Symbiotic Subversion (Mutualistic Hijacking) | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 22 | Loop 20 Rule 5: Non-Euclidean Thermal Wormhole | WARN noise: close to random noise (compression 1.00) | WARN noise: close to random noise (compression 1.00) | REVIEW |
| 23 | Loop 20 Rule 6: Möbius Boundary Twist | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 24 | Loop 22 Rule 7: Dissipative Decoherence in a Thermal Bath | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 25 | Loop 23 Rule 7: Recombination-Driven Zoonotic Spillover | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 26 | Loop 23 Rule 5: Viroid Hyperparasitism | WARN dead: single colour from row 482/800 | FAIL dead: single colour from row 388/800 | REVIEW |
| 27 | Loop 24 Rule 1: Stochastic Vicsek-1D Flocking | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 28 | Loop 24 Rule 2: Multi-Angle Filament Alignment | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 29 | Loop 24 Rule 9: Active Matter Phase Transition | PASS dynamic: aperiodic and structured | PASS dynamic: aperiodic and structured | PASS |
| 30 | Loop 25 Rule 1: Stochastic Sandpile Cascade | WARN near-static: only ~0.9 cells change per row | WARN dead: single colour from row 572/800 | REVIEW |

## Metrics

Computed on the last rows of each image. Activity: share of cells that change per step. Compression: zlib size relative to the same cells shuffled (about 1.0 means noise-like). Settle row: first row of the final dead, frozen or periodic regime.

| Image | Label | Activity | Compression | Entropy (bits) | Period | Shift | Settle row |
|---|---|---|---|---|---|---|---|
| rule 01 single_seed | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 141 |
| rule 01 random | periodic | 1.0 | 0.048 | 3.0 | 8 | 0 | 26 |
| rule 02 single_seed | dynamic | 0.5719 | 0.692 | 2.128 |  |  |  |
| rule 02 random | dynamic | 0.5687 | 0.703 | 2.124 |  |  |  |
| rule 03 single_seed | translating | 0.005 | 0.287 | 0.042 | 1 | 1 | 2 |
| rule 03 random | dynamic | 0.4437 | 0.59 | 1.757 |  |  |  |
| rule 04 single_seed | dynamic | 0.5832 | 0.795 | 2.095 |  |  |  |
| rule 04 random | dynamic | 0.6658 | 0.87 | 2.194 |  |  |  |
| rule 05 single_seed | periodic | 0.674 | 0.033 | 2.475 | 8 | 0 | 597 |
| rule 05 random | dynamic | 0.7086 | 0.49 | 2.537 |  |  |  |
| rule 06 single_seed | translating | 0.0175 | 0.149 | 0.089 | 1 | -1 | 6 |
| rule 06 random | translating | 0.765 | 0.027 | 2.218 | 1 | -1 | 6 |
| rule 07 single_seed | dynamic | 0.9976 | 0.04 | 2.496 |  |  |  |
| rule 07 random | dynamic | 0.8825 | 0.862 | 3.169 |  |  |  |
| rule 08 single_seed | near-static | 0.0025 | 0.317 | 0.085 |  |  |  |
| rule 08 random | dynamic | 0.789 | 0.17 | 2.423 |  |  |  |
| rule 09 single_seed | dynamic | 0.8631 | 0.043 | 2.289 |  |  |  |
| rule 09 random | dynamic | 0.997 | 0.035 | 2.322 |  |  |  |
| rule 10 single_seed | dynamic | 0.8322 | 0.308 | 3.719 |  |  |  |
| rule 10 random | noise | 0.9388 | 0.998 | 4.0 |  |  |  |
| rule 11 single_seed | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 13 |
| rule 11 random | dynamic | 0.4938 | 0.883 | 0.995 |  |  |  |
| rule 12 single_seed | near-static | 0.0039 | 0.054 | 1.484 |  |  |  |
| rule 12 random | dynamic | 0.1952 | 0.608 | 2.018 |  |  |  |
| rule 13 single_seed | dynamic | 0.0642 | 0.829 | 0.444 |  |  |  |
| rule 13 random | dynamic | 0.0665 | 0.845 | 0.417 |  |  |  |
| rule 14 single_seed | dynamic | 0.2634 | 0.058 | 1.231 |  |  |  |
| rule 14 random | noise | 0.8541 | 0.914 | 3.28 |  |  |  |
| rule 15 single_seed | dynamic | 0.0051 | 0.074 | 1.042 |  |  |  |
| rule 15 random | dynamic | 0.0086 | 0.064 | 2.979 |  |  |  |
| rule 16 single_seed | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 1 |
| rule 16 random | dynamic | 0.5749 | 0.725 | 2.036 |  |  |  |
| rule 17 single_seed | dynamic | 0.81 | 0.895 | 2.203 |  |  |  |
| rule 17 random | dynamic | 0.8126 | 0.887 | 2.203 |  |  |  |
| rule 18 single_seed | noise | 0.8111 | 0.908 | 2.943 |  |  |  |
| rule 18 random | noise | 0.8539 | 0.956 | 3.403 |  |  |  |
| rule 19 single_seed | dynamic | 0.4104 | 0.295 | 2.342 |  |  |  |
| rule 19 random | noise | 0.7106 | 0.976 | 3.204 |  |  |  |
| rule 20 single_seed | frozen | 0.0 | 0.44 | 0.025 | 1 | 0 | 3 |
| rule 20 random | dynamic | 0.2628 | 0.636 | 1.401 |  |  |  |
| rule 21 single_seed | dynamic | 0.7252 | 0.507 | 2.19 |  |  |  |
| rule 21 random | dynamic | 0.7434 | 0.35 | 2.186 |  |  |  |
| rule 22 single_seed | noise | 0.9168 | 1.001 | 3.585 |  |  |  |
| rule 22 random | noise | 0.9167 | 1.0 | 3.585 |  |  |  |
| rule 23 single_seed | dynamic | 1.0 | 0.099 | 1.856 |  |  |  |
| rule 23 random | dynamic | 0.9938 | 0.473 | 1.872 |  |  |  |
| rule 24 single_seed | dynamic | 0.0203 | 0.371 | 0.912 |  |  |  |
| rule 24 random | dynamic | 0.1196 | 0.739 | 1.702 |  |  |  |
| rule 25 single_seed | dynamic | 0.1552 | 0.439 | 1.366 |  |  |  |
| rule 25 random | dynamic | 0.2798 | 0.693 | 1.755 |  |  |  |
| rule 26 single_seed | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 482 |
| rule 26 random | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 388 |
| rule 27 single_seed | dynamic | 0.1054 | 0.7 | 1.149 |  |  |  |
| rule 27 random | dynamic | 0.1062 | 0.691 | 1.151 |  |  |  |
| rule 28 single_seed | dynamic | 0.1445 | 0.452 | 1.965 |  |  |  |
| rule 28 random | dynamic | 0.1432 | 0.596 | 1.187 |  |  |  |
| rule 29 single_seed | dynamic | 0.3916 | 0.73 | 2.157 |  |  |  |
| rule 29 random | dynamic | 0.3905 | 0.725 | 2.158 |  |  |  |
| rule 30 single_seed | near-static | 0.0011 | 0.107 | 0.715 |  |  |  |
| rule 30 random | dead | 0.0 | 1.0 | -0.0 | 1 | 0 | 572 |

## Legend

- **PASS**: aperiodic and structured to the end of the run.
- **WARN**: periodic, translating, near-static, noise-like, or dead/frozen only after the halfway row. Can still be a winner; look at it.
- **FAIL**: dead or frozen before the halfway row, so most of the image is trivial.
- **ERROR**: the rule raised an exception or the image is missing.
- Gate **REWORK**: no image of the rule is better than FAIL. **REVIEW**: best image is a WARN.
