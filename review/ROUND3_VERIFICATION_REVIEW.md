# Round 3 Verification Review

## Decision

### Minor Revision before external specialist review

This is an adversarial internal re-review, not external peer review or journal
acceptance. The revised manuscript closes the two mathematical extensions that
were open in Round 2: connected positive amplification and the minimum order
of a cubic-DIM counterexample. It also derives a precise paired-edge normal
form for the still-unclassified exact \((3,2,2)\) sign problem and records a
counterexample to the tempting matching-only simplification. No new fatal
error was found in the stated theorem chain.

The decision remains Minor Revision because author-controlled metadata,
licensing, archival deposition, external priority review, and independent
human proof reading are absent. Open exact complexity and sharp-constant
questions are correctly labelled research problems rather than incomplete
proofs of stated theorems.

## Revision response checklist

### Priority 1 — former mathematical and assurance objections

| # | Original concern | Author-side claim | Status | Revision location | Verified? | Quality assessment |
|---|---|---|---|---|---|---|
| A1 | Formula-side significance might reduce to transport from the 2008 graph cost | Added constructive regular-DIM bounds, terminal calculus, connected amplifier, minimality, and paired-edge theory | FULLY_ADDRESSED for internal readiness | Sections 5.8 and 6 | Yes | These are formula-native or family-wide consequences. Venue significance remains an external editorial judgment. |
| A2 | Proper exact \((3,2,2)\) sign complexity remained open | Derived the exact paired-edge surplus identity and falsified a matching-only shortcut; retained open status | FULLY_ADDRESSED as an honest research boundary | Section 5.8; `paired_edge_normal_form.py`; counterexample receipt | Yes | The revision advances and isolates the problem without claiming an unsupported P/NP classification. |
| A3 | Positive spectrum constructions were disconnected | Proved the connected edge-cover amplifier and separately certified a connected value-one 2-switch | FULLY_ADDRESSED for positive amplification | Theorem 12; connected proof receipt | Yes | Arbitrary signed connected realization remains open and is stated as such. |
| A4 | Smallest counterexample order was unknown | Combined the SAT 2024 20-clause theorem with exact incidence counts | FULLY_ADDRESSED | Corollary 13 | Yes | The proof covers tautological and repeated indexed clauses by deletion/collapse before invoking the imported lower bound. Classification of all equality cases remains open. |
| A5 | Finite positive claims required stronger independent checks | Added second-base and connected-switch native/Lean LRAT paths | FULLY_ADDRESSED for the encoded finite claims | Appendix A; Section 8; proof and connector receipts | Yes | The encoders and DIMACS/Lean wrappers remain translation obligations and are disclosed. |

### Priority 2 — scholarly and artifact objections

| # | Original concern | Status | Notes |
|---|---|---|---|
| B1 | Priority search was not exhaustive | PARTIALLY_ADDRESSED | New O--West, SAT 2024, and rainbow-matching adjacency checks are logged. MathSciNet, zbMATH, theses, non-English literature, and specialist review remain unexhausted. |
| B2 | Artifact lacked a durable release boundary | PARTIALLY_ADDRESSED | Hashes, pinned checker, receipts, and replay commands are present. Public repository, license, DOI, and submission archive remain author-controlled. |
| B3 | General theory lacked proof-assistant formalization | ACKNOWLEDGED_LIMITATION | Three finite UNSAT claims are Lean-checked; the universal theorems remain written mathematics. The manuscript states this accurately. |
| B4 | Exact constants were not known | ACKNOWLEDGED_LIMITATION | The certified intervals are \(16/15\le C_3^{\rm DIM}\le7/6\) and \(1/72\le\lambda_3^{\rm DIM}\le1/20\); only the edge-cover-amplifier subclass is asymptotically sharp at \(1/72\). |

### Priority 3 — author-controlled submission items

| # | Item | Status |
|---|---|---|
| C1 | Author names, affiliations, ORCIDs, and approved CRediT roles | NOT_ADDRESSED; requires authors |
| C2 | Funding and competing-interest declarations | NOT_ADDRESSED; requires authors |
| C3 | Rights-holder-selected license | NOT_ADDRESSED; requires rights holder |
| C4 | Public repository, archival DOI, and immutable submission manifest | NOT_ADDRESSED; requires release authority |
| C5 | Human SAT/complexity and domination-theory proof reading | NOT_ADDRESSED; external action |

## New issues found during re-review

| # | Severity | Location | Finding and required handling |
|---|---|---|---|
| NEW-1 | Minor/engineering | `connectors/pp-beta1/` | The connected direct LRAT is 5,793,599,477 bytes. Deposit it as a separately identified proof object or compressed archive; do not silently omit it from a package that claims self-contained replay. |
| NEW-2 | Minor/assurance | Theorem 12, equation (6.1) | The terminal signature is a transparent \(3^8\)-state exhaustive lemma, not an LRAT-certified table. Keep the checker-assisted label and invite independent replay or a future proof-logged signature compiler. |
| NEW-3 | Minor/presentation | Abstract and Section 5 | General fixed-width hardness and the exact \((3,2,2)\) slice could be conflated. The revised abstracts now say “unrestricted occurrences” and explicitly identify the open paired-edge slice. |

## Decision rationale

All formerly critical internal proof obligations now have either conventional
written proofs or an explicit finite witness plus regenerated SAT encoding,
LRAT contradiction, and native/Lean replay. The connected amplifier and
order-50 theorem materially strengthen the graph-theoretic contribution. The
matching-only counterexample is also a positive integrity result: it prevents
an attractive but false complexity claim from entering the paper.

The remaining mathematical questions are openly scoped extensions, not gaps in
the theorems as stated. The remaining blockers concern external scholarly
validation and author authority. The correct internal verdict is therefore
Minor Revision before external specialist review, not Accept, resolved in the
community, formally verified in full, or released.
