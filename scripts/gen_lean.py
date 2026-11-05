#!/usr/bin/env python3
"""Generate the Lean certificate-data block from the arXiv S(8) coloring.

Input : upstream-data/S8_n5372.txt -- the ancillary coloring of arXiv:2610.31362
        (Chen, Zhu, Long), digits 1..8, one per integer 1..5372.
Output: the `cert : List (Fin 8)` literal (colors re-indexed to 0..7) written
        into the proof module. Run from the repo root:  python3 scripts/gen_lean.py
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "upstream-data" / "S8_n5372.txt"
TARGET = ROOT / "SchurNumber8" / "LeapsInBounds" / "Proofs" / "Schur8Lower5372.lean"
N = 5372
K = 8


def main() -> None:
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    digits = "".join(raw.decode().split())
    if len(digits) != N or not set(digits) <= set("12345678"):
        sys.exit(f"unexpected certificate: len={len(digits)}")
    colors = [int(ch) - 1 for ch in digits]  # 0-indexed
    body = "[" + ", ".join(str(c) for c in colors) + "]"
    lines = [body[i : i + 100] for i in range(0, len(body), 100)]
    block = "\n".join("  " + ln for ln in lines)

    text = TARGET.read_text()
    new, nsub = re.subn(
        r"(def cert : List \(Fin 8\) :=)\s*\[.*?\]",
        lambda m: m.group(1) + "\n" + block,
        text,
        count=1,
        flags=re.S,
    )
    if nsub != 1:
        sys.exit("cert literal not found in " + str(TARGET))
    new = re.sub(r"-- SHA-256 [0-9a-f]{64}", f"-- SHA-256 {sha}", new)
    TARGET.write_text(new)
    print(f"updated {TARGET} ({len(colors)} colors, sha256 {sha})")


if __name__ == "__main__":
    main()
