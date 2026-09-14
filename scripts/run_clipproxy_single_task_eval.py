#!/usr/bin/env python3
"""Run one cliproxy-backed Terminus-2 trial without touching existing suite jobs."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path

import run_clipproxy_2024_2025_eval as base


REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=base.DEFAULT_ENV_FILE)
    parser.add_argument("--jobs-dir", type=Path, default=REPO_ROOT / "jobs")
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--suite", choices=["cumcm", "mcm"], required=True)
    parser.add_argument("--task-slug", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--reasoning-effort", default=None)
    parser.add_argument("--n-concurrent", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def output_artifact_exists(job_dir: Path, task_slug: str) -> bool:
    return any(job_dir.glob(f"{task_slug}__*/artifacts/root/results/{task_slug}_result.json"))


def main() -> int:
    args = parse_args()
    env_values = base.load_env_file(args.env_file)
    upstream_base = env_values.get("CLIPROXY_API_BASE")
    upstream_key = env_values.get("CLIPROXY_API_KEY")
    if not upstream_base or not upstream_key:
        raise SystemExit("CLIPROXY_API_BASE/CLIPROXY_API_KEY must be set")

    cases = [case for case in base.load_cases() if case.contest == args.suite]
    if args.task_slug not in {case.slug for case in cases}:
        raise SystemExit(f"Unknown {args.suite} task slug: {args.task_slug}")

    job_dir = args.jobs_dir / args.job_name
    if output_artifact_exists(job_dir, args.task_slug):
        raise SystemExit(f"Refusing to rerun: artifact already exists in {job_dir}")

    existing_api_base = base.existing_api_base(job_dir)
    existing_port = base.port_from_api_base(existing_api_base) if existing_api_base else None
    port = existing_port or (args.port if base.is_port_free(args.port) else base.find_free_port(args.port + 1))
    proxy_base = f"http://127.0.0.1:{port}/v1"
    proxy_log_path = args.jobs_dir / f"{args.job_name}-proxy.log"
    skip_tasks = [case.slug for case in cases if case.slug != args.task_slug]
    if (job_dir / "config.json").exists():
        command = [
            "harbor",
            "job",
            "resume",
            "--job-path",
            str(job_dir),
            "--filter-error-type",
            "AgentTimeoutError",
        ]
    else:
        command = base.harbor_command(
            args.job_name,
            REPO_ROOT / "tasks" / args.suite.upper(),
            args.model,
            proxy_base,
            args.reasoning_effort,
            args.jobs_dir,
            args.n_concurrent,
            skip_tasks,
        )

    if args.dry_run:
        print(f"proxy_base={proxy_base}")
        print(" ".join(command))
        return 0

    args.jobs_dir.mkdir(parents=True, exist_ok=True)
    proxy_env = os.environ.copy()
    proxy_env.update(
        {
            "UPSTREAM_API_BASE": upstream_base,
            "UPSTREAM_API_KEY": upstream_key,
            "PROXY_PORT": str(port),
        }
    )

    print(f"Starting retry proxy on {proxy_base}; log: {proxy_log_path}", flush=True)
    with proxy_log_path.open("a") as proxy_log:
        proxy = subprocess.Popen(
            [sys.executable, str(REPO_ROOT / "scripts" / "openai_cooldown_retry_proxy.py")],
            cwd=REPO_ROOT,
            env=proxy_env,
            stdout=proxy_log,
            stderr=proxy_log,
            start_new_session=True,
        )
        try:
            base.wait_for_port(port)
            run_env = os.environ.copy()
            run_env.update(env_values)
            run_env["OPENAI_API_KEY"] = upstream_key
            run_env["OPENAI_BASE_URL"] = proxy_base

            print(f"Running {' '.join(command)}", flush=True)
            return subprocess.run(command, cwd=REPO_ROOT, env=run_env).returncode
        finally:
            if proxy.poll() is None:
                os.killpg(proxy.pid, signal.SIGTERM)
                try:
                    proxy.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proxy.pid, signal.SIGKILL)


if __name__ == "__main__":
    raise SystemExit(main())
