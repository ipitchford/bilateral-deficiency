# Bilateral deficiency as a SAT-style optimisation parameter

## Structural theory, computational behaviour, regular-DIM classification, and a reproducible infrastructure prototype

**Status:** archived Stage-1 research synthesis, superseded 9 August 2026  
**Scope:** indexed Boolean CNF formulas; finite simple graphs  
**Assurance:** written proofs plus clean-room exhaustive tests and exact receipts; not formal verification or peer review

> **Supersession note.** `MANUSCRIPT.md`, `INTEGRITY_AUDIT.md`, and the
> reproducibility supplement contain the final theorem numbering and later
> results: the constructive regular-DIM upper bound, exact terminal calculus,
> connected edge-cover amplifier, O--West density \(1/72\), global order-50
> minimality, and the paired-edge normal form. This report is retained as the
> research-stage record and is not the normative statement of current claims.

## Abstract

For an indexed CNF formula (F), define the **bilateral deficiency**

\[
\beta(F)=\min_{\alpha\ \mathrm{bilateral}}
\bigl(|T_F(\alpha)|-|U(\alpha)|\bigr),
\]

where (U(\alpha)) is the set of unassigned variables, (T_F(\alpha)) is the
indexed family of clauses not satisfied by an assigned literal, and
bilaterality requires every unassigned variable to occur in both polarities
among those residual clauses. This report establishes that \(\beta\) is a
mathematically distinct optimisation parameter, not merely notation for one
graph computation.

Its optimisation domain is exactly the set of bipolar residual restrictions:
\(\beta\) is the least ordinary clause-variable deficiency among them. There
is a size-preserving bijection between bilateral assignments of (F) and
independent dominating sets of the clause-literal graph (G(F)); consequently
the complete independent-domination polynomial is (z^kB_F(z)), where
(B_F) is the bilateral-deficiency Laurent polynomial. The parameter is
additive on variable-disjoint unions, is invariant under an exact width lift,
equals the MaxSAT defect at width at most two, and recovers the full MaxSAT
optimum after indexed clause replication. The decision problem changes from a
polynomial sign test at width two to NP-completeness at fixed threshold zero
for proper simple exact (r)-CNF at every fixed (r\ge3). It is tractable at
bounded incidence treewidth through the formula-graph translation.

For every (d)-regular graph with a specified dominating induced matching,
the graph is exactly a formula graph of a signed-occurrence-((d-1)) indexed
(d)-CNF, allowing tautological clauses, and

\[
i(G)-\mu^*(G)=\beta(F).
\]

Thus \(\beta\) classifies the full structured graph family by the sign and size
of its invariant gap. In the proper exact ((3,2,2)) subclass its spectrum is
all of \(\mathbb Z\), using verified \(+1\) and \(-1\) components.

The accompanying prototype independently implements the reference semantics,
exact enumeration, theorem-driven solver selection, compositional benchmark
generation, and machine-checkable additive manifests. These results support
all six proposed uses, with qualifications: discovery becomes systematic but
not polynomial; compact lower-bound certificates remain proof-system
dependent; algorithm selection is theorem-level rather than a guarantee of
wall-clock superiority; and suitability as AI-mathematics infrastructure is
demonstrated technically, not sociologically.

## 1. Indexed formulas and residual semantics

An **indexed CNF** is a finite sequence (F=(C_a)_{a\in A}) of clauses on an
explicit variable set (V(F)=\{x_1,\ldots,x_k\}). A clause is a set of
literals, so repeated positions inside one clause collapse. Extensionally equal
clauses at different indices remain different clauses. Empty and tautological
clauses are permitted unless a restricted class excludes them.

Let \(\alpha\in\{0,1,*\}^k\) be a partial assignment. Define:

- (U(\alpha)=\{x_j:\alpha(x_j)=*\});
- (T_F(\alpha)=\{a\in A:C_a\text{ has no assigned true literal}\});
- (F\!\upharpoonright\!\alpha) by deleting satisfied clauses and deleting
  assigned false literals from every surviving clause.

A residual formula is **bipolar** if each of its variables occurs positively
and negatively. The assignment \(\alpha\) is **bilateral** if, for every
unassigned (x_j), both (x_j) and \(\neg x_j) occur among the clauses
indexed by (T_F(\alpha)). Equivalently, every explicitly unassigned variable
survives in the residual and the residual is bipolar.

Complete assignments are bilateral vacuously. Hence

