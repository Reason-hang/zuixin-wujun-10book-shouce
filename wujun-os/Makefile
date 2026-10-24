ZIP ?= _打包吴军10本电子书.zip
PY ?= python3

.PHONY: restore-check freeze probe test status verify-pack verify-anchors pack split check-units p0-smoke s03 s04 s05 s06 s07 s08 p0 gates handover unitcards batch

restore-check: verify-pack freeze probe test status

# GATE 骨架（T-00-04）：聚合全部确定性闸门，任一失败非零退出；lint（S17）随 P5 实现
gates: verify-pack probe p0

freeze:
	$(PY) scripts/s00_freeze.py --zip "$(ZIP)" --out src_frozen --log logs/g0_inputs.md

probe:
	$(PY) scripts/s01_probe.py --src src_frozen --out logs/p0_probe.md

test:
	$(PY) scripts/selftest.py

status:
	$(PY) scripts/status.py

verify-pack:
	$(PY) scripts/verify_pack.py

verify-anchors:
	$(PY) scripts/anchor_tool.py verify --ledger "ledger/溯源与处置台账.md" --books-dir src_frozen

pack:
	$(PY) scripts/pack.py

split:
	$(PY) scripts/s01_split.py --src src_frozen --rules data/split_rules --out data/units

check-units:
	$(PY) scripts/s02_consistency.py --src src_frozen --units data/units --report logs/g2g3.md

p0-smoke: split check-units

s03:
	$(PY) scripts/s03_numbering.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g4.md

s04:
	$(PY) scripts/s04_catalog.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g5.md

s05:
	$(PY) scripts/s05_duplicates.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g6.md

s06:
	$(PY) scripts/s06_nonsource.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g7.md

s07:
	$(PY) scripts/s07_reverse.py --src src_frozen --units data/units --out logs/g8.md

s08:
	$(PY) scripts/s08_d5.py --src src_frozen --baseline spec/baseline_facts.json --units data/units --d5 "out/D5_内容盘点与单元清单.md" --denominator logs/p0_denominator.md

# P0 全链: 切分 → 行覆盖/守恒 → G4–G8 对账 → D5 分母冻结；任一关失败即停（make 默认串行、遇错退出）
p0: split check-units s03 s04 s05 s06 s07 s08

handover:
	$(PY) scripts/make_handover.py

unitcards:
	$(PY) scripts/s09_unitcards.py --units data/units --out data/unitcards

batch:
	$(PY) scripts/s10_batch.py --units data/units --cards data/unitcards --out data/batches --log logs/batch_plan.md
