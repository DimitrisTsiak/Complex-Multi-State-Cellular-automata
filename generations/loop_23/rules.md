# Loop 23 Cellular Automata Rules: Evolutionary Mutational Wars & Stochastic Pathology

This document details 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Evolutionary Mutational Wars & Stochastic Pathology**. 

These rules model epidemiological processes such as contact transmission probabilities, multi-strain viral competition, genetic drift, stochastic mutation noise, host immunization decay, and epigenetic host-pathogen co-evolution. Each rule is defined on a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The transition functions incorporate probabilistic state changes, representing stochastic interactions and mutations.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Antigenic Drift Competition](#rule-1-antigenic-drift-competition) | 6 | Radius $r=1$ | Dual-strain contact transmission and cross-immunity drift | Alternating colored fronts leaving behind dynamic immunized patches |
| **2** | [Hyper-Mutational Cascade](#rule-2-hyper-mutational-cascade-symmetric-error-catastrophe) | 6 | Radius $r=1$ | Progressive mutation leading to increased infectivity but error catastrophe | Expanding fronts breaking into fragmented necrotic holes and immune boundaries |
| **3** | [Quorum-Sensing Pathogen Suppression](#rule-3-quorum-sensing-pathogen-suppression) | 5 | Radius $r=2$ | Density-dependent immune recruitment and latent-to-active activation | Silent latent networks chased by explosive immune clearing fronts |
| **4** | [Stochastic Phenotypic Switching](#rule-4-stochastic-phenotypic-switching) | 5 | Radius $r=1$ | Bet-hedging switching between active colonizer and dormant persister states | Rapidly wiped out active waves with quiet, persistent seeds sparking reinfection |
| **5** | [Viroid Hyperparasitism](#rule-5-viroid-hyperparasitism) | 6 | Radius $r=1$ | Helper-dependent sub-viral integration and replication hijacking | Nested multi-layered waves stabilizing into periodic spiral patterns |
| **6** | [Retroviral Integration and Oncogenic Drift](#rule-6-retroviral-integration-and-oncogenic-drift) | 6 | Radius $r=2$ | Genome integration leading to latent proviruses and competitive tumor growth | Slow-expanding tumor patches erupting into aggressive necrotic clusters |
| **7** | [Recombination-Driven Zoonotic Spillover](#rule-7-recombination-driven-zoonotic-spillover) | 6 | Radius $r=1$ | Co-infection facilitating genetic segment swapping and highly lethal strain creation | Collision zones of mild endemic strains igniting fast-moving lethal spillover waves |
| **8** | [Epigenetic Vaccination Memory and Drift](#rule-8-epigenetic-vaccination-memory-and-drift) | 6 | Radius $r=1$ | Host immune memory selection driving viral antigenic variant oscillations | Cyclic waves of infection chasing alternating domains of immunized hosts |
| **9** | [Spatial Quarantining and Vector Transmission](#rule-9-spatial-quarantining-and-vector-transmission) | 5 | Radius $r=2$ | Short-range contact and long-range vector jumps countered by active shutdown | Quarantine firewalls breached by vector sparks creating chaotic spatial outbreaks |
| **10** | [Antagonistic Co-evolutionary Arms Race](#rule-10-antagonistic-co-evolutionary-arms-race) | 7 | Radius $r=1$ | Multi-allele Red Queen frequency-dependent receptor-antigen matching | Perpetual turbulent mosaic of shifting host alleles and matching viral strains |

---

## Rule Definitions

### Rule 1: Antigenic Drift Competition
* **Domain Connection:** Models two competing viral strains spreading in a susceptible population, subject to mutation (drift) and partial cross-immunity.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Susceptible Host ($S$)
  * State $1$: Infected with Strain A ($I_A$)
  * State $2$: Infected with Strain B ($I_B$)
  * State $3$: Recovered & Immunized against A ($R_A$)
  * State $4$: Recovered & Immunized against B ($R_B$)
  * State $5$: Cross-Immune to both strains ($R_{AB}$)
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_A(x)$ and $N_B(x)$ be the counts of neighbors in state $1$ and $2$ in the outer neighborhood $N^*(x) = \{x-1, x+1\}$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Susceptible):**
    - The infection probability by Strain A is $p_A = 1 - (1 - \beta_A)^{N_A(x)}$, where transmission probability $\beta_A = 0.60$.
    - The infection probability by Strain B is $p_B = 1 - (1 - \beta_B)^{N_B(x)}$, where transmission probability $\beta_B = 0.50$.
    - With probability $p_A (1 - p_B)$ (exposed only to A):
      - Stays infected with A (state $1$) with probability $1 - \mu$.
      - Mutates to strain B (state $2$) with probability $\mu = 0.10$.
    - With probability $p_B (1 - p_A)$ (exposed only to B):
      - Stays infected with B (state $2$) with probability $1 - \mu$.
      - Mutates to strain A (state $1$) with probability $\mu = 0.10$.
    - With probability $p_A p_B$ (exposed to both):
      - Becomes infected with A (state $1$) with probability $0.50$.
      - Becomes infected with B (state $2$) with probability $0.50$.
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($I_A$):**
    - Recovers to $R_A$ (state $3$) with recovery probability $\gamma = 0.70$.
    - Otherwise, remains infected with A (state $1$).
  - **If $s = 2$ ($I_B$):**
    - Recovers to $R_B$ (state $4$) with recovery probability $\gamma = 0.70$.
    - Otherwise, remains infected with B (state $2$).
  - **If $s = 3$ ($R_A$):**
    - Can be infected by Strain B with cross-immunity discount. Infection probability is $p_B' = 1 - (1 - (1 - \sigma)\beta_B)^{N_B(x)}$, where cross-immunity protection is $\sigma = 0.50$ (giving effective transmission rate $0.25$).
      - If infected, transitions to $I_B$ (state $2$) with probability $1 - \mu$ ($0.90$) and to $I_A$ (state $1$) with probability $\mu = 0.10$.
    - If not infected, decays to Susceptible (state $0$) with decay probability $\alpha = 0.15$.
    - Otherwise, remains $R_A$ (state $3$).
  - **If $s = 4$ ($R_B$):**
    - Can be infected by Strain A with cross-immunity discount. Infection probability is $p_A' = 1 - (1 - (1 - \sigma)\beta_A)^{N_A(x)}$, where cross-immunity protection is $\sigma = 0.50$ (giving effective transmission rate $0.30$).
      - If infected, transitions to $I_A$ (state $1$) with probability $1 - \mu$ ($0.90$) and to $I_B$ (state $2$) with probability $\mu = 0.10$.
    - If not infected, decays to Susceptible (state $0$) with decay probability $\alpha = 0.15$.
    - Otherwise, remains $R_B$ (state $4$).
  - **If $s = 5$ ($R_{AB}$):**
    - Decays to $R_A$ (state $3$) with probability $0.05$.
    - Decays to $R_B$ (state $4$) with probability $0.05$.
    - Otherwise, remains $R_{AB}$ (state $5$).
* **Mathematical/Physical Rationale:** Models the classic evolutionary landscape of multi-strain pandemics. Competing strains generate selective pressures on the host population, which are balanced by cross-immunity. Genetic drift occurs when one strain gains a local spatial advantage, only to be checked by host immunity, driving the other strain's expansion.
* **Expected Visual Behavior:** Propagating waves of infection leaving behind trails of temporary immunity. When Strain A and Strain B wavefronts meet, they form complex boundary lines of cross-resistance, resulting in a mosaic of oscillating red (Strain A) and blue (Strain B) domains.

---

### Rule 2: Hyper-Mutational Cascade (Symmetric Error Catastrophe)
* **Domain Connection:** Simulates an unstable virus undergoing sequential mutational steps. Higher mutants become increasingly infectious but compromise structural stability, leading to host cell lysis (death) and eventual extinction of the viral population.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Healthy Host ($H$)
  * State $1$: Wild-type Virus ($V_1$) - highly stable, low transmissibility
  * State $2$: First Mutant ($V_2$) - moderately stable, medium transmissibility
  * State $3$: Hyper-Mutant ($V_3$) - highly unstable, very high transmissibility
  * State $4$: Lytic / Dead Cell ($D$) - cell lysed, cannot be infected
  * State $5$: Immunized ($R$) - temporary protection
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_k(x)$ be the count of neighbors in state $k \in \{1, 2, 3\}$ in the outer neighborhood.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Healthy):**
    - Infection probability by strain $k$ is $p_k = 1 - (1 - \beta_k)^{N_k(x)}$, where $\beta_1 = 0.25, \beta_2 = 0.50, \beta_3 = 0.75$.
    - If infected (with combined probability $P_{inf} = 1 - (1-p_1)(1-p_2)(1-p_3)$):
      - Select infecting strain $k$ proportionally to individual infection pressure: $p_k / (p_1 + p_2 + p_3)$.
      - With mutation probability $\mu = 0.20$, the strain mutates to $\min(k+1, 4)$. (If it mutates to $4$, the host cell is lysed instantly).
      - With probability $1 - \mu = 0.80$, the cell enters infected state $k$.
    - Otherwise, remains Healthy (state $0$).
  - **If $s = 1$ ($V_1$):**
    - Spontaneous mutation: transitions to $V_2$ (state $2$) with probability $m_{12} = 0.10$.
    - Lysis: transitions to $D$ (state $4$) with probability $l_1 = 0.10$.
    - Otherwise, remains $V_1$ (state $1$).
  - **If $s = 2$ ($V_2$):**
    - Spontaneous mutation: transitions to $V_3$ (state $3$) with probability $m_{23} = 0.15$.
    - Lysis: transitions to $D$ (state $4$) with probability $l_2 = 0.30$.
    - Otherwise, remains $V_2$ (state $2$).
  - **If $s = 3$ ($V_3$):**
    - Lysis: transitions to $D$ (state $4$) with probability $l_3 = 0.70$.
    - Otherwise, remains $V_3$ (state $3$).
  - **If $s = 4$ ($D$):**
    - Clearance: transitions to Immunized (state $5$) with probability $r_{clear} = 0.40$.
    - Otherwise, remains $D$ (state $4$).
  - **If $s = 5$ ($R$):**
    - Decay: decays to Healthy (state $0$) with probability $d_{imm} = 0.20$.
    - Otherwise, remains $R$ (state $5$).
* **Mathematical/Physical Rationale:** Models the biological threshold of error catastrophe. If mutation rate is too high, the virus accumulates deleterious mutations, driving itself to extinction by destroying host tissue faster than it can infect new hosts.
* **Expected Visual Behavior:** Outbreaks begin as slow-propagating clusters of state 1. Rapidly, fast-moving but highly destructive rings of state 3 erupt inside the fronts, leaving large dead patches (state 4). This triggers a local population collapse, resulting in fragmented, dendritic structures.

---

### Rule 3: Quorum-Sensing Pathogen Suppression
* **Domain Connection:** Models a host immune system that triggers a localized macrophage response only when the density of active infections exceeds a threshold (quorum sensing).
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Healthy Host ($H$)
  * State $1$: Latent Infection ($I_L$) - asymptomatic, low transmission
  * State $2$: Active Infection ($I_A$) - symptomatic, high transmission, emits quorum signals
  * State $3$: Activated Immune Cell ($M$) - destroys pathogens, recruited by active infections
  * State $4$: Exhausted Host / Tissue ($E$) - temporarily refractory
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
  Let $N_A(x)$ and $N_M(x)$ be the counts of neighbors in states $2$ and $3$ respectively.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Healthy):**
    - Infection by $I_A$: probability is $p_{inf} = 1 - (1 - \beta)^{N_A(x)}$ where transmission rate $\beta = 0.50$.
      - If infected, becomes Latent $I_L$ (state $1$) with probability $0.80$, and Active $I_A$ (state $2$) with probability $0.20$.
    - Quorum recruitment: If $N_A(x) \ge 2$, immune recruitment triggers. The cell transitions to Activated Immune $M$ (state $3$) with probability $P_{recruit} = 0.20 \times N_A(x)$.
    - Otherwise, remains Healthy (state $0$).
  - **If $s = 1$ ($I_L$):**
    - Immune clearance: If $N_M(x) \ge 1$, cell is cleared to Healthy (state $0$) with probability $0.75$.
    - Activation: Transitions to Active $I_A$ (state $2$) with probability $0.10 + 0.05 \times N_A(x)$ (quorum-sensing induced activation).
    - Otherwise, remains Latent (state $1$).
  - **If $s = 2$ ($I_A$):**
    - Immune clearance: If $N_M(x) \ge 1$, cell is cleared and becomes Exhausted (state $4$) with probability $0.85$.
    - Natural decay: Transitions to Exhausted (state $4$) with probability $0.15$.
    - Otherwise, remains Active (state $2$).
  - **If $s = 3$ ($M$):**
    - Exhaustion: Transitions to Exhausted (state $4$) with probability $0.40$.
    - Otherwise, remains Active Immune (state $3$).
  - **If $s = 4$ ($E$):**
    - Regeneration: Transitions to Healthy (state $0$) with probability $0.25$.
    - Otherwise, remains Exhausted (state $4$).
* **Mathematical/Physical Rationale:** Simulates non-linear host defense activation. Latent cells represent a reservoirs of silent pathogens. When these reservoirs ignite stochastically and form clusters of active infection, the host triggers a localized macrophage firewall.
* **Expected Visual Behavior:** Thin, dendritic networks of latency (state 1) spread silently. Once they accumulate, they ignite into active clusters (state 2) which are immediately targeted by expanding fields of immune cells (state 3). This generates rhythmic, self-limiting clearings resembling cellular defenses in human tissue.

---

### Rule 4: Stochastic Phenotypic Switching
* **Domain Connection:** Models phenotypic plasticity where pathogens switch stochastically between a fast-growing, vulnerable "colonizer" state and a dormant, highly resistant "persister" state to hedge against host immune shocks.
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Susceptible Host ($S$)
  * State $1$: Colonizer Pathogen ($I_C$) - rapid transmission, highly vulnerable to immune shocks
  * State $2$: Persister Pathogen ($I_P$) - slow transmission, highly resistant to shocks
  * State $3$: Cleared / Immunized ($R$) - temporary immunity
  * State $4$: Immune Shock State ($K$) - localized immune response clearing colonizers
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_C(x)$, $N_P(x)$, and $N_K(x)$ be neighborhood counts of states $1, 2,$ and $4$ in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - Local Shock Probability: A cell enters the Shock State $K$ (state $4$) with probability $P_{shock} = 0.15 \times (N_C(x) + N_P(x))$, representing localized immune activation.
  - **If $s = 0$ (Susceptible):**
    - If shock occurs (with probability $P_{shock}$): transitions to $K$ (state $4$).
    - Else, infection by $I_C$ occurs with probability $p_C = 1 - (1 - \beta_C)^{N_C(x)}$ ($\beta_C = 0.65$), and infection by $I_P$ with probability $p_P = 1 - (1 - \beta_P)^{N_P(x)}$ ($\beta_P = 0.10$).
    - If infected, transitions to $I_C$ (state $1$) with probability $0.90$, and $I_P$ (state $2$) with probability $0.10$.
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($I_C$):**
    - If shock occurs or $N_K(x) \ge 1$: cleared to $R$ (state $3$) with probability $0.95$.
    - Phenotypic switch: transitions to Persister $I_P$ (state $2$) with probability $f_{CP} = 0.08$.
    - Natural recovery: transitions to $R$ (state $3$) with probability $\gamma_C = 0.15$.
    - Otherwise, remains Colonizer (state $1$).
  - **If $s = 2$ ($I_P$):**
    - If shock occurs or $N_K(x) \ge 1$: cleared to $R$ (state $3$) with probability $0.05$ (high resistance).
    - Phenotypic switch: transitions to Colonizer $I_C$ (state $1$) with probability $f_{PC} = 0.12$.
    - Natural recovery: transitions to $R$ (state $3$) with probability $\gamma_P = 0.02$.
    - Otherwise, remains Persister (state $2$).
  - **If $s = 3$ ($R$):**
    - Decay: decays to Susceptible (state $0$) with probability $d_{imm} = 0.15$.
    - Otherwise, remains Immunized (state $3$).
  - **If $s = 4$ ($K$):**
    - Decay: decays to Susceptible (state $0$) with probability $d_{shock} = 0.80$.
    - Otherwise, remains in Shock State (state $4$).
* **Mathematical/Physical Rationale:** Models the evolutionary survival strategy of biological bet-hedging. Under frequent environmental pressure (immune shocks), a population composed purely of colonizers would perish. Maintaining a reservoir of slow-growing persisters ensures survival and subsequent repopulation.
* **Expected Visual Behavior:** Outbreaks expand as rapid fronts of state 1. When immune shocks (state 4) trigger, they sweep through the colonizer population, wiping out entire bands. A few scattered persisters (state 2) survive the shock, slowly switching back to state 1 to start new epidemics. This creates a flashing, intermittent, patch-like pattern.

---

### Rule 5: Viroid Hyperparasitism
* **Domain Connection:** Models a three-trophic system where a primary virus infects hosts, but is targeted by a satellite viroid that hijacks its replication machinery. This reduces viral virulence and facilitates host recovery.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Susceptible Host ($S$)
  * State $1$: Primary Virus ($I$) - standard infected state
  * State $2$: Co-infected ($C$) - virus and viroid replicating together
  * State $3$: Viroid-dominated ($V$) - viroid has suppressed primary virus
  * State $4$: Necrotic / Dead ($D$) - host cell death
  * State $5$: Recovered ($R$) - temporary immunity
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_I(x)$, $N_C(x)$, and $N_V(x)$ be neighborhood counts in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Susceptible):**
    - Infection probability by primary virus is $p_{inf} = 1 - (1 - \beta_I)^{N_I(x)} \cdot (1 - 0.5 \beta_I)^{N_C(x)}$, where $\beta_I = 0.55$.
    - If infected, transitions to $I$ (state $1$).
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($I$):**
    - Hyperinfection by viroid: probability is $p_{hyper} = 1 - (1 - \beta_V)^{N_C(x) + N_V(x)}$, where $\beta_V = 0.60$.
      - If hyperinfected, transitions to Co-infected (state $2$).
    - Otherwise, cell death: transitions to $D$ (state $4$) with probability $0.10$.
    - Otherwise, natural recovery: transitions to $R$ (state $5$) with probability $0.10$.
    - Otherwise, remains Infected (state $1$).
  - **If $s = 2$ ($C$):**
    - Suppression: Viroid shuts down virus replication, transitioning the cell to Viroid-dominated $V$ (state $3$) with probability $0.35$.
    - Lysis: cell dies and becomes $D$ (state $4$) with probability $0.20$.
    - Otherwise, remains Co-infected (state $2$).
  - **If $s = 3$ ($V$):**
    - Recovery: Since virus load is low, cell recovers to $R$ (state $5$) with probability $0.45$.
    - Otherwise, remains Viroid-dominated (state $3$).
  - **If $s = 4$ ($D$):**
    - Regeneration: Dead host tissue regenerated to Susceptible $S$ (state $0$) with probability $r_{reg} = 0.30$.
    - Otherwise, remains Dead (state $4$).
  - **If $s = 5$ ($R$):**
    - Decay: Immunity decays to Susceptible $S$ (state $0$) with probability $0.15$.
    - Otherwise, remains Recovered (state $5$).
* **Mathematical/Physical Rationale:** Models the role of sub-viral parasites in disease suppression. Because the viroid requires the helper virus to replicate, it cannot infect Susceptible ($0$) cells directly. This introduces a mathematical delay line and a negative feedback loop that dampens epidemic peaks and stabilizes the host population.
* **Expected Visual Behavior:** The primary virus (state 1) spreads as a fast wave. It is chased by the viroid (state 2 and 3) which eats the virus wave from the inside. This creates a nested wave structure where a red band (primary virus) is chased by a blue band (viroid) and green band (recovered), stabilizing into periodic self-sustaining spiral-like waves.

---

### Rule 6: Retroviral Integration and Oncogenic Drift
* **Domain Connection:** Models retroviral integration into the host genome, leading to either latency or oncogenic cell transformation. Tumor cells proliferate and crowd out healthy tissues, representing cancer progression as a form of genetic drift.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Normal Cell ($N$)
  * State $1$: Actively Infected ($I_A$) - replicates and spreads virus
  * State $2$: Latently Infected ($I_L$) - provirus integrated, silent
  * State $3$: Slow-growing Tumor ($T_1$) - stochastically progresses
  * State $4$: Aggressive Tumor ($T_2$) - fast growing, high crowding pressure
  * State $5$: Necrotic / Dead ($D$)
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
  Let $N_{IA}(x)$, $N_{T1}(x)$, and $N_{T2}(x)$ be neighborhood counts in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Normal):**
    - Infection: probability of retroviral infection is $p_{inf} = 1 - (1 - \beta)^{N_{IA}(x)}$ where $\beta = 0.35$.
      - If infected, becomes Active $I_A$ (state $1$) with probability $0.55$, and Latent $I_L$ (state $2$) with probability $0.45$.
    - Crowding: If $N_{T2}(x) \ge 2$, the normal cell is crushed by tumor pressure and becomes Necrotic $D$ (state $5$) with probability $0.40$.
    - Otherwise, remains Normal (state $0$).
  - **If $s = 1$ ($I_A$):**
    - Integration to latency: transitions to $I_L$ (state $2$) with probability $0.15$.
    - Oncogenic mutation: transitions to Tumor $T_1$ (state $3$) with probability $\mu = 0.05$.
    - Lysis/Death: transitions to $D$ (state $5$) with probability $0.25$.
    - Otherwise, remains $I_A$ (state $1$).
  - **If $s = 2$ ($I_L$):**
    - Reactivation: transitions to Active $I_A$ (state $1$) with probability $0.10$.
    - Latent mutation: transitions to Tumor $T_1$ (state $3$) with probability $\mu_{latent} = 0.02$.
    - Otherwise, remains $I_L$ (state $2$).
  - **If $s = 3$ ($T_1$):**
    - Proliferation: Invades a Normal cell (state $0$) neighbor with probability $0.15$. (If $S_t(x) = 0$ and is not infected, it can also transition to $T_1$ with probability $1 - (1 - 0.15)^{N_{T1}(x)}$).
    - Malignant progression: transitions to Aggressive $T_2$ (state $4$) with probability $\alpha_{prog} = 0.08$.
    - Apoptosis: transitions to $D$ (state $5$) with probability $0.05$.
    - Otherwise, remains $T_1$ (state $3$).
  - **If $s = 4$ ($T_2$):**
    - Aggressive Proliferation: Invades any Normal (0) or Infected ($I_A, I_L$) neighbor with probability $0.45$. (If $S_t(x) \in \{0, 1, 2\}$, it can transition to $T_2$ with probability $1 - (1 - 0.45)^{N_{T2}(x)}$).
    - Necrosis: due to rapid growth, transitions to $D$ (state $5$) with probability $0.12$.
    - Otherwise, remains $T_2$ (state $4$).
  - **If $s = 5$ ($D$):**
    - Clearance: Dead cell cleared and replaced by Normal $N$ (state $0$) with probability $0.35$.
    - Otherwise, remains $D$ (state $5$).
* **Mathematical/Physical Rationale:** Models somatic evolution and ecological competition within a tissue. Normal, latently infected, actively infected, and tumor cells compete for space. The aggressive tumor $T_2$ acts as an invasive species, but its high necrosis rate ($0.12$) models nutrient limitation (ischemia), preventing total domination and maintaining dynamic equilibrium.
* **Expected Visual Behavior:** Outbreaks of retroviruses leave a wake of latent cells (state 2). Stochastically, tumor seeds (state 3) appear in these wakes. They grow into slow, expanding patches, which then suddenly erupt into aggressive, fast-growing clusters of state 4. The tissue becomes a mosaic of healthy cells, viral activity, and expanding tumor colonies.

---

### Rule 7: Recombination-Driven Zoonotic Spillover
* **Domain Connection:** Models two endemic viral strains circulating in separate ecological niches. Co-infection of a host cell leads to a genetic recombination event, spawning a highly virulent, zoonotic recombinant strain that rapidly spreads through the entire population.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Susceptible ($H$)
  * State $1$: Infected with Strain A ($I_A$)
  * State $2$: Infected with Strain B ($I_B$)
  * State $3$: Co-infected Host ($I_{AB}$) - genetic mixing vessel
  * State $4$: Recombinant Strain ($I_R$) - highly infectious and lethal
  * State $5$: Dead Host ($D$)
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_A(x), N_B(x), N_{AB}(x), N_R(x)$ be neighborhood counts in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Susceptible):**
    - Infection probability by A is $p_A = 1 - (1 - \beta_A)^{N_A(x) + 0.5 N_{AB}(x)}$ ($\beta_A = 0.45$).
    - Infection probability by B is $p_B = 1 - (1 - \beta_B)^{N_B(x) + 0.5 N_{AB}(x)}$ ($\beta_B = 0.45$).
    - Infection probability by Recombinant R is $p_R = 1 - (1 - \beta_R)^{N_R(x)}$ ($\beta_R = 0.80$).
    - If exposed to R (probability $p_R$): transitions to $I_R$ (state $4$).
    - Else if co-exposed to A and B (probability $p_A p_B$): transitions to Co-infected $I_{AB}$ (state $3$).
    - Else if exposed to A only (probability $p_A (1 - p_B)$): transitions to $I_A$ (state $1$).
    - Else if exposed to B only (probability $p_B (1 - p_A)$): transitions to $I_B$ (state $2$).
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($I_A$):**
    - Superinfection by B: probability $p_{super\_B} = 1 - (1 - \beta_B)^{N_B(x) + 0.5 N_{AB}(x)}$. If superinfected, transitions to Co-infected $I_{AB}$ (state $3$).
    - Natural recovery: transitions to Susceptible (state $0$) with probability $\gamma_A = 0.20$.
    - Otherwise, remains $I_A$ (state $1$).
  - **If $s = 2$ ($I_B$):**
    - Superinfection by A: probability $p_{super\_A} = 1 - (1 - \beta_A)^{N_A(x) + 0.5 N_{AB}(x)}$. If superinfected, transitions to Co-infected $I_{AB}$ (state $3$).
    - Natural recovery: transitions to Susceptible (state $0$) with probability $\gamma_B = 0.20$.
    - Otherwise, remains $I_B$ (state $2$).
  - **If $s = 3$ ($I_{AB}$):**
    - Recombination event: The two viral genomes swap segments. Transitions to Recombinant $I_R$ (state $4$) with probability $\rho = 0.25$.
    - Recovery: transitions to Susceptible (state $0$) with probability $0.10$.
    - Otherwise, remains Co-infected (state $3$).
  - **If $s = 4$ ($I_R$):**
    - Lethality: transitions to Dead $D$ (state $5$) with probability $m_R = 0.40$.
    - Recovery: transitions to Susceptible (state $0$) with probability $\gamma_R = 0.10$.
    - Otherwise, remains $I_R$ (state $4$).
  - **If $s = 5$ ($D$):**
    - Decay: Dead cell decays back to Susceptible $H$ (state $0$) with probability $d_D = 0.25$.
    - Otherwise, remains Dead (state $5$).
* **Mathematical/Physical Rationale:** Highlights the mathematical mechanism of viral recombination. The superinfection probability ($p_{super}$) acts as the pathway to create the co-infected state $I_{AB}$. This models how hybrid strains can emerge in dense populations and trigger devastating epidemics due to high transmission rates ($\beta_R = 0.80$).
* **Expected Visual Behavior:** Initially, Strain A and Strain B spread as separate, mild, slow-moving fronts. Where they overlap and collide, co-infected cells (state 3) form. Suddenly, bright sparks of state 4 (recombinant) erupt at these collision interfaces. State 4 spreads as an ultra-fast, destructive wave, leaving a massive trail of state 5 (dead host cells).

---

### Rule 8: Epigenetic Vaccination Memory and Drift
* **Domain Connection:** Models the co-evolutionary arms race between viral antigenic drift and host immune memory. Hosts retain specific immunological memory of viral surface proteins, which decay stochastically. The mismatch between viral antigen and host memory determines susceptibility.
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Susceptible, No Memory ($S$)
  * State $1$: Viral Strain 1 ($V_1$) - carries antigen type 1
  * State $2$: Viral Strain 2 ($V_2$) - carries antigen type 2
  * State $3$: Host with Memory 1 ($M_1$) - immune to $V_1$, vulnerable to $V_2$
  * State $4$: Host with Memory 2 ($M_2$) - immune to $V_2$, vulnerable to $V_1$
  * State $5$: Cross-Immunized Host ($M_{12}$) - immune to both
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_1(x)$ and $N_2(x)$ be counts of infected neighbors in states 1 and 2 in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Susceptible):**
    - Infection by $V_1$: probability $p_1 = 1 - (1 - \beta)^{N_1(x)}$ ($\beta = 0.60$).
    - Infection by $V_2$: probability $p_2 = 1 - (1 - \beta)^{N_2(x)}$ ($\beta = 0.60$).
    - If infected by both (probability $p_1 p_2$): becomes $V_1$ with probability $0.50$ and $V_2$ with probability $0.50$.
    - Else if infected by $V_1$ only (probability $p_1 (1-p_2)$): transitions to $V_1$ (state $1$).
    - Else if infected by $V_2$ only (probability $p_2 (1-p_1)$): transitions to $V_2$ (state $2$).
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($V_1$):**
    - Antigenic drift (mutation): transitions to $V_2$ (state $2$) with probability $\mu = 0.12$.
    - Clearance & Memory acquisition: transitions to $M_1$ (state $3$) with probability $\gamma = 0.48$.
    - Otherwise, remains $V_1$ (state $1$).
  - **If $s = 2$ ($V_2$):**
    - Antigenic drift (mutation): transitions to $V_1$ (state $1$) with probability $\mu = 0.12$.
    - Clearance & Memory acquisition: transitions to $M_2$ (state $4$) with probability $\gamma = 0.48$.
    - Otherwise, remains $V_2$ (state $2$).
  - **If $s = 3$ ($M_1$):**
    - Exposure to mismatched $V_2$: infection probability is $p_{match\_fail} = 1 - (1 - 0.35)^{N_2(x)}$ (reduced infectivity).
      - If infected, transitions to $V_2$ (state $2$).
    - If not infected, can upgrade memory to $M_{12}$ (state $5$) upon exposure: probability is $0.15 \times N_2(x)$.
    - If neither occurs, decays to Susceptible $S$ (state $0$) with probability $d_{imm} = 0.10$.
    - Otherwise, remains $M_1$ (state $3$).
  - **If $s = 4$ ($M_2$):**
    - Exposure to mismatched $V_1$: infection probability is $p_{match\_fail} = 1 - (1 - 0.35)^{N_1(x)}$.
      - If infected, transitions to $V_1$ (state $1$).
    - If not infected, can upgrade memory to $M_{12}$ (state $5$) upon exposure: probability is $0.15 \times N_1(x)$.
    - If neither occurs, decays to Susceptible $S$ (state $0$) with probability $d_{imm} = 0.10$.
    - Otherwise, remains $M_2$ (state $4$).
  - **If $s = 5$ ($M_{12}$):**
    - Double immunization decay: transitions to $M_1$ (state $3$) with probability $0.08$, or to $M_2$ (state $4$) with probability $0.08$.
    - Otherwise, remains $M_{12}$ (state $5$).
* **Mathematical/Physical Rationale:** Implements immunological memory as a dynamic state machine. It shows how host immunization acts as a selective pressure that drives genetic drift: as hosts become immune to $V_1$, the virus is forced to mutate to $V_2$ to survive, establishing a feedback loop of oscillating dominance.
* **Expected Visual Behavior:** The system forms self-organizing spatial domains. In domains dominated by $M_1$ hosts, Strain 2 ($V_2$) thrives and expands, converting hosts to $M_2$. In $M_2$ domains, Strain 1 ($V_1$) expands. This leads to cyclic waves of infection chasing alternating patterns of blue ($M_1$) and purple ($M_2$) immune blocks.

---

### Rule 9: Spatial Quarantining and Vector Transmission
* **Domain Connection:** Models disease transmission occurring via two pathways: direct contact (short-range) and insect/air vectors (long-range/stochastic jumps). Hosts react to nearby infections by entering a temporary quarantine state, sealing themselves from interaction.
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Susceptible Host ($S$)
  * State $1$: Infected Host ($I$) - transmits directly and spawns vectors
  * State $2$: Quarantined Host ($Q$) - fully sealed, cannot infect or be infected
  * State $3$: Vector Swarm ($V$) - highly mobile, spreads infection rapidly
  * State $4$: Exhausted Host ($E$) - recovering, immune to direct contact but vulnerable to vectors
* **Neighborhood ($N(x)$):** Radius $r=2$ including the cell itself:
  $$N(x) = \{x-2, x-1, x, x+1, x+2\}$$
  Let $N_I(x)$, $N_Q(x)$, and $N_V(x)$ be neighborhood counts in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ (Susceptible):**
    - Quarantine trigger: If $N_I(x) \ge 1$ or $N_V(x) \ge 1$, cell has a probability of quarantining: $p_{quar} = 0.35$.
      - If quarantine triggers, transitions to $Q$ (state $2$).
    - Else, infection occurs. Direct infection probability: $p_{direct} = 1 - (1 - 0.40)^{N_I(x)}$. Vector infection probability: $p_{vector} = 1 - (1 - 0.70)^{N_V(x)}$.
      - Total infection probability: $p_{inf} = 1 - (1 - 0.40)^{N_I(x)} \cdot (1 - 0.70)^{N_V(x)}$.
      - If infected, transitions to $I$ (state $1$).
    - Otherwise, remains Susceptible (state $0$).
  - **If $s = 1$ ($I$):**
    - Vector shedding: spawns a vector $V$ (state $3$) in a neighboring empty cell (state $0$) with probability $0.15$.
    - Recovery: transitions to Exhausted $E$ (state $4$) with probability $\gamma = 0.25$.
    - Otherwise, remains Infected (state $1$).
  - **If $s = 2$ ($Q$):**
    - Isolation decay: quarantine breaks down, transitioning back to Susceptible $S$ (state $0$) with probability $d_{quar} = 0.20$.
    - Otherwise, remains Quarantined (state $2$).
  - **If $s = 3$ ($V$):**
    - Dispersal / Die-off: The vector swarm flies away or dies, transitioning to Susceptible (state $0$) with probability $0.65$.
    - Otherwise, remains Vector Swarm (state $3$).
  - **If $s = 4$ ($E$):**
    - Vector reinfection: vulnerable only to vectors. Infection probability is $p_{reinf} = 1 - (1 - 0.35)^{N_V(x)}$.
      - If infected, transitions to $I$ (state $1$).
    - Recovery: recovers fully to Susceptible $S$ (state $0$) with probability $0.30$.
    - Otherwise, remains Exhausted (state $4$).
* **Mathematical/Physical Rationale:** Combines contact-based contagion with vector-mediated stochastic jumps (state 3), creating a multi-scale transmission dynamic. The host's active response ($Q$) acts as a dynamically assembled firewall, testing whether self-organized quarantine barriers can contain stochastic outbreaks.
* **Expected Visual Behavior:** The infection spreads out, prompting surrounding hosts to turn grey ($Q$), forming protective rings. However, the vector swarms (state 3) act as sparks that hop over these quarantine walls, starting new infection fires in unprotected zones. This results in chaotic, expanding circular waves punctuated by sudden, long-range outbreaks.

---

### Rule 10: Antagonistic Co-evolutionary Arms Race
* **Domain Connection:** Models the classic Red Queen hypothesis. Hosts have three distinct receptor alleles, and pathogens have three matching antigen types. A host cell is immune only to a pathogen with the matching index. Mutations continuously shift the pathogen's antigen, prompting hosts to adapt their receptors.
* **States ($N$):** $7$ states ($0, 1, 2, 3, 4, 5, 6$).
  * State $0$: Unprimed Host ($H$)
  * State $1$: Pathogen Strain $V_1$
  * State $2$: Pathogen Strain $V_2$
  * State $3$: Pathogen Strain $V_3$
  * State $4$: Immune Host $I_1$ - immune to $V_1$, infected by $V_2, V_3$
  * State $5$: Immune Host $I_2$ - immune to $V_2$, infected by $V_1, V_3$
  * State $6$: Immune Host $I_3$ - immune to $V_3$, infected by $V_1, V_2$
* **Neighborhood ($N(x)$):** Radius $r=1$ including the cell itself:
  $$N(x) = \{x-1, x, x+1\}$$
  Let $N_{V1}(x)$, $N_{V2}(x)$, $N_{V3}(x)$ be neighborhood counts in $N^*(x)$.
* **Transition Function:**
  Let $s = S_t(x)$ be the current state.
  - **If $s = 0$ ($H$):**
    - Infection: Probability of infection by $V_k$ is $p_k = 1 - (1 - \beta)^{N_{Vk}(x)}$ where $\beta = 0.50$.
      - If infected, transitions to $V_k$ (state $k$). (If infected by multiple, chooses one with equal probability).
    - Immune Priming: If not infected, but there is any pathogen in the neighborhood, the host has a probability $p_{prime} = 0.25$ of priming into a random immune state: transitions to $I_1$ (state $4$), $I_2$ (state $5$), or $I_3$ (state $6$) with equal probability $1/3$ each.
    - Otherwise, remains Unprimed (state $0$).
  - **If $s = 1$ ($V_1$):**
    - Mutation: mutates to $V_2$ (state $2$) or $V_3$ (state $3$) with probability $\mu = 0.08$ each.
    - Clearance: host clears infection and becomes immune $I_1$ (state $4$) with probability $\gamma = 0.40$.
    - Otherwise, remains $V_1$ (state $1$).
  - **If $s = 2$ ($V_2$):**
    - Mutation: mutates to $V_1$ (state $1$) or $V_3$ (state $3$) with probability $\mu = 0.08$ each.
    - Clearance: host clears infection and becomes immune $I_2$ (state $5$) with probability $\gamma = 0.40$.
    - Otherwise, remains $V_2$ (state $2$).
  - **If $s = 3$ ($V_3$):**
    - Mutation: mutates to $V_1$ (state $1$) or $V_2$ (state $2$) with probability $\mu = 0.08$ each.
    - Clearance: host clears infection and becomes immune $I_3$ (state $6$) with probability $\gamma = 0.40$.
    - Otherwise, remains $V_3$ (state $3$).
  - **If $s = 4$ ($I_1$):**
    - Infected by $V_2$ or $V_3$: Infection probability is $p_{inf} = 1 - (1 - \beta)^{N_{V2}(x) + N_{V3}(x)}$ ($\beta = 0.50$). If infected, transitions to the infecting strain.
    - Drift: Epigenetic receptor drift to $I_2$ (state $5$) or $I_3$ (state $6$) with probability $0.04$ each.
    - Decay: decays back to Unprimed $H$ (state $0$) with probability $d = 0.08$.
    - Otherwise, remains $I_1$ (state $4$).
  - **If $s = 5$ ($I_2$):**
    - Infected by $V_1$ or $V_3$: Infection probability is $p_{inf} = 1 - (1 - \beta)^{N_{V1}(x) + N_{V3}(x)}$ ($\beta = 0.50$). If infected, transitions to the infecting strain.
    - Drift: Epigenetic receptor drift to $I_1$ (state $4$) or $I_3$ (state $6$) with probability $0.04$ each.
    - Decay: decays back to Unprimed $H$ (state $0$) with probability $d = 0.08$.
    - Otherwise, remains $I_2$ (state $5$).
  - **If $s = 6$ ($I_3$):**
    - Infected by $V_1$ or $V_2$: Infection probability is $p_{inf} = 1 - (1 - \beta)^{N_{V1}(x) + N_{V2}(x)}$ ($\beta = 0.50$). If infected, transitions to the infecting strain.
    - Drift: Epigenetic receptor drift to $I_1$ (state $4$) or $I_2$ (state $5$) with probability $0.04$ each.
    - Decay: decays back to Unprimed $H$ (state $0$) with probability $d = 0.08$.
    - Otherwise, remains $I_3$ (state $6$).
* **Mathematical/Physical Rationale:** Simulates the frequency-dependent selection dynamics of host-pathogen systems. When Host $I_1$ dominates, virus $V_1$ is blocked, creating a selective advantage for mutant viruses $V_2$ or $V_3$. As they expand, they select for hosts with $I_2$ or $I_3$ receptors, leading to continuous co-evolutionary oscillations.
* **Expected Visual Behavior:** The space-time diagram displays a highly colorful, shifting tapestry. Blocks of host immune types shift in response to traveling wavefronts of the matching and mismatched viral strains. No single strain can dominate long-term, creating a state of perpetual, turbulent coexistence.
