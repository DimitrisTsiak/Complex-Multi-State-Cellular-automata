# Loop 6 Cellular Automata Review Report: Fluid & Convective Systems

This report provides a detailed visual, aesthetic, and physical analysis of the 20 space-time diagrams generated in `loop_6/output/`. The simulations consist of 10 distinct cellular automata rules, each evaluated under two initial conditions:
1. **Single active cell** (a localized high-energy perturbation in the center of a quiescent lattice).
2. **Random initial conditions** (a disordered, high-entropy initialization across the entire lattice).

---

## Individual Rule Analysis

### Rule 1: Clamped Advection-Diffusion
*   **Visual Observations (Single):** A single, highly defined diagonal stripe with a small gradient width that drifts to the left (top-center to bottom-left) and wraps around the boundaries periodically. It persists indefinitely without decaying.
*   **Visual Observations (Random):** A highly ordered, dense set of parallel diagonal stripes in vibrant shades of blue, cyan, green, and red drifting leftwards.
*   **Order vs. Chaos:** Extremely ordered. The system quickly self-organizes from random noise into a clean, laminar advective flow.
*   **Physics-to-Visual Link:** Discretizing the advection-diffusion equation usually leads to dispersion and decay. However, the sign-based gradient diffusion term acts as a non-linear restoring force. It holds the wave together, resulting in a stable, non-dispersive travelling wave (a **soliton** or **glider**) that propagates at a constant speed of 1 cell per step.
*   **Aesthetic Rating:** **9/10**. The resulting space-time diagrams are exceptionally clean, sharp, and showcase a beautiful laminar structure.

### Rule 2: Buoyancy Convective Plumes
*   **Visual Observations (Single):** The active cell dissipates almost immediately, leaving a completely black canvas.
*   **Visual Observations (Random):** A striking, high-contrast pattern of thin, parallel orange/red diagonal lines drifting leftwards against a deep black background.
*   **Order vs. Chaos:** Highly ordered after a transient phase. The system filters out all cold plumes (blue) and resolves into pure, non-decaying hot plumes.
*   **Physics-to-Visual Link:** This rule models hot (rising, left-moving) and cold (sinking, right-moving) plumes. Hot plumes are clamped to a minimum state of 1 (`val2 = np.maximum(1, S_right - 1)`), meaning they never decay to 0 on their own. Cold plumes decay to 0 (`cond4` maps state 3 to 0). Consequently, any cold fluid quickly dissipates or is annihilated by collisions with hot fluid. Once all cold fluid is gone, the surviving hot fluid flows leftward indefinitely without any opposing flow to trigger collisions.
*   **Aesthetic Rating:** **8.5/10**. The contrast of neon orange lines against a dark charcoal background is visually stunning.

### Rule 3: Rayleigh-Bénard Convective Cells
*   **Visual Observations (Single):** Dies out to black instantly.
*   **Visual Observations (Random):** A tiny, chaotic band of purple and green pixels at the very top (first 30 steps), which quickly fades into a completely black image.
*   **Order vs. Chaos:** Dissipative decay to a quiescent state.
*   **Physics-to-Visual Link:** The rule simulates velocity shear collisions forming vortex cores, which then decay and eject new flows. However, because there is no continuous external heating (buoyancy driving force) to pump energy back into the system, the kinetic energy of the initial state is lost to viscous dissipation and decay, bringing the lattice to complete rest.
*   **Aesthetic Rating:** **2/10**. The simulation is too short-lived to create any interesting visual structures.

### Rule 4: Compressible Gas Shockwaves
*   **Visual Observations (Single):** A single thin vertical magenta line on a dark violet background.
*   **Visual Observations (Random):** A static set of vertical stripes in shades of pink, magenta, and purple.
*   **Order vs. Chaos:** Frozen steady state. All dynamics freeze within 2–3 steps.
*   **Physics-to-Visual Link:** Cells accumulate pressure from neighbors and discharge when they exceed state 4. In both single and random conditions, once the initial discharging cells (states $\ge 4$) dump their energy and there are no remaining high-pressure cells to trigger further discharges, propagation stops, freezing the lattice.
*   **Aesthetic Rating:** **3/10**. Visually static and uninteresting.

### Rule 5: Viscous Drag & Shear Flow
*   **Visual Observations (Single):** Dies out to slate black immediately.
*   **Visual Observations (Random):** A frozen set of vertical stripes of slate, teal, and amber.
*   **Order vs. Chaos:** Frozen steady state.
*   **Physics-to-Visual Link:** Momentum is smoothed via local averaging. Since there is no advection term to move the velocity fields horizontally, the local average quickly reaches a spatial equilibrium, creating static vertical stripes where shear is too low to trigger turbulence.
*   **Aesthetic Rating:** **3/10**. Static and lacks movement.

### Rule 6: Surface Tension & Cohesion
*   **Visual Observations (Single):** Dissipates to black instantly.
*   **Visual Observations (Random):** A solid light blue block with a few thin vertical dark bands.
*   **Order vs. Chaos:** Frozen phase separation.
*   **Physics-to-Visual Link:** Liquid phases pull together (cohesion) and isolate gas phases. The cells quickly condense into large, static droplets (the light blue block) and gas voids, remaining completely motionless after the first step.
*   **Aesthetic Rating:** **2.5/10**. Low complexity and static.

