#!/usr/bin/env python3
"""Integration and mutation tests for generated benchmark proof packages."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


BASE = Path(__file__).resolve().parent


class WorkflowTests(unittest.TestCase):
    def run_command(self, *arguments: str, success: bool = True):
        completed = subprocess.run(
            list(arguments), cwd=BASE, text=True, capture_output=True, check=False
        )
        if success and completed.returncode != 0:
            self.fail(completed.stdout + completed.stderr)
        if not success and completed.returncode == 0:
            self.fail("corrupted workflow unexpectedly passed")
        return completed

    def test_generated_graph_is_bound_and_corruption_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "benchmark"
            self.run_command(
                "python3",
                "generate_benchmark.py",
                "--family",
                "general",
                "--target",
                "2",
                "--output-dir",
                str(output),
            )
            self.run_command("python3", "verify_benchmark.py", str(output))
            graph = output / "formula_graph.edgelist"
            graph.write_text(graph.read_text(encoding="ascii") + "0 999\n", encoding="ascii")
            rejected = self.run_command(
                "python3", "verify_benchmark.py", str(output), success=False
            )
            self.assertIn("edge-list hash mismatch", rejected.stderr)

    def test_threshold_compiler_preserves_frozen_zero_encoding(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "positive.cnf"
            mapping = Path(temporary) / "positive-map.json"
            self.run_command(
                "python3",
                "generate_positive_base_cnf.py",
                "instances/txgraffiti_15_20.cnf",
                str(output),
                "--map",
                str(mapping),
            )
            self.assertEqual(
                output.read_bytes(),
                (BASE / "proof/positive-base-beta-le-0.cnf").read_bytes(),
            )
            self.assertEqual(
                mapping.read_bytes(),
                (BASE / "proof/positive-base-encoding-map.json").read_bytes(),
            )

    @unittest.skipUnless(shutil.which("lean"), "Lean is not installed")
    def test_lean_terminal_signature(self):
        completed = self.run_command(
            "lean", "--run", "lean_terminal_signature.lean"
        )
        self.assertIn("checked assignments: 6561", completed.stdout)
        self.assertIn("s LEAN_TERMINAL_SIGNATURE_VERIFIED", completed.stdout)

    @unittest.skipUnless(shutil.which("cadical"), "CaDiCaL is not installed")
    def test_general_threshold_compiler_has_exact_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "unit-pair.cnf"
            source.write_text("p cnf 1 2\n1 0\n-1 0\n", encoding="ascii")
            for threshold, expected_status in ((0, 20), (1, 10)):
                output = Path(temporary) / f"threshold-{threshold}.cnf"
                mapping = Path(temporary) / f"threshold-{threshold}.json"
                self.run_command(
                    "python3",
                    "generate_positive_base_cnf.py",
                    str(source),
                    str(output),
                    "--map",
                    str(mapping),
                    "--threshold",
                    str(threshold),
                )
                completed = self.run_command(
                    "cadical", "-q", str(output), success=False
                )
                self.assertEqual(completed.returncode, expected_status)
                metadata = json.loads(mapping.read_text(encoding="utf-8"))
                if threshold != 0:
                    self.assertEqual(metadata["threshold"], threshold)

    @unittest.skipUnless(shutil.which("cadical"), "CaDiCaL is not installed")
    def test_formula_and_graph_threshold_compilers_agree(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "unit-pair.cnf"
            source.write_text("p cnf 1 2\n1 0\n-1 0\n", encoding="ascii")
            for threshold, expected_status in ((0, 20), (1, 10)):
                statuses = []
                for compiler in ("formula", "graph"):
                    output = Path(temporary) / f"{compiler}-{threshold}.cnf"
                    mapping = Path(temporary) / f"{compiler}-{threshold}.json"
                    script = (
                        "generate_positive_base_cnf.py"
                        if compiler == "formula"
                        else "generate_graph_threshold_cnf.py"
                    )
                    self.run_command(
                        "python3",
                        script,
                        str(source),
                        str(output),
                        "--map",
                        str(mapping),
                        "--threshold",
                        str(threshold),
                    )
                    result = self.run_command(
                        "cadical", "-q", str(output), success=False
                    )
                    statuses.append(result.returncode)
                self.assertEqual(statuses, [expected_status, expected_status])

    def test_cleanroom_threshold_audit_and_semantic_corpus(self):
        completed = self.run_command(
            "python3",
            "verify_threshold_encoding_cleanroom.py",
            "instances/txgraffiti_15_20.cnf",
            "proof/positive-base-beta-le-0.cnf",
            "proof/positive-base-encoding-map.json",
        )
        receipt = json.loads(completed.stdout)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["semantic_corpus"]["case_count"], 7)
        self.assertTrue(
            receipt["structural_audit"]["canonical_clause_order_exact"]
        )

    def test_cleanroom_threshold_audit_rejects_rehashed_clause_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            source = temporary_path / "txgraffiti_15_20.cnf"
            encoding = temporary_path / "positive-base-beta-le-0.cnf"
            mapping = temporary_path / "positive-base-encoding-map.json"
            shutil.copyfile(BASE / "instances/txgraffiti_15_20.cnf", source)
            shutil.copyfile(BASE / "proof/positive-base-beta-le-0.cnf", encoding)
            raw_map = json.loads(
                (BASE / "proof/positive-base-encoding-map.json").read_text(
                    encoding="utf-8"
                )
            )

            lines = encoding.read_text(encoding="ascii").splitlines()
            self.assertEqual(lines[4], "1 2 3 0")
            lines[4] = "1 2 -3 0"
            mutated = "\n".join(lines) + "\n"
            encoding.write_text(mutated, encoding="ascii")
            raw_map["encoding_sha256"] = hashlib.sha256(
                mutated.encode("ascii")
            ).hexdigest()
            raw_map["input"] = source.name
            mapping.write_text(
                json.dumps(raw_map, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            completed = self.run_command(
                "python3",
                "verify_threshold_encoding_cleanroom.py",
                str(source),
                str(encoding),
                str(mapping),
                "--skip-semantic-corpus",
                success=False,
            )
            self.assertIn("clause multiset mismatch", completed.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
