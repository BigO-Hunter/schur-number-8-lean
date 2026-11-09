# S(8) ≥ 5372 — Lean-verified

A machine-checked proof, in Lean 4 + Mathlib, that the eight-color Schur
certificate published as an ancillary file of arXiv:2610.31362 is valid:

```lean
theorem schur8_lower_5372 : LeapsInBounds.Schur.LowerBound 8 5372
```

where `LeapsInBounds.Schur.LowerBound k n` (the trusted statement of
[daniel-munro/leaps-in-bounds](https://github.com/daniel-munro/leaps-in-bounds))
is `∃ c : ℕ → Fin k, ¬ HasMonoSum k n c`, i.e. some `k`-coloring of `1..n` has
no monochromatic solution to `x + y = z` with `x = y` allowed — the Schur
number definition. So this is **S(8) ≥ 5372**.

**Read NOTICE first: the mathematics is Chen–Zhu–Long's (arXiv:2610.31362);
this repo only adds the Lean verification.**

## Status

- Axioms of the main theorem: `propext, Classical.choice, Quot.sound` — the
  standard three only. No `sorry`, no `native_decide`, no extra axioms.
- Accepted by the leaps-in-bounds checker: `python scripts/check_certificates.py
  --lean` reports **737/737 certificates ok** with `schur-8-lower-5372` added
  (their checker replays every proof-module declaration through the kernel and
  walks the axiom graph against its allowlist).
- Toolchain: `leanprover/lean4:v4.35.0`, Mathlib `v4.35.0` — the pins used by
  leaps-in-bounds' `formal/`.

## Layout

```
NOTICE                      attribution and provenance (read this first)
upstream-data/              arXiv:2610.31362 ancillary files, verbatim:
                            data/S8_n5372.txt (the certificate), certificate.col,
                            solutions537.txt, check.py (authors' checker;
                            `cd upstream-data && python3 check.py` passes),
                            SHA256SUMS
SchurNumber8/               standalone Lake package
  LeapsInBounds/Statements/Schur.lean       trusted statement (vendored)
  LeapsInBounds/Proofs/Schur8Lower5372.lean  the proof
leaps-patch/                ready-to-apply contribution to leaps-in-bounds:
  certificates/schur/schur-8-lower-5372.yml   certificate metadata
  certificates/schur/schur-8-lower-5372.txt   witness (0-indexed, for humans)
  formal/LeapsInBounds/Proofs/Schur8Lower5372.lean  identical proof module
scripts/gen_lean.py         regenerates the Lean data from the downloaded file
verification/               captured build/check/axiom output
```

## Build

```bash
git clone https://github.com/darkhipo/schur-number-8-lean
cd schur-number-8-lean/SchurNumber8
lake exe cache get   # fetches Mathlib oleans (~2 GB, mostly cache hits)
lake build           # ~20 s after cache; prints the #print axioms line
```

Expected final line:

```
info: ... 'LeapsInBounds.Proofs.Schur8Lower5372.schur8_lower_5372'
depends on axioms: [propext, Classical.choice, Quot.sound]
```

## How the proof works

`Schur8Lower5372.lean` (291 lines, most of it data):

1. `cert : List (Fin 8)` — the 5372 colors, generated from
   `upstream-data/data/S8_n5372.txt` by `scripts/gen_lean.py` (colors re-indexed
   from 1..8 to 0..7; SHA-256 in the file header).
2. `maskOf k` — per-color bitmask, derived from `cert` *inside* Lean, so the
   data lives in exactly one place.
3. `cert_ok` — the only kernel-heavy step: a single `by decide` over
   8 × 5372 boolean checks (`Nat.testBit`, `Nat.shiftLeft`, `Nat.land` are
   GMP-fast in the kernel). It proves every color class sum-free within
   `1..5372`: for each member `x`, `(m <<< x) &&& m == 0`.
4. A short bit-arithmetic bridge (`testBit_mask`, `mem_bit`) turns `cert_ok`
   into the quantified `¬ HasMonoSum 8 5372 colorOf`. No pairwise
   enumeration of the 14.4M pairs is ever evaluated — the statement is not
   weakened, only the checker is optimized.

## Relation to known results

- S(6) ≥ 537 and S(7) ≥ 1696 were already carried by leaps-in-bounds as
  Python-checked witness certificates (`kind: witness`); S(6) is from the
  same arXiv paper. Nothing here claims novelty for those.
- What is new here: the **first Lean-verified** certificate for
  **S(8) ≥ 5372** (a corollary the paper itself derives via the Bengone et
  al. width-10 template), contributed as a `kind: lean` certificate to
  leaps-in-bounds, which previously had no Lean Schur proofs.
  PR: https://github.com/daniel-munro/leaps-in-bounds/pull/1

## License

Licensed under the CFSF License — see [LICENSE](LICENSE) ([github.com/darkhipo/cfsf](https://github.com/darkhipo/cfsf)) for this repo's original content; the vendored statement file and the
redistributed arXiv ancillary files remain the work of their authors (see
NOTICE).

---

## Why this repo is up

Reproducible verified bounds: a kernel-only checker for the published S(8) ≥ 5372 certificate — anyone can recheck the arXiv ancillary claim without trusting it.

[BigO-Hunter](https://github.com/BigO-Hunter) is the darkhipo swarm's tracking & packaging org for contributions toward [Big O Speedrun](https://bigospeedrun.com) — a companion, never the project. Org story: [profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).

## What work can be done here

The checker is complete. Open work: independent reruns of the kernel-only check; S(9) and beyond need new certificates, not reruns.

