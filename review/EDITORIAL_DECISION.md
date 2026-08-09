# Editorial Decision

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission draft
- **Decision date:** 8 August 2026
- **Review round:** 1

## Decision

### Major Revision

The manuscript contains a credible specialist-journal contribution, and no reviewer identified an obvious fatal error in the main universal theorem architecture. It is not yet independently checkable or historically positioned at the standard required for its flagship classification and “parameter in its own right” claims.

## Reviewer summary

| Reviewer | Role | Recommendation | Confidence |
|---|---|---|---:|
| EIC | theoretical-CS handling editor | Major Revision | 4/5 |
| R1 | proof and complexity methodology | Major Revision | 4/5 |
| R2 | SAT and graph-theory domain | Major Revision | 4/5 |
| R3 | proof engineering and research software | Major Revision | 4/5 |
| DA | reductive adversary | strongest case against present publication | n/a |

The four scored weighted averages are 78.1, 76.4, 75.7, and 79.2. They fall in the rubric's nominal minor-revision band, but every scored reviewer applied a linchpin override because the same unclosed base-value and standalone-presentation issue supports central claims.

## Consensus analysis

### Points of agreement

**[CONSENSUS-4] Main architecture is promising.** EIC S2, R1 S1–S3, R2 S2–S3, and R3 S1–S2 all identify the bijection and downstream theorem sequence as coherent and potentially publishable. None reports a visible fatal contradiction in Theorems 2, 4–7, 9, or 10.

**[CONSENSUS-4] The positive base is the principal proof-assurance gap.** EIC W1, R1 W1, R2 W5, and R3 W1 require the explicit component and stronger support for \(\beta(P)\ge1\). The DA makes the same point in Objection 5. This is the highest-priority revision because it controls separation, the positive spectrum, positive benchmarks, and part of the compact-proof claim.

**[CONSENSUS-4] Claim boundaries are unusually honest.** EIC S1/S3, R1's reproducibility comments, R2 S1, and R3 S1 all credit the distinction between the 2008 antecedent, the new theory, and the differing roles of mathematical proof and computation.

**[CONSENSUS-3] Historical positioning needs substantive expansion.** EIC W2 and R2 W1–W4 treat it as major; R1 asks for exact algorithmic pinpoints; R3 focuses elsewhere. The DA argues that inadequate lineage leaves the repackaging objection viable.

**[CONSENSUS-3] The artifact is strong but not yet archival.** EIC W3, R3 W2–W4, and R1 W1 require a durable, specifically identified proof/checker/release boundary. R2 asks that the positive component be inspectable within the article.

### Points of disagreement

**Disagreement 1: Is the paper already more than a renaming exercise?**

- **EIC/R1/R2 view:** The bijection, algebra, complexity results, and regular-DIM coordinate collectively create a meaningful new theory even though the cost arithmetic is antecedent.
- **DA view:** Most results may be standard transport, direct-product algebra, or lexicographic weighting after the parameter is defined to mirror independent domination.
- **Resolution:** The balanced reviews carry the publication judgment, but the adversarial objection is not dismissed. The revision must add a sharper antecedent comparison and foreground formula-native consequences such as the width-two Hall theorem, exact MILP, residual search problem, and any newly obtained structural result. A new connected theorem would be valuable but is not mandatory if the originality claim remains narrow.

**Disagreement 2: How serious is the bounded-treewidth statement?**

- **R1 view:** The full-polynomial and complexity claim requires theorem-level source support and output-bit analysis.
- **Other reviewers:** No direct error identified; the issue was not central to their lenses.
- **Resolution:** Treat as a required major clarification because optimization, total counting, and size-refined counting are different claims. Weakening to the exact published guarantee is acceptable.

**Disagreement 3: Are current benchmarks evidence of a broad benchmarking use?**

- **R3/DA view:** They are narrow disjoint-union conformance tests, not representative hardness evidence.
- **EIC/R1/R2 view:** The algebraic construction is a legitimate controlled use when appropriately scoped.
- **Resolution:** Rename them “algebraic conformance benchmarks” and preserve the existing disclaimer. No empirical solver study is required for the current theoretical paper.

## Decision rationale

The manuscript clears the threshold for revision rather than rejection because the central bijection has a complete inverse, the width-two and lifting arguments expose genuine combinatorial structure, the complexity reductions are largely explicit, and the regular-DIM edge count yields a useful exact gap identity. The paper also handles degenerate indexed formulas and evidence boundaries more carefully than is typical for an initial computational-theory submission. These strengths answer much, though not all, of the objection that the work merely names a known cost.

Major rather than minor revision is required because one finite premise controls several headline claims and is presently supported only by separately implemented exhaustive computation. The manuscript itself acknowledges that a receipt is not a certificate. The paper must therefore either provide an independently checkable lower-bound proof or recast those dependent results as explicitly computer-assisted with a small trusted checker and complete archive. In parallel, the exact positive formula must appear in the article, the 2008 antecedent and polynomial lineage need precise bibliographic treatment, the MaxCut reduction and width-two incidence terminology need local repairs, and the bounded-treewidth counting consequence must be sourced at theorem level or weakened. These issues are substantial but tractable in one revision cycle; they do not require abandoning the central definition or proof architecture.

## Required revisions

