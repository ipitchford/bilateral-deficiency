# Connected-switch large proof object

The compact source archive intentionally omits
`beta-le-0-direct.lrat` because it is 5,793,599,477 bytes. The normative proof
object remains a separate artifact with:

~~~text
filename: beta-le-0-direct.lrat
bytes: 5793599477
lines/actions: 11393023
sha256: 323402633cf890918c5690080279973a99fdd63fc80802d60842a958ba13db7f
encoding: beta-le-0.cnf
encoding_sha256: 54493aeb68ecd3d276cbf73765ef6c727275fc71e7a84ad195cdb1d0d8830c9d
~~~

`receipts/connected-switch-proof-verification.json` records a clean full
replay. The pinned native checker reports `c VERIFIED`, and Lean 4.32.1 parses
11,393,023 LRAT actions and reports `s LEAN_LRAT_VERIFIED`.

From a checkout containing the proof object at this path, run:

~~~sh
python3 verify_connected_switch_proof.py \
  --receipt receipts/connected-switch-proof-verification.json
~~~

The proof establishes unsatisfiability of the byte-identical threshold CNF.
The general encoding lemma in `proof/README.md` is the semantic bridge from
that finite CNF to \(\beta>0\); the explicit witness then gives \(\beta=1\).
