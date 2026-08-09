#!/usr/bin/env python3
"""Check a compositional benchmark and independently solve each template."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from bd_core import IndexedCNF, beta, disjoint_union, read_dimacs
from generate_benchmark import edge_list_text, recipe, templates


def solve_template(
    formula: IndexedCNF, name: str, exact_solver: Path | None, base: Path
) -> int:
    if formula.variables <= 10:
        return beta(formula).value
    if exact_solver is None:
        raise ValueError(f"template {name} requires --exact-solver")
    paths = {
        "positive-322": base / "instances/txgraffiti_15_20.cnf",
    }
    if name not in paths:
        raise ValueError(f"no DIMACS path registered for large template {name}")
    completed = subprocess.run(
        [str(exact_solver.resolve()), str(paths[name])],
        check=True,
        text=True,
        capture_output=True,
    )
    return int(json.loads(completed.stdout)["beta"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--exact-solver", type=Path)
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    manifest_path = args.directory / "manifest.json"
    cnf_path = args.directory / "benchmark.cnf"
    graph_path = args.directory / "formula_graph.edgelist"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "bilateral-deficiency/compositional-benchmark/v1":
        raise ValueError("unsupported benchmark manifest schema")
    digest = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    if digest != manifest["benchmark_cnf_sha256"]:
        raise ValueError("benchmark CNF hash mismatch")
    graph_digest = hashlib.sha256(graph_path.read_bytes()).hexdigest()
    if graph_digest != manifest["formula_graph_edgelist_sha256"]:
        raise ValueError("formula-graph edge-list hash mismatch")

    family = manifest["family"]
    target = int(manifest["claimed_beta"])
    available = templates(family)
    expected_blocks = recipe(family, target)
    declared_blocks = [(block["template"], int(block["copies"])) for block in manifest["blocks"]]
    if declared_blocks != expected_blocks:
        raise ValueError("manifest block recipe does not match family and target")

    components: list[IndexedCNF] = []
    proved_beta = 0
    template_receipts: dict[str, int] = {}
    for name, copies in declared_blocks:
        formula, declared_beta = available[name]
        actual_beta = solve_template(formula, name, args.exact_solver, base)
        if actual_beta != declared_beta:
            raise ValueError(
                f"template {name} beta mismatch: declared {declared_beta}, solved {actual_beta}"
            )
        template_receipts[name] = actual_beta
        components.extend([formula] * copies)
        proved_beta += copies * actual_beta

    expected_formula = disjoint_union(*components)
    actual_formula = read_dimacs(cnf_path)
    if actual_formula != expected_formula:
        raise ValueError("benchmark is not the declared variable-disjoint block formula")
    expected_graph = edge_list_text(actual_formula).encode("ascii")
    if graph_path.read_bytes() != expected_graph:
        raise ValueError("formula graph is not the deterministic graph of the benchmark CNF")
    if proved_beta != target:
        raise ValueError(f"additive beta {proved_beta} does not equal target {target}")

    result = {
        "status": "COMPOSITIONAL_BENCHMARK_VERIFIED",
        "family": family,
        "beta": proved_beta,
        "template_receipts": template_receipts,
        "variables": actual_formula.variables,
        "indexed_clauses": len(actual_formula.clauses),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
