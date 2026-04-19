#!/bin/zsh
set -euo pipefail

WORKSPACE_ROOT="/Users/erqianwang/Repos/agentic-workspace"
cd "$WORKSPACE_ROOT"

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

set -a
source "$WORKSPACE_ROOT/.env"
set +a

OPENCODE_BIN="$(command -v opencode || true)"
if [[ -z "$OPENCODE_BIN" && -x "/opt/homebrew/bin/opencode" ]]; then
  OPENCODE_BIN="/opt/homebrew/bin/opencode"
fi
if [[ -z "$OPENCODE_BIN" ]]; then
  echo "opencode not found in PATH" >&2
  exit 1
fi

PORT="${OPENCODE_BASE_URL##*:}"
if [[ -z "$PORT" || "$PORT" == "$OPENCODE_BASE_URL" ]]; then
  PORT="4096"
fi

export OPENCODE_SERVER_USERNAME="${OPENCODE_USERNAME}"
export OPENCODE_SERVER_PASSWORD="${OPENCODE_PASSWORD}"

exec "$OPENCODE_BIN" serve --hostname 127.0.0.1 --port "$PORT"
