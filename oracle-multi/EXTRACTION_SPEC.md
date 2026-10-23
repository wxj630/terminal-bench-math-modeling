# Extraction spec: O-award paper answers → multi-oracle panels

## Goal
For each of the 18 benchmark tasks, extract the **numeric answers** reported by
**every** outstanding (O-award) paper for that problem, in the exact field
layout the benchmark's `tests/score_config.json` uses. Each paper becomes one
additional "oracle panel"; the final O-Eval is the mean over all papers.

## Where the papers are
`/Volumes/PSSD/code/Mathematical_Modeling/Math-Modeling-BAO-Reports/outstanding/<cumcm|mcm>/<year>-<X>/<paper_id>/ocr/<paper_id>.md`

## Output: one JSON per paper
Write to
`oracle-multi/<task-slug>/<paper_id>.json`

with this shape (values omitted when a paper does not report the field):

```json
{
  "paper_id": "A178",
  "task_slug": "cumcm-2024-a-dragon-dance",
  "source": "cumcm/2024-A/A178/ocr/A178.md",
  "fields": {
    "experiment_result.q5.max_head_speed_mps": 1.2462,
    "experiment_result.q5.max_speed_ratio_when_head_1mps": null
  },
  "notes": "free-text: where the number was found, unit conversions applied, ambiguities"
}
```

Rules:
- `fields` keys must be **exactly** the `path` strings from that task's
  `tests/score_config.json` (scored metrics only).
- Value must be a **number in the benchmark's unit**, or `null` if the paper
  provides no auditable route to that metric. **Never invent or interpolate a value.**
- A deterministic derivation is allowed only when the benchmark metric explicitly
  normalizes or aggregates values that the paper reports directly, the formula has
  no modeling choice, and the result is needed to put papers on a common scale.
  Examples are a relative improvement computed from the paper's fixed/adaptive
  endpoints, or a country total computed by summing every per-sport medal effect
  listed for that country. Every such field must include a machine-readable
  `derivations` entry with the reported inputs, formula kind, and computed value;
  `notes` must mark it `DERIVED`. If there is any choice about which values to use,
  set the field to `null` instead.
- If the paper reports a different quantity that is clearly the same thing but
  on another scale, convert it and say so in `notes` (e.g. "reported 124.62 cm/s
  → 1.2462 m/s").
- If you cannot find a field, set `null` and say why in `notes`
  ("only reports the method, not the number").
- Quote the surrounding sentence in `notes` (short) so a human can audit.

## Unit discipline (important — OCR mangles units)
The OCR text frequently mislabels units (e.g. reports `1.33 cm/s` where physics
implies m/s). Apply these checks and record what you did:
1. Prefer the unit written in the paper; convert to the benchmark unit.
2. If the written unit is **physically implausible** for the problem
   (e.g. a dragon head at `1.33 cm/s` when the problem fixes it at `1 m/s`),
   record the number as written in `notes`, and set the field to `null` rather
   than silently "fixing" it — **unless** the conversion is unambiguous
   (cm→m is unambiguous once you decide the label was wrong; in that case
   convert and note it).
3. Never adjust a value to match the benchmark's existing anchor.

## Per-task metric lists
Use the `tests/score_config.json` of the matching task for the exact paths,
directions and current anchor value. The current anchor's paper id (the one that
already has a full reproduction) is in the task's
`solution/oracle/**/solution.py` path; you may use its value only as a
sanity reference in `notes`, never to overwrite another paper's answer.

## One core scalar per task

Every task must expose exactly **one** scored field: the final-question core.
The field must be something the original last question asks for (or, when that
question is a memo/qualitative recommendation, the last numeric or binary decision
it rests on), and it must be reported by as many human papers as possible.

A paper either supplies a non-null value for that core or carries a machine-readable
`exclusion_reason`. Papers may never be silently dropped. Valid reasons include:

- `number_only_in_figure`: the paper reports the quantity only as a plot and gives
  no fixed-vs-adaptive pair or percentage;
- `different_time_points`: the paper reports the quantity at times the benchmark
  does not score;
- `figure_only`: only a closed-form curve or heatmap is given;
- `no_numeric_estimate`: only relative uncertainties are reported;
- `different_unit_of_analysis`: the paper reports per-sample values for many
  different objects, not one estimate for the benchmark object.

Do not average across incompatible objects (for example, 11 different staircases)
and do not digitize a curve silently. If neither a reported value nor a
deterministic, auditable conversion exists, exclude the paper and record why.

## Reporting back
Return a compact table: paper_id, whether the task core is present, and the key
number. Flag any paper that is unusable with one of the structured reasons above.
