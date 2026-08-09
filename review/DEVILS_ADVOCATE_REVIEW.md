# Devil's Advocate Report

## Mandate

Construct the strongest technically serious case against publication of the manuscript in its present form. This report intentionally does not balance each objection with a score or recommendation rubric.

## Strongest rejection thesis

The manuscript has not yet shown that “bilateral deficiency” is a new mathematical parameter rather than the unit-weight specialization of a known independent-domination reduction cost, transported back through a graph encoding and then decorated with standard closure and reduction consequences. The 2008 formula \(k+t|T|-|U|\) already contains the objective. At \(t=1\), subtracting the fixed \(k\) gives exactly \(|T|-|U|\). The manuscript's feasible domain can be read as nothing more than the inverse image of independent dominating sets under the same literal-pair construction. On this hostile reading, the parameter is defined precisely so Theorem 2 is true, Theorem 1 restates that definition, Corollary 3 reindexes a known graph polynomial, and Theorem 4 inherits product behavior from disconnected graph union.

## Objection 1: the distinctness tests do not establish conceptual independence

Showing that ordinary deficiency, maximum deficiency, satisfiability, and MaxSAT defect fail to determine \(\beta\) proves only non-equivalence to four coarse summaries. Infinitely many artificial functions would pass those tests. The paper needs a positive reason why SAT researchers should optimize \(\beta\) except when they are already solving independent domination on the corresponding graph. The current strongest intrinsic description—least deficiency among bipolar residuals—is very close to the definition itself and is not connected to a pre-existing SAT operation, structural decomposition, or tractability theory beyond the results created for the paper.

**What would defeat this objection:** prove a formula-native theorem not obtained transparently from independent domination, such as a kernelization, obstruction theory, autarky interaction, or exact-\((3,2,2)\) structural characterization that solves a recognized SAT question.

## Objection 2: most algebraic results are standard gadgets in new notation

Disjoint-union additivity and generating-function multiplication are expected for any componentwise minimization. Width lifting is a local two-clause gadget with cost preservation. Clause replication is ordinary lexicographic weighting: use a coefficient larger than the secondary objective range to recover the primary MaxSAT optimum. These are correct and useful, but they do not by themselves establish a deep parameter theory.

**What would defeat this objection:** develop nontrivial operations on connected formulas/graphs, a minor-like or restriction order, monotonicity/non-monotonicity theory, extremal bounds, or a decomposition theorem that cannot be described as direct product accounting.

## Objection 3: the advertised sharp complexity boundary is weaker than it sounds

At width two, \(\beta=\tau\), so the easy sign test is simply 2-SAT satisfiability and the variable-threshold hardness is simply Max-2-SAT/MaxCut. At width three, the sign reduction uses an externally supplied negative offset gadget plus width lifting. The motivating exact \((3,2,2)\) sign problem remains open. Thus the paper does not resolve the most structurally relevant complexity slice; it transfers known hardness across a broad exact-width class.

**What would defeat this objection:** determine the sign complexity on proper exact \((3,2,2)\)-CNF, or prove a significant parameterized/approximation result native to \(\beta\).

## Objection 4: the “complete classification” is conditional, equipped, and disconnected

The coordinatisation applies only after a dominating induced matching is supplied and oriented. The identity \(i-\mu^*=\beta\) then follows because the formula graph construction makes \(i=k+\beta\) and regular edge counting fixes \(\mu^*=k\). This is an exact coordinate, but not a classification of regular-DIM graphs up to structure. The all-integer spectrum is manufactured by disconnected unions of one positive and one negative component. It says little about connected graphs, extremal order, uniqueness, or recognition when the DIM is not supplied.

**What would defeat this objection:** give a connected composition or a connected-family spectrum, an algorithm to find/recognize the relevant DIM within the claimed complexity, or a structural theorem beyond the numerical gap identity.

## Objection 5: the positive half of the spectrum is not proved to mathematicians' usual standard

The negative component has a short occurrence-count lower bound. The positive component has a JSON receipt from exhaustive code. The manuscript correctly refuses to call that receipt a certificate, but nevertheless uses the value as a premise in separation and spectrum results. Two implementations and many tests reduce the probability of error; they do not provide an independently checkable lower-bound proof. The paper's most rhetorically important example therefore has the weakest proof status.

**What would defeat this objection:** include a small proof object checked by a standard or formally verified checker, or a human-readable lower bound for the explicit formula.

## Objection 6: the six uses are demonstrations, not external validation

Discovery means enumerating a formula class and checking a necessary-and-sufficient objective, but no new nontrivial discovery beyond the motivating example is reported. Compact proof production is compact only for upper bounds or disconnected composition; the hard lower bound remains uncompressed. Algorithm selection is a theorem table without empirical comparison. Benchmarks are algebraic copies of two bases. Family classification is the equipped numerical identity discussed above. AI-math infrastructure is an engineering workflow with no evidence of adoption, error-rate reduction, or improved theorem discovery. The disclaimers are honest, but after enforcing them the uses may be too modest to sustain the manuscript's broad framing.

**What would defeat this objection:** add one genuinely new connected mathematical discovery made using \(\beta\), a proof-producing lower-bound pipeline, and a benchmark study showing that the structural router changes solver behavior on diverse instances.

## Objection 7: the novelty search is not adequate for a naming claim

The manuscript acknowledges that MathSciNet, zbMATH, theses, non-English literature, and hypergraph terminology remain to be searched. It also appears to cite a later rather than earliest independent-domination polynomial source. A bounded web/database search cannot carry the claim that a new named parameter has been established, especially when the exact cost already occurs in 2008.

**What would defeat this objection:** a reproducible specialist search, an exact comparison with the 2008 construction, and wording that makes the paper valuable even if an older equivalent definition is found.

## Falsifiable tests for the authors' thesis

1. Remove the name “bilateral deficiency” and state the results entirely as independent domination on formula graphs. Which theorem becomes harder to formulate or prove?
2. Give a SAT-native algorithm whose correctness or complexity is clearer in \(\beta\) language than through the graph bijection.
3. Produce two formulas with the same formula graph up to isomorphism but different plausible SAT-side structure, and show what \(\beta\) reveals beyond the graph invariant.
4. Replace the positive JSON receipt with a checker-verifiable proof and determine whether the resulting proof exposes new structure.
5. Search for the objective under “partial assignment cost,” “residual surplus/deficiency,” “bipolar restriction,” and hypergraph transversal language; report the closest exact collision.

## Bottom line

The current manuscript contains several correct and elegant results, but the strongest adversarial interpretation remains viable: this is a well-engineered repackaging of a known reduction cost whose most distinctive complexity question is open and whose positive base is not yet certified. Publication becomes compelling if the authors close at least two of the following three gaps: specialist priority/lineage, proof-producing certification of the positive base, and a formula-native or connected structural theorem that cannot be dismissed as transport through independent domination.
