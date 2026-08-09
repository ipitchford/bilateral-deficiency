# Paper configuration, source corpus, outline, and argument blueprint

**Status:** planning record; superseded by the completed manuscript on
9 August 2026. Section allocations below describe the initial architecture,
not the final theorem inventory.

## Configuration record

| Field | Selection |
|---|---|
| Paper type | Original theoretical research article |
| Disciplines | SAT, computational complexity, graph theory |
| Target | Journal-neutral preprint; adaptable to *Theoretical Computer Science* or DMTCS |
| Working title | *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs* |
| Main language | English |
| Abstracts | English and independently written Traditional Chinese |
| Citations | Numbered mathematical style with verified DOI/URL metadata |
| Target length | approximately 10,000 words, excluding abstracts, references, and appendices |
| Outputs | Markdown, LaTeX/BibTeX, PDF, reproducibility supplement, artifact archive |
| Authorship | Placeholders only; no invented author identity |
| Existing materials | Stage 1 report, clean-room Python reference implementation, C++ exact solver, tests, benchmark packages |

## Phase 1 source corpus and search boundary

The source corpus is inherited from the completed research stage. Inclusion
required a direct connection to at least one of the following: formula graphs
and independent domination, CNF deficiency and residual structure, exact
occurrence SAT, MaxSAT/Almost-2-SAT, bounded-treewidth domination algorithms,
or independent-domination generating polynomials. Publisher records, open full
texts, DOI metadata, and primary papers were preferred. Search absence is not
treated as proof of priority.

| Source | Role in the paper | Position relative to the contribution |
|---|---|---|
| Chlebík & Chlebíková (2008) | Literal-pair graph with replicated clause vertices and exact partial-assignment cost decomposition | Closest antecedent; narrows originality claim |
| Zverovich (2006) | Satgraph with clause clique and SAT/independent-domination equivalence | Related architecture; clique collapses mixed optimisation |
| Zhang, Peitl & Szeider (2024) | Clause-literal encodings and exact occurrence bounds | Architecture and bounded-occurrence antecedent |
| Ahadi & Dehghan (2019) | Twice-positive/twice-negative 3-SAT hardness | Formula-class antecedent; does not determine the sign of beta |
| Kullmann (2011) | Deficiency, autarkies, lean kernels | Closest SAT parameter theory; different optimisation domain |
| Szeider (2004) | Maximum deficiency and parameterised SAT | Computational comparison |
| Garey, Johnson & Stockmeyer (1976) | Simple MaxCut NP-completeness | Hardness source for width two and sign dichotomy |
| Razgon & O'Sullivan (2009) | Almost-2-SAT fixed-parameter algorithm | Width-two algorithmic consequence |
| Focke et al. (2025) | Generalised domination on bounded-treewidth graphs | Treewidth algorithmic consequence |
| Jahari & Alikhani (2018) | Independent domination polynomial | Generating-polynomial context |
| TxGraffiti 4.0.0-rc1 package | Verified positive exact-(3,2,2) base instance | Finite object only; not authority for general theorems |

## Structure selection

The paper uses an adapted **Theoretical Analysis** structure. A standard social-
science theoretical template would separate background, critique, extension,
and applications. For a mathematical paper, proof dependencies require a more
specific sequence: prior-art boundary, definitions, structural theorems,
algebra, complexity, graph classification, applications, and assurance.

## Detailed outline

### Abstract (250 English words; Traditional Chinese abstract separate)

**Purpose:** State the parameter, principal theorem, algebraic and complexity
results, regular-DIM classification, and bounded novelty claim. Distinguish
written theorems from finite computational verification.

### 1. Introduction (650 words)

**Purpose:** Pose the theoretical question: when a formula-graph counterexample
mechanism produces a residual objective, is that objective a genuine SAT
parameter or disposable notation?

- Define the evaluation criteria for a distinct optimisation parameter.
- Summarise the main contributions without claiming global priority.
- State the six application questions and the qualified answers.
- Give a paper roadmap.

**Evidence:** TxGraffiti package for motivation; Chlebík--Chlebíková and
Zverovich for historical framing.

**Transition:** The originality claim can only be evaluated after the closest
formula-graph and deficiency antecedents are separated precisely.

### 2. Prior art and claim boundary (900 words)

**Purpose:** Establish what is and is not new before presenting theorems.

- **2.1 Formula-graph antecedents:** Zverovich's clause clique; the ordinary
  independent clause side; Zhang--Peitl--Szeider.
