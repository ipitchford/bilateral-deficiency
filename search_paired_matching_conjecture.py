#!/usr/bin/env python3
"""Falsification search for the matching-only paired-edge conjecture."""

from __future__ import annotations

import argparse
import json
import random

from bd_core import IndexedCNF, beta
from paired_edge_normal_form import (
    maximum_pair_feasible_matching,
    paired_clause_graph,
)


def random_exact_322(
    variables: int, generator: random.Random, attempts: int = 10_000
) -> IndexedCNF:
    if variables % 3:
        raise ValueError("the number of variables must be divisible by three")
    literals = [
        literal
        for variable in range(1, variables + 1)
        for literal in (variable, variable, -variable, -variable)
    ]
    for _ in range(attempts):
        generator.shuffle(literals)
        clauses = [
            frozenset(literals[index : index + 3])
            for index in range(0, len(literals), 3)
        ]
        if any(len(clause) != 3 for clause in clauses):
            continue
        if any(len({abs(literal) for literal in clause}) != 3 for clause in clauses):
            continue
        if len(set(clauses)) != len(clauses):
            continue
        return IndexedCNF.from_clauses(variables, clauses)
    raise RuntimeError("failed to sample a proper simple exact formula")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variables", type=int, default=6)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260809)
    args = parser.parse_args()
    generator = random.Random(args.seed)

    value_counts: dict[int, int] = {}
    for sample in range(args.samples):
        formula = random_exact_322(args.variables, generator)
        value = beta(formula).value
        graph = paired_clause_graph(formula)
        matching = maximum_pair_feasible_matching(graph)
        matching_value = graph.vertices // 4 - matching
        value_counts[value] = value_counts.get(value, 0) + 1
        if matching_value != value:
            print(
                json.dumps(
                    {
                        "status": "COUNTEREXAMPLE",
                        "sample": sample,
                        "variables": formula.variables,
                        "clauses": [sorted(clause) for clause in formula.clauses],
                        "beta": value,
                        "matching_value": matching_value,
                        "maximum_pair_feasible_matching": matching,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            raise SystemExit(1)

    print(
        json.dumps(
            {
                "status": "NO_COUNTEREXAMPLE_FOUND",
                "assurance_boundary": (
                    "Random finite search is falsification only and does not prove "
                    "the matching-only conjecture."
                ),
                "variables": args.variables,
                "samples": args.samples,
                "seed": args.seed,
                "beta_histogram": value_counts,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
