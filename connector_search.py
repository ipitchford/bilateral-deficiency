#!/usr/bin/env python3
"""Search occurrence-preserving 2-switches for connected positive formulas.

The search joins two exact (3,2,2) formulas by swapping one literal incidence
from a clause in each component.  It preserves every signed occurrence count.
Candidate lower bounds are decided by the general beta-threshold compiler and
CaDiCaL; any retained UNSAT result can subsequently be proof-logged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from collections import Counter, deque
from pathlib import Path

from bd_core import (
    FALSE,
    TRUE,
    Assignment,
    IndexedCNF,
    assignment_text,
    bilateral_deficiency,
    dimacs_text,
    disjoint_union,
    formula_graph,
    ids_to_assignment,
    is_bilateral,
    read_dimacs,
)
from generate_positive_base_cnf import (
    build_beta_nonpositive_encoding,
    read_dimacs as read_encoding_dimacs,
    render_dimacs,
)
from generate_graph_threshold_cnf import (
    build_graph_threshold_encoding,
    render_graph_encoding,
)


def shift_literal(literal: int, offset: int) -> int:
    return (1 if literal > 0 else -1) * (abs(literal) + offset)


def occurrence_switch(
    left: IndexedCNF,
    right: IndexedCNF,
    left_clause: int,
    left_literal: int,
    right_clause: int,
    right_literal: int,
) -> IndexedCNF:
    """Join two disjoint formulas by swapping the declared incidences."""

    combined = disjoint_union(left, right)
    right_clause_index = len(left.clauses) + right_clause
    shifted_right_literal = shift_literal(right_literal, left.variables)
    clauses = list(combined.clauses)

    if left_literal not in clauses[left_clause]:
        raise ValueError("left literal is not in the declared clause")
    if shifted_right_literal not in clauses[right_clause_index]:
        raise ValueError("right literal is not in the declared clause")

    clauses[left_clause] = (
        clauses[left_clause] - {left_literal}
    ) | {shifted_right_literal}
    clauses[right_clause_index] = (
        clauses[right_clause_index] - {shifted_right_literal}
    ) | {left_literal}
    return IndexedCNF.from_clauses(combined.variables, clauses)


def formula_graph_is_connected(formula: IndexedCNF) -> bool:
    graph = formula_graph(formula)
    if not graph:
        return True
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return len(reached) == len(graph)


def exact_322_audit(formula: IndexedCNF) -> dict[str, object]:
    occurrences: Counter[int] = Counter(
        literal for clause in formula.clauses for literal in clause
    )
    proper = all(
        len(clause) == 3 and len({abs(literal) for literal in clause}) == 3
        for clause in formula.clauses
    )
    simple = len(set(formula.clauses)) == len(formula.clauses)
    exact = all(
        occurrences[variable] == 2 and occurrences[-variable] == 2
        for variable in range(1, formula.variables + 1)
    )
    return {
        "proper": proper,
        "simple": simple,
        "exact_322": exact,
        "connected_formula_graph": formula_graph_is_connected(formula),
    }


def encoding_for_threshold(
    formula_path: Path, threshold: int, compiler: str = "formula"
) -> tuple[str, dict[str, object]]:
    input_bytes = formula_path.read_bytes()
    input_sha256 = hashlib.sha256(input_bytes).hexdigest()
    if compiler == "formula":
        variable_count, clauses = read_encoding_dimacs(formula_path)
        builder, metadata = build_beta_nonpositive_encoding(
            variable_count, clauses, threshold=threshold
        )
        rendered = render_dimacs(
            builder, formula_path.name, input_sha256, threshold=threshold
        )
    elif compiler == "graph":
        builder, metadata = build_graph_threshold_encoding(
            formula_path, threshold
        )
        rendered = render_graph_encoding(
            builder, formula_path, threshold, input_sha256
        )
    else:
        raise ValueError(f"unknown threshold compiler: {compiler}")
    metadata["compiler"] = compiler
    metadata["input"] = formula_path.name
    metadata["input_sha256"] = input_sha256
    metadata["encoding_sha256"] = hashlib.sha256(
        rendered.encode("utf-8")
    ).hexdigest()
    return rendered, metadata


def run_cadical(cnf_path: Path, quiet: bool = True) -> subprocess.CompletedProcess[str]:
    command = ["cadical"]
    if quiet:
        command.append("-q")
    command.append(str(cnf_path))
    return subprocess.run(command, text=True, capture_output=True, check=False)


def decode_assignment(
    output: str, metadata: dict[str, object], variable_count: int
) -> Assignment:
    true_variables = {
        int(token)
        for line in output.splitlines()
        if line.startswith("v ")
        for token in line[2:].split()
        if int(token) > 0
    }
    zero = {int(key): int(value) for key, value in metadata["state_zero"].items()}
    one = {int(key): int(value) for key, value in metadata["state_one"].items()}
    unassigned = {
        int(key): int(value) for key, value in metadata["state_unassigned"].items()
    }
    assignment: list[int] = []
    for variable in range(1, variable_count + 1):
        states = [
            encoding_variable in true_variables
            for encoding_variable in (zero[variable], one[variable], unassigned[variable])
        ]
        if sum(states) != 1:
            raise ValueError(f"model has invalid state for variable {variable}")
        assignment.append((FALSE, TRUE, -1)[states.index(True)])
    return tuple(assignment)


def decode_graph_assignment(
    output: str, metadata: dict[str, object], formula: IndexedCNF
) -> Assignment:
    true_variables = {
        int(token)
        for line in output.splitlines()
        if line.startswith("v ")
        for token in line[2:].split()
        if int(token) > 0
    }
    selected_map = {
        int(vertex): int(encoding_variable)
        for vertex, encoding_variable in metadata["selected"].items()
    }
    selected_vertices = frozenset(
        vertex
        for vertex, encoding_variable in selected_map.items()
        if encoding_variable in true_variables
    )
    return ids_to_assignment(formula, selected_vertices)


def ordered_occurrences(formula: IndexedCNF) -> list[tuple[int, int]]:
    return [
        (clause_index, literal)
        for clause_index, clause in enumerate(formula.clauses)
        for literal in sorted(clause, key=lambda value: (abs(value), value))
    ]


def write_candidate(
    output_dir: Path,
    formula: IndexedCNF,
    switch: dict[str, int],
    lower_threshold: int,
    compiler: str,
    tested: int,
    elapsed_seconds: float,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    formula_path = output_dir / "connected-switch.cnf"
    formula_path.write_text(
        dimacs_text(formula, "connected exact (3,2,2) occurrence 2-switch"),
        encoding="ascii",
    )

    lower_text, lower_map = encoding_for_threshold(
        formula_path, lower_threshold, compiler=compiler
    )
    lower_path = output_dir / f"beta-le-{lower_threshold}-{compiler}.cnf"
    lower_path.write_text(lower_text, encoding="ascii")
    (output_dir / f"beta-le-{lower_threshold}-{compiler}-map.json").write_text(
        json.dumps(lower_map, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    upper_threshold = lower_threshold + 1
    upper_text, upper_map = encoding_for_threshold(
        formula_path, upper_threshold, compiler=compiler
    )
    upper_path = output_dir / f"beta-le-{upper_threshold}-{compiler}.cnf"
    upper_path.write_text(upper_text, encoding="ascii")
    upper_result = run_cadical(upper_path, quiet=False)
    if upper_result.returncode != 10:
        raise RuntimeError(
            f"expected beta <= {upper_threshold} to be SAT, got "
            f"CaDiCaL exit {upper_result.returncode}"
        )
    if compiler == "formula":
        assignment = decode_assignment(
            upper_result.stdout, upper_map, formula.variables
        )
    else:
        assignment = decode_graph_assignment(upper_result.stdout, upper_map, formula)
    if not is_bilateral(formula, assignment):
        raise AssertionError("decoded threshold witness is not bilateral")
    deficiency = bilateral_deficiency(formula, assignment)
    if deficiency > upper_threshold:
        raise AssertionError("decoded threshold witness misses its declared bound")
    upper_witness = assignment_text(assignment)

    receipt = {
        "schema": "bilateral-deficiency/connected-switch-search/v1",
        "formula_sha256": hashlib.sha256(formula_path.read_bytes()).hexdigest(),
        "variables": formula.variables,
        "clauses": len(formula.clauses),
        "switch": switch,
        "audit": exact_322_audit(formula),
        "lower_threshold": lower_threshold,
        "compiler": compiler,
        "lower_encoding_sha256": lower_map["encoding_sha256"],
        "lower_solver_status": "UNSAT",
        "upper_threshold": upper_threshold,
        "upper_encoding_sha256": upper_map["encoding_sha256"],
        "upper_solver_status": "SAT",
        "upper_witness": assignment_text(assignment),
        "upper_witness_deficiency": deficiency,
        "switches_tested": tested,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "assurance_boundary": (
            "The SAT witness is checked against the independent Python semantics. "
            "The UNSAT status is a discovery result until a proof log is generated "
            "and independently checked."
        ),
    }
    (output_dir / "search-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--lower-threshold", type=int, default=1)
    parser.add_argument("--max-switches", type=int, default=0)
    parser.add_argument(
        "--compiler", choices=("formula", "graph"), default="graph"
    )
    args = parser.parse_args()

    left = read_dimacs(args.left)
    right = read_dimacs(args.right)
    left_occurrences = ordered_occurrences(left)
    right_occurrences = ordered_occurrences(right)
    tested = 0
    started = time.monotonic()

    with tempfile.TemporaryDirectory(prefix="bd-connector-search-") as temporary:
        temporary_path = Path(temporary)
        formula_path = temporary_path / "candidate.cnf"
        encoding_path = temporary_path / "threshold.cnf"
        for left_clause, left_literal in left_occurrences:
            for right_clause, right_literal in right_occurrences:
                if args.max_switches and tested >= args.max_switches:
                    print(json.dumps({"status": "EXHAUSTED_LIMIT", "tested": tested}))
                    return
                formula = occurrence_switch(
                    left,
                    right,
                    left_clause,
                    left_literal,
                    right_clause,
                    right_literal,
                )
                audit = exact_322_audit(formula)
                if not all(audit.values()):
                    continue
                tested += 1
                formula_path.write_text(dimacs_text(formula), encoding="ascii")
                encoding, _ = encoding_for_threshold(
                    formula_path, args.lower_threshold, compiler=args.compiler
                )
                encoding_path.write_text(encoding, encoding="ascii")
                result = run_cadical(encoding_path)
                if result.returncode == 20:
                    switch = {
                        "left_clause": left_clause + 1,
                        "left_literal": left_literal,
                        "right_clause": right_clause + 1,
                        "right_literal": right_literal,
                    }
                    receipt = write_candidate(
                        args.output_dir,
                        formula,
                        switch,
                        args.lower_threshold,
                        args.compiler,
                        tested,
                        time.monotonic() - started,
                    )
                    print(json.dumps(receipt, indent=2, sort_keys=True))
                    return
                if result.returncode != 10:
                    raise RuntimeError(
                        f"CaDiCaL failed with exit {result.returncode}: {result.stderr}"
                    )

    print(json.dumps({"status": "NO_CANDIDATE", "tested": tested}))


if __name__ == "__main__":
    main()
