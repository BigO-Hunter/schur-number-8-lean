# leaps-in-bounds contribution package (prepared, not submitted)

This directory contains everything needed to add `S(8) ≥ 5372` to
[daniel-munro/leaps-in-bounds](https://github.com/daniel-munro/leaps-in-bounds)
as a `kind: lean` certificate — **held for the ASK FIRST route request**
(bigospeedrun/verifier issue) before anything is opened upstream.

## Files

- `certificates/schur/schur-8-lower-5372.yml` — drop into `certificates/schur/`.
  Constant `schur-8` is already a valid constant there (k ranges 1..9) and
  `chen-zhu-long-2026` is already a registered source whose notes even
  anticipate this corollary ("S(8) >= 5372 follows from S(6) >= 537 by a
  recurrence").
- `certificates/schur/schur-8-lower-5372.txt` — the witness in leaps'
  0-indexed `coloring` format (digits 0..7), for human inspection and their
  Python witness checker. Not required for `kind: lean`.
- `formal/LeapsInBounds/Proofs/Schur8Lower5372.lean` — drop into
  `formal/LeapsInBounds/Proofs/`. Byte-identical to
  `SchurNumber8/LeapsInBounds/Proofs/Schur8Lower5372.lean` in this repo.
  The module name is under their trusted `LeapsInBounds.Proofs.*` prefix and
  imports only their `LeapsInBounds.Statements.Schur`.

## Verification already run against leaps-in-bounds @ 790ab900172c0c488db3124e89d6acbb80f8144f

- `python scripts/check_certificates.py --lean --no-build` with this yml added:
  **737/737 certificates ok** (was 736/736 before, with 461 Lean proofs
  skipped → 462 checked; their kernel replay + axiom walk accepted the new
  module).
- Their checker's allowlist is exactly `[propext, Classical.choice,
  Quot.sound]`; the theorem's `#print axioms` is exactly that list.

## Apply

```bash
cd leaps-in-bounds
cp -R /path/to/schur-number-8-lean/leaps-patch/certificates/schur/. certificates/schur/
cp /path/to/schur-number-8-lean/leaps-patch/formal/LeapsInBounds/Proofs/Schur8Lower5372.lean \
   formal/LeapsInBounds/Proofs/
cd formal && lake build
cd .. && python scripts/check_certificates.py --lean
```
