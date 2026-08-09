# Response to Round 1

Date: 8 August 2026  
Status: revision record for internal pre-submission review

We thank the simulated reviewers for identifying one linchpin proof gap and
several local specification problems. The revision does not treat review as
external validation; it records exactly how each criticism changed the
manuscript and artifact.

## Required revisions

### R1. Positive exact \((3,2,2)\) base — satisfied internally

- Appendix A now prints all 20 indexed clauses of \(P\).
- Proposition 11 gives the bilateral witness `0000***********`, its 12
  residual indices, 11 unassigned variables, and deficiency one.
- The appendix and `proof/README.md` prove a two-direction encoding lemma for
  \(\beta(P)\le0\).
- The deterministic encoding has 731 variables and 9,256 clauses.
- The package includes a trimmed LRAT and a CaDiCaL-direct LRAT.
- The pinned native checker accepts both. Lean 4.32.1 accepts all 118,497
  actions in the direct proof and invokes `LRAT.check_sound` in the successful
  branch.
- Exact hashes and a deterministic verification receipt bind the formula,
  encoder, CNF, map, proof, checker source, Lean wrapper, and result.

The dependent spectrum theorem is no longer supported only by an exhaustive
JSON receipt. The remaining boundary is explicit: the DIMACS parser and the
written formula-to-CNF encoding lemma have not been fully formalized.

### R2. Priority and lineage — partially satisfied; specialist extension remains

- Section 2.2 now pinpoints Chlebík--Chlebíková, Section 2.3, proof of Theorem
  5, author-preprint pp. 10--11, and states their exact equation
  \(|D|=|D_1|+(5k)bt\).
- The comparison now distinguishes the source's \(3k\) variables and \(5k\)
  clauses from the manuscript's generic \(n\)-variable shift.
- Markus Dod's 2016 paper is now credited before the 2018 independent-
  domination-polynomial paper.
- `PRIOR_ART_SEARCH_LOG.md` records representative exact queries, located
  collisions, the four-feature identity test, stopping rule, and unexhausted
  routes.
- The manuscript expressly avoids global priority.

MathSciNet, zbMATH, dissertations, non-English literature, and specialist
review remain unexhausted and are reported as a pre-submission obligation.

### R3. Proof specifications — satisfied

- Theorem 7 now uses the signed literal-occurrence bipartite multigraph,
  explicitly handling two parallel incidences from a tautological binary
  clause to one clause neighbor.
- Theorem 9 restricts normalized Simple MaxCut inputs to \(1\le K\le m\),
  mapping trivial inputs to a one-edge yes instance or triangle no instance.
- The MILP declares every \(a_j^0,a_j^1,u_j,r_a\) binary.

### R4. Bounded-treewidth counting — satisfied at the stated model

Section 5.6 now cites the size-specific generalized-domination counting
guarantee, calls it once for every set size, and accounts for the polynomial
number of calls and polynomial coefficient bit length. The complete explicit
polynomial claim is therefore derived rather than inferred from generic
counting.

### R5. Immutable artifact boundary — satisfied locally, externally pending

- Proof/checker hashes, pinned checker commit, exact commands, and an
  archive-level checksum/manifest procedure are supplied.
- `LICENSE-PENDING.md` refuses to invent a license without rights-holder
  authority.
- `CITATION.cff.template` exposes the author, ORCID, repository, DOI, and
  license fields still requiring human action.

A public version-controlled repository and archival DOI cannot be created
without the responsible author's authorization. The object is described as a
candidate archive, not a released scholarly artifact.

### R6. Independence and benchmark wording — satisfied

“Clean-room” and “independently written” claims were replaced by the narrower
“separately implemented” description. The generated packages are now called
“algebraic conformance benchmarks,” with an explicit statement that they are
neither representative SAT distributions nor an empirical performance suite.

## Suggested revisions

- S1 comparison table: added in Section 2.3.
- S2 rhetorical scope: “complete” is qualified by equipped family and
  numerical coordinate; Theorem 1 retains theorem numbering for cross-
  reference stability.
- S3 preprocessing/autarky programme: not solved; left for future work rather
  than padded with conjectural claims.
- S4 threat model: proof-generation failures, corruption rejection, optimized
  Python, deterministic regeneration, and parser/encoding trust are documented.
- S5 spelling: British spelling is used in the title/prose except fixed source,
  code, and problem terminology.
- S6 connected composition: stated prominently as open.

## Resulting assurance statement

The revision supports the internal conclusion that every stated mathematical
theorem has either a written proof or, for the finite positive base, a written
encoding lemma plus checker-verified LRAT contradiction and explicit witness.
It does not support claims of exhaustive priority, full formalization, journal
acceptance, archival release, or community adoption.
