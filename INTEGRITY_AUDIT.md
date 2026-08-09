# Manuscript Integrity Audit

**Manuscript:** *Bilateral Deficiency: Residual SAT Optimisation and Independent
Domination in Regular-DIM Graphs*  
**Audit date:** 9 August 2026  
**Status:** post-major-revision internal audit; not journal peer review

## 1. Summary

| Metric | Result |
|---|---:|
| Body word count, Sections 1--9 (`pandoc -t plain`) | 10,494 |
| Total manuscript word count, including Appendix A and references (`pandoc -t plain`) | 11,943 |
| In-text citation markers | 30 |
| Unique reference entries | 18 |
| Orphan in-text citations | 0 |
| Orphan references | 0 |
| Reference order | exact order of first appearance, 1--18 |
| DOI-eligible journal/proceedings entries with DOI | 13/13 |
| Unexpected control bytes | 0 |
| Inline TeX delimiters | 556 open / 556 close |
| Display TeX delimiters | 63 open / 63 close |
| Normal test suite | 25/25 pass |
| Python `-O` test suite | 25/25 pass |
| Warnings-enabled C++ build | pass |
| Algebraic benchmark packages verified | 4/4 |
| Native LRAT checks | 4/4 verified across three positive formulas |
| Lean direct-LRAT checks | 118,497; 35,737; and 11,393,023 actions; verified |
| Parser-independent Lean terminal lemma | 6,561 assignments; exact four-row signature; verified |
| Clean-room threshold-encoding audit | 731 variables; 9,256 clauses; seven-formula semantic corpus; mutation rejected |

The first-round reviewers all required major revision because the positive
base \(P\) was a linchpin for the integer-spectrum theorem but had only an
exhaustive execution receipt. The revision adds Appendix A, a two-direction
encoding lemma, a deterministic 731-variable/9,256-clause encoding, two
native-checked LRAT paths, and a direct LRAT path accepted by Lean 4.32.1.

## 2. Citation and priority audit

All 18 references are cited and every bracketed citation has a listed entry.
Numbering follows first appearance. Publisher or primary records were used for
the new references: Dod's 2016 arXiv record, the ACM record for bounded-
treewidth generalized domination, the DRAT and LRAT proceedings records, the
official CaDiCaL 3.0 LIPIcs record, the Lean 4 proceedings record, and the
LeanSAT source repository.

The closest antecedent now has an exact pinpoint: Chlebík--Chlebíková,
Section 2.3, proof of Theorem 5, pp. 10--11 of the author preprint. Their
equation \(|D|=|D_1|+(5k)bt\) is stated before the manuscript rewrites it as
the generic replicated-clause cost \(|D_1|+t|T|\). This prevents the cost
decomposition from being claimed as new.

The independent domination polynomial is credited first to Markus Dod (2016),
then to Jahari--Alikhani (2018). The manuscript and
`PRIOR_ART_SEARCH_LOG.md` expressly avoid a global-priority claim. The search
did not exhaust MathSciNet, zbMATH, theses, non-English literature, or all
hypergraph-transversal terminology.

## 3. Claim-to-evidence matrix

