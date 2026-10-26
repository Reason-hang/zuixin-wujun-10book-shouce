#!/usr/bin/env python3
"""S17: Generate SHA-256 manifest for P4 step-12 K-card freeze (data/cards only)."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cards-root", default="data/cards", help="Root directory of unit JSON files")
    p.add_argument("--out", default="state/p4_k_card_freeze_manifest.sha256")
    p.add_argument("--meta", default="state/p4_freeze.json", help="Freeze metadata JSON")
    args = p.parse_args()
    root = Path(args.cards_root)
    files = sorted(root.rglob("*.json"))
    lines = []
    for f in files:
        rel = f.as_posix()
        lines.append(f"{sha256_file(f)}  {rel}\n")
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    meta = {
        "frozen_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "card_files": len(files),
        "manifest_path": args.out,
        "note": "Run only after P4 step 11+13 user sign-off",
    }
    Path(args.meta).write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"files={len(files)} manifest={args.out} meta={args.meta}")


if __name__ == "__main__":
    main()