- **2.2 The 2008 cost decomposition:** derive
  \(|D|=k+t|T|-|U|\) from Chlebík--Chlebíková and identify the missing bilateral
  feasible-domain/converse/optimisation steps.
- **2.3 Deficiency theory:** contrast ordinary deficiency, maximum deficiency,
  surplus, autarky, and lean-kernel domains.
- **2.4 Priority statement:** apparently new as an explicit parameter and full
  theory after bounded search; underlying cost decomposition is prior art.

**Evidence:** Chlebík & Chlebíková; Zverovich; Zhang et al.; Ahadi & Dehghan;
Kullmann; Szeider.

**Transition:** With the priority boundary fixed, the parameter can be defined
without retrofitting novelty into the notation.

### 3. Bilateral residuals and the formula-graph bijection (1,300 words)

**Purpose:** Establish the universal structural foundation.

- **3.1 Indexed semantics:** explicit variable set, indexed duplicate clauses,
  tautologies, empty clauses, restriction by a partial assignment.
- **3.2 Residual-core theorem:** bilateral assignments are exactly restrictions
  whose surviving variables form a bipolar residual; beta is its least
  clause-variable deficiency.
- **3.3 Size-preserving bijection:** prove both maps between bilateral
  assignments and independent dominating sets and show they are inverse.
- **3.4 Polynomial identity:** derive
  \(D_i(G(F),z)=z^kB_F(z)\), including multiplicities.
- **3.5 Replicated-clause bridge:** define weighted beta and recover the 2008
  construction as \(G(F^{[t]})\).

**Evidence:** Original proofs; Chlebík--Chlebíková for the bridge; Jahari--
Alikhani for graph-polynomial context.

**Transition:** The bijection makes beta structurally meaningful; algebraic and
separation theorems determine whether it has an independent formula-side life.

### 4. Separation and algebra (1,200 words)

**Purpose:** Prove that beta is not determined by standard SAT quantities and
has nontrivial closure behaviour.

- **4.1 Separation examples:** same ordinary and maximum deficiency but
  different beta; satisfiable negative-beta and unsatisfiable nonpositive-beta
  formulas; distinction from MaxSAT above width two.
- **4.2 Additivity:** prove beta additivity and Laurent-polynomial convolution.
- **4.3 Exact width lift:** preserve beta while raising exact width and retaining
  proper simple structure.
- **4.4 Clause replication:** recover the complete MaxSAT optimum and interpret
  the number of optimally unassigned variables.

**Evidence:** Original proofs and clean-room exhaustive cross-checks.

**Transition:** These operations expose both easy and hard computational
regimes, motivating a sharp complexity analysis.

### 5. Complexity and algorithm selection (1,700 words)

**Purpose:** Establish a nontrivial computational theory and derive solver
guidance.

- **5.1 Membership and baseline enumeration:** beta-threshold is in NP; exact
  ternary enumeration uses \(O(3^k\|F\|)\) time.
- **5.2 Width-two theorem:** prove beta equals the MaxSAT defect via Hall's
  theorem, including duplicate, unit, empty, and tautological clauses.
- **5.3 Width-two consequences:** sign in P, arbitrary thresholds NP-complete
  through Simple MaxCut, threshold-FPT through Almost-2-SAT.
- **5.4 Width-three sign hardness:** prove the negative exact-(3,2,2) gadget,
  fixed-threshold NP-completeness for proper simple exact width at least three,
  and para-NP-hardness in the threshold alone.
- **5.5 Bounded incidence treewidth:** transfer a tree decomposition to the
  formula graph and invoke generalised-domination algorithms.
- **5.6 Solver decision table:** theorem-level routing, not an empirical claim
  of fastest implementation.

**Evidence:** Original reductions and proofs; Garey et al.; Razgon--O'Sullivan;
Focke et al.

**Transition:** Complexity explains how beta is computed. The next section
shows what the value means throughout a graph class.

### 6. Regular graphs with a dominating induced matching (900 words)

**Purpose:** Give a surjective coordinatisation and exact gap classification.

- Orient a specified dominating induced matching and reconstruct an indexed
  signed-occurrence formula, allowing tautological clauses.
- Prove the converse formula-to-graph construction.
- Derive vertex and edge counts.
- Prove \(\mu^*=k\) by the explicit matching and edge-domination lower bound.
- Conclude \(i(G)-\mu^*(G)=\beta(F_M)\).
- Prove the full integer spectrum in the proper exact-(3,2,2) subclass using
  verified positive and negative components.