\[
\beta(F)=\min_{\alpha\ \mathrm{bilateral}}
\delta_F(\alpha),
\qquad
\delta_F(\alpha)=|T_F(\alpha)|-|U(\alpha)|
\]

is defined for every indexed CNF.

### Theorem 1 (residual-core characterisation)

\[
\boxed{
\beta(F)=
\min_{\substack{\alpha:\,F\upharpoonright\alpha\text{ bipolar}\\
V(F\upharpoonright\alpha)=U(\alpha)}}
\bigl(c(F\upharpoonright\alpha)-n(F\upharpoonright\alpha)\bigr).
}
\]

#### Proof

The surviving indexed clauses are exactly (T_F(\alpha)), so their number is
\(|T_F(\alpha)|\). An assignment is bilateral exactly when every unassigned
variable occurs in both polarities in the residual. In that case the residual
variable set is exactly (U(\alpha)), and its variable count is
\(|U(\alpha)|\). Thus its ordinary deficiency is
\(|T_F(\alpha)|-|U(\alpha)|\). Minimising over the same feasible assignments
gives the equality. \(\square\)

This is different from ordinary deficiency, maximum deficiency, and surplus.
Ordinary deficiency evaluates one formula; maximum deficiency maximises over
clause subfamilies; bilateral deficiency minimises over partial-assignment
residuals subject to a polarity constraint. A bipolar residual need not be
lean, so \(\beta\) is not merely the deficiency of a lean kernel.

## 2. Exact translation to independent domination

Construct (G(F)) with two literal vertices (v_j^-,v_j^+) joined by an edge
for every variable, one vertex (c_a) for every indexed clause, and an edge
from (c_a) to each literal vertex contained in (C_a). Clause vertices are
independent.

### Theorem 2 (size-preserving bijection)

The map

\[
\alpha\longmapsto
D_\alpha=
\{\text{literal selected by each assigned variable}\}
\cup\{c_a:a\in T_F(\alpha)\}
\]

is a bijection from bilateral assignments of (F) to independent dominating
sets of (G(F)). It satisfies

\[
|D_\alpha|=k+\delta_F(\alpha).
\]

Consequently,

\[
\boxed{i(G(F))=k+\beta(F).}
\]

#### Proof

For bilateral \(\alpha\), at most one endpoint of each complementary pair is
selected. A selected clause has no selected literal neighbour, by the
definition of (T_F(\alpha)), and clause vertices are mutually nonadjacent.
Thus (D_\alpha) is independent.

An assigned literal pair is dominated by its selected endpoint. A clause not
in (T_F(\alpha)) is dominated by a selected true literal, while a clause in
(T_F(\alpha)) is selected. If (x_j) is unassigned, bilaterality supplies a
selected residual clause incident with (v_j^+) and another (possibly the
same tautological clause) incident with (v_j^-). Hence (D_\alpha) dominates
the graph. Its size is

\[
(k-|U(\alpha)|)+|T_F(\alpha)|=k+\delta_F(\alpha).
\]

Conversely, let (D) be an independent dominating set. Independence selects
at most one literal from each complementary pair. Use the selected endpoint as
the assigned truth value and leave a variable unassigned if neither endpoint
is selected. A clause vertex belongs to (D) exactly when it has no selected
literal neighbour: independence proves the forward exclusion, and domination
proves the reverse inclusion. Thus the selected clause vertices are exactly
(T_F(\alpha_D)). Both endpoints of an unassigned pair must be dominated by
selected clause vertices, forcing both residual polarities. Hence
\(\alpha_D\) is bilateral. The two constructions recover one another and
preserve the displayed size. \(\square\)

### Corollary 2.1 (complete solution polynomial)

Define the Laurent polynomial

\[
B_F(z)=\sum_{\alpha\ \mathrm{bilateral}}z^{\delta_F(\alpha)}.
\]

If (D_i(G,z)=\sum_Dz^{|D|}) sums over all independent dominating sets, then

\[
\boxed{D_i(G(F),z)=z^kB_F(z).}
\]

This is stronger than equality of optimum values: it preserves every solution
size and its multiplicity. Independent-domination polynomials already exist as
graph invariants; the result identifies the exact formula-side polynomial for
formula graphs.

## 3. Closest prior art and the defensible novelty boundary

The claim that no equivalent cost identity occurs in inspected prior work must
be corrected.

### 3.1 Chlebík--Chlebíková is the closest antecedent

