ZIP ?= _打包吴军10本电子书.zip
PY ?= python3

.PHONY: restore-check freeze probe test status verify-pack verify-anchors pack split check-units p0-smoke

restore-check: verify-pack freeze probe test status

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
