# Field Analysis and Reviewer Configuration

## Manuscript classification

- **Primary field:** theoretical computer science, especially propositional satisfiability, structural complexity, and exact optimization.
- **Secondary fields:** graph theory (independent domination and dominating induced matchings), combinatorial optimization, parameterized algorithms, and reproducible/formal mathematics.
- **Paper type:** theoretical paper with a computational research artifact. The universal claims live or die by written proofs; exhaustive computation supplies finite base values, regression evidence, and reproducibility records.
- **Central contribution under review:** whether the residual objective called bilateral deficiency is sufficiently intrinsic, distinct, and productive to count as a SAT-style parameter rather than notation extracted from an established domination reduction.
- **Target standard:** a strong specialist journal. The most natural current fits are *Theoretical Computer Science* and *Discrete Mathematics & Theoretical Computer Science*. A more complexity-centred revision could also be considered by *Journal of Computer and System Sciences*; a more algorithmic revision would need substantially more algorithmic development before an algorithms journal would be natural.
- **Current maturity:** complete pre-submission draft with a substantial artifact, not yet author-complete, formally verified, archived, or externally refereed.

## Five independent review lenses

### EIC — theoretical-computer-science editor

- **Identity:** associate editor handling structural complexity, reductions, and graph optimization.
- **Question:** Is the contribution clearly differentiated, appropriately scoped, and ready for a specialist journal?
- **Expected blind spot:** may underweight implementation-level assurance details.

### Reviewer 1 — proof and complexity methodology

- **Identity:** researcher in reductions, parameterized complexity, and exact algorithms.
- **Question:** Are the definitions, bijections, reductions, boundary cases, and parameterized claims logically complete?
- **Expected blind spot:** not the final authority on historical SAT-deficiency terminology.

### Reviewer 2 — SAT and graph-domination domain literature

- **Identity:** scholar working across clausal deficiency/autarkies, independent domination, domination polynomials, and dominating induced matchings.
- **Question:** Does the paper locate the closest antecedents and justify the claimed conceptual delta?
- **Expected blind spot:** may prefer established terminology even where the new packaging has operational value.

### Reviewer 3 — proof engineering and research software

- **Identity:** formal-methods and research-software specialist concerned with certificate semantics, reproducibility, and AI-assisted mathematics.
- **Question:** Do the artifact and prose preserve the boundary between theorem, finite computation, execution receipt, and independently checkable proof?
- **Expected blind spot:** may undervalue a clean mathematical result that lacks immediate proof-system integration.

### Devil's Advocate — reductive adversary

- **Identity:** complexity theorist instructed to construct the strongest case that the proposed parameter is redundant or the manuscript overstates completeness.
- **Question:** Can every claimed advance be collapsed into the 2008 cost decomposition, independent domination on formula graphs, or MaxSAT defect?
- **Expected blind spot:** intentionally optimized for falsification rather than balanced publication advice.

## Review protocol

Each reviewer reads the frozen manuscript and supplement without seeing the other reports. Reports use section references because the Markdown source is not paginated. The editorial synthesis is produced only after all five reports exist. Numerical scores are treated as ordinal aids, not empirical predictions of acceptance.
