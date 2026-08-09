#!/usr/bin/env python3
"""Generate the connected prism/enforcer family with beta = gap = s."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from bd_core import IndexedCNF, dimacs_text, read_dimacs
from connector_search import exact_322_audit
from terminal_signature import signature_json, terminal_signature


def prism_edges(size: int) -> list[tuple[int, int]]:
    if size < 3:
        raise ValueError("prism size must be at least three")
    edges: list[tuple[int, int]] = []
    for layer in (0, 1):
        offset = layer * size
        for index in range(size):
            left = offset + index
            right = offset + (index + 1) % size
            edges.append(tuple(sorted((left, right))))
    for index in range(size):
        edges.append((index, size + index))
    if len(set(edges)) != 3 * size:
        raise AssertionError("prism edge construction is not simple")
    return edges


def edge_enforcer_amplifier(
    enforcer: IndexedCNF,
    vertex_count: int,
    edges: list[tuple[int, int]],
) -> IndexedCNF:
    """Apply the edge-enforcer construction to a labeled cubic skeleton."""

    if vertex_count <= 0:
        raise ValueError("the skeleton must have at least one vertex")
    normalized_edges = [tuple(sorted(edge)) for edge in edges]
    if any(
        left == right or left < 0 or right >= vertex_count
        for left, right in normalized_edges
    ):
        raise ValueError("skeleton edges must be loopless and in range")
    if len(set(normalized_edges)) != len(normalized_edges):
        raise ValueError("the skeleton must be simple")

    terminal_count = len(edges)
    clauses: list[set[int]] = []
    next_variable = terminal_count + 1

    for terminal, _edge in enumerate(normalized_edges, start=1):
        mapping = {1: terminal}
        for local_variable in range(2, enforcer.variables + 1):
            mapping[local_variable] = next_variable
            next_variable += 1
        for clause in enforcer.clauses:
            clauses.append(
                {
                    (1 if literal > 0 else -1) * mapping[abs(literal)]
                    for literal in clause
                }
            )

    incident: dict[int, list[int]] = defaultdict(list)
    for terminal, (left, right) in enumerate(normalized_edges, start=1):
        incident[left].append(terminal)
        incident[right].append(terminal)
    for vertex in range(vertex_count):
        if len(incident[vertex]) != 3:
            raise ValueError("every skeleton vertex must have degree three")
        clauses.append(set(incident[vertex]))

    return IndexedCNF.from_clauses(next_variable - 1, clauses)


def prism_amplifier(enforcer: IndexedCNF, size: int) -> IndexedCNF:
    return edge_enforcer_amplifier(enforcer, 2 * size, prism_edges(size))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int)
    parser.add_argument("output", type=Path)
    parser.add_argument("--enforcer", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    enforcer = read_dimacs(args.enforcer)
    signature = terminal_signature(enforcer, (1,))
    formula = prism_amplifier(enforcer, args.size)
    audit = exact_322_audit(formula)
    if not all(audit.values()):
        raise AssertionError(f"prism amplifier failed exact audit: {audit}")

    expected_variables = 24 * args.size
    expected_clauses = 32 * args.size
    expected_graph_order = 80 * args.size
    expected_beta = args.size
    if formula.variables != expected_variables:
        raise AssertionError("unexpected prism-amplifier variable count")
    if len(formula.clauses) != expected_clauses:
        raise AssertionError("unexpected prism-amplifier clause count")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = dimacs_text(
        formula,
        f"prism/enforcer connected amplifier s={args.size}; beta={expected_beta}",
    )
    args.output.write_text(rendered, encoding="ascii")
    receipt = {
        "schema": "bilateral-deficiency/prism-enforcer-amplifier/v1",
        "parameter_s": args.size,
        "source_enforcer": args.enforcer.name,
        "source_enforcer_sha256": hashlib.sha256(args.enforcer.read_bytes()).hexdigest(),
        "source_doi": "10.4230/LIPIcs.SAT.2024.31",
        "formula_sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
        "formula_variables": formula.variables,
        "formula_clauses": len(formula.clauses),
        "formula_graph_order": expected_graph_order,
        "audit": audit,
        "beta": expected_beta,
        "minimum_maximal_matching": 24 * args.size,
        "independent_domination": 25 * args.size,
        "gap": expected_beta,
        "gap_density": "1/80",
        "ratio": "25/24",
        "base_prism_vertices": 2 * args.size,
        "base_prism_edges": 3 * args.size,
        "base_prism_matching": args.size,
        "base_prism_edge_cover": args.size,
        "terminal_signature": signature_json(signature, args.enforcer),
        "proof_rule": (
            "terminal min-plus reduction to minimum edge cover of "
            "C_s square K_2; rho=|V|-nu=2s-s=s"
        ),
        "assurance_boundary": (
            "The family theorem is a written universal proof using the finite "
            "enforcer signature. This receipt checks the instantiated syntax, "
            "counts, hashes, and connectivity for the declared s."
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
