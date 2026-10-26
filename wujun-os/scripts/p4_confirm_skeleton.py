#!/usr/bin/env python3
"""Mark P4 step-13 skeleton confirmation in dictionary change report."""
from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

REPORT = Path("logs/p4_step13_dictionary_change_report_20261026.md")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--i-authorized", action="store_true")
    args = p.parse_args()
    if not args.i_authorized:
        raise SystemExit("Refused: pass --i-authorized after user says 确认骨架 in chat")
    text = REPORT.read_text(encoding="utf-8")
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    text = re.sub(
        r"`user_confirmed_skeleton`: \*\*no\*\*.*",
        f"`user_confirmed_skeleton`: **yes** @ {ts}",
        text,
        count=1,
    )
    REPORT.write_text(text, encoding="utf-8")
    print(f"updated {REPORT}")


if __name__ == "__main__":
    main()
