#!/usr/bin/env python3
"""Generate a transparent CNF for the claim beta(F) <= 0.

The encoding uses a deterministic one-hot prefix automaton for
|T|-|U| <= 0.  It intentionally does not import bd_core.py: the proof encoding
and the research implementation have separate DIMACS parsers and separate
variable maps.  Source clauses must use the manuscript's canonical set-valued
representation: complementary literals are allowed, but a literal token may
not be repeated within one clause.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    declared_variables: int | None = None
    declared_clauses: int | None = None
    tokens: list[int] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError(f"unsupported DIMACS header: {line!r}")
            declared_variables = int(fields[2])
            declared_clauses = int(fields[3])
            continue
        tokens.extend(int(field) for field in line.split())

    if declared_variables is None or declared_clauses is None:
        raise ValueError("missing DIMACS header")

    clauses: list[tuple[int, ...]] = []
    current: list[int] = []
    for token in tokens:
        if token == 0:
            clauses.append(tuple(current))
            current = []
        else:
            if abs(token) > declared_variables:
                raise ValueError(f"literal {token} exceeds declared variable count")
            current.append(token)
    if current:
        raise ValueError("unterminated DIMACS clause")
    if len(clauses) != declared_clauses:
        raise ValueError(
            f"header declares {declared_clauses} clauses, parsed {len(clauses)}"
        )
    for clause_index, clause in enumerate(clauses, start=1):
        if len(clause) != len(set(clause)):
            raise ValueError(
                "source clause "
                f"{clause_index} repeats a literal token; canonical set-valued "
                "clauses are required"
            )
    return declared_variables, clauses


class CnfBuilder:
    def __init__(self) -> None:
        self.next_variable = 1
        self.names: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def variable(self, name: str) -> int:
        if name in self.names:
            raise ValueError(f"duplicate encoding variable name: {name}")
        result = self.next_variable
        self.next_variable += 1
        self.names[name] = result
        return result

    def add(self, *literals: int) -> None:
        if not literals:
            raise ValueError("the generator does not add empty clauses directly")
        if 0 in literals:
            raise ValueError("zero is not a clause literal")
        if len(set(literals)) != len(literals):
            raise ValueError(f"duplicate literal in generated clause: {literals}")
        if any(-literal in literals for literal in literals):
            raise ValueError(f"tautological generated clause: {literals}")
        self.clauses.append(tuple(literals))


def add_exactly_one(builder: CnfBuilder, variables: list[int]) -> None:
    builder.add(*variables)
    for left_index, left in enumerate(variables):
        for right in variables[left_index + 1 :]:
            builder.add(-left, -right)


def build_beta_nonpositive_encoding(
    variable_count: int,
    clauses: list[tuple[int, ...]],
    threshold: int = 0,
) -> tuple[CnfBuilder, dict[str, object]]:
    builder = CnfBuilder()

    state_zero: dict[int, int] = {}
    state_one: dict[int, int] = {}
    state_unassigned: dict[int, int] = {}
    for variable in range(1, variable_count + 1):
        state_zero[variable] = builder.variable(f"x{variable}=0")
        state_one[variable] = builder.variable(f"x{variable}=1")
        state_unassigned[variable] = builder.variable(f"x{variable}=*")

    residual: dict[int, int] = {}
    for clause_index in range(1, len(clauses) + 1):
        residual[clause_index] = builder.variable(f"residual[{clause_index}]")

    # Every original variable has exactly one state: 0, 1, or unassigned.
    for variable in range(1, variable_count + 1):
        add_exactly_one(
            builder,
            [state_zero[variable], state_one[variable], state_unassigned[variable]],
        )

    positive_occurrences: dict[int, list[int]] = {
        variable: [] for variable in range(1, variable_count + 1)
    }
    negative_occurrences: dict[int, list[int]] = {
        variable: [] for variable in range(1, variable_count + 1)
    }

    # residual[a] is true exactly when clause a has no assigned-true literal.
    for clause_index, clause in enumerate(clauses, start=1):
        true_state_literals: list[int] = []
        for literal in clause:
            variable = abs(literal)
            if literal > 0:
                true_state_literals.append(state_one[variable])
                positive_occurrences[variable].append(clause_index)
            else:
                true_state_literals.append(state_zero[variable])
                negative_occurrences[variable].append(clause_index)
        residual_variable = residual[clause_index]
        for true_state in true_state_literals:
            builder.add(-residual_variable, -true_state)
        builder.add(residual_variable, *true_state_literals)

    # An unassigned variable must occur with each sign in a residual clause.
    for variable in range(1, variable_count + 1):
        builder.add(
            -state_unassigned[variable],
            *(residual[index] for index in positive_occurrences[variable]),
        )
        builder.add(
            -state_unassigned[variable],
            *(residual[index] for index in negative_occurrences[variable]),
        )

    # Track the prefix difference d = residuals seen - unassigned variables
    # seen.  Exactly one balance state is true in each layer.  The two
    # transition clauses per predecessor force the unique successor according
    # to the current Boolean input.
    threshold_inputs = [
        (residual[index], 1) for index in range(1, len(clauses) + 1)
    ] + [
        (state_unassigned[variable], -1)
        for variable in range(1, variable_count + 1)
    ]

    balance_states: dict[tuple[int, int], int] = {}
    initial_state = builder.variable("balance[0,0]")
    balance_states[0, 0] = initial_state
    builder.add(initial_state)
    previous = {0: initial_state}

    for layer, (input_variable, weight) in enumerate(threshold_inputs, start=1):
        reachable = sorted(
            set(previous).union(difference + weight for difference in previous)
        )
        current = {
            difference: builder.variable(f"balance[{layer},{difference}]")
            for difference in reachable
        }
        for difference, encoding_variable in current.items():
            balance_states[layer, difference] = encoding_variable
        add_exactly_one(builder, list(current.values()))

        for difference, predecessor in previous.items():
            builder.add(-predecessor, input_variable, current[difference])
            builder.add(
                -predecessor,
                -input_variable,
                current[difference + weight],
            )
        previous = current

    # Reject precisely the final differences above the requested threshold.
    for difference, encoding_variable in previous.items():
        if difference > threshold:
            builder.add(-encoding_variable)

    metadata: dict[str, object] = {
        "claim": (
            "there exists a bilateral partial assignment with |T|-|U| <= 0"
            if threshold == 0
            else "there exists a bilateral partial assignment with "
            f"|T|-|U| <= {threshold}"
        ),
        "original_variable_count": variable_count,
        "original_clause_count": len(clauses),
        "encoding_variable_count": builder.next_variable - 1,
        "encoding_clause_count": len(builder.clauses),
        "state_zero": state_zero,
        "state_one": state_one,
        "state_unassigned": state_unassigned,
        "residual": residual,
        "balance_states": {
            f"{layer},{difference}": encoding_variable
            for (layer, difference), encoding_variable in balance_states.items()
        },
    }
    if threshold != 0:
        metadata["threshold"] = threshold
    return builder, metadata


def render_dimacs(
    builder: CnfBuilder,
    input_name: str,
    input_sha256: str,
    threshold: int = 0,
) -> str:
    lines = [
        (
            "c beta(F) <= 0 encoding by deterministic prefix balance"
            if threshold == 0
            else f"c beta(F) <= {threshold} encoding by deterministic prefix balance"
        ),
        f"c input {input_name}",
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
    parser.add_argument("--threshold", type=int, default=0)
    args = parser.parse_args()

    variable_count, clauses = read_dimacs(args.input)
    builder, metadata = build_beta_nonpositive_encoding(
        variable_count, clauses, threshold=args.threshold
    )
    input_bytes = args.input.read_bytes()
    input_sha256 = hashlib.sha256(input_bytes).hexdigest()
    dimacs = render_dimacs(
        builder, args.input.name, input_sha256, threshold=args.threshold
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.map_path.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dimacs, encoding="utf-8")
    metadata["input"] = args.input.name
    metadata["input_sha256"] = input_sha256
    metadata["encoding_sha256"] = hashlib.sha256(dimacs.encode("utf-8")).hexdigest()
    args.map_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "input": str(args.input),
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