**Evidence:** Original proof; finite values independently reproduced by the
artifact.

**Transition:** Classification converts the six proposed uses from speculation
into theorem-backed workflows whose limitations can be assessed individually.

### 7. Applications and mathematical infrastructure (850 words)

**Purpose:** Answer the six questions with evidence-calibrated verdicts.

- **7.1 Systematic discovery:** exact criterion within the formula-generated
  regular-DIM family; complexity qualification.
- **7.2 Proof production:** upper witnesses, lower proof trees or proof logs,
  and compositional certificates; no uniform short lower certificates claimed.
- **7.3 Solver selection:** map syntactic structure to MaxSAT, ternary search,
  treewidth DP, or independent-domination methods.
- **7.4 Controlled benchmarks:** width lift, replication, additivity, and
  verified prescribed-value instances.
- **7.5 Family classification:** state exactly what beta classifies and what it
  does not.
- **7.6 AI-assisted mathematics:** claim-evidence pipeline and safeguards;
  technical suitability rather than adoption.

**Evidence:** Artifact outputs, universal theorems, and exact finite receipts.

**Transition:** Infrastructure claims require a transparent trust and
missingness audit.

### 8. Reproducibility, limitations, and open problems (300 words)

**Purpose:** Separate proof, finite verification, novelty search, and future
work.

- Clean-room implementation boundary and cross-model tests.
- Corrected implementation bug as evidence for independent checks.
- Open exact-(3,2,2) sign complexity; connected positive amplification is
  settled later in Theorem 12, while arbitrary signed connected realization
  remains open.
- No global priority, formal verification, peer review, or community-adoption
  claim.

**Transition:** The conclusion can now state the strongest established thesis
without exceeding these boundaries.

### 9. Conclusion (200 words)

**Purpose:** Synthesize the structural, algebraic, computational, and graph-
classification evidence proving that beta is a distinct parameter. Reiterate
the bounded novelty claim and the qualified status of the infrastructure use.

## Word-count allocation

| Section | Target words |
|---|---:|
| 1. Introduction | 650 |
| 2. Prior art and claim boundary | 900 |
| 3. Residuals and bijection | 1,300 |
| 4. Separation and algebra | 1,200 |
| 5. Complexity and algorithms | 1,700 |
| 6. Regular-DIM classification | 900 |
| 7. Applications and infrastructure | 850 |
| 8. Reproducibility and limitations | 300 |
| 9. Conclusion | 200 |
| **Total** | **8,000** |

## Evidence map

| Paper section | Assigned sources or evidence | Function | Stance |
|---|---|---|---|
| 1 | TxGraffiti package; Chlebík--Chlebíková; Zverovich | Motivation and problem framing | Neutral/context |
| 2.1 | Zverovich; Zhang et al.; Ahadi--Dehghan | Architecture and formula-class antecedents | Narrows novelty |
| 2.2 | Chlebík--Chlebíková | Closest cost-decomposition antecedent | Strong counterevidence to broad originality |
| 2.3 | Kullmann; Szeider | Deficiency-domain comparison | Supports distinct optimisation domain |
| 3 | Original proofs; Jahari--Alikhani | Bijection and polynomial context | Supports structural thesis |
| 4 | Original proofs; clean-room tests | Separation and algebra | Supports distinctness |
| 5.2--5.3 | Garey et al.; Razgon--O'Sullivan | Width-two hardness and FPT consequences | Supports computational theory |
| 5.5 | Focke et al. | Bounded-treewidth algorithms | Supports algorithm routing |
| 6 | Original proofs; positive and negative receipts | Graph-family classification | Supports family-wide thesis |
| 7 | Prototype, tests, benchmark manifests | Six practical uses | Supports qualified application claims |
| 8 | Test logs, assurance boundary, literature search record | Limitations and reproducibility | Qualifies all claims |

Every included source is assigned. No literature source is used as authority
for a theorem proved in the paper; citations identify antecedents or imported
complexity results.

## Argument blueprint

### Central thesis

Bilateral deficiency is a distinct SAT-style optimisation parameter because it
has a formula-native residual domain, exactly and bijectively translates
independent domination on formula graphs, exhibits algebraic and computational
behaviour not determined by satisfiability or standard deficiency, and is the
complete signed gap coordinate for regular graphs with a specified dominating
induced matching. Its underlying cost decomposition has 2008 prior art, so the
originality claim concerns the explicit parameter and theory rather than the
first appearance of the cost expression.

