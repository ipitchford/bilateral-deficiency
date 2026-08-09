#!/usr/bin/env python3
"""Generate controlled bilateral-deficiency benchmark families."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from bd_core import IndexedCNF, dimacs_text, disjoint_union, formula_graph, read_dimacs


BASE = Path(__file__).resolve().parent


def templates(family: str) -> dict[str, tuple[IndexedCNF, int]]:
    if family == "general":
        return {
            "positive-unit": (IndexedCNF.from_clauses(1, [(1,), (-1,)]), 1),
            "negative-unit": (
                IndexedCNF.from_clauses(3, [(1, 2, 3), (-1, -2, -3)]),
                -1,
            ),
            "zero-unit": (IndexedCNF.from_clauses(1, [(1,)]), 0),
        }
    if family == "exact-322":
        return {
            "positive-322": (read_dimacs(BASE / "instances/txgraffiti_15_20.cnf"), 1),
            "negative-322": (read_dimacs(BASE / "instances/negative_322.cnf"), -1),
        }
    raise ValueError(f"unknown family: {family}")


def recipe(family: str, target: int) -> list[tuple[str, int]]:
    if family == "general":
        if target > 0:
            return [("positive-unit", target)]
        if target < 0:
            return [("negative-unit", -target)]
        return [("zero-unit", 1)]
    if target > 0:
        return [("positive-322", target)]
    if target < 0:
        return [("negative-322", -target)]
    # A nonempty exact-(3,2,2) zero instance demonstrates sign cancellation.
    return [("positive-322", 1), ("negative-322", 1)]


def edge_list_text(formula: IndexedCNF) -> str:
    graph = formula_graph(formula)
    lines = [f"{u} {v}" for u, neighbours in enumerate(graph) for v in neighbours if u < v]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("general", "exact-322"), required=True)
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    available = templates(args.family)
    blocks = recipe(args.family, args.target)
    components: list[IndexedCNF] = []
    for name, copies in blocks:
        components.extend([available[name][0]] * copies)
    formula = disjoint_union(*components)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cnf_path = args.output_dir / "benchmark.cnf"
    graph_path = args.output_dir / "formula_graph.edgelist"
    manifest_path = args.output_dir / "manifest.json"
    cnf = dimacs_text(
        formula,
        f"controlled bilateral-deficiency benchmark; family={args.family}; target={args.target}",
    )
    cnf_path.write_text(cnf, encoding="ascii")
    graph_path.write_text(edge_list_text(formula), encoding="ascii")

    manifest = {
        "schema": "bilateral-deficiency/compositional-benchmark/v1",
        "family": args.family,
        "claimed_beta": args.target,
        "variables": formula.variables,
        "indexed_clauses": len(formula.clauses),
        "formula_graph_order": len(formula_graph(formula)),
        "blocks": [
            {
                "template": name,
                "copies": copies,
                "component_variables": available[name][0].variables,
                "component_clauses": len(available[name][0].clauses),
                "claimed_component_beta": available[name][1],
            }
            for name, copies in blocks
        ],
        "benchmark_cnf_sha256": hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
        "formula_graph_edgelist_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "proof_rule": "variable-disjoint additivity of bilateral deficiency",
        "graph_consequence": (
            "for exact-322, the formula graph is cubic with a dominating induced matching, "
            "mu_star=k and i=k+beta"
            if args.family == "exact-322"
            else "i(G(F))=k+beta(F)"
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
