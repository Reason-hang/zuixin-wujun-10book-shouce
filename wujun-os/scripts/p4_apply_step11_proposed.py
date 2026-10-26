#!/usr/bin/env python3
"""Copy proposed step-11 spotcheck to authoritative CSV (run only after user chat authorization)."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PROPOSED = Path("logs/p4_step11_proposed_user_verdicts.csv")
OFFICIAL = Path("logs/p4_step11_user_spotcheck_20.csv")
BACKUP = Path("logs/p4_step11_user_spotcheck_20.csv.bak")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--i-authorized", action="store_true", help="Required: user said 采纳提议稿 in chat")
    args = p.parse_args()
    if not args.i_authorized:
        raise SystemExit("Refused: pass --i-authorized only after user authorization in chat")
    if not PROPOSED.is_file():
        raise SystemExit(f"Missing {PROPOSED}")
    if OFFICIAL.is_file() and OFFICIAL.read_text(encoding="utf-8").strip():
        first = OFFICIAL.read_text(encoding="utf-8").splitlines()
        if len(first) > 1 and any("," in ln and ln.split(",")[4].strip() for ln in first[1:]):
            raise SystemExit("Official CSV already has user_verdict; abort")
    if OFFICIAL.is_file():
        shutil.copy2(OFFICIAL, BACKUP)
    shutil.copy2(PROPOSED, OFFICIAL)
    print(f"copied {PROPOSED} -> {OFFICIAL}")


if __name__ == "__main__":
    main()