### Sub-argument A: structural independence

- **Claim:** Beta is the minimum ordinary deficiency over bipolar residuals and
  preserves the full independent-dominating-set spectrum.
- **Evidence:** Residual-core theorem; size-preserving bijection; polynomial
  identity; exhaustive small-formula cross-model tests.
- **Reasoning:** A separately defined formula domain with an invertible graph
  translation is more than notation for one finite optimum.
- **Counter-argument:** Beta is merely \(i(G(F))-k\) written on formulas.
- **Response:** The residual definition does not mention graphs and yields
  formula-side theorems (width two, lift, replication, additivity) that are not
  consequences of one graph value alone.

### Sub-argument B: nontrivial algebra and computation

- **Claim:** Beta has closure laws, an integer spectrum, tractable islands, and
  sharp hardness transitions.
- **Evidence:** Additivity, convolution, width lift, MaxSAT recovery,
  width-two equality, exact-width sign hardness, bounded-treewidth transfer.
- **Counter-argument:** These are routine corollaries of generic independent
  domination.
- **Response:** The width-two Hall argument and replication identity are
  formula-specific; the width lift preserves exact CNF structure in a way that
  generic graph algorithms do not express.

### Sub-argument C: complete regular-DIM classification

- **Claim:** For every regular graph with a specified dominating induced
  matching, beta is exactly \(i-\mu^*\).
- **Evidence:** Bidirectional coordinatisation, edge count, matching lower
  bound, master bijection.
- **Counter-argument:** The theorem covers only formula-generated examples.
- **Response:** The graph-to-formula construction is surjective for the entire
  specified-M class, including tautological clauses.

### Sub-argument D: six operational uses

- **Claim:** The parameter supports systematic discovery, proof packaging,
  theorem-driven solver routing, controlled benchmarks, family classification,
  and an AI-mathematics claim-evidence interface.
- **Evidence:** Analyzer, exact solver, compositional generator/checker,
  mutation test, generated values, theorem table.
- **Counter-argument:** A prototype cannot prove usefulness or adoption.
- **Response:** Claim technical capability only. Do not infer solver dominance,
  community uptake, or peer acceptance.

### Sub-argument E: originality survives the corrected antecedent only in bounded form

- **Claim:** The explicit residual parameter and developed theory appear new
  after bounded search.
- **Evidence:** Definition-by-definition comparison with the closest inspected
  sources.
- **Counter-argument:** Chlebík--Chlebíková already wrote the same cost.
- **Response:** Concede the cost decomposition fully. Attribute it, then isolate
  the additional feasible-domain characterization, converse bijection,
  optimisation parameter, algebra, complexity, and graph classification. State
  that global priority is not secured.

## Logical dependency flow

```text
Indexed residual semantics
        |
        +--> bipolar residual theorem
        |
        +--> bilateral assignment <--> independent dominating set
                         |
                         +--> optimum identity
                         +--> solution polynomial
                         +--> regular-DIM gap theorem
        |
        +--> additivity --> compositional certificates and benchmarks
        +--> width lift --> fixed-width hardness and width-controlled families
        +--> replication --> weighted 2008 bridge and MaxSAT recovery
        +--> width-two Hall theorem --> 2-SAT/Almost-2-SAT routing
                         |
                         +--> six application assessments
```

## Argument-strength audit

| Sub-argument | Evidence strength | Logical status | Residual risk |
|---|---|---|---|
| Structural independence | Strong | Direct universal proofs plus exhaustive edge-case tests | Formalisation not yet completed |
| Algebra and complexity | Strong | Direct proofs; imported hardness/FPT facts sourced | Exact-(3,2,2) sign remains open |
| Regular-DIM classification | Strong | Surjective construction and elementary matching count | Connected amplification unresolved |
| Six operational uses | Moderate to strong | Four uses constructive; two necessarily qualified | Practical solver performance and adoption unmeasured |
| Bounded originality | Moderate | Targeted source comparison with a material correction | Global priority cannot be proved by finite search |

## Notes for drafting

- Use “distinct parameter” for the mathematical conclusion and “appears new
  after bounded search” for priority.
- Attribute the 2008 cost decomposition at first presentation.
- Never use finite test results as proof of universal statements.
- Distinguish a receipt from a proof certificate.
- Treat “systematic” as a complete criterion within a class, not as efficient.
- Treat “AI infrastructure” as a demonstrated interface, not a sociological
  forecast.
- Keep the exact-(3,2,2) sign problem and connected amplification explicitly
  open.
