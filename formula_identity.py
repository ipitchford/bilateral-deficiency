#!/usr/bin/env python3
"""Canonical formula-graph identity audit using nauty's labelg."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from bd_core import IndexedCNF, formula_graph, read_dimacs


def nauty_tool(name: str) -> str:
    """Resolve upstream and Debian/Ubuntu names for a nauty executable."""
    for candidate in (name, f"nauty-{name}"):
        executable = shutil.which(candidate)
        if executable is not None:
            return executable
    raise RuntimeError(
        f"nauty executable {name!r} was not found; install nauty and ensure "
        f"either {name!r} or 'nauty-{name}' is on PATH"
    )


def adjacency_matrix_text(formula: IndexedCNF) -> str:
    graph = formula_graph(formula)
    rows = [
        "".join("1" if column in graph[row] else "0" for column in range(len(graph)))
        for row in range(len(graph))
    ]
    return f"n={len(graph)}\nm\n" + "\n".join(rows) + "\nq\n"


def canonical_graph6(formula: IndexedCNF, colored: bool) -> str:
    with tempfile.TemporaryDirectory(prefix="bd-identity-") as temporary:
        temporary_path = Path(temporary)
        matrix = temporary_path / "graph.matrix"
        graph6 = temporary_path / "graph.g6"
        canonical = temporary_path / "canonical.g6"
        matrix.write_text(adjacency_matrix_text(formula), encoding="ascii")
        converted = subprocess.run(
            [nauty_tool("amtog"), "-q", str(matrix), str(graph6)],
            text=True,
            capture_output=True,
            check=False,
        )
        if converted.returncode != 0:
            raise RuntimeError(converted.stderr)
        command = [nauty_tool("labelg"), "-q"]
        if colored:
            colors = "a" * (2 * formula.variables) + "b" * len(formula.clauses)
            command.append(f"-f{colors}")
        command.extend([str(graph6), str(canonical)])
        labeled = subprocess.run(
            command, text=True, capture_output=True, check=False
        )
        if labeled.returncode != 0:
            raise RuntimeError(labeled.stderr)
        return canonical.read_text(encoding="ascii").strip()


def identity_audit(left_path: Path, right_path: Path) -> dict[str, object]:
    left = read_dimacs(left_path)
    right = read_dimacs(right_path)
    same_order = (
        left.variables == right.variables and len(left.clauses) == len(right.clauses)
    )
    if same_order:
        left_plain = canonical_graph6(left, colored=False)
        right_plain = canonical_graph6(right, colored=False)
        left_colored = canonical_graph6(left, colored=True)
        right_colored = canonical_graph6(right, colored=True)
        plain_isomorphic = left_plain == right_plain
        formula_isomorphic = left_colored == right_colored
    else:
        left_plain = right_plain = left_colored = right_colored = ""
        plain_isomorphic = formula_isomorphic = False
    return {
        "schema": "bilateral-deficiency/formula-identity-audit/v1",
        "left": left_path.name,
        "left_sha256": hashlib.sha256(left_path.read_bytes()).hexdigest(),
        "right": right_path.name,
        "right_sha256": hashlib.sha256(right_path.read_bytes()).hexdigest(),
        "same_formula_dimensions": same_order,
        "plain_formula_graph_isomorphic": plain_isomorphic,
        "colored_formula_graph_isomorphic": formula_isomorphic,
        "left_plain_canonical_sha256": hashlib.sha256(
            left_plain.encode("ascii")
        ).hexdigest(),
        "right_plain_canonical_sha256": hashlib.sha256(
            right_plain.encode("ascii")
        ).hexdigest(),
        "left_colored_canonical_sha256": hashlib.sha256(
            left_colored.encode("ascii")
        ).hexdigest(),
        "right_colored_canonical_sha256": hashlib.sha256(
            right_colored.encode("ascii")
        ).hexdigest(),
        "colored_equivalence": (
            "variable renaming, independent variable sign switches, and indexed "
            "clause permutation"
        ),
        "assurance_boundary": (
            "Canonical labels establish graph/formula isomorphism relative to "
            "the declared coloring. They do not establish historical priority."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = identity_audit(args.left, args.right)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
