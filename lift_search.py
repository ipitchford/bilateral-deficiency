#!/usr/bin/env python3
"""Search connected two-lifts of an exact (3,2,2) formula for positive gap."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from itertools import combinations
from pathlib import Path

from bd_core import (
    IndexedCNF,
    assignment_text,
    bilateral_deficiency,
    dimacs_text,
    is_bilateral,
    read_dimacs,
)
from connector_search import (
    decode_assignment,
    decode_graph_assignment,
    encoding_for_threshold,
    exact_322_audit,
    run_cadical,
)


def ordered_incidence_count(formula: IndexedCNF) -> int:
    return sum(len(clause) for clause in formula.clauses)


def two_lift(formula: IndexedCNF, crossed: frozenset[int]) -> IndexedCNF:
    incidence = 0
    lifted_clauses: list[set[int]] = []
    clause_literals = [
        sorted(clause, key=lambda literal: (abs(literal), literal))
        for clause in formula.clauses
    ]
    incidence_indices: list[list[int]] = []
    for literals in clause_literals:
        indices = list(range(incidence, incidence + len(literals)))
        incidence_indices.append(indices)
        incidence += len(literals)

    for layer in (0, 1):
        for literals, indices in zip(clause_literals, incidence_indices):
            lifted: set[int] = set()
            for literal, index in zip(literals, indices):
                target_layer = layer ^ (index in crossed)
                variable = abs(literal) + target_layer * formula.variables
                lifted.add((1 if literal > 0 else -1) * variable)
            lifted_clauses.append(lifted)
    return IndexedCNF.from_clauses(2 * formula.variables, lifted_clauses)


def candidate_masks(
    incidence_count: int,
    exhaustive_weight: int,
    random_weight: int,
    samples: int,
    seed: int,
):
    for weight in range(1, exhaustive_weight + 1):
        for chosen in combinations(range(incidence_count), weight):
            yield frozenset(chosen)
    generator = random.Random(seed)
    seen: set[frozenset[int]] = set()
    for _ in range(samples):
        chosen = frozenset(generator.sample(range(incidence_count), random_weight))
        if chosen in seen:
            continue
        seen.add(chosen)
        yield chosen


def write_lift_candidate(
    output_dir: Path,
    formula: IndexedCNF,
    crossed: frozenset[int],
    threshold: int,
    compiler: str,
    tested: int,
    elapsed: float,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    formula_path = output_dir / "connected-two-lift.cnf"
    formula_path.write_text(
        dimacs_text(formula, "connected exact (3,2,2) two-lift"),
        encoding="ascii",
    )
    lower_text, lower_map = encoding_for_threshold(
        formula_path, threshold, compiler=compiler
    )
    lower_path = output_dir / f"beta-le-{threshold}-{compiler}.cnf"
    lower_path.write_text(lower_text, encoding="ascii")
    (output_dir / f"beta-le-{threshold}-{compiler}-map.json").write_text(
        json.dumps(lower_map, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    upper_threshold = threshold + 1
    upper_text, upper_map = encoding_for_threshold(
        formula_path, upper_threshold, compiler=compiler
    )
    upper_path = output_dir / f"beta-le-{upper_threshold}-{compiler}.cnf"
    upper_path.write_text(upper_text, encoding="ascii")
    upper_result = run_cadical(upper_path, quiet=False)
    if upper_result.returncode != 10:
        raise RuntimeError(
            f"expected beta <= {upper_threshold} SAT, got {upper_result.returncode}"
        )
    assignment = (
        decode_assignment(upper_result.stdout, upper_map, formula.variables)
        if compiler == "formula"
        else decode_graph_assignment(upper_result.stdout, upper_map, formula)
    )
    if not is_bilateral(formula, assignment):
        raise AssertionError("decoded lift witness is not bilateral")
    deficiency = bilateral_deficiency(formula, assignment)
    if deficiency > upper_threshold:
        raise AssertionError("decoded lift witness exceeds the upper threshold")

    receipt = {
        "schema": "bilateral-deficiency/two-lift-search/v1",
        "formula_sha256": hashlib.sha256(formula_path.read_bytes()).hexdigest(),
        "variables": formula.variables,
        "clauses": len(formula.clauses),
        "crossed_incidence_indices_zero_based": sorted(crossed),
        "crossed_incidence_count": len(crossed),
        "audit": exact_322_audit(formula),
        "compiler": compiler,
        "lower_threshold": threshold,
        "lower_solver_status": "UNSAT",
        "lower_encoding_sha256": lower_map["encoding_sha256"],
        "upper_threshold": upper_threshold,
        "upper_solver_status": "SAT",
        "upper_encoding_sha256": upper_map["encoding_sha256"],
        "upper_witness": assignment_text(assignment),
        "upper_witness_deficiency": deficiency,
        "masks_tested": tested,
        "elapsed_seconds": round(elapsed, 6),
        "assurance_boundary": (
            "The upper witness is independently checked. The lower solver "
            "status remains provisional until its proof log is checked."
        ),
    }
    (output_dir / "search-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--lower-threshold", type=int, default=1)
    parser.add_argument("--compiler", choices=("formula", "graph"), default="graph")
    parser.add_argument("--exhaustive-weight", type=int, default=0)
    parser.add_argument("--random-weight", type=int, default=12)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=322)
    args = parser.parse_args()

    base = read_dimacs(args.base)
    incidence_count = ordered_incidence_count(base)
    tested = 0
    started = time.monotonic()
    for crossed in candidate_masks(
        incidence_count,
        args.exhaustive_weight,
        args.random_weight,
        args.samples,
        args.seed,
    ):
        formula = two_lift(base, crossed)
        audit = exact_322_audit(formula)
        if not all(audit.values()):
            continue
        tested += 1
        temporary_formula = args.output_dir.parent / ".two-lift-candidate.cnf"
        temporary_encoding = args.output_dir.parent / ".two-lift-threshold.cnf"
        temporary_formula.write_text(dimacs_text(formula), encoding="ascii")
        encoding, _ = encoding_for_threshold(
            temporary_formula, args.lower_threshold, compiler=args.compiler
        )
        temporary_encoding.write_text(encoding, encoding="ascii")
        result = run_cadical(temporary_encoding)
        temporary_formula.unlink(missing_ok=True)
        temporary_encoding.unlink(missing_ok=True)
        if result.returncode == 20:
            receipt = write_lift_candidate(
                args.output_dir,
                formula,
                crossed,
                args.lower_threshold,
                args.compiler,
                tested,
                time.monotonic() - started,
            )
            print(json.dumps(receipt, indent=2, sort_keys=True))
            return
        if result.returncode != 10:
            raise RuntimeError(f"CaDiCaL failed with exit {result.returncode}")
    print(json.dumps({"status": "NO_CANDIDATE", "tested": tested}))


if __name__ == "__main__":
    main()
