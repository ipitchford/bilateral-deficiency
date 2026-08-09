# Peer Review Report — Proof and Complexity Methodology

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission draft
- **Review date:** 8 August 2026
- **Review round:** 1

## Reviewer information

- **Role:** Peer Reviewer 1 (Methodology)
- **Identity:** researcher in complexity reductions, parameterized algorithms, and exact combinatorial optimization
- **Focus:** correctness and completeness of definitions, bijections, reductions, edge cases, algorithms, and proof/computation boundaries

## Overall assessment

- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject
- **Confidence:** 4/5

The paper defines a ternary-assignment optimization problem and develops it through exact translations, closure operations, reductions, and structural algorithms. The central bijection in Theorem 2 is clean: selected literals encode assigned variables, selected clause vertices encode residual clauses, and domination of both endpoints enforces the two-polarity condition. The width-two Hall argument, width lift, clause-replication recovery, and fixed-width hardness construction form a convincing proof sequence. I did not find a fatal logical error in these universal arguments. Two claims nevertheless need stronger formal support before acceptance. First, the claimed integer spectrum for proper exact \((3,2,2)\)-CNF uses \(\beta(P)=1\), but only an external exhaustive receipt supports the lower bound in the present submission. Second, the bounded-treewidth claim imports optimization and full-polynomial counting from generalized domination without identifying the exact source theorem and output complexity. Several smaller proof specifications should also be tightened, including the range of the MaxCut threshold and the multigraph interpretation in the tautological width-two case. These issues are fixable, but the spectrum result is a central theorem and requires re-review.

## Strengths

### S1. Exact feasible-domain bijection

Theorem 2 proves both directions and explicitly handles empty clauses, tautologies, duplicate indexed clauses, and absent variables in the following discussion. This eliminates common one-way-reduction gaps and makes the formula objective genuinely equivalent to independent domination on the image class.

### S2. The width boundary is proof-motivated

Theorem 7 derives Hall's condition from two residual polarities and width at most two. Lemma 8 then exhibits the slack at width three, and Theorem 9 converts it into fixed-threshold hardness. This is a coherent combinatorial explanation rather than an isolated hardness claim.

### S3. Replication has a correct lexicographic interpretation

Theorem 6 bounds \(\beta(F^{[r]})\) between \(r\tau-k\) and \(r\tau\) and uses \(r>k\) to show that every minimizer first minimizes residual clauses and then maximizes unassigned variables. The ceiling recovery is correctly justified.

### S4. Degenerate semantics are not swept aside

The definitions explicitly retain clause indices and the declared variable set. This is necessary for clause replication and for formula-graph twins, and the artifact tests the same cases.

## Weaknesses

### W1. The positive finite base is not proved at the manuscript's assurance level

**Problem:** Sections 4.1 and 6 use the fact that a 15-variable component \(P\) has \(\beta(P)=1\). Section 8 reports exhaustive counts, but there is no formal proof object or human-checkable lower-bound argument for \(\beta(P)\ge1\).

**Why it matters:** This value is a linchpin for separation from satisfiability and, together with additivity, the theorem that the exact \((3,2,2)\) value spectrum is all integers. An executable receipt is not an independently checkable mathematical proof of an optimum.

**Suggestion:** Include the complete instance and witness; produce a proof-producing optimization encoding with a small trusted checker, or give a structural lower bound. If this is not feasible, state a formally delimited computer-assisted theorem and make the checker/proof archive part of the result.

**Severity:** Critical for the spectrum claim; Major for the paper as a whole.

### W2. The MaxCut reduction omits threshold preprocessing

**Problem:** Theorem 9 adds \(m-K\) copies of \(N\) without stating the standard restriction \(0\le K\le m\). For arbitrary encoded \(K\), the copy count can be negative.

**Why it matters:** A polynomial reduction must be a total, well-defined mapping on its declared source language.

**Suggestion:** Restrict the cited source problem to \(0\le K\le m\), or explicitly map the trivial cases \(K\le0\) and \(K>m\) to fixed yes/no instances.

**Severity:** Minor.

### W3. The bounded-treewidth consequence needs a theorem-level citation and output analysis

**Problem:** Section 5.6 states that Focke et al. yield \(2^{O(t)}|F|^{O(1)}\)-time optimization and counting, and hence the “complete Laurent polynomial.” It does not identify the precise theorem, whether all cardinalities are counted in one run, or how integer-output bit complexity is handled.

