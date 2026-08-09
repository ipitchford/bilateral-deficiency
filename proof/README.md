# Positive-formula certificates

This directory supplies a checker-verifiable proof that the canonical
15-variable formula \(P\) has \(\beta(P)=1\). The proof has two halves.

1. The ternary vector `0000***********` is bilateral, leaves 11 variables and
   12 indexed clauses residual, and therefore proves \(\beta(P)\le1\).
2. `positive-base-unsat.lrat` is a trimmed LRAT proof that the CNF encoding of
   \(\beta(P)\le0\) is unsatisfiable. The separately compiled `lrat-check`
   validates this derivation.
3. `positive-base-direct.lrat` is CaDiCaL's direct LRAT proof of the same fact.
   It is validated both by `lrat-check` and by Lean 4's
   `Std.Tactic.BVDecide.LRAT` checker through `lean_lrat_check.lean`.

Either verified LRAT proof establishes \(\beta(P)\ge1\), subject to the
encoding lemma below. The two files provide different certificate-production
paths rather than two logically necessary premises.

## Encoding lemma

For each formula variable \(x_j\), use Boolean variables
\(z_j^0,z_j^1,u_j\), constrained so exactly one is true. They mean that
\(x_j\) is assigned 0, assigned 1, or unassigned. For each indexed clause
\(C_a\), a Boolean variable \(r_a\) is defined by

\[
r_a\longleftrightarrow
\bigwedge_{\ell\in C_a}\neg s_\ell,
\]

where \(s_{x_j}=z_j^1\) and \(s_{\neg x_j}=z_j^0\). Thus \(r_a=1\) exactly
when no literal in \(C_a\) has been assigned true. Bilaterality is encoded by

\[
u_j\to\bigvee_{a:x_j\in C_a}r_a,
\qquad
u_j\to\bigvee_{a:\neg x_j\in C_a}r_a.
\]

It remains to express \(\sum_a r_a-\sum_j u_j\le0\). Order the input bits as
\(r_1,\ldots,r_m,u_1,\ldots,u_k\), with respective weights
\(+1,\ldots,+1,-1,\ldots,-1\). For every reachable prefix difference \(d\),
introduce a one-hot state \(q_{i,d}\). Set \(q_{0,0}=1\). If input bit \(b_i\)
has weight \(w_i\), add the two implications

\[
q_{i-1,d}\wedge\neg b_i\to q_{i,d},
\qquad
q_{i-1,d}\wedge b_i\to q_{i,d+w_i}.
\]

Exactly one state is true in each layer, and every final state with \(d>0\)
is forbidden.

**Lemma.** The generated CNF is satisfiable if and only if there is a
bilateral partial assignment \(\alpha\) with
\(\delta_P(\alpha)=|T_P(\alpha)|-|U(\alpha)|\le0\).

**Proof.** Given a satisfying Boolean assignment, the exactly-one state bits
define a unique ternary assignment. The equivalence clauses make \(r_a\) the
indicator of membership in \(T_P(\alpha)\), and the two polarity clauses make
every unassigned variable bilateral. Induction on \(i\) in the transition
clauses gives

\[
q_{i,d}=1\quad\Longrightarrow\quad
d=\sum_{h\le i}w_hb_h.
\]

The unique allowed final state therefore has nonpositive difference.
Conversely, a bilateral \(\alpha\) with nonpositive difference determines the
state variables and residual bits. Setting the unique true prefix state to
its actual difference satisfies every transition and final clause. Hence it
extends to a satisfying Boolean assignment. \(\square\)

## Reproduction

From the artifact root:

~~~sh
python3 generate_positive_base_cnf.py \
  instances/txgraffiti_15_20.cnf \
  proof/positive-base-beta-le-0.cnf \
  --map proof/positive-base-encoding-map.json

make -C third_party/drat-trim lrat-check drat-trim

python3 verify_positive_base_proof.py \
  --receipt receipts/positive-base-proof-verification.json
~~~

Verification does not require regenerating a proof. To reproduce the two
generation paths with CaDiCaL 3.0, use:

~~~sh
cadical --unsat --binary \
  proof/positive-base-beta-le-0.cnf \
  proof/positive-base-unsat.dratb

third_party/drat-trim/drat-trim \
  proof/positive-base-beta-le-0.cnf \
  proof/positive-base-unsat.dratb \
  -i -L proof/positive-base-unsat.lrat

