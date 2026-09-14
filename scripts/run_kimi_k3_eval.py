#!/usr/bin/env python3
"""Run Kimi K3 over all current math-modeling tasks with cooldown retries."""

from __future__ import annotations

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = Path("/Volumes/PSSD/code/My-Agent/.env")


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


def find_free_port(start: int) -> int:
    for port in range(start, start + 200):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise SystemExit(f"No free port found near {start}")


def wait_for_port(port: int, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                sock.connect(("127.0.0.1", port))
                return
            except OSError:
                time.sleep(0.2)
    raise SystemExit(f"Proxy did not open port {port}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--jobs-dir", type=Path, default=REPO_ROOT / "jobs")
    parser.add_argument("--job-prefix", default="terminus2-kimi-k3-current")
    parser.add_argument("--model", default=None)
    parser.add_argument("--n-concurrent", type=int, default=1)
    parser.add_argument("--port", type=int, default=30318)
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

    upstream_base = env_values.get("KIMI_API_BASE") or env_values.get("CLIPROXY_API_BASE")
    upstream_key = env_values.get("KIMI_API_KEY") or env_values.get("CLIPROXY_API_KEY")
    model = args.model or env_values.get("KIMI_MODEL", "kimi-k3")
    if not upstream_base or not upstream_key:
        raise SystemExit("KIMI_API_BASE/KIMI_API_KEY or CLIPROXY_API_BASE/CLIPROXY_API_KEY must be set")

    port = find_free_port(args.port)
    proxy_base = f"http://127.0.0.1:{port}/v1"
    args.jobs_dir.mkdir(parents=True, exist_ok=True)
    proxy_log_path = args.jobs_dir / f"{args.job_prefix}-proxy.log"

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
            wait_for_port(port)
            run_env = os.environ.copy()
            run_env.update(env_values)
            run_env["OPENAI_API_KEY"] = upstream_key

            suites: list[tuple[str, Path]] = []
            if args.only in {"cumcm", "all"}:
                suites.append(("cumcm", REPO_ROOT / "tasks" / "CUMCM"))
            if args.only in {"mcm", "all"}:
                suites.append(("mcm", REPO_ROOT / "tasks" / "MCM"))

            failures = 0
            for suite_name, task_path in suites:
                job_name = f"{args.job_prefix}-{suite_name}-retryproxy"
                cmd = harbor_command(
                    job_name,
                    task_path,
                    model,
                    proxy_base,
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
        finally:
            if proxy.poll() is None:
                os.killpg(proxy.pid, signal.SIGTERM)
                try:
                    proxy.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proxy.pid, signal.SIGKILL)


if __name__ == "__main__":
    raise SystemExit(main())
