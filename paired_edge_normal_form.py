#!/usr/bin/env python3
"""Paired-edge normal form for proper simple exact (3,2,2)-CNF."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from bd_core import (
    FALSE,
    TRUE,
    UNASSIGNED,
    Assignment,
    IndexedCNF,
    is_bilateral,
    read_dimacs,
    residual,
)


@dataclass(frozen=True)
class SignedClauseEdge:
    variable: int
    positive: bool
    endpoints: tuple[int, int]


@dataclass(frozen=True)
class PairedClauseGraph:
    vertices: int
    pairs: tuple[tuple[SignedClauseEdge, SignedClauseEdge], ...]

    @property
    def edges(self) -> tuple[SignedClauseEdge, ...]:
        return tuple(edge for pair in self.pairs for edge in pair)


def paired_clause_graph(formula: IndexedCNF) -> PairedClauseGraph:
    """Construct the cubic clause multigraph and its signed edge pairs."""

    if any(len(clause) != 3 for clause in formula.clauses):
        raise ValueError("every clause must have exactly three distinct literals")
    if any(
        any(-literal in clause for literal in clause) for clause in formula.clauses
    ):
        raise ValueError("tautological clauses are not proper")
    if len(set(formula.clauses)) != len(formula.clauses):
        raise ValueError("indexed clauses must be pairwise distinct")

    occurrences: dict[int, list[int]] = {
        literal: []
        for variable in range(1, formula.variables + 1)
        for literal in (variable, -variable)
    }
    for clause_index, clause in enumerate(formula.clauses):
        for literal in clause:
            occurrences[literal].append(clause_index)

    pairs: list[tuple[SignedClauseEdge, SignedClauseEdge]] = []
    for variable in range(1, formula.variables + 1):
        positive_occurrences = occurrences[variable]
        negative_occurrences = occurrences[-variable]
        if len(positive_occurrences) != 2 or len(negative_occurrences) != 2:
            raise ValueError("every signed literal must occur exactly twice")
        positive = SignedClauseEdge(
            variable, True, tuple(sorted(positive_occurrences))
        )
        negative = SignedClauseEdge(
            variable, False, tuple(sorted(negative_occurrences))
        )
        if set(positive.endpoints) & set(negative.endpoints):
            raise ValueError("opposite signed edges must be vertex-disjoint")
        pairs.append((positive, negative))

    degree = [0] * len(formula.clauses)
    for edge in (edge for pair in pairs for edge in pair):
        left, right = edge.endpoints
        if left == right:
            raise ValueError("a signed edge must join two distinct clauses")
        degree[left] += 1
        degree[right] += 1
    if any(value != 3 for value in degree):
        raise AssertionError("the clause multigraph is not cubic")
    return PairedClauseGraph(len(formula.clauses), tuple(pairs))


def selection_from_assignment(
    graph: PairedClauseGraph, assignment: Assignment
) -> frozenset[SignedClauseEdge]:
    if len(assignment) != len(graph.pairs):
        raise ValueError("assignment length does not match the edge pairing")
    selected: set[SignedClauseEdge] = set()
    for value, (positive, negative) in zip(assignment, graph.pairs, strict=True):
        if value == TRUE:
            selected.add(positive)
        elif value == FALSE:
            selected.add(negative)
        elif value != UNASSIGNED:
            raise ValueError("assignment entries must be 0, 1, or -1")
    return frozenset(selected)


def covered_vertices(selection: frozenset[SignedClauseEdge]) -> frozenset[int]:
    return frozenset(
        endpoint for edge in selection for endpoint in edge.endpoints
    )


def is_pair_feasible(
    graph: PairedClauseGraph, selection: frozenset[SignedClauseEdge]
) -> bool:
    covered = covered_vertices(selection)
    selected_by_variable: dict[int, int] = {}
    graph_edges = set(graph.edges)
    if not selection <= graph_edges:
        return False
    for edge in selection:
        selected_by_variable[edge.variable] = (
            selected_by_variable.get(edge.variable, 0) + 1
        )
    if any(count > 1 for count in selected_by_variable.values()):
        return False
    for positive, negative in graph.pairs:
        if positive.variable in selected_by_variable:
            continue
        if set(positive.endpoints) <= covered:
            return False
        if set(negative.endpoints) <= covered:
            return False
    return True


def pair_surplus(selection: frozenset[SignedClauseEdge]) -> int:
    return len(covered_vertices(selection)) - len(selection)


def deficiency_from_selection(
    graph: PairedClauseGraph, selection: frozenset[SignedClauseEdge]
) -> int:
    if not is_pair_feasible(graph, selection):
        raise ValueError("edge selection is not pair-feasible")
    if graph.vertices % 4:
        raise AssertionError("an exact (3,2,2) formula has a multiple of four clauses")
    return graph.vertices // 4 - pair_surplus(selection)


def maximum_pair_feasible_matching(graph: PairedClauseGraph) -> int:
    """Exact backtracking benchmark for the matching-restricted subproblem."""

    edges = graph.edges
    best = 0

    def search(
        index: int,
        selected: frozenset[SignedClauseEdge],
        used_vertices: frozenset[int],
        used_variables: frozenset[int],
    ) -> None:
        nonlocal best
        if len(selected) + min(
            (graph.vertices - len(used_vertices)) // 2,
            len(graph.pairs) - len(used_variables),
        ) <= best:
            return
        if index == len(edges):
            if is_pair_feasible(graph, selected):
                best = max(best, len(selected))
            return
        edge = edges[index]
        search(index + 1, selected, used_vertices, used_variables)
        endpoints = frozenset(edge.endpoints)
        if edge.variable not in used_variables and not endpoints & used_vertices:
            search(
                index + 1,
                selected | {edge},
                used_vertices | endpoints,
                used_variables | {edge.variable},
            )

    search(0, frozenset(), frozenset(), frozenset())
    return best


def audit_assignment_identity(formula: IndexedCNF, assignment: Assignment) -> None:
    graph = paired_clause_graph(formula)
    selection = selection_from_assignment(graph, assignment)
    if is_bilateral(formula, assignment) != is_pair_feasible(graph, selection):
        raise AssertionError("bilaterality and pair-feasibility disagree")
    if is_bilateral(formula, assignment):
        direct = len(residual(formula, assignment).clauses) - assignment.count(
            UNASSIGNED
        )
        if direct != deficiency_from_selection(graph, selection):
            raise AssertionError("CNF and paired-edge objectives disagree")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--matching-benchmark", action="store_true")
    args = parser.parse_args()
    formula = read_dimacs(args.input)
    graph = paired_clause_graph(formula)
    result: dict[str, object] = {
        "clauses": graph.vertices,
        "variables": len(graph.pairs),
        "paired_edges": len(graph.edges),
        "cubic_degree_sum": 2 * len(graph.edges),
    }
    if args.matching_benchmark:
        result["maximum_pair_feasible_matching"] = maximum_pair_feasible_matching(
            graph
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
