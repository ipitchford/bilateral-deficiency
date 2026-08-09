#!/usr/bin/env python3
"""Exact boundary signatures for bilateral-deficiency terminal gadgets."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from bd_core import (
    FALSE,
    TRUE,
    UNASSIGNED,
    Assignment,
    IndexedCNF,
    assignment_text,
    beta,
    read_dimacs,
    residual,
)


POSITIVE = 1
NEGATIVE = 2
BOTH = POSITIVE | NEGATIVE


@dataclass(frozen=True)
class SignatureEntry:
    states: tuple[int, ...]
    masks: tuple[int, ...]
    value: int
    witness: Assignment


@dataclass(frozen=True)
class TerminalSignature:
    variables: int
    clauses: int
    terminals: tuple[int, ...]
    entries: tuple[SignatureEntry, ...]


def _internal_is_bilateral(
    formula: IndexedCNF, assignment: Assignment, terminals: frozenset[int]
) -> bool:
    surviving_literals = set().union(*residual(formula, assignment).clauses)
    for variable, state in enumerate(assignment, start=1):
        if variable in terminals or state != UNASSIGNED:
            continue
        if variable not in surviving_literals or -variable not in surviving_literals:
            return False
    return True


def _terminal_mask(
    surviving_literals: set[int], terminal: int, state: int
) -> int:
    if state != UNASSIGNED:
        return 0
    return (
        (POSITIVE if terminal in surviving_literals else 0)
        | (NEGATIVE if -terminal in surviving_literals else 0)
    )


def terminal_signature(
    formula: IndexedCNF, terminals: tuple[int, ...]
) -> TerminalSignature:
    if len(set(terminals)) != len(terminals):
        raise ValueError("terminal variables must be distinct")
    if any(terminal < 1 or terminal > formula.variables for terminal in terminals):
        raise ValueError("terminal variable lies outside the formula")

    terminal_set = frozenset(terminals)
    best: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, Assignment]] = {}
    for assignment in product((UNASSIGNED, FALSE, TRUE), repeat=formula.variables):
        if not _internal_is_bilateral(formula, assignment, terminal_set):
            continue
        surviving = residual(formula, assignment)
        surviving_literals = set().union(*surviving.clauses)
        states = tuple(assignment[terminal - 1] for terminal in terminals)
        masks = tuple(
            _terminal_mask(surviving_literals, terminal, state)
            for terminal, state in zip(terminals, states)
        )
        unassigned_internal = sum(
            state == UNASSIGNED
            for variable, state in enumerate(assignment, start=1)
            if variable not in terminal_set
        )
        value = len(surviving.clauses) - unassigned_internal
        key = (states, masks)
        previous = best.get(key)
        if previous is None or (value, assignment) < previous:
            best[key] = (value, assignment)

    entries = tuple(
        SignatureEntry(states, masks, value, witness)
        for (states, masks), (value, witness) in sorted(best.items())
    )
    return TerminalSignature(
        formula.variables, len(formula.clauses), terminals, entries
    )


def close_signature(signature: TerminalSignature) -> tuple[int, SignatureEntry]:
    feasible: list[tuple[int, SignatureEntry]] = []
    for entry in signature.entries:
        if any(
            state == UNASSIGNED and mask != BOTH
            for state, mask in zip(entry.states, entry.masks)
        ):
            continue
        terminal_charge = sum(state == UNASSIGNED for state in entry.states)
        feasible.append((entry.value - terminal_charge, entry))
    if not feasible:
        raise AssertionError("complete terminal assignments must be feasible")
    return min(feasible, key=lambda item: (item[0], item[1].witness))


def compose_closed_signatures(
    left: TerminalSignature, right: TerminalSignature
) -> tuple[int, SignatureEntry, SignatureEntry]:
    if len(left.terminals) != len(right.terminals):
        raise ValueError("signatures must expose the same number of terminals")

    feasible: list[tuple[int, SignatureEntry, SignatureEntry]] = []
    for left_entry in left.entries:
        for right_entry in right.entries:
            if left_entry.states != right_entry.states:
                continue
            if any(
                state == UNASSIGNED and (left_mask | right_mask) != BOTH
                for state, left_mask, right_mask in zip(
                    left_entry.states, left_entry.masks, right_entry.masks
                )
            ):
                continue
            terminal_charge = sum(
                state == UNASSIGNED for state in left_entry.states
            )
            value = left_entry.value + right_entry.value - terminal_charge
            feasible.append((value, left_entry, right_entry))
    if not feasible:
        raise AssertionError("complete terminal assignments must compose")
    return min(
        feasible,
        key=lambda item: (item[0], item[1].witness, item[2].witness),
    )


def glue_formulas_on_terminals(
    left: IndexedCNF,
    left_terminals: tuple[int, ...],
    right: IndexedCNF,
    right_terminals: tuple[int, ...],
) -> IndexedCNF:
    if len(left_terminals) != len(right_terminals):
        raise ValueError("terminal lists must have equal length")
    if len(set(left_terminals)) != len(left_terminals):
        raise ValueError("left terminal list contains duplicates")
    if len(set(right_terminals)) != len(right_terminals):
        raise ValueError("right terminal list contains duplicates")

    terminal_count = len(left_terminals)
    left_internal = [
        variable
        for variable in range(1, left.variables + 1)
        if variable not in left_terminals
    ]
    right_internal = [
        variable
        for variable in range(1, right.variables + 1)
        if variable not in right_terminals
    ]
    left_map = {
        terminal: index + 1 for index, terminal in enumerate(left_terminals)
    }
    right_map = {
        terminal: index + 1 for index, terminal in enumerate(right_terminals)
    }
    next_variable = terminal_count + 1
    for variable in left_internal:
        left_map[variable] = next_variable
        next_variable += 1
    for variable in right_internal:
        right_map[variable] = next_variable
        next_variable += 1

    def remap_clause(clause: frozenset[int], mapping: dict[int, int]) -> set[int]:
        return {
            (1 if literal > 0 else -1) * mapping[abs(literal)]
            for literal in clause
        }

    clauses = [remap_clause(clause, left_map) for clause in left.clauses]
    clauses.extend(remap_clause(clause, right_map) for clause in right.clauses)
    return IndexedCNF.from_clauses(next_variable - 1, clauses)


def signature_json(
    signature: TerminalSignature, input_path: Path | None = None
) -> dict[str, object]:
    result: dict[str, object] = {
        "schema": "bilateral-deficiency/terminal-signature/v1",
        "variables": signature.variables,
        "clauses": signature.clauses,
        "terminals": list(signature.terminals),
        "mask_legend": {"0": "none", "1": "positive", "2": "negative", "3": "both"},
        "entries": [
            {
                "states": assignment_text(entry.states),
                "masks": list(entry.masks),
                "value": entry.value,
                "witness": assignment_text(entry.witness),
            }
            for entry in signature.entries
        ],
    }
    if input_path is not None:
        result["input"] = input_path.name
        result["input_sha256"] = hashlib.sha256(input_path.read_bytes()).hexdigest()
    closed_value, closed_entry = close_signature(signature)
    result["closed_value"] = closed_value
    result["closed_witness"] = assignment_text(closed_entry.witness)
    result["assurance_boundary"] = (
        "The signature is an exhaustive receipt over 3^n local assignments. "
        "The composition theorem is a written universal argument; this JSON "
        "does not by itself certify that theorem."
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--terminals", required=True)
    parser.add_argument("--verify-closed-beta", action="store_true")
    args = parser.parse_args()

    formula = read_dimacs(args.input)
    terminals = tuple(
        int(field) for field in args.terminals.split(",") if field.strip()
    )
    signature = terminal_signature(formula, terminals)
    rendered = signature_json(signature, args.input)
    if args.verify_closed_beta:
        exact = beta(formula).value
        if rendered["closed_value"] != exact:
            raise AssertionError("closed terminal signature disagrees with beta")
        rendered["verified_closed_beta"] = exact
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(rendered, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(args.output), "entries": len(signature.entries)}))


if __name__ == "__main__":
    main()
