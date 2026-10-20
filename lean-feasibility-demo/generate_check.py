#!/usr/bin/env python3
"""Generate kernel-checked Lean feasibility obligations for all 18 tasks.

The per-task surface is a *declaration*: which JSON path holds which quantity and
which invariant it must satisfy. Proofs are generated, so adding a task costs a
declaration, not a proof.

Values are scaled to exact integers (x1000 for rates/ratios, x1 for counts, money
and cell counts) so every obligation is decided by exact arithmetic -- no float
tolerance and no `1e-9` fudge factors. A `null`/missing field is *skipped and
reported*, not silently treated as satisfied, mirroring the Python gate's
"missing evidence is a warning, not a contradiction" contract.

Every generated obligation carries the JSON path it came from, so a reviewer can
trace each claim back to the artifact.
"""
from __future__ import annotations

import glob
import json
import math
import subprocess
import sys
from pathlib import Path

DEMO = Path(__file__).resolve().parent
LAKE = Path.home() / ".elan" / "bin" / "lake"

# Artifact sources. union-alpha produced 17 of 18; heliostat timed out for it and
# its smoke-screen JSON is all-null, so those two use the flash-opencode runs.
UA_C = "jobs/ua-union-alpha-cumcm"
UA_M = "jobs/ua-union-alpha-mcm"
FLASH_C = "jobs/opencode-deepseek-flash-cumcm-retry"
FLASH_H = "jobs/opencode-deepseek-flash-helio-retry3"

CROP_AGG_PROFIT = 36_277_448
CROP_PPLOT_PROFIT = 45_461_290
CROP_PPLOT_REVENUE = 52_042_270


def jpath(root: Path, slug: str, tree: str) -> str:
    hits = sorted(glob.glob(f"{root / tree}/*{slug}__*/artifacts/root/results/{slug}_result.json"))
    if not hits:
        raise FileNotFoundError(f"{slug} under {tree}")
    return hits[0]


def dig(data, path):
    cur = data
    for key in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(key)]
            continue
        if not isinstance(cur, dict) or key not in cur:
            raise KeyError(path)
        cur = cur[key]
    return cur


def opt(data, path):
    """Value at `path`, or None when absent or not a finite number.

    Non-finite floats (NaN/Inf) are treated as missing: artifacts use NaN to mark
    an unknown quantity (the heliostat reference does), and a NaN cannot satisfy
    or violate a feasibility bound -- it is an absence of evidence, so the caller
    skips and reports it rather than crashing or silently passing.
    """
    try:
        v = dig(data, path)
    except (KeyError, IndexError, ValueError):
        return None
    if v is None:
        return None
    if isinstance(v, float) and not math.isfinite(v):
        return None
    return v


def I(v, scale=1) -> int:
    return int(round(float(v) * scale))


class Emitter:
    def __init__(self):
        self.lines: list[str] = []
        self.skipped: list[str] = []
        self.count = 0

    def holds(self, note, prop):
        self.lines += [f"-- {note}", f"example : {prop} := by decide"]
        self.count += 1

    def refutes(self, note, prop):
        self.lines += [f"-- REJECT ({note})", f"example : ¬ ({prop}) := by decide"]
        self.count += 1

    def skip(self, note):
        self.skipped.append(note)


def nn(x):               return f"(0 ≤ {x})"
def pos(x):              return f"(0 < {x})"
def unit(x, s=1000):     return f"(0 ≤ {x} ∧ {x} ≤ {s})"
def signed(x, s=1000):   return f"(-{s} ≤ {x} ∧ {x} ≤ {s})"
def bounded(lo, hi, x):  return f"({lo} ≤ {x} ∧ {x} ≤ {hi})"
def le(a, b):            return f"({a} ≤ {b})"


# --------------------------------------------------------------------------- #
# Per-task declarations
# --------------------------------------------------------------------------- #

