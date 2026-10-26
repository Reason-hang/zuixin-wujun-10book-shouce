#!/usr/bin/env python3
"""S16: Cohen's kappa for P4 blind relabel (v2 §15.5.5 step 10)."""
from __future__ import annotations

import argparse
import csv
from collections import Counter


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> tuple[float, float]:
    if len(labels_a) != len(labels_b):
        raise ValueError("label lists must have equal length")
    n = len(labels_a)
    if n == 0:
        return float("nan"), float("nan")
    cats = set(labels_a) | set(labels_b)
    po = sum(a == b for a, b in zip(labels_a, labels_b)) / n
    c1, c2 = Counter(labels_a), Counter(labels_b)
    pe = sum((c1.get(c, 0) / n) * (c2.get(c, 0) / n) for c in cats)
    if pe >= 1.0:
        return 1.0, po
    return (po - pe) / (1 - pe), po


def load_csv_pairs(ground_truth: str, relabel: str) -> tuple[list[str], list[str]]:
    gt = {r["claim_id"]: r["original_primary"] for r in csv.DictReader(open(ground_truth))}
    rel = {r["claim_id"]: r["relabel_primary"] for r in csv.DictReader(open(relabel))}
    ids = sorted(set(gt) & set(rel))
    return [gt[i] for i in ids], [rel[i] for i in ids]


def main() -> None:
    p = argparse.ArgumentParser(description="Cohen's kappa for blind relabel pairs")
    p.add_argument("--ground-truth", required=True, help="CSV: claim_id,original_primary")
    p.add_argument("--relabel", required=True, help="CSV: claim_id,relabel_primary,...")
    p.add_argument("--min-kappa", type=float, default=0.6)
    args = p.parse_args()
    a, b = load_csv_pairs(args.ground_truth, args.relabel)
    k, po = cohen_kappa(a, b)
    status = "PASS" if k >= args.min_kappa else "FAIL"
    print(f"n={len(a)} Po={po:.4f} kappa={k:.4f} threshold={args.min_kappa} -> {status}")
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
