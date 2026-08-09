# Recorded environment

This file records the producer-side environment used during release
preparation on 2026-08-09. It is descriptive, not a claim that the mathematics
depends on this hardware or operating system.

## Recorded platform

| Component | Recorded value |
|---|---|
| Operating system | macOS 26.5.2, build 25F84 |
| Architecture | Apple arm64 |
| Python | CPython 3.14.6 |
| C++ compiler | Apple clang 21.0.0, C++17 mode |
| Lean | 4.32.1, commit `f054605aea4b840552cca2e725580bffd1e1b704` |
| Git | 2.50.1 |
| Pandoc | 3.9 |
| PDF renderer | Google Chrome 151.0.7922.76 |
| Native LRAT checker | `drat-trim` commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` |

## Core requirements

- Python 3 with only the standard library for the reference implementation,
  generators, verifiers, and tests.
- A C++17 compiler for `bd_exact.cpp`.
- POSIX `make` and a C compiler to build the pinned native LRAT checker.
- Sufficient memory and disk for the chosen proof layer.

Lean is required for the proof-assistant certificate paths but not for reading
the universal written proofs or running the Python reference calculations.
CaDiCaL 3.0 is needed only to regenerate solver proofs; packaged LRAT replay
does not require CaDiCaL.

## Resource distinction

- The compact positive-base and enforcer-composition proofs are suitable for
  routine replay.
- The connected-switch direct proof is 5,793,599,477 bytes and contains
  11,393,023 LRAT actions. Full native and Lean replay is an extended check and
  requires correspondingly larger local storage and runtime.

## Headline checks

The recorded local run reports 25 tests passing in normal Python mode and 25
tests passing under `python3 -O`. Tests that depend on optional executables are
explicitly skipped when those executables are absent; a run with skips is not
byte-for-byte equivalent to the full recorded environment.

Use the commands and expected transcripts in `REPRODUCIBILITY_SUPPLEMENT.md`.
Receipts bind important inputs, generated encodings, proof objects, and checker
sources by SHA-256.

## Portability boundary

Generated solver proofs need not be byte-identical across solver versions.
The packaged proof bytes and their hashes are normative. Successful execution
on another platform is valuable reproduction evidence only when its exact
scope, environment, inputs, and outputs are recorded; it is not automatically
an independent mathematical review.
