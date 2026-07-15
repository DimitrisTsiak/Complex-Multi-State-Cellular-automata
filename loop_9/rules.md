# Loop 9 Cellular Automata Rules: Social Segregation & Game Theory

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Social Segregation & Game Theory**. 

Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$. The rules model complex multi-agent social interactions, strategic game-theoretic decisions, and segregation dynamics on a spatial network.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Local Schelling Segregation](#rule-1-local-schelling-segregation) | 3 | Radius $r=2$ | Local segregation and vacancy colonization | Clean phase separation and homogeneous blocks |
| **2** | [Spatial Prisoner's Dilemma](#rule-2-spatial-prisoners-dilemma) | 4 | Radius $r=1$ | Imitation of fittest strategy with wealth tracking | Gliders of defectors and protective cooperator clusters |
| **3** | [Hawk-Dove with Resource Cycles](#rule-3-hawk-dove-with-resource-cycles) | 5 | Radius $r=1$ | Payoff-based survival with resource depletion and recovery | Spreading wavefronts followed by refractory bands |
| **4** | [Minority Game & Local Non-Conformity](#rule-4-minority-game--local-non-conformity) | 6 | Radius $r=2$ | Contrarian choice dynamics with polarization memory | Flickering boundaries and stable polarized walls |
| **5** | [Public Goods with Punishment & Exhaustion](#rule-5-public-goods-with-punishment--exhaustion) | 5 | Radius $r=1$ | Altruistic punishment, defector coercion, and fatigue | Cyclic feedback loops and waves chasing each other |
| **6** | [Segregationist vs Integrationist Dynamics](#rule-6-segregationist-vs-integrationist-dynamics) | 5 | Radius $r=2$ | Multi-group segregation with diversity-seeking agents | Homogeneous blocks separated by integrationist buffer zones |
| **7** | [Hawk-Dove-Retaliator Game](#rule-7-hawk-dove-retaliator-game) | 4 | Radius $r=1$ | Multi-strategy evolutionary imitation and conflict death | Retaliators forming stable walls that block Hawks |
| **8** | [Class Struggle and Elite Overproduction](#rule-8-class-struggle-and-elite-overproduction) | 6 | Radius $r=2$ | Elite competition, structural crises, and revolutions | Periodic socio-economic waves and elite collapse |
| **9** | [Rumor Propagation with Skepticism](#rule-9-rumor-propagation-with-skepticism) | 7 | Radius $r=2$ | Information epidemics with skeptics and active debunkers | Spreading rumor envelopes extinguished by debunker walls |
| **10** | [Spatial Ultimatum Game](#rule-10-spatial-ultimatum-game) | 5 | Radius $r=1$ | Proposer-responder bargaining and strategy imitation | Intricate fractal boundaries and clustered fair-players |

---

## Rule Definitions

### Rule 1: Local Schelling Segregation
* **States ($N$):** $3$ states ($0, 1, 2$).
  * State $0$: Vacant (empty land).
  * State $1$: Group Red.
  * State $2$: Group Blue.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $N_1(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ and $N_2(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ be the counts of Red and Blue neighbors, respectively. Let the total occupied neighbor count be $D(x) = N_1(x) + N_2(x)$.
  
  * If $S_t(x) = 1$ (Red cell):
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } D(x) \ge 1 \text{ and } N_1(x) \ge N_2(x) \\
    0 & \text{otherwise (unhappy agent emigrates)}
    \end{cases}$$
  * If $S_t(x) = 2$ (Blue cell):
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } D(x) \ge 1 \text{ and } N_2(x) \ge N_1(x) \\
    0 & \text{otherwise (unhappy agent emigrates)}
    \end{cases}$$
  * If $S_t(x) = 0$ (Vacant cell):
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } N_1(x) > N_2(x) \text{ and } N_1(x) \ge 2 \\
    2 & \text{if } N_2(x) > N_1(x) \text{ and } N_2(x) \ge 2 \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:**
  This CA models a localized, deterministic version of Schelling's famous model of segregation. Instead of non-local swapping of cell positions, unsatisfied agents leave (state becomes vacant $0$), and vacant spaces are colonized by the local majority if it is sufficiently strong.
* **Expected Visual Behavior:**
  Rapid phase separation into large, homogeneous blocks of states 1 and 2, bordered by thin, transient zones of vacancy (state 0).

---

### Rule 2: Spatial Prisoner's Dilemma
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Poor Cooperator (C).
  * State $1$: Rich Cooperator (C).
  * State $2$: Poor Defector (D).
  * State $3$: Rich Defector (D).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
  Let $M(x) = \{x-1, x, x+1\}$ be the neighborhood including the cell itself.
* **Transition Function:**
  Let the underlying strategy of state $s$ be:
  $$Strat(s) = \begin{cases} C & \text{if } s \in \{0, 1\} \\ D & \text{if } s \in \{2, 3\} \end{cases}$$
  The payoff matrix $Payoff(s_1, s_2)$ for strategy $s_1$ against $s_2$ is:
  - $Payoff(C, C) = 3$
  - $Payoff(C, D) = 0$
  - $Payoff(D, C) = 5$
  - $Payoff(D, D) = 1$
  
  For each cell $z$ in the lattice, its total payoff is:
  $$P_t(z) = Payoff(Strat(S_t(z)), Strat(S_t(z-1))) + Payoff(Strat(S_t(z)), Strat(S_t(z+1)))$$
  
  At each time step, cell $x$ identifies the cell $y^* \in M(x)$ that has the highest payoff $P_t(y^*)$. Ties are broken by prioritizing self ($x$), then left ($x-1$), then right ($x+1$). Let $Strat_{new} = Strat(S_t(y^*))$.
  
  The new state $S_{t+1}(x)$ is determined by adopting $Strat_{new}$ and updating the wealth state based on the value of $P_t(y^*)$:
  - If $Strat_{new} = C$:
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } P_t(y^*) \ge 4 \\ 0 & \text{otherwise} \end{cases}$$
  - If $Strat_{new} = D$:
    $$S_{t+1}(x) = \begin{cases} 3 & \text{if } P_t(y^*) \ge 6 \\ 2 & \text{otherwise} \end{cases}$$
* **Mathematical Rationale:**
  This rule models the classic Nowak-May spatial game dynamics. Agents imitate the strategy of their most successful neighbor. We overlay this with a secondary "wealth" state (Rich/Poor) to track historical success, adding color and memory depth to the system.
* **Expected Visual Behavior:**
  Vibrant gliders of defectors exploiting cooperative clusters, cooperators forming stable defensive shields, and varying levels of wealth creating textured regions.

---

### Rule 3: Hawk-Dove with Resource Cycles
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Resource Ready (uncolonized).
  * State $1$: Hawk (aggressive strategy).
  * State $2$: Dove (cooperative/sharing strategy).
  * State $3$: Depleted Resource (Regenerating stage 1).
  * State $4$: Depleted Resource (Regenerating stage 2).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $Payoff(s_a, s_b)$ be the payoff for state $s_a$ against $s_b$:
  - Hawk vs Hawk: $-2$
  - Hawk vs Dove: $+4$
  - Dove vs Hawk: $0$
  - Dove vs Dove: $+2$
  - Against empty/depleted states ($0, 3, 4$): $0$
  
  For cell $x$, its total payoff is:
  $$P_t(x) = \sum_{y \in N(x)} Payoff(S_t(x), S_t(y))$$
  
  Transitions:
  * If $S_t(x) = 1$ (Hawk):
    $$S_{t+1}(x) = \begin{cases} 1 & \text{if } P_t(x) > 0 \\ 3 & \text{otherwise (death/depletion)} \end{cases}$$
  * If $S_t(x) = 2$ (Dove):
    $$S_{t+1}(x) = \begin{cases} 2 & \text{if } P_t(x) > 0 \\ 3 & \text{otherwise (death/depletion)} \end{cases}$$
  * If $S_t(x) = 3$: $S_{t+1}(x) = 4$
  * If $S_t(x) = 4$: $S_{t+1}(x) = 0$
  * If $S_t(x) = 0$ (Resource Ready):
    Let $H(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ and $D(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$.
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } H(x) \ge 1 \text{ and } H(x) \ge D(x) \\
    2 & \text{if } D(x) \ge 1 \text{ and } D(x) > H(x) \\
    0 & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:**
  This rule couples evolutionary game theory with an ecological resource cycle. Over-crowding of Hawks leads to negative payoffs and death. When a player dies, the land becomes depleted (states 3 and 4) and must regenerate before being re-colonized.
* **Expected Visual Behavior:**
  Spreading circular wavefronts of Hawks and Doves, followed by dark refractory/depleted regions (states 3 and 4), resembling excitable waves but driven by game-theoretic payoffs.

---

### Rule 4: Minority Game & Local Non-Conformity
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * States $0, 1, 2$: Left-leaning opinion (0: Weak, 1: Moderate, 2: Polarized).
  * States $3, 4, 5$: Right-leaning opinion (3: Weak, 4: Moderate, 5: Polarized).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $L(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{0, 1, 2\})$ and $R(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{3, 4, 5\})$ be the counts of Left-leaning and Right-leaning neighbors.
  
  * If $L(x) > R(x)$ (Left is majority):
    The cell moves toward Right (contrarian reaction):
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x) = 2 \\
    0 & \text{if } S_t(x) = 1 \\
    3 & \text{if } S_t(x) = 0 \text{ (crosses over to Right)} \\
    4 & \text{if } S_t(x) = 3 \\
    5 & \text{if } S_t(x) = 4 \\
    5 & \text{if } S_t(x) = 5
    \end{cases}$$
  * If $R(x) > L(x)$ (Right is majority):
    The cell moves toward Left (contrarian reaction):
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } S_t(x) = 5 \\
    3 & \text{if } S_t(x) = 4 \\
    0 & \text{if } S_t(x) = 3 \text{ (crosses over to Left)} \\
    1 & \text{if } S_t(x) = 0 \\
    2 & \text{if } S_t(x) = 1 \\
    2 & \text{if } S_t(x) = 2
    \end{cases}$$
  * If $L(x) = R(x)$ (Tie):
    Cells moderate their opinions, decaying toward weaker polarization states:
    $$S_{t+1}(x) = \begin{cases}
    1 & \text{if } S_t(x) = 2 \\
    0 & \text{if } S_t(x) = 1 \\
    0 & \text{if } S_t(x) = 0 \\
    4 & \text{if } S_t(x) = 5 \\
    3 & \text{if } S_t(x) = 4 \\
    3 & \text{if } S_t(x) = 3
    \end{cases}$$
* **Mathematical Rationale:**
  This rule models contrarian dynamics (Minority Game) where agents prefer to align with the minority choice. Being in the minority increases their polarization, while being in the majority causes them to shift away, and consensus/neutrality causes moderation.
* **Expected Visual Behavior:**
  Flickering chaotic boundaries, checkerboard patterns of alternating states, and stable localized polarized walls.

---

### Rule 5: Public Goods with Punishment & Exhaustion
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Defector (D).
  * State $1$: Cooperator (C).
  * State $2$: Active Punisher (P).
  * State $3$: Exhausted Punisher (EP, refractory).
  * State $4$: Coerced Cooperator (CC, temporary).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $D(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 0)$ (Defectors).
  Let $P(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ (Active Punishers).
  Let $C(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{1, 4\})$ (Cooperators).
  
  * If $S_t(x) = 0$ (Defector):
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } P(x) \ge 1 \text{ (coerced by punishment)} \\
    1 & \text{else if } C(x) = 0 \text{ and } P(x) = 0 \text{ (lonely defector starts cooperating)} \\
    0 & \text{otherwise}
    \end{cases}$$
  * If $S_t(x) = 1$ (Cooperator):
    $$S_{t+1}(x) = \begin{cases}
    0 & \text{if } D(x) \ge 1 \text{ and } P(x) = 0 \text{ (exploited by defector)} \\
    2 & \text{else if } C(x) \ge 1 \text{ and } D(x) = 0 \text{ (solid cooperative environment inspires punishment vigilance)} \\
    1 & \text{otherwise}
    \end{cases}$$
  * If $S_t(x) = 2$ (Active Punisher):
    $$S_{t+1}(x) = \begin{cases}
    3 & \text{if } D(x) \ge 1 \text{ (exhausted after punishing defectors)} \\
    2 & \text{otherwise}
    \end{cases}$$
  * If $S_t(x) = 3$ (Exhausted Punisher):
    $$S_{t+1}(x) = 1 \text{ (recovers as a normal Cooperator)}$$
  * If $S_t(x) = 4$ (Coerced Cooperator):
    $$S_{t+1}(x) = 0 \text{ (coercion wears off, slips back to defection)}$$
* **Mathematical Rationale:**
  This rule models a Public Goods game with altruistic punishment. Punishing defectors is effective but costly, leading to exhaustion (state 3) and a cycle of cooperation, exploitation, punishment, coercion, and decay.
* **Expected Visual Behavior:**
  Complex interlocking cyclic structures. Defector waves are chased by punisher waves, which leave behind exhausted trails, creating a visual feedback loop.

---

### Rule 6: Segregationist vs Integrationist Dynamics
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Vacant.
  * State $1$: Segregationist Type A.
  * State $2$: Segregationist Type B.
  * State $3$: Segregationist Type C.
  * State $4$: Integrationist Type (prefers diversity).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $N_k(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = k)$ for $k \in \{1, 2, 3, 4\}$.
  
  * If $S_t(x) \in \{1, 2, 3\}$ (Segregationists):
    Let $self\_state = S_t(x)$.
    $$S_{t+1}(x) = \begin{cases}
    self\_state & \text{if } N_{self\_state}(x) \ge 1 \text{ and } N_{self\_state}(x) \ge \max(N_1(x), N_2(x), N_3(x)) \\
    0 & \text{otherwise (unhappy agent leaves)}
    \end{cases}$$
  * If $S_t(x) = 4$ (Integrationist):
    Let $ActiveStates(x) = \sum_{k=1}^4 \mathbb{I}(N_k(x) > 0)$.
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } ActiveStates(x) \ge 2 \text{ and } \max(N_1(x), N_2(x), N_3(x), N_4(x)) \le 2 \\
    0 & \text{otherwise (unhappy agent leaves)}
    \end{cases}$$
  * If $S_t(x) = 0$ (Vacant):
    - Let $MaxSeg = \max(N_1(x), N_2(x), N_3(x))$.
    - If there is exactly one $k \in \{1, 2, 3\}$ such that $N_k(x) = MaxSeg$ and $MaxSeg \ge 2$:
      $$S_{t+1}(x) = k$$
    - Else if $N_4(x) \ge 2$:
      $$S_{t+1}(x) = 4 \text{ (Integrationists colonize)}$$
    - Else:
      $$S_{t+1}(x) = 0$$
* **Mathematical Rationale:**
  Extends Schelling's segregation to multiple groups and introduces an "integrationist" type that explicitly thrives on local diversity but flees homogeneity or single-group dominance.
* **Expected Visual Behavior:**
  Monolithic blocks of segregationist states (1, 2, 3) bordered by vibrant, thin, or breathing strips of integrationists (4) acting as buffer zones.

---

### Rule 7: Hawk-Dove-Retaliator Game
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Empty.
  * State $1$: Hawk (H).
  * State $2$: Dove (D).
  * State $3$: Retaliator (R).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
  Let $M(x) = \{x-1, x, x+1\}$ be the neighborhood including the cell itself.
* **Transition Function:**
  Pairwise game payoffs are defined as:
  - If $s_a = 0$ or $s_b = 0 \to Payoff(s_a, s_b) = 0$
  - Hawk vs Hawk: $Payoff(1, 1) = -2$
  - Hawk vs Dove: $Payoff(1, 2) = 4$
  - Hawk vs Retaliator: $Payoff(1, 3) = -2$ (Retaliator acts like Hawk)
  - Dove vs Hawk: $Payoff(2, 1) = 0$
  - Dove vs Dove: $Payoff(2, 2) = 2$
  - Dove vs Retaliator: $Payoff(2, 3) = 2$ (Retaliator acts like Dove)
  - Retaliator vs Hawk: $Payoff(3, 1) = -2$
  - Retaliator vs Dove: $Payoff(3, 2) = 2$
  - Retaliator vs Retaliator: $Payoff(3, 3) = 2$ (acts like Dove)

  For any cell $z$, its total payoff is:
  $$P_t(z) = Payoff(S_t(z), S_t(z-1)) + Payoff(S_t(z), S_t(z+1))$$
  
  At each step, cell $x$ identifies $y^* = \arg\max_{y \in M(x)} P_t(y)$. Ties are resolved by preferring self ($x$), then left ($x-1$), then right ($x+1$).
  
  * If $P_t(y^*) < 0$:
    $$S_{t+1}(x) = 0 \text{ (conflict/costs too high, cell becomes empty)}$$
  * If $P_t(y^*) \ge 0$:
    $$S_{t+1}(x) = \begin{cases}
    S_t(y^*) & \text{if } S_t(y^*) \ge 1 \\
    S_t(x) & \text{otherwise}
    \end{cases}$$
* **Mathematical Rationale:**
  Classic spatial evolutionary game theory including the Retaliator strategy. Retaliators are evolutionary stable against Hawks, whereas Doves are susceptible to Hawks. This creates a spatial struggle between the three strategies.
* **Expected Visual Behavior:**
  Hawks invade Doves, but Retaliators block Hawks and form highly stable, cooperative regions. The boundaries between Retaliator-dominated regions and Hawks show complex patterns.

---

### Rule 8: Class Struggle and Elite Overproduction
* **States ($N$):** $6$ states ($0, 1, 2, 3, 4, 5$).
  * State $0$: Underclass (Destitute).
  * State $1$: Working Class.
  * State $2$: Middle Class.
  * State $3$: Upper-Middle Class.
  * State $4$: Elite.
  * State $5$: Revolutionary.
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $E(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 4)$ (Elite count).
  Let $R(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 5)$ (Revolutionary count).
  Let $W(x) = \sum_{y \in N(x)} S_t(y)$ (local wealth index).
  
  * If $S_t(x) = 4$ (Elite):
    $$S_{t+1}(x) = \begin{cases}
    5 & \text{if } E(x) \ge 3 \text{ (elite overproduction leads to crisis/revolution)} \\
    3 & \text{else if } W(x) < 4 \text{ (declining wealth causes demotion)} \\
    4 & \text{otherwise}
    \end{cases}$$
  * If $S_t(x) = 5$ (Revolutionary):
    $$S_{t+1}(x) = 1 \text{ (decays to Working Class after revolution)}$$
  * If $S_t(x) \in \{0, 1, 2, 3\}$:
    - If $R(x) \ge 1$:
      $$S_{t+1}(x) = \begin{cases}
      0 & \text{if } S_t(x) = 3 \text{ (upper class targets of revolution are stripped of wealth)} \\
      1 & \text{otherwise (joining the working-class movement)}
      \end{cases}$$
    - If $R(x) = 0$:
      $$S_{t+1}(x) = \begin{cases}
      S_t(x) + 1 & \text{if } W(x) \ge 2 \cdot S_t(x) + 2 \text{ (social mobility / promotion)} \\
      \max(0, S_t(x) - 1) & \text{else if } W(x) < S_t(x) \text{ (economic decline / demotion)} \\
      S_t(x) & \text{otherwise}
      \end{cases}$$
* **Mathematical Rationale:**
  Models Turchin's theory of elite overproduction and structural-demographic cycles. Elites compete for resources; too many elites trigger revolutions (state 5). The revolutionary state spreads, demotes elites and upper-middle cells, and resets the system.
* **Expected Visual Behavior:**
  Periodic waves of revolution (state 5) that wipe out clusters of elites (state 4), followed by slow rebuilding of Middle and Elite classes, creating vertical, periodic socioeconomic cycles.

---

### Rule 9: Rumor Propagation with Skepticism
* **States ($N$):** $7$ states ($0, 1, 2, 3, 4, 5, 6$).
  * State $0$: Unaware (Susceptible).
  * State $1$: Active Believer (spreads rumor).
  * State $2$: Skeptical Believer (spreads rumor weakly).
  * State $3$: Inactive Believer (knows, doesn't spread).
  * State $4$: Skeptic (resistant, blocks spreading).
  * State $5$: Debunker (actively refutes).
  * State $6$: Recovery (refractory).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $B(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 1)$ (Active Believers).
  Let $S\!B(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 2)$ (Skeptical Believers).
  Let $D(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 5)$ (Debunkers).
  Let $Spreading(x) = B(x) + S\!B(x)$.
  
  * If $S_t(x) = 0$ (Unaware):
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } Spreading(x) \ge 2 \text{ and } D(x) \ge 1 \text{ (exposed but protected by debunkers)} \\
    1 & \text{else if } B(x) \ge 2 \text{ (convinced by active believers)} \\
    2 & \text{else if } Spreading(x) \ge 2 \text{ (convinced but skeptical)} \\
    0 & \text{otherwise}
    \end{cases}$$
  * If $S_t(x) = 1$ (Active Believer):
    $$S_{t+1}(x) = \begin{cases}
    4 & \text{if } D(x) \ge 1 \text{ (debunked)} \\
    2 & \text{otherwise (cools down to skeptical believer)}
    \end{cases}$$
  * If $S_t(x) = 2$ (Skeptical Believer):
    $$S_{t+1}(x) = 3 \text{ (becomes inactive)}$$
  * If $S_t(x) = 3$ (Inactive Believer):
    $$S_{t+1}(x) = 6 \text{ (recovers)}$$
  * If $S_t(x) = 4$ (Skeptic):
    $$S_{t+1}(x) = \begin{cases}
    2 & \text{if } B(x) \ge 3 \text{ (overwhelmed by rumors, starts believing)} \\
    5 & \text{otherwise (becomes an active debunker)}
    \end{cases}$$
  * If $S_t(x) = 5$ (Debunker):
    $$S_{t+1}(x) = 6 \text{ (exhausted)}$$
  * If $S_t(x) = 6$ (Recovery):
    $$S_{t+1}(x) = 0 \text{ (back to susceptible)}$$
* **Mathematical Rationale:**
  An epidemiological rumor model incorporating skeptics (who resist and can turn into debunkers) and debunkers (who actively suppress active rumor-mongers). This creates a complex epidemiological battle between truth, rumors, and skepticism.
* **Expected Visual Behavior:**
  Rumor waves (states 1 and 2) propagating outward, met by skeptic walls (state 4) which turn into debunker waves (state 5), extinguishing the rumor and leaving recovery trails (state 6).

---

### Rule 10: Spatial Ultimatum Game
* **States ($N$):** $5$ states ($0, 1, 2, 3, 4$).
  * State $0$: Rationalist (offers 2, accepts $\ge 1$).
  * State $1$: Fair-Player (offers 5, accepts $\ge 5$).
  * State $2$: Hyper-Fair (offers 8, accepts $\ge 3$).
  * State $3$: Spiteful (offers 2, accepts $\ge 5$).
  * State $4$: Mimic (acts like Fair-Player: offers 5, accepts $\ge 5$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
  Let $M(x) = \{x-1, x, x+1\}$ be the neighborhood including the cell itself.
* **Transition Function:**
  Let the offer $O(s)$ and acceptance threshold $T(s)$ for each state $s$ be:
  - $O(0) = 2, T(0) = 1$
  - $O(1) = 5, T(1) = 5$
  - $O(2) = 8, T(2) = 3$
  - $O(3) = 2, T(3) = 5$
  - $O(4) = 5, T(4) = 5$
  
  For two interacting states $s_1, s_2$:
  - Proposer payoff for $s_1$ against $s_2$:
    $$Prop(s_1, s_2) = \begin{cases} 10 - O(s_1) & \text{if } O(s_1) \ge T(s_2) \\ 0 & \text{otherwise} \end{cases}$$
  - Responder payoff for $s_1$ against $s_2$:
    $$Resp(s_1, s_2) = \begin{cases} O(s_2) & \text{if } O(s_2) \ge T(s_1) \\ 0 & \text{otherwise} \end{cases}$$
  - Combined pairwise payoff:
    $$G(s_1, s_2) = Prop(s_1, s_2) + Resp(s_1, s_2)$$
    
  For any cell $z$, its total payoff is:
  $$P_t(z) = G(S_t(z), S_t(z-1)) + G(S_t(z), S_t(z+1))$$
  
  At each step, cell $x$ identifies $y^* = \arg\max_{y \in M(x)} P_t(y)$. Ties are resolved by prioritizing self ($x$), then left ($x-1$), then right ($x+1$).
  
  The transition is:
  $$S_{t+1}(x) = \begin{cases}
  S_t(y^*) & \text{if } S_t(y^*) \neq 4 \\
  S_t(x) & \text{if } S_t(y^*) = 4 \text{ (keeps current strategy to avoid vacuous mimic loops)}
  \end{cases}$$
* **Mathematical Rationale:**
  Applies the Ultimatum Game to a spatial grid, where strategies compete based on the payoffs from proposers and responders. Spiteful players punish low offers from Rationalists but also fail to cooperate with each other, while Fair-players dominate if they cluster.
* **Expected Visual Behavior:**
  Complex fractal boundaries and pockets of Fair-players (state 1) surviving amidst Rationalists and Spiteful players.
