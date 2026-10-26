#!/usr/bin/env python3
"""P7 步 3：事实源声明与冻结哈希草稿。"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/事实源与冻结哈希_草稿.md"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    base = json.loads((ROOT / "spec/baseline_facts.json").read_text(encoding="utf-8"))
    p4 = json.loads((ROOT / "state/p4_freeze.json").read_text(encoding="utf-8"))
    manifest = ROOT / "state/p4_k_card_freeze_manifest.sha256"
    n_manifest = sum(1 for ln in manifest.read_text().splitlines() if ln.strip()) if manifest.is_file() else 0

    lines = [
        "# 事实源声明与冻结哈希（草稿）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`scripts/s12_export_p7_fact_source.py`\n\n",
        "## 十书原文（src_frozen）\n\n",
        "| 书码 | 文件名 | SHA-256（baseline） |\n",
        "|---|---|---|\n",
    ]
    for b in base.get("books", []):
        fn = b.get("file", "")
        code = b.get("code") or fn[:8]
        sha = b.get("sha256", "")
        lines.append(f"| {code} | {fn} | `{sha[:16]}…` |\n")

    lines.append("\n## P4 K 卡冻结\n\n")
    lines.append(f"- 冻结时间: {p4.get('frozen_at', '')}\n")
    lines.append(f"- 清单文件数: {p4.get('card_files', n_manifest)}（manifest 行 {n_manifest}）\n")
    lines.append(f"- 清单路径: `{p4.get('manifest_path', '')}`\n")
    lines.append("- 漂移检测: `scripts/s15_check_all.py` → P4 freeze manifest\n\n")

    zip_path = ROOT / "dist"
    packs = sorted(zip_path.glob("wujun-os-pack_*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if packs:
        z = packs[0]
        lines.append("## 最近交付包\n\n")
        lines.append(f"- 文件: `{z.name}`\n")
        lines.append(f"- SHA-256: `{sha256_file(z)}`\n")

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT}")


if __name__ == "__main__":
    main()
