# Lean feasibility certificates

A kernel-checked parallel layer for the benchmark's programmatic feasibility gate
(`scripts/feasibility_checks.py`). It rewrites the gate's `hard_errors` logic as
Lean 4 theorems, so "this artifact is (in)feasible" becomes a machine-checkable
fact instead of a float comparison that happens to pass.

All 18 tasks are covered against **real saved artifacts** (17 from the anonymous
`stealth/union-alpha` run, 2 cells from the flash-opencode run for the tasks
union-alpha did not produce usable output for — see *Artifact sources*). The
generator also runs against the committed O-award references at
`tasks/<contest>/<slug>/tests/expected_result.json`, the same input the Python
gate's oracle suite uses.

## What it checks

**624 obligations, all discharged by `decide` on exact integers.** Every
`hard_errors` branch in the Python gate is one of six decidable forms, and the
library provides one predicate per form:

| Form | Example obligation | Lean predicate |
|---|---|---|
| domain / range | probability ∈ [0,1]; thickness ∈ (0,500] µm | `InUnit`, `Bounded`, `Positive` |
| integer / binary | decision bits ∈ {0,1}; counts are integers | `Binary` |
| ordering | q95 ≥ mean; peak users ≥ spread average; interval low ≤ high | `≤` |
| exact identity | area = count×width×height; union ≤ Σ parts | arithmetic |
| finite-domain | decision-bit count ∈ {16,17}; cases == 1..6 | disjunction |
| partition / sum | four land-use counts sum to the declared grid | `SumEq` |

No Mathlib is needed: Lean core's `decide` and `omega` suffice. Clean build from
scratch is under a second.

## Verdicts on the saved artifacts

The layer reproduces the Python gate's conclusion (no hard violation) on all 17
union-alpha artifacts, and additionally upgrades two soft warnings into
*proofs*:

- **`mcm-2025-b-juneau-tourism`** — Python warns "acceptance_index is reported
  above 1.0, suggesting a percentage scale". Lean proves the acceptance index
  `85.098` is *refuted* for the unit convention and fits the percent convention,
  while `sustainability_score = 118.362` fits **neither** — for every tolerance
  within the declared 5% budget. Widening the tolerance is not an escape.
- **`cumcm-2024-c-crop-planting`** — Python warns that the profit is "only
  reachable under the per-plot cap reading". Lean proves the profit lies strictly
  inside the per-plot/aggregate gap, so the verdict rests on a *declared* reading
  rather than on arithmetic.
- **`mcm-2025-c-olympic-medals`** — the recommendation *count* is deliberately not
  an obligation. The contest statement says "choose three countries", but the
  O-award reference reports four and the scoring config scores
  `recommendations[0..3]`. So three-vs-four is a stated interpretation difference
  (the Python gate records it as a warning), and the hard invariants asserted here
  are the real structural ones: gains nonnegative, NOC/Sport pairs nonempty and
  distinct.

## Layout

| File | Role |
|---|---|
| `FeasibilityDemo/Invariants.lean` | reusable predicates (`InUnit`, `Binary`, `Bounded`, `InIndex`, …) and kernel-checked lemmas |
| `FeasibilityDemo/Cases.lean` | **generated**: 623 obligations across all 18 tasks, each annotated with its JSON path |
| `FeasibilityDemo/CropPlanting.lean`, `Juneau.lean` | hand-written worked instances (record type + `Feasible` predicate + certificates) |
| `FeasibilityDemo/Sensitivity.lean` | proves the instances are not vacuous: the same predicate accepts a corrected artifact and rejects the reported one |
| `FeasibilityDemo/TrustAudit.lean` | `#print axioms` on every certificate |
| `generate_check.py` | artifact → Lean bridge; the per-task surface is a *declaration* |
| `negative_test.py` | discrimination suite: 10 mutations, each must break the build |
| `check_references.py` | runs the generator against the committed O-award references |
| `verify.sh` | one-shot: generate → check → audit → discriminate → references |

## Usage

```sh
export PATH="$HOME/.elan/bin:$PATH"     # Lean 4 via elan
./verify.sh                             # full end-to-end verification
```

Individual pieces:

```sh
python3 generate_check.py <benchmark-root>   # (re)generate Cases.lean and build
python3 negative_test.py                     # discrimination suite (saved artifacts)
python3 check_references.py                  # generator vs committed references
lake build                                   # kernel check only
```

`lake build` with unchanged sources is a warm no-op; `generate_check.py` rewrites
`Cases.lean` from the artifacts, so a changed artifact is re-audited on the next
run.

## Trust

`#print axioms` reports only `[propext, Quot.sound]` (Lean's standard classical
logic) or no axioms at all. There is no `sorryAx` and no `native_decide` — the
latter would trust the compiler via `Lean.ofReduceBool` rather than the kernel, so
the generated file is grep-checked for it (`verify.sh` step 3 of 5 covers the audit;
`grep -nE '\bsorry\b|native_decide' FeasibilityDemo/*.lean` should only ever hit a
comment).

## Artifact sources

`generate_check.py` locates each task's result JSON by slug:

```
jobs/ua-union-alpha-cumcm/<slug>__*/artifacts/root/results/<slug>_result.json
jobs/ua-union-alpha-mcm/<slug>__*/artifacts/root/results/<slug>_result.json
```

Two deviations, both because union-alpha produced no usable artifact:

- `cumcm-2023-a-heliostat-field` → `jobs/opencode-deepseek-flash-helio-retry3/`
- `cumcm-2025-a-smoke-screen` → `jobs/opencode-deepseek-flash-cumcm-retry/`
  (union-alpha's own smoke-screen JSON is all-`null`)

When a field is `null`, absent, or non-finite (`NaN`/`Inf` — the heliostat
reference uses `NaN` to mark unknown mirror dimensions) the obligation is
**skipped and reported**, never silently satisfied. This mirrors the Python gate's
"missing evidence is a warning, not a contradiction" contract. Skips on the saved
artifacts today: multibeam's `sa_avg_overlap_pct`; maasai's partition check (its
`grid_count` is `null`, so the four land-use counts cannot be tied to a declared
total); and the olympic recommendation count (an interpretation difference, not a
bound).

## Adding a task

Add a declaration to `TASKS` in `generate_check.py`: a slug, an artifact tree, and
a function that walks the JSON and emits `e.holds(...)` / `e.refutes(...)` calls.
The proofs are generated; the task-specific cost is writing the walk, not a proof.
