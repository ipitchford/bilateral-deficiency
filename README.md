# Bilateral deficiency research and proof package

This package develops bilateral deficiency from the public TxGraffiti
conjecture 3 release into a general indexed-CNF optimization parameter. It
contains the manuscript, written proofs, separately implemented exact solvers,
cross-model tests, a structural analyzer, algebraic conformance benchmarks,
three native- and Lean-checked finite threshold certificates, and a
parser-independent Lean proof of the enforcer's finite terminal signature.

The package does not import the original release verifier. The canonical CNF
is treated as an input object and checked through separate residual and graph
semantics.

## Release anchors

- Version: `1.0.1-candidate`
- DOI: <https://doi.org/10.5281/zenodo.21857209>
- Source: <https://github.com/ipitchford/bilateral-deficiency>
- Evidence Press: <https://evidencepress.org/releases/bilateral-deficiency-regular-dim/>
- Parent release: <https://doi.org/10.5281/zenodo.21852504>

The DOI is the archival identity for this child candidate. The Git tag binds
the compact source package; the separately listed extended LRAT object is
deposited under the same archival record but is not part of the GitHub source
tree.

## Principal mathematical result

For an indexed CNF \(F\), a partial assignment is bilateral when every
unassigned variable occurs in both signs among the indexed clauses not already
satisfied. The parameter is

\[
\beta(F)=\min_{\alpha\text{ bilateral}}
\bigl(|T_F(\alpha)|-|U(\alpha)|\bigr).
\]

The manuscript proves that bilateral assignments are in a size-preserving
bijection with independent dominating sets of the formula graph, giving
\(i(G(F))=|V(F)|+\beta(F)\). It develops residual, algebraic, complexity,
bounded-treewidth, regular-DIM, and exact signed-occurrence \((3,2,2)\)
spectrum consequences.

For every simple \(d\)-regular graph equipped with a dominating induced
matching, the package also proves the constructive replacement inequality

\[
i(G)\le \mu^*(G)+
\left\lfloor\frac{2(d-1)}{d\,2^d}\mu^*(G)\right\rfloor,
\]

including the cubic bound
\(i(G)\le\mu^*(G)+\lfloor\mu^*(G)/6\rfloor\).

The published \(E_{3,2,2}\) enforcer also yields a connected amplifier. For
every connected cubic skeleton \(R\), the generated exact signed-occurrence
\((3,2,2)\) formula
\(A(R)\) satisfies

\[
\beta(A(R))=\rho(R)=|V(R)|-\nu(R).
\]

For \(R=C_s\square K_2\), the associated connected cubic DIM graph has order
\(80s\), minimum maximal matching number \(24s\), and independent domination
number \(25s\). O--West extremal skeletons sharpen the attainable asymptotic
gap density of this construction from \(1/80\) to \(1/72\).

The SAT 2024 lower bound of 20 clauses for an unsatisfiable
\((3,2,2)\)-formula, combined with the coordinatisation counts, proves that
order 50 is minimum among cubic graphs admitting a dominating induced matching
and satisfying \(i(G)>\mu^*(G)\). The motivating graph attains that bound and
is connected. The minimum outside the DIM class remains open.

## Start here

- `MANUSCRIPT.md`: complete paper, including the connected amplifier theorem.
- `THEOREM_DEPENDENCIES.md`: typed ledger for every imported load-bearing result.
- `TERMINAL_CALCULUS.md`: exact min-plus terminal composition rule.
- `lean_terminal_signature.lean`: parser-independent formal check of the
  enforcer's complete four-entry finite signature.
- `generate_prism_amplifier.py`: reproducible connected-family generator.
- `generate_owest_amplifier.py`: extremal-matching skeleton amplifier.
- `paired_edge_normal_form.py`: exact normal form for the unresolved sign slice.
- `verify_connected_switch_proof.py`: full replay of the connected value-one
  occurrence switch.
- `REPRODUCIBILITY_SUPPLEMENT.md`: exact commands and assurance boundaries.
- `proof/README.md`: encoding lemma and lower-bound certificate chain.
- `verify_threshold_encoding_cleanroom.py`: production-independent structural
  and small-corpus semantic audit of the threshold encoding.
