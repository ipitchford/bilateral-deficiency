# Imported theorem dependency ledger

**Release:** *Bilateral Deficiency: Residual SAT Optimisation and Independent
Domination in Regular-DIM Graphs*  
**Status:** unrefereed candidate  
**Purpose:** identify every load-bearing imported mathematical result and make
its convention transfer auditable.

| Dependency | Exact theorem or object used | Convention transfer | Local consequence and check | Residual obligation |
|---|---|---|---|---|
| T. Zhang, T. Peitl, and S. Szeider, *Small Unsatisfiable k-CNFs with Bounded Literal Occurrence*, SAT 2024, Appendix A.1 | The displayed ten-clause \(E_{3,2,2}\) enforcer and the property that its distinguished variable is false in every satisfying assignment | The clauses are transcribed as an indexed CNF; a global polarity choice orients the terminal as \(x_1\); internal signed occurrences and the terminal's two negative occurrences are recounted | `terminal_signature.py` independently enumerates the local semantics; `lean_terminal_signature.lean` hard-codes the ten clauses and proves that the complete signature is exactly \((0,\varnothing,0),(1,\varnothing,1),(*,\varnothing,1),(*,\{-\},1)\) | The source formula and forced-terminal property remain imported. The Lean theorem's translation boundary is the visible ten-clause transcription. |
| Zhang--Peitl--Szeider, Theorem 15 and Table 1 | An unsatisfiable \((3,2,2)\)-formula has at least 20 distinct clauses | From a reconstructed cubic-DIM formula, tautological clauses are deleted and duplicate indexed clauses collapsed. The result has width at most three and each signed literal occurs at most twice, as required by the cited bounded-occurrence convention. | Positive \(\beta\) implies unsatisfiability. For the original exact signed-occurrence formula, \(3m=4k\) and \(|V(G)|=2k+m=5m/2\), giving the DIM-qualified order lower bound 50. | The finite search/classification proof of the 20-clause result is not independently rerun in this package. |
| S. O and D. B. West, *Balloons, cut-edges, matchings, and total domination in regular graphs of odd degree*, JGT 64 (2010), Corollaries 2.3 and 4.4 and Theorem 5.2 | Every connected cubic graph of order \(r\) has matching number at least \((4r-1)/9\), sharply for infinitely many graphs; the equality family is \(\mathcal H_1\) | Their order variable \(n\) is the present skeleton order \(r\); their matching number \(\alpha'(G)\) is the present \(\nu(G)\). The canonical sequence is parameterised as \(r_t=16+18t\). | The amplifier theorem converts \(r-\nu(R)\) to the graph gap. The generator checks the displayed skeleton parameters before deriving the construction-specific limiting density \(1/72\). | The O--West proof and full equality-family classification remain imported. |

## Boundary

Local checks validate transcription, syntax, parameter conversion, and the
stated downstream calculation. They do not independently prove the imported
theorems, establish literature novelty, or constitute specialist review.

The canonical source citations and URLs are in `MANUSCRIPT.md` and
`PRIOR_ART_SEARCH_LOG.md`.
