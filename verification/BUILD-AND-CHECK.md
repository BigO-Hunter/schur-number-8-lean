# Verification log — S(8) ≥ 5372

Machine: macOS arm64 (Apple Silicon), Lean via elan.

## Toolchain / pins

- lean-toolchain: `leanprover/lean4:v4.35.0`
- Mathlib: `v4.35.0` (lake-manifest resolves the same commits as
  daniel-munro/leaps-in-bounds formal/ at 790ab900172c0c488db3124e89d6acbb80f8144f)

## Certificate provenance

- `upstream-data/S8_n5372.txt` downloaded from
  `https://arxiv.org/src/2610.31362v1/anc/data/S8_n5372.txt`
- SHA-256: `d0abd71d8de5749bcd12c6bbbb909033a3f8baa17a624364751669b6cb586d24`
- Matches line `data/S8_n5372.txt` in the authors' `SHA256SUMS` (also from the
  arXiv anc directory, `upstream-data/SHA256SUMS`).
- The authors' own checker (`upstream-data/check.py`) asserts this file equals
  the coloring their S(6) template construction produces, and that every class
  is sum-free.

## Build (standalone package)

```
$ cd SchurNumber8 && lake exe cache get && lake build
...
info: LeapsInBounds/Proofs/Schur8Lower5372.lean:292:0:
  'LeapsInBounds.Proofs.Schur8Lower5372.schur8_lower_5372'
  depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (515 jobs).
```

Explicit axiom check:

```
$ cat /tmp/axioms.lean
import LeapsInBounds.Proofs.Schur8Lower5372
#print axioms LeapsInBounds.Proofs.Schur8Lower5372.schur8_lower_5372
$ lake env lean /tmp/axioms.lean
'LeapsInBounds.Proofs.Schur8Lower5372.schur8_lower_5372'
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no `Lean.ofReduceBool` (i.e. no `native_decide`), no others.

## leaps-in-bounds end-to-end check

With `leaps-patch/certificates/schur/schur-8-lower-5372.yml` dropped into a
checkout of daniel-munro/leaps-in-bounds @ 790ab900172c0c488db3124e89d6acbb80f8144f
and the proof module built with their pins:

```
$ python3 scripts/check_certificates.py -v --lean --no-build
...
ok       schur-6-lower-537        (pre-existing witness cert)
ok       schur-7-lower-1696       (pre-existing witness cert)
ok       schur-8-lower-5372       (this work)
...
Checked 737 certificates: 737 ok
```

Their `--lean` path (scripts/check_lean.lean) imports the proof module, replays
every declaration in it through the kernel on top of the trusted environment,
compares the theorem's type with the expected `LeapsInBounds.Schur.LowerBound 8
5372` built syntactically from their trusted statement, and walks the axiom
graph against the allowlist `[propext, Classical.choice, Quot.sound]`.

## Timing

Full rebuild of the proof module: ~15 s (the `cert_ok` `by decide` dominates;
it evaluates 8 bitmasks × 5372 membership/shift checks).
