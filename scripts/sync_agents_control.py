#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

BASE_WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
OPENCLAW_CONFIG = Path("/home/ubuntu/.openclaw/openclaw.json")
CONTROL_FILE = BASE_WORKSPACE / "config" / "agents" / "control.yaml"
CORE_FILES = ["AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md", "TOOLS.md", "HEARTBEAT.md", "IDENTITY.md"]


def load_control():
    if not CONTROL_FILE.exists():
        raise SystemExit(f"control file missing: {CONTROL_FILE}")
    with CONTROL_FILE.open() as f:
        data = yaml.safe_load(f)
    if not data or "agents" not in data:
        raise SystemExit("control file must contain an 'agents' list")
    return data["agents"]


def load_config():
    if not OPENCLAW_CONFIG.exists():
        raise SystemExit(f"openclaw config missing: {OPENCLAW_CONFIG}")
    with OPENCLAW_CONFIG.open() as f:
        return json.load(f)


def ensure_workspace(agent_workspace: str) -> Path:
    path = Path(agent_workspace)
    if not path.is_absolute():
        path = (BASE_WORKSPACE / agent_workspace).resolve()
    path.mkdir(parents=True, exist_ok=True)
    for core in CORE_FILES:
        src = BASE_WORKSPACE / core
        dst = path / core
        if src.exists() and not dst.exists():
            shutil.copy(src, dst)
    memory_dir = path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    return path


def build_agent_list(agents, default_model):
    entries = []
    bindings = []
    workspace_records = []
    for agent in agents:
        workspace = agent.get("workspace")
        if not workspace:
            raise SystemExit(f"agent {agent['id']} missing workspace")
        ws_path = ensure_workspace(workspace)
        entries.append(
            {
                "id": agent["id"],
                "name": agent["name"],
                "workspace": str(ws_path),
                "model": agent.get("model", default_model),
            }
        )
        match = {"channel": agent["channel"]}
        if "peer" in agent:
            match_peer = dict(agent["peer"])
            if "id" in match_peer:
                match_peer["id"] = str(match_peer["id"])
            match["peer"] = match_peer
        bindings.append({"agentId": agent["id"], "match": match})
        workspace_records.append(str(ws_path))
    return entries, bindings, workspace_records


def dump_config(config):
    with OPENCLAW_CONFIG.open("w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def restart_gateway():
    subprocess.run(["openclaw", "gateway", "restart"], check=True)


def main():
    parser = argparse.ArgumentParser(description="Sync agents from control file into openclaw config.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned config without writing")
    parser.add_argument("--no-restart", action="store_true", help="Skip restarting the gateway")
    args = parser.parse_args()

    agents = load_control()
    config = load_config()
    default_model = config["agents"]["defaults"]["model"]["primary"]

    new_list, new_bindings, workspace_paths = build_agent_list(agents, default_model)

    planned = {
        "agents": new_list,
        "bindings": new_bindings,
    }

    if args.dry_run:
        print("Planned agents list:")
        print(json.dumps(new_list, indent=2, ensure_ascii=False))
        print("Planned bindings list:")
        print(json.dumps(new_bindings, indent=2, ensure_ascii=False))
        return

    config["agents"]["list"] = new_list
    config["bindings"] = new_bindings
    dump_config(config)

    print("Updated openclaw.json agents/bindings from control file.")
    print("Workspaces now present:")
    for ws in workspace_paths:
        print(f" - {ws}")

    if not args.no_restart:
        print("Restarting gateway to pick up new config...")
        restart_gateway()
    else:
        print("Skipping gateway restart at owner request.")


if __name__ == "__main__":
    main()