| # | Revision item | Source | Severity | Section | Acceptance criterion |
|---|---|---|---|---|---|
| R1 | Make the positive exact-\((3,2,2)\) base explicit and independently checkable | all reviewers, DA | Critical | 4, 6, appendix, supplement | formula, upper witness, lower-bound proof status, checker/proof data, and hashes are present |
| R2 | Complete and report a specialist priority/lineage audit | EIC, R2, DA | Major | 2, references | closest collision pinpointed; databases/queries/date/stopping rule reported; wording recalibrated |
| R3 | Repair proof specifications | R1 | Major/minor bundle | 5 | MaxCut threshold totality, signed-occurrence Hall object, binary MILP domains, and exact sign convention stated |
| R4 | Substantiate or narrow bounded-treewidth counting | R1 | Major | 5.6 | exact cited theorem and output model supplied, or claim narrowed to what the source proves |
| R5 | Produce an immutable artifact boundary | EIC, R3 | Major | declarations, supplement | versioned manifest, source hashes, proof/checker hashes, license, reproducible commands, archive identifier or explicit pre-deposition status |
| R6 | Remove unsupported independence/benchmark breadth language | R3, DA | Major/minor | 7–8, supplement | “separately implemented” and “algebraic conformance benchmarks” used unless stronger evidence is documented |

### Required item details

**R1: Positive-base certification**

- **Problem:** \(\beta(P)=1\) is a premise of the spectrum and separation claims, but the paper does not state \(P\) and the lower bound is an execution receipt.
- **Requirement:** Add an appendix listing \(P\), its clause/occurrence properties, a bilateral witness of value 1, and the exact lower-bound assurance. Prefer a standard unsatisfiability or pseudo-Boolean proof with a small checker. If unavailable, label the dependent statements computer-assisted and archive enough information for independent rechecking.
- **Acceptance criterion:** A reader can identify the exact bytes and validate the lower-bound claim without trusting the exhaustive solver's status summary.

**R2: Priority and lineage**

- **Problem:** The naming/contribution claim spans terminology not covered by the current short bibliography.
- **Requirement:** Search specialist databases and citation neighborhoods; inspect partial-assignment, residual deficiency/surplus, bipolar restriction, hypergraph/transversal, independent-domination polynomial, and formula-graph terminology. Add the exact 2008 page/equation or construction pinpoint and the earliest located polynomial source.
- **Acceptance criterion:** The paper reports a reproducible search boundary and its wording would remain correct if a close but non-identical antecedent is later found.

**R3: Proof specification repairs**

- **Problem:** Theorem 9 omits \(0\le K\le m\); Theorem 7 mixes simple incidence adjacency with signed occurrence counts; the MILP variable domains are implicit.
- **Requirement:** Repair all three points and define the decision threshold encoding/sign convention.
- **Acceptance criterion:** Each proof is a total formal argument under its declared inputs, including tautological width-two clauses and trivial MaxCut thresholds.

**R4: Bounded-treewidth claim**

- **Problem:** Full size-refined polynomial counting is stronger than generic optimization or total counting.
- **Requirement:** Identify the exact theorem and arithmetic/output-cost model, derive size refinement explicitly, or weaken the claim.
- **Acceptance criterion:** Every algorithmic consequence is directly supported by a cited theorem plus a written reduction.

**R5: Artifact release boundary**

- **Problem:** The current package is locally reproducible but has no immutable scholarly identity.
- **Requirement:** Add a mechanically generated top-level manifest, license/citation metadata, clean source-to-result instructions, and proof/checker bindings. Deposit when author authority permits; until then mark the object “candidate archive,” not “released.”
- **Acceptance criterion:** All normative files and generated proof objects are bound to one version and the prose does not imply public archival status prematurely.

## Suggested revisions

| # | Revision item | Source | Priority | Expected improvement |
|---|---|---|---|---|
| S1 | Add a compact comparison table for ordinary/max deficiency, surplus/autarky, MaxSAT defect, and the 2008 cost | R2, DA | P2 | makes conceptual delta auditable |
| S2 | Rename Theorem 1 as a characterization proposition and scope “complete” in the same sentence | EIC | P2 | reduces rhetorical inflation |
| S3 | Add invariance questions under autarky reduction, pure-literal elimination, and common SAT preprocessing | R2, DA | P2 | opens a formula-native research programme |
| S4 | Add malformed-input, overflow-bound, and untrusted-manifest threat-model notes/tests | R3 | P2 | hardens artifact assurance |
| S5 | Use one English spelling convention | EIC | P3 | copyediting consistency |
| S6 | Add connected composition/recognition questions prominently | DA | P2 | acknowledges the present classification boundary |

## Revision roadmap

### Priority 1 — proof linchpins

- [ ] R1: explicit positive component and lower-bound proof/checker boundary
- [ ] R3: repair reduction and incidence specifications
- [ ] R4: verify or narrow the treewidth claim

### Priority 2 — scholarly positioning

- [ ] R2: reproducible specialist-priority audit and exact antecedent pinpoints
- [ ] S1–S3: comparison table, scoped terminology, and SAT-native research questions

### Priority 3 — archive and presentation

- [ ] R5–R6: candidate release manifest, provenance wording, conformance-benchmark label
- [ ] S4–S6: threat model, spelling, and open-problem refinements
- [ ] Complete author, CRediT, funding, interest, repository, and DOI fields before actual submission

## Recommended revision deadline

- **Date:** 3 October 2026
- **Basis:** eight weeks for a major revision
- **External dependencies:** author metadata, specialist database access, public repository selection, DOI deposition, and any signed authorship declarations cannot be completed without the responsible human author.

## Closing

The reviewers find a real and potentially publishable theorem architecture. A revised submission should concentrate on making its strongest finite premise independently checkable, its historical delta auditable, and its artifact immutable. The revised manuscript should undergo another proof and domain review before submission.
