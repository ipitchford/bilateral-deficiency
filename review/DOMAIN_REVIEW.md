# Peer Review Report — SAT and Graph-Theory Domain Lens

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission draft
- **Review date:** 8 August 2026
- **Review round:** 1

## Reviewer information

- **Role:** Peer Reviewer 2 (Domain)
- **Identity:** scholar working on clausal deficiency/autarkies, independent domination, domination polynomials, and dominating induced matchings
- **Focus:** conceptual distinctness, literature lineage, graph/SAT terminology, and significance of the regular-DIM classification

## Overall assessment

- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject
- **Confidence:** 4/5

The manuscript extracts the unit-weight residual cost implicit in a formula-to-independent-domination construction and organizes it as a formula parameter with a bilateral residual domain. The paper is commendably explicit that Chlebík and Chlebíková already supply the underlying arithmetic. The real contribution is therefore the total package: exact converse mapping, solution-spectrum identity, residual characterization, algebra, width dichotomy, and the coordinatisation of regular graphs equipped with a dominating induced matching. I find this package potentially publishable and more than a renaming exercise. The current literature case is nevertheless too narrow to support even a carefully qualified “appears to be new” statement without additional specialist searching. The independent-domination polynomial discussion appears to omit earlier work, and the closest antecedent is paraphrased without a page or named-result pinpoint. The connection to SAT deficiency, surplus, autarkies, and residual/restriction parameters needs a more systematic comparison table. Finally, the flagship exact-\((3,2,2)\) spectrum should include the positive formula and proof status in the paper itself. I recommend major revision because conceptual priority and standalone presentation are central to the paper's reason for publication.

## Strengths

### S1. The manuscript names its closest antecedent rather than hiding it

Section 2.2 derives \(k+t|T|-|U|\) directly from the 2008 construction and explicitly disclaims novelty of that decomposition. This makes the proposed advance assessable on the domain, inverse map, and subsequent theory.

### S2. Separation from nearby SAT quantities is concrete

Section 4.1 uses formulas with equal ordinary and maximum deficiency but different \(\beta\), followed by satisfiable negative and unsatisfiable positive examples. These examples answer the first objection a SAT reader will raise: that the objective is merely standard deficiency or MaxSAT defect.

### S3. The formula-graph image class is characterized in both directions

Section 6 does not merely construct regular-DIM graphs. It reconstructs exact signed-occurrence formulas from every simple regular graph equipped with an oriented specified DIM, while carefully allowing tautological clauses when required.

### S4. The exact-\((3,2,2)\) slice is mathematically well motivated

The paper connects it to cubic regular-DIM graphs and to existing occurrence-bounded SAT work. The open sign-complexity problem is appropriately not inferred from satisfiability hardness.

## Weaknesses

### W1. The priority audit is incomplete in precisely the terminology branches most likely to collide

**Problem:** Section 2.4 acknowledges a bounded search, but the manuscript still depends on a short reference list to position a new parameter spanning SAT restrictions, hypergraph incidence, and independent domination.

**Why it matters:** Closely related objects may be indexed under partial assignments, residual deficiency, surplus, critical/lean restrictions, transversal deficiency, or domination-cost polynomials rather than the chosen name.

**Suggestion:** Search MathSciNet, zbMATH, DBLP citation neighborhoods, theses, and hypergraph/transversal literature. Report databases, queries, dates, inclusion rule, and the nearest collisions. Keep the present qualified wording unless the audit supports something stronger.

**Severity:** Major.

### W2. The independent-domination polynomial lineage is too shallow

**Problem:** Section 3.4 cites a 2018 arXiv paper as evidence that \(D_i(G,z)\) “is studied as” the independent domination polynomial. Earlier work appears to exist, including Markus Dod's 2016 preprint *The Independent Domination Polynomial* (arXiv:1602.08250), and the terminology/history should be checked beyond one source.

**Why it matters:** The polynomial identity is presented as a contribution-strengthening result. Its graph-side object must be cited to the correct lineage without implying a later paper originated it.

**Suggestion:** Add the earliest located definition and a concise history, or use a neutral definition without a priority implication.

**Severity:** Major literature correction.

### W3. The 2008 decomposition needs an exact pinpoint and a sharper delta table

**Problem:** Section 2.2 gives the equation but no page, lemma, or construction label. The narrative list of what [2] does not develop is useful but hard to audit item by item.

