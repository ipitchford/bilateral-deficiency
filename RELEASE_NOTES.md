# Release notes

## v1.0.1-candidate — 2026-08-09

Patch candidate superseding `v1.0.0-candidate`. The mathematical content and
finite proof payload are unchanged. This version makes the nauty identity
audit portable across upstream/Homebrew executable names and Debian/Ubuntu's
`nauty-`-prefixed names, and installs the declared nauty dependency in GitHub
Actions. The original candidate tag and release remain immutable for audit.

## v1.0.0-candidate — 2026-08-09

Initial unrefereed Evidence Press child candidate of the TxGraffiti conjecture
3 resolution. The immutable parent is archived at
<https://doi.org/10.5281/zenodo.21852504>.
The child candidate is archived at
<https://doi.org/10.5281/zenodo.21857209>.

### Mathematical scope

- Defines bilateral deficiency intrinsically through bipolar residual
  restrictions.
- Proves a size-preserving bijection and solution-polynomial correspondence
  with independent dominating sets of formula graphs.
- Develops algebraic operations, MaxSAT recovery, and the fixed-width
  complexity boundary while separating exact clause width from exact signed
  occurrence.
- Establishes bilateral deficiency as the exact gap coordinate
  \(i(G)-\mu^*(G)\) for regular graphs equipped with a dominating induced
  matching.
- Proves the constructive regular-DIM upper bound, including the cubic
  \(7/6\) ratio bound.
- Gives a connected edge-cover amplifier and connected cubic-DIM families with
  linear gap; the \(1/72\) density is sharp within that construction.
- Proves that order 50 is minimum among finite simple cubic graphs admitting a
  dominating induced matching and satisfying \(i(G)>\mu^*(G)\).

### Assurance additions

- Three named finite threshold encodings have native- and Lean-checked direct
  LRAT paths; four native derivations are retained across the three formulas.
- The eight-variable terminal signature is proved exactly in Lean from a
  visible hard-coded transcription of the ten attributed clauses.
- A standard-library clean-room validator independently reconstructs the
  threshold encoding and checks a seven-formula exhaustive semantic corpus.
  This is producer-side validation, not independent reproduction.
- Imported results now have a typed dependency ledger.
- The artifact is separated into compact core, optional 5.79 GB extended proof,
  and documentation layers.

### Explicitly not part of this release

- journal submission or journal peer review;
- external specialist review;
- unaffiliated independent reproduction;
- a claim of minimum order outside the cubic-DIM class;
- exact determination of the cubic-DIM extremal constants;
- classification of all order-50 extremisers;
- full proof-assistant formalisation of the universal theory;
- a comprehensive or definitive novelty determination.

### Attribution and licensing

The scholarly author is Anonymous. Ian Pitchford acts only as package
maintainer and publisher. Original prose, data, and figures are CC BY 4.0;
original source code is MIT licensed; third-party material retains its upstream
terms.

### Lineage policy

This release is a new immutable child. It does not mutate the parent Evidence
Press or Zenodo payload. Later review, reproduction, formalisation, correction,
or extension should be separately versioned and linked.
