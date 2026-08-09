#!/usr/bin/env python3
"""Replay the attributed enforcer-composition proof that beta = 1."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from bd_core import FALSE, TRUE, UNASSIGNED, bilateral_deficiency, is_bilateral, read_dimacs


ROOT = Path(__file__).resolve().parent
ENFORCER = ROOT / "instances" / "sat2024_e322_enforcer.cnf"
FORMULA = ROOT / "instances" / "sat2024_enforcer_composition.cnf"
COMPOSITION_RECEIPT = ROOT / "receipts" / "sat2024-enforcer-composition.json"
ENCODING = ROOT / "proof" / "enforcer-composition-beta-le-0.cnf"
ENCODING_MAP = ROOT / "proof" / "enforcer-composition-beta-le-0-map.json"
DIRECT_LRAT = ROOT / "proof" / "enforcer-composition-direct.lrat"
COMPOSITION_GENERATOR = ROOT / "generate_enforcer_base.py"
THRESHOLD_GENERATOR = ROOT / "generate_positive_base_cnf.py"
LEAN_WRAPPER = ROOT / "lean_lrat_check.lean"
DEFAULT_LRAT_CHECKER = ROOT / "third_party" / "drat-trim" / "lrat-check"
LRAT_CHECKER_SOURCE = ROOT / "third_party" / "drat-trim" / "lrat-check.c"
PINNED_COMMIT = ROOT / "third_party" / "drat-trim" / "PINNED_COMMIT"
UPPER_WITNESS = "100*****1******"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def check_upper_witness() -> dict[str, object]:
    formula = read_dimacs(FORMULA)
    assignment = tuple(
        UNASSIGNED if symbol == "*" else TRUE if symbol == "1" else FALSE
        for symbol in UPPER_WITNESS
    )
    if len(assignment) != formula.variables:
        raise ValueError("upper witness has the wrong length")
    if not is_bilateral(formula, assignment):
        raise ValueError("upper witness is not bilateral")
    value = bilateral_deficiency(formula, assignment)
    if value != 1:
        raise ValueError(f"upper witness has deficiency {value}, expected 1")
    return {"witness": UPPER_WITNESS, "deficiency": value}


def regenerate_and_compare() -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="bd-enforcer-proof-") as directory:
        temporary = Path(directory)
        regenerated_formula = temporary / FORMULA.name
        regenerated_receipt = temporary / COMPOSITION_RECEIPT.name
        composition = subprocess.run(
            [
                sys.executable,
                str(COMPOSITION_GENERATOR),
                str(ENFORCER),
                str(regenerated_formula),
                "--receipt",
                str(regenerated_receipt),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if composition.returncode != 0:
            raise RuntimeError(
                "composition regeneration failed:\n"
                + composition.stdout
                + composition.stderr
            )
        if regenerated_formula.read_bytes() != FORMULA.read_bytes():
            raise ValueError("regenerated composition formula differs")
        if regenerated_receipt.read_bytes() != COMPOSITION_RECEIPT.read_bytes():
            raise ValueError("regenerated composition receipt differs")

        regenerated_encoding = temporary / ENCODING.name
        regenerated_map = temporary / ENCODING_MAP.name
        threshold = subprocess.run(
            [
                sys.executable,
                str(THRESHOLD_GENERATOR),
                str(regenerated_formula),
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
        if threshold.returncode != 0:
            raise RuntimeError(
                "threshold regeneration failed:\n"
                + threshold.stdout
                + threshold.stderr
            )
        if regenerated_encoding.read_bytes() != ENCODING.read_bytes():
            raise ValueError("regenerated threshold CNF differs")
        if regenerated_map.read_bytes() != ENCODING_MAP.read_bytes():
            raise ValueError("regenerated threshold map differs")

    return {
        "enforcer_sha256": sha256(ENFORCER),
        "formula_sha256": sha256(FORMULA),
        "composition_receipt_sha256": sha256(COMPOSITION_RECEIPT),
        "composition_generator_sha256": sha256(COMPOSITION_GENERATOR),
        "threshold_generator_sha256": sha256(THRESHOLD_GENERATOR),
        "encoding_sha256": sha256(ENCODING),
        "encoding_map_sha256": sha256(ENCODING_MAP),
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
        "checker_source_sha256": sha256(LRAT_CHECKER_SOURCE),
        "checker_commit": PINNED_COMMIT.read_text(encoding="utf-8").strip(),
        "proof_sha256": sha256(DIRECT_LRAT),
        "verified": True,
        "transcript": [
            line
            for line in transcript.strip().splitlines()
            if "verification time" not in line
        ],
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
        "wrapper_sha256": sha256(LEAN_WRAPPER),
        "proof_sha256": sha256(DIRECT_LRAT),
        "verified": True,
        "transcript": transcript.strip().splitlines(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lrat-checker", type=Path, default=DEFAULT_LRAT_CHECKER)
    parser.add_argument("--lean", default="lean")
    parser.add_argument("--skip-lean", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    receipt = {
        "schema": "bilateral-deficiency/enforcer-composition-proof/v1",
        "claim": "beta(sat2024_enforcer_composition.cnf) = 1",
        "source_doi": "10.4230/LIPIcs.SAT.2024.31",
        "upper_bound": check_upper_witness(),
        "regeneration": regenerate_and_compare(),
        "lower_bound": {
            "native_lrat": check_native(args.lrat_checker),
            "lean_lrat": {"skipped": True}
            if args.skip_lean
            else check_lean(args.lean),
        },
        "logical_inference": [
            "the general encoding lemma gives CNF satisfiable iff beta <= 0",
            "native and Lean LRAT checking prove the CNF unsatisfiable",
            "therefore beta >= 1",
            "the explicit bilateral witness has deficiency 1",
            "therefore beta = 1",
        ],
        "assurance_boundary": (
            "The finite terminal source is attributed to SAT 2024. LRAT proves "
            "the regenerated threshold CNF UNSAT; the written general encoding "
            "lemma remains the bridge to bilateral deficiency."
        ),
    }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
