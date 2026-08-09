#!/usr/bin/env python3
"""Verify the complete candidate certificate for beta(P) = 1.

This verifier regenerates the beta(P) <= 0 CNF, checks byte identity, validates
the explicit upper witness directly, invokes a separately compiled C LRAT
checker on two lower-bound proofs, and invokes Lean's verified LRAT checker on
the direct proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "instances" / "txgraffiti_15_20.cnf"
ENCODING = ROOT / "proof" / "positive-base-beta-le-0.cnf"
ENCODING_MAP = ROOT / "proof" / "positive-base-encoding-map.json"
LRAT_PROOF = ROOT / "proof" / "positive-base-unsat.lrat"
DIRECT_LRAT_PROOF = ROOT / "proof" / "positive-base-direct.lrat"
LEAN_WRAPPER = ROOT / "lean_lrat_check.lean"
GENERATOR = ROOT / "generate_positive_base_cnf.py"
DEFAULT_LRAT_CHECKER = ROOT / "third_party" / "drat-trim" / "lrat-check"
LRAT_CHECKER_SOURCE = ROOT / "third_party" / "drat-trim" / "lrat-check.c"
PINNED_COMMIT = ROOT / "third_party" / "drat-trim" / "PINNED_COMMIT"
UPPER_WITNESS = "0000***********"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variable_count: int | None = None
    declared_clause_count: int | None = None
    clauses: list[tuple[int, ...]] = []
    current: list[int] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError(f"bad DIMACS header: {line!r}")
            variable_count = int(fields[2])
            declared_clause_count = int(fields[3])
            continue
        for field in line.split():
            literal = int(field)
            if literal == 0:
                clauses.append(tuple(current))
                current = []
            else:
                current.append(literal)

    if variable_count is None or declared_clause_count is None:
        raise ValueError("missing DIMACS header")
    if current:
        raise ValueError("unterminated DIMACS clause")
    if len(clauses) != declared_clause_count:
        raise ValueError("DIMACS clause count mismatch")
    return variable_count, clauses


def check_upper_witness() -> dict[str, object]:
    variable_count, clauses = read_dimacs(INPUT)
    if len(UPPER_WITNESS) != variable_count:
        raise ValueError("upper witness has the wrong length")

    state = {
        index: symbol for index, symbol in enumerate(UPPER_WITNESS, start=1)
    }
    if any(symbol not in {"0", "1", "*"} for symbol in state.values()):
        raise ValueError("upper witness contains an invalid state")

    residual_indices: list[int] = []
    for clause_index, clause in enumerate(clauses, start=1):
        satisfied = False
        for literal in clause:
            symbol = state[abs(literal)]
            if symbol == "*":
                continue
            value = symbol == "1"
            if (literal > 0 and value) or (literal < 0 and not value):
                satisfied = True
                break
        if not satisfied:
            residual_indices.append(clause_index)

    unassigned = [variable for variable, symbol in state.items() if symbol == "*"]
    for variable in unassigned:
        positive = any(
            variable in clauses[index - 1] for index in residual_indices
        )
        negative = any(
            -variable in clauses[index - 1] for index in residual_indices
        )
        if not positive or not negative:
            raise ValueError(f"upper witness is not bilateral at variable {variable}")

    deficiency = len(residual_indices) - len(unassigned)
    if deficiency != 1:
        raise ValueError(f"upper witness has deficiency {deficiency}, expected 1")
    return {
        "witness": UPPER_WITNESS,
        "residual_clause_indices": residual_indices,
        "residual_clause_count": len(residual_indices),
        "unassigned_variable_count": len(unassigned),
        "deficiency": deficiency,
    }


def regenerate_and_compare() -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="bd-positive-proof-") as directory:
        temporary = Path(directory)
        regenerated_cnf = temporary / "encoding.cnf"
        regenerated_map = temporary / "encoding-map.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                str(INPUT),
                str(regenerated_cnf),
                "--map",
                str(regenerated_map),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "encoding regeneration failed:\n"
                + completed.stdout
                + completed.stderr
            )
        if regenerated_cnf.read_bytes() != ENCODING.read_bytes():
            raise ValueError("regenerated CNF differs from the packaged encoding")
        if regenerated_map.read_bytes() != ENCODING_MAP.read_bytes():
            raise ValueError("regenerated map differs from the packaged map")

    map_data = json.loads(ENCODING_MAP.read_text(encoding="utf-8"))
    if map_data["input_sha256"] != sha256(INPUT):
        raise ValueError("encoding map does not bind the canonical input")
    if map_data["encoding_sha256"] != sha256(ENCODING):
        raise ValueError("encoding map does not bind the generated CNF")
    return {
        "input_sha256": sha256(INPUT),
        "generator_sha256": sha256(GENERATOR),
        "encoding_sha256": sha256(ENCODING),
        "encoding_map_sha256": sha256(ENCODING_MAP),
    }


def check_lrat(checker: Path, proof: Path) -> dict[str, object]:
    if not checker.is_file():
        raise FileNotFoundError(f"LRAT checker not found: {checker}")
    completed = subprocess.run(
        [str(checker), str(ENCODING), str(proof)],
        check=False,
        capture_output=True,
        text=True,
    )
    transcript = completed.stdout + completed.stderr
    if completed.returncode != 0 or "c VERIFIED" not in transcript:
        raise RuntimeError("LRAT verification failed:\n" + transcript)
    try:
        checker_label = str(checker.resolve().relative_to(ROOT))
    except ValueError:
        checker_label = str(checker.resolve())
    normalized_transcript = [
        line
        for line in transcript.strip().splitlines()
        if "verification time" not in line
    ]
    return {
        "checker": checker_label,
        "checker_exit": completed.returncode,
        "checker_reported_verified": True,
        "lrat_proof": str(proof.relative_to(ROOT)),
        "lrat_proof_sha256": sha256(proof),
        "lrat_checker_source_sha256": sha256(LRAT_CHECKER_SOURCE),
        "lrat_checker_commit": PINNED_COMMIT.read_text(encoding="utf-8").strip(),
        "transcript": normalized_transcript,
    }


def check_lean(lean_command: str) -> dict[str, object]:
    resolved = shutil.which(lean_command)
    if resolved is None:
        raise FileNotFoundError(f"Lean executable not found: {lean_command}")
    completed = subprocess.run(
        [
            resolved,
            "--run",
            str(LEAN_WRAPPER),
            str(ENCODING),
            str(DIRECT_LRAT_PROOF),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    transcript = completed.stdout + completed.stderr
    if completed.returncode != 0 or "s LEAN_LRAT_VERIFIED" not in transcript:
        raise RuntimeError("Lean LRAT verification failed:\n" + transcript)
    return {
        "checker": "Lean Std.Tactic.BVDecide.LRAT",
        "checker_exit": completed.returncode,
        "checker_reported_verified": True,
        "lean_version": subprocess.run(
            [resolved, "--version"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "wrapper": str(LEAN_WRAPPER.relative_to(ROOT)),
        "wrapper_sha256": sha256(LEAN_WRAPPER),
        "lrat_proof": str(DIRECT_LRAT_PROOF.relative_to(ROOT)),
        "lrat_proof_sha256": sha256(DIRECT_LRAT_PROOF),
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
        "claim": "beta(txgraffiti_15_20.cnf) = 1",
        "upper_bound": check_upper_witness(),
        "encoding_regeneration": regenerate_and_compare(),
        "lower_bound": {
            "trimmed_lrat": check_lrat(args.lrat_checker, LRAT_PROOF),
            "direct_lrat": check_lrat(args.lrat_checker, DIRECT_LRAT_PROOF),
            "lean_direct_lrat": (
                {"skipped": True}
                if args.skip_lean
                else check_lean(args.lean)
            ),
        },
        "logical_inference": [
            "the encoding lemma gives: CNF satisfiable iff beta(P) <= 0",
            "the C-checked and Lean-checked LRAT derivations prove the CNF unsatisfiable",
            "therefore beta(P) >= 1",
            "the bilateral witness has deficiency 1, so beta(P) <= 1",
            "therefore beta(P) = 1",
        ],
        "assurance_boundary": (
            "The C and Lean LRAT checkers certify CNF unsatisfiability. The written "
            "encoding lemma is the mathematical bridge from that CNF to bilateral "
            "deficiency; the wrapper's DIMACS parser remains part of the trusted "
            "translation boundary for the Lean run."
        ),
    }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