| Claim | Universal proof dependency | Finite or external check | Status and boundary |
|---|---|---|---|
| \(\beta\) is the least deficiency of a bipolar residual | equality of domains/objective in Theorem 1 | residual unit tests | proved in manuscript |
| bilateral assignments and formula-graph independent dominating sets are in size-preserving bijection | both directions and inverse in Theorem 2 | full spectra on more than 100 formulas | proved; computation is regression evidence |
| \(D_i(G(F),z)=z^kB_F(z)\) | coefficient-preserving corollary of Theorem 2 | exhaustive multiplicity equality | proved |
| distinct from ordinary/maximum deficiency, SAT, and unit-weight MaxSAT defect | explicit separating formulas plus Theorem 7 | exact finite enumeration | proved |
| additivity and spectral convolution | product factorization of feasible assignments | value and spectrum tests | proved |
| uniform-width lift preserves \(\beta\) | local clause case split | exhaustive lift tests | proved |
| replication recovers MaxSAT | interval argument with \(r>k\) | replication controls | proved |
| width at most two gives \(\beta=\tau\) | Hall argument on signed-occurrence bipartite multigraph | exhaustive width-two corpus | proved, including tautological parallel incidences |
| arbitrary width-two threshold is NP-complete | Simple MaxCut identity | triangle control | proved; source instances normalized to \(1\le K\le m\) |
| sign is NP-complete at every fixed uniform width \(r\ge3\) | negative gadget, width lift, additivity, MaxCut | exact negative receipt | proved |
| bounded incidence treewidth is tractable | explicit decomposition lift and size-specific generalized-domination counting | no performance benchmark | theorem-level; full polynomial obtained by polynomially many size calls |
| regular-DIM coordinatisation is surjective | graph/formula inverse constructions | degree/signature tests | proved for graphs equipped with a specified oriented DIM |
| \(i(G)-\mu^*(G)=\beta(F_M)\) | Theorem 2 plus regular edge-count bound | canonical 16--15 check | proved |
| constructive regular-DIM replacement bound | random endpoint choice plus conditional expectations | exact rational derandomization tests | proved; algorithm produces an explicit independent dominating set |
| positive base \(\beta(P)=1\) | upper witness, encoding lemma, LRAT UNSAT lower bound | exhaustive solver, two native checks, one Lean check | checker-assisted finite proposition proved in Appendix A |
| attributed enforcer composition has \(\beta=1\) | terminal composition and generic encoding lemma | byte regeneration, native LRAT, Lean LRAT | independently checked second positive base; not needed for spectrum/minimality |
| connected occurrence switch has \(\beta=1\) | explicit witness and generic encoding lemma | reconstruction, byte regeneration, native LRAT, 11,393,023-action Lean LRAT | extended optional conformance formula; proof file is 5.79 GB and is not theorem-critical |
| exact signed-occurrence \((3,2,2)\) spectrum is \(\mathbb Z\) | Proposition 14, Lemma 8, additivity | generated values \(3,-2,0\) | proved; additive constructions may be disconnected |
| connected edge-cover amplifier | enforcer signature plus edge-cover completion argument | Python enumerates all \(3^8\) local states; parser-independent Lean proves the exact table; generated prism \(s=3\) syntax/connectivity audit | universal reduction proved in writing; finite signature formally checked from hard-coded clauses |
| connected cubic DIM graphs with gap \(s\) on \(80s\) vertices | Theorem 12 applied to \(C_s\square K_2\) | instantiated \(s=3\) receipt | proved for every \(s\ge3\); receipt checks one instance |
| asymptotic connected gap density at least \(1/72\) | Theorem 12 plus O--West extremal matching family | canonical order-16 skeleton/amplifier receipt | proved; \(1/72\) is sharp only within the edge-cover-amplifier subclass |
| minimum counterexample order in the cubic-DIM class is 50 | positive value implies UNSAT; SAT 2024 20-clause lower bound; cubic incidence count | connected order-50 graph from \(P\) | proved across the full DIM-equipped cubic class, including tautological or repeated indexed clauses; minimum outside DIM is open |
| exact signed-occurrence \((3,2,2)\) paired-edge normal form | reversible assignment/edge-selection map and occurrence count | all states of \(N\); matching-only counterexample checked independently | identity proved; tempting reduction to pair-feasible matching is false |
| six proposed uses | preceding theorems and artifact workflows | analyzer, generator, verifier, mutation rejection | technically established with explicit qualifications |

## 4. Adversarial proof checks

### 4.1 Degenerate indexed formulas

The master bijection was checked against empty clauses, tautologies, duplicate
indices, and explicit unused variables. Empty clause vertices must be selected;
tautological residual clauses may dominate both literal endpoints; duplicate
indices remain distinct; and unused variables cannot remain bilateral.

### 4.2 Width-two multigraph semantics

The Hall proof now explicitly uses the signed literal-occurrence bipartite
multigraph. A tautological binary clause supplies two parallel signed
incidences but one underlying clause neighbor. Thus bilaterality gives
\(2|X|\) incident edges and width two caps them at \(2|N(X)|\), exactly the
neighbor inequality Hall requires.

### 4.3 MaxCut reduction range

The fixed-threshold reduction adds \(m-K\) negative gadgets. The revision
states \(1\le K\le m\); trivial Simple MaxCut inputs are normalized to a
one-edge threshold-one yes instance or a triangle threshold-three no instance.
Hence the lifted formula is nonempty and 3-uniform, and the number of
gadget copies is always a nonnegative polynomially bounded integer.

### 4.4 Binary linear formulation

All variables \(a_j^0,a_j^1,u_j,r_a\) are now explicitly declared binary.
The residual inequalities force \(r_a=1\) exactly when no assigned-true
literal occurs, and the two polarity inequalities enforce bilaterality. The
formulation is an exact specification, not a claim about a solver's status.

### 4.5 Bounded-treewidth output model

The cited algorithm counts generalized dominating sets of a specified size.
Calling it once for every size \(s\) adds a polynomial factor. Every
coefficient has \(O(n)\) bits and there are \(O(n)\) coefficients, so explicit
output of the complete polynomial remains polynomial in the input/output
model.