In their 2008 approximation-hardness reduction for bounded-degree Minimum
Independent Dominating Set, Chlebík and Chlebíková construct two literal
vertices per variable and (t) vertices per clause. For an independent
dominating set (D), they let (D_1) be its literal part, interpret (D_1) as
a partial assignment, call clauses without a selected literal *bad*, and state

\[
|D|=|D_1|+t\cdot(\text{number of bad clauses}).
\]

Writing \(|D_1|=k-|U|\), this is exactly
\(k+t|T|-|U|\). Their purpose is an approximation lower bound. They do not
state the bilateral feasibility condition, prove the converse for all partial
assignments, define a residual-deficiency parameter, derive an exact optimum
identity, or develop its algebraic and complexity theory. Nevertheless, the
cost decomposition is clearly implicit prior art and must be credited.

This antecedent is naturally absorbed by the weighted family

\[
\beta_t(F)=\min_{\alpha\ \mathrm{bilateral}}
\bigl(t|T_F(\alpha)|-|U(\alpha)|\bigr).
\]

If (F^{[t]}) repeats every indexed clause (t) times, then

\[
\beta_t(F)=\beta(F^{[t]}),
\qquad
i(G(F^{[t]}))=k+\beta_t(F).
\]

Thus the 2008 graph is the replicated-clause member of the present exact
framework.

### 3.2 Other close but non-equivalent antecedents

- Zverovich's satgraph has a clique on the clause side. At most one clause
  vertex can be selected, collapsing the optimum to (k) for satisfiable
  formulas and (k+1) for unsatisfiable formulas. It does not retain the mixed
  solution spectrum.
- Zhang, Peitl, and Szeider use clause-literal graph encodings to generate and
  classify small bounded-occurrence unsatisfiable formulas. This supplies
  architecture and exact-occurrence antecedents, not the present objective.
- Ahadi and Dehghan prove hardness for twice-positive/twice-negative 3-SAT and
  apply it to domination questions. Satisfiability alone does not determine
  the sign of \(\beta\).
- Kullmann and Szeider develop deficiency, maximum deficiency, matching
  autarkies, lean kernels, and surplus. Their optimisation domains differ from
  bipolar residual restrictions.

### 3.3 Priority statement

The strongest defensible statement is:

> Bilateral deficiency appears to be new as an explicitly defined SAT-style
> residual optimisation parameter with a size-preserving independent-domination
> bijection and the theory proved here. The underlying partial-assignment cost
> decomposition is implicit in Chlebík and Chlebíková (2008). Global priority
> is not secured by the bounded search.

A finite literature search cannot prove global priority. Unindexed theses,
non-English sources, alternative hypergraph terminology, and inaccessible full
texts remain residual risks.

## 4. Separation from familiar SAT quantities

### Proposition 3 (not ordinary or maximum deficiency)

Let

\[
F_0=(x)\wedge(y)\wedge(x\vee y),
\qquad
F_1=(x)\wedge(y)\wedge(\neg x\vee\neg y).
\]

Both have ordinary deficiency (3-2=1), and both have maximum deficiency
one. Yet (F_0) is satisfiable and has \(\beta(F_0)=0\), while (F_1) has
MaxSAT defect one and, by the width-two theorem below,
\(\beta(F_1)=1\). Therefore neither ordinary nor maximum deficiency determines
bilateral deficiency. \(\square\)

### Proposition 4 (not satisfiability or MaxSAT defect)

For

\[
H=(x\vee y\vee z)\wedge(\neg x\vee\neg y\vee\neg z),
\]

the empty assignment is bilateral with deficiency (2-3=-1). The formula is
satisfiable, so its MaxSAT defect is zero; the width-three occurrence bound
below excludes a lower value, giving \(\beta(H)=-1\).

The verified exact ((3,2,2)) positive component (P) has \(\beta(P)=1\)
and is unsatisfiable. The exact negative component (N) in Section 7 has
\(\beta(N)=-1\). Additivity gives unsatisfiable formulas

\[
\beta(P\sqcup N)=0,
\qquad
\beta(P\sqcup N\sqcup N)=-1.
\]

Hence satisfiable formulas may have negative \(\beta\), and unsatisfiable
formulas may have positive, zero, or negative \(\beta\). The parameter is not a
relabelled SAT or MaxSAT answer. \(\square\)

## 5. Algebraic behaviour

