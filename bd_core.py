#!/usr/bin/env python3
"""Reference implementation of bilateral deficiency for indexed CNF formulas.

Literals are non-zero signed integers.  A formula is a sequence of clauses;
clauses are normalized to frozensets, while duplicate indexed clauses remain
distinct sequence entries.  An explicit variable count permits absent
variables, as in the theorem's indexed-CNF convention.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Iterable, Iterator, Sequence


UNASSIGNED = -1
FALSE = 0
TRUE = 1
Assignment = tuple[int, ...]
Clause = frozenset[int]


@dataclass(frozen=True)
class IndexedCNF:
    variables: int
    clauses: tuple[Clause, ...]

    @classmethod
    def from_clauses(
        cls, variables: int, clauses: Iterable[Iterable[int]]
    ) -> "IndexedCNF":
        normalized = tuple(frozenset(int(lit) for lit in clause) for clause in clauses)
        if variables < 0:
            raise ValueError("variable count must be non-negative")
        for clause in normalized:
            for literal in clause:
                if literal == 0 or abs(literal) > variables:
                    raise ValueError(f"literal {literal} is outside 1..{variables}")
        return cls(variables, normalized)

    @property
    def maximum_width(self) -> int:
        return max((len(clause) for clause in self.clauses), default=0)


@dataclass(frozen=True)
class Residual:
    """A residual formula, retaining the source indices of surviving clauses."""

    clause_indices: tuple[int, ...]
    clauses: tuple[Clause, ...]
    variables: frozenset[int]


@dataclass(frozen=True)
class BetaResult:
    value: int
    witness: Assignment
    bilateral_count: int
    spectrum: tuple[tuple[int, int], ...]


def _literal_satisfied(literal: int, assignment: Assignment) -> bool:
    value = assignment[abs(literal) - 1]
    return value != UNASSIGNED and (value == TRUE) == (literal > 0)


def _literal_falsified(literal: int, assignment: Assignment) -> bool:
    value = assignment[abs(literal) - 1]
    return value != UNASSIGNED and (value == TRUE) != (literal > 0)


def validate_assignment(formula: IndexedCNF, assignment: Assignment) -> None:
    if len(assignment) != formula.variables:
        raise ValueError("assignment length does not equal the variable count")
    if any(value not in {UNASSIGNED, FALSE, TRUE} for value in assignment):
        raise ValueError("assignment values must be UNASSIGNED, FALSE, or TRUE")


def residual(formula: IndexedCNF, assignment: Assignment) -> Residual:
    """Return F restricted by an assignment, with falsified literals deleted."""

    validate_assignment(formula, assignment)
    indices: list[int] = []
    clauses: list[Clause] = []
    remaining_variables: set[int] = set()
    for index, clause in enumerate(formula.clauses):
        if any(_literal_satisfied(literal, assignment) for literal in clause):
            continue
        reduced = frozenset(
            literal for literal in clause if not _literal_falsified(literal, assignment)
        )
        indices.append(index)
        clauses.append(reduced)
        remaining_variables.update(abs(literal) for literal in reduced)
    return Residual(tuple(indices), tuple(clauses), frozenset(remaining_variables))


def is_bipolar(residual_formula: Residual) -> bool:
    literals = set().union(*residual_formula.clauses) if residual_formula.clauses else set()
    return all(variable in literals and -variable in literals for variable in residual_formula.variables)


def is_bilateral(formula: IndexedCNF, assignment: Assignment) -> bool:
    """Check both residual signs for every explicitly unassigned variable."""

    r = residual(formula, assignment)
    unassigned = {j + 1 for j, value in enumerate(assignment) if value == UNASSIGNED}
    if r.variables != unassigned:
        # Equality also rejects absent unassigned variables, which cannot be bilateral.
        return False
    return is_bipolar(r)


def bilateral_deficiency(formula: IndexedCNF, assignment: Assignment) -> int:
    if not is_bilateral(formula, assignment):
        raise ValueError("assignment is not bilateral")
    r = residual(formula, assignment)
    return len(r.clauses) - len(r.variables)


def partial_assignments(variables: int) -> Iterator[Assignment]:
    yield from product((UNASSIGNED, FALSE, TRUE), repeat=variables)


def complete_assignments(variables: int) -> Iterator[Assignment]:
    yield from product((FALSE, TRUE), repeat=variables)


def beta(formula: IndexedCNF) -> BetaResult:
    best: int | None = None
    witness: Assignment | None = None
    count = 0
    spectrum: Counter[int] = Counter()
    for assignment in partial_assignments(formula.variables):
        if not is_bilateral(formula, assignment):
            continue
        value = bilateral_deficiency(formula, assignment)
        count += 1
        spectrum[value] += 1
        if best is None or value < best:
            best = value
            witness = assignment
    if best is None or witness is None:
        raise AssertionError("complete assignments must make beta well-defined")
    return BetaResult(best, witness, count, tuple(sorted(spectrum.items())))


def maxsat_defect(formula: IndexedCNF) -> int:
    answer = len(formula.clauses)
    for assignment in complete_assignments(formula.variables):
        missed = sum(
            not any(_literal_satisfied(literal, assignment) for literal in clause)
            for clause in formula.clauses
        )
        answer = min(answer, missed)
    return answer


def expected_unsatisfied_clauses(
    formula: IndexedCNF, assignment: Assignment
) -> Fraction:
    """Exact expectation after completing unassigned variables uniformly.

    A surviving non-tautological clause with ``r`` unassigned variables is
    missed with probability ``2**(-r)``.  A tautological clause has zero miss
    probability, including when the variable witnessing the tautology is
    still unassigned.
    """

    validate_assignment(formula, assignment)
    expectation = Fraction(0)
    for clause in formula.clauses:
        if any(_literal_satisfied(literal, assignment) for literal in clause):
            continue

        unassigned_literals = {
            literal
            for literal in clause
            if assignment[abs(literal) - 1] == UNASSIGNED
        }
        if any(-literal in unassigned_literals for literal in unassigned_literals):
            continue

        unassigned_variables = {abs(literal) for literal in unassigned_literals}
        expectation += Fraction(1, 1 << len(unassigned_variables))
    return expectation


def conditional_expectation_complete_assignment(
    formula: IndexedCNF,
) -> tuple[Assignment, int, tuple[Fraction, ...]]:
    """Derandomize a uniform complete assignment by conditional expectations.

    Variables are fixed in index order, with zero chosen on exact ties.  The
    returned trace contains the initial expectation followed by the
    expectation after every deterministic choice.
    """

    assignment = [UNASSIGNED] * formula.variables
    trace = [expected_unsatisfied_clauses(formula, tuple(assignment))]

    for index in range(formula.variables):
        candidates: list[tuple[Fraction, int]] = []
        for value in (FALSE, TRUE):
            assignment[index] = value
            candidates.append(
                (expected_unsatisfied_clauses(formula, tuple(assignment)), value)
            )
        expectation, chosen = min(candidates)
        assignment[index] = chosen
        trace.append(expectation)

    completed = tuple(assignment)
    unsatisfied = len(residual(formula, completed).clauses)
    if trace[-1] != unsatisfied:
        raise AssertionError("complete-assignment expectation must be integral")
    return completed, unsatisfied, tuple(trace)


def formula_graph(formula: IndexedCNF) -> tuple[frozenset[int], ...]:
    """Build G(F); literal vertices are 0..2k-1 and clauses follow them."""

    order = 2 * formula.variables + len(formula.clauses)
    adjacency = [set() for _ in range(order)]
    for j in range(formula.variables):
        negative, positive = 2 * j, 2 * j + 1
        adjacency[negative].add(positive)
        adjacency[positive].add(negative)
    for index, clause in enumerate(formula.clauses):
        clause_vertex = 2 * formula.variables + index
        for literal in clause:
            literal_vertex = 2 * (abs(literal) - 1) + (literal > 0)
            adjacency[clause_vertex].add(literal_vertex)
            adjacency[literal_vertex].add(clause_vertex)
    return tuple(frozenset(neighbours) for neighbours in adjacency)


def assignment_to_ids(formula: IndexedCNF, assignment: Assignment) -> frozenset[int]:
    if not is_bilateral(formula, assignment):
        raise ValueError("assignment is not bilateral")
    selected: set[int] = set()
    for j, value in enumerate(assignment):
        if value != UNASSIGNED:
            selected.add(2 * j + (value == TRUE))
    clause_offset = 2 * formula.variables
    selected.update(clause_offset + index for index in residual(formula, assignment).clause_indices)
    return frozenset(selected)


def ids_to_assignment(formula: IndexedCNF, selected: frozenset[int]) -> Assignment:
    graph = formula_graph(formula)
    if not is_independent_dominating(graph, selected):
        raise ValueError("selected vertices are not an independent dominating set")
    values: list[int] = []
    for j in range(formula.variables):
        negative, positive = 2 * j, 2 * j + 1
        if negative in selected:
            values.append(FALSE)
        elif positive in selected:
            values.append(TRUE)
        else:
            values.append(UNASSIGNED)
    assignment = tuple(values)
    if not is_bilateral(formula, assignment):
        raise AssertionError("the formula-graph inverse did not produce a bilateral assignment")
    return assignment


def is_independent_dominating(
    graph: Sequence[frozenset[int]], selected: frozenset[int]
) -> bool:
    order = len(graph)
    if any(vertex < 0 or vertex >= order for vertex in selected):
        return False
    if any(graph[vertex] & selected for vertex in selected):
        return False
    dominated = set(selected)
    for vertex in selected:
        dominated.update(graph[vertex])
    return len(dominated) == order


def independent_dominating_sets(
    graph: Sequence[frozenset[int]], maximum_order: int = 24
) -> Iterator[frozenset[int]]:
    """Brute-force graph-side enumerator used only for independent small tests."""

    order = len(graph)
    if order > maximum_order:
        raise ValueError(f"graph order {order} exceeds brute-force limit {maximum_order}")
    for mask in range(1 << order):
        selected = frozenset(vertex for vertex in range(order) if mask & (1 << vertex))
        if is_independent_dominating(graph, selected):
            yield selected


def disjoint_union(*formulas: IndexedCNF) -> IndexedCNF:
    clauses: list[Clause] = []
    offset = 0
    for formula in formulas:
        clauses.extend(
            frozenset((1 if literal > 0 else -1) * (abs(literal) + offset) for literal in clause)
            for clause in formula.clauses
        )
        offset += formula.variables
    return IndexedCNF.from_clauses(offset, clauses)


def read_dimacs(path: str | Path) -> IndexedCNF:
    variables: int | None = None
    declared_clauses: int | None = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    for raw_line in Path(path).read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError("invalid DIMACS header")
            variables, declared_clauses = int(fields[2]), int(fields[3])
            continue
        if variables is None:
            raise ValueError("DIMACS clause precedes header")
        for field in line.split():
            literal = int(field)
            if literal == 0:
                clauses.append(pending)
                pending = []
            else:
                pending.append(literal)
    if variables is None or declared_clauses is None:
        raise ValueError("missing DIMACS header")
    if pending:
        raise ValueError("unterminated DIMACS clause")
    if len(clauses) != declared_clauses:
        raise ValueError("declared DIMACS clause count does not match input")
    return IndexedCNF.from_clauses(variables, clauses)


def dimacs_text(formula: IndexedCNF, comment: str | None = None) -> str:
    lines: list[str] = []
    if comment:
        lines.extend(f"c {line}" for line in comment.splitlines())
    lines.append(f"p cnf {formula.variables} {len(formula.clauses)}")
    for clause in formula.clauses:
        body = " ".join(str(literal) for literal in sorted(clause, key=lambda x: (abs(x), x)))
        lines.append(f"{body} 0" if body else "0")
    return "\n".join(lines) + "\n"


def width_lift(formula: IndexedCNF) -> IndexedCNF:
    """Replace each C_a by C_a or y_a and C_a or not-y_a."""

    clauses: list[Clause] = []
    for index, clause in enumerate(formula.clauses):
        fresh = formula.variables + index + 1
        clauses.append(clause | {fresh})
        clauses.append(clause | {-fresh})
    return IndexedCNF.from_clauses(formula.variables + len(formula.clauses), clauses)


def replicate_clauses(formula: IndexedCNF, copies: int) -> IndexedCNF:
    if copies < 1:
        raise ValueError("copies must be positive")
    return IndexedCNF.from_clauses(
        formula.variables,
        (clause for clause in formula.clauses for _ in range(copies)),
    )


def assignment_text(assignment: Assignment) -> str:
    symbols = {UNASSIGNED: "*", FALSE: "0", TRUE: "1"}
    return "".join(symbols[value] for value in assignment)