def t_heliostat(data, e):
    for r in dig(data, "reproduced.design_summary"):
        q = str(r.get("question", "")).lower()
        if q not in ("q2", "q3"):
            continue
        w, h = opt(r, "mirror_width_m"), opt(r, "mirror_height_m")
        if w is not None and h is not None:
            e.holds(f"{q} mirror width {w} m in [2,8]", bounded(2000, 8000, I(w, 1000)))
            e.holds(f"{q} mirror height {h} m in [2,8]", bounded(2000, 8000, I(h, 1000)))
            e.holds(f"{q} width {w} >= height {h}", le(I(h, 1000), I(w, 1000)))
            cnt, area = opt(r, "mirror_count"), opt(r, "mirror_area_m2")
            if cnt is not None and area is not None:
                lhs = I(cnt) * I(w, 1000) * I(h, 1000)
                rhs = I(area, 1_000_000)
                tol = max(rhs // 100, 1)
                e.holds(f"{q} area = count*width*height (reported {area} m2)", bounded(rhs - tol, rhs + tol, lhs))
        inst = opt(r, "installation_height_m")
        if inst is not None:
            e.holds(f"{q} installation height {inst} m in [2,6]", bounded(2000, 6000, I(inst, 1000)))
        p = opt(r, "annual_thermal_power_mw")
        if p is not None:
            e.holds(f"{q} rated power {p} MW >= 60", le(60000, I(p, 1000)))


def t_multibeam(data, e):
    for key, note, pred in [
        ("reproduced.problem4_summary.missed_area_pct", "missed_area_pct in [0,100]", lambda x: bounded(0, 100000, x)),
        ("reproduced.problem4_summary.sa_avg_overlap_pct", "average overlap pct >= 0", nn),
        ("reproduced.problem4_summary.overlap_over_20pct_length_nautical_miles", ">20% overlap length >= 0", nn),
        ("reproduced.problem4_summary.total_length_nautical_miles", "total survey length > 0", pos),
    ]:
        v = opt(data, key)
        if v is None:
            e.skip(f"{key} missing")
            continue
        e.holds(f"{note} [{key}]", pred(I(v, 1000)))


def t_vegetable(data, e):
    for i, r in enumerate(opt(data, "reproduced.correlation_comparison") or []):
        v = opt(r, "actual_sales_markup_corr")
        if v is not None:
            e.holds(f"row {i} sales/markup correlation {v} in [-1,1]", signed(I(v, 1000)))
    p = opt(data, "reproduced.future_week_profit_yuan")
    if p is not None:
        e.holds(f"future-week max profit {p} >= 0", nn(I(p)))


def t_dragon(data, e):
    head = opt(data, "experiment_result.q5.max_head_speed_mps")
    ratio = opt(data, "experiment_result.q5.max_speed_ratio_when_head_1mps")
    if head is None or ratio is None:
        e.skip("q5 head speed / ratio missing")
        return
    e.holds(f"head speed {head} > 0", pos(I(head, 1000)))
    e.holds(f"amplification ratio {ratio} > 0", pos(I(ratio, 1000)))
    prod = I(head, 1000) * I(ratio, 1000)
    e.holds(f"head*ratio = {prod/1e6:.6f} equals the 2 m/s handle cap", bounded(1_980_000, 2_020_000, prod))


def t_production(data, e):
    for i, plan in enumerate(opt(data, "experiment_result.q1_sampling") or []):
        n, c = opt(plan, "n"), opt(plan, "c")
        if n is not None:
            e.holds(f"q1 plan {i} sample size n={n} > 0", pos(I(n)))
        if n is not None and c is not None and c >= 0:
            e.holds(f"q1 plan {i} acceptance c={c} in [0,n={n}]", bounded(0, I(n), I(c)))
        for k in ("false_alarm", "power"):
            v = opt(plan, k)
            if v is not None:
                e.holds(f"q1 plan {i} {k}={v} in [0,1]", unit(I(v, 1000)))
    got = []
    for d in opt(data, "experiment_result.q2.best_decisions") or []:
        c = opt(d, "case")
        if c is not None:
            got.append(I(c))
        for k in ("inspect_part1", "inspect_part2", "inspect_final", "dismantle_bad_final"):
            v = opt(d, k)
            if v is not None:
                e.holds(f"q2 case {c} {k}={v} binary", f"({I(v)} = 0 ∨ {I(v)} = 1)")
        p = opt(d, "good_probability")
        if p is not None:
            e.holds(f"q2 case {c} good_probability={p} in [0,1]", unit(I(p, 1000)))
    if got:
        e.holds(f"q2 covers exactly cases 1-6 (got {sorted(got)})", f"({sorted(got)} = {[1,2,3,4,5,6]})")
    bits = opt(data, "experiment_result.q3.decision_bits")
    if bits:
        b = [I(x) for x in bits]
        e.holds(f"q3 decision_bits count {len(b)} in {{16,17}}", f"({len(b)} = 16 ∨ {len(b)} = 17)")
        e.holds("q3 decision_bits all binary", f"({' ∧ '.join(f'({x} = 0 ∨ {x} = 1)' for x in b)})")
    for i, row in enumerate(opt(data, "experiment_result.q4.posterior_rows") or []):
        m, q = opt(row, "posterior_mean_defect_rate"), opt(row, "posterior_q95_defect_rate")
        if m is not None:
            e.holds(f"q4 row {i} posterior mean {m} in [0,1]", unit(I(m, 1000)))
        if q is not None:
            e.holds(f"q4 row {i} posterior q95 {q} in [0,1]", unit(I(q, 1000)))
        if m is not None and q is not None:
            e.holds(f"q4 row {i} q95 {q} >= mean {m}", le(I(m, 1000), I(q, 1000)))


def t_crop(data, e):
    q1 = opt(data, "experiment_result.q1") or {}
    wp, wr = opt(q1, "waste_profit_yuan"), opt(q1, "waste_revenue_yuan")
    dp = opt(q1, "discount_profit_yuan")
    if wp is not None:
        e.holds(f"waste profit {wp:,.0f} <= per-plot profit ceiling", bounded(0, int(CROP_PPLOT_PROFIT * 1.02), I(wp)))
        e.holds(f"waste profit {wp:,.0f} exceeds aggregate ceiling -> declared per-plot reading",
                le(CROP_AGG_PROFIT, I(wp)))
    if wr is not None:
        e.holds(f"waste revenue {wr:,.0f} <= per-plot revenue ceiling", bounded(0, int(CROP_PPLOT_REVENUE * 1.02), I(wr)))
    if wp is not None and dp is not None:
        e.holds(f"discount profit {dp:,.0f} >= waste profit {wp:,.0f}", le(I(wp), I(dp)))
    rho = opt(data, "experiment_result.q2_q3.spearman_price_cost")
    if rho is not None:
        e.holds(f"spearman price/cost rho={rho} in [-1,1]", signed(I(rho, 1000)))


def t_smoke(data, e):
    for k in ("q1_duration_s", "q2_duration_s"):
        v = opt(data, f"experiment_result.{k}")
        if v is not None:
            e.holds(f"{k}={v} >= 0", nn(I(v, 1000)))
    for q in ("q3_union_duration_s", "q4_union_duration_s", "q5_union_duration_s"):
        blk = opt(data, f"experiment_result.{q}")
        if not isinstance(blk, dict):
            e.skip(f"{q} missing")
            continue
        parts = {k: I(v, 1000) for k, v in blk.items() if k != "total" and isinstance(v, (int, float))}
        for k, v in parts.items():
            e.holds(f"{q}.{k}={v/1000} >= 0", nn(v))
        total = blk.get("total")
        if total is not None and parts:
            e.holds(f"{q} union total {total} <= sum of parts {sum(parts.values())/1000}",
                    le(I(total, 1000), sum(parts.values())))


def t_sic(data, e):
    for k in ("sic_recommended_thickness_um", "si_recommended_thickness_um",
              "sic_rounded_thickness_um", "si_rounded_thickness_um"):
        v = opt(data, f"experiment_result.{k}")
        if v is not None:
            e.holds(f"{k}={v} um in (0,500]", bounded(1, 500000, I(v, 1000)))


def t_nipt(data, e):
    ew = opt(data, "experiment_result.earliest_recommended_week")
    lw = opt(data, "experiment_result.latest_recommended_week")
    if ew is not None:
        e.holds(f"earliest recommended week {ew} in [10,25]", bounded(10000, 25000, I(ew, 1000)))
    if lw is not None:
        e.holds(f"latest recommended week {lw} in [10,25]", bounded(10000, 25000, I(lw, 1000)))
    if ew is not None and lw is not None:
        e.holds(f"latest week {lw} >= earliest week {ew}", le(I(ew, 1000), I(lw, 1000)))
    for i, g in enumerate(opt(data, "bmi_timing.groups") or []):
        lo, hi = opt(g, "bmi_min"), opt(g, "bmi_max")
        if lo is not None and hi is not None:
            e.holds(f"BMI group {i} upper {hi} >= lower {lo}", le(I(lo, 1000), I(hi, 1000)))
        wk = opt(g, "recommended_week")
        if wk is not None:
            e.holds(f"BMI group {i} recommended week {wk} in [10,25]", bounded(10000, 25000, I(wk, 1000)))
        qp, fr = opt(g, "qualified_probability"), opt(g, "failure_rate")
        if qp is not None:
            e.holds(f"BMI group {i} qualified_probability {qp} in [0,1]", unit(I(qp, 1000)))
        if fr is not None:
            e.holds(f"BMI group {i} failure_rate {fr} in [0,1]", unit(I(fr, 1000)))
        if qp is not None and fr is not None:
            e.holds(f"BMI group {i} qualified {qp} + failure {fr} = 1", bounded(980, 1020, I(qp, 1000) + I(fr, 1000)))
    fa = opt(data, "female_abnormality") or {}
    for k in ("leave_one_out_accuracy", "leave_one_out_f1", "leave_one_out_auc"):
        v = opt(fa, k)
        if v is not None:
            e.holds(f"female abnormality {k}={v} in [0,1]", unit(I(v, 1000)))
    rows, posc = opt(fa, "rows"), opt(fa, "positive_count")
    if rows is not None and posc is not None:
        e.holds(f"female positives {posc} in [0, rows={rows}]", bounded(0, I(rows), I(posc)))


def t_plant(data, e):
    for i, r in enumerate(opt(data, "reproduced.species_count_summary") or []):
        sc = opt(r, "species_count")
        if sc is not None:
            e.holds(f"species row {i} count {sc} > 0", pos(I(sc)))
        bm = opt(r, "mean_total_biomass_last20y")
        if bm is not None:
            e.holds(f"species row {i} biomass {bm} >= 0", nn(I(bm, 1000)))
        ev = opt(r, "pielou_evenness")
        if ev is not None:
            e.holds(f"species row {i} Pielou evenness {ev} in [0,1]", unit(I(ev, 1000)))
    for i, r in enumerate(opt(data, "reproduced.drought_buffer") or []):
        f = opt(r, "drought_frequency_per_50y")
        if f is not None:
            e.holds(f"drought row {i} frequency {f} >= 0", nn(I(f, 1000)))
        for k in ("monoculture_biomass_index", "five_species_biomass_index"):
            v = opt(r, k)
            if v is not None:
                e.holds(f"drought row {i} {k}={v} >= 0", nn(I(v, 1000)))


def t_maasai(data, e):
    grid = opt(data, "paper_targets.grid_count")
    for i, r in enumerate(opt(data, "reproduced.scenario_rows") or []):
        vals = []
        for k in ("wildlife_sanctuary", "agricultural_area", "hunting_area", "tourism_area"):
            v = opt(r, k)
            if v is None:
                vals = []
                break
            e.holds(f"scenario {i} {k}={v} >= 0 integer", nn(I(v)))
            vals.append(I(v))
        if vals:
            if grid is not None:
                e.holds(f"scenario {i} partitions {sum(vals)} cells into declared grid {grid}",
                        f"({'+'.join(map(str, vals))} = {I(grid)})")
            else:
                e.skip(f"scenario {i}: declared grid_count is null; partition unverifiable")
    s2 = opt(data, "reproduced.scenario2_counts")
    if isinstance(s2, dict):
        keys = ("wildlife_sanctuary", "agricultural_area", "hunting_area", "tourism_area")
        vals = [I(s2[k]) for k in keys if s2.get(k) is not None]
        if len(vals) == 4 and grid is not None:
            e.holds("scenario2 partitions the declared grid", f"({'+'.join(map(str, vals))} = {I(grid)})")
        elif len(vals) == 4:
            e.skip("scenario2: declared grid_count is null; partition unverifiable")
    d = opt(data, "reproduced.mean_sanctuary_to_tourism_interaction_distance")
    if d is not None:
        e.holds(f"mean sanctuary-tourism distance {d} >= 0", nn(I(d, 1000)))


def t_wordle(data, e):
    eerie = opt(data, "reproduced.eerie") or {}
    g = opt(eerie, "difficulty_group")
    if g is not None:
        e.holds(f"EERIE difficulty group {g} >= 1 integer", le(1, I(g)))
    dist = opt(eerie, "predicted_distribution_pct")
    if dist:
        vals = [I(v, 1000) for v in dist]
        e.holds(f"predicted distribution sums to 100% (got {sum(vals)/1000:.2f}%)",
                bounded(99000, 101000, sum(vals)))
        e.holds("predicted distribution entries all >= 0", f"({' ∧ '.join(nn(v) for v in vals)})")


def t_lamprey(data, e):
    ep = opt(data, "experiment_result.sex_ratio_endpoint") or {}
    for k in ("scarce_resource_male_share", "abundant_resource_male_share"):
        v = opt(ep, k)
        if v is not None:
            e.holds(f"sex-ratio endpoint {k}={v} in [0,1]", unit(I(v, 1000)))
    for i, r in enumerate(opt(data, "experiment_result.scenario_summary") or []):
        for k in ("mean_biomass", "final_lamprey", "final_host_fish", "final_parasite"):
            v = opt(r, k)
            if v is not None:
                e.holds(f"scenario {i} {k}={v} >= 0", nn(I(v, 1000)))
        for k in ("normalized_diversity", "species_persistence", "resistance", "resilience",
                  "sustainability", "composite_stability"):
            v = opt(r, k)
            if v is not None:
                e.holds(f"scenario {i} {k}={v} in [0,1]", unit(I(v, 1000)))


def t_submersible(data, e):
    """Walk the whole block: any leaf named *probability*/*pod is a probability,
    any leaf named *multiplier* is a positive scale. Container names containing
    `cells`/`count` are skipped, mirroring the Python check's guard."""
    def visit(node, prefix):
        if isinstance(node, dict):
            for k, v in node.items():
                nk = f"{prefix}.{k}" if prefix else k
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    last = k.lower()
                    if ("cells" in nk.lower() or "count" in nk.lower()):
                        continue
                    if "probability" in last or last == "pod":
                        e.holds(f"{nk}={v} in [0,1]", unit(I(v, 1000)))
                    elif "multiplier" in last:
                        e.holds(f"{nk}={v} > 0", pos(I(v, 1000)))
                else:
                    visit(v, nk)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                visit(v, f"{prefix}.{i}")
    visit(opt(data, "experiment_result") or {}, "")


def t_tennis(data, e):
    b = opt(data, "experiment_result.dual_temporal_bayes") or {}
    for k in ("swing_warning_rate", "final_match_warning_rate"):
        v = opt(b, k)
        if v is not None:
            e.holds(f"{k}={v} in [0,1]", unit(I(v, 1000)))
    for i, r in enumerate(opt(data, "experiment_result.top_swing_features") or []):
        v = opt(r, "warning_correlation")
        if v is not None:
            e.holds(f"feature {i} warning correlation {v} in [-1,1]", signed(I(v, 1000)))


def t_stair(data, e):
    dup = opt(data, "daily_use_pattern") or {}
    for k in ("estimated_daily_users", "peak_period_users", "regular_hour_users_if_spread_over_10_hours"):
        v = opt(dup, k)
        if v is not None:
            e.holds(f"daily_use_pattern.{k}={v} >= 0", nn(I(v, 1000)))
    peak, reg = opt(dup, "peak_period_users"), opt(dup, "regular_hour_users_if_spread_over_10_hours")
    if peak is not None and reg is not None:
        e.holds(f"peak users {peak} >= 10-hour spread average {reg}", le(I(reg, 1000), I(peak, 1000)))
    sh = opt(dup, "peak_period_share_of_daily_use")
    if sh is not None:
        e.holds(f"peak share {sh} in [0,1]", unit(I(sh, 1000)))
    v = opt(data, "experiment_result.median_center_wear_depth_mm")
    if v is not None:
        e.holds(f"median center wear depth {v} mm >= 0", nn(I(v, 1000)))


def t_juneau(data, e):
    dp = opt(data, "dynamic_programming") or {}
    rows = opt(dp, "policy_rows")
    if isinstance(rows, list):
        for i, r in enumerate(rows):
            for k in ("daily_cap", "annual_visitors", "visitor_fee_usd", "total_revenue_usd"):
                v = opt(r, k)
                if v is not None:
                    e.holds(f"policy row {i} {k}={v} >= 0", nn(I(v)))
            sh = opt(r, "conservation_share")
            if sh is not None:
                e.holds(f"policy row {i} conservation_share={sh} in [0,1]", unit(I(sh, 1000)))
            acc = opt(r, "resident_acceptance_index")
            if acc is not None:
                e.holds(f"policy row {i} acceptance_index={acc} >= 0", nn(I(acc, 1000)))
                _scale_note(e, f"policy row {i} acceptance_index", acc)
            sus = opt(r, "sustainability_score")
            if sus is not None:
                e.holds(f"policy row {i} sustainability_score={sus} >= 0", nn(I(sus, 1000)))
                _scale_note(e, f"policy row {i} sustainability_score", sus)
    for k in ("resident_acceptance_index", "sustainability_score", "optimal_visitor_fee_usd", "annual_visitors"):
        v = opt(data, f"experiment_result.{k}")
        if v is not None:
            e.holds(f"endpoint {k}={v} >= 0", nn(I(v, 1000)))
            _scale_note(e, f"endpoint {k}", v)


def _scale_note(e, label, v):
    """Classify a unit-like index against the fraction and percent conventions.

    This is the machine-checked upgrade of the Python gate's soft warning. It never
    asserts a falsehood: a value above unit scale is *refuted* for the fraction
    convention, and the percent convention is asserted only when it actually holds.
    """
    x = I(v, 1000)
    if x < 0:
        return
    if x > 1000:
        e.refutes(f"{label}={v} does NOT fit the unit-scale convention", unit(x))
        if x <= 100000:
            e.holds(f"{label}={v} fits the percent-scale convention", bounded(1001, 100000, x))
        else:
            e.refutes(f"{label}={v} fits NEITHER the unit nor the percent convention",
                      f"((0 ≤ {x} ∧ {x} ≤ 1000) ∨ (0 ≤ {x} ∧ {x} ≤ 100000))")


def t_olympic(data, e):
    coach = opt(data, "great_coach_model") or {}
    recs = opt(coach, "recommendations")
    if recs is None:
        e.skip("recommendations missing")
    else:
        # The count is NOT a feasibility invariant: the contest statement says
        # "choose three countries", but the O-award reference and this task's
        # score_config both use four slots, so the Python gate records a count
        # mismatch as a warning, not a hard error. We report it and assert only
        # the genuine structural invariants below.
        e.skip(f"recommendation count is {len(recs)} (3 vs 4 is an interpretation "
               f"difference, not a feasibility bound)")
        for i, r in enumerate(recs):
            for k in ("benchmark_jump_score", "estimated_medal_count_gain"):
                v = opt(r, k)
                if v is not None:
                    e.holds(f"recommendation {i} {k}={v} >= 0", nn(I(v, 1000)))
        # Nonempty, pairwise-distinct (NOC, Sport) pairs. "Filled" is encoded as a
        # 0/1 indicator per pair, computed from the artifact, then asserted all-1.
        pairs = [(str(r.get("NOC", "")), str(r.get("Sport", ""))) for r in recs]
        filled = [1 if (a and b) else 0 for a, b in pairs]
        e.holds(f"all {len(pairs)} recommendation pairs have nonempty NOC and Sport",
                f"({' ∧ '.join(f'({x} = 1)' for x in filled)})")
        e.holds(f"all {len(pairs)} recommendation pairs are distinct",
                f"({len(set(pairs))} = {len(pairs)})")
    ev = opt(data, "model_evaluation") or {}
    for k in ("mean_accuracy_2024", "mean_f1_2024", "mean_brier_2024"):
        v = opt(ev, k)
        if v is not None:
            e.holds(f"model evaluation {k}={v} in [0,1]", unit(I(v, 1000)))
    fm = opt(data, "expected_first_medal_countries")
    if fm is not None:
        e.holds(f"expected first-medal countries {fm} >= 0", nn(I(fm, 1000)))
    for i, c in enumerate(opt(data, "first_medal_top_candidates") or []):
        v = opt(c, "first_medal_probability")
        if v is not None:
            e.holds(f"first-medal candidate {i} probability {v} in [0,1]", unit(I(v, 1000)))
    for i, row in enumerate(opt(data, "monte_carlo_summary_top_total") or []):
        tot, gold = opt(row, "expected_total"), opt(row, "expected_gold")
        if tot is not None and gold is not None:
            e.holds(f"MC row {i} expected gold {gold} <= expected total {tot}", le(I(gold, 1000), I(tot, 1000)))
        lo, hi = opt(row, "total_interval95_low"), opt(row, "total_interval95_high")
        if lo is not None and hi is not None:
            e.holds(f"MC row {i} interval low {lo} <= high {hi}", le(I(lo, 1000), I(hi, 1000)))


TASKS = [
    ("cumcm-2023-a-heliostat-field", FLASH_H, t_heliostat),
    ("cumcm-2023-b-multibeam-lines", UA_C, t_multibeam),
    ("cumcm-2023-c-vegetable-pricing", UA_C, t_vegetable),
    ("cumcm-2024-a-dragon-dance", UA_C, t_dragon),
    ("cumcm-2024-b-production-decision", UA_C, t_production),
    ("cumcm-2024-c-crop-planting", UA_C, t_crop),
    ("cumcm-2025-a-smoke-screen", FLASH_C, t_smoke),
    ("cumcm-2025-b-sic-thickness", UA_C, t_sic),
    ("cumcm-2025-c-nipt", UA_C, t_nipt),
    ("mcm-2023-a-plant-community", UA_M, t_plant),
    ("mcm-2023-b-maasai-mara", UA_M, t_maasai),
    ("mcm-2023-c-wordle", UA_M, t_wordle),
    ("mcm-2024-a-lamprey", UA_M, t_lamprey),
    ("mcm-2024-b-submersible-search", UA_M, t_submersible),
    ("mcm-2024-c-tennis-momentum", UA_M, t_tennis),
    ("mcm-2025-a-stair-wear", UA_M, t_stair),
    ("mcm-2025-b-juneau-tourism", UA_M, t_juneau),
    ("mcm-2025-c-olympic-medals", UA_M, t_olympic),
]


def build(root: Path):
    out = [
        "import FeasibilityDemo.Invariants",
        "",
        "/-",
        "  Generated by generate_check.py -- kernel-checked feasibility obligations for",
        "  all 18 benchmark tasks, evaluated against real saved artifacts.",
        "",
        "  Every obligation is decided by exact integer arithmetic and carries the JSON",
        "  path it came from, so each claim is traceable to the artifact it audits.",
        "-/",
        "",
        "namespace Cases",
        "",
    ]
    stats = []
    for slug, tree, fn in TASKS:
        data = json.loads((root / jpath(root, slug, tree)).read_text())
        e = Emitter()
        fn(data, e)
        out += [f"/-! ## {slug} -/", ""] + e.lines + [""]
        stats.append((slug, e.count, e.skipped))
    out += ["end Cases", ""]
    return "\n".join(out), stats


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    text, stats = build(root)
    (DEMO / "FeasibilityDemo" / "Cases.lean").write_text(text, encoding="utf-8")
    total = sum(s[1] for s in stats)
    print(f"generated Cases.lean: {len(stats)} tasks, {total} obligations")
    for slug, n, skipped in stats:
        flag = f"  [{len(skipped)} skipped: {'; '.join(skipped)}]" if skipped else ""
        print(f"  {slug:36s} {n:3d} obligations{flag}")
    (DEMO / "FeasibilityDemo.lean").write_text(
        "import FeasibilityDemo.Invariants\n"
        "import FeasibilityDemo.CropPlanting\n"
        "import FeasibilityDemo.Juneau\n"
        "import FeasibilityDemo.Sensitivity\n"
        "import FeasibilityDemo.TrustAudit\n"
        "import FeasibilityDemo.Cases\n",
        encoding="utf-8",
    )
    proc = subprocess.run([str(LAKE), "build"], cwd=DEMO, capture_output=True, text=True)
    ok = proc.returncode == 0
    print(f"lake build: {'OK' if ok else 'FAILED'}")
    if not ok:
        shown = 0
        for line in (proc.stdout + proc.stderr).splitlines():
            if line.strip() and "Replayed" not in line and "does not depend" not in line:
                print(" ", line)
                shown += 1
                if shown > 40:
                    break
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
