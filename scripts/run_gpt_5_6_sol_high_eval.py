#!/usr/bin/env python3
"""Run GPT-5.6 SOL high over 2024-2025 math-modeling tasks via cliproxy."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = Path("/Volumes/PSSD/code/My-Agent/.env")
DEFAULT_PORT = 30356
TARGET_YEARS = {2024, 2025}


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


def load_cases() -> tuple[Any, ...]:
    path = REPO_ROOT / "scripts" / "build_mathmodel_tasks.py"
    spec = importlib.util.spec_from_file_location("build_mathmodel_tasks", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.CASES


def skip_tasks_for_suite(suite_name: str) -> list[str]:
    return [
        case.slug
        for case in load_cases()
        if case.contest == suite_name and case.year not in TARGET_YEARS
    ]


def is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
        return True


def find_free_port(start: int) -> int:
    for port in range(start, start + 200):
        if is_port_free(port):
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
    parser.add_argument("--job-prefix", default="terminus2-gpt-5.6-sol-high-2024-2025")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--n-concurrent", type=int, default=1)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--only", choices=["cumcm", "mcm", "all"], default="all")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def job_name(prefix: str, suite_name: str) -> str:
    return f"{prefix}-{suite_name}-retryproxy"


def existing_api_base(job_dir: Path) -> str | None:
    config_path = job_dir / "config.json"
    if not config_path.exists():
        return None
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    agents = config.get("agents")
    if not isinstance(agents, list) or not agents:
        return None
    kwargs = agents[0].get("kwargs")
    if not isinstance(kwargs, dict):
        return None
    api_base = kwargs.get("api_base")
    return api_base if isinstance(api_base, str) and api_base else None


def port_from_api_base(api_base: str) -> int | None:
    match = re.search(r"127\.0\.0\.1:(\d+)", api_base)
    return int(match.group(1)) if match else None


def resolve_proxy_port(args: argparse.Namespace, suites: list[str]) -> int:
    existing_ports: set[int] = set()
    for suite_name in suites:
        api_base = existing_api_base(args.jobs_dir / job_name(args.job_prefix, suite_name))
        if api_base is None:
            continue
        port = port_from_api_base(api_base)
        if port is not None:
            existing_ports.add(port)

    if len(existing_ports) > 1:
        raise SystemExit(f"Existing jobs use conflicting proxy ports: {sorted(existing_ports)}")
    if existing_ports:
        return next(iter(existing_ports))
    if is_port_free(args.port):
        return args.port
    return find_free_port(args.port + 1)


def harbor_command(
    job: str,
    task_path: Path,
    model: str,
    api_base: str,
    reasoning_effort: str,
    jobs_dir: Path,
    n_concurrent: int,
    skip_tasks: list[str],
) -> list[str]:
    command = [
        "harbor",
        "run",
        "--job-name",
        job,
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
        f"reasoning_effort={reasoning_effort}",
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

    upstream_base = env_values.get("CLIPROXY_API_BASE") or env_values.get("KIMI_API_BASE")
    upstream_key = env_values.get("CLIPROXY_API_KEY") or env_values.get("KIMI_API_KEY")
    if not upstream_base or not upstream_key:
        raise SystemExit("CLIPROXY_API_BASE/CLIPROXY_API_KEY or KIMI_API_BASE/KIMI_API_KEY must be set")

    suite_names: list[str] = []
    if args.only in {"cumcm", "all"}:
        suite_names.append("cumcm")
    if args.only in {"mcm", "all"}:
        suite_names.append("mcm")

    args.jobs_dir.mkdir(parents=True, exist_ok=True)
    port = resolve_proxy_port(args, suite_names)
    proxy_base = f"http://127.0.0.1:{port}/v1"
    proxy_log_path = args.jobs_dir / f"{args.job_prefix}-proxy.log"

    commands = [
        harbor_command(
            job_name(args.job_prefix, suite_name),
            REPO_ROOT / "tasks" / suite_name.upper(),
            args.model,
            proxy_base,
            args.reasoning_effort,
            args.jobs_dir,
            args.n_concurrent,
            skip_tasks_for_suite(suite_name),
        )
        for suite_name in suite_names
    ]

    if args.dry_run:
        print(f"proxy_base={proxy_base}")
        for command in commands:
            print(" ".join(command))
        return 0

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
            run_env["OPENAI_BASE_URL"] = proxy_base

            failures = 0
            for command in commands:
                print(f"Running {' '.join(command)}", flush=True)
                completed = subprocess.run(command, cwd=REPO_ROOT, env=run_env)
                if completed.returncode != 0:
                    failures += 1
                    print(f"{command[command.index('--job-name') + 1]} exited with {completed.returncode}", flush=True)
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
