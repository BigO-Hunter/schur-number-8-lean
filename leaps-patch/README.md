# leaps-in-bounds contribution package

This directory contains the contribution prepared for
[daniel-munro/leaps-in-bounds](https://github.com/daniel-munro/leaps-in-bounds),
which owns Schur-number evidence review. Schur evidence belongs there, not on
a separate BigO board — see the redirect note on
bigospeedrun/verifier#153.

## Files (all three are part of the contribution)

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
  imports only their existing trusted `LeapsInBounds.Statements.Schur` — the
  statement file itself is NOT part of the contribution.

## Verification already run against leaps-in-bounds @ 790ab900172c0c488db3124e89d6acbb80f8144f

- `python scripts/check_certificates.py --lean --no-build` with this yml added:
  **737/737 certificates ok** (their kernel replay + axiom walk accepted the
  new module; allowlist is exactly `propext, Classical.choice, Quot.sound`).

## Apply

```bash
cd leaps-in-bounds
cp -R /path/to/schur-number-8-lean/leaps-patch/certificates/schur/. certificates/schur/
cp /path/to/schur-number-8-lean/leaps-patch/formal/LeapsInBounds/Proofs/Schur8Lower5372.lean \
   formal/LeapsInBounds/Proofs/
cd formal && lake build
cd .. && python scripts/check_certificates.py --lean
```