cadical --unsat --lrat --no-binary --checkproof=2 \
  proof/positive-base-beta-le-0.cnf \
  proof/positive-base-direct.lrat
~~~

CaDiCaL uses exit status 20 for UNSAT. The packaged proof files are normative;
a newly generated proof need not be byte-identical because solver versions and
proof scheduling can change, but it must verify against the same byte-identical
encoding.

The pinned checker source is the official `drat-trim` repository at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The checker establishes the LRAT
derivation, not the encoding lemma; the displayed proof establishes the
encoding lemma, not the correctness of a particular proof file. Together with
the upper witness they establish the exact value.

The Lean run adds a proof-assistant-checked certificate path: the theorem
`LRAT.check_sound` converts a successful checker result to `CNF.Unsat`. The
artifact's narrow DIMACS parser and the conversion from file bytes to Lean's
CNF representation remain in the trusted translation boundary. Consequently,
the correct assurance description is *Lean-checked LRAT unsatisfiability plus
a written encoding lemma*, not complete formalization of bilateral deficiency.

## Clean-room encoding validation

`verify_threshold_encoding_cleanroom.py` adds a producer-side implementation
check for the translation obligation. It uses only the Python standard library
and deliberately imports neither the production compiler nor `bd_core.py`.
Starting from the mathematical DIMACS formula and the public variable map, it
independently:

1. checks that the named variables form a bijection onto every CNF variable;
2. reconstructs the ternary-state, residual, bilaterality, balance-transition,
   and threshold clauses;
3. compares the reconstruction with the packaged CNF clause-by-clause, as both
   a logical multiset and the declared canonical sequence; and
4. runs a small declared formula corpus through the production compiler, then
   compares exhaustive mathematical evaluation of every ternary assignment
   with a separate standard-library DPLL solver, both globally and with each
   ternary state fixed.

Replay the audit and regenerate its deterministic receipt with:

~~~sh
python3 verify_threshold_encoding_cleanroom.py \
  instances/txgraffiti_15_20.cnf \
  proof/positive-base-beta-le-0.cnf \
  proof/positive-base-encoding-map.json \
  --receipt receipts/threshold-encoding-cleanroom-validation.json
~~~

This closes a concrete common-mode implementation risk more tightly than a
hash or solver rerun alone. It remains producer-side clean-room validation,
not external reproduction, independent expert review, proof-assistant
formalisation, or a proof of the universal theory.

## Generic threshold compiler and additional positive formulas

`generate_positive_base_cnf.py` accepts an arbitrary integer `--threshold q`;
its proof is unchanged except that final balance states above \(q\) are
forbidden. The frozen \(q=0\) output for \(P\) remains byte-identical.

`verify_enforcer_composition_proof.py` applies the same compiler and proof
chain to a second 15-variable positive formula composed from opposite-polarity
copies of the published SAT 2024 enforcer. Its direct LRAT file has 35,737
actions and passes both native and Lean checking.

`verify_connected_switch_proof.py` reconstructs a connected 30-variable
formula from two copies of \(P\), verifies its value-one witness, regenerates
the 2,686-variable threshold encoding byte-for-byte, and checks the direct
LRAT proof natively and with Lean. That proof has 11,393,023 actions and is
5,793,599,477 bytes, so it is stored under `connectors/pp-beta1/` rather than
this directory. These additional certificates validate finite formulas and
the reusable compiler; they do not formalize the connected amplifier theorem.

## Parser-independent enforcer terminal lemma

`lean_terminal_signature.lean` hard-codes the ten displayed clauses of the
SAT 2024 eight-variable enforcer. It independently defines tri-state residual
semantics, internal bilaterality, terminal polarity masks, and the delayed
terminal local cost. The theorem `enforcer_terminal_signature_exact` uses
`native_decide` to evaluate all \(3^8=6561\) partial assignments and proves that
the complete terminal table has exactly four rows:

\[
(0,\varnothing,0),\quad (1,\varnothing,1),\quad
(*,\varnothing,1),\quad (*,\{-\},1).
\]

Replay the finite proof from the artifact root with the pinned Lean toolchain:

~~~sh
lean --run lean_terminal_signature.lean
~~~

The expected final line is `s LEAN_TERMINAL_SIGNATURE_VERIFIED`. This proof
has no DIMACS-parser or Python dependency. Its translation boundary is the
visible transcription of the ten mathematical clauses into the Lean list;
it proves the finite signature, not the universal terminal-composition or
connected-amplifier theorem.
