# AI index — bilateral-deficiency

## Identity and version

Documentation addendum: 2026-09-24. Indexes [source commit 6b141ec3ad64](https://github.com/ipitchford/bilateral-deficiency/tree/6b141ec3ad647ac64359f2fa8bd703b6c25e0abc) and candidate tag `v1.0.1-candidate`. This index was added after that release: it is **not** part of the original tag, DOI archive or frozen manifest. Existing release files and checksums remain unchanged. For historical manifest/allow-list checks, use a clean checkout of that tag, not this documentation-enriched branch. The addendum is authenticated by Git history.

[Release identity and DOI](README.md) · [Evidence Press context](https://evidencepress.org/releases/bilateral-deficiency-regular-dim/)

## Exact scope

Bilateral partial assignments of an indexed CNF give i(G(F))=|V(F)|+β(F). The paper develops the regular-DIM replacement bound and connected amplifier β(A(R))=|V(R)|−ν(R), with exact signed-occurrence (3,2,2) hypotheses. Order 50 minimality is within the cubic DIM class, not all cubic graphs.

The linked manuscript and claim register control all hypotheses and quantifiers; this index is a navigation aid, not a substitute proof.

## Claim and evidence map

- [MANUSCRIPT.md](MANUSCRIPT.md) — Definitions, hypotheses and proofs.
- [CLAIMS.json](CLAIMS.json) — Claims.
- [THEOREM_DEPENDENCIES.md](THEOREM_DEPENDENCIES.md) — Imported results.
- [ASSURANCE.md](ASSURANCE.md) — Finite formal verification boundary.
- [REPRODUCIBILITY_SUPPLEMENT.md](REPRODUCIBILITY_SUPPLEMENT.md) — Full commands and expected results.
- [proof/README.md](proof/README.md) — Encoding and certificates.
- [PRIOR_ART_SEARCH_LOG.md](PRIOR_ART_SEARCH_LOG.md) — Prior-art search.
- [PROVENANCE.md](PROVENANCE.md) — Provenance.
- [LICENSE.md](LICENSE.md) — Rights.

## Reproduce

From the indexed release root, after inspecting the commands and installing the documented environment:

```sh
python3 -m unittest discover -v
python3 -O -m unittest discover -v
```

The README records 25 tests per mode. Follow the supplement for C++, native LRAT and Lean checking; Python tests alone do not replay those layers. The optional 5,793,599,477-byte extended LRAT object is separate from the source tree.

## Trust boundary and safe reuse

Lean checks identified finite encodings and the enforcer terminal table, not the universal theory or compiler correctness. The extended object is not a premise of the amplifier theorem; imported SAT 2024 and O–West results remain dependencies.

No new mathematical validation, formalisation, independent reproduction or novelty audit was performed for this documentation repair. Preserve the anonymous attribution and existing citation metadata. Distinguish producer checks, finite formal results, universal written arguments and external review. Before downstream reuse, match the exact statement and dependency scope and check subsequent corrections; a DOI or successful command alone is not proof of correctness.

## Licence and provenance

Use the rights/provenance sources linked above and [README](README.md); cited and third-party material retains its own terms. This new index is dedicated under CC0-1.0, without changing any existing licence or attribution.

