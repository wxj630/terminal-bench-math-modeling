# Contributing to Terminal-Bench Math Modeling

Terminal-Bench Math Modeling (TB-MathModeling) contains Harbor tasks built from mathematical-modeling contest workflows. The current corpus focuses on CUMCM and MCM problems A, B, and C from 2023, 2024, and 2025.

## Task Scope

A good TB-MathModeling task should:

- Come from a real modeling contest problem or comparable applied-mathematics workflow.
- Provide enough contest statement context and data for an agent to work without internet access.
- Require non-trivial modeling, data processing, simulation, optimization, or statistical analysis.
- Produce concrete artifacts that can be verified programmatically.
- Include an oracle solution derived from reproducible reference code or a clearly documented solution path.

Tasks live under `tasks/mathematical-sciences/applied-mathematics/<task-slug>/`.

## Task Layout

Each task should include:

- `instruction.md`: task-facing instructions based on the original contest problem statement.
- `task.toml`: Harbor metadata, timeouts, tags, paths, and internet policy.
- `environment/Dockerfile`: task runtime dependencies.
- `tests/`: verifier code and hidden reference artifacts.
- `solution/solve.sh`: oracle solution entry point.

The required agent artifact for generated tasks is:

```text
/root/results/<task-slug>_result.json
```

## Local Checks

Run an oracle validation for a single task:

```bash
harbor run -p tasks/mathematical-sciences/applied-mathematics/<task-slug> -a oracle
```

Run the whole applied-mathematics set:

```bash
harbor run -p tasks/mathematical-sciences/applied-mathematics -a oracle
```

Run static checks where useful:

```bash
for check in ci_checks/check-*.sh; do bash "$check" tasks/mathematical-sciences/applied-mathematics/<task-slug>; done
for check in ci_checks/check-*.py; do python3 "$check" tasks/mathematical-sciences/applied-mathematics/<task-slug>; done
```

## Regenerating Generated Tasks

This repository includes a generator that rebuilds the 18 contest tasks from the local `Math-Modeling-BAO` corpus:

```bash
python scripts/build_mathmodel_tasks.py
```

After regenerating, rerun oracle validation before committing task changes.
