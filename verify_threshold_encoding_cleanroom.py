#!/usr/bin/env python3
"""Clean-room audit of the bilateral-deficiency threshold CNF encoding.

This validator intentionally does not import ``generate_positive_base_cnf`` or
``bd_core``. It has its own DIMACS parser, reconstructs every expected clause
from the mathematical input and public variable map, and uses a small
standard-library DPLL solver for exhaustive semantic checks on a declared
corpus.

The result is producer-side clean-room validation. It is not external
reproduction, proof-assistant formalisation, or a proof of the universal
encoding lemma independent of this implementation and its runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
State = tuple[int, ...]


class AuditError(ValueError):
    """Raised when an input, map, or encoding fails the independent audit."""


@dataclass(frozen=True)
class ParsedDimacs:
    variable_count: int
    clauses: Formula
    comments: tuple[str, ...]


@dataclass(frozen=True)
class EncodingMap:
    threshold: int
    encoding_variable_count: int
    encoding_clause_count: int
    state_zero: dict[int, int]
    state_one: dict[int, int]
    state_unassigned: dict[int, int]
    residual: dict[int, int]
    balance: dict[tuple[int, int], int]


@dataclass(frozen=True)
class CorpusCase:
    name: str
    variable_count: int
    clauses: Formula


CORPUS: tuple[CorpusCase, ...] = (
    CorpusCase("empty-formula", 1, ()),
    CorpusCase("positive-unit", 1, ((1,),)),
    CorpusCase("empty-clause", 1, ((),)),
    CorpusCase("opposite-unit-pair", 1, ((1,), (-1,))),
    CorpusCase("indexed-duplicate", 1, ((1,), (1,), (-1,))),
    CorpusCase("satisfiable-two-variable", 2, ((1, 2), (-1, 2))),
    CorpusCase(
        "four-polarity-square",
        2,
        ((1, 2), (-1, 2), (1, -2), (-1, -2)),
    ),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_dimacs(path: Path) -> ParsedDimacs:
    """Parse DIMACS independently, including clauses split across lines."""

    declared_variables: int | None = None
    declared_clauses: int | None = None
    comments: list[str] = []
    tokens: list[int] = []

    try:
        lines = path.read_text(encoding="ascii").splitlines()
    except UnicodeDecodeError as error:
        raise AuditError(f"{path}: DIMACS is not ASCII") from error

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("c") and (line == "c" or line[1].isspace()):
            comments.append(line[1:].strip())
            continue
        if line.startswith("p") and (len(line) == 1 or line[1].isspace()):
            if declared_variables is not None:
                raise AuditError(f"{path}:{line_number}: duplicate DIMACS header")
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise AuditError(f"{path}:{line_number}: unsupported header {line!r}")
            try:
                declared_variables = int(fields[2])
                declared_clauses = int(fields[3])
            except ValueError as error:
                raise AuditError(
                    f"{path}:{line_number}: non-integer DIMACS count"
                ) from error
            if declared_variables < 0 or declared_clauses < 0:
                raise AuditError(f"{path}:{line_number}: negative DIMACS count")
            continue
        if declared_variables is None:
            raise AuditError(f"{path}:{line_number}: data precedes DIMACS header")
        try:
            tokens.extend(int(field) for field in line.split())
        except ValueError as error:
            raise AuditError(f"{path}:{line_number}: non-integer DIMACS token") from error

    if declared_variables is None or declared_clauses is None:
        raise AuditError(f"{path}: missing DIMACS header")

    clauses: list[Clause] = []
    current: list[int] = []
    for token in tokens:
        if token == 0:
            clauses.append(tuple(current))
            current.clear()
            continue
        if abs(token) > declared_variables:
            raise AuditError(
                f"{path}: literal {token} exceeds variable count {declared_variables}"
            )
        current.append(token)
    if current:
        raise AuditError(f"{path}: final DIMACS clause is not terminated by zero")
    if len(clauses) != declared_clauses:
        raise AuditError(
            f"{path}: header declares {declared_clauses} clauses, parsed {len(clauses)}"
        )
    return ParsedDimacs(declared_variables, tuple(clauses), tuple(comments))


def _require_plain_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise AuditError(f"{label} must be an integer")
    return value


def _index_map(
    raw: object,
    label: str,
    expected_indices: Iterable[int],
) -> dict[int, int]:
    if not isinstance(raw, dict):
        raise AuditError(f"{label} must be an object")
    expected = set(expected_indices)
    parsed: dict[int, int] = {}
    for raw_key, raw_value in raw.items():
        try:
            index = int(raw_key)
        except (TypeError, ValueError) as error:
            raise AuditError(f"{label} contains non-integer key {raw_key!r}") from error
        if str(index) != raw_key:
            raise AuditError(f"{label} contains non-canonical key {raw_key!r}")
        parsed[index] = _require_plain_int(raw_value, f"{label}[{raw_key}]")
    if set(parsed) != expected:
        missing = sorted(expected - set(parsed))
        extra = sorted(set(parsed) - expected)
        raise AuditError(f"{label} index mismatch: missing={missing}, extra={extra}")
    return parsed


def load_encoding_map(
    map_path: Path,
    mathematical: ParsedDimacs,
    input_path: Path,
    encoding_path: Path,
) -> EncodingMap:
    try:
        raw = json.loads(map_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"{map_path}: invalid UTF-8 JSON") from error
    if not isinstance(raw, dict):
        raise AuditError(f"{map_path}: top-level value must be an object")

    required = {
        "claim",
        "original_variable_count",
        "original_clause_count",
        "encoding_variable_count",
        "encoding_clause_count",
        "state_zero",
        "state_one",
        "state_unassigned",
        "residual",
        "balance_states",
        "input",
        "input_sha256",
        "encoding_sha256",
    }
    missing = sorted(required - set(raw))
    if missing:
        raise AuditError(f"{map_path}: missing required fields {missing}")

    original_variables = _require_plain_int(
        raw["original_variable_count"], "original_variable_count"
    )
    original_clauses = _require_plain_int(
        raw["original_clause_count"], "original_clause_count"
    )
    if original_variables != mathematical.variable_count:
        raise AuditError("map original_variable_count does not match mathematical input")
    if original_clauses != len(mathematical.clauses):
        raise AuditError("map original_clause_count does not match mathematical input")

    if raw["input"] != input_path.name:
        raise AuditError("map input filename does not match mathematical input")
    input_hash = sha256_path(input_path)
    if raw["input_sha256"] != input_hash:
        raise AuditError("map input_sha256 does not match mathematical input bytes")
    encoding_hash = sha256_path(encoding_path)
    if raw["encoding_sha256"] != encoding_hash:
        raise AuditError("map encoding_sha256 does not match encoding bytes")

    threshold = _require_plain_int(raw.get("threshold", 0), "threshold")
    expected_claim = (
        "there exists a bilateral partial assignment with |T|-|U| <= 0"
        if threshold == 0
        else "there exists a bilateral partial assignment with "
        f"|T|-|U| <= {threshold}"
    )
    if raw["claim"] != expected_claim:
        raise AuditError("map claim is inconsistent with its threshold")

    variable_count = _require_plain_int(
        raw["encoding_variable_count"], "encoding_variable_count"
    )
    clause_count = _require_plain_int(
        raw["encoding_clause_count"], "encoding_clause_count"
    )
    if variable_count <= 0 or clause_count <= 0:
        raise AuditError("encoding counts must be positive")

    indices = range(1, mathematical.variable_count + 1)
    state_zero = _index_map(raw["state_zero"], "state_zero", indices)
    state_one = _index_map(raw["state_one"], "state_one", indices)
    state_unassigned = _index_map(
        raw["state_unassigned"], "state_unassigned", indices
    )
    residual = _index_map(
        raw["residual"], "residual", range(1, len(mathematical.clauses) + 1)
    )

    raw_balance = raw["balance_states"]
    if not isinstance(raw_balance, dict):
        raise AuditError("balance_states must be an object")
    balance: dict[tuple[int, int], int] = {}
    for raw_key, raw_value in raw_balance.items():
        if not isinstance(raw_key, str) or raw_key.count(",") != 1:
            raise AuditError(f"invalid balance_states key {raw_key!r}")
        layer_text, difference_text = raw_key.split(",")
        try:
            layer = int(layer_text)
            difference = int(difference_text)
        except ValueError as error:
            raise AuditError(f"invalid balance_states key {raw_key!r}") from error
        if raw_key != f"{layer},{difference}":
            raise AuditError(f"non-canonical balance_states key {raw_key!r}")
        balance[layer, difference] = _require_plain_int(
            raw_value, f"balance_states[{raw_key}]"
        )

    all_ids = (
        list(state_zero.values())
        + list(state_one.values())
        + list(state_unassigned.values())
        + list(residual.values())
        + list(balance.values())
    )
    expected_ids = list(range(1, variable_count + 1))
    if sorted(all_ids) != expected_ids:
        counts = Counter(all_ids)
        aliases = sorted(variable for variable, count in counts.items() if count > 1)
        missing_ids = sorted(set(expected_ids) - set(all_ids))
        out_of_range = sorted(set(all_ids) - set(expected_ids))
        raise AuditError(
            "map variables are not a bijection onto 1..N: "
            f"aliases={aliases}, missing={missing_ids}, out_of_range={out_of_range}"
        )

    return EncodingMap(
        threshold,
        variable_count,
        clause_count,
        state_zero,
        state_one,
        state_unassigned,
        residual,
        balance,
    )


def _exactly_one(variables: Sequence[int]) -> list[Clause]:
    if not variables:
        raise AuditError("an exactly-one family cannot be empty")
    clauses: list[Clause] = [tuple(variables)]
    clauses.extend(
        (-left, -right)
        for left_index, left in enumerate(variables)
        for right in variables[left_index + 1 :]
    )
    return clauses


def reconstruct_clauses(
    mathematical: ParsedDimacs,
    mapping: EncodingMap,
) -> list[Clause]:
    """Reconstruct the complete encoding from its mathematical definitions."""

    expected: list[Clause] = []
    for variable in range(1, mathematical.variable_count + 1):
        expected.extend(
            _exactly_one(
                (
                    mapping.state_zero[variable],
                    mapping.state_one[variable],
                    mapping.state_unassigned[variable],
                )
            )
        )

    positive_occurrences = {
        variable: [] for variable in range(1, mathematical.variable_count + 1)
    }
    negative_occurrences = {
        variable: [] for variable in range(1, mathematical.variable_count + 1)
    }

    for clause_index, clause in enumerate(mathematical.clauses, start=1):
        if len(set(clause)) != len(clause):
            raise AuditError(
                f"mathematical clause {clause_index} repeats a literal; "
                "the audited production compiler rejects such clauses"
            )
        true_states: list[int] = []
        for literal in clause:
            variable = abs(literal)
            if literal > 0:
                true_states.append(mapping.state_one[variable])
                positive_occurrences[variable].append(clause_index)
            else:
                true_states.append(mapping.state_zero[variable])
                negative_occurrences[variable].append(clause_index)
        residual = mapping.residual[clause_index]
        expected.extend((-residual, -state) for state in true_states)
        expected.append((residual, *true_states))

    for variable in range(1, mathematical.variable_count + 1):
        expected.append(
            (
                -mapping.state_unassigned[variable],
                *(mapping.residual[index] for index in positive_occurrences[variable]),
            )
        )
        expected.append(
            (
                -mapping.state_unassigned[variable],
                *(mapping.residual[index] for index in negative_occurrences[variable]),
            )
        )

    weighted_inputs = [
        (mapping.residual[index], 1)
        for index in range(1, len(mathematical.clauses) + 1)
    ] + [
        (mapping.state_unassigned[variable], -1)
        for variable in range(1, mathematical.variable_count + 1)
    ]

    reachable_by_layer: dict[int, tuple[int, ...]] = {0: (0,)}
    previous = (0,)
    for layer, (_, weight) in enumerate(weighted_inputs, start=1):
        current = tuple(sorted(set(previous) | {value + weight for value in previous}))
        reachable_by_layer[layer] = current
        previous = current
    expected_balance_keys = {
        (layer, difference)
        for layer, differences in reachable_by_layer.items()
        for difference in differences
    }
    if set(mapping.balance) != expected_balance_keys:
        missing = sorted(expected_balance_keys - set(mapping.balance))
        extra = sorted(set(mapping.balance) - expected_balance_keys)
        raise AuditError(
            f"balance-state reachability mismatch: missing={missing}, extra={extra}"
        )

    expected.append((mapping.balance[0, 0],))
    previous = (0,)
    for layer, (input_variable, weight) in enumerate(weighted_inputs, start=1):
        current = reachable_by_layer[layer]
        expected.extend(_exactly_one([mapping.balance[layer, d] for d in current]))
        for difference in previous:
            predecessor = mapping.balance[layer - 1, difference]
            expected.append(
                (-predecessor, input_variable, mapping.balance[layer, difference])
            )
            expected.append(
                (
                    -predecessor,
                    -input_variable,
                    mapping.balance[layer, difference + weight],
                )
            )
        previous = current

    final_layer = len(weighted_inputs)
    for difference in previous:
        if difference > mapping.threshold:
            expected.append((-mapping.balance[final_layer, difference],))
    return expected


def _normalise_clause(clause: Clause) -> Clause:
    return tuple(sorted(clause, key=lambda literal: (abs(literal), literal < 0)))


def _first_difference(expected: Sequence[Clause], actual: Sequence[Clause]) -> str:
    for index, (expected_clause, actual_clause) in enumerate(
        itertools.zip_longest(expected, actual), start=1
    ):
        if expected_clause != actual_clause:
            return f"clause {index}: expected={expected_clause}, actual={actual_clause}"
    return "no difference"


def audit_encoding(
    input_path: Path,
    encoding_path: Path,
    map_path: Path,
) -> tuple[dict[str, object], ParsedDimacs, ParsedDimacs, EncodingMap]:
    mathematical = parse_dimacs(input_path)
    encoded = parse_dimacs(encoding_path)
    mapping = load_encoding_map(map_path, mathematical, input_path, encoding_path)

    if encoded.variable_count != mapping.encoding_variable_count:
        raise AuditError("encoding header variable count does not match map")
    if len(encoded.clauses) != mapping.encoding_clause_count:
        raise AuditError("encoding header clause count does not match map")

    expected_input_comment = f"input {input_path.name}"
    expected_hash_comment = f"input_sha256 {sha256_path(input_path)}"
    if expected_input_comment not in encoded.comments:
        raise AuditError("encoding lacks the map-bound input filename comment")
    if expected_hash_comment not in encoded.comments:
        raise AuditError("encoding lacks the map-bound input SHA-256 comment")

    expected_clauses = reconstruct_clauses(mathematical, mapping)
    if len(expected_clauses) != mapping.encoding_clause_count:
        raise AuditError(
            "independent reconstruction count disagrees with map: "
            f"expected={len(expected_clauses)}, map={mapping.encoding_clause_count}"
        )

    expected_multiset = Counter(_normalise_clause(clause) for clause in expected_clauses)
    actual_multiset = Counter(_normalise_clause(clause) for clause in encoded.clauses)
    if expected_multiset != actual_multiset:
        missing = list((expected_multiset - actual_multiset).elements())[:3]
        extra = list((actual_multiset - expected_multiset).elements())[:3]
        raise AuditError(
            f"encoding clause multiset mismatch: missing={missing}, extra={extra}"
        )
    if tuple(expected_clauses) != encoded.clauses:
        raise AuditError(
            "encoding clauses are logically complete but not in the declared canonical "
            f"order; {_first_difference(expected_clauses, encoded.clauses)}"
        )

    report: dict[str, object] = {
        "input": input_path.name,
        "input_sha256": sha256_path(input_path),
        "encoding": encoding_path.name,
        "encoding_sha256": sha256_path(encoding_path),
        "map": map_path.name,
        "map_sha256": sha256_path(map_path),
        "threshold": mapping.threshold,
        "original_variables": mathematical.variable_count,
        "original_clauses": len(mathematical.clauses),
        "encoding_variables": encoded.variable_count,
        "encoding_clauses": len(encoded.clauses),
        "map_is_variable_bijection": True,
        "reachable_balance_states_exact": True,
        "clause_multiset_exact": True,
        "canonical_clause_order_exact": True,
    }
    return report, mathematical, encoded, mapping


def assignment_semantics(state: State, clauses: Formula) -> tuple[bool, int]:
    residual: list[Clause] = []
    for clause in clauses:
        satisfied = False
        for literal in clause:
            value = state[abs(literal) - 1]
            if value != -1 and (
                (literal > 0 and value == 1) or (literal < 0 and value == 0)
            ):
                satisfied = True
                break
        if not satisfied:
            residual.append(clause)

    unassigned = [index + 1 for index, value in enumerate(state) if value == -1]
    for variable in unassigned:
        if not any(variable in clause for clause in residual):
            return False, len(residual) - len(unassigned)
        if not any(-variable in clause for clause in residual):
            return False, len(residual) - len(unassigned)
    return True, len(residual) - len(unassigned)


def exact_beta(variable_count: int, clauses: Formula) -> tuple[int, int]:
    best: int | None = None
    count = 0
    for state in itertools.product((0, 1, -1), repeat=variable_count):
        count += 1
        bilateral, difference = assignment_semantics(state, clauses)
        if bilateral and (best is None or difference < best):
            best = difference
    if best is None:
        raise AuditError("no bilateral assignment found; full assignments should be bilateral")
    return best, count


def dpll_satisfiable(variable_count: int, clauses: Sequence[Clause]) -> bool:
    """A compact complete SAT solver used only for the declared tiny corpus."""

    initial = [-1] * (variable_count + 1)

    def propagate(assignment: list[int]) -> bool:
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unresolved: list[int] = []
                satisfied = False
                for literal in clause:
                    value = assignment[abs(literal)]
                    if value == -1:
                        unresolved.append(literal)
                    elif (literal > 0 and value == 1) or (
                        literal < 0 and value == 0
                    ):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not unresolved:
                    return False
                if len(unresolved) == 1:
                    literal = unresolved[0]
                    variable = abs(literal)
                    required = 1 if literal > 0 else 0
                    current = assignment[variable]
                    if current != -1 and current != required:
                        return False
                    if current == -1:
                        assignment[variable] = required
                        changed = True
        return True

    def choose_variable(assignment: list[int]) -> int | None:
        shortest: list[int] | None = None
        for clause in clauses:
            unresolved: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment[abs(literal)]
                if value == -1:
                    unresolved.append(literal)
                elif (literal > 0 and value == 1) or (
                    literal < 0 and value == 0
                ):
                    satisfied = True
                    break
            if satisfied:
                continue
            if shortest is None or len(unresolved) < len(shortest):
                shortest = unresolved
        return None if not shortest else abs(shortest[0])

    def search(assignment: list[int]) -> bool:
        if not propagate(assignment):
            return False
        variable = choose_variable(assignment)
        if variable is None:
            return True
        for value in (1, 0):
            branch = assignment.copy()
            branch[variable] = value
            if search(branch):
                return True
        return False

    return search(initial)


def render_formula(case: CorpusCase) -> str:
    lines = [f"c clean-room corpus case {case.name}"]
    lines.append(f"p cnf {case.variable_count} {len(case.clauses)}")
    lines.extend(
        " ".join(str(literal) for literal in clause)
        + (" " if clause else "")
        + "0"
        for clause in case.clauses
    )
    return "\n".join(lines) + "\n"


def constrained_state_units(state: State, mapping: EncodingMap) -> list[Clause]:
    units: list[Clause] = []
    for variable, value in enumerate(state, start=1):
        if value == 0:
            units.append((mapping.state_zero[variable],))
        elif value == 1:
            units.append((mapping.state_one[variable],))
        elif value == -1:
            units.append((mapping.state_unassigned[variable],))
        else:
            raise AuditError(f"invalid ternary state value {value}")
    return units


def run_semantic_corpus(compiler_path: Path) -> list[dict[str, object]]:
    if not compiler_path.is_file():
        raise AuditError(f"production compiler not found: {compiler_path}")
    results: list[dict[str, object]] = []

    with tempfile.TemporaryDirectory(prefix="bd-cleanroom-") as temporary:
        temporary_path = Path(temporary)
        for case in CORPUS:
            input_path = temporary_path / f"{case.name}.cnf"
            input_path.write_text(render_formula(case), encoding="ascii")
            beta, assignment_count = exact_beta(case.variable_count, case.clauses)
            threshold_results: list[dict[str, object]] = []

            for threshold in (beta - 1, beta):
                encoding_path = temporary_path / f"{case.name}-q{threshold}.cnf"
                map_path = temporary_path / f"{case.name}-q{threshold}.json"
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(compiler_path),
                        str(input_path),
                        str(encoding_path),
                        "--map",
                        str(map_path),
                        "--threshold",
                        str(threshold),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                if completed.returncode != 0:
                    raise AuditError(
                        f"production compiler failed for {case.name}, q={threshold}: "
                        f"{completed.stderr.strip() or completed.stdout.strip()}"
                    )

                audit, _, encoded, mapping = audit_encoding(
                    input_path, encoding_path, map_path
                )
                expected_overall = beta <= threshold
                actual_overall = dpll_satisfiable(
                    encoded.variable_count, encoded.clauses
                )
                if actual_overall != expected_overall:
                    raise AuditError(
                        f"semantic mismatch for {case.name}, q={threshold}: "
                        f"mathematical={expected_overall}, encoded={actual_overall}"
                    )

                constrained_checks = 0
                for state in itertools.product(
                    (0, 1, -1), repeat=case.variable_count
                ):
                    bilateral, difference = assignment_semantics(state, case.clauses)
                    expected_extension = bilateral and difference <= threshold
                    actual_extension = dpll_satisfiable(
                        encoded.variable_count,
                        list(encoded.clauses) + constrained_state_units(state, mapping),
                    )
                    constrained_checks += 1
                    if actual_extension != expected_extension:
                        raise AuditError(
                            f"state-extension mismatch for {case.name}, q={threshold}, "
                            f"state={state}: mathematical={expected_extension}, "
                            f"encoded={actual_extension}"
                        )

                threshold_results.append(
                    {
                        "threshold": threshold,
                        "mathematical_threshold_truth": expected_overall,
                        "encoded_sat": actual_overall,
                        "constrained_state_checks": constrained_checks,
                        "encoding_variables": audit["encoding_variables"],
                        "encoding_clauses": audit["encoding_clauses"],
                        "encoding_sha256": audit["encoding_sha256"],
                    }
                )

            results.append(
                {
                    "case": case.name,
                    "variables": case.variable_count,
                    "clauses": len(case.clauses),
                    "ternary_assignments_exhausted": assignment_count,
                    "exact_beta": beta,
                    "thresholds": threshold_results,
                }
            )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="mathematical DIMACS formula")
    parser.add_argument("encoding", type=Path, help="production threshold CNF")
    parser.add_argument("map", type=Path, help="production JSON variable map")
    parser.add_argument(
        "--compiler",
        type=Path,
        default=Path(__file__).resolve().with_name("generate_positive_base_cnf.py"),
        help="production compiler executable used only to create the small corpus",
    )
    parser.add_argument("--receipt", type=Path)
    parser.add_argument(
        "--skip-semantic-corpus",
        action="store_true",
        help="run only the structural audit of the supplied encoding",
    )
    args = parser.parse_args()

    try:
        structural, _, _, _ = audit_encoding(args.input, args.encoding, args.map)
        corpus = (
            []
            if args.skip_semantic_corpus
            else run_semantic_corpus(args.compiler.resolve())
        )
    except (AuditError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    receipt: dict[str, object] = {
        "schema": "bilateral-deficiency-threshold-cleanroom-validation-v1",
        "status": "PASS",
        "assurance_boundary": (
            "producer-side clean-room validation of the compiler output; not "
            "external reproduction, independent expert review, proof-assistant "
            "formalisation, or a proof of the universal theory"
        ),
        "implementation_independence": {
            "standard_library_only": True,
            "imports_production_compiler": False,
            "imports_bd_core": False,
            "production_compiler_used_as_black_box_for_corpus": True,
            "validator_sha256": sha256_path(Path(__file__).resolve()),
            "production_compiler_sha256": sha256_path(args.compiler.resolve()),
        },
        "structural_audit": structural,
        "semantic_corpus": {
            "description": (
                "For each declared formula, all 3^n partial assignments are "
                "evaluated mathematically. The production encoding is audited "
                "clause-by-clause and checked by an independent DPLL solver at "
                "q=beta-1 and q=beta, both globally and under every ternary state."
            ),
            "case_count": len(corpus),
            "cases": corpus,
        },
    }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