- `INTEGRITY_AUDIT.md`: post-revision claim/evidence and adversarial audit.
- `SHA256SUMS`: normative package-wide SHA-256 inventory; it lists every
  tracked release file other than itself.
- `PRIOR_ART_SEARCH_LOG.md`: bounded historical search and stopping rule.
- `review/`: internal and simulated review records; none is external specialist
  validation or journal peer review.

## Artifact layers

- **Core:** manuscript and supplement; source formulas; finite witnesses;
  semantics, tests and generators; compact threshold encodings and LRAT
  certificates; native checker source; Lean wrappers; hashes and replay receipt.
- **Extended:** the 5,793,599,477-byte connected-switch LRAT object. It is an
  optional conformance benchmark, not a premise of the connected amplifier or
  order-50 theorems. Its exact size and SHA-256 are recorded in
  `connectors/pp-beta1/LARGE_PROOF_MANIFEST.md`.
- **Documentation:** dependency, claim, assurance, provenance, environment,
  licensing and package-manifest records.

## Minimal verification

~~~sh
python3 -m unittest discover -v
python3 -O -m unittest discover -v

c++ -std=c++17 -O2 -Wall -Wextra -pedantic bd_exact.cpp -o bd_exact
./bd_exact instances/txgraffiti_15_20.cnf

make -C third_party/drat-trim lrat-check drat-trim
python3 verify_positive_base_proof.py \
  --receipt receipts/positive-base-proof-verification.json
python3 verify_enforcer_composition_proof.py \
  --receipt receipts/enforcer-composition-proof-verification.json
python3 verify_threshold_encoding_cleanroom.py \
  instances/txgraffiti_15_20.cnf \
  proof/positive-base-beta-le-0.cnf \
  proof/positive-base-encoding-map.json \
  --receipt receipts/threshold-encoding-cleanroom-validation.json
lean --run lean_terminal_signature.lean

for d in generated/exact-gap-0 generated/exact-gap-3 \
         generated/exact-gap-minus-2 generated/general-minus-4
do
  python3 verify_benchmark.py "$d" --exact-solver ./bd_exact
done
~~~

Expected headline results are 25/25 tests in each Python mode, exhaustive
\(\beta(P)=1\), native verification of the compact LRAT paths, Lean
verification of the 118,497- and 35,737-action direct LRAT proofs, Lean
verification of the four-entry terminal signature, and benchmark values
\(0,3,-2,-4\).

The extended full connected-switch replay is deliberately separate because
its direct LRAT file is 5,793,599,477 bytes and checking it takes minutes:

~~~sh
python3 verify_connected_switch_proof.py \
  --receipt receipts/connected-switch-proof-verification.json
~~~

The expected result is a reconstructed connected exact signed-occurrence
\((3,2,2)\) formula
with \(\beta=1\), native `VERIFIED`, and Lean verification of 11,393,023 LRAT
actions. Use `--skip-lean` for a faster native-only integrity pass; that weaker
run must not replace the recorded full receipt.

## Assurance boundary

- Written proofs establish the universal theorems.
- A bilateral witness establishes an upper bound.
- Exhaustive receipts record finite searches but are not proof-system logs.
- LRAT proves three finite threshold encodings unsatisfiable; four native
  derivations and three direct Lean paths are supplied.
- The written encoding lemma and clean-room conformance checks connect those
  CNFs to the corresponding bilateral-deficiency lower bounds.
- The threshold compiler accepts canonical set-valued source clauses. It
  permits tautologies but rejects repeated literal tokens rather than silently
  normalizing arbitrary DIMACS input.
- Lean also proves the finite enforcer terminal table from hard-coded clauses;
  the general theory is not fully formalized.
- Hashes establish artifact identity, not mathematical correctness.
- Historical priority, journal acceptance, and community adoption are external
  questions.

## Release status

This is an anonymously attributed, unrefereed Evidence Press candidate. No
journal submission or external specialist review has been undertaken. The
repository and archival record are public release infrastructure, not evidence
of independent reproduction, peer review, novelty, or mathematical acceptance.
Original prose, data and figures are released under CC BY 4.0; original source
code is MIT licensed; vendored third-party material retains its upstream terms.
