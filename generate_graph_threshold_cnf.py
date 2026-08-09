#!/usr/bin/env python3
"""Compile beta(F) <= q through independent domination of the formula graph."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from bd_core import formula_graph, read_dimacs
from generate_positive_base_cnf import CnfBuilder


def add_contradiction(builder: CnfBuilder) -> None:
    witness = builder.variable("contradiction")
    builder.add(witness)
    builder.add(-witness)


def add_at_most_k(
    builder: CnfBuilder, variables: list[int], bound: int
) -> dict[tuple[int, int], int]:
    """Sinz sequential-counter encoding of sum(variables) <= bound."""

    if bound < 0:
        add_contradiction(builder)
        return {}
    if bound >= len(variables):
        return {}
    if bound == 0:
        for variable in variables:
            builder.add(-variable)
        return {}

    sequential: dict[tuple[int, int], int] = {}
    for index in range(1, len(variables)):
        for count in range(1, bound + 1):
            sequential[index, count] = builder.variable(
                f"sequential[{index},{count}]"
            )

    first = variables[0]
    builder.add(-first, sequential[1, 1])
    for count in range(2, bound + 1):
        builder.add(-sequential[1, count])

    for index in range(2, len(variables)):
        current = variables[index - 1]
        builder.add(-current, sequential[index, 1])
        builder.add(-sequential[index - 1, 1], sequential[index, 1])
        for count in range(2, bound + 1):
            builder.add(
                -current,
                -sequential[index - 1, count - 1],
                sequential[index, count],
            )
            builder.add(
                -sequential[index - 1, count], sequential[index, count]
            )
        builder.add(-current, -sequential[index - 1, bound])

    builder.add(-variables[-1], -sequential[len(variables) - 1, bound])
    return sequential


def build_graph_threshold_encoding(
    formula_path: Path, threshold: int
) -> tuple[CnfBuilder, dict[str, object]]:
    formula = read_dimacs(formula_path)
    graph = formula_graph(formula)
    builder = CnfBuilder()
    selected = [
        builder.variable(f"selected[{vertex}]") for vertex in range(len(graph))
    ]

    for vertex, neighbours in enumerate(graph):
        for neighbour in neighbours:
            if vertex < neighbour:
                builder.add(-selected[vertex], -selected[neighbour])
    for vertex, neighbours in enumerate(graph):
        builder.add(selected[vertex], *(selected[n] for n in sorted(neighbours)))

    independent_domination_bound = formula.variables + threshold
    sequential = add_at_most_k(
        builder, selected, independent_domination_bound
    )
    metadata: dict[str, object] = {
        "claim": f"beta(F) <= {threshold}",
        "threshold": threshold,
        "formula_variables": formula.variables,
        "formula_clauses": len(formula.clauses),
        "formula_graph_vertices": len(graph),
        "independent_domination_bound": independent_domination_bound,
        "selected": {str(vertex): variable for vertex, variable in enumerate(selected)},
        "sequential": {
            f"{index},{count}": variable
            for (index, count), variable in sequential.items()
        },
        "encoding_variable_count": builder.next_variable - 1,
        "encoding_clause_count": len(builder.clauses),
    }
    return builder, metadata


def render_graph_encoding(
    builder: CnfBuilder,
    formula_path: Path,
    threshold: int,
    input_sha256: str,
) -> str:
    lines = [
        f"c beta(F) <= {threshold} via independent domination of G(F)",
        f"c input {formula_path.name}",
        f"c input_sha256 {input_sha256}",
        f"p cnf {builder.next_variable - 1} {len(builder.clauses)}",
    ]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in builder.clauses)
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("--threshold", type=int, required=True)
    args = parser.parse_args()

    builder, metadata = build_graph_threshold_encoding(args.input, args.threshold)
    input_sha256 = hashlib.sha256(args.input.read_bytes()).hexdigest()
    rendered = render_graph_encoding(
        builder, args.input, args.threshold, input_sha256
    )
    metadata["input"] = args.input.name
    metadata["input_sha256"] = input_sha256
    metadata["encoding_sha256"] = hashlib.sha256(
        rendered.encode("utf-8")
    ).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.map_path.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="ascii")
    args.map_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(args.output),
                "map": str(args.map_path),
                "variables": builder.next_variable - 1,
                "clauses": len(builder.clauses),
                "encoding_sha256": metadata["encoding_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
