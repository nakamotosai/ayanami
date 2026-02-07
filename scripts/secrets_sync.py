#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import secrets
from pathlib import Path

BASE_DIR = Path("/home/ubuntu/.openclaw")
OPENCLAW_JSON = BASE_DIR / "openclaw.json"
SECRETS_DIR = BASE_DIR / "credentials"
SECRETS_JSON = SECRETS_DIR / "secrets.json"
SECRETS_ENV = SECRETS_DIR / "secrets.env"
OPENCLAW_ENV = BASE_DIR / ".env"


def _load_openclaw_json() -> dict:
    raw = OPENCLAW_JSON.read_text(encoding="utf-8")
    cleaned = re.sub(r",\s*([\]}])", r"\1", raw)
    return json.loads(cleaned)


def _write_env_files(env_lines: list[str]) -> None:
    SECRETS_ENV.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    SECRETS_ENV.chmod(0o600)
    OPENCLAW_ENV.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    OPENCLAW_ENV.chmod(0o600)


def _write_secrets_env(secrets_data: dict) -> None:
    env = []
    hooks = secrets_data.get("hooks", {})
    gateway = secrets_data.get("gateway", {})
    channels = secrets_data.get("channels", {})
    providers = secrets_data.get("providers", {})

    if hooks.get("token"):
        env.append(f"HOOKS_TOKEN={hooks['token']}")
    if hooks.get("sourceToken"):
        env.append(f"HOOKS_SOURCE_TOKEN={hooks['sourceToken']}")
    if gateway.get("authToken"):
        env.append(f"GATEWAY_AUTH_TOKEN={gateway['authToken']}")
    if gateway.get("port"):
        env.append(f"GATEWAY_PORT={gateway['port']}")

    if channels.get("telegram", {}).get("botToken"):
        env.append(f"TELEGRAM_BOT_TOKEN={channels['telegram']['botToken']}")
    if channels.get("discord", {}).get("token"):
        env.append(f"DISCORD_BOT_TOKEN={channels['discord']['token']}")
    if channels.get("line", {}).get("channelSecret"):
        env.append(f"LINE_CHANNEL_SECRET={channels['line']['channelSecret']}")
    if channels.get("line", {}).get("channelAccessToken"):
        env.append(f"LINE_CHANNEL_ACCESS_TOKEN={channels['line']['channelAccessToken']}")

    if providers:
        for name, pdata in providers.items():
            if pdata.get("apiKey"):
                env.append(f"PROVIDER_{name.upper()}_API_KEY={pdata['apiKey']}")

    _write_env_files(env)


def export_secrets() -> None:
    cfg = _load_openclaw_json()
    secrets_data = {
        "hooks": {
            "token": (cfg.get("hooks") or {}).get("token", ""),
            "sourceToken": "",
            "path": (cfg.get("hooks") or {}).get("path", "/hooks"),
        },
        "gateway": {
            "authToken": ((cfg.get("gateway") or {}).get("auth") or {}).get("token", ""),
            "port": (cfg.get("gateway") or {}).get("port", 18789),
        },
        "channels": {
            "telegram": {
                "botToken": (cfg.get("channels") or {}).get("telegram", {}).get("botToken", ""),
            },
            "discord": {
                "token": (cfg.get("channels") or {}).get("discord", {}).get("token", ""),
            },
            "line": {
                "channelSecret": (cfg.get("channels") or {}).get("line", {}).get("channelSecret", ""),
                "channelAccessToken": (cfg.get("channels") or {}).get("line", {}).get("channelAccessToken", ""),
            },
        },
        "providers": {},
    }

    providers = (cfg.get("models") or {}).get("providers") or {}
    for name, pdata in providers.items():
        api_key = pdata.get("apiKey")
        if api_key:
            secrets_data["providers"][name] = {"apiKey": api_key}

    if not secrets_data["hooks"].get("sourceToken"):
        secrets_data["hooks"]["sourceToken"] = secrets.token_hex(24)

    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    SECRETS_JSON.write_text(json.dumps(secrets_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SECRETS_JSON.chmod(0o600)
    _write_secrets_env(secrets_data)


def apply_secrets() -> None:
    if not SECRETS_JSON.exists():
        raise SystemExit("secrets.json not found")
    secrets_data = json.loads(SECRETS_JSON.read_text(encoding="utf-8"))
    cfg = _load_openclaw_json()

    hooks = secrets_data.get("hooks", {})
    if hooks.get("token"):
        cfg.setdefault("hooks", {})["token"] = hooks["token"]

    gateway = secrets_data.get("gateway", {})
    if gateway.get("authToken"):
        cfg.setdefault("gateway", {}).setdefault("auth", {})["token"] = gateway["authToken"]

    channels = secrets_data.get("channels", {})
    if channels.get("telegram", {}).get("botToken"):
        cfg.setdefault("channels", {}).setdefault("telegram", {})["botToken"] = channels["telegram"]["botToken"]
    if channels.get("discord", {}).get("token"):
        cfg.setdefault("channels", {}).setdefault("discord", {})["token"] = channels["discord"]["token"]
    if channels.get("line", {}).get("channelSecret"):
        cfg.setdefault("channels", {}).setdefault("line", {})["channelSecret"] = channels["line"]["channelSecret"]
    if channels.get("line", {}).get("channelAccessToken"):
        cfg.setdefault("channels", {}).setdefault("line", {})["channelAccessToken"] = channels["line"]["channelAccessToken"]

    providers = secrets_data.get("providers", {})
    if providers:
        cfg.setdefault("models", {}).setdefault("providers", {})
        for name, pdata in providers.items():
            if pdata.get("apiKey"):
                cfg["models"]["providers"].setdefault(name, {})["apiKey"] = pdata["apiKey"]

    OPENCLAW_JSON.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync OpenClaw secrets with credentials files")
    ap.add_argument("--export", action="store_true", help="export from openclaw.json to secrets files")
    ap.add_argument("--apply", action="store_true", help="apply secrets.json to openclaw.json")
    args = ap.parse_args()

    if args.apply:
        apply_secrets()
    else:
        export_secrets()


if __name__ == "__main__":
    main()
