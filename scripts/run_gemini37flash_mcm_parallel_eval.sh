#!/usr/bin/env bash
set -euo pipefail

cd /Volumes/PSSD/code/My-Agent/Agent-Benchmark/terminal-bench-math-modeling

if [[ "${ALLOW_GEMINI_PARALLEL_MCM:-0}" != "1" ]]; then
  mkdir -p jobs
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Gemini parallel MCM is disabled; set ALLOW_GEMINI_PARALLEL_MCM=1 to run it intentionally." >> jobs/terminus2-gemini-3.7-flash-high-2024-2025-mcm-parallel-runner.log
  exit 0
fi

set -a
source /Volumes/PSSD/code/My-Agent/.env
set +a

export UPSTREAM_API_BASE="${CLIPROXY_API_BASE}"
export UPSTREAM_API_KEY="${CLIPROXY_API_KEY}"
export OPENAI_API_KEY="${CLIPROXY_API_KEY}"
export OPENAI_BASE_URL="http://127.0.0.1:30374/v1"
export PROXY_PORT="30374"

proxy_log="jobs/terminus2-gemini-3.7-flash-high-2024-2025-mcm-parallel-proxy.log"
runner_log="jobs/terminus2-gemini-3.7-flash-high-2024-2025-mcm-parallel-runner.log"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] starting proxy on http://127.0.0.1:30374/v1"
  python3 scripts/openai_cooldown_retry_proxy.py >> "${proxy_log}" 2>&1 &
  proxy_pid=$!
  trap 'kill "${proxy_pid}" 2>/dev/null || true' EXIT

  python3 - <<'PY'
import socket
import sys
import time

deadline = time.time() + 20
while time.time() < deadline:
    sock = socket.socket()
    sock.settimeout(0.5)
    try:
        sock.connect(("127.0.0.1", 30374))
        sock.close()
        sys.exit(0)
    except OSError:
        sock.close()
        time.sleep(0.2)
raise SystemExit("proxy did not open port 30374")
PY

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] starting harbor mcm parallel job"
  harbor run \
    --job-name terminus2-gemini-3.7-flash-high-2024-2025-mcm-parallel \
    --jobs-dir /Volumes/PSSD/code/My-Agent/Agent-Benchmark/terminal-bench-math-modeling/jobs \
    --path /Volumes/PSSD/code/My-Agent/Agent-Benchmark/terminal-bench-math-modeling/tasks/MCM \
    --agent terminus-2 \
    --model openai/gemini-3.7-flash-high \
    --agent-kwarg api_base=http://127.0.0.1:30374/v1 \
    --agent-kwarg record_terminal_session=false \
    --n-concurrent 1 \
    --yes \
    --exclude-task-name mcm-2023-a-plant-community \
    --exclude-task-name mcm-2023-b-maasai-mara \
    --exclude-task-name mcm-2023-c-wordle \
    --exclude-task-name mcm-2024-a-lamprey \
    --exclude-task-name mcm-2024-b-submersible-search \
    --exclude-task-name mcm-2024-c-tennis-momentum
  rc=$?
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] harbor exited with ${rc}"
  exit "${rc}"
} >> "${runner_log}" 2>&1
