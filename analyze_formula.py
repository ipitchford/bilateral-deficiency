#!/usr/bin/env python3
"""Classify a CNF instance and recommend exact bilateral-deficiency algorithms."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path

from bd_core import IndexedCNF, beta, formula_graph, read_dimacs


def incidence_is_forest(formula: IndexedCNF) -> bool:
    nodes = formula.variables + len(formula.clauses)
    parent = list(range(nodes))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(left: int, right: int) -> bool:
        left, right = find(left), find(right)
        if left == right:
            return False
        parent[right] = left
        return True

    for index, clause in enumerate(formula.clauses):
        clause_node = formula.variables + index
        for variable in {abs(literal) - 1 for literal in clause}:
            if not union(variable, clause_node):
                return False
    return True


def regular_dim_signature(formula: IndexedCNF) -> int | None:
    widths = {len(clause) for clause in formula.clauses}
    if len(widths) != 1:
        return None
    degree = next(iter(widths), 0)
    if degree < 1:
        return None
    occurrences = Counter(literal for clause in formula.clauses for literal in clause)
    if any(
        occurrences[sign * variable] != degree - 1
        for variable in range(1, formula.variables + 1)
        for sign in (-1, 1)
    ):
        return None
    graph = formula_graph(formula)
    if any(len(neighbours) != degree for neighbours in graph):
        raise AssertionError("regular-DIM syntactic signature did not produce a regular graph")
    return degree


def solve(formula: IndexedCNF, path: Path, exact_solver: Path | None) -> tuple[int, str]:
    if formula.variables <= 10:
        return beta(formula).value, "python-reference-ternary-enumeration"
    if exact_solver is None:
        raise ValueError("solving more than 10 variables requires --exact-solver")
    completed = subprocess.run(
        [str(exact_solver.resolve()), str(path.resolve())],
        check=True,
        text=True,
        capture_output=True,
    )
    return int(json.loads(completed.stdout)["beta"]), "cpp-exhaustive-ternary-receipt"


def analyze(formula: IndexedCNF) -> dict[str, object]:
    maximum_width = formula.maximum_width
    incidence_forest = incidence_is_forest(formula)
    dim_degree = regular_dim_signature(formula)
    recommendations: list[dict[str, str]] = []

    if maximum_width <= 2:
        recommendations.append(
            {
                "method": "MaxSAT or Almost-2-SAT",
                "reason": "the width-two theorem gives beta(F)=minimum falsified clauses",
            }
        )
    if incidence_forest:
        recommendations.append(
            {
                "method": "bounded-treewidth dynamic programming",
                "reason": "the incidence graph is a forest (treewidth at most 1)",
            }
        )
    if formula.variables <= 20:
        recommendations.append(
            {
                "method": "exact ternary enumeration",
                "reason": f"the complete search has 3^{formula.variables} partial assignments",
            }
        )
    recommendations.append(
        {
            "method": "formula-graph independent-domination branch-and-reduce",
            "reason": "the size-preserving bijection gives i(G(F))=k+beta(F)",
        }
    )
    if maximum_width >= 3:
        recommendations.append(
            {
                "method": "general SAT/MILP/branch-and-bound with proof logging",
                "reason": "the sign problem is NP-hard already for exact width three",
            }
        )

    return {
        "variables": formula.variables,
        "indexed_clauses": len(formula.clauses),
        "maximum_width": maximum_width,
        "incidence_graph_is_forest": incidence_forest,
        "regular_dim_degree": dim_degree,
        "formula_graph_order": 2 * formula.variables + len(formula.clauses),
        "recommendations": recommendations,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("formula", type=Path)
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--exact-solver", type=Path)
    args = parser.parse_args()

    formula = read_dimacs(args.formula)
    report = analyze(formula)
    if args.solve:
        value, method = solve(formula, args.formula, args.exact_solver)
        report["beta"] = value
        report["solver_used"] = method
        degree = report["regular_dim_degree"]
        if degree is not None:
            k = formula.variables
            report["regular_dim_classification"] = {
                "degree": degree,
                "mu_star": k,
                "independent_domination": k + value,
                "gap_i_minus_mu_star": value,
                "violates_i_le_mu_star": value > 0,
            }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
