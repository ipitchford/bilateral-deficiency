# Bilateral Deficiency: Residual SAT Optimisation and Independent Domination in Regular-DIM Graphs

**Anonymous**  
**Independent research release**  
**Version 1.0.1-candidate | 9 August 2026**<br>
**DOI: 10.5281/zenodo.21857209**  
**Unrefereed candidate; no journal submission or external specialist review has been undertaken**

## Abstract

Let \(F\) be an indexed CNF on \(k\) variables. Call a partial assignment
\(\alpha\) bilateral when every unassigned variable occurs in both polarities
among the clauses not already satisfied by an assigned literal, and define

\[
\beta(F)=\min_{\alpha\ \mathrm{bilateral}}
\bigl(|T_F(\alpha)|-|U(\alpha)|\bigr).
\]

We prove that \(\beta\) is the minimum ordinary deficiency of a bipolar
residual restriction. A size-preserving bijection with independent dominating
sets of the clause-literal formula graph \(G(F)\) gives
\(i(G(F))=k+\beta(F)\) and a generating-polynomial identity. The parameter is
additive, invariant under width lifting, equal to the MaxSAT defect at width at
most two, and sufficient to recover MaxSAT after clause replication. With
unrestricted occurrences, its sign is polynomial-time decidable at width two
and NP-complete for every fixed uniform width \(r\ge3\); the proper, simple,
exact signed-occurrence \((3,2,2)\) slice remains open.

Every regular graph equipped with a dominating induced matching is
coordinatised by a formula satisfying \(i(G)-\mu^*(G)=\beta(F)\). Conditional
expectation gives the constructive bound
\[
i(G)\le \mu^*(G)+
\left\lfloor\frac{2(d-1)}{d\,2^d}\mu^*(G)\right\rfloor
\]
in the \(d\)-regular DIM class. A published enforcer yields a connected
amplifier with \(\beta(A(R))=\rho(R)\), connected linear-gap families, and
asymptotic gap density \(1/72\). An imported 20-clause lower bound proves that
order 50 is minimum among cubic graphs admitting a dominating induced matching
and satisfying \(i(G)>\mu^*(G)\). Three finite encodings have native- and
Lean-checked LRAT proofs. Those checks do not formalise the universal theory;
the release is unrefereed and has no independent reproduction or specialist
review.

**Keywords:** CNF deficiency, partial assignment, independent domination,
dominating induced matching, MaxSAT, parameterized complexity, formula graph

## 摘要

設 \(F\) 為含 \(k\) 個變數的具索引 CNF。若每個未指派變數在剩餘子句中
均保留正、負兩種極性，則該部分指派稱為雙側，並定義雙側虧缺
\(\beta(F)=\min(|T_F(\alpha)|-|U(\alpha)|)\)。本文證明它是雙極剩餘限制
的最小普通虧缺；雙側指派與子句-文字圖的獨立支配集存在保持大小的雙射，
故 \(i(G(F))=k+\beta(F)\)，生成多項式亦相應。參數可加、在寬度提升下
不變；寬度至多二時等於 MaxSAT 缺陷。若不限制文字出現次數，其符號判定
在寬度二屬 P，而在每個固定均勻子句寬度 \(r\ge3\) 為 NP 完全；精確符號
出現次數 \((3,2,2)\) 的情形仍未分類。對附有支配誘導匹配的正則圖，
\(i(G)-\mu^*(G)=\beta(F)\)，並有可建構上界。發表的強制元件給出值等於
骨架最小邊覆蓋的連通放大器；O--West 極值骨架使漸近差距密度達 \(1/72\)。
外部二十子句下界證明：在承認支配誘導匹配的三次圖中，違反不等式的最小
階數為 50。三組 SAT/LRAT 有限命題由原生檢查器與 Lean 檢查；理論仍是
未經同儕審查的書面證明，尚無獨立重現或完整形式化。

**關鍵詞：** CNF 虧缺；部分指派；獨立支配；支配誘導匹配；MaxSAT；
參數化複雜度

## 1. Introduction

A graph-theoretic construction can expose a useful expression without
establishing a new formula parameter. This distinction matters in the setting
that motivated the present work. A verified release resolving the third
TxGraffiti conjecture used a 15-variable exact signed-occurrence
\((3,2,2)\)-CNF to construct a
cubic graph with a dominating induced matching and with independent domination
number one larger than its minimum maximal-matching number [1]. The formula
side of the construction naturally produced a residual objective: the number
of clauses left unsatisfied by the assigned literals, minus the number of
variables deliberately left unassigned. The immediate question was whether
this expression merely recorded the accounting of that finite graph, or
whether it supported a formula-side theory independent of the example.

The standard for a positive answer should be demanding. A distinct
optimisation parameter ought to have a specified domain on general indexed
formulas, an intrinsic interpretation, exact translations to neighbouring
problems, separation from established quantities, nontrivial algebra, a
computational theory, and uses that survive beyond the motivating instance.
It should also be described within a defensible priority boundary. The last
condition is particularly important here because the closest prior reduction,
due to Chlebík and Chlebíková, already expresses the size of an independent
dominating set as a literal-selection cost plus a penalty for bad clauses [2].
The new theory therefore cannot be presented as the first appearance of the
underlying arithmetic.

This paper develops the resulting parameter, called **bilateral deficiency**.
The adjective records its feasible-domain condition: every unassigned variable
must retain both literal polarities in the residual. The principal structural
result is a size-preserving bijection between bilateral assignments of an
indexed CNF \(F\) and independent dominating sets of a canonical formula graph
\(G(F)\). The objective then becomes an exact coordinate:

\[
i(G(F))=|V(F)|+\beta(F).
\]

The bijection preserves not only the optimum but every solution size and its
multiplicity. On the formula side, \(\beta\) is precisely the least
clause-variable deficiency among residual restrictions that remain bipolar.
These two characterisations give the parameter both a SAT semantics and a
graph semantics.

Four further groups of results establish that the definition has mathematical
life beyond this identity. First, explicit examples separate it from ordinary
deficiency, maximum deficiency, satisfiability, and MaxSAT defect. Second, it
is additive on variable-disjoint unions, its complete solution polynomial is
multiplicative, and a local width-lifting operation preserves its value.
Third, its complexity has a sharp width boundary: at width at most two it
equals the MaxSAT defect, while the sign problem is NP-complete on proper
simple \(r\)-uniform CNF for every fixed \(r\ge3\). Indexed clause replication
recovers MaxSAT exactly, and bounded incidence treewidth gives a
single-exponential parameterized algorithm. Fourth, regular graphs equipped
with a dominating induced matching admit a complete coordinatisation by a
signed-occurrence formula class. Within that class, \(\beta\) is exactly the
signed gap \(i-\mu^*\), and a constructive probabilistic argument bounds this
gap above by \(2(d-1)\mu^*/(d\,2^d)\). A parser-independent Lean-checked finite
terminal signature for the published \(E_{3,2,2}\) enforcer then supports a
connected composition theorem:
attaching one enforcer to every edge of a connected cubic skeleton \(R\)
makes \(\beta\) equal to the minimum edge-cover number of \(R\). Prisms give
an explicit infinite family with a linear positive gap.

These theorems support six concrete uses. They give a necessary-and-sufficient
search objective for counterexamples within formula-generated regular-DIM
graphs, concise upper witnesses and compositional lower proofs, structural
algorithm routing, prescribed-value benchmark generation, a full sign
classification of a structured graph family, and a typed claim-evidence
interface for AI-assisted mathematics. Each use has a qualification.
Systematic discovery is not polynomial-time discovery, lower-bound proofs need
not be short, theorem-level routing does not predict the fastest engineering
implementation, and technical infrastructure does not demonstrate community
adoption.

The paper proceeds by fixing the prior-art boundary before introducing the
definition. Section 3 proves the residual and graph characterisations. Section
4 establishes separation and algebra. Section 5 develops complexity and
algorithm selection. Section 6 coordinatises the regular-DIM family. Section 7
evaluates the six uses, and Section 8 records reproducibility limits and open
problems. All general statements are supported by written proofs. Computation
is used only to check finite objects and implementations, not as a substitute
for the universal arguments.

## 2. Prior art and claim boundary

### 2.1 Formula graphs and independent domination

Several SAT-to-graph constructions use a complementary pair of literal
vertices for each variable and clause vertices adjacent to their literals.
What changes between constructions is the clause-side adjacency and the
optimization objective. Zverovich's satgraph makes the clause vertices a
clique [3]. At most one of those vertices can then appear in an independent
set, and the independent domination optimum collapses to a satisfiability
indicator: \(k\) for a satisfiable \(k\)-variable formula and \(k+1\) for an
unsatisfiable one. That construction establishes a close architectural
antecedent, but it deliberately discards the number and structure of residual
clauses.

Clause-literal encodings also serve exact formula generation. Zhang, Peitl,
and Szeider used such representations to generate and classify small
unsatisfiable \(k\)-CNFs under literal-occurrence bounds [4]. Their work is
especially relevant to the exact signed-occurrence \((3,2,2)\) class used
later in this paper:
each clause has width three and each signed literal occurs twice. Ahadi and
Dehghan proved hardness results for the corresponding twice-positive,
twice-negative form of 3-SAT and applied that source problem to domination
questions [5]. These papers establish that exact signed-occurrence spaces are
neither artificial nor computationally trivial. They optimize satisfiability
or a target graph problem, however, not the residual difference defined here.

### 2.2 The closest antecedent: the replicated-clause cost

The strongest overlap occurs in Chlebík and Chlebíková's approximation
reduction for bounded-degree Minimum Independent Dominating Set [2]. The exact
pinpoint is Section 2.3, proof of Theorem 5, pp. 10--11 of the authors'
preprint. Their graph contains two adjacent literal vertices for each variable
and \(t\) indexed vertices for each clause. An independent dominating set
\(D\) has a literal part \(D_1\), which determines a partial assignment.
Clauses without a selected literal are called bad. If the formula has \(5k\)
clauses and a fraction \(b\) is bad, the paper puts all \(t\) copies of every
bad clause into \(D_2\) and records

\[
|D|=|D_1|+|D_2|=|D_1|+(5k)bt.
\]

Equivalently, with \(T\) the indexed set of bad clauses, the decomposition is
\(|D|=|D_1|+t|T|\).

Writing \(n\) for the number of formula variables and letting \(U\) denote
variables for which neither literal was selected, \(|D_1|=n-|U|\). The generic
replicated cost is therefore \(n+t|T|-|U|\). At \(t=1\), this is exactly the
objective used below, shifted by the constant \(n\). In the notation of [2],
\(n=3k\); the neutral letter prevents their scaling parameter from being
confused with the variable count used elsewhere in this paper.

This antecedent decides the novelty boundary. The decomposition itself is not
new. What is not developed in [2] is the exact formula-side feasible domain
forced by domination of both endpoints of every unselected literal pair; a
converse mapping for all feasible partial assignments; a residual
clause-variable parameter; an optimum identity and full solution polynomial;
or the algebraic, complexity, and regular-graph classification results proved
here. The relationship is therefore one of extraction and extension: an
implicit cost in an approximation reduction becomes an explicit residual
optimization object with its own theory.

### 2.3 Deficiency parameters in SAT

For a formula with \(m\) indexed clauses and \(n\) variables, ordinary
deficiency is \(m-n\). SAT theory also studies maximum deficiency over clause
subfamilies, matching autarkies, lean kernels, and surplus. Kullmann gives a
systematic clausal theory connecting autarkies and deficiency [6], while
Szeider analyzes bounded clause-variable difference in minimally
unsatisfiable formulas and parameterized satisfiability [7]. These quantities
are close enough that a new definition must be distinguished by its
optimization domain, not by a renamed arithmetic expression.

