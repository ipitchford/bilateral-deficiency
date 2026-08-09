# Assurance statement

This document says what the package evidence establishes and, equally
importantly, what it does not establish. The machine-readable companion is
`ASSURANCE.json`.

## Evidence layers

| Layer | Present evidence | Strongest warranted description | Not warranted |
|---|---|---|---|
| Universal mathematics | Definitions and written proofs in `MANUSCRIPT.md` | Unrefereed mathematical candidate with explicit dependencies and open boundaries | Fully formalised theory, expert validation, correctness by consensus |
| Finite semantics | Exhaustive solvers, witnesses, structural tests, mutation tests, and generator receipts | Producer-side finite conformance checks | Proof of every universal theorem |
| Core lower bounds | Regenerated threshold CNFs, compact LRAT derivations, pinned native checker, and direct Lean LRAT checking | Native- and Lean-checked unsatisfiability of identified finite encodings | A formally verified compiler or universal encoding theorem |
| Terminal signature | Independent Python enumeration and a parser-independent Lean theorem over the ten hard-coded clauses | Formally checked exact finite four-row table | Independent validation of the imported source or a formal proof of the universal amplifier |
| Encoding bridge | Written encoding lemma plus a standard-library clean-room reconstructor, independent DPLL solver, exhaustive small corpus, and mutation control | Producer-side clean-room structural and semantic validation | Independent reproduction, external code audit, or proof-assistant formalisation of the compiler |
| Extended proof | 5,793,599,477-byte LRAT object checked natively and with Lean; hash-bound receipt | Additional finite conformance evidence for the connected switch | A premise required by the written general amplifier theorem |
| Identity and packaging | SHA-256 hashes, manifests, tagged source, archival record, and public readback when published | Artifact identity and release traceability | Mathematical truth, novelty, review, or acceptance |

## Current assurance flags

- **Unrefereed candidate:** yes.
- **Journal submission:** no.
- **External specialist review:** no.
- **Independent reproduction:** no.
- **Independent implementation by an unaffiliated party:** no.
- **Partial finite formal verification:** yes.
- **Full proof-assistant formalisation of the universal theory:** no.
- **Producer-side clean-room encoding validation:** yes.
- **Comprehensive novelty determination:** no.
- **Immutable parent/child release separation:** required for publication.

## Formal-verification boundary

Lean is used in two narrow ways:

1. Lean's LRAT machinery checks direct certificates proving that three named
   finite threshold CNFs are unsatisfiable. The relevant DIMACS parser,
   file-to-proposition conversion, and written encoding lemma remain part of
   the translation boundary.
2. `lean_terminal_signature.lean` hard-codes the ten enforcer clauses and uses
   native decision procedures to prove the exact finite terminal table over
   all 6,561 partial assignments. The visible clause transcription is its
   source boundary.

Accordingly, the package may say “three finite lower-bound encodings have
native- and Lean-checked LRAT certificates” and “the finite terminal signature
is checked in Lean.” It must not say that the bilateral-deficiency theory, the
regular-DIM theorem, or the complete paper is Lean-verified.

## Clean-room boundary

`verify_threshold_encoding_cleanroom.py` does not import `bd_core` or the
production threshold compiler. It independently reconstructs the symbolic map
and clauses, compares the complete 731-variable, 9,256-clause encoding, and
checks seven small formulas at both sides of their exact threshold using an
independent DPLL implementation and exhaustive ternary-state constraints.

The production compiler is still run as a black-box corpus producer within the
same producer workflow. “Clean-room validation” therefore
describes implementation separation inside the producer-side release. It is
not evidence of unaffiliated reproduction or specialist review.

## Imported-result boundary

The package imports the displayed SAT 2024 enforcer, the bounded-occurrence
20-clause lower bound, and O--West matching results. Local work checks the
transcriptions, conventions, and downstream arithmetic described in
`THEOREM_DEPENDENCIES.md`; it does not independently prove those sources.

## Publication boundary

Evidence Press publication, a Zenodo DOI, a GitHub release, CI success, and
successful public readback are distribution and identity controls. The child
candidate must remain explicitly linked to, and distinct from, the immutable
TxGraffiti parent record at doi:10.5281/zenodo.21852504.
