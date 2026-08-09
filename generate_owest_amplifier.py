#!/usr/bin/env python3
"""Generate O--West extremal skeletons and their connected BD amplifiers."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path

from bd_core import dimacs_text, read_dimacs
from connector_search import exact_322_audit
from generate_prism_amplifier import edge_enforcer_amplifier


OWEST_DOI = "10.1002/jgt.20443"


def canonical_t1_tree(expansions: int) -> tuple[int, list[tuple[int, int]], set[int]]:
    """Return the canonical member of T_1 after ``expansions`` leaf expansions."""

    if expansions < 0:
        raise ValueError("the expansion count must be nonnegative")
    edges = [(0, 1), (0, 2), (0, 3)]
    leaves = {1, 2, 3}
    next_vertex = 4

    for _ in range(expansions):
        leaf = min(leaves)
        leaves.remove(leaf)
        for _branch in range(2):
            branch = next_vertex
            next_vertex += 1
            edges.append((leaf, branch))
            for _child in range(2):
                child = next_vertex
                next_vertex += 1
                edges.append((branch, child))
                leaves.add(child)
    return next_vertex, edges, leaves


def balloon_b1_edges() -> list[tuple[int, int]]:
    """The five-vertex cubic balloon B_1, with vertex zero as its neck."""

    deleted = {(0, 1), (0, 4), (2, 3)}
    return [
        (left, right)
        for left in range(5)
        for right in range(left + 1, 5)
        if (left, right) not in deleted
    ]


def owest_h1_skeleton(expansions: int) -> tuple[int, list[tuple[int, int]]]:
    """Construct the canonical cubic O--West H_1 skeleton."""

    tree_order, tree_edges, leaves = canonical_t1_tree(expansions)
    edges = list(tree_edges)
    next_vertex = tree_order
    for leaf in sorted(leaves):
        mapping = {0: leaf}
        for local in range(1, 5):
            mapping[local] = next_vertex
            next_vertex += 1
        edges.extend(
            (mapping[left], mapping[right]) for left, right in balloon_b1_edges()
        )
    return next_vertex, [tuple(sorted(edge)) for edge in edges]


def audit_cubic_skeleton(
    vertex_count: int, edges: list[tuple[int, int]]
) -> dict[str, object]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    normalized = [tuple(sorted(edge)) for edge in edges]
    simple = len(normalized) == len(set(normalized)) and all(
        left != right and left >= 0 and right < vertex_count
        for left, right in normalized
    )
    for left, right in normalized:
        adjacency[left].add(right)
        adjacency[right].add(left)
    cubic = all(len(adjacency[vertex]) == 3 for vertex in range(vertex_count))
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    return {
        "simple": simple,
        "cubic": cubic,
        "connected": len(reached) == vertex_count,
        "edge_count": len(edges),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("expansions", type=int)
    parser.add_argument("output", type=Path)
    parser.add_argument("--enforcer", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()

    enforcer = read_dimacs(args.enforcer)
    skeleton_order, skeleton_edges = owest_h1_skeleton(args.expansions)
    skeleton_audit = audit_cubic_skeleton(skeleton_order, skeleton_edges)
    if not all(
        skeleton_audit[key] for key in ("simple", "cubic", "connected")
    ):
        raise AssertionError(f"O--West skeleton audit failed: {skeleton_audit}")

    formula = edge_enforcer_amplifier(enforcer, skeleton_order, skeleton_edges)
    formula_audit = exact_322_audit(formula)
    if not all(formula_audit.values()):
        raise AssertionError(f"amplifier exact audit failed: {formula_audit}")

    expected_order = 16 + 18 * args.expansions
    matching_number = (4 * expected_order - 1) // 9
    edge_cover = expected_order - matching_number
    if skeleton_order != expected_order:
        raise AssertionError("unexpected O--West skeleton order")
    if 9 * matching_number != 4 * expected_order - 1:
        raise AssertionError("O--West matching formula is nonintegral")

    rendered = dimacs_text(
        formula,
        (
            f"O--West H_1/enforcer amplifier expansions={args.expansions}; "
            f"beta={edge_cover}"
        ),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="ascii")

    graph_order = 40 * skeleton_order
    minimum_maximal_matching = 12 * skeleton_order
    independent_domination = minimum_maximal_matching + edge_cover
    receipt = {
        "schema": "bilateral-deficiency/owest-enforcer-amplifier/v1",
        "canonical_expansions": args.expansions,
        "owest_source_doi": OWEST_DOI,
        "skeleton_order": skeleton_order,
        "skeleton_edges": len(skeleton_edges),
        "skeleton_audit": skeleton_audit,
        "skeleton_matching_number": matching_number,
        "skeleton_edge_cover": edge_cover,
        "matching_value_boundary": (
            "The matching number is theorem-derived from the O--West H_1 "
            "family; the generator audits structure but does not implement blossom."
        ),
        "source_enforcer": args.enforcer.name,
        "source_enforcer_sha256": hashlib.sha256(args.enforcer.read_bytes()).hexdigest(),
        "formula_sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
        "formula_variables": formula.variables,
        "formula_clauses": len(formula.clauses),
        "formula_audit": formula_audit,
        "beta": edge_cover,
        "formula_graph_order": graph_order,
        "minimum_maximal_matching": minimum_maximal_matching,
        "independent_domination": independent_domination,
        "gap": edge_cover,
        "gap_density": str(Fraction(edge_cover, graph_order)),
        "ratio": str(Fraction(independent_domination, minimum_maximal_matching)),
        "assurance_boundary": (
            "The edge-cover amplifier is a written universal proof and the "
            "matching formula is a cited theorem. This receipt checks the "
            "declared finite syntax, counts, hashes, and connectivity."
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
