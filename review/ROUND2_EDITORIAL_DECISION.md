# Round 2 Editorial Decision

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and
  the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission revision
- **Decision date:** 8 August 2026
- **Review round:** 2
- **Nature of review:** adversarial internal simulation, not external peer
  review

## Decision

### Minor Revision before external submission

The critical proof-assurance defect from Round 1 is closed. No internally
identified fatal error remains in the theorem chain, and the positive base is
now supported by an explicit witness, a written encoding lemma, independently
checkable LRAT proofs, and a direct LRAT path accepted by Lean's verified
checker. The manuscript is suitable to be handed to human specialists for
real review once author-controlled submission and archival items are supplied.

This decision is not acceptance. Historical priority remains bounded rather
than exhaustive, the general theory is not proof-assistant formalized, and no
external mathematician has endorsed the arguments.

## Round 1 requirement disposition

| Item | Round 2 status | Evidence |
|---|---|---|
| R1 positive base | Satisfied | Appendix A, Proposition 11, `proof/`, native and Lean receipts |
| R2 priority/lineage | Substantially satisfied; specialist extension pending | exact 2008 pinpoint, Dod 2016, `PRIOR_ART_SEARCH_LOG.md` |
| R3 proof specifications | Satisfied | signed multigraph, binary MILP, normalized \(1\le K\le m\) |
| R4 treewidth counting | Satisfied | size-specific call derivation and output-bit analysis |
| R5 immutable boundary | Satisfied locally; public archive external | checksum manifest, pinned checker, license/citation placeholders |
| R6 wording | Satisfied | “separately implemented” and “algebraic conformance benchmark” terminology |

## Reviewer-lens reassessment

| Lens | Round 1 | Round 2 | Principal finding |
|---|---|---|---|
| handling editor | Major Revision | Minor Revision | article is now standalone at its finite linchpin |
| proof/complexity methodology | Major Revision | Minor Revision | local proof specifications and treewidth output model repaired |
| SAT/graph domain | Major Revision | Minor Revision | antecedent and polynomial lineage materially improved; specialist priority audit remains |
| proof engineering/software | Major Revision | Minor Revision | proof/checker chain is reproducible and assurance levels are separated |
| devil's advocate | rejection case viable | objections narrowed | transport/connectedness/sign-slice objections remain significance questions, not discovered correctness failures |

## New Round 2 findings and repairs

### F1. Antecedent notation collision — repaired

The first revision quoted the source's \(5k\)-clause equation but then reused
\(k\) as the generic variable count. In the cited construction the formula has
\(3k\) variables. Section 2.2 now writes the generic count as \(n\), states
\(|D_1|=n-|U|\), and explicitly notes \(n=3k\) in the source notation.

### F2. Empty MaxCut corner case — repaired

The first revision allowed \(K=0\), permitting an empty source graph and an
empty lifted formula. Theorem 9 now normalizes inputs to \(1\le K\le m\):
trivial yes inputs map to one edge with threshold one, and trivial no inputs
map to the triangle with threshold three. The target construction is therefore
nonempty exact width three and uses \(m-K\ge0\) gadgets.

### F3. Positive witness transparency — strengthened

Appendix A now includes the complete signed-occurrence table for \(P\) and a
residual polarity table for every unassigned variable in the upper witness.
Both exact \((3,2,2)\) structure and bilaterality can be checked without code.

## Surviving adversarial objections

### A1. Transport versus native SAT significance

The hostile reading—that \(\beta\) is the pullback of independent domination
through a known graph architecture—cannot be disproved by terminology. The
paper now answers it with formula-native content: the bipolar-residual
characterization, width-two Hall equality, exact MILP, clause-replication
recovery, width lift, and a sharp fixed-width sign boundary. Whether that is
significant enough for a particular venue is an editorial judgment for real
reviewers, not an internal correctness issue.

### A2. The most structured sign slice remains open

The complexity of \(\beta(F)\le0\) for proper simple exact
\((3,2,2)\)-CNF remains open. The manuscript does not imply otherwise. The
broad fixed-width theorem and the structured open slice are now stated next to
one another.

### A3. Spectrum constructions are disconnected

The all-integer spectrum uses variable-disjoint union. A connected composition
or connected-family spectrum would strengthen the work and remains open. The
current theorem is still correct for the class it states.

### A4. Priority is not exhaustive

The reproducible search log improves the historical claim but does not replace
MathSciNet/zbMATH/thesis/non-English searching or specialist judgment. The
paper's wording is conditional (“appears to be new”) and would remain accurate
if a close non-identical antecedent were later found.

### A5. Formalization is partial

Lean checks the finite LRAT contradiction, not the full definition, encoding
compiler, or general theorem chain. The manuscript states this boundary. Full
formalization would increase assurance but is not a prerequisite for an
ordinary mathematics submission.

## Remaining minor revisions controlled by the human authors

1. Supply author names, affiliations, ORCIDs, approved CRediT roles, funding,
   and conflict declarations.
2. Choose a license as rights holder and replace `LICENSE-PENDING.md`.
3. Create a public version-controlled repository and archival DOI; insert the
   immutable identifiers in the manuscript and `CITATION.cff`.
4. Obtain a specialist priority audit using the unexhausted routes.
5. Have at least one SAT/complexity specialist and one domination-theory
   specialist independently read the written proofs and encoding lemma.
6. Rerun the manifest, proof, tests, DOI/retraction screening, and rendered-
   document checks on the exact submission archive.

## Editorial conclusion

The Round 1 linchpin override no longer applies. The positive base is now
independently checkable without trusting the exhaustive solver's status line,
and all local specification repairs requested by the methodology review are
present. The remaining work concerns external scholarly validation and
author-controlled release metadata. The correct handoff is therefore “minor
revision before external submission,” not “proved beyond doubt,” “accepted,”
or “released.”
