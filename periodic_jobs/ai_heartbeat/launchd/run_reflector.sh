#!/bin/zsh
set -euo pipefail

WORKSPACE_ROOT="/Users/erqianwang/Repos/agentic-workspace"
cd "$WORKSPACE_ROOT"

set -a
source "$WORKSPACE_ROOT/.env"
set +a

PORT="${OPENCODE_BASE_URL##*:}"
if [[ -z "$PORT" || "$PORT" == "$OPENCODE_BASE_URL" ]]; then
  PORT="4096"
fi

for _ in {1..30}; do
  if nc -z 127.0.0.1 "$PORT" >/dev/null 2>&1; then
    exec "$WORKSPACE_ROOT/.venv/bin/python" "$WORKSPACE_ROOT/periodic_jobs/ai_heartbeat/reflector.py"
  fi
  sleep 2
done

echo "OpenCode server is not reachable on port $PORT" >&2
exit 1
