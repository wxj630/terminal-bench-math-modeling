# Terminal Bench Math Modeling

This repository is a Harbor benchmark for mathematical-modeling contest workflows. The generated task set covers CUMCM and MCM problems A, B, and C from 2023, 2024, and 2025.

## Structure

- `tasks/CUMCM/`: generated China Undergraduate Mathematical Contest in Modeling tasks.
- `tasks/MCM/`: generated Mathematical Contest in Modeling tasks.
- `scripts/build_mathmodel_tasks.py`: task generator backed by the local `Math-Modeling-BAO` corpus.
- `ci_checks/`: copied Harbor/static-check utilities.
- `rubrics/`: Harbor rubric files adapted for modeling tasks.
- `jobs/`: local Harbor run output, ignored by git.

Each task contains:

- `instruction.md`
- `task.toml`
- `environment/Dockerfile`
- `tests/`
- `solution/solve.sh`

## Generated Tasks

The task instruction should be based on the original contest problem statement. The required output artifact is:

```text
/root/results/<task-slug>_result.json
```

Agent-visible data belongs under `/root/data/repo` inside the container. Hidden verifier references belong in `tests/`.

## Oracle Policy

Oracle solutions should use the outstanding-paper reproduction code and results from the local source corpus rather than inventing a new solution. The oracle `solve.sh` should copy the reproduction code to a temporary location, expose only task-visible data to the runtime, run the reproduction, and write the result JSON expected by the verifier.

## Verification

Use Harbor to validate the oracle:

```bash
harbor run -p tasks/CUMCM -a oracle
harbor run -p tasks/MCM -a oracle
```

For one task:

```bash
harbor run -p tasks/<CUMCM-or-MCM>/<task-slug> -a oracle
```

Do not commit `jobs/` output unless explicitly requested.
