# Peer Review Report — Proof Engineering and Research Software

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission draft
- **Review date:** 8 August 2026
- **Review round:** 1

## Reviewer information

- **Role:** Peer Reviewer 3 (Cross-disciplinary perspective)
- **Identity:** formal-methods and research-software specialist working on proof certificates, reproducibility, and AI-assisted mathematics
- **Focus:** whether the artifact makes claims checkable, separates evidence types, and substantiates the six infrastructure-oriented uses

## Overall assessment

- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject
- **Confidence:** 4/5

This paper combines a mathematical parameter theory with an executable artifact that enumerates bilateral assignments, constructs formula graphs, compares full solution spectra, routes structural methods, and builds prescribed-value benchmarks. Its strongest research-software feature is epistemic typing: the prose repeatedly distinguishes a witness, a search receipt, a structural proof, a proof log, and universal mathematics. The supplement records not only successful runs but two concrete failures, including a residual-polarity bug caught through cross-representation testing. This is exemplary practice for AI-assisted computational mathematics. The principal shortcoming is that the most important positive optimum still lacks a proof object whose validation trusts less code than the search itself. Cross-model agreement is valuable, but the Python and C++ implementations share the same human/AI-derived specification and do not constitute independent mathematical certification. The package is also not yet archival: source paths are local, the repository revision/DOI is missing, and the hash table is not yet bound to a signed release manifest. The six uses are credible as demonstrated workflows, not yet as performance or adoption claims. I recommend major revision centred on a proof-producing lower bound and immutable release engineering.

## Strengths

### S1. Evidence types are explicitly separated

Section 7.2 states that an upper witness proves only an upper bound, an exhaustive receipt depends on implementation, and a structural proof or proof log has a different assurance role. Supplement S1 repeats this hierarchy. This prevents a common category error in computational mathematics.

### S2. Cross-representation tests compare more than optima

Supplement S5 compares the forward and inverse maps and the complete coefficient identity \(D_i(G(F),z)=z^kB_F(z)\) over more than one hundred small formulas. Matching full spectra is much more sensitive to implementation defects than matching one optimum.

### S3. Failure disclosure is technically informative

Supplement S7 explains that the first C++ scan recorded an unassigned polarity before determining that the clause was satisfied. It also records a TeX serialization/control-byte failure. Both incidents motivate concrete controls rather than generic claims of “careful validation.”

### S4. Generated benchmarks are cryptographically bound to their graph images

Supplement S6 verifies manifests, CNF and graph hashes, recipes, distinct component templates, reconstruction, and additive values. The mutation-rejection test demonstrates that binding failures are detected.

## Weaknesses

### W1. The positive-base lower bound is not independently checkable

**Problem:** The canonical \(\beta=1\) result is supported by a deterministic exhaustive receipt and cross-implementation agreement, but not by a DRAT/LRAT-style proof, verified branch tree, proof assistant object, or short structural inequality.

**Why it matters:** This base value supports separation and every positive exact-\((3,2,2)\) benchmark. Re-executing a search program reproduces a computation; it does not reduce trust to a small checker.

**Suggestion:** Encode \(\beta(P)\le0\) as SAT or pseudo-Boolean feasibility, emit an unsatisfiability proof in a standard format, and validate it with at least one small independent checker. Bind the instance, encoding, proof, checker source, and checker output in the release manifest.

**Severity:** Critical for the strongest computer-assisted claims.

### W2. “Independent implementations” overstates independence without a provenance model

**Problem:** Section 7.2 calls the positive base implementation independently written, while the disclosure says AI assisted software generation and test design. Both implementations may share the same natural-language specification, examples, or generated logic.

**Why it matters:** Correlated design errors can survive agreement. The documented polarity bug shows that subtle semantic mistakes are realistic.

**Suggestion:** Describe independence operationally: authorship/provenance, shared test vectors, shared libraries, and whether one implementation was written without reading the other. Prefer “separately implemented” unless stronger independence is documented.

**Severity:** Major wording/assurance issue.

### W3. The artifact is reproducible locally but not yet a durable scholarly object

