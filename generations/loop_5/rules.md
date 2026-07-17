# Loop 5 Cellular Automata Rules: Neural Firing, Plasticity & Memory

This document contains 10 distinct, mathematically rigorous cellular automata (CA) rules focused on the domain of **Neural Firing, Plasticity & Memory**.

In this domain, the state transitions model the electrical activity of somatic membranes, the adaptation of thresholds, the strengthening or weakening of connections (plasticity), and chemical modulations (memory). Each rule is designed for a 1D lattice where the state of cell $x$ at discrete time step $t$ is denoted by $S_t(x) \in \{0, 1, \dots, N-1\}$.

---

## Summary of Rules

| Rule # | Name | States ($N$) | Neighborhood | Primary Mechanism | Key Visual Expectation |
|---|---|---|---|---|---|
| **1** | [Hebbian Synaptic Potentiation](#rule-1-hebbian-synaptic-potentiation) | 6 | Radius $r=1$ | Parallel weak/potentiated activity cycles | Intermittent high-velocity bursts and memory paths |
| **2** | [Spike-Timing-Dependent Plasticity (STDP)](#rule-2-spike-timing-dependent-plasticity-stdp) | 8 | Radius $r=1$ | Activity-correlated connection updates | Self-limiting directional wave propagation |
| **3** | [Excitatory-Inhibitory (E-I) Lattice](#rule-3-excitatory-inhibitory-e-i-lattice) | 4 | Radius $r=2$ | Spatial cell identity and hyperpolarization | Breathing structures, pacemakers, and localized blocks |
| **4** | [Glial-Modulated Synaptic Transmission](#rule-4-glial-modulated-synaptic-transmission) | 8 | Radius $r=1$ | Slow glial feedback modulating threshold | Wave envelopes with local persistent memory scars |
| **5** | [Spike-Rate Adaptation (SRA)](#rule-5-spike-rate-adaptation-sra) | 6 | Radius $r=2$ | Firing history raises threshold | Self-limiting wave bursts and periodic refractory gaps |
| **6** | [Synaptic Vesicle Depletion](#rule-6-synaptic-vesicle-depletion) | 5 | Radius $r=1$ | Firing depletes transmitter reserves | Fragmented, non-continuous waves and pulse trains |
| **7** | [Coincidence Detection Delay Lines](#rule-7-coincidence-detection-delay-lines) | 7 | Asymmetric $r=2$ | Synchrony-gated axonal delays | Multi-directional wave collisions triggering new pulses |
| **8** | [Retrograde Gas (NO) Modulated Potentiation](#rule-8-retrograde-gas-no-modulated-potentiation) | 6 | Radius $r=2$ | Diffusing retrograde gas lowers threshold | Broad, self-reinforcing wave envelopes |
| **9** | [Homeostatic Density Regulation](#rule-9-homeostatic-density-regulation) | 6 | Radius $r=2$ | Over- or under-excitation scales threshold | Homeostatic stabilization of wave density |
| **10** | [Metabolic Energy-Gated Firing](#rule-10-metabolic-energy-gated-firing) | 7 | Radius $r=1$ | Activity-dependent ATP depletion & recharge | Alternating bursts, fatigue pauses, and recovery waves |

---

## Rule Definitions

### Rule 1: Hebbian Synaptic Potentiation
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Quiescent Weak ($Q_W$).
  * State $1$: Excited Weak ($E_W$).
  * State $2$: Refractory Weak ($R_W$).
  * State $3$: Quiescent Potentiated ($Q_P$).
  * State $4$: Excited Potentiated ($E_P$).
  * State $5$: Refractory Potentiated ($R_P$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let the active firing neighbor count be:
  $$F_t(x) = \mathbb{I}(S_t(x-1) \in \{1, 4\}) + \mathbb{I}(S_t(x+1) \in \{1, 4\})$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } F_t(x) = 2 \\
  4 & \text{if } S_t(x) = 1 \text{ and } F_t(x) \ge 1 \quad \text{(Hebbian potentiation)} \\
  2 & \text{if } S_t(x) = 1 \text{ and } F_t(x) = 0 \quad \text{(Normal decay)} \\
  0 & \text{if } S_t(x) = 2 \\
  4 & \text{if } S_t(x) = 3 \text{ and } F_t(x) \ge 1 \quad \text{(Lowered threshold)} \\
  0 & \text{if } S_t(x) = 3 \text{ and } F_t(x) = 0 \quad \text{(Depotentiation/Forgetting)} \\
  5 & \text{if } S_t(x) = 4 \\
  3 & \text{if } S_t(x) = 5 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** This rule models synaptic plasticity by creating two parallel cycles of activity (Weak: $0 \to 1 \to 2 \to 0$ and Potentiated: $3 \to 4 \to 5 \to 3$). A weak cell requires high input density to fire ($F_t(x) = 2$). If a weak cell fires while a neighbor also fires, its connection is potentiated ($1 \to 4$). Once potentiated, the resting state is $3$, which has a lower firing threshold ($F_t(x) \ge 1$). Lack of activity causes the potentiated state to decay back to the weak state ($3 \to 0$).
* **Expected Visual Behavior:** High-velocity propagation bursts through potentiated pathways (state 3) and slower, sparser propagation through weak pathways. It creates transient traces that act as "memory channels" in the space-time diagram.

---

### Rule 2: Spike-Timing-Dependent Plasticity (STDP)
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * The state $S_t(x)$ is decomposed into two components:
    * Firing Activity: $a_t(x) = S_t(x) \pmod 2 \in \{0, 1\}$ (0 = Quiet, 1 = Firing).
    * Connection Weight: $w_t(x) = \lfloor S_t(x)/2 \rfloor \in \{0, 1, 2, 3\}$ (0 = Weakest, 3 = Strongest).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let the weighted neighbor activity input be:
  $$I_t(x) = w_t(x) \cdot (a_t(x-1) + a_t(x+1))$$
  * Activity Transition:
    $$a_{t+1}(x) = \begin{cases}
    1 & \text{if } a_t(x) = 0 \text{ and } I_t(x) \ge 2 \\
    0 & \text{otherwise}
    \end{cases}$$
  * Weight Transition:
    $$w_{t+1}(x) = \begin{cases}
    \min(3, w_t(x) + 1) & \text{if } a_{t+1}(x) = 1 \text{ and } (a_t(x-1) + a_t(x+1) \ge 1) \\
    \max(0, w_t(x) - 1) & \text{else if } a_t(x) = 1 \text{ and } (a_{t+1}(x-1) + a_{t+1}(x+1) \ge 1) \\
    w_t(x) & \text{otherwise}
    \end{cases}$$
  * Combined State:
    $$S_{t+1}(x) = 2 \cdot w_{t+1}(x) + a_{t+1}(x)$$
* **Mathematical Rationale:** STDP strengthens connections when a pre-synaptic firing event precedes a post-synaptic firing event (LTP) and weakens them when the order is reversed (LTD). Here, if a quiet cell fires ($a_{t+1}(x)=1$) immediately after a neighbor fired ($a_t(y)=1$), its weight increases. If it was firing ($a_t(x)=1$) and a neighbor fires next ($a_{t+1}(y)=1$), its weight decreases.
* **Expected Visual Behavior:** Waves of firing that leave a trail of modified connection weights. The boundaries of the waves are self-regulated by the LTD mechanism, preventing runaway expansion and creating structured, self-limiting directional wave corridors.

---

### Rule 3: Excitatory-Inhibitory (E-I) Lattice
* **States ($N$):** $4$ states ($0, 1, 2, 3$).
  * State $0$: Quiescent ($Q$).
  * State $1$: Firing ($F$).
  * State $2$: Refractory ($R$).
  * State $3$: Hyperpolarized ($H$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Lattice Heterogeneity:**
  * Cells at indices where $x \pmod 3 \in \{1, 2\}$ are designated as Excitatory (E).
  * Cells at indices where $x \pmod 3 = 0$ are designated as Inhibitory (I).
* **Transition Function:**
  Let $E_t(x)$ and $I_t(x)$ be the active excitatory and inhibitory neighbors, respectively:
  $$E_t(x) = \sum_{y \in N(x), y \pmod 3 \neq 0} \mathbb{I}(S_t(y) = 1)$$
  $$I_t(x) = \sum_{y \in N(x), y \pmod 3 = 0} \mathbb{I}(S_t(y) = 1)$$
  Let the net input be:
  $$A_t(x) = E_t(x) - 2 \cdot I_t(x)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } A_t(x) \ge 1 \\
  3 & \text{if } S_t(x) = 1 \text{ and } I_t(x) \ge 1 \quad \text{(Hyperpolarization)} \\
  2 & \text{if } S_t(x) = 1 \text{ and } I_t(x) = 0 \quad \text{(Normal Refractory)} \\
  0 & \text{if } S_t(x) = 2 \\
  1 & \text{if } S_t(x) = 3 \text{ and } A_t(x) \ge 2 \quad \text{(High threshold recovery)} \\
  0 & \text{if } S_t(x) = 3 \text{ and } A_t(x) < 2 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Real brains maintain a strict balance between excitation and inhibition. In this rule, spatial positions are heterogeneous (2 E-cells for every 1 I-cell). Firing inhibitory cells project a negative weight ($w = -2$), suppressing neighboring firing. Furthermore, active inhibition drives firing cells into a deep hyperpolarized state (3) instead of a standard refractory state (2), raising their activation threshold for the next step.
* **Expected Visual Behavior:** Self-organizing localized pacemakers and breathing structures. The spatial heterogeneity restricts continuous wave fronts, causing them to break into periodic oscillations and localized blocks.

---

### Rule 4: Glial-Modulated Synaptic Transmission
* **States ($N$):** $8$ states ($0, 1, \dots, 7$).
  * The state is decomposed into:
    * Neural Activity: $n_t(x) = S_t(x) \pmod 4 \in \{0, 1, 2, 3\}$ (0 = Quiescent, 1 = Firing, 2 = Refractory Phase 1, 3 = Refractory Phase 2).
    * Glial Modulation: $g_t(x) = \lfloor S_t(x)/4 \rfloor \in \{0, 1\}$ (0 = Normal, 1 = Potentiated/Glial Cloud).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $F_t(x) = \mathbb{I}(n_t(x-1) = 1) + \mathbb{I}(n_t(x+1) = 1)$ be the firing neighbor count.
  * Neural State transition $n_{t+1}(x)$:
    $$n_{t+1}(x) = \begin{cases}
    1 & \text{if } n_t(x) = 0 \text{ and } g_t(x) = 0 \text{ and } F_t(x) = 2 \\
    1 & \text{if } n_t(x) = 0 \text{ and } g_t(x) = 1 \text{ and } F_t(x) \ge 1 \\
    2 & \text{if } n_t(x) = 1 \\
    3 & \text{if } n_t(x) = 2 \\
    0 & \text{if } n_t(x) = 3 \\
    n_t(x) & \text{otherwise}
    \end{cases}$$
  * Glial State transition $g_{t+1}(x)$:
    $$g_{t+1}(x) = \begin{cases}
    1 & \text{if } n_t(x) = 1 \text{ and } F_t(x) \ge 1 \quad \text{(High-activity glial release)} \\
    0 & \text{if } n_t(x) = 0 \text{ and } F_t(x) = 0 \quad \text{(Glial clearance)} \\
    g_t(x) & \text{otherwise}
    \end{cases}$$
  * Combined State:
    $$S_{t+1}(x) = 4 \cdot g_{t+1}(x) + n_{t+1}(x)$$
* **Mathematical Rationale:** Astrocytes release gliotransmitters (such as glutamate) in response to high local firing, enhancing the synaptic gain of nearby neurons. Here, the slow-moving glial variable $g_t(x)$ records local activity. When $g_t(x) = 1$, the neural threshold to fire is halved (from $F=2$ to $F \ge 1$). The glial modulation only decays when the neuron and its neighbors are silent.
* **Expected Visual Behavior:** Large-scale "wave envelopes" that propagate easily through areas where glial clouds are active. Silent areas slowly freeze back into a high-threshold state, creating persistent memory scars and pathways in space-time.

---

### Rule 5: Spike-Rate Adaptation (SRA)
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Quiescent ($Q$).
  * State $1$: Firing ($F$).
  * State $2$: Refractory ($R$).
  * State $3$: Quiescent Habituated ($Q_H$).
  * State $4$: Firing Habituated ($F_H$).
  * State $5$: Refractory Habituated ($R_H$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $F_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{1, 4\})$ be the active firing neighbor count.
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } F_t(x) \ge 1 \\
  2 & \text{if } S_t(x) = 1 \\
  3 & \text{if } S_t(x) = 2 \quad \text{(Enters habituated state after firing)} \\
  4 & \text{if } S_t(x) = 3 \text{ and } F_t(x) \ge 3 \quad \text{(High threshold to re-fire)} \\
  0 & \text{if } S_t(x) = 3 \text{ and } F_t(x) < 3 \quad \text{(Recovers from habituation)} \\
  5 & \text{if } S_t(x) = 4 \\
  3 & \text{if } S_t(x) = 5 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Real neurons adapt to high-frequency stimulation by raising their threshold (habituation). In this rule, any firing event ($1$) transitions the cell into an habituated state ($3$). In this state, the cell requires at least $3$ active neighbors to fire again. If it fails to receive sufficient excitation, it returns to the normal quiescent state ($0$).
* **Expected Visual Behavior:** Self-limiting burst structures. An initial wave propagates easily (threshold 1), but leaves behind a trail of habituated cells (state 3) that acts as a barrier, causing subsequent wave trains to break up or freeze.

---

### Rule 6: Synaptic Vesicle Depletion
* **States ($N$):** $5$ states ($0, 1, \dots, 4$).
  * State $0$: Depleted Quiescent ($Q_D$, cannot transmit or fire).
  * State $1$: Partially Charged Quiescent ($Q_P$, high threshold).
  * State $2$: Fully Charged Quiescent ($Q_C$, normal threshold).
  * State $3$: Firing ($F$).
  * State $4$: Refractory ($R$).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $F_t(x) = \mathbb{I}(S_t(x-1) = 3) + \mathbb{I}(S_t(x+1) = 3)$ be the firing neighbor count.
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } S_t(x) = 2 \text{ and } F_t(x) \ge 1 \\
  3 & \text{if } S_t(x) = 1 \text{ and } F_t(x) = 2 \quad \text{(Low transmitter, needs more input)} \\
  2 & \text{if } S_t(x) = 1 \text{ and } F_t(x) < 2 \quad \text{(Recharges to full)} \\
  1 & \text{if } S_t(x) = 0 \quad \text{(Slowly recharges to partial)} \\
  4 & \text{if } S_t(x) = 3 \\
  0 & \text{if } S_t(x) = 4 \quad \text{(Enters depleted state after firing)} \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Short-term depression models the exhaustion of ready-releasable synaptic vesicles. In this rule, firing ($3$) empties the vesicle pool, forcing the cell into a depleted state ($0$) upon recovery. The cell must recharge sequentially ($0 \to 1 \to 2$). In the partially charged state ($1$), it has a higher firing threshold ($F_t(x) = 2$) than in the fully charged state ($F_t(x) \ge 1$).
* **Expected Visual Behavior:** Non-continuous propagation, where continuous wave fronts fragment into discrete "pulse trains". It prevents long-term sustained activity, instead generating sparse periodic waves.

---

### Rule 7: Coincidence Detection Delay Lines
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Quiescent ($Q$).
  * State $1$: Coincidence Hub ($C$).
  * States $2, 3, 4, 5$: Delay line stages.
  * State $6$: Firing Terminal ($T$, triggers neighbors).
* **Neighborhood ($N(x)$):** Asymmetric radius $r=2$:
  $$N(x) = \{x-2, x-1, x+1\}$$
* **Transition Function:**
  Let the active firing inputs in the neighborhood be:
  $$I_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 6)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \text{ and } I_t(x) \ge 2 \quad \text{(Coincidence detection)} \\
  S_t(x) + 1 & \text{if } 1 \le S_t(x) \le 5 \quad \text{(Axonal propagation)} \\
  0 & \text{if } S_t(x) = 6 \quad \text{(Decays to rest)} \\
  0 & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** In neural circuits, delay lines and coincidence detectors are used to compute spatial and temporal correlations. Here, a cell only fires ($1$) if it receives at least two inputs simultaneously ($I_t(x) \ge 2$). Once triggered, the signal propagates along a 5-step delay line ($2 \to 3 \to 4 \to 5 \to 6$) representing axonal conduction delay, before arriving at the terminal state $6$, which can excite neighbors.
* **Expected Visual Behavior:** Complex geometric interference patterns. Diagonal lines represent propagating delay lines. When two lines collide at a specific point, they register a coincidence, initiating a new set of propagating delay lines.

---

### Rule 8: Retrograde Gas (NO) Modulated Potentiation
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Quiescent ($Q$).
  * State $1$: Normal Firing ($F$).
  * State $2$: Normal Refractory ($R$).
  * State $3$: Gas Emission ($G$).
  * State $4$: Potentiated Firing ($F_P$).
  * State $5$: Potentiated Refractory ($R_P$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $F_t(x)$ and $G_t(x)$ be the counts of firing and gas-emitting neighbors:
  $$F_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) \in \{1, 4\})$$
  $$G_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 3)$$
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  4 & \text{if } S_t(x) = 0 \text{ and } G_t(x) \ge 1 \text{ and } F_t(x) \ge 1 \quad \text{(Retrograde potentiation)} \\
  1 & \text{if } S_t(x) = 0 \text{ and } G_t(x) = 0 \text{ and } F_t(x) \ge 2 \quad \text{(Normal threshold firing)} \\
  2 & \text{if } S_t(x) = 1 \\
  0 & \text{if } S_t(x) = 2 \\
  3 & \text{if } S_t(x) = 4 \quad \text{(Potentiated firing emits retrograde gas)} \\
  5 & \text{if } S_t(x) = 3 \\
  0 & \text{if } S_t(x) = 5 \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Retrograde messengers (like Nitric Oxide) are gases that diffuse backward from the post-synaptic neuron to the pre-synaptic terminal, facilitating future transmitter release. Here, a potentiated firing neuron ($4$) transitions to state $3$, emitting gas. This gas ($3$) lowers the firing threshold of neighboring quiescent cells ($0$) from $2$ to $1$, while also forcing them to enter the potentiated firing state ($4$) when triggered.
* **Expected Visual Behavior:** Broad, self-reinforcing wave envelopes. Once a localized region triggers potentiation, a "gas cloud" is established, driving a rapid expansion of the wavefront across the space-time grid.

---

### Rule 9: Homeostatic Density Regulation
* **States ($N$):** $6$ states ($0, 1, \dots, 5$).
  * State $0$: Normal Quiescent ($Q_N$, threshold = 2).
  * State $1$: Sensitized Quiescent ($Q_S$, threshold = 1).
  * State $2$: Desensitized Quiescent ($Q_D$, threshold = 4).
  * State $3$: Firing ($F$).
  * State $4$: Refractory ($R$).
  * State $5$: Deep Refractory ($R_D$).
* **Neighborhood ($N(x)$):** Radius $r=2$ excluding the cell itself:
  $$N(x) = \{x-2, x-1, x+1, x+2\}$$
* **Transition Function:**
  Let $F_t(x) = \sum_{y \in N(x)} \mathbb{I}(S_t(y) = 3)$ be the active firing neighbor count.
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  3 & \text{if } S_t(x) = 0 \text{ and } F_t(x) \ge 2 \\
  1 & \text{if } S_t(x) = 0 \text{ and } F_t(x) = 0 \quad \text{(Sensitizes under low activity)} \\
  3 & \text{if } S_t(x) = 1 \text{ and } F_t(x) \ge 1 \quad \text{(Fires easily)} \\
  3 & \text{if } S_t(x) = 2 \text{ and } F_t(x) \ge 4 \quad \text{(Fires only under extreme pressure)} \\
  0 & \text{if } S_t(x) = 2 \text{ and } F_t(x) = 0 \quad \text{(Decays back to normal)} \\
  5 & \text{if } S_t(x) = 3 \text{ and } F_t(x) \ge 3 \quad \text{(Over-excitation causes deep refractory)} \\
  4 & \text{if } S_t(x) = 3 \text{ and } F_t(x) < 3 \quad \text{(Normal refractory)} \\
  0 & \text{if } S_t(x) = 4 \\
  2 & \text{if } S_t(x) = 5 \quad \text{(Enters desensitized state)} \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Homeostatic plasticity stabilizes network activity by scaling weights or intrinsic excitability. In this rule, if a cell is quiescent and receives no stimulation ($F_t(x) = 0$), it sensitizes ($1$), dropping its threshold to $1$. Conversely, if it fires under high local stimulation ($F_t(x) \ge 3$), it enters a deep refractory state ($5$) that decays into a desensitized quiescent state ($2$), raising its threshold to $4$.
* **Expected Visual Behavior:** Extremely stable average firing densities. The space-time diagram will self-regulate to prevent both silent extinction and chaotic overgrowth, resulting in uniform, lattice-like distribution of firing pulses.

---

### Rule 10: Metabolic Energy-Gated Firing
* **States ($N$):** $7$ states ($0, 1, \dots, 6$).
  * State $0$: Quiet, Exhausted ($Q_E$, no energy, cannot fire).
  * State $1$: Quiet, Charged ($Q_C$, normal energy, threshold = 1).
  * State $2$: Quiet, Hyper-Charged ($Q_H$, high energy, threshold = 1).
  * State $3$: Firing from Charged ($F_C$).
  * State $4$: Firing from Hyper-Charged ($F_H$).
  * State $5$: Refractory Low ($R_L$, recovering to exhausted state).
  * State $6$: Refractory High ($R_H$, recovering to charged state).
* **Neighborhood ($N(x)$):** Radius $r=1$ excluding the cell itself:
  $$N(x) = \{x-1, x+1\}$$
* **Transition Function:**
  Let $F_t(x) = \mathbb{I}(S_t(x-1) \in \{3, 4\}) + \mathbb{I}(S_t(x+1) \in \{3, 4\})$ be the firing neighbor count.
  The transition is defined as:
  $$S_{t+1}(x) = \begin{cases}
  1 & \text{if } S_t(x) = 0 \quad \text{(Recharges energy)} \\
  3 & \text{if } S_t(x) = 1 \text{ and } F_t(x) \ge 1 \quad \text{(Fires, depletes charge)} \\
  2 & \text{if } S_t(x) = 1 \text{ and } F_t(x) = 0 \quad \text{(Accumulates extra energy)} \\
  4 & \text{if } S_t(x) = 2 \text{ and } F_t(x) \ge 1 \quad \text{(Fires with reserve energy)} \\
  2 & \text{if } S_t(x) = 2 \text{ and } F_t(x) = 0 \quad \text{(Stays hyper-charged)} \\
  5 & \text{if } S_t(x) = 3 \quad \text{(Decays to low refractory)} \\
  6 & \text{if } S_t(x) = 4 \quad \text{(Decays to high refractory)} \\
  0 & \text{if } S_t(x) = 5 \quad \text{(Recovers exhausted)} \\
  1 & \text{if } S_t(x) = 6 \quad \text{(Recovers charged)} \\
  S_t(x) & \text{otherwise}
  \end{cases}$$
* **Mathematical Rationale:** Neural excitation is constrained by metabolic limits (ATP availability). In this rule, firing depletes energy. If a neuron fires from a normal charged state ($1 \to 3$), it decays through $5 \to 0$ (exhausted), requiring an extra step to recharge. If it fires from a hyper-charged state ($2 \to 4$) which it reached by remaining inactive, it decays through $6 \to 1$, avoiding the exhausted state.
* **Expected Visual Behavior:** Alternating periods of high-frequency bursts and collective silence. When waves pass through, they exhaust the cells, causing a temporary "pausing" or gap in the space-time propagation until metabolic recharging is complete.
