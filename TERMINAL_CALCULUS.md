# Certified terminal signatures for bilateral deficiency

## Gadget model

Let (H) be an indexed CNF and let (B=(b_1,\ldots,b_t)) be an ordered set
of terminal variables.  The remaining variables are internal.  For a partial
assignment \(\alpha\), require bilaterality only for unassigned internal
variables.  For every unassigned terminal, record a two-bit residual mask:
bit (+) says that the positive literal occurs in a surviving indexed clause,
and bit (-) says the same for the negative literal.

For a terminal state vector (s\in\{0,1,*\}^t) and mask vector
(p\in\{0,+,-,\pm\}^t), define

\[
\Sigma_H(s,p)=
\min_\alpha\bigl(|T_H(\alpha)|-|U_{\mathrm{int}}(\alpha)|\bigr),
\]

where \(\alpha|_B=s\), every unassigned internal variable is bilateral, and
the terminal residual masks are exactly (p).  Infeasible entries are
omitted.  Assigned terminals have mask zero.  The implementation stores one
lexicographically least minimizing witness for every finite entry.

## Exact closing rule

If the terminals are no longer exposed, an entry is feasible precisely when
each unassigned terminal has mask \(\pm\).  Its global value is

\[
\Sigma_H(s,p)-|\{j:s_j=*\}|.
\]

The subtraction is delayed until closing because each global terminal variable
must contribute (-1) exactly once, regardless of how many gadgets meet it.
Taking the minimum of this expression over feasible entries gives
\(\beta(H)\).

## Exact two-gadget composition theorem

Let (H_1,H_2) have disjoint indexed clause sets and disjoint internal
variable sets, and identify their ordered terminal lists.  There are no other
shared variables.  Let (H=H_1\cup_B H_2).  Then

\[
\beta(H)=
\min_{s,p_1,p_2}
\left(
\Sigma_{H_1}(s,p_1)+\Sigma_{H_2}(s,p_2)
-|\{j:s_j=*\}|
\right),
\]

where, for every (j) with (s_j=*), the bitwise union
(p_{1,j}\lor p_{2,j}) contains both polarities.

### Proof

Restrict any global assignment to each gadget.  Surviving indexed clauses
partition by gadget, and unassigned internal variables partition by gadget.
The terminal state is common.  An unassigned terminal is globally bilateral
if and only if the union of the two local residual masks supplies both signs.
Thus every global bilateral assignment contributes the displayed sum for one
feasible pair of entries, proving the lower bound by local minimization.

Conversely, take minimizing witnesses for a feasible pair with the same
terminal state.  Their internal assignments have disjoint domains and hence
combine uniquely.  Local bilaterality handles every unassigned internal
variable; the mask-union condition handles every unassigned terminal.  Clause
survival is local, so the combined objective is exactly the displayed sum.
This constructs a global bilateral assignment and proves the reverse bound.

## Occurrence accounting

Each signature is accompanied by the positive and negative occurrence counts
of its terminals.  A closed exact ((3,2,2)) formula is obtained only when
the composed gadgets supply total terminal counts (2) in each sign, every
internal signed literal already has count (2), every clause has three
distinct variables, and indexed clauses are pairwise distinct.  These are
separate syntactic gates; a favorable min-plus value cannot compensate for a
failed occurrence audit.

## Certificate boundary

`terminal_signature.py` exhaustively enumerates (3^n) local assignments,
emits every finite boundary entry, and retains a witness.  Recomputing the
JSON from the same indexed CNF checks the finite table.  The theorem above is
a universal written proof, not a consequence of trusting the JSON.  For large
gadgets, the same table format can be populated by the general threshold CNF
compiler with proof-logged lower bounds instead of exhaustive enumeration.
