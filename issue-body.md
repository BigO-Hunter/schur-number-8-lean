**ASK-FIRST route request — not a Lean submission. No statement PR opened, no submit tool used.**

## Result

A **first Lean-verified certificate for S(8) ≥ 5372** — the eight-color Schur-number lower bound, in the exact statement shape used by [daniel-munro/leaps-in-bounds](https://github.com/daniel-munro/leaps-in-bounds), standard axioms only:

```lean
theorem schur8_lower_5372 : LeapsInBounds.Schur.LowerBound 8 5372
-- ∃ c : ℕ → Fin 8, ¬ HasMonoSum 8 5372 c   (x = y allowed; trusted statement file)
```

The mathematics is **not ours**: the certificate is `data/S8_n5372.txt` from the ancillary files of **arXiv:2610.31362** (Z. Chen, L. Zhu, F. Long, "A new lower bound for the sixth Schur number: S(6) ≥ 537"; repo [jeffchen006/Schur-Number-6](https://github.com/jeffchen006/Schur-Number-6)), SHA-256 `d0abd71d8de5749bcd12c6bbbb909033a3f8baa17a624364751669b6cb586d24`, verified against the authors' own `SHA256SUMS` on download. The paper derives S(8) ≥ 5372 from S(6) ≥ 537 via the Bengone et al. width-10 template; the eight-color file is their explicit corollary certificate. Full attribution is in the repo's `NOTICE`.

## What is actually novel

- S(6) ≥ 537 and S(7) ≥ 1696 **already exist** in leaps-in-bounds as `kind: witness` (Python-checked) certificates — claimed by nobody here.
- leaps-in-bounds has **no `kind: lean` Schur proofs at all** and **no `schur-8` certificate**; this repo adds the first Lean proof of `LowerBound 8 5372` against their trusted `Statements/Schur.lean`, plus a ready-to-apply `kind: lean` patch for their tree.

## Repo & commit

- https://github.com/darkhipo/schur-number-8-lean
- commit `c732a77472d96200d6ebe12612224b893f57d1c1` (branch `main`)
- `SchurNumber8/` is a standalone Lake package; `leaps-patch/` is the drop-in for leaps-in-bounds (`certificates/schur/schur-8-lower-5372.{yml,txt}` + `formal/LeapsInBounds/Proofs/Schur8Lower5372.lean`).
- Proof shape (292-line module, ~16 KB of it certificate data): per-color bitmask derived from the coloring *inside* Lean; the only kernel-heavy step is one `by decide` over 8 × 5372 boolean membership/shift checks (`Nat.testBit`/`shiftLeft`/`land`, GMP-fast in the kernel, ~15 s); a short bit-arithmetic bridge gives the quantified `¬ HasMonoSum`. No `native_decide`; no statement weakened — the pairwise quantifier is proved, only the checker is optimized.

## Build (standalone)

```
cd SchurNumber8 && lake exe cache get && lake build
# Build completed successfully (515 jobs); #print axioms re-emitted on every build
```

## Axiom audit

```
'LeapsInBounds.Proofs.Schur8Lower5372.schur8_lower_5372'
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no `Lean.ofReduceBool`, nothing else.

## Cross-check against leaps-in-bounds @ `790ab900172c0c488db3124e89d6acbb80f8144f`

With the patch yml added and the module built under their pins (lean `v4.35.0`, Mathlib `v4.35.0`):

```
python3 scripts/check_certificates.py --lean --no-build
ok  schur-6-lower-537   ok  schur-7-lower-1696   ok  schur-8-lower-5372
Checked 737 certificates: 737 ok
```

Their `--lean` path replays every proof-module declaration through the kernel and walks the axiom graph against their allowlist (exactly the standard three), and type-compares the theorem against `LeapsInBounds.Schur.LowerBound 8 5372` built syntactically from the trusted statement. `schur-8` is a registered constant there (`k` ∈ 1..9) and `chen-zhu-long-2026` is already a registered source whose notes anticipate this corollary.

## Request

1. Open a **`schur-numbers` board** (k-parameterized: S(1)..S(9) map to leap constants; this row = `schur-8`, lower bound 5372)?
2. If so, which evidence route do you want pinned:
   - **(a)** this standalone repo as the artifact (statement vendored verbatim from leaps-in-bounds, pins identical to theirs), or
   - **(b)** direct contribution of `leaps-patch/` to `daniel-munro/leaps-in-bounds` upstream (I hold the PR until you say go), with this repo kept as the provenance/build record?

Holding all of it until a maintainer answers.