**Why it matters:** Optimization, total counting, and size-refined counting are distinct algorithmic claims. A full polynomial can have large integer coefficients even though it has only linearly many exponents.

**Suggestion:** Cite the exact theorem(s), state the arithmetic/output model, and either derive size-refined counting by an explicit cardinality variable or weaken the claim to the optimization/counting quantities directly guaranteed by the source.

**Severity:** Major.

### W4. The width-two incidence proof should explicitly use a signed-occurrence multigraph

**Problem:** Theorem 7 calls the construction a variable-clause incidence graph but counts two incidences from a tautological clause containing both signs of one variable. In the usual simple incidence graph that is one edge.

**Why it matters:** The inequality is valid only when the counted object is clear. Hall's neighbor set is simple while the capacity bound counts literal occurrences with multiplicity.

**Suggestion:** Define a bipartite signed-occurrence multigraph for the counting step, then apply Hall to its underlying adjacency relation. State that each clause node has at most two incident literal occurrences.

**Severity:** Minor.

### W5. The MILP is exact but under-specified as a reusable executable model

**Problem:** Section 5.1 says “0–1 optimization model” but does not repeat that all \(a_j^0,a_j^1,u_j,r_a\) are binary, nor give a model file or tested implementation.

**Why it matters:** The inequalities are mathematically sufficient over binary variables, but the paper promotes the model as a second executable specification.

**Suggestion:** State the domains explicitly and add a small LP/MPS generator or cross-check if the executable-specification claim is retained.

**Severity:** Minor.

## Detailed comments

### Definitions and Theorems 1–2

Theorem 1 is essentially definitional but correct. Theorem 2 is the strongest foundational result. The converse correctly observes that an unselected clause vertex must have a selected literal neighbor, while a selected clause vertex cannot have one by independence.

### Algebra

Theorem 4 follows from factorization of the feasible domain and is sound. Theorem 5's local accounting is convincing; an explicit map between feasible assignments, or a sentence that all three local choices attain the same net cost when a clause survives, would make the equality of feasible objective sets even clearer.

### Complexity

The NP membership and direct enumeration bounds are correct under the indexed input model. Theorem 9 needs only the threshold-domain repair noted above. The claim “sign is polynomial-time decidable at width two” should consistently mean \(\beta\le0\) or \(\beta>0\); since \(\beta=\tau\ge0\) there, this is equivalent to satisfiability.

### Regular-DIM result

The edge-count proof that \(\mu^*=k\) is sound for a finite simple \(d\)-regular graph with a specified DIM: every maximal matching is edge-dominating and each selected edge covers at most \(2d-1\) edges. The spectrum corollary remains conditional on the finite positive base unless strengthened.

### Reproducibility

Testing normal and optimized Python, comparing full spectra across formula and graph models, and recording the residual-polarity bug are valuable. They test the implementations, not the universal proofs, as the supplement correctly states.

## Questions for the authors

1. What proof system can express the lower bound \(\beta(P)\ge1\), and what is the smallest trusted checker needed to validate it?
2. Which exact result of Focke et al. supplies size-refined counting, and what running-time model includes coefficient bit complexity?
3. Is “proper” defined identically everywhere (no tautologies and no repeated variable within a clause), and can that definition be gathered in one place?
4. Will the MILP formulation be implemented and tested, or should it be presented only as a mathematical formulation?

## Minor issues

- State \(0\le K\le m\) in Theorem 9.
- Use “signed literal-occurrence multigraph” in Theorem 7.
- Give the allowed input range and encoding convention for threshold \(q\).
- Add a sentence explaining how empty clauses behave in the MILP lower-bound inequality.

## Dimension scores

| Dimension | Score | Descriptor | Notes |
|---|---:|---|---|
| Originality | 74 | Adequate | Methodologically meaningful extraction; historical judgment left to domain review |
| Methodological rigor | 78 | Strong | Universal proofs look sound; two imported/finite linchpins need strengthening |
| Evidence sufficiency | 67 | Adequate | Strong regression suite; no independently checkable positive-base lower bound |
| Argument coherence | 87 | Strong | Theorem sequence is unusually well integrated |
| Writing quality | 84 | Strong | Definitions are precise; a few technical objects need sharper naming |
| Literature integration | 70 | Adequate | Exact algorithmic source pinpoints needed |
| Significance and impact | 75 | Strong | Useful structural bridge if finite and treewidth claims are closed |
| **Weighted average** | **76.4** | **Minor range numerically; Major Revision by critical-claim override** | The spectrum linchpin and imported counting claim require re-review |