### Rule 7: Thermohaline Circulation
*   **Visual Observations (Single):** A thin vertical orange line on a solid yellow background.
*   **Visual Observations (Random):** Static vertical stripes of yellow, orange, green, and teal.
*   **Order vs. Chaos:** Frozen steady state.
*   **Physics-to-Visual Link:** This double-diffusive convection rule shows brief diagonal advection at the very top, but because the salinity and temperature fields rapidly diffuse and average out, the system freezes into stable static layers.
*   **Aesthetic Rating:** **3.5/10**. Colorful but completely static.

### Rule 8: Kelvin-Helmholtz Instability
*   **Visual Observations (Single):** Dies out to a solid blue background.
*   **Visual Observations (Random):** A chaotic, multi-colored mixing layer at the very top (first 10–15 steps) displaying orange and pink vortex rolls. This layer quickly resolves into parallel diagonal stripes of blue and magenta drifting leftwards.
*   **Order vs. Chaos:** Organized dynamic flow. The chaotic shear instabilities resolve into a stable, uniform traveling wave.
*   **Physics-to-Visual Link:** The velocity difference across the interface triggers vortex roll-ups (state 7) and wave instabilities (state 6). These vortices relax and transfer momentum until the opposing velocity fields organize into a single, dominant direction. In this case, leftward flowing states (0, 1, 2) win out and propagate as a stable traveling wave train.
*   **Aesthetic Rating:** **8/10**. The transition from chaotic vortices at the top to clean, colorful diagonal stripes is visually compelling.

### Rule 9: Evaporative Convection (Marangoni)
*   **Visual Observations (Single):** Fades to black instantly.
*   **Visual Observations (Random):** A very thin band of colored noise at the top, fading to black by step 10.
*   **Order vs. Chaos:** Dissipative decay to zero.
*   **Physics-to-Visual Link:** Surfactant spreads from low to high surface tension. Since the surfactant evaporates rapidly (decreasing by 1 or 2 at each step) and there is no source renewing it, the concentration drops to zero everywhere.
*   **Aesthetic Rating:** **1.5/10**. Fades too quickly.

### Rule 10: Porous Darcy Gravity Currents
*   **Visual Observations (Single):** A thin double vertical sand/rust line in the center.
*   **Visual Observations (Random):** Highly textured, static vertical stripes of sand, gold, olive, and blue.
*   **Order vs. Chaos:** Frozen steady state with high-frequency spatial texture.
*   **Physics-to-Visual Link:** Gravity-driven drainage flows downhill but stops abruptly when the height drops below the capillary trapping threshold ($S < 3$). In both cases, the fluid drains until it is trapped by capillary forces, leaving behind stable "cliffs" that cannot flatten further.
*   **Aesthetic Rating:** **5/10**. Although static, the high-frequency sand-like texture is visually interesting.

---

## Winner Rules Selection

Based on the visual structures, long-term behavior, and aesthetic quality, the **top 3 winner rules** are:

| Rank | Rule # | Name | Reason for Selection |
| :---: | :---: | :--- | :--- |
| **1** | **Rule 1** | **Clamped Advection-Diffusion** | The only rule that successfully produces a stable, non-decaying **soliton (glider)** from a single cell initialization. In the random initialization, it forms a beautiful, highly ordered, multi-colored laminar wave train that propagates indefinitely. |
| **2** | **Rule 2** | **Buoyancy Convective Plumes** | Showcases a highly clean, high-contrast aesthetic. It exhibits an interesting physical asymmetry where the cold sinking plumes act as transient forces that shape the hot plumes before decaying, leaving behind a striking set of persistent, leftward-propagating thermal fronts. |
| **3** | **Rule 8** | **Kelvin-Helmholtz Instability** | Displays the most complex temporal evolution. The top section showcases a brief, chaotic mixing zone representing vortex roll-up instabilities, which then self-organize and relax into a stable, colorful traveling wave train. |

---

## Summary of Space-Time Dynamics

```
  Rule 1 (Advection)   ==> [Dynamic Traveling Solitons] (WINNER 1)
  Rule 2 (Buoyancy)    ==> [Asymmetric Decay to Left-Flow] (WINNER 2)
  Rule 8 (K-H Shear)   ==> [Chaotic Vortex -> Laminar Flow] (WINNER 3)
  Rules 3, 9           ==> [Viscous/Evaporative Dissipation to Rest]
  Rules 4, 5, 6, 7, 10 ==> [Frozen Static Vertical Stripes]
```

---

## Recommendations for Loop 7

To move from frozen or rapidly decaying behaviors to more complex, organic, and open-ended dynamics, we should adjust the design parameters in the next loop:
1.  **Continuous External Forcing (Driving Terms):** Rules like Rayleigh-Bénard Convection (Rule 3) require a background temperature gradient. We should introduce source terms (e.g., heating from the bottom boundary or random energy injections) to counteract viscous dissipation.
2.  **Softer Decay/Evaporation Rates:** For Rule 9, reducing the evaporation rate or adding a local surfactant concentration generator would prevent rapid extinction and allow Marangoni waves to spread further and form rich dendritic plumes.
3.  **Active Advection/Transport in Static Rules:** Rules 4, 5, 6, 7, and 10 all freeze into vertical stripes because they lack a directional advection velocity or a momentum term. Introducing a global or local pressure-driven transport field would cause these structures to migrate, collide, and morph over time, yielding much richer space-time dynamics.
