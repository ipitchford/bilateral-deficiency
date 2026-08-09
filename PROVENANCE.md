# Provenance and lineage

## Release lineage

This package is an immutable child candidate of:

- **Public parent:** *TxGraffiti Conjecture 3: Resolution by an Order-50 Cubic
  Counterexample*, Evidence Press,
  <https://evidencepress.org/releases/txgraffiti-c3-resolution/>.
- **Parent archive:** <https://doi.org/10.5281/zenodo.21852504>.

The child identity is:

- **Archive:** <https://doi.org/10.5281/zenodo.21857209>.
- **Source:** <https://github.com/ipitchford/bilateral-deficiency>.
- **Evidence Press:**
  <https://evidencepress.org/releases/bilateral-deficiency-regular-dim/>.

The child develops the motivating finite object into a bilateral-deficiency
theory, a regular-DIM coordinatisation, connected amplification, and a
DIM-qualified minimum-order theorem. It does not amend or replace the parent
payload, receipts, status, or public claims. Any later correction,
formalisation, review, or independent reproduction should likewise be issued
as a separately identified descendant or related record.

## Scholarly and publication roles

- **Scholarly author:** Anonymous.
- **Package maintainer and publisher:** Ian Pitchford.
- **Role boundary:** Ian Pitchford's repository, archive, and Evidence Press
  maintenance does not confer scholarly authorship. Evidence Press publication
  does not confer peer-review or expert-endorsement status.
- **AI assistance:** AI systems assisted with research, calculation, code,
  checking, editing, and release preparation. Their outputs were treated as
  untrusted until checked through the documented workflows; AI systems are not
  authors. The manuscript contains the controlling disclosure.

## Local mathematical inputs

The canonical motivating formula is
`instances/txgraffiti_15_20.cnf`, bound in the receipts by SHA-256
`d6b1d133018e4237fef73c3ed895a956e23f3d588dd92206254d49dfdc742813`.
Generated formulas, graphs, threshold encodings, witnesses, and receipts are
derived from source scripts in this package. Indexed clause multiplicity is
part of the mathematical data and must not be normalised away.

## Load-bearing external dependencies

The complete typed transfer ledger is `THEOREM_DEPENDENCIES.md`. Its three
principal sources are:

1. Zhang, Peitl, and Szeider (SAT 2024), DOI
   <https://doi.org/10.4230/LIPIcs.SAT.2024.31>: the displayed
   \(E_{3,2,2}\) enforcer and the 20-clause bounded-occurrence lower bound.
2. O and West (2010), DOI <https://doi.org/10.1002/jgt.20443>: matching bounds
   and the cubic equality family used in the amplifier-density calculation.
3. Chlebík and Chlebíková (2008), DOI
   <https://doi.org/10.1016/j.ic.2008.07.003>: prior partial-assignment cost
   decomposition relevant to the originality boundary.

These results remain imported. Local checks validate the recorded
transcriptions, convention transfers, and downstream consequences, not the
external proofs themselves.

## Proof-object provenance

- The core threshold encodings are deterministically regenerated from their
  named formulas and maps.
- Compact LRAT objects are checked by the vendored `drat-trim` native checker,
  pinned to commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, and the direct
  proofs are also checked by Lean 4.32.1.
- `lean_terminal_signature.lean` is independent of the DIMACS parser and
  hard-codes the ten attributed enforcer clauses.
- The clean-room validator is implementation-separated within the same
  producer workflow; it is not an unaffiliated reproduction.
- The connected-switch direct LRAT object is 5,793,599,477 bytes with SHA-256
  `323402633cf890918c5690080279973a99fdd63fc80802d60842a958ba13db7f`.
  It is distributed as an extended archival asset and is excluded from the
  compact source archive.

## Identity controls

The immutable tag, archival deposit, checksums, and public readback records
bind bytes and lineage. They do not upgrade the candidate's review or
mathematical-assurance status.
