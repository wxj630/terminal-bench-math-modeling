# Reviewing TB-MathModeling Tasks

Review tasks from a benchmark integrity perspective first: correctness, verifiability, anti-cheat boundaries, and reproducibility matter more than style.

## Review Order

1. Read `instruction.md`.
2. Inspect `task.toml`.
3. Inspect `tests/`.
4. Inspect `solution/solve.sh` and any oracle support files.
5. Inspect `environment/Dockerfile`.
6. Run oracle validation.

## Review Questions

- Does the instruction reflect the original contest problem closely enough for a solver to know what to produce?
- Are all required input files available inside the agent-visible environment?
- Are hidden oracle references only available to the verifier?
- Does the verifier check the requested artifact by schema, identifiers, and meaningful numeric values rather than brittle strings?
- Does the oracle solution actually run the reproduction code and produce the expected result artifact?
- Is internet disabled unless the task truly requires it?
- Are dependencies installed in the Dockerfile and not pulled dynamically at solve time?

## Validation

For one task:

```bash
harbor run -p tasks/<CUMCM-or-MCM>/<task-slug> -a oracle
```

For the full generated set:

```bash
harbor run -p tasks/CUMCM -a oracle
harbor run -p tasks/MCM -a oracle
```

A generated task should pass oracle validation before it is considered ready.
