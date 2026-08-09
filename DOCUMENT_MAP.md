# Document and artifact map

## Reading order

1. `STATUS.md` — release status, scope qualifier, and open boundaries.
2. `MANUSCRIPT.md` — complete mathematical argument and canonical references.
3. `CLAIMS.json` — machine-readable claim ledger.
4. `ASSURANCE.md` — interpretation of written, computational, certificate, and
   formal evidence.
5. `REPRODUCIBILITY_SUPPLEMENT.md` — commands, expected outputs, and detailed
   proof chain.
6. `THEOREM_DEPENDENCIES.md` — typed transfers for imported results.
7. `INTEGRITY_AUDIT.md` — adversarial claim/evidence audit.

## Core release layer

The compact core is intended to contain:

- manuscript source and rendered release PDF;
- `README.md`, the reproducibility supplement, claim/assurance/status records,
  provenance, environment, release notes, licences, and citation metadata;
- canonical formulas in `instances/` and generated conformance fixtures in
  `generated/`;
- original Python and C++ solvers, analyzers, compilers, generators, and tests;
- `TERMINAL_CALCULUS.md`, `terminal_signature.py`, and
  `lean_terminal_signature.lean`;
- theorem-critical threshold CNFs, maps, compact LRAT files, native-checker
  source, Lean wrapper, and receipts in `proof/`, `third_party/`, and
  `receipts/`;
- the connected-switch source formula, threshold CNF, map, search receipt, and
  `connectors/pp-beta1/LARGE_PROOF_MANIFEST.md`.

The core contains enough information to inspect the universal written proofs,
run the normal conformance suite, replay the two compact certificate chains,
and identify the optional large proof exactly.

## Extended release layer

`connectors/pp-beta1/beta-le-0-direct.lrat` is a 5,793,599,477-byte direct
LRAT proof with SHA-256
`323402633cf890918c5690080279973a99fdd63fc80802d60842a958ba13db7f`.
It belongs in the archival extended layer, not Git history or the compact
source ZIP. Its receipt is
`receipts/connected-switch-proof-verification.json`.

The extended object is optional finite conformance evidence. It is not a
logical premise of the written connected-amplifier or order-50 theorems.

## Documentation and development context

- `PRIOR_ART_SEARCH_LOG.md` records a bounded search, not a novelty guarantee.
- `SHA256SUMS` is the normative inventory of every tracked release file other
  than the inventory itself.
- `review/` contains internal and simulated review records. These files are
  development context and are not external specialist or journal reviews.
- `RESEARCH_REPORT.md` and `PAPER_BLUEPRINT.md` are development records; where
  wording differs, the release manuscript and claim ledger control.

## Excluded local material

The public source archive should exclude:

- `literature/`, including downloaded papers and extracted full text;
- generated executables and object files;
- Python caches and local test caches;
- scratch material under `work/`;
- intermediate HTML and PDF renderings other than the designated release PDF;
- the 5.79 GB LRAT object from Git and the compact ZIP;
- credentials, tokens, editor state, and operating-system metadata.

`LICENSE.md` governs original material by type, while
`THIRD_PARTY_NOTICES.md` and directory-local licences govern upstream material.

The designated rendered files are
`output/pdf/bilateral-deficiency-regular-dim-v1.0.1-candidate.pdf` and
`output/pdf/bilateral-deficiency-reproducibility-supplement-v1.0.1-candidate.pdf`.
