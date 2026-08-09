# Prior-art search log: bilateral deficiency

Date of final search pass: 2026-08-09  
Purpose: bound the historical claim in `MANUSCRIPT.md`; this log is not a
novelty certificate and does not affect the truth of the mathematical results.

## Search protocol

The search used exact-phrase and concept queries in public web indexes,
publisher pages, arXiv, and citation chains from the closest located papers.
Queries were varied across SAT, clausal deficiency, partial assignments,
autarkies, formula graphs, and independent domination. Results were inspected
for identity of all four defining features:

1. optimization over partial assignments;
2. residual indexed clauses not already satisfied;
3. two-polarity survival for every unassigned variable; and
4. the objective `residual clauses - unassigned variables`.

A source sharing only the arithmetic, graph architecture, or target graph
invariant was treated as an antecedent, not as an equivalent definition.

## Representative exact queries

The query set included the following strings and close spelling variants:

- `"bilateral deficiency" SAT`
- `"bilateral deficiency" CNF`
- `SAT "residual deficiency" partial assignment`
- `CNF "residual deficiency"`
- `"bipolar residual" SAT`
- `"bipolar restriction" CNF deficiency`
- `"partial assignment" "clauses" "unassigned variables" deficiency`
- `"partial assignment" "|T|-|U|" SAT`
- `SAT residual restriction clause variable difference`
- `formula graph independent domination SAT clause literal`
- `satgraph independent domination clause vertices literal pairs`
- `independent domination polynomial formula graph SAT`
- `autarky residual formula deficiency both polarities`
- `lean kernel maximum deficiency residual restriction`
- `Chlebik Chlebikova independent dominating set bad clauses D1 D2`
- `"|D1|" "bad clauses" independent dominating set`
- `exact (3,2,2) CNF independent domination`
- `independent domination cubic graph dominating induced matching complexity`
- `rainbow matching color class matching of size two complexity`
- `maximum matching connected cubic graph 4n/9 sharp balloons`

The search also followed references and citing sources for Zverovich's
satgraph paper, Chlebík--Chlebíková's bounded-degree independent-domination
reduction, the clausal-deficiency/autarky literature, and independent
domination polynomials.

## Located antecedents and classification

| Source | Located overlap | Boundary after inspection |
|---|---|---|
| Chlebík and Chlebíková (2008), Section 2.3, proof of Theorem 5, author-preprint pp. 10--11 | literal choices over their `3k` variables define a partial assignment; every bad clause contributes all replicated clause vertices; exact cost `|D|=|D1|+(5k)bt` | closest arithmetic antecedent; generically the cost is `n+t|T|-|U|` for `n` variables; no explicit bilateral feasible domain, residual parameter, all-solution bijection, or theory developed here |
| Zverovich (2006), *Satgraphs and independent domination. Part 1* | complementary literal pairs and clause vertices in a SAT-to-independent-domination graph | clause vertices form a clique, collapsing the optimum to a satisfiability indicator rather than retaining residual-clause count |
| Kullmann (2011) and Szeider (2004) | deficiency, maximum deficiency, autarkies, lean structure, and clause--variable difference | optimize over formulas, subfamilies, or autarkic structure, not the stated bilateral residual domain |
| Dod (2016) | independent domination polynomial and multiplicativity | establishes earlier polynomial terminology; no SAT residual parameter |
| Jahari and Alikhani (2018) | later study of the independent domination polynomial | cited as later polynomial literature, not as origin |
| Zhang--Peitl--Szeider (2024); Ahadi--Dehghan (2019) | exact signed-occurrence CNF classes, including the twice-positive/twice-negative setting; the former publishes the terminal enforcer and proves the 20-clause UNSAT lower bound used here | essential finite ingredient and minimality theorem, but different optimization targets |
| O--West (2010) | sharp matching lower bound and equality family for connected cubic skeletons | combined here with the new edge-cover amplifier; no bilateral-deficiency parameter |
| Le--Pfender (2014) and Hommelsheim--Jehmlich--Mühlenthaler (2026) | hardness of rainbow matching under small color classes, including two disjoint edges per color in the latter work | adjacent to the paired-edge normal form, but missing its induced-coverage condition and surplus objective; not a complexity proof for BD-Sign \((3,2,2)\) |
| TxGraffiti conjecture 3 release (2026) | motivating exact formula, graph, and verified finite gap | parent construction from which the present formula-side theory is extracted |

The published enforcer also generated a second 15-variable, 20-clause positive
base by opposite-polarity terminal composition. Canonical colored formula-graph
comparison found that object nonisomorphic to the TxGraffiti base, even after
allowing variable renaming and independent sign switches. This is an object-
identity result, not a novelty result: the construction is reported as an
attributed synthesis from the SAT 2024 enforcer.

Exact-phrase searches for `residual deficiency` also returned unrelated uses
in group theory. Those are lexical collisions only.

## Current historical statement

No equivalent definition containing all four defining features was found in
the inspected sources. The strongest warranted wording is therefore:

> Bilateral deficiency appears to be new as an explicitly defined SAT-style
> residual optimization parameter together with the bijective, algebraic,
> complexity, and regular-DIM theory developed here. The underlying
> partial-assignment cost decomposition has a 2008 antecedent.

This is explicitly not a claim of global priority.

## Unexhausted routes and stopping boundary

The following routes were not exhaustively searched and remain mandatory for
a journal-level priority audit:

- MathSciNet and zbMATH full-text/controlled-vocabulary searches;
- dissertations, habilitations, and non-English sources;
- hypergraph transversal and signed-incidence terminology not indexed as SAT;
- all citing literature for every deficiency/autarky source;
- non-digitized conference proceedings and unpublished notes;
- direct review by specialists in clausal deficiency and independent
  domination.

The search stopped when repeated query variants produced only the antecedent
classes above and no source matching all four defining features. This is a
practical stopping rule, not evidence that an unlocated source cannot exist.

## Stable primary links

- Chlebík--Chlebíková author PDF:
  https://pure.port.ac.uk/ws/files/82933/DOMINATING_elsart.pdf
- Dod arXiv record: https://arxiv.org/abs/1602.08250
- Focke et al. publisher record: https://doi.org/10.1145/3731452
- CaDiCaL 3.0 proceedings record:
  https://doi.org/10.4230/LIPIcs.SAT.2026.40
- DRAT-trim paper: https://doi.org/10.1007/978-3-319-09284-3_31
- LRAT verification paper:
  https://doi.org/10.1007/978-3-319-63046-5_14
- Zhang--Peitl--Szeider SAT 2024 paper:
  https://doi.org/10.4230/LIPIcs.SAT.2024.31
- O--West cubic matching paper: https://doi.org/10.1002/jgt.20443
- Rainbow matching complexity: https://arxiv.org/abs/1312.7253
