# Programmatic feasibility gate

The feasibility gate answers one question for every model artifact: **is this a
genuinely achievable answer, or does it merely satisfy the scored fields while
violating a stated physical, geometric, or logical constraint?** It is fully
programmatic — no human or LLM judge sits in the scoring loop.

## Where it lives

| File | Role |
|---|---|
| `scripts/feasibility_checks.py` | The gate: one `*_check(data)` per task, a `CHECKS` registry, and `validate_artifact(data, task_slug)` |
| `scripts/test_feasibility_checks.py` | Contract tests that keep the gate honest (run in CI) |
| `.github/workflows/feasibility-gate.yml` | CI job that runs the contract tests on any task/check change |

## How a verdict is produced

`validate_artifact` looks the task up in `CHECKS` and calls its checker. Every
checker returns the same shape:

```python
{"status": str, "hard_errors": list[str], "warnings": list[str], "evidence": str}
```

* `hard_errors` — a genuine contradiction (negative rate, impossible
  probability, union longer than its parts, head speed × amplification above the
  2 m/s cap, a value above a proven ceiling). The pipeline penalises the whole
  task: O-Eval raw `0`, Robust BO-Eval `-100%`.
* `warnings` — missing evidence or a stated interpretation difference. The task
  is scored normally, and the warning is recorded in the audit.
* Empty `hard_errors` — the artifact is at least not infeasible.

Missing evidence is deliberately **not** a hard error: an artifact that omits a
block is incomplete, not impossible. This separation is what keeps the gate from
turning "the model didn't report X" into a false infeasibility verdict.

## Coverage

All 18 tasks are covered (`python3 scripts/feasibility_checks.py --coverage`).
The checks fall into two styles:

* **Structural / domain bounds** — rates in `[0,1]`, correlations in `[-1,1]`,
  probabilities in `[0,1]`, counts nonnegative, distributions summing to 100,
  peak ≥ spread average. These catch field-level contradictions.
* **Constraint replay** — heliostat rated power ≥ 60 MW and installation height
  in `[2,6] m`; the dragon-dance `head_speed × ratio ≤ 2 m/s` cap; the
  crop-planting demand-capped revenue ceiling; smoke-screen union ≤ sum of parts.
  These catch answers that are formally compliant but physically impossible.

## The three contracts

`scripts/test_feasibility_checks.py` enforces three invariants. Each one exists
because the corresponding failure actually happened in this benchmark:

1. **Coverage** — every task has a registered check. *Failure it prevents:*
   CUMCM 2024 C shipped with no check, so a 40M-class answer entered the board
   ungated.
2. **Oracle self-consistency** — the O-award reference artifact for every task
   must PASS its own check. *Failure it prevents:* a mis-set threshold that
   rejects the correct answer. A gate that fails the human outstanding solution
   is wrong by construction, so the fix is always to correct the bound or the
   schema path, never to gate the reference.
3. **Discrimination** — synthetic violations must be rejected, for the right
   reason. *Failure it prevents:* a check that satisfies coverage while always
   returning "pass". The suite also asserts no check hard-fails an empty
   artifact, which is what caught `olympic_check` treating a missing block as a
   contradiction.

## Adding a check for a new task

1. Write `def <name>_check(data: dict[str, Any]) -> dict[str, Any]` returning the
   standard shape.
2. Register it in `CHECKS` under the task slug.
3. Add its oracle to the self-consistency run automatically (it reads
   `tasks/*/<slug>/solution/oracle/**/result.json`).
4. If the task has a hard bound, add one synthetic violation to
   `SYNTHETIC_VIOLATIONS` so the discrimination test proves it fires.
5. Run `.venv/bin/python scripts/test_feasibility_checks.py` — a missing
   registration or an oracle failure turns it red.

## Commands

```bash
python3 scripts/feasibility_checks.py --coverage                 # 18/18?
python3 scripts/test_feasibility_checks.py                       # all contracts
python3 scripts/feasibility_checks.py --task <slug> --artifact <result.json>
```