**Problem:** Declarations promise a future repository URL and DOI. The supplement records platform and hashes but no immutable archive identity, signed top-level manifest, license, environment capture, or clean-room reproduction transcript from a second machine.

**Why it matters:** Local reproducibility can decay. A published mathematical result should identify exactly which bytes underlie the computational base case.

**Suggestion:** Create a versioned archive with license, top-level SHA-256 manifest, environment/build instructions, source-only build, generated proof objects, and an external clean-room reproduction record. Deposit it in a DOI-minting repository.

**Severity:** Major.

### W4. Hash checking authenticates consistency, not source authority

**Problem:** The package uses cryptographic hashes effectively, but readers could mistake them for proof that the hashed content is correct or historically authoritative.

**Why it matters:** Hashes detect mutation relative to a manifest; they do not validate the semantics, theorem, or origin of the manifest.

**Suggestion:** Add one explicit sentence distinguishing integrity binding from mathematical validation and sign the release tag/manifest if an author identity is to be authenticated.

**Severity:** Minor.

### W5. The benchmark suite controls values but has narrow structural diversity

**Problem:** Prescribed values are assembled mainly by disjoint copies of one positive and one negative component, plus width lifting and replication.

**Why it matters:** Such instances are useful unit benchmarks but may be easy for component detection and are not evidence of solver robustness or representative hardness.

**Suggestion:** Label the current collection “algebraic conformance benchmarks.” Add connected, symmetry-varied, corrupted, and independently generated families before making any solver-evaluation claim.

**Severity:** Minor because the manuscript already disclaims representativeness.

## Detailed comments

### Mathematical-to-software interface

The indexed clause semantics are a sound choice: duplicates and explicit unused variables survive serialization. The witness round-trip in Section 3.3 gives a simple checker for feasibility and upper bounds. A corresponding parameter-native lower-bound format remains the missing half.

### Tests and receipts

Normal and `python -O` execution guards against assertion-only checks. The strongest tests enumerate independently expressed formula and graph solution spaces, and mutation rejection tests the package boundary. Add negative tests for malformed DIMACS indices, integer overflow limits in the C++ counters, and manifest path traversal if the verifier will process untrusted packages.

### AI-assistance claim

Section 7.6 supports a concrete architecture, not evidence that AI improves mathematical productivity. The wording is currently calibrated. The final archive should retain prompts/provenance only to the extent compatible with privacy and author policy, while the human authors remain accountable for the mathematical result.

### Reproducibility supplement

The supplement is unusually useful. The normative hash list should be generated mechanically at release time, and its generation command/script should itself be included and hashed.

## Questions for the authors

1. Can the positive lower bound be compiled to a standard unsatisfiability or pseudo-Boolean proof, and which independent checker will validate it?
2. What evidence supports the word “independent” for the Python and C++ implementations?
3. Will the final artifact include a source-only bootstrap that reproduces every generated file and receipt from an empty output directory?
4. Which threat model does the benchmark verifier assume: trusted local packages or adversarial archives?

## Minor issues

- Document counter types and overflow bounds in the C++ enumerator.
- Include license and citation metadata (`CITATION.cff`) in the archive.
- Generate rather than manually maintain the normative hash table.
- Reserve “certificate” for objects with an explicit checker and acceptance predicate.

## Dimension scores

| Dimension | Score | Descriptor | Notes |
|---|---:|---|---|
| Originality | 78 | Strong | Evidence-typed infrastructure is a meaningful contribution |
| Methodological rigor | 82 | Strong | Excellent finite controls; proof-producing lower bound missing |
| Evidence sufficiency | 69 | Adequate | Reproduction evidence strong, certification weak at the key base |
| Argument coherence | 88 | Strong | Claims and assurance boundaries line up well |
| Writing quality | 86 | Strong | Precise and admirably candid |
| Literature integration | 72 | Adequate | Proof-engineering sources/formats could be integrated more directly |
| Significance and impact | 79 | Strong | Strong model for research artifacts if finalized archivally |
| **Weighted average** | **79.2** | **Minor range numerically; Major Revision by proof-object/archive override** | The central computational optimum needs a smaller trusted base |
