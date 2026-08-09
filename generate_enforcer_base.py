#!/usr/bin/env python3
"""Compose the SAT 2024 (3,2,2)-enforcer with its terminal flip."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from bd_core import IndexedCNF, assignment_text, dimacs_text, read_dimacs
from connector_search import exact_322_audit
from terminal_signature import (
    compose_closed_signatures,
    glue_formulas_on_terminals,
    signature_json,
    terminal_signature,
)


def flip_variable(formula: IndexedCNF, variable: int) -> IndexedCNF:
    clauses = []
    for clause in formula.clauses:
        clauses.append(
            {
                -literal if abs(literal) == variable else literal
                for literal in clause
            }
        )
    return IndexedCNF.from_clauses(formula.variables, clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("enforcer", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--terminal", type=int, default=1)
    args = parser.parse_args()

    enforcer = read_dimacs(args.enforcer)
    flipped = flip_variable(enforcer, args.terminal)
    left_signature = terminal_signature(enforcer, (args.terminal,))
    right_signature = terminal_signature(flipped, (args.terminal,))
    value, left_entry, right_entry = compose_closed_signatures(
        left_signature, right_signature
    )
    composed = glue_formulas_on_terminals(
        enforcer, (args.terminal,), flipped, (args.terminal,)
    )
    audit = exact_322_audit(composed)
    if not all(audit.values()):
        raise AssertionError(f"composed enforcer base failed audit: {audit}")
    if value != 1:
        raise AssertionError(f"expected composed value one, got {value}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = dimacs_text(
        composed,
        "SAT 2024 E_(3,2,2) glued to a terminal-flipped copy; beta=1 by terminal signatures",
    )
    args.output.write_text(rendered, encoding="ascii")
    receipt = {
        "schema": "bilateral-deficiency/enforcer-composition/v1",
        "source": "Zhang-Peitl-Szeider SAT 2024 Appendix A.1 E_(3,2,2)",
        "source_doi": "10.4230/LIPIcs.SAT.2024.31",
        "enforcer": args.enforcer.name,
        "enforcer_sha256": hashlib.sha256(args.enforcer.read_bytes()).hexdigest(),
        "output": args.output.name,
        "output_sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
        "terminal": args.terminal,
        "variables": composed.variables,
        "clauses": len(composed.clauses),
        "audit": audit,
        "beta": value,
        "left_minimizing_witness": assignment_text(left_entry.witness),
        "right_minimizing_witness": assignment_text(right_entry.witness),
        "left_signature": signature_json(left_signature),
        "right_signature": signature_json(right_signature),
        "proof_rule": "exact two-gadget terminal min-plus composition",
        "assurance_boundary": (
            "The finite local signatures are exhaustive receipts and the "
            "composition rule is proved in TERMINAL_CALCULUS.md. Formula "
            "isomorphism to any previously supplied base is a separate audit."
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(args.output), "beta": value, "audit": audit}))


if __name__ == "__main__":
    main()
