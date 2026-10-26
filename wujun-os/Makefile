ZIP ?= _打包吴军10本电子书.zip
PY ?= python3

.PHONY: restore-check freeze probe test status verify-pack verify-anchors pack split check-units p0-smoke s03 s04 s05 s06 s07 s08 p0 gates handover unitcards batch

restore-check: verify-pack freeze probe test status

# GATE 骨架（T-00-04）：聚合全部确定性闸门，任一失败非零退出；lint（S17）随 P5 实现
gates: verify-pack probe p0

# P6 可复算子集（非全量 G0–G10）
p6-subset:
	$(PY) scripts/s15_check_all.py

render-check:
	$(PY) scripts/s18_render_check.py

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

export-anchors:
	$(PY) scripts/s12_export_anchor_ledger.py

d3-export:
	$(PY) scripts/s12_export_anchor_ledger.py
	$(PY) scripts/s12_export_unit_disposal.py
	$(PY) scripts/s12_export_k_claim_table.py
	$(PY) scripts/s12_export_x_exclusion.py

p6-spotcheck-v20:
	$(PY) scripts/s12_export_p6_spotcheck_v20.py

g-logs-index:
	$(PY) scripts/s15_g_logs_index.py

fact-source:
	$(PY) scripts/s12_export_p7_fact_source.py

p6-matrix:
	$(PY) scripts/s16_p6_coverage_matrix.py

ac36-sample:
	$(PY) scripts/s13_ac36_sample_recall.py

ac36-anchor-ping:
	$(PY) scripts/s13_ac36_anchor_ping.py

ac36-semantic-heuristic:
	$(PY) scripts/s13_ac36_semantic_heuristic.py

ac36-agent-draft:
	$(PY) scripts/s13_ac36_agent_draft_column.py

ac36-low-ngram-pack:
	$(PY) scripts/s13_ac36_low_ngram_pack.py && $(PY) scripts/s13_ac36_fill_agent_verdicts.py

g10-blind-agent-draft:
	$(PY) scripts/s13_g10_blind_agent_draft.py

p6-spotcheck-agent:
	$(PY) scripts/s13_p6_spotcheck_agent_draft.py

d4-snapshot:
	$(PY) scripts/s15_export_d4_snapshot.py

g9-subset:
	$(PY) scripts/s12_g9_subset_check.py

p6-adversarial-preflight:
	$(PY) scripts/s17_p6_adversarial_preflight.py

p6-user-prep:
	$(MAKE) ac36-agent-draft ac36-low-ngram-pack g10-blind-agent-draft p6-spotcheck-agent p6-adversarial-preflight

user-signoff-apply:
	$(PY) scripts/s13_user_signoff_apply.py

user-signoff-dry-run:
	$(PY) scripts/s13_user_signoff_apply.py --dry-run --accept-text "$$(cat logs/user_signoff_example.txt)"

p6-step-status:
	$(PY) scripts/s17_p6_step_status.py

v6-audit:
	$(PY) scripts/s17_v6_completion_audit.py

p7-preflight:
	$(PY) scripts/s18_p7_preflight.py

v6-engineering:
	$(MAKE) test p6-subset p6-adversarial-preflight p7-preflight p6-step-status

v6-roll-forward:
	$(PY) scripts/s17_v6_roll_forward_check.py

math-mapping-audit:
	$(PY) scripts/s17_math_mapping_audit.py

g10-blind-sample:
	$(PY) scripts/s13_g10_blind_unit_sample.py

p6-prep-artifacts:
	$(MAKE) p6-matrix ac36-sample g10-blind-sample p6-spotcheck-v20 g-logs-index fact-source

d07-comm-index:
	$(PY) scripts/s17_d07_comm_cluster_index.py

p6-scene-drill:
	$(PY) scripts/s17_p6_scene_drill_index.py

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

s11:
	$(PY) scripts/s11_readlevel.py
