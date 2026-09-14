#!/usr/bin/env python3
"""Run GLM-5.3 over all current math-modeling tasks."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = Path("/Volumes/PSSD/code/My-Agent/.env")
DEFAULT_API_BASE = "https://open.bigmodel.cn/api/coding/paas/v4"


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        raise SystemExit(f"Missing env file: {path}")

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--jobs-dir", type=Path, default=REPO_ROOT / "jobs")
    parser.add_argument("--job-prefix", default="terminus2-glm-5.3-current")
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-base", default=None)
    parser.add_argument("--n-concurrent", type=int, default=1)
    parser.add_argument("--only", choices=["cumcm", "mcm", "all"], default="all")
    parser.add_argument("--skip-task", action="append", default=[])
    return parser.parse_args()


def harbor_command(
    job_name: str,
    task_path: Path,
    model: str,
    api_base: str,
    jobs_dir: Path,
    n_concurrent: int,
    skip_tasks: list[str],
) -> list[str]:
    command = [
        "harbor",
        "run",
        "--job-name",
        job_name,
        "--jobs-dir",
        str(jobs_dir),
        "--path",
        str(task_path),
        "--agent",
        "terminus-2",
        "--model",
        f"openai/{model}",
        "--agent-kwarg",
        f"api_base={api_base}",
        "--agent-kwarg",
        "record_terminal_session=false",
        "--n-concurrent",
        str(n_concurrent),
        "--yes",
    ]
    for task_name in skip_tasks:
        command.extend(["--exclude-task-name", task_name])
    return command


def main() -> int:
    args = parse_args()
    env_values = load_env_file(args.env_file)

    api_key = env_values.get("GLM_API_KEY") or env_values.get("OPENAI_API_KEY")
    api_base = args.api_base or env_values.get("OPENAI_BASE_URL") or DEFAULT_API_BASE
    model = args.model or env_values.get("EVAL_MODEL") or "glm-5.3"
    if not api_key:
        raise SystemExit("GLM_API_KEY or OPENAI_API_KEY must be set")

    run_env = os.environ.copy()
    run_env.update(env_values)
    run_env["OPENAI_API_KEY"] = api_key
    run_env["OPENAI_BASE_URL"] = api_base

    args.jobs_dir.mkdir(parents=True, exist_ok=True)

    suites: list[tuple[str, Path]] = []
    if args.only in {"cumcm", "all"}:
        suites.append(("cumcm", REPO_ROOT / "tasks" / "CUMCM"))
    if args.only in {"mcm", "all"}:
        suites.append(("mcm", REPO_ROOT / "tasks" / "MCM"))

    failures = 0
    for suite_name, task_path in suites:
        job_name = f"{args.job_prefix}-{suite_name}"
        cmd = harbor_command(
            job_name,
            task_path,
            model,
            api_base,
            args.jobs_dir,
            args.n_concurrent,
            args.skip_task,
        )
        print(f"Running {job_name}: {' '.join(cmd)}", flush=True)
        completed = subprocess.run(cmd, cwd=REPO_ROOT, env=run_env)
        if completed.returncode != 0:
            failures += 1
            print(f"{job_name} exited with {completed.returncode}", flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