The relevant quantities differ as follows.

| Quantity | Objects optimized over | Objective | Feasibility condition |
|---|---|---|---|
| ordinary deficiency | the presented indexed formula | \(|F|-|V(F)|\) | none |
| maximum deficiency / surplus | clause subfamilies or their variable neighborhoods | maximum clause--variable excess, or its dual | subformula or neighborhood choice |
| autarky / lean-kernel methods | partial assignments and clauses they touch | remove or characterize autarkic structure | every touched clause is satisfied |
| MaxSAT defect \(\tau\) | complete assignments | falsified indexed clauses | every variable assigned |
| bilateral deficiency \(\beta\) | residual restrictions induced by partial assignments | \(|T|-|U|\) | every unassigned variable survives in both signs |
| replicated-clause cost of [2] | literal selections in one reduction graph | \(|D_1|+t|T|\) | graph independence and domination |

Bilateral deficiency minimizes, rather than maximizes, a clause-variable
difference. More importantly, it minimizes over partial-assignment residuals
subject to a two-polarity survival condition. It does not range over arbitrary
clause subfamilies, and a feasible bipolar residual need not be lean. Ordinary
deficiency evaluates one presented formula. Maximum deficiency scans
subformulas. Bilateral deficiency scans residual restrictions. The separation
examples in Section 4 prove that neither ordinary nor maximum deficiency
determines its value.

The polarity condition also prevents an identification with an unrestricted
residual minimum. Without it, leaving variables unassigned would earn a unit
reward even when those variables had disappeared from every surviving clause.
The optimum would then depend on the declared variable universe in an
unstructured way. Bilaterality makes each reward accountable: an unassigned
variable must still participate on both sides of the remaining constraint
system. This is analogous in spirit to matching conditions that organize
autarky theory, but its quantifiers and objective differ. An autarky satisfies
every clause it touches. A bilateral assignment constrains the variables it
does not assign. A lean kernel removes autarkic structure. A bilateral
residual is selected by minimizing its own deficiency and need not be lean.
Existing deficiency language is therefore essential context without making
the new optimum redundant.

### 2.4 Priority statement

The literature inspection supports the following calibrated statement.
Bilateral deficiency appears to be new as an explicitly defined SAT-style
residual optimization parameter together with the bijective, algebraic,
complexity, and regular-DIM theory proved here. The partial-assignment cost
decomposition is implicit in Chlebík and Chlebíková [2]. An earlier source for
the independent domination polynomial was also located and is credited below
[8]. The dated search log accompanying the artifact records exact-phrase and
concept searches over SAT deficiency, residual restrictions, autarkies,
formula graphs, independent domination, domination polynomials, and the 2008
reduction lineage.

This is not a claim of global priority. The inspection used public web and
publisher indexes and targeted citation chaining, but did not exhaust
MathSciNet, zbMATH, dissertations, non-English literature,
hypergraph-transversal terminology, or all non-digitized sources. The
mathematical results below do not depend on priority, and a subject specialist
would need to re-audit the historical description before any future journal
submission.

### 2.5 Imported theorem dependencies

Three external mathematical inputs are load-bearing. The table records the
exact imported object or result, the convention transfer used here, and the
consequence checked locally. This separates attribution and interface checks
from the original proofs in their cited sources.