### Theorem 5 (additivity and convolution)

If (F_1,F_2) have disjoint variable sets, then

\[
\boxed{\beta(F_1\sqcup F_2)=\beta(F_1)+\beta(F_2)},
\qquad
\boxed{B_{F_1\sqcup F_2}(z)=B_{F_1}(z)B_{F_2}(z)}.
\]

#### Proof

A partial assignment on the union factors uniquely into assignments on the
two variable sets. It is bilateral exactly when both restrictions are
bilateral. Surviving clause counts and unassigned variable counts add, so
deficiencies add. Taking minima proves the first identity; summing all pairs
of assignments proves the polynomial convolution. \(\square\)

### Theorem 6 (exact width lift)

For each indexed clause (C_a), introduce a fresh variable (y_a) and replace
(C_a) by

\[
C_a\vee y_a,
\qquad
C_a\vee\neg y_a.
\]

Call the result (L(F)). Then

\[
\boxed{\beta(L(F))=\beta(F).}
\]

If (F) is proper, duplicate-free exact (r)-CNF, then (L(F)) is proper,
duplicate-free exact ((r+1))-CNF.

#### Proof

Restrict a partial assignment \(\alpha'\) to the original variables, obtaining
\(\alpha\). If (C_a) is satisfied by \(\alpha\), both lifted clauses vanish,
and bilaterality forces (y_a) to be assigned. Both sides contribute zero. If
(C_a) survives and (y_a) is assigned, exactly one lifted clause survives;
if (y_a) is unassigned, both survive while (y_a) contributes one unassigned
variable. In both residual cases the net contribution
\(|T|-|U|\) is one, matching the original surviving clause. The surviving
lifted clause or clauses retain all original unassigned literals, so bilateral
feasibility for original variables is preserved in both directions. Taking
minima proves the identity. Fresh variables distinguish the lifted clauses and
preserve proper exactness. \(\square\)

### Theorem 7 (MaxSAT recovery by indexed replication)

Let \(\tau(F)\) be the minimum number of clauses falsified by a complete
assignment. Repeat each indexed clause (r) times, with (r>k). Then

\[
\boxed{
\tau(F)=\left\lceil\frac{\beta(F^{[r]})}{r}\right\rceil.
}
\]

More precisely,

\[
\beta(F^{[r]})=r\tau(F)-u^*,
\]

where (u^*) is the largest number of variables that can remain unassigned in
a bilateral assignment leaving exactly \(\tau(F)\) original clauses residual.

#### Proof

Replication preserves bilaterality and changes the objective to
\(r|T|-|U|\). Every completion of a partial assignment falsifies at most its
\(|T|\) residual original clauses, so \(|T|\ge\tau(F)\). Hence

\[
r\tau(F)-k\le\beta(F^{[r]})\le r\tau(F),
\]

where the upper bound uses an optimal complete assignment. Because (r>k),
the interval contains no multiple-of-(r) ambiguity, proving the ceiling
formula. A minimiser cannot have \(|T|\ge\tau(F)+1\), since then its objective
would exceed the complete upper bound. It therefore minimises
\(r\tau(F)-|U|\), proving the refined statement. \(\square\)

## 6. The sharp width-two theorem

### Theorem 8

For every indexed CNF whose clauses have width at most two,

\[
\boxed{\beta(F)=\tau(F).}
\]

This includes indexed duplicates, units, empty clauses, and tautological binary
clauses.

#### Proof

An optimal complete assignment is bilateral, so \(\beta(F)\le\tau(F)\).

For the reverse inequality, take a bilateral assignment with residual formula
on (u) variables and (t) indexed clauses. Form the variable-clause
incidence bipartite multigraph, counting signed literal occurrences. For any
set (X) of residual variables, bilaterality supplies at least two occurrences
per variable, while every residual clause has at most two occurrences. Thus

\[
2|X|\le e(X,N(X))\le2|N(X)|,
\]

so Hall's condition \(|N(X)|\ge|X|\) holds. Match every residual variable to a
distinct containing clause. Set each variable to satisfy its matched literal;
the completion satisfies at least (u) distinct residual clauses and therefore
falsifies at most (t-u) clauses. Hence
\(\tau(F)\le t-u\). Minimising over bilateral assignments gives
\(\tau(F)\le\beta(F)\). \(\square\)

### Corollary 8.1 (sign and algorithms at width two)

\[
\beta(F)\ge0,
\qquad
\beta(F)=0\iff F\text{ is satisfiable}.
\]

Thus the sign test is ordinary 2-SAT. The threshold problem
\(\beta(F)\le q\) is the clause-deletion form of Almost 2-SAT and is
fixed-parameter tractable in (q); the original Razgon--O'Sullivan algorithm
runs in (O(15^q q m^3)).

### Corollary 8.2 (NP-completeness for arbitrary thresholds)

For a simple graph (H=(V,E)), use a variable (x_v) for each vertex and the
two clauses

\[
(x_u\vee x_v),
\qquad
(\neg x_u\vee\neg x_v)
\]

for every edge (uv). A cut edge falsifies neither clause and an uncut edge
falsifies exactly one. Therefore

\[
\boxed{\beta(F_H)=|E|-\operatorname{MaxCut}(H)}.
\]

Simple MaxCut is NP-complete, so deciding \(\beta(F)\le q\) is NP-complete
even for proper duplicate-free exact 2-CNF. Membership in NP follows because a
partial assignment is a polynomially checkable bilateral witness.

## 7. Fixed-threshold hardness from width three onward

Consider

\[
\begin{aligned}
N={}&(x_4\vee x_5\vee\neg x_6)
\wedge(\neg x_1\vee x_3\vee\neg x_6)
\wedge(\neg x_2\vee x_3\vee x_4)\\
&\wedge(\neg x_1\vee\neg x_4\vee\neg x_5)
\wedge(x_2\vee\neg x_5\vee x_6)
\wedge(x_1\vee\neg x_2\vee\neg x_3)\\
&\wedge(x_2\vee\neg x_3\vee\neg x_4)
\wedge(x_1\vee x_5\vee x_6).
\end{aligned}
\]

It is proper, simple, exact 3-CNF and each signed literal occurs twice.

### Lemma 9

\[
\boxed{\beta(N)=-1.}
\]

#### Proof

Set (x_1=1,x_5=x_6=0), leaving (x_2,x_3,x_4) unassigned. The two
surviving clauses are

\[
(\neg x_2\vee x_3\vee x_4),
\qquad
(x_2\vee\neg x_3\vee\neg x_4),
\]

so the assignment is bilateral with deficiency (2-3=-1).

For any bilateral residual with (u) variables and (t) clauses,
bilaterality and width three give (2u\le3t). If (t-u\le-2), then
\(t\le u-2\), so (2u\le3u-6) and (u\ge6). As (N) has only six
variables, (u=6), meaning the assignment is empty and all eight clauses
survive. This contradicts (t\le4). Hence no deficiency below (-1) exists.
\(\square\)

### Theorem 10 (width dichotomy for the sign)

For every fixed (r\ge3), deciding

\[
\beta(F)\le0
\]

is NP-complete on proper simple exact (r)-CNF. Consequently
\(\beta(F)>0\) is coNP-complete on the same class.

#### Proof

Given a Simple MaxCut instance ((H,K)), assume (0\le K\le|E(H)|=m).
The exact 2-CNF above has \(\beta=m-\operatorname{MaxCut}(H)\). Apply one
width lift, preserving \(\beta\) and obtaining proper simple exact 3-CNF. Add
\(m-K\) variable-disjoint copies of (N). By additivity,

\[
\beta(F')=m-\operatorname{MaxCut}(H)-(m-K)
=K-\operatorname{MaxCut}(H).
\]

Thus \(\beta(F')\le0\) exactly when (H) has a cut of size at least (K).
Membership in NP is witnessed by a bilateral assignment. Further fixed width
lifts prove every (r>3). \(\square\)

The general problem parameterised only by (q) is therefore para-NP-hard: its
slice at (q=0) is already NP-hard for exact 3-CNF.

The sign problem for the narrower proper exact ((3,2,2)) class remains open.
Ordinary satisfiability hardness for that class does not settle it because the
sign of \(\beta\) is not determined by satisfiability.

## 8. Bounded-treewidth tractability

Let (I(F)) be the unsigned variable-clause incidence graph. Replacing every
variable in every bag of a width-(t) tree decomposition by its two literal
vertices gives a decomposition of (G(F)) of width at most (2t+1). It covers
the complementary-pair and incidence edges and preserves the running
intersection property.

Independent dominating sets are \((\sigma,\rho)\)-sets with
\(\sigma=\{0\}\) and \(\rho=\{1,2,\ldots\}\). Algorithms for finite or
cofinite \((\sigma,\rho)\)-sets on bounded-treewidth graphs therefore compute
the optimum and count solutions by size in (2^{O(t)}|F|^{O(1)}) time when a
decomposition is supplied. Through Theorem 2 this computes \(\beta(F)\) and
the whole (B_F(z)).

## 9. Complete coordinatisation of regular-DIM graphs

Let (G) be a simple (d)-regular graph, (d\ge2), with a specified dominating induced
matching (M), and let (|M|=k). Orient every edge of (M), using its endpoints
as the positive and negative literal vertices of one variable. Every vertex
outside (V(M)) becomes an indexed clause containing its neighbouring literal
vertices.

Because (M) is induced, endpoints of different matching edges have no edges
between them. Because (M) edge-dominates (G), vertices outside (V(M)) are
independent. Each such vertex has (d) distinct literal neighbours. A clause
may contain both signs of one variable. Each signed literal has one matching
edge and (d-1) remaining incidences, so it occurs exactly (d-1) times.

Conversely, any indexed formula in which every clause contains (d) distinct
literal vertices and every signed literal occurs exactly (d-1) times produces
a (d)-regular formula graph whose complementary-pair edges form a dominating
induced matching. The constructions are inverse up to labels and orientations.

The counts are

\[
m=\frac{2k(d-1)}d,
\qquad
|V(G)|=\frac{2k(2d-1)}d,
\qquad
|E(G)|=k(2d-1).
\]

The pair matching is maximal, so \(\mu^*(G)\le k\). Every maximal matching is
edge-dominating, while one matching edge in a (d)-regular graph dominates at
most (2d-1) graph edges. As (G) has (k(2d-1)) edges, every maximal
matching has at least (k) edges. Thus \(\mu^*(G)=k\). Theorem 2 gives:

### Theorem 11 (regular-DIM gap classification)

\[
\boxed{i(G)-\mu^*(G)=\beta(F_M).}
\]

Therefore

\[
\begin{array}{c|c}
\beta(F_M)>0&i(G)>\mu^*(G)\\
\beta(F_M)=0&i(G)=\mu^*(G)\\
\beta(F_M)<0&i(G)<\mu^*(G).
\end{array}
\]

This classifies the entire (d)-regular family equipped with a dominating
induced matching, not just the original graph. For (d=3), proper formulas are
the non-tautological exact ((3,2,2)) subclass.

The verified positive component (P) has \(\beta(P)=1\), and Lemma 9 gives a
proper exact ((3,2,2)) component with value (-1). Their variable-disjoint
unions prove

\[
\boxed{
\{\beta(F):F\text{ proper simple exact }(3,2,2)\text{-CNF}\}=\mathbb Z.
}
\]

The corresponding additive cubic regular-DIM graphs are generally
disconnected. Later work in the manuscript settles connected positive
amplification: Theorem 12 identifies an explicit connected family with an
edge-cover problem, and a separate occurrence-switch formula has a native-
and Lean-checked value-one certificate. Connected constructions for every
signed integer remain open.

## 10. Evaluation of the six proposed uses

### 10.1 Systematic counterexample discovery — **yes, with a complexity qualification**

For every proper exact ((3,2,2)) formula (F), the graph (G(F)) is cubic,
its complementary pairs form a dominating induced matching,
\(\mu^*(G(F))=k\), and

\[
G(F)\text{ violates }i\le\mu^*
\iff\beta(F)>0.
\]

This gives a complete discovery pipeline:

1. generate formulas in the exact signed-occurrence space, using symmetry
   breaking if desired;
2. optimise \(\beta\), not merely SAT;
3. retain positive instances;
4. translate them canonically to cubic graphs;
5. emit an assignment witness for the upper bound and a logged lower-bound
   proof.

The supplied `analyze_formula.py` performs steps 2--4 on an input. It
re-identifies the canonical 15-variable formula as
\(\beta=1\), \(\mu^*=15\), (i=16). “Systematic” means necessary and
sufficient within the class; it does not mean polynomial-time, and the exact
((3,2,2)) sign complexity is not yet classified.

### 10.2 Compact, machine-checkable proofs — **yes for important families; qualified in general**

- A claim \(\beta(F)\le q\) has a compact witness: one bilateral partial
  assignment of deficiency at most (q).
- A lower bound \(\beta(F)\ge q\) is a coNP-type obligation. In general it
  needs an exhaustive, branch-and-bound, SAT/MILP proof-logging, or graph-IDS
  certificate; uniformly short certificates are not expected without a major
  complexity collapse.
- The canonical graph already has a 21,803-byte compressed independent-
  domination proof tree. The clean-room `bd_exact.cpp` independently reproduces
  the formula-side result and a stratified exhaustive receipt.
- Additive instances admit compositional certificates: solve each distinct
  component once, verify the variable-disjoint block structure, and add the
  values. `verify_benchmark.py` implements this proof rule.

Thus the parameter supports compact proofs, but proof size depends on formula
structure and the chosen proof system.

### 10.3 Algorithm selection — **yes at theorem level**

The proved decision map is:

| Recognised structure | Recommended exact route | Guarantee |
|---|---|---|
| width at most two | MaxSAT / Almost 2-SAT | \(\beta=\tau\); sign in P; FPT in threshold |
| small variable count | ternary enumeration | (O(3^k\,\|F\|)), complete |
| bounded incidence treewidth | tree-decomposition DP through (G(F)) | (2^{O(t)}|F|^{O(1)}) |
| regular-DIM signature | formula optimisation or graph IDS | exact gap (i-\mu^*=\beta) |
| unrestricted width at least three | proof-logging branch-and-bound / IDS / MILP | NP-hard already at threshold zero |

`analyze_formula.py` implements this structural routing. It does not claim to
predict the fastest solver among several implementations with the same
worst-case guarantee.

### 10.4 Controlled benchmark generation — **yes, constructively**

Three independent controls are available:

1. width lift changes exact clause width while preserving \(\beta\);
2. indexed replication preserves the feasible domain and encodes MaxSAT;
3. disjoint union adds values and convolves complete spectra.

The prototype generated and verified exact ((3,2,2)) instances with values
(3,-2,0), corresponding to cubic regular-DIM graphs with precisely those
values of (i-\mu^*). Every integer target is generated from the verified
(+1) and (-1) components. Manifests bind the CNF and graph encodings by
hash and record the additive proof rule.

### 10.5 Classification of an entire structured graph family — **yes**

Theorem 11 is a coordinatisation and classification theorem for every finite
simple (d)-regular graph supplied with a dominating induced matching. It
identifies the exact formula class, proves \(\mu^*=k\), and makes \(\beta\) the
complete signed gap invariant. The classification does not assert that
\(\beta\) alone determines graph isomorphism or every other graph invariant.

### 10.6 Infrastructure for AI-assisted mathematics — **technically demonstrated, adoption unproved**

The parameter supports a useful claim-evidence interface:

\[
\text{indexed CNF}
\rightarrow
\text{canonical residual objective}
\rightarrow
\text{exact solver}
\rightarrow
\text{certificate or receipt}
\rightarrow
\text{independent checker}
\rightarrow
\text{graph theorem instantiation}.
\]

The prototype provides:

- canonical indexed semantics, including duplicates and tautologies;
- two independently written exact implementations (Python reference and C++
  exhaustive solver);
- graph-side versus formula-side exhaustive bijection tests;
- deterministic JSON receipts and compositional manifests;
- theorem-driven solver routing;
- normal and `python -O` test runs;
- an example where cross-checking exposed and corrected a residual-polarity
  implementation bug before acceptance.

This is meaningful infrastructure for AI-assisted conjecture generation,
counterexample search, proof packaging, and claim calibration. It does not make
model output a proof, eliminate the need for independent review, secure
priority, or demonstrate community adoption.

## 11. Reproducible evidence

The clean-room package does not import the release verifier. Its current checks
include:

- exhaustive graph/formula bijection and size-spectrum equality over more than
  one hundred small indexed formulas, including empty, unit, binary,
  tautological, and absent-variable cases;
- exhaustive width-two equality with MaxSAT defect on a generated corpus;
- width-lift, additivity, spectrum convolution, replication, DIMACS indexing,
  and regular-DIM signature tests;
- all Python tests under ordinary execution and `python -O`;
- dependency-free C++ enumeration of the canonical formula:
  (3^{15}=14{,}348{,}907) partial assignments,
  (939{,}975) bilateral assignments, and \(\beta=1\);
- independent exact verification of (N) with \(\beta=-1\);
- generated and compositionally verified benchmark values (3,-2,0,-4).

Passing computations verify the stated finite objects and exercise theorem
implementations. They are not conventional peer review or formal proofs of the
general theorems; those burdens are carried by the written arguments.

## 12. Open boundaries

1. Determine the complexity of \(\beta(F)\le0\) for proper simple exact
   ((3,2,2))-CNF.
2. Find a connected regular-DIM composition with controlled additive or
   superadditive \(\beta\), particularly an unbounded positive gap.
3. Develop a parameter-native lower-bound proof format, ideally compilable to
   a standard SAT proof such as DRAT/LRAT or to a small formally verified
   checker.
4. Formalise the bijection, residual-core theorem, width-two theorem, and
   regular-DIM coordinatisation in a proof assistant.
5. Perform a specialist priority audit in MathSciNet, zbMATH, theses, and
   hypergraph/transversal terminology, explicitly including the 2008
   Chlebík--Chlebíková bridge.
6. Benchmark solver families empirically; theorem-level applicability does not
   determine practical dominance.

## 13. Conclusion

Bilateral deficiency has an independent mathematical life. It is the minimum
deficiency of a bipolar residual, the exact formula-side coordinate of
independent domination on formula graphs, an additive and width-stable
optimisation parameter, a strict extension of width-two MaxSAT defect, a
carrier of the full MaxSAT optimum after replication, and the exact gap
invariant for regular graphs with a dominating induced matching. Its values
span all integers even in the central exact ((3,2,2)) class.

The strongest novelty claim is not that the underlying partial-assignment cost
was wholly unseen: Chlebík and Chlebíková already used that decomposition in
2008. The advance supported here is the explicit feasible domain, bijective
optimum identity, residual interpretation, algebra, sharp width behaviour,
complexity theory, complete regular-DIM coordinatisation, and reproducible
infrastructure built around the parameter.

That is sufficient to establish bilateral deficiency as a distinct SAT-style
optimisation parameter rather than notation introduced solely for one graph.

## References

Ahadi, A., & Dehghan, A. (2019). “\((2/2/3)\)-SAT problem and its applications
in dominating set problems.” *Discrete Mathematics & Theoretical Computer
Science*, 21(4). <https://doi.org/10.23638/DMTCS-21-4-9>

Chlebík, M., & Chlebíková, J. (2008). “Approximation hardness of dominating
set problems in bounded degree graphs.” *Information and Computation*,
206(11), 1264–1275. <https://doi.org/10.1016/j.ic.2008.07.003>

Focke, J., Marx, D., Mc Inerney, F., Neuen, D., Sankar, G. S., Schepper, P., &
Wellnitz, P. (2025). “Tight complexity bounds for counting generalized
dominating sets in bounded-treewidth graphs—Part I: Algorithmic results.”
*ACM Transactions on Algorithms*, 21(3), Article 27.
<https://doi.org/10.1145/3731452>

Garey, M. R., Johnson, D. S., & Stockmeyer, L. (1976). “Some simplified
NP-complete graph problems.” *Theoretical Computer Science*, 1(3), 237–267.
<https://doi.org/10.1016/0304-3975(76)90059-1>

Jahari, S., & Alikhani, S. (2018). “On the independent domination polynomial
of a graph.” arXiv:1808.07369. <https://arxiv.org/abs/1808.07369>

Kullmann, O. (2011). “Constraint satisfaction problems in clausal form I:
Autarkies and deficiency.” *Fundamenta Informaticae*, 109(1), 27–81.
<https://doi.org/10.3233/FI-2011-428>

Razgon, I., & O'Sullivan, B. (2009). “Almost 2-SAT is fixed-parameter
tractable.” *Journal of Computer and System Sciences*, 75(8), 435–450.
<https://doi.org/10.1016/j.jcss.2009.04.002>

Szeider, S. (2004). “Minimal unsatisfiable formulas with bounded
clause-variable difference are fixed-parameter tractable.” *Journal of Computer
and System Sciences*, 69(4), 656–674.
<https://doi.org/10.1016/j.jcss.2004.04.009>

Zhang, T., Peitl, T., & Szeider, S. (2024). “Small unsatisfiable \(k\)-CNFs with
bounded literal occurrence.” *LIPIcs SAT 2024*, Article 31.
<https://doi.org/10.4230/LIPIcs.SAT.2024.31>

Zverovich, I. E. (2006). “Satgraphs and independent domination. Part 1.”
*Theoretical Computer Science*, 352(1–3), 47–56.
<https://doi.org/10.1016/j.tcs.2005.08.038>