### 4.6 Positive base certificate

The upper witness leaves 11 variables and 12 indexed clauses, with residual
indices \(1,3,4,5,7,8,10,12,14,15,18,19\). The generator encodes exactly-one
ternary states, residual equivalences, bilateral polarity implications, and a
prefix-sum automaton forbidding positive final deficiency. The written lemma
proves satisfiability iff \(\beta(P)\le0\).

The encoding digest is
`c282d2d35f66e81ae175d9afa560b9a5ded2d00f51d8b02c380d939102156c11`.
The direct LRAT digest is
`61bb30cadaf1cbf4bd15662a1a97b0a6352b416a187532c887000493f46f755a`.
The native checker reports `VERIFIED`; Lean parses 118,497 actions and reports
`LEAN_LRAT_VERIFIED`. A standard-library clean-room validator independently
reconstructs the 731-variable map and every one of the 9,256 clauses, checks a
seven-formula semantic corpus with an independent DPLL procedure, and rejects
a rehashed clause mutation. The written general encoding lemma remains a
mathematical translation obligation. This is producer-side conformance
evidence, not independent reproduction or full formalization of bilateral
deficiency.

### 4.7 Connected-switch certificate

The recorded 2-switch reconstructs a 30-variable, 40-clause formula from two
copies of \(P\). Direct audits establish properness, simplicity, exact
signed-occurrence \((3,2,2)\) counts, and connectedness. The value-one witness is
checked by the residual semantics. The independently regenerated encoding of
\(\beta\le0\) has digest
`54493aeb68ecd3d276cbf73765ef6c727275fc71e7a84ad195cdb1d0d8830c9d`.
Its 5,793,599,477-byte direct LRAT proof has digest
`323402633cf890918c5690080279973a99fdd63fc80802d60842a958ba13db7f`.
The pinned native checker reports `VERIFIED`; Lean parses 11,393,023 actions
and reports `LEAN_LRAT_VERIFIED`.

## 5. Implementation and AI failure-mode audit

Five concrete development failures were surfaced and corrected:

1. The first C++ scan recorded unassigned polarities before confirming clause
   survival. Cross-model testing found the error; survival is now classified
   first.
2. A TeX serialization boundary created control bytes. The source was restored
   and byte/delimiter checks now pass.
3. A symmetric injection-based threshold encoding generated more than 400 MB
   of an unfinished proof. It was abandoned in favor of the deterministic
   prefix-balance automaton; the partial proof was deleted and is not evidence.
4. The DRAT-translated LRAT passed the native checker but not Lean. CaDiCaL's
   direct LRAT passes both. A direct witness checker also corrected an early
   12/13 versus 11/12 transcription error in the proof README.
5. The paired-edge normal form initially suggested a matching-only reduction.
   A deterministic search found a 9-variable counterexample whose optimal
   selected edges overlap. The manuscript now proves the broader surplus
   identity and leaves its complexity open instead of importing an invalid
   rainbow-matching classification.
6. The production parser accepts repeated literal tokens, while its clause
   builder treats clauses as sets. The release therefore declares canonical
   set-valued clauses as the compiler domain; the clean-room validator rejects
   undeclared normalization instead of implying arbitrary DIMACS support.

These incidents justify the separate semantic implementations, complete-
spectrum comparisons, optimized-Python tests, deterministic regeneration,
native and Lean proof paths, cryptographic binding, and mutation rejection.
They do not replace human mathematical review.

## 6. Assurances not undertaken in this release

- No external specialist was asked to extend the priority search through the
  unexhausted routes in `PRIOR_ART_SEARCH_LOG.md`.
- No unaffiliated party independently read every proof, reimplemented the
  semantics, or validated the CNF encoding bridge.
- Journal submission and editorial peer review were expressly outside this
  release workflow.
- The exact signed-occurrence \((3,2,2)\) sign complexity, sharp constants,
  classification of
  all order-50 extremizers, and full proof-assistant formalization remain open
  research problems. Connected positive amplification and the minimum order
  itself are settled by Theorem 12 and Corollary 13.
- Future journal metadata, external acceptance, and community adoption remain
  wholly external to this package.

## 7. Current conclusion

No unresolved internal contradiction, orphan citation, failed executable
check, or missing proof component for a stated theorem was found in this
revision. The strongest remaining limitations are historical coverage,
translation obligations around the encoding bridge and general proofs, and
absence of independent external assessment. Those boundaries are
stated in the manuscript rather than inferred from passing computation.
