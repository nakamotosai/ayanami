#!/usr/bin/env bash
set -euo pipefail

usage(){
  cat <<'EOF'
Usage: $0 AGENT_NAME [--workspace-root PATH] [--allow-existing]

Creates a skeleton for an always-on/persistent child agent workspace.

Examples:
  ./scripts/create-persistent-child-agent.sh chii-always-on
  ./scripts/create-persistent-child-agent.sh chii-monitor --workspace-root /home/ubuntu/.openclaw/always-on --allow-existing
EOF
}

# Default configuration
WORKSPACE_ROOT=""
ALLOW_EXISTING=

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace-root)
      WORKSPACE_ROOT="$2"
      shift 2
      ;;
    --allow-existing)
      ALLOW_EXISTING=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      if [[ -z "${AGENT_NAME:-}" ]]; then
        AGENT_NAME="$1"
        shift
      else
        echo "Unexpected argument: $1" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "${AGENT_NAME:-}" ]]; then
  echo "Agent name must be provided." >&2
  usage
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$REPO_ROOT/workspaces/agents}"
TARGET="${WORKSPACE_ROOT%/}/$AGENT_NAME"

if [[ -d "$TARGET" && -z "$ALLOW_EXISTING" ]]; then
  echo "Target workspace already exists: $TARGET" >&2
  exit 1
fi

mkdir -p "$TARGET"

CORE_FILES=(AGENTS.md SOUL.md USER.md MEMORY.md TOOLS.md)

for file in "${CORE_FILES[@]}"; do
  if [[ -f "$REPO_ROOT/$file" ]]; then
    cp "$REPO_ROOT/$file" "$TARGET/${file}"
  fi
done

mkdir -p "$TARGET/scripts" "$TARGET/config" "$TARGET/policies" "$TARGET/bindings"

cat <<EOF > "$TARGET/README.md"
# Persistent Child Agent: $AGENT_NAME

This workspace contains the always-on agent named $AGENT_NAME.
EOF

cp "$REPO_ROOT/skills/persistent-child-agent-workflow/templates/gateway-config.patch" "$TARGET/config/gateway-config.patch"
cp "$REPO_ROOT/skills/persistent-child-agent-workflow/templates/agent-rules.md" "$TARGET/policies/agent-rules.md"
cp "$REPO_ROOT/skills/persistent-child-agent-workflow/templates/bindings.yaml" "$TARGET/bindings/bindings.yaml"

cat <<EOF
Workspace created at: $TARGET
Review agent-rules and gateway patch before starting the agent.
EOF
