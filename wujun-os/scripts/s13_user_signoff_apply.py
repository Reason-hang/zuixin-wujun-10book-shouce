#!/usr/bin/env python3
"""在用户授权文件存在时，将 Agent 草稿写入正式签收列（须含 M3-确认 与 P6-代签 范围）。"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "logs/user_signoff_authorization.txt"
AC36 = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"
AC36_DRAFT = ROOT / "logs/ac36_recall_agent_draft_column_20261026.md"
G10 = ROOT / "out/覆盖与质检报告/G10②_盲抽单元表_草稿.md"
G10_DRAFT = ROOT / "logs/g10_blind_agent_draft_column_20261026.md"
SPOT = ROOT / "out/覆盖与质检报告/P6_用户抽查20张_草稿.md"
SPOT_DRAFT = ROOT / "logs/p6_spotcheck_agent_draft_20261026.md"
M3_PHRASE = "M3-确认：接受 v0.9.1 题面改版；三题均部分，判定见 m3_trial_feedback 表。"


def parse_auth_text(text: str) -> tuple[bool, set[str]]:
    if M3_PHRASE not in text:
        return False, set()
    scopes: set[str] = set()
    m = re.search(r"P6-代签[：:]\s*([^\n]+)", text)
    if m:
        for part in re.split(r"[,，\s]+", m.group(1).strip()):
            if part:
                scopes.add(part.upper())
    return True, scopes


def load_auth(path: Path) -> tuple[bool, set[str]]:
    if not path.is_file():
        return False, set()
    return parse_auth_text(path.read_text(encoding="utf-8"))


def parse_ac36_draft() -> dict[str, str]:
    out: dict[str, str] = {}
    if not AC36_DRAFT.is_file():
        return out
    for ln in AC36_DRAFT.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("| `C-"):
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 3:
            continue
        cid = parts[0].strip("`")
        sug = parts[2]
        val = "Y" if "Y（启发式）" in sug else "待复核"
        out[cid] = f"{val}（用户授权·{datetime.now().date()}）"
    return out


def apply_ac36(mapping: dict[str, str]) -> int:
    lines = AC36.read_text(encoding="utf-8").splitlines(keepends=True)
    n = 0
    out: list[str] = []
    for ln in lines:
        if ln.startswith("|") and "C-" in ln and not ln.startswith("| #"):
            parts = ln.strip().strip("|").split("|")
            if len(parts) >= 6 and parts[0].strip().isdigit():
                cid = parts[1].strip()
                if cid in mapping and not parts[5].strip():
                    parts[5] = f" {mapping[cid]} "
                    ln = "|" + "|".join(parts) + "|\n"
                    n += 1
        out.append(ln if ln.endswith("\n") else ln + "\n")
    if n:
        hdr = f"> 回读列部分由 `s13_user_signoff_apply.py` 于 {datetime.now().isoformat(timespec='seconds')} 写入（用户授权）。\n"
        if "user_signoff_apply" not in "".join(out[:8]):
            out.insert(4, hdr)
        AC36.write_text("".join(out), encoding="utf-8")
    return n


def parse_g10_draft() -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in G10_DRAFT.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or "单元 ID" in ln:
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) >= 3 and re.match(r"^[A-Z0-9]+-U\d+$", parts[0]):
            uid, draft = parts[0], parts[2]
            if draft.startswith("否"):
                out[uid] = "否"
            elif "待" in draft:
                out[uid] = "待复核"
            else:
                out[uid] = draft[:40]
    return out


def apply_g10(mapping: dict[str, str]) -> int:
    lines = G10.read_text(encoding="utf-8").splitlines(keepends=True)
    n = 0
    out: list[str] = []
    uid_in = re.compile(r"\|\s*[A-Z0-9]+\s*\|\s*([A-Z0-9]+-U\d+)\s*\|")
    for ln in lines:
        if not ln.startswith("|") or "---" in ln or "单元 ID" in ln:
            out.append(ln if ln.endswith("\n") else ln + "\n")
            continue
        m = uid_in.search(ln)
        if m and m.group(1) in mapping and re.search(r"\|\s*\|\s*$", ln.rstrip()):
            val = mapping[m.group(1)].replace("|", "｜")
            ln = re.sub(r"\|\s*\|\s*$", f"| {val} |", ln.rstrip()) + "\n"
            n += 1
        out.append(ln if ln.endswith("\n") else ln + "\n")
    if n:
        G10.write_text("".join(out), encoding="utf-8")
    return n


def parse_spot_draft() -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in SPOT_DRAFT.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("| V-"):
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) >= 7:
            vid, dj = parts[0], parts[6]
            if dj.startswith("ok"):
                out[vid] = "ok（用户授权·Agent草稿）"
            elif "FAIL" in dj:
                out[vid] = "FAIL"
            else:
                out[vid] = "待复核"
    return out


def apply_spot(mapping: dict[str, str]) -> int:
    lines = SPOT.read_text(encoding="utf-8").splitlines(keepends=True)
    n = 0
    out: list[str] = []
    for ln in lines:
        if ln.startswith("| V-"):
            parts = [p.strip() for p in ln.strip().strip("|").split("|")]
            if len(parts) >= 6:
                vid = parts[0]
                if vid in mapping and not parts[5].strip():
                    parts[5] = mapping[vid]
                    ln = "| " + " | ".join(parts) + " |\n"
                    n += 1
        out.append(ln if ln.endswith("\n") else ln + "\n")
    if n:
        SPOT.write_text("".join(out), encoding="utf-8")
    return n


def mark_m3_boards(auth_path: Path) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    (ROOT / "logs/m3_user_signoff_record.md").write_text(
        f"# M3 用户签收记录\n\n- 时间: {ts}\n- 源: `{auth_path.relative_to(ROOT)}`\n"
        f"- 短语: `{M3_PHRASE}`\n",
        encoding="utf-8",
    )
    wb = ROOT / "state/p5_workboard.md"
    old_wb = (
        "| 11 | M3 v0.9 用户试用 | 🔄 | 三题均**部分**；题面 **v0.9.1**（人读出处+国内电商）；待你确认后标 ✅ |"
    )
    new_wb = (
        "| 11 | M3 v0.9 用户试用 | ✅ | 用户授权文件；三题均**部分**（v0.9.1 题面） |"
    )
    if wb.is_file():
        t = wb.read_text(encoding="utf-8")
        if old_wb in t:
            wb.write_text(t.replace(old_wb, new_wb), encoding="utf-8")
    gap = ROOT / "logs/p5_acceptance_gap_20261026.md"
    if gap.is_file():
        t = gap.read_text(encoding="utf-8")
        t = t.replace(
            "| M3 v0.9.1 | 用户试用 3 问题 | 三题**部分**；题面改版见 `m3_trial_feedback_20261026.md`；需求文 `m3_user_feedback_requirements_20261026.md` | 🔄 待用户 `M3-确认` |",
            "| M3 v0.9.1 | 用户试用 3 问题 | 三题**部分**；v0.9.1 题面；`m3_user_signoff_record.md` | ✅ 用户授权 |",
        )
        t = t.replace(
            "**M3 步 11 待你确认 v0.9.1**",
            "**M3 步 11 ✅**（用户授权）；P6 人工项仍开放",
        )
        gap.write_text(t, encoding="utf-8")
    m3 = ROOT / "logs/m3_trial_feedback_20261026.md"
    if m3.is_file():
        t = m3.read_text(encoding="utf-8")
        t = t.replace(
            "| P5 步 11 | 🔄 **待你确认**：改版题面是否满足「能判定」；确认后可标 ✅ |",
            f"| P5 步 11 | ✅ **用户确认**（{ts}，`user_signoff_authorization.txt`） |",
        )
        m3.write_text(t, encoding="utf-8")
    ent = ROOT / "logs/p6_entry_criteria_20261026.md"
    if ent.is_file():
        t = ent.read_text(encoding="utf-8")
        t = t.replace(
            "| 2 | P5 达 v0.9 试用（M3） | ❌ | 待发 **`M3-确认：…`**；签收清单 `logs/p6_user_signoff_checklist_20261026.md` |",
            "| 2 | P5 达 v0.9 试用（M3） | ✅ | `m3_user_signoff_record.md`；P6 步 3/7/11 等仍待签收 |",
        )
        ent.write_text(t, encoding="utf-8")


def mark_p6_partial(scopes: set[str], ac_n: int, g10_n: int, spot_n: int) -> None:
    wb = ROOT / "state/p6_workboard.md"
    if not wb.is_file():
        return
    t = wb.read_text(encoding="utf-8")
    if "AC36" in scopes and ac_n:
        t = t.replace(
            "**正式回读列**待你填",
            f"**正式回读列**已填 {ac_n} 格（用户授权·启发式）",
        )
    if "G10" in scopes and g10_n:
        t = t.replace(
            "G10② 漏收列空",
            f"G10② 漏收列已填 {g10_n}（用户授权·草稿）",
            1,
        ) if "G10② 漏收列空" in t else t.replace(
            "**漏收列**待填",
            f"**漏收列**已填 {g10_n}（用户授权）",
        )
    if "SPOTCHECK20" in scopes and spot_n:
        t = t.replace(
            "**「你的判断」列**待你填",
            f"**「你的判断」列**已填 {spot_n}（用户授权·Agent草稿）",
        )
    wb.write_text(t, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", default=str(AUTH))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--accept-text",
        default="",
        help="写入 authorization 文件后执行（聊天原文，可含多行）",
    )
    args = ap.parse_args()
    auth_path = Path(args.auth)
    if args.accept_text.strip() and not args.dry_run:
        auth_path.write_text(args.accept_text.strip() + "\n", encoding="utf-8")
        print(f"wrote {auth_path}")
    elif args.accept_text.strip() and args.dry_run:
        ok, scopes = parse_auth_text(args.accept_text.strip())
        if not ok:
            print("SKIP: accept-text missing M3 phrase")
            return 0
        print(f"auth OK scopes={scopes or 'M3-only'} (dry-run, no writes)")
        return 0
    ok, scopes = load_auth(auth_path)
    if not ok:
        print(f"SKIP: missing auth or M3 phrase in {args.auth}")
        print(f"Create file with exact line: {M3_PHRASE}")
        return 0 if args.dry_run else 2
    print(f"auth OK scopes={scopes or 'M3-only'}")
    if args.dry_run:
        return 0
    mark_m3_boards(auth_path)
    ac_n = g10_n = spot_n = 0
    if "AC36" in scopes:
        ac_n = apply_ac36(parse_ac36_draft())
    if "G10" in scopes:
        g10_n = apply_g10(parse_g10_draft())
    if "SPOTCHECK20" in scopes:
        spot_n = apply_spot(parse_spot_draft())
    mark_p6_partial(scopes, ac_n, g10_n, spot_n)
    total = ac_n + g10_n + spot_n
    subprocess.run([sys.executable, "scripts/s17_p6_step_status.py"], cwd=ROOT, check=False)
    print(f"cells_filled={total} (ac36={ac_n} g10={g10_n} spot={spot_n})")
    print("next: make pack && make test && make p6-subset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