| Imported source | Exact input used | Convention transfer | Locally checked consequence |
|---|---|---|---|
| Zhang--Peitl--Szeider [4, Appendix A.1] | The displayed ten-clause \(E_{3,2,2}\) enforcer with one terminal forced false in every satisfying assignment | Variables and clauses are transcribed into the present indexed-CNF convention; a global polarity switch fixes the terminal orientation; internal signed occurrences and the terminal's two negative occurrences are recounted | The hard-coded formula and its four-entry terminal signature are checked independently of the production DIMACS parser; the signature then enters Theorem 12 |
| Zhang--Peitl--Szeider [4, Theorem 15 and Table 1] | The smallest unsatisfiable \((3,2,2)\)-formula has 20 distinct clauses | Tautologies are deleted and duplicate indexed clauses collapsed; clause width is at most three and each signed literal occurs at most twice, matching the source's bounded-occurrence convention | Positive \(\beta\) implies unsatisfiability; the incidence identities \(3m=4k\) and \(|V(G)|=2k+m\) then give the order-50 lower bound in Corollary 13 |
| O--West [13, Corollaries 2.3 and 4.4; Theorem 5.2] | Every connected cubic graph of order \(r\) has matching number at least \((4r-1)/9\), with an infinite equality family \(\mathcal H_1\) | Their \(n\) is the present skeleton order \(r\), and their matching number \(\alpha'\) is the present \(\nu\) | Theorem 12 converts \(r-\nu(R)\) into the amplifier gap; the displayed family parameters are checked before deriving the construction-specific density \(1/72\) |

The local checks validate transcription, syntax, and the stated consequences.
They do not independently re-prove the imported theorems.

## 3. Bilateral residuals and the formula-graph bijection

### 3.1 Indexed residual semantics

An **indexed CNF** is a finite sequence \(F=(C_a)_{a\in A}\) of clauses on an
explicit finite variable set \(V(F)=\{x_1,\ldots,x_k\}\). A clause is a set of
literals: repeated positions within a clause collapse, while extensionally
equal clauses at different indices remain distinct. This distinction is
essential because clause replication is one of the algebraic operations.
Empty and tautological clauses are permitted unless a restricted formula
class excludes them. An explicit variable may occur in no clause.

A partial assignment is a map
\(\alpha:V(F)\to\{0,1,*\}\), where \(*\) denotes unassigned. Define

\[
U(\alpha)=\{x\in V(F):\alpha(x)=*\}
\]

and let \(T_F(\alpha)\subseteq A\) contain exactly those clause indices for
which no literal has been made true by \(\alpha\). The residual
\(F\!\upharpoonright\!\alpha\) is obtained by deleting satisfied indexed
clauses and deleting assigned false literals from every survivor. It retains
the original indices. A residual is **bipolar** if each variable occurring in
it occurs with both signs.

The assignment \(\alpha\) is **bilateral** if every variable in
\(U(\alpha)\) occurs positively and negatively among the clauses indexed by
\(T_F(\alpha)\). This requirement does two jobs. It ensures that each explicit
unassigned variable actually survives, and it makes the residual bipolar.
Complete assignments are bilateral vacuously. Thus the feasible set is always
nonempty, even when \(F\) contains empty clauses or unused variables.

Define the residual objective and its optimum by

\[
\delta_F(\alpha)=|T_F(\alpha)|-|U(\alpha)|,
\qquad
\beta(F)=\min_{\alpha\ \mathrm{bilateral}}\delta_F(\alpha).
\]

The use of indexed clauses means that \(|T_F(\alpha)|\) counts multiplicity.
The use of an explicit variable set means that assigning an otherwise absent
variable is sometimes necessary for feasibility. These conventions remove
two ambiguities that would otherwise make replication and graph translation
ill-defined.

### 3.2 Least deficiency of a bipolar residual

**Theorem 1 (residual-core characterization).** For every indexed CNF \(F\),

\[
\beta(F)=
\min_{\substack{\alpha:
F\upharpoonright\alpha\ \mathrm{bipolar}\\
V(F\upharpoonright\alpha)=U(\alpha)}}
\left(c(F\upharpoonright\alpha)-n(F\upharpoonright\alpha)\right).
\]

**Proof.** The surviving indexed clauses are exactly those in
\(T_F(\alpha)\), so their number is \(|T_F(\alpha)|\). The assignment is
bilateral precisely when every unassigned variable occurs in both polarities
in the residual. Under that condition the residual is bipolar and its
variable set is exactly \(U(\alpha)\). Its ordinary deficiency is therefore
\(|T_F(\alpha)|-|U(\alpha)|\). Conversely, every residual appearing in the
displayed domain satisfies the bilateral condition. The two minima range over
the same assignments with the same objective. \(\square\)

The theorem provides the requested intrinsic SAT interpretation. The
parameter is not defined by reference to a graph, although the graph
translation will make it computationally and structurally useful. It selects
the least deficient bipolar core obtainable by restriction, with explicit
control of variables that have disappeared.

### 3.3 A size-preserving bijection

Construct the **formula graph** \(G(F)\) as follows. For each variable \(x_j\),
create adjacent literal vertices \(v_j^+\) and \(v_j^-\). For every indexed
clause \(C_a\), create a clause vertex \(c_a\). Clause vertices are mutually
nonadjacent, and \(c_a\) is adjacent to the literal vertex for each literal in
\(C_a\). Tautological clauses are adjacent to both endpoints of the relevant
pair. Equal clauses at different indices give distinct twin clause vertices.

**Theorem 2 (bilateral assignment--independent domination bijection).** The
map

\[
\alpha\longmapsto D_\alpha=
\{\text{the true literal vertex selected for every assigned variable}\}
\cup\{c_a:a\in T_F(\alpha)\}
\]

is a bijection from the bilateral assignments of \(F\) to the independent
dominating sets of \(G(F)\). Moreover,

\[
|D_\alpha|=k+\delta_F(\alpha),
\qquad
i(G(F))=k+\beta(F).
\]

**Proof.** Let \(\alpha\) be bilateral. At most one endpoint of each literal
pair is selected. A selected clause vertex has no selected literal neighbor,
because its clause has no assigned true literal. Clause vertices are mutually
nonadjacent, so \(D_\alpha\) is independent.

Every assigned literal pair is dominated by its selected endpoint. If a
clause is not in \(T_F(\alpha)\), an assigned true literal dominates it; if it
is in \(T_F(\alpha)\), its own clause vertex is selected. For an unassigned
variable, bilaterality supplies a selected residual clause adjacent to the
positive endpoint and a selected residual clause adjacent to the negative
endpoint. The two clauses may coincide when a tautology is present. Hence
\(D_\alpha\) dominates all vertices. Its size is

\[
(k-|U(\alpha)|)+|T_F(\alpha)|=k+\delta_F(\alpha).
\]

Conversely, let \(D\) be an independent dominating set. Independence allows
at most one endpoint from each literal pair. Assign the corresponding truth
value when one endpoint is selected and leave the variable unassigned when
neither is selected. A clause vertex belongs to \(D\) exactly when it has no
selected literal neighbor: independence proves that a selected clause has no
such neighbor, and domination forces every unselected clause to have one.
Thus the selected clause vertices are precisely \(T_F(\alpha_D)\). If neither
endpoint of a literal pair is selected, both endpoints must be dominated by
selected clause vertices. The residual consequently contains both polarities
of that variable, so \(\alpha_D\) is bilateral. Both constructions recover
their inputs, and the size equation already proved completes the result.
\(\square\)

The converse is the step that turns a one-way reduction cost into a genuine
parameter identity. It shows that no independent dominating set falls outside
the formula-side feasible domain and no bilateral assignment is lost.

Several boundary cases show why the indexed formulation is not cosmetic. An
empty clause has an isolated clause vertex and must be selected in every
independent dominating set; on the formula side it survives every assignment
and contributes one to \(|T|\). A tautological clause is always satisfied by a
complete assignment, but under an unassigned variable it can dominate both
literal endpoints from one selected clause vertex. The bilateral definition
therefore permits the same residual clause to witness both polarities.
Duplicate indexed clauses become distinct independent twins and are counted
separately on both sides. An explicit variable absent from every clause cannot
be left unassigned by a bilateral assignment, just as neither endpoint of its
isolated complementary edge can be dominated by a clause vertex. These cases
agree without auxiliary exceptions.

The bijection is compatible with witnesses as well as values. A formula-side
certificate records a ternary vector and its residual clause indices. Its
image is obtained without search. A graph-side independent dominating set
recovers the ternary vector by inspecting complementary pairs, and its
selected clause vertices must equal the recomputed residual indices. This
round trip gives a linear-time checker once the formula and candidate are
fixed. It does not certify optimality, but it makes every claimed upper bound
transparent.

### 3.4 Complete solution polynomial

Define a Laurent polynomial on the formula side by

\[
B_F(z)=\sum_{\alpha\ \mathrm{bilateral}}z^{\delta_F(\alpha)}.
\]

Let \(D_i(G,z)=\sum_D z^{|D|}\), where the sum ranges over all independent
dominating sets. This polynomial was introduced under the name independent
domination polynomial by Dod [8] and subsequently studied by Jahari and
Alikhani [9]. Theorem 2 immediately gives more than equality of optima.

**Corollary 3.** For every indexed CNF \(F\) on \(k\) variables,

\[
D_i(G(F),z)=z^kB_F(z).
\]

Every exponent and coefficient is preserved after the constant shift. Thus
the formula parameter carries the full independent-domination solution-size
spectrum on formula graphs, including multiplicities. This identity provides
a strong cross-model test: independently enumerating bilateral assignments
and graph independent dominating sets must yield the same polynomial, not
merely the same minimum.

### 3.5 Replicated clauses and the 2008 construction

For an integer \(t\ge1\), define

\[
\beta_t(F)=\min_{\alpha\ \mathrm{bilateral}}
\bigl(t|T_F(\alpha)|-|U(\alpha)|\bigr).
\]

Let \(F^{[t]}\) repeat every indexed clause \(t\) times. Replication preserves
the bilateral feasible domain and multiplies the surviving-clause count, so

\[
\beta_t(F)=\beta(F^{[t]}),
\qquad
i(G(F^{[t]}))=k+\beta_t(F).
\]

The graph used in [2] is therefore the replicated-clause member of this exact
framework. This observation credits the antecedent while clarifying what the
parameter adds: the domain, inverse map, residual semantics, and theory remain
visible for every replication weight.

## 4. Separation and algebra

### 4.1 Separation from standard SAT quantities

The arithmetic \(|T|-|U|\) resembles deficiency, but its optimum is not
determined by ordinary or maximum deficiency. Consider

\[
F_0=(x)\wedge(y)\wedge(x\vee y),
\qquad
F_1=(x)\wedge(y)\wedge(\neg x\vee\neg y).
\]

Both formulas have two variables and three clauses, so ordinary deficiency is
one. Every proper clause subfamily has deficiency at most one, so their maximum
deficiencies also agree. Formula \(F_0\) is satisfiable and, by the width-two
theorem below, has \(\beta(F_0)=0\). Formula \(F_1\) cannot satisfy all three
clauses but can satisfy two, hence \(\beta(F_1)=1\). Equal ordinary and maximum
deficiencies can therefore coexist with different bilateral deficiencies.

The comparison is stronger than a sign example. Both formulas have the same
numbers of variables and indexed clauses, the same clause-width profile
\((1,1,2)\), and the same maximum deficiency. Their different values arise
from polarity geometry under restriction. In \(F_0\), a satisfying completion
reaches zero. In \(F_1\), every completion leaves one clause false, and the
width-two theorem shows that no strategically unassigned variable can improve
the objective. Bilateral deficiency consequently distinguishes formulas that
all of these coarser statistics identify.

Nor is \(\beta\) a relabelled satisfiability or MaxSAT answer. Let

\[
H=(x\vee y\vee z)\wedge(\neg x\vee\neg y\vee\neg z).
\]

The empty assignment is bilateral and has deficiency \(2-3=-1\), while \(H\)
is satisfiable and has MaxSAT defect zero. The width-three occurrence bound
\(2|U|\le3|T|\) excludes any value below \(-1\), so
\(\beta(H)=-1\). Conversely, Proposition 14 proves that the explicit
15-variable exact signed-occurrence \((3,2,2)\) component \(P\) is
unsatisfiable and has value
\(+1\). Combining that
positive component with the negative component of Lemma 8 by disjoint union
gives unsatisfiable formulas of value zero and negative one. Satisfiability
therefore does not determine even the sign of \(\beta\).

### 4.2 Additivity and spectral convolution

**Theorem 4 (disjoint-union algebra).** If \(F_1\) and \(F_2\) have disjoint
variable sets, then

\[
\beta(F_1\sqcup F_2)=\beta(F_1)+\beta(F_2),
\qquad
B_{F_1\sqcup F_2}(z)=B_{F_1}(z)B_{F_2}(z).
\]

**Proof.** Every partial assignment on the union factors uniquely into a pair
of partial assignments. It is bilateral exactly when both restrictions are
bilateral, because no literal or clause crosses the variable partition.
Surviving clause counts and unassigned variable counts add. Hence objectives
add for every feasible pair. Taking minima proves the first identity, while
summing the monomials over all feasible pairs proves the polynomial product.
\(\square\)

This algebra is nontrivial in two senses. It controls optimum values and full
solution distributions, and it supports compositional certificates. Once the
value of each distinct component has been proved, arbitrarily large block
instances can be checked by verifying the partition and adding component
values. The operation also shows that negative values are not pathological
one-off events: any positive and negative base components generate a two-sided
integer semigroup.

The polynomial identity retains information discarded by the minimum. If
\(b_j(F)\) is the number of bilateral assignments of deficiency \(j\), then
the coefficient rule

\[
b_j(F_1\sqcup F_2)=\sum_{p+q=j}b_p(F_1)b_q(F_2)
\]

is an exact convolution. It permits distribution-sensitive tests in which two
formulas have equal \(\beta\) but different near-optimal spectra. On the graph
side, the same coefficients count independent dominating sets at each size
after the variable shift. Additivity is therefore not merely a device for
manufacturing optimum values. It transports a complete counting invariant
through disjoint composition.

### 4.3 Exact width lift

For every clause \(C_a\), introduce a fresh variable \(y_a\) and replace the
clause by

\[
C_a\vee y_a,
\qquad C_a\vee\neg y_a.
\]

Write \(L(F)\) for the lifted formula.

**Theorem 5 (width-lift invariance).** For every indexed CNF \(F\),

\[
\beta(L(F))=\beta(F).
\]

If \(F\) is a proper, duplicate-free \(r\)-uniform CNF, then \(L(F)\) is a
proper, duplicate-free \((r+1)\)-uniform CNF.

**Proof.** Restrict a partial assignment on \(L(F)\) to the original variables.
If \(C_a\) is satisfied by that restriction, both lifted clauses disappear.
Bilaterality then forces \(y_a\) to be assigned, since an unassigned \(y_a\)
would have neither polarity in the residual. The original clause and its
lifted pair both contribute zero to the objective.

Suppose \(C_a\) survives. If \(y_a\) is assigned, exactly one lifted clause
survives; if \(y_a\) is unassigned, both survive and the new variable adds one
to \(|U|\). In either case the net contribution is one, exactly the
contribution of the original surviving clause. The surviving lifted clauses
contain the same unassigned original literals, so bilaterality of every
original variable is preserved in both directions. Local choices for distinct
\(y_a\) are independent. The feasible objectives therefore correspond
exactly, proving equality of minima. Fresh variables distinguish the two
children of every clause and preserve properness and uniform clause width.
\(\square\)

Repeated lifting moves a construction from width two to every larger uniform
clause width without changing \(\beta\). This makes the operation useful both in
hardness reductions and in algebraic conformance benchmark design.

### 4.4 Recovering MaxSAT by clause replication

Let \(\tau(F)\) denote the minimum number of clauses falsified by a complete
assignment. Every completion of a partial assignment can falsify only clauses
that survived the partial assignment, so \(|T_F(\alpha)|\ge\tau(F)\).

**Theorem 6 (MaxSAT recovery).** If \(F\) has \(k\) variables and \(r>k\), then

\[
\tau(F)=\left\lceil\frac{\beta(F^{[r]})}{r}\right\rceil.
\]

More precisely,

\[
\beta(F^{[r]})=r\tau(F)-u^*,
\]

where \(u^*\) is the maximum number of variables left unassigned by a
bilateral assignment with exactly \(\tau(F)\) original residual clauses.

**Proof.** Replication changes the objective to \(r|T|-|U|\). Since
\(|T|\ge\tau(F)\) and \(|U|\le k\), every feasible assignment has value at
least \(r\tau(F)-k\). A complete MaxSAT-optimal assignment is bilateral and
has value \(r\tau(F)\). Thus

\[
r\tau(F)-k\le\beta(F^{[r]})\le r\tau(F).
\]

Because \(r>k\), dividing by \(r\) and taking the ceiling yields
\(\tau(F)\). A minimizer cannot have \(|T|\ge\tau(F)+1\), since then its value
is at least \(r(\tau(F)+1)-k>r\tau(F)\). It must therefore have exactly
\(\tau(F)\) residual clauses and maximize \(|U|\), proving the refined formula.
\(\square\)

The result places \(\beta\) in a precise relation to MaxSAT. At unit weight it
can differ sharply from the MaxSAT defect. Under a sufficiently large indexed
penalty it contains both the defect and a secondary optimum measuring how
many variables can remain bilateral at MaxSAT optimality.

## 5. Complexity and algorithm selection

### 5.1 Baseline decision problem

Define **BILATERAL-DEFICIENCY** as the decision problem asking whether
\(\beta(F)\le q\). It belongs to NP: a ternary assignment is a polynomial-size
certificate, and one can scan the indexed clauses to check the residual
count, the unassigned count, and both-polarity occurrence for every unassigned
variable. Direct exact enumeration takes \(O(3^k\|F\|)\) time and polynomial
space. This baseline is useful for small \(k\), but the next results show that
syntax should guide a solver whenever additional structure is present.

The input conventions affect this membership statement only in predictable
ways. Clause indices and the explicit variable count are part of the instance,
so duplicates and unused variables require no reconstruction. For each
surviving clause, a verifier records the signs of its unassigned literals only
after confirming that no assigned literal satisfies the clause. It then tests
two sign bits per unassigned variable. The certificate checker is linear in
the total literal-incidence size, apart from integer arithmetic for the
threshold. This ordering matters in implementations: recording a polarity
from a clause that is later discovered to be satisfied creates a false
bilateral witness.

The definition also has a direct 0--1 optimization model. All variables in the
following formulation are explicitly binary. For each formula variable
\(x_j\), introduce \(a_j^0,a_j^1,u_j\in\{0,1\}\) with
\(a_j^0+a_j^1+u_j=1\). For each indexed clause \(a\), let \(r_a\) indicate
that no assigned true literal occurs in that clause, with
\(r_a\in\{0,1\}\). If \(s_{\ell}\) denotes
\(a_j^1\) for a positive literal \(x_j\) and \(a_j^0\) for a negative literal
\(\neg x_j\), impose

\[
r_a\le 1-s_{\ell}\quad(\ell\in C_a),
\qquad
r_a\ge 1-\sum_{\ell\in C_a}s_{\ell}.
\]

These constraints make \(r_a\) exactly the residual-clause indicator,
including for empty and tautological clauses. Bilaterality is expressed by

\[
u_j\le\sum_{a:x_j\in C_a}r_a,
\qquad
u_j\le\sum_{a:\neg x_j\in C_a}r_a.
\]

Minimizing \(\sum_a r_a-\sum_j u_j\) is therefore an exact binary linear
formulation of \(\beta(F)\). It offers a general MILP route and, more
importantly, a second executable specification against which specialized
solvers can be checked. A solver optimum still requires a verifiable lower
bound or trusted optimization proof. The formulation alone does not turn an
optimizer's status line into a certificate.

### 5.2 Width at most two

**Theorem 7 (width-two equality).** If every clause of \(F\) has width at most
two, then

\[
\beta(F)=\tau(F).
\]

The statement includes indexed duplicate clauses, units, empty clauses, and
tautological binary clauses.

**Proof.** A complete MaxSAT-optimal assignment is bilateral, so
\(\beta(F)\le\tau(F)\). For the reverse inequality, take any bilateral
assignment whose residual has \(u\) variables and \(t\) indexed clauses. Form
the **signed literal-occurrence bipartite multigraph** of the residual. Its
left vertices are residual variables, its right vertices are indexed residual
clauses, and each signed literal occurrence is a separate edge. Thus a
tautological binary clause containing \(x\) and \(\neg x\) gives two parallel
edges from variable \(x\) to one clause vertex. For a set \(X\) of residual
variables, let \(N(X)\) be the underlying set of adjacent clause vertices.
Bilaterality supplies at least two signed occurrences per variable in \(X\).
All such incidences end in \(N(X)\), and each residual clause has at most two
signed literal occurrences. Consequently

\[
2|X|\le e(X,N(X))\le2|N(X)|.
\]

Hall's condition holds, so every residual variable can be matched to a
distinct containing clause. Assign each variable to satisfy its literal in
the matched clause. The matched clauses are distinct, hence at least \(u\) of
the \(t\) residual clauses become satisfied. Completing any remaining choices
therefore falsifies at most \(t-u\) clauses. It follows that
\(\tau(F)\le t-u\) for every bilateral assignment. Minimization gives
\(\tau(F)\le\beta(F)\), completing the equality. \(\square\)

The proof explains why width two is the exact boundary for this argument.
Bilaterality supplies two incidences per residual variable. Width two gives at
most two incidences per residual clause, so Hall's inequality follows with
coefficient one. At width three, the same count yields only
\(2|X|\le3|N(X)|\), which cannot match all variables to distinct clauses.
Lemma 8 exploits precisely this slack. The complexity dichotomy below is thus
visible in the combinatorial proof rather than appearing as an unrelated
reduction artifact.

Empty clauses do not disturb the matching argument because they consume no
variable incidence and may remain among the \(t-u\) falsified clauses. A unit
clause contributes capacity one rather than two, which only strengthens the
upper incidence bound. A tautological binary clause contains both literals of
one variable but remains a single distinct clause vertex, and the argument
still uses only its two incidences.

The equality has two different algorithmic consequences. First,
\(\beta(F)=0\) exactly when a width-two formula is satisfiable, so the sign is
decided by 2-SAT in polynomial time. Second, arbitrary thresholds encode the
clause-deletion or Almost-2-SAT objective. The latter is fixed-parameter
tractable in the permitted number \(q\) of falsified clauses. Razgon and
O'Sullivan gave an \(O(15^q q m^3)\) algorithm [10]. Thus a restricted slice
can have an easy sign test and an NP-hard variable threshold without
contradiction.

### 5.3 NP-complete thresholds already at uniform width two

The threshold hardness has a direct graph reduction. Given a simple graph
\(H=(V,E)\), create a variable \(x_v\) for every vertex. For each edge \(uv\),
include the two clauses

\[
(x_u\vee x_v),
\qquad
(\neg x_u\vee\neg x_v).
\]

Under a complete assignment, a cut edge falsifies neither clause and an uncut
edge falsifies exactly one. Theorem 7 yields

\[
\beta(F_H)=\tau(F_H)=|E|-\operatorname{MaxCut}(H).
\]

Simple MaxCut is NP-complete [11]. Therefore BILATERAL-DEFICIENCY is
NP-complete even for proper duplicate-free 2-uniform CNF when \(q\) is part of
the input.

### 5.4 A negative exact signed-occurrence \((3,2,2)\) component

The fixed-threshold hardness proof needs a proper uniform-width component with
negative value. Let \(N\) be

\[
\begin{aligned}
 &(x_4\vee x_5\vee\neg x_6)
\wedge(\neg x_1\vee x_3\vee\neg x_6)
\wedge(\neg x_2\vee x_3\vee x_4)\\
{}\wedge{}&(\neg x_1\vee\neg x_4\vee\neg x_5)
\wedge(x_2\vee\neg x_5\vee x_6)
\wedge(x_1\vee\neg x_2\vee\neg x_3)\\
{}\wedge{}&(x_2\vee\neg x_3\vee\neg x_4)
\wedge(x_1\vee x_5\vee x_6).
\end{aligned}
\]

Every clause contains three different variables, no clauses repeat, and each
signed literal occurs exactly twice.

**Lemma 8.** \(\beta(N)=-1\).

**Proof.** Set \(x_1=1\) and \(x_5=x_6=0\), leaving
\(x_2,x_3,x_4\) unassigned. Exactly two clauses survive:

\[
(\neg x_2\vee x_3\vee x_4),
\qquad
(x_2\vee\neg x_3\vee\neg x_4).
\]

Each unassigned variable occurs with both signs, so the residual is bilateral
and has value \(2-3=-1\). For a lower bound, every width-three bilateral
residual with \(u\) variables and \(t\) clauses has at least \(2u\) literal
occurrences and at most \(3t\), hence \(2u\le3t\). If \(t-u\le-2\), then
\(t\le u-2\), and the two inequalities imply \(u\ge6\). Formula \(N\) has only
six variables, so \(u=6\), the assignment is empty, and all eight clauses
survive. This contradicts \(t\le4\). No smaller value exists. \(\square\)

The proof illustrates a useful certificate pattern. An upper bound is one
partial assignment. The lower bound is a global occurrence inequality plus a
finite boundary case, not a trust in solver output.

### 5.5 Fixed-threshold hardness from width three onward

**Theorem 9 (sign dichotomy by width).** For every fixed \(r\ge3\), deciding
\(\beta(F)\le0\) is NP-complete on proper simple \(r\)-uniform CNF. Its
complement, deciding \(\beta(F)>0\), is coNP-complete on the same class.

**Proof.** Reduce from the Simple MaxCut decision problem: given \(H\) and
\(K\), decide whether \(H\) has a cut of size at least \(K\) [11]. We restrict
without loss of generality to \(1\le K\le m=|E(H)|\). An input with \(K\le0\)
is trivially positive and is replaced by the fixed one-edge instance with
threshold one; an input with \(K>m\) is trivially negative and is replaced by
the fixed triangle instance with threshold three. Both replacements satisfy
\(1\le K\le m\), preserve the answer, and ensure \(m\ge1\). Form the
2-uniform CNF \(F_H\) above. Then
\(\beta(F_H)=m-\operatorname{MaxCut}(H)\). Apply one width lift, preserving the
value and producing a proper simple 3-uniform CNF. Add \(m-K\)
variable-disjoint copies of \(N\). By Theorem 4 and Lemma 8, the resulting
formula \(F'\) satisfies

\[
\beta(F')=m-\operatorname{MaxCut}(H)-(m-K)
=K-\operatorname{MaxCut}(H).
\]

Thus \(\beta(F')\le0\) exactly when the MaxCut instance is positive. The
reduction is polynomial and the problem is in NP. Repeated width lifts prove
the statement for each fixed \(r>3\). Complementation gives the coNP result.
\(\square\)

The problem parameterized only by \(q\) is consequently para-NP-hard: the
fixed slice \(q=0\) remains NP-hard at uniform width three. This rules out an FPT
algorithm in \(q\) alone unless \(P=NP\), contrasting with Almost-2-SAT. The
complexity of the sign problem on the narrower proper exact signed-occurrence
\((3,2,2)\) class
remains open. Satisfiability hardness for that class [5] does not resolve the
question because Section 4 showed that satisfiability does not determine the
sign of \(\beta\).

### 5.6 Bounded incidence treewidth

Let \(I(F)\) be the unsigned variable-clause incidence graph. Suppose it has a
tree decomposition of width \(t\). Replace every variable in each bag by its
two literal vertices and retain the clause vertices. The resulting bags cover
all formula-graph incidence edges and all complementary-pair edges, and they
preserve connected bag occurrence for every vertex. Their size is at most
twice the original bag size, giving formula-graph treewidth at most \(2t+1\).

Independent dominating sets are generalized \((\sigma,\rho)\)-sets with
\(\sigma=\{0\}\) and \(\rho=\{1,2,\ldots\}\). The bounded-treewidth algorithms
of Focke et al. apply to finite or cofinite degree sets and count sets of a
specified size [12]. With a decomposition supplied, one invocation for each
size \(s=0,\ldots,|V(G(F))|\) yields every coefficient of the independent
domination polynomial. This polynomial number of calls preserves the bound
\(2^{O(t)}|F|^{O(1)}\). Each coefficient is at most \(2^{|V(G(F))|}\), so its
binary representation has \(O(|F|)\) bits and the complete explicit output has
polynomial bit length. Taking the least nonzero size also gives the optimum.
Through Theorem 2 and Corollary 3, this computes \(\beta(F)\) and the complete
Laurent polynomial \(B_F(z)\). This is an exact structural route, not a
heuristic association between incidence width and solver performance.

### 5.7 Theorem-driven solver routing

The complexity results give a decision table rather than one universal
implementation.

| Recognized structure | Exact route | Mathematical guarantee |
|---|---|---|
| Clause width at most two | MaxSAT / Almost-2-SAT | \(\beta=\tau\), sign in P, threshold FPT |
| Small variable count | Ternary bilateral enumeration | \(O(3^k\|F\|)\), complete |
| Bounded incidence treewidth | Tree-decomposition DP via \(G(F)\) | \(2^{O(t)}|F|^{O(1)}\) |
| Regular-DIM formula signature | Formula optimization or graph IDS | exact gap \(i-\mu^*=\beta\) |
| Unrestricted fixed width \(r\ge3\) | proof-logging search, IDS, or MILP | NP-hard already at \(q=0\) |

This table supports algorithm selection in the precise sense that recognized
structure determines applicable exact reductions and parameterized bounds. It
does not claim that a prototype router can predict wall-clock dominance among
well-engineered solvers.

### 5.8 Paired-edge normal form for the unresolved \((3,2,2)\) slice

The occurrence restriction admits a more precise reformulation than generic
3-CNF. Let \(F\) be proper, simple, and exact signed-occurrence \((3,2,2)\),
with \(m\) clauses
and \(k\) variables. Form a clause multigraph \(Q(F)\) whose vertices are the
clauses. For each signed literal \(\ell\), join the two clauses containing
\(\ell\) by an edge \(e_\ell\). The graph is cubic, parallel edges are
possible, and for every variable \(x\) the two edges
\(e_x^+,e_x^-\) are vertex-disjoint and form a prescribed pair. Conversely,
every cubic multigraph whose edges are partitioned into such disjoint pairs
recovers an exact signed-occurrence \((3,2,2)\) formula up to variable names
and sign switches.

Call a set \(S\subseteq E(Q(F))\) **pair-feasible** when it contains at most
one edge from each prescribed pair and, for every pair not represented in
\(S\), each of its two edges has at least one endpoint outside \(V(S)\). Then

\[
\boxed{\displaystyle
\beta(F)=\frac m4-
\max_{S\ \mathrm{pair\text{-}feasible}}
\bigl(|V(S)|-|S|\bigr).}
\tag{5.1}
\]

To prove the identity, map an assigned variable to the edge belonging to its
satisfying sign and map an unassigned variable to no edge. The clauses
satisfied by assigned literals are exactly \(V(S)\). The condition imposed on
an unrepresented pair says exactly that at least one occurrence of each sign
survives, which is bilaterality. Since \(|S|=k-|U|\),

\[
|T|-|U|=m-|V(S)|-(k-|S|)
=\frac m4+|S|-|V(S)|,
\]

where \(3m=4k\) was used in the last equality. The construction is reversible,
so minimization gives (5.1).

Thus the exact sign question is equivalent to deciding whether the paired
coverage surplus in (5.1) is at least \(m/4\). This resembles a rainbow
matching problem because at most one edge may be selected from each two-edge
color class, but it has an additional induced-coverage condition on every
unselected pair and the objective is \(|V(S)|-|S|\), not cardinality. Ordinary
rainbow-matching hardness therefore does not, without a further reduction,
settle this slice. Nor can the maximum in (5.1) be restricted to
pair-feasible matchings: the supplied 9-variable, 12-clause counterexample has
\(\beta=-1\), hence optimum surplus four, while exhaustive matching search
finds no pair-feasible matching larger than three. Overlapping selected edges
are therefore an essential part of the exact normal form. The enforcer family
of Theorem 12 is a polynomial subcase:
its normal form collapses to minimum edge cover. Equation (5.1) records the
remaining complexity obstruction exactly and prevents the broader width-three
hardness theorem from being misreported as a solution of the bounded-occurrence
case.

## 6. Regular graphs with a dominating induced matching

Let \(G\) be a finite simple \(d\)-regular graph, \(d\ge2\), supplied with a
dominating induced matching \(M\) of size \(k\). A dominating induced matching
is an induced matching that edge-dominates the graph. Orient each edge of
\(M\), label its endpoints as the positive and negative literal vertices of
one variable, and turn every vertex outside \(V(M)\) into an indexed clause
containing its neighboring literal vertices.

This construction has rigid consequences. Endpoints of different matching
edges have no edges between them because \(M\) is induced. Vertices outside
\(V(M)\) form an independent set: an edge between two such vertices would
share no endpoint with an edge of \(M\), contrary to edge domination. Each
outside vertex has \(d\) distinct literal neighbors, so each clause contains
\(d\) distinct literal vertices. A clause may contain both signs of one
variable, which is why tautologies must be allowed in the complete
coordinatisation. Each signed literal vertex uses one incident edge in \(M\)
and has \(d-1\) remaining clause incidences. It therefore occurs exactly
\(d-1\) times in the formula.

Conversely, begin with an indexed formula in which every clause contains
exactly \(d\) distinct literal vertices and every signed literal occurs exactly
\(d-1\) times. Its formula graph is \(d\)-regular. The complementary-pair
edges form an induced matching, every other edge meets exactly one of those
edges, and the matching is dominating. The two constructions are inverse up
to labels and orientations. Hence this is a surjective coordinatisation of the
entire family of \(d\)-regular graphs equipped with a specified dominating
induced matching, rather than a construction of selected examples.

The phrase “equipped with” is essential. A graph can have more than one
dominating induced matching, and orienting a matching edge chooses which
endpoint represents the positive literal. Reversing one orientation switches
the corresponding variable sign throughout the reconstructed formula. These
operations may change the labeled formula while preserving an isomorphic
formula graph and the value of \(\beta\), because Theorem 10 identifies that
value with a graph-invariant gap. The coordinatisation is canonical relative
to a labeled, oriented matching and invariant, for the purpose of the gap,
under the resulting sign switches. It does not assert that an unlabeled graph
has a unique formula representation.

Counting degrees gives further invariants. If there are \(m\) clause vertices,
then the \(2k\) literal vertices have \(2k(d-1)\) clause incidences and the
clauses have \(dm\) such incidences. Therefore

\[
m=\frac{2k(d-1)}d,
\qquad
|V(G)|=\frac{2k(2d-1)}d,
\qquad
|E(G)|=k(2d-1).
\]

Let \(\mu^*(G)\) denote the minimum size of a maximal matching. The specified
pair matching is maximal, so \(\mu^*(G)\le k\). Every maximal matching is
edge-dominating. In a \(d\)-regular graph, one matching edge can dominate at
most \(2d-1\) graph edges: itself and the \(2(d-1)\) other edges incident with
its endpoints. Since \(G\) has \(k(2d-1)\) edges, every maximal matching has
at least \(k\) edges. Thus \(\mu^*(G)=k\).

This lower bound uses only regularity and maximality. The edges of any maximal
matching collectively dominate every graph edge, and one selected edge can
cover no more than its closed edge-neighborhood of size \(2d-1\). Equality is
witnessed by the specified DIM. The matching parameter is therefore fixed
throughout the coordinatised class before independent domination is optimized.
That separation makes \(\beta\) a coordinate of the entire gap rather than
one term in an equation with two unknown graph optima.

**Theorem 10 (regular-DIM gap classification).** Let \(F_M\) be the indexed
formula reconstructed from an oriented specified dominating induced matching
of a simple \(d\)-regular graph \(G\). Then

\[
i(G)-\mu^*(G)=\beta(F_M).
\]

**Proof.** The coordinatisation shows that \(G=G(F_M)\). Theorem 2 gives
\(i(G)=k+\beta(F_M)\), while the preceding edge count proves
\(\mu^*(G)=k\). Subtraction yields the identity. \(\square\)

**Theorem 11 (constructive regular-DIM replacement bound).** Let \(G\) be a
finite simple \(d\)-regular graph, \(d\ge2\), equipped with a dominating
induced matching. Then

\[
i(G)\le \mu^*(G)+
\left\lfloor
\frac{2(d-1)}{d\,2^d}\mu^*(G)
\right\rfloor.
\]

In particular,

\[
\frac{i(G)}{\mu^*(G)}
\le 1+\frac{2(d-1)}{d\,2^d}.
\]

An independent dominating set satisfying the integral bound can be found in
deterministic polynomial time.

**Proof.** Use the coordinatisation above and write \(k=|M|=\mu^*(G)\) and
\(m=2k(d-1)/d\) for the number of clause vertices. Choose one endpoint of
each edge of \(M\) independently and uniformly. A clause vertex is not
dominated precisely when none of its literal neighbours is selected. If the
associated clause is tautological, two of those neighbours are the endpoints
of one matching edge, so this probability is zero. Otherwise its \(d\)
literal neighbours lie on distinct matching edges and exactly one choice on
each edge avoids it. Its non-domination probability is therefore \(2^{-d}\).

If \(X\) counts the undominated clause vertices, linearity of expectation gives

\[
\mathbb E X\le \frac{m}{2^d}
=\frac{2k(d-1)}{d\,2^d}.
\]

Some choice consequently has
\(X\le\lfloor 2k(d-1)/(d\,2^d)\rfloor\). Add all of its undominated clause
vertices to the \(k\) selected literal vertices. Clause vertices are mutually
nonadjacent, and an added clause vertex has no selected literal neighbour by
definition, so the resulting set is independent. Every literal pair is
dominated by its selected endpoint, while every clause vertex is either
already dominated or is added. Thus the set is independently dominating and
has the asserted size.

For the algorithmic statement, expose the endpoint choices one matching edge
at a time and select the branch with no larger conditional expectation. The
conditional expectation never increases and the final integer value of \(X\)
is at most the floor of its initial expectation. All clause contributions can
be maintained directly from the incidence representation. \(\square\)

For cubic graphs this yields the concrete inequalities

\[
i(G)\le \mu^*(G)+\left\lfloor\frac{\mu^*(G)}6\right\rfloor
\le \frac76\mu^*(G).
\]

Since a cubic DIM graph in this coordinatisation has
\(|V(G)|=10\mu^*(G)/3\), it also gives

\[
\frac{i(G)-\mu^*(G)}{|V(G)|}\le\frac1{20}.
\]

More generally, the vertex count preceding Theorem 10 converts Theorem 11
into the all-degree density bound

\[
\frac{i(G)-\mu^*(G)}{|V(G)|}
\le \frac{d-1}{2^d(2d-1)}.
\tag{6.0}
\]

The degree-two endpoint can be settled exactly rather than bounded. Every
finite simple 2-regular component is a cycle, and a cycle has a dominating
induced matching precisely when its length is divisible by three. On
\(C_{3a}\), both the independent domination number and the minimum size of a
maximal matching are \(a\). Additivity over components therefore gives

\[
i(G)=\mu^*(G),
\qquad C_2^{\rm DIM}=1,
\qquad \lambda_2^{\rm DIM}=0.
\]

Thus the complete degree-two case and a constructive upper bound for every
\(d\ge2\) are known; positive constructions and sharp constants beyond degree
three remain separate questions.

Consequently, the sign of \(\beta(F_M)\) gives a complete trichotomy for the
gap:

\[
\begin{array}{c|c}
\beta(F_M)>0 & i(G)>\mu^*(G),\\
\beta(F_M)=0 & i(G)=\mu^*(G),\\
\beta(F_M)<0 & i(G)<\mu^*(G).
\end{array}
\]

For \(d=3\), non-tautological formulas in the coordinatisation are precisely
proper exact signed-occurrence \((3,2,2)\)-CNFs. Let \(P\) be the explicit
15-variable formula
of Appendix A. Proposition 14 proves \(\beta(P)=1\); the original formula was
supplied by the motivating release [1]. Let \(N\) be Lemma 8's component with
\(\beta(N)=-1\). Both are proper, simple, and exact signed-occurrence
\((3,2,2)\). Theorem 4
then proves

\[
\{\beta(F):F\text{ proper simple exact signed-occurrence }(3,2,2)
\text{-CNF}\}=\mathbb Z.
\]

Indeed, use \(z\) copies of \(P\) for an integer \(z>0\), \(-z\) copies of
\(N\) for \(z<0\), and \(P\sqcup N\) for zero. The corresponding cubic
regular-DIM graphs from this additive proof are generally disconnected. The
result is a full value spectrum, not a claim that \(\beta\) determines graph
isomorphism or every other invariant.

The following construction supplies the missing connected positive
amplification. Its finite ingredient is the \(E_{3,2,2}\) enforcer published
by Zhang, Peitl, and Szeider [4, Appendix A.1]. In the polarity used here it
is the ten-clause formula

\[
\begin{aligned}
E={}&(\neg x_1\vee\neg x_4\vee\neg x_8)
\wedge(\neg x_2\vee\neg x_6\vee\neg x_8)
\wedge(\neg x_1\vee\neg x_6\vee x_8)\\
&\wedge(\neg x_4\vee\neg x_7\vee x_8)
\wedge(\neg x_3\vee\neg x_5\vee x_7)
\wedge(\neg x_2\vee x_5\vee x_6)\\
&\wedge(\neg x_3\vee x_4\vee\neg x_7)
\wedge(x_3\vee\neg x_5\vee x_6)
\wedge(x_2\vee x_5\vee x_7)\\
&\wedge(x_2\vee x_3\vee x_4).
\end{aligned}
\]

The distinguished terminal is \(x_1\). It occurs negatively twice and not
positively; every other literal occurs exactly twice in each sign. Define a
local cost by counting surviving clauses of \(E\) and subtracting only
unassigned internal variables \(x_2,\ldots,x_8\), leaving the terminal charge
until gadgets are closed. Requiring bilaterality only for the internal
variables gives exactly the following finite terminal signature; these are
all feasible entries:

\[
\begin{array}{c|c|c}
\text{state of }x_1&\text{residual terminal signs}&\text{minimum local cost}\\
\hline
0&\varnothing&0\\
1&\varnothing&1\\
*&\varnothing&1\\
*&\{-\}&1.
\end{array}
\tag{6.1}
\]

The table is a finite lemma with two supplied paths. The Python enumerator
checks all \(3^8=6561\) local partial assignments and records a minimizing
witness for every entry. Separately, `lean_terminal_signature.lean` hard-codes
the ten displayed clauses, independently defines residual survival, internal
bilaterality, terminal masks and local cost, and proves by `native_decide` that
the complete computed signature equals exactly the four displayed rows. This
path has no DIMACS-parser or Python dependency; its translation boundary is
the visible clause transcription. Assigning the terminal zero permits cost
zero; assigning it one costs one; and leaving it unassigned can supply its
negative residual sign at local cost one before the terminal's single global
\(-1\) charge is applied.

**Theorem 12 (connected edge-cover amplifier).** Let \(R\) be a finite simple
connected cubic graph with \(r\) vertices. For every edge \(e\in E(R)\), take
a fresh copy \(E_e\) of the enforcer, identify its terminal \(x_1\) with a
variable \(y_e\), and keep all internal variables disjoint. For every vertex
\(v\in V(R)\), add the positive clause

\[
D_v=\bigvee_{e\ni v}y_e.
\]

Call the resulting indexed formula \(A(R)\). Then \(A(R)\) is proper, simple,
exact signed-occurrence \((3,2,2)\), and its formula graph is connected.
Moreover,

\[
\beta(A(R))=\rho(R)=r-\nu(R),
\tag{6.2}
\]

where \(\rho(R)\) is the minimum edge-cover number and \(\nu(R)\) the maximum
matching number. Consequently its cubic DIM graph satisfies

\[
|V(G(A(R)))|=40r,\qquad
\mu^*(G(A(R)))=12r,\qquad
i(G(A(R)))=12r+\rho(R).
\tag{6.3}
\]

**Proof.** A cubic graph has \(3r/2\) edges. Each enforcer copy contributes
seven fresh internal variables in addition to its edge terminal and ten
clauses; the vertex clauses contribute \(r\) more clauses. Thus \(A(R)\) has
\(12r\) variables and \(16r\) clauses. Every internal signed literal retains
its two occurrences from \(E\). Each terminal occurs negatively twice in its
enforcer and positively in the two vertex clauses at the ends of its edge.
The clauses have three distinct variables and no two are equal: enforcer
clauses from different copies have disjoint internal variables, and a vertex
clause cannot equal an enforcer clause. Hence the formula is proper, simple,
and exact signed-occurrence \((3,2,2)\).

For the value calculation, let \(S\subseteq E(R)\) be the set of terminals
assigned one. By (6.1), those enforcers contribute one each, terminals
assigned zero contribute zero, and a terminal left unassigned has net
contribution zero after its delayed terminal charge. A vertex clause survives
exactly when its vertex is not incident with \(S\). Moreover, every
unassigned terminal can be replaced by zero without changing which vertex
clauses survive or increasing the cost. It follows that

\[
\beta(A(R))=\min_{S\subseteq E(R)}
\bigl(|S|+u_R(S)\bigr),
\tag{6.4}
\]

where \(u_R(S)\) is the number of vertices uncovered by \(S\). Every edge
cover has objective equal to its cardinality. Conversely, from any \(S\), add
one incident edge for each uncovered vertex; the result is an edge cover of
size at most \(|S|+u_R(S)\). Hence (6.4) equals \(\rho(R)\). Since \(R\) has no
isolated vertices, the standard edge-cover identity gives
\(\rho(R)=r-\nu(R)\).

The literal--clause incidence supplied by the vertex clauses contains the
subdivision incidence graph of the connected skeleton \(R\). Direct
inspection of the displayed enforcer shows that every vertex of each copy's
formula graph is joined to its terminal pair. Thus all copies join the same
connected core, proving connectivity. Finally, the counts above and Theorem
10 give (6.3). \(\square\)

Taking \(R=C_s\square K_2\), \(s\ge3\), gives \(r=2s\) and a perfect matching
of size \(s\), so \(\rho(R)=s\). Therefore there is an explicit infinite
family of connected cubic DIM graphs \(G_s\) with

\[
|V(G_s)|=80s,\qquad \mu^*(G_s)=24s,\qquad i(G_s)=25s,
\qquad i(G_s)-\mu^*(G_s)=s.
\tag{6.5}
\]

In particular, their ratio is \(25/24\) and their gap density is \(1/80\).
The edge-cover reduction also allows a sharper choice of skeleton. O and West
proved that every connected cubic graph of order \(r\) has matching number at
least \((4r-1)/9\), and characterized an infinite equality family
\(\mathcal H_1\) [13]. A canonical sequence \(R_t\in\mathcal H_1\) has

\[
r_t=16+18t,\qquad
\nu(R_t)=\frac{4r_t-1}{9},\qquad
\rho(R_t)=\frac{5r_t+1}{9}.
\tag{6.6}
\]

Applying Theorem 12 gives connected cubic DIM graphs of order \(40r_t\) and
gap \((5r_t+1)/9\). Their gap density tends to \(1/72\), and their ratio tends
to \(113/108\). The initial skeleton has order 16 and gives the exact tuple
\((|V|,\mu^*,i)=(640,192,201)\), hence ratio \(67/64\). The same O--West lower
bound shows that \(1/72\) is the sharp asymptotic density attainable inside
this edge-cover-amplifier construction, even though it need not be sharp for
the full cubic DIM class.

If

\[
C_3^{\rm DIM}=\sup_G\frac{i(G)}{\mu^*(G)}
\quad\text{and}\quad
\lambda_3^{\rm DIM}=\limsup_{n\to\infty}
\sup_{\substack{G:\ |V(G)|\ge n}}
\frac{i(G)-\mu^*(G)}{|V(G)|},
\]

where \(G\) ranges over connected cubic graphs equipped with a DIM, then the
finite base \(P\), Theorem 11, and (6.5) give the certified bounds

\[
\frac{16}{15}\le C_3^{\rm DIM}\le\frac76,
\qquad
\frac1{72}\le\lambda_3^{\rm DIM}\le\frac1{20}.
\tag{6.7}
\]

**Corollary 13 (minimum counterexample order in the cubic-DIM class).** If a finite simple
cubic graph \(G\) is equipped with a dominating induced matching and satisfies
\(i(G)>\mu^*(G)\), then \(|V(G)|\ge50\). Equality is attained by the connected
graph generated from \(P\) in Appendix A.

**Proof.** Reconstruct the indexed signed-occurrence formula \(F_M\) from the
specified DIM. If \(i(G)>\mu^*(G)\), Theorem 10 gives \(\beta(F_M)>0\). Every
complete assignment is bilateral, so \(F_M\) must be unsatisfiable. Delete
tautological clauses and collapse repeated indexed clauses. Neither operation
changes satisfiability, and the result is an unsatisfiable non-tautological
3-CNF in which each signed literal occurs at most twice. Zhang, Peitl, and
Szeider proved that every such \((3,2,2)\)-formula has at least 20 distinct
clauses [4, Theorem 15]. Hence the original indexed formula has \(m\ge20\)
clauses. Its occurrence count is \(3m=4k\), while its formula graph has order
\(2k+m=5m/2\), so \(|V(G)|\ge50\). Proposition 14 and a direct incidence
traversal show that \(P\) has positive value and a connected 50-vertex formula
graph. \(\square\)

## 7. Six uses and an infrastructure for mathematics

### 7.1 Systematic discovery

Within the proper exact signed-occurrence \((3,2,2)\) space, the formula graph
is cubic, its
complementary pairs form a dominating induced matching, and

\[
G(F)\text{ satisfies }i(G)>\mu^*(G)
\quad\Longleftrightarrow\quad
\beta(F)>0.
\]

This turns counterexample discovery into a necessary-and-sufficient formula
search: generate formulas under the signed-occurrence constraints, optimize
\(\beta\), retain positive instances, and translate them canonically. Symmetry
breaking can quotient variable renamings, sign switches, and clause
permutations without altering the objective. The method is systematic because
the coordinatisation is surjective for graphs with a specified DIM. It is not
an efficient enumeration theorem, and the sign complexity of the exact
\((3,2,2)\) slice remains unknown.

### 7.2 Compact proof production

An upper bound \(\beta(F)\le q\) has a compact certificate: a bilateral partial
assignment with deficiency at most \(q\). A lower bound
\(\beta(F)\ge q\) is different. In unrestricted formulas it is a coNP-type
obligation and may require exhaustive branch-and-bound, a SAT or MILP proof
log, a graph-side independent-domination certificate, or a structural
inequality such as Lemma 8. No uniform polynomial-size lower certificate is
claimed.

Composition supplies an important exception. For a block-disjoint formula,
Theorem 4 reduces the proof to three checks: certify each distinct component,
verify the declared variable and clause partition, and add the values. A
benchmark containing thousands of copies need not be searched monolithically.
The artifact implements this proof rule and binds each CNF to its reconstructed
graph by cryptographic hash. Compactness therefore arises from mathematical
structure rather than compression of an unexplained solver verdict.

There are consequently three assurance levels for a reported value. A
bilateral assignment alone proves an upper bound. An exhaustive receipt
records that a particular program searched its declared domain, but its force
depends on the implementation and execution environment. A structural proof
or independently checkable proof log establishes the lower bound without
trusting the optimizer's summary. The current package uses a written
occurrence inequality for the negative gadget, a separately implemented
exhaustive solver for the positive base instance, an independently checkable
LRAT lower-bound certificate for that base, and additive manifests for large
composites. The direct LRAT file is checked both by the pinned native checker
and by Lean's verified LRAT checker; the formula-to-encoding equivalence
remains a displayed mathematical lemma. A JSON receipt records this chain but
is not itself the proof.

### 7.3 Algorithm selection

Section 5 provides a structural dispatcher. Width-two formulas should be sent
to MaxSAT or Almost-2-SAT methods because equality with \(\tau\) is a theorem.
Small formulas can use direct ternary enumeration, and small-incidence-width
formulas admit tree-decomposition dynamic programming. A recognized
regular-DIM signature permits either formula optimization or graph independent
domination, with the output interpreted immediately as a gap. Unrestricted
width-three instances require general proof-producing optimization unless
further structure is detected. This is a mathematical selection layer, not a
learned performance model.

### 7.4 Algebraic conformance benchmark generation

The algebra gives orthogonal benchmark controls. Width lifting changes the
uniform clause width while preserving the target value. Indexed replication changes
the penalty scale and exposes a MaxSAT primary optimum plus the \(u^*\)
secondary optimum. Disjoint union adds prescribed values and convolves all
solution multiplicities. The positive and negative exact signed-occurrence
\((3,2,2)\)
components generate every integer target while preserving the regular-DIM
signature.

The current artifact includes verified target values \(3,-2,0\), and \(-4\).
Its manifests identify component templates, multiplicities, formula hashes,
graph hashes, and the additive proof rule. These are algebraic conformance
benchmarks because the expected value follows from a theorem and separately
checked base components. They test whether a solver or transformation respects
prescribed identities. They are not presented as statistically representative
samples of industrial SAT distributions or as an empirical performance suite.

### 7.5 Classification of a structured graph family

Theorem 10 classifies every finite simple \(d\)-regular graph supplied with a
dominating induced matching. It identifies the precise formula class, proves the
matching parameter \(\mu^*=k\), and makes \(\beta\) the complete signed gap
coordinate. The word “complete” refers to the trichotomy and numerical value
of \(i-\mu^*\) throughout this equipped family. It does not mean that two
formulas with equal \(\beta\) yield isomorphic graphs, nor that the parameter
classifies regular graphs without a specified DIM.

### 7.6 AI-assisted mathematical infrastructure

Bilateral deficiency supports a typed pipeline suited to assisted discovery:

\[
\text{indexed CNF}
\to\text{canonical residual objective}
\to\text{exact solver}
\to\text{certificate or receipt}
\to\text{independent checker}
\to\text{graph-theorem instance}.
\]

The type boundaries matter. Indexed semantics prevent silent loss of duplicate
clauses. The bilateral condition is checked independently of the objective.
The polynomial identity permits cross-model comparison of every solution
size. Composition manifests separate base proofs from large-instance assembly.
Tests under both ordinary Python and optimization mode guard against
assertion-only verification. During development, a cross-check exposed a
specific implementation error: residual polarities had been recorded from a
clause before the scan later discovered that another assigned literal
satisfied it. The C++ solver was corrected to classify clause survival before
recording residual occurrences. This failure is informative because it shows
why independently phrased semantics and cross-model tests are necessary.

The positive-base development adds a second instructive failure boundary. A
first cardinality encoding was mathematically adequate but generated a large,
symmetry-heavy proof. Replacing it by a deterministic prefix-balance automaton
produced a compact encoding whose direct LRAT proof is accepted by both a
native checker and Lean. An intermediate LRAT translation passed the native
checker but not Lean; retaining separate proof paths exposed this format-level
incompatibility instead of concealing it behind a solver status. Hashes bind
the input, encoding, map, proof, wrapper, and receipt, but hashes establish
identity rather than correctness.

The infrastructure claim is technical. The artifact demonstrates that a model
can propose instances, route exact methods, generate a lower-bound encoding,
and emit checkable evidence without making its own prose authoritative. It
does not establish that generated text is a proof, that the complete theorem
has been formalized, or that the parameter has received mathematical community
adoption.

## 8. Reproducibility, limitations, and open problems

The accompanying package contains a separately implemented Python semantics,
a dependency-free C++ exhaustive solver, unit and exhaustive cross-model
tests, a structural analyzer, an algebraic conformance benchmark generator and
verifier, a deterministic SAT threshold encoder, three finite threshold
encodings, four native-checked LRAT derivations, Lean wrappers for the three
direct derivations, and the parser-independent Lean terminal lemma. The Python
tests compare bilateral assignments with graph independent dominating sets,
including full size spectra, over more than one hundred small indexed formulas.
They cover empty, unit, binary, tautological, duplicate-clause, and absent-
variable cases. Tests also exercise width-two equality, additivity,
convolution, lifting, replication, DIM signatures, graph reconstruction, and
mutation rejection. The same suite passes with ordinary execution and
`python -O`.

The C++ solver enumerated all \(3^{15}=14{,}348{,}907\) partial assignments of
the canonical formula, found \(939{,}975\) bilateral assignments, and returned
\(\beta=1\). It independently returned \(-1\) for \(N\). These receipts verify
finite computations and agreement between implementations. They do not prove
the universal theorems. Conversely, the written proofs do not certify that a
particular source archive or executable was transmitted without corruption.
The supplement supplies commands, expected results, and hashes so these
assurance layers remain separate. In addition, the lower-bound encoding for
\(P\) has 731 variables and 9,256 clauses. A native checker verifies both the
trimmed and direct LRAT derivations; Lean 4.32.1's
`Std.Tactic.BVDecide.LRAT` checker verifies the direct derivation. Proposition
14 states the encoding lemma and the exact hashes needed to connect these
finite artifacts to \(\beta(P)=1\).

The semantic bridge for this first encoding is also checked by a standard-
library clean-room validator that imports neither the production encoder nor
`bd_core.py`. It independently reconstructs the complete 731-variable map and
the multiset and canonical order of all 9,256 clauses. On a seven-formula
corpus it compares the mathematical ternary-state oracle with an independent
DPLL implementation at the exact thresholds \(q=\beta-1\) and \(q=\beta\),
including 66 fixed-state checks, and rejects a rehashed clause mutation. The
production compiler is invoked only as a black box to make the corpus
encodings. This is producer-side clean-room conformance evidence, not an
unaffiliated reproduction or a proof of the universal encoding lemma.

The enforcer composition used to validate the terminal calculus has a separate
certificate chain. Its independently regenerated threshold encoding again has
731 variables and 9,256 clauses. The direct LRAT proof has 35,737 actions and
is accepted by both the pinned native checker and Lean. This second proof is
not needed for Corollary 13 or the integer spectrum, which already use \(P\);
it checks an attributed, structurally distinct positive base and the generic
threshold compiler on a second input.

The connected occurrence switch is an extended, optional third finite
certificate chain; no theorem in this paper depends on replaying it. Its
value-one witness is checked directly, while a byte-regenerated 2,686-variable,
65,061-clause encoding of \(\beta\le0\) is refuted by a 5,793,599,477-byte
direct LRAT proof. The pinned native checker reports `VERIFIED`; Lean parses
11,393,023 actions and reports `LEAN_LRAT_VERIFIED`. The proof's size is an
engineering limitation, not a logical gap, and motivates compact structured
certificates for future connected searches. The core archive retains its
formula, encoding, map, hash and verification receipt; the raw 5.79 GB LRAT is
distributed as a separately listed extended object.

Three mathematical problems are immediate. The complexity of
\(\beta(F)\le0\) on proper simple exact signed-occurrence
\((3,2,2)\)-CNF is open. Theorem 12
settles connected positive amplification, but the exact constants in (6.7),
and connected constructions for arbitrary signed values remain open.
Corollary 13 settles the minimum order within the cubic-DIM class, although
classification of all order-50 extremizers and the minimum outside DIM remain
open. The general threshold compiler supplied
with the artifact should be extended with compact proof-producing backends
for larger instances. Formalization of the encoding lemma and Theorems 1, 2,
7, 10, 11, and 12 is also desirable.

Two external limitations remain. The priority search was bounded and should
be extended through MathSciNet, zbMATH, dissertations, and alternative
terminology. No empirical solver competition has been conducted, so the
algorithm table records applicability and asymptotic guarantees rather than
performance rankings. The work is unrefereed. Three finite threshold encodings
have direct LRAT derivations checked by Lean, and the enforcer terminal table
has a separate parser-independent Lean proof, but the general mathematical
theory has not been formalized in a proof assistant.

These limits also constrain the novelty claim. The search found a close
antecedent that materially changed the paper's wording, which shows that the
audit was substantive. It does not show that every terminology branch has
been exhausted. Mathematical correctness, computational reproduction,
historical priority, and scholarly acceptance are four distinct review
questions and are reported separately here.

## 9. Conclusion

Bilateral deficiency satisfies the criteria set in the introduction. It is
the minimum deficiency of a bipolar residual, the exact formula-side
coordinate of independent domination on formula graphs, an additive and
width-stable optimization parameter, equal to the width-two MaxSAT defect and
capable of recovering general MaxSAT after replication. Its sign changes from
polynomial-time decidable at width two to NP-complete at every fixed uniform
clause width at least three when occurrences are unrestricted. On regular
graphs with a specified dominating induced matching, it is exactly the
invariant gap \(i-\mu^*\), and its proper exact signed-occurrence
\((3,2,2)\) spectrum is all integers. The enforcer construction additionally
gives an infinite connected cubic family with linear gap and identifies its
value exactly with an edge-cover number. O--West skeletons yield asymptotic
gap density \(1/72\), while the SAT 2024 clause lower bound proves that order
50 is minimum among cubic graphs admitting a dominating induced matching and
satisfying \(i(G)>\mu^*(G)\). The minimum outside the DIM-equipped class remains
open.

The strongest warranted originality claim is correspondingly precise. The
partial-assignment cost decomposition has a 2008 antecedent [2]. The explicit
bilateral domain, residual parameter, size-preserving bijection, algebra,
complexity boundary, regular-DIM coordinatisation, and reproducible
infrastructure constitute the advance supported here. These results establish
that bilateral deficiency is not disposable notation for one graph. Global
priority, full formal verification, peer acceptance, and adoption remain
separate questions.

The resulting research programme is concrete. Complexity on the exact
signed-occurrence \((3,2,2)\) sign slice, sharp regular-DIM constants,
classification of the order-50 extremizers, stronger proof-producing
compilation, and proof-assistant
formalization of the theory are independent next steps. None is needed for
the parameter identity, but each would strengthen a different
assurance layer. In its current form, the theory already supplies a general
definition, exact translations, separations, closure operations, a sharp width
boundary, and a complete regular-DIM gap coordinate. That combination is the
mathematical content of the claim that \(\beta\) is a parameter in its own
right.

## Appendix A. The positive exact signed-occurrence \((3,2,2)\) base

This appendix makes the only finite positive component used in the integer
spectrum theorem completely explicit. Let \(P\) be the following indexed CNF;
the displayed order is its clause indexing.

\[
\begin{aligned}
 &(x_1\vee x_9\vee\neg x_{11})
\wedge(\neg x_4\vee\neg x_{10}\vee\neg x_{13})
\wedge(x_1\vee\neg x_9\vee\neg x_{14})\\
{}\wedge{}&(x_2\vee x_6\vee x_{14})
\wedge(\neg x_5\vee\neg x_6\vee x_{15})
\wedge(x_2\vee\neg x_3\vee x_{15})\\
{}\wedge{}&(x_3\vee x_5\vee\neg x_9)
\wedge(\neg x_6\vee\neg x_{12}\vee\neg x_{15})
\wedge(\neg x_1\vee x_5\vee\neg x_{11})\\
{}\wedge{}&(x_4\vee\neg x_7\vee\neg x_{15})
\wedge(\neg x_2\vee x_8\vee\neg x_{12})
\wedge(x_3\vee x_9\vee x_{11})\\
{}\wedge{}&(\neg x_4\vee\neg x_8\vee x_{10})
\wedge(x_7\vee\neg x_8\vee x_{13})
\wedge(x_4\vee x_7\vee\neg x_{13})\\
{}\wedge{}&(\neg x_2\vee\neg x_7\vee x_{14})
\wedge(\neg x_3\vee x_{11}\vee\neg x_{14})
\wedge(x_8\vee x_{10}\vee x_{12})\\
{}\wedge{}&(\neg x_{10}\vee x_{12}\vee x_{13})
\wedge(\neg x_1\vee\neg x_5\vee x_6).
\end{aligned}
\]

Every clause has three distinct variables and the clauses are pairwise
different. The complete signed-occurrence audit is:

| variable | positive clause indices | negative clause indices |
|---:|---:|---:|
| \(x_1\) | 1, 3 | 9, 20 |
| \(x_2\) | 4, 6 | 11, 16 |
| \(x_3\) | 7, 12 | 6, 17 |
| \(x_4\) | 10, 15 | 2, 13 |
| \(x_5\) | 7, 9 | 5, 20 |
| \(x_6\) | 4, 20 | 5, 8 |
| \(x_7\) | 14, 15 | 10, 16 |
| \(x_8\) | 11, 18 | 13, 14 |
| \(x_9\) | 1, 12 | 3, 7 |
| \(x_{10}\) | 13, 18 | 2, 19 |
| \(x_{11}\) | 12, 17 | 1, 9 |
| \(x_{12}\) | 18, 19 | 8, 11 |
| \(x_{13}\) | 14, 19 | 2, 15 |
| \(x_{14}\) | 4, 16 | 3, 17 |
| \(x_{15}\) | 5, 6 | 8, 10 |

Thus \(P\) is proper, simple, and exact signed-occurrence \((3,2,2)\).

**Proposition 14 (checker-assisted finite base).** \(\beta(P)=1\).

**Proof.** For the upper bound, use the ternary assignment

\[
\alpha=0000***********,
\]

where the first four variables are assigned zero and the other eleven are
unassigned. Exactly the indexed clauses

\[
1,3,4,5,7,8,10,12,14,15,18,19
\]

survive. Each unassigned variable occurs in both signs among those twelve
clauses, so \(\alpha\) is bilateral and
\(\delta_P(\alpha)=12-11=1\). Hence \(\beta(P)\le1\).

For direct inspection, the positive/negative residual witnesses for
\(x_5,\ldots,x_{15}\) are respectively

| variable | positive clauses | negative clauses |
|---:|---:|---:|
| \(x_5\) | 7 | 5 |
| \(x_6\) | 4 | 5, 8 |
| \(x_7\) | 14, 15 | 10 |
| \(x_8\) | 18 | 14 |
| \(x_9\) | 1, 12 | 3, 7 |
| \(x_{10}\) | 18 | 19 |
| \(x_{11}\) | 12 | 1 |
| \(x_{12}\) | 18, 19 | 8 |
| \(x_{13}\) | 14, 19 | 15 |
| \(x_{14}\) | 4 | 3 |
| \(x_{15}\) | 5 | 8, 10 |

For the lower bound, encode the proposition \(\beta(P)\le0\) as CNF. For
each \(x_j\), use three Boolean variables \(z_j^0,z_j^1,u_j\), constrained to
have exactly one true value, representing assignment to zero, assignment to
one, and nonassignment. For every indexed clause \(C_a\), define a Boolean
variable \(r_a\) by clauses expressing

\[
r_a\longleftrightarrow
\bigwedge_{\ell\in C_a}\neg s_\ell,
\qquad
s_{x_j}=z_j^1,
\quad
s_{\neg x_j}=z_j^0.
\]

Thus \(r_a\) is true exactly when \(C_a\) survives. The implications

\[
u_j\to\bigvee_{a:x_j\in C_a}r_a,
\qquad
u_j\to\bigvee_{a:\neg x_j\in C_a}r_a
\]

express bilaterality. Finally, order the bits as
\(r_1,\ldots,r_{20},u_1,\ldots,u_{15}\), with respective weights \(+1\) and
\(-1\). One-hot variables \(q_{i,d}\) track the unique prefix sum. Starting
from \(q_{0,0}\), the clauses encode both transitions

\[
q_{i-1,d}\wedge\neg b_i\to q_{i,d},
\qquad
q_{i-1,d}\wedge b_i\to q_{i,d+w_i},
\]

and forbid every final state with \(d>0\).

We record the required encoding lemma explicitly. The encoding is satisfiable
if and only if there is a bilateral partial assignment \(\gamma\) with
\(\delta_P(\gamma)\le0\). In the forward direction, the exactly-one clauses
define \(\gamma\); the \(r_a\) equivalences identify its indexed residual, the
two polarity implications give bilaterality, and induction over the automaton
layers shows that the final state equals
\(\sum_a r_a-\sum_j u_j\le0\). Conversely, any such \(\gamma\) fixes the
assignment and residual indicators, and setting the unique true state in each
layer to the actual prefix sum satisfies every encoding clause. This proves
the equivalence.

The resulting DIMACS instance has 731 variables and 9,256 clauses. Its SHA-256
digest is
`c282d2d35f66e81ae175d9afa560b9a5ded2d00f51d8b02c380d939102156c11`.
The trimmed companion certificate is obtained through the DRAT proof format
[14]. The independently checkable lower-bound derivations use LRAT [15] and
were generated by CaDiCaL 3.0 [16]. The direct LRAT derivation has digest
`61bb30cadaf1cbf4bd15662a1a97b0a6352b416a187532c887000493f46f755a`.
The pinned native `lrat-check` accepts it, and Lean 4.32.1 [17] using the LRAT
checker now distributed in Lean core [18] accepts all 118,497 actions and
returns `LEAN_LRAT_VERIFIED`. Therefore the encoded CNF
is unsatisfiable. By the encoding lemma, no bilateral assignment has value at
most zero, so \(\beta(P)\ge1\). Together with the displayed witness,
\(\beta(P)=1\). \(\square\)

The assurance boundary is exact. The LRAT checker proves unsatisfiability of
the 9,256-clause encoding, and Lean's `LRAT.check_sound` theorem connects a
successful LRAT check to `CNF.Unsat`. A clean-room validator independently
reconstructs the symbolic map and every clause of this encoding and performs
small-formula semantic checks, reducing - but not eliminating - the translation
obligation represented by the written encoding lemma. The general bilateral-
deficiency theory is not thereby fully formalized. The artifact regenerates
the CNF and encoding map byte-for-byte, checks the witness independently,
invokes both native LRAT paths and the Lean path, and emits deterministic
receipts.

## Declarations

### Data and code availability

The manuscript is accompanied by a reproducibility supplement and an artifact
archive containing source code, indexed CNF instances, generated graph data,
tests, and exact receipts. Version 1.0.1-candidate is archived at
<https://doi.org/10.5281/zenodo.21857209>, with source at
<https://github.com/ipitchford/bilateral-deficiency>. The motivating
TxGraffiti release and its public repository are listed in Reference [1].

### Ethics approval

This theoretical and computational study involved no human participants,
personal data, animals, or biological materials. Institutional ethics approval
was therefore not applicable.

### Author contributions (CRediT)

**Anonymous:** Conceptualization, Formal analysis, Methodology, Software,
Validation, Writing-original draft, and Writing-review and editing. Ian
Pitchford acts as archive maintainer and Evidence Press publisher and is not
listed as a scholarly author. AI systems are not authors.

### Funding

No specific funding is reported for this unrefereed release.

### Declaration of interests

No competing interests are reported for this unrefereed release.

### AI-assistance disclosure

OpenAI Codex was used to assist literature discovery, mathematical drafting,
software generation, test design, and editorial revision. Its outputs were
treated as untrusted proposals and checked against primary sources, written
proofs, separately implemented solvers and checkers, exhaustive finite tests,
and mutation controls. The anonymous scholarly author remains accountable for
every claim, citation, proof, and disclosed artifact.

## References

[1] Evidence Press, “TxGraffiti conjecture 3 resolution,” 2026. [Online].
Available: https://evidencepress.org/releases/txgraffiti-c3-resolution/ and source
repository: https://github.com/ipitchford/txgraffiti-conjecture3-resolution

[2] M. Chlebík and J. Chlebíková, “Approximation hardness of dominating set
problems in bounded degree graphs,” *Information and Computation*, vol. 206,
no. 11, pp. 1264-1275, 2008, doi: 10.1016/j.ic.2008.07.003.

[3] I. E. Zverovich, “Satgraphs and independent domination. Part 1,”
*Theoretical Computer Science*, vol. 352, nos. 1-3, pp. 47-56, 2006,
doi: 10.1016/j.tcs.2005.08.038.

[4] T. Zhang, T. Peitl, and S. Szeider, “Small unsatisfiable \(k\)-CNFs with
bounded literal occurrence,” in *Proc. 27th International Conference on Theory
and Applications of Satisfiability Testing (SAT 2024)*, LIPIcs, vol. 305,
Art. no. 31, 2024, doi: 10.4230/LIPIcs.SAT.2024.31.

[5] A. Ahadi and A. Dehghan, “The \((2/2/3)\)-SAT problem and its applications
in dominating set problems,” *Discrete Mathematics & Theoretical Computer
Science*, vol. 21, no. 4, 2019, doi: 10.23638/DMTCS-21-4-9.

[6] O. Kullmann, “Constraint satisfaction problems in clausal form I:
Autarkies and deficiency,” *Fundamenta Informaticae*, vol. 109, no. 1,
pp. 27-81, 2011, doi: 10.3233/FI-2011-428.

[7] S. Szeider, “Minimal unsatisfiable formulas with bounded clause-variable
difference are fixed-parameter tractable,” *Journal of Computer and System
Sciences*, vol. 69, no. 4, pp. 656-674, 2004,
doi: 10.1016/j.jcss.2004.04.009.

[8] M. Dod, “The independent domination polynomial,” arXiv:1602.08250, 2016.
[Online]. Available: https://arxiv.org/abs/1602.08250

[9] S. Jahari and S. Alikhani, “On the independent domination polynomial of a
graph,” arXiv:1808.07369, 2018. [Online]. Available:
https://arxiv.org/abs/1808.07369

[10] I. Razgon and B. O'Sullivan, “Almost 2-SAT is fixed-parameter
tractable,” *Journal of Computer and System Sciences*, vol. 75, no. 8,
pp. 435-450, 2009, doi: 10.1016/j.jcss.2009.04.002.

[11] M. R. Garey, D. S. Johnson, and L. Stockmeyer, “Some simplified
NP-complete graph problems,” *Theoretical Computer Science*, vol. 1, no. 3,
pp. 237-267, 1976, doi: 10.1016/0304-3975(76)90059-1.

[12] J. Focke, D. Marx, F. Mc Inerney, D. Neuen, G. S. Sankar, P. Schepper,
and P. Wellnitz, “Tight complexity bounds for counting generalized dominating
sets in bounded-treewidth graphs-Part I: Algorithmic results,” *ACM
Transactions on Algorithms*, vol. 21, no. 3, Art. no. 27, 2025,
doi: 10.1145/3731452.

[13] S. O and D. B. West, “Balloons, cut-edges, matchings, and total
domination in regular graphs of odd degree,” *Journal of Graph Theory*, vol.
64, no. 2, pp. 116-131, 2010, doi: 10.1002/jgt.20443.

[14] N. Wetzler, M. J. H. Heule, and W. A. Hunt, Jr., “DRAT-trim: Efficient
checking and trimming using expressive clausal proofs,” in *Theory and
Applications of Satisfiability Testing-SAT 2014*, LNCS, vol. 8561,
pp. 422-429, 2014, doi: 10.1007/978-3-319-09284-3_31.

[15] L. Cruz-Filipe, M. J. H. Heule, W. A. Hunt, Jr., M. Kaufmann, and
P. Schneider-Kamp, “Efficient certified RAT verification,” in *Automated
Deduction-CADE 26*, LNCS, vol. 10395, pp. 220-236, 2017,
doi: 10.1007/978-3-319-63046-5_14.

[16] F. Pollitt, M. Fleury, K. Fazekas, N. Froleyks, A. Schidler,
D. Schreiber, and A. Biere, “CaDiCaL 3.0,” in *29th International Conference
on Theory and Applications of Satisfiability Testing (SAT 2026)*, LIPIcs,
vol. 377, Art. no. 40, pp. 40:1-40:14, 2026,
doi: 10.4230/LIPIcs.SAT.2026.40.

[17] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and programming
language,” in *Automated Deduction-CADE 28*, LNCS, vol. 12699, pp. 625-635,
2021, doi: 10.1007/978-3-030-79876-5_37.

[18] Lean Prover Community, “LeanSAT: verified SAT reasoning,” software
repository, 2024. [Online]. Available: https://github.com/leanprover/leansat