**Why it matters:** This is the paper's closest collision and therefore the reference that skeptical readers will inspect first.

**Suggestion:** Cite the exact page/equation/construction and add a table comparing: graph construction, feasible-domain statement, converse, objective, optimum identity, solution polynomial, algebra, complexity, and regular-DIM classification.

**Severity:** Major.

### W4. The deficiency/autarky comparison should be more formal

**Problem:** Section 2.3 explains the quantifier differences in prose, but maximum deficiency, surplus, matching autarkies, lean kernels, and residual restrictions are not given symbol-level definitions or direct non-equivalence statements.

**Why it matters:** SAT specialists decide whether a parameter is distinct by its exact domain and quantifiers. A prose distinction can conceal an equality under a standard kernel operation.

**Suggestion:** Add a compact comparison table and one proposition/example for each nearest parameter family. State explicitly whether \(\beta\) is invariant under common simplifications such as deletion of satisfied clauses, pure-literal elimination, or autarky reduction; if unknown, list these as questions.

**Severity:** Major for positioning; the existing separation examples partially mitigate it.

### W5. The positive component must be visible in the mathematical article

**Problem:** The exact-\((3,2,2)\) spectrum cites an external “verified component” \(P\) rather than listing it.

**Why it matters:** The spectrum is a graph-theoretic classification corollary and should be independently inspectable from the article and supplement.

**Suggestion:** Include \(P\) in an appendix with the graph/formula correspondence and the exact status of its lower-bound verification.

**Severity:** Major.

## Detailed comments

### Title and abstract

“Exact coordinate” is justified only on the formula-graph/equipped-DIM class and should not be read as a coordinate for arbitrary graphs. Adding “on formula graphs” already helps; the abstract should repeat the equipped-family scope near “complete.”

### Prior art

This section is the paper's editorial fulcrum. The Zverovich comparison is helpful. The occurrence-bounded SAT sources motivate the class but do not position the parameter itself. A broader search is mandatory.

### Structural results

Theorem 2 is useful because its inverse identifies precisely why both signs are required. Corollary 3 should be connected to the earliest independent-domination polynomial literature. The replication connection to [2] is a credible explanation of lineage.

### Regular-DIM theory

The coordinatisation and proof \(\mu^*=k\) are elegant. “Complete” should always be followed immediately by “for the numerical gap on graphs equipped with a specified DIM,” since it is not an isomorphism classification and the generated all-integer examples are disconnected.

### Uses

The discovery and family-classification uses are strongest. The benchmark and AI-infrastructure uses are useful but currently instantiated by one positive and one negative base component rather than a diverse hard-instance ecology.

## Questions for the authors

1. Which existing SAT operations preserve \(\beta\), and how does the parameter behave under autarky reduction or lean-kernel extraction?
2. Is there an earlier independent-domination generating-function definition than the sources currently cited, and what terminology did it use?
3. Does the 2008 construction already prove a converse for the independent dominating sets relevant to its reduction, even if it does not formulate the bilateral domain?
4. Can the coordinatisation be quotiented by orientation/sign-switch equivalence in a way that yields a cleaner classification statement?

## Minor issues

- Define “proper” and “simple” once at first use and use the same graph/formula senses consistently.
- Add named equation or page pinpoints to the closest antecedents.
- Avoid using “coordinate” without specifying the ambient class.
- Explain whether tautological clauses are standard or exceptional in the intended exact-\((d,d-1,d-1)\) terminology.

## Dimension scores

| Dimension | Score | Descriptor | Notes |
|---|---:|---|---|
| Originality | 70 | Adequate | A credible new package, but collision search is not mature enough |
| Methodological rigor | 79 | Strong | Structural translations appear sound |
| Evidence sufficiency | 67 | Adequate | Literature and positive-base evidence need strengthening |
| Argument coherence | 84 | Strong | Claims are carefully qualified and sequenced |
| Writing quality | 82 | Strong | Precise, with some overuse of broad terms such as “complete” |
| Literature integration | 58 | Weak | Important sources present, but likely omissions and no reproducible priority search |
| Significance and impact | 76 | Strong | Meaningful bridge if distinctness survives the specialist audit |
| **Weighted average** | **75.7** | **Minor range numerically; Major Revision by literature/standalone override** | The paper's contribution claim requires a deeper lineage audit |
