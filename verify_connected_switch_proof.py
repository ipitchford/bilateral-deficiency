#!/usr/bin/env python3
"""Replay the proof that the connected occurrence switch has beta = 1."""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from bd_core import (
    FALSE,
    TRUE,
    UNASSIGNED,
    bilateral_deficiency,
    is_bilateral,
    read_dimacs,
)
from connector_search import exact_322_audit, occurrence_switch


ROOT = Path(__file__).resolve().parent
POSITIVE_BASE = ROOT / "instances" / "txgraffiti_15_20.cnf"
CONNECTOR_DIR = ROOT / "connectors" / "pp-beta1"
FORMULA = CONNECTOR_DIR / "connected-switch.cnf"
SEARCH_RECEIPT = CONNECTOR_DIR / "search-receipt.json"
ENCODING = CONNECTOR_DIR / "beta-le-0.cnf"
ENCODING_MAP = CONNECTOR_DIR / "beta-le-0-map.json"
DIRECT_LRAT = CONNECTOR_DIR / "beta-le-0-direct.lrat"
THRESHOLD_GENERATOR = ROOT / "generate_positive_base_cnf.py"
LEAN_WRAPPER = ROOT / "lean_lrat_check.lean"
DEFAULT_LRAT_CHECKER = ROOT / "third_party" / "drat-trim" / "lrat-check"
LRAT_CHECKER_SOURCE = ROOT / "third_party" / "drat-trim" / "lrat-check.c"
PINNED_COMMIT = ROOT / "third_party" / "drat-trim" / "PINNED_COMMIT"


@functools.cache
def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def assignment_from_text(text: str) -> tuple[int, ...]:
    symbols = {"*": UNASSIGNED, "0": FALSE, "1": TRUE}
    try:
        return tuple(symbols[symbol] for symbol in text)
    except KeyError as error:
        raise ValueError(f"invalid witness symbol: {error.args[0]!r}") from error


def check_formula_and_witness() -> dict[str, object]:
    receipt = json.loads(SEARCH_RECEIPT.read_text(encoding="utf-8"))
    formula = read_dimacs(FORMULA)
    audit = exact_322_audit(formula)
    if not all(audit.values()):
        raise ValueError(f"connected formula audit failed: {audit}")

    switch = receipt["switch"]
    source = read_dimacs(POSITIVE_BASE)
    reconstructed = occurrence_switch(
        source,
        source,
        int(switch["left_clause"]) - 1,
        int(switch["left_literal"]),
        int(switch["right_clause"]) - 1,
        int(switch["right_literal"]),
    )
    if reconstructed != formula:
        raise ValueError("occurrence-switch reconstruction differs from formula")

    witness_text = str(receipt["upper_witness"])
    witness = assignment_from_text(witness_text)
    if len(witness) != formula.variables:
        raise ValueError("upper witness has the wrong length")
    if not is_bilateral(formula, witness):
        raise ValueError("upper witness is not bilateral")
    value = bilateral_deficiency(formula, witness)
    if value != 1:
        raise ValueError(f"upper witness has deficiency {value}, expected 1")

    return {
        "audit": audit,
        "clauses": len(formula.clauses),
        "formula_sha256": sha256(FORMULA),
        "positive_base_sha256": sha256(POSITIVE_BASE),
        "switch": switch,
        "variables": formula.variables,
        "witness": witness_text,
        "witness_deficiency": value,
    }


def regenerate_encoding() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="bd-connected-proof-") as directory:
        temporary = Path(directory)
        regenerated_encoding = temporary / ENCODING.name
        regenerated_map = temporary / ENCODING_MAP.name
        completed = subprocess.run(
            [
                sys.executable,
                str(THRESHOLD_GENERATOR),
                str(FORMULA),
                str(regenerated_encoding),
                "--map",
                str(regenerated_map),
                "--threshold",
                "0",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "threshold regeneration failed:\n"
                + completed.stdout
                + completed.stderr
            )
        if regenerated_encoding.read_bytes() != ENCODING.read_bytes():
            raise ValueError("regenerated threshold CNF differs")
        if regenerated_map.read_bytes() != ENCODING_MAP.read_bytes():
            raise ValueError("regenerated threshold map differs")

    return {
        "encoding_map_sha256": sha256(ENCODING_MAP),
        "encoding_sha256": sha256(ENCODING),
        "generator_sha256": sha256(THRESHOLD_GENERATOR),
        "regenerated_byte_identical": True,
    }


def check_native(checker: Path) -> dict[str, object]:
    completed = subprocess.run(
        [str(checker), str(ENCODING), str(DIRECT_LRAT)],
        check=False,
        capture_output=True,
        text=True,
    )
    transcript = completed.stdout + completed.stderr
    if completed.returncode != 0 or "c VERIFIED" not in transcript:
        raise RuntimeError("native LRAT verification failed:\n" + transcript)
    try:
        checker_label = str(checker.resolve().relative_to(ROOT))
    except ValueError:
        checker_label = str(checker.resolve())
    return {
        "checker": checker_label,
        "checker_commit": PINNED_COMMIT.read_text(encoding="utf-8").strip(),
        "checker_source_sha256": sha256(LRAT_CHECKER_SOURCE),
        "proof_bytes": DIRECT_LRAT.stat().st_size,
        "proof_sha256": sha256(DIRECT_LRAT),
        "transcript": [
            line
            for line in transcript.strip().splitlines()
            if "verification time" not in line
        ],
        "verified": True,
    }


def check_lean(command: str) -> dict[str, object]:
    executable = shutil.which(command)
    if executable is None:
        raise FileNotFoundError(f"Lean executable not found: {command}")
    completed = subprocess.run(
        [executable, "--run", str(LEAN_WRAPPER), str(ENCODING), str(DIRECT_LRAT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    transcript = completed.stdout + completed.stderr
    if completed.returncode != 0 or "s LEAN_LRAT_VERIFIED" not in transcript:
        raise RuntimeError("Lean LRAT verification failed:\n" + transcript)
    return {
        "checker": "Lean Std.Tactic.BVDecide.LRAT",
        "lean_version": subprocess.run(
            [executable, "--version"], check=True, capture_output=True, text=True
        ).stdout.strip(),
        "proof_sha256": sha256(DIRECT_LRAT),
        "transcript": transcript.strip().splitlines(),
        "verified": True,
        "wrapper_sha256": sha256(LEAN_WRAPPER),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lrat-checker", type=Path, default=DEFAULT_LRAT_CHECKER)
    parser.add_argument("--lean", default="lean")
    parser.add_argument("--skip-lean", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    lower_bound = {"native_lrat": check_native(args.lrat_checker)}
    lower_bound["lean_lrat"] = (
        {"skipped": True} if args.skip_lean else check_lean(args.lean)
    )
    receipt = {
        "assurance_boundary": (
            "The occurrence switch and upper witness are checked against the "
            "independent formula semantics. LRAT proves the regenerated threshold "
            "CNF UNSAT; the written encoding lemma remains the bridge to beta > 0."
        ),
        "claim": "beta(connected-switch.cnf) = 1",
        "encoding": regenerate_encoding(),
        "formula_and_upper_bound": check_formula_and_witness(),
        "logical_inference": [
            "the explicit bilateral witness proves beta <= 1",
            "the general encoding lemma gives CNF satisfiable iff beta <= 0",
            "native and Lean LRAT checking prove the CNF unsatisfiable",
            "therefore beta >= 1",
            "therefore beta = 1",
        ],
        "lower_bound": lower_bound,
        "schema": "bilateral-deficiency/connected-switch-proof/v1",
    }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
