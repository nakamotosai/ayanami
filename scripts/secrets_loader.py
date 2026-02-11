#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

BASE_DIR = Path('/home/ubuntu/.openclaw')
SECRETS_ENV = BASE_DIR / 'credentials' / 'secrets.env'
SECRETS_JSON = BASE_DIR / 'credentials' / 'secrets.json'
OPENCLAW_JSON = BASE_DIR / 'openclaw.json'


def _load_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        data[key.strip()] = value.strip()
    return data


def _load_openclaw_json() -> dict:
    if not OPENCLAW_JSON.exists():
        return {}
    raw = OPENCLAW_JSON.read_text(encoding='utf-8')
    cleaned = re.sub(r',\s*([\]}])', r'\1', raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


def load_secrets() -> dict:
    if SECRETS_JSON.exists():
        try:
            return json.loads(SECRETS_JSON.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pass
    env = _load_env(SECRETS_ENV)
    if env:
        return {'env': env}
    return {}


def resolve_hook_token() -> str:
    secrets = load_secrets()
    if isinstance(secrets.get('hooks'), dict) and secrets['hooks'].get('token'):
        return secrets['hooks']['token']
    env = secrets.get('env') or {}
    if env.get('HOOKS_TOKEN'):
        return env['HOOKS_TOKEN']
    cfg = _load_openclaw_json()
    return (cfg.get('hooks') or {}).get('token', '')


def resolve_hook_source_token() -> str:
    secrets = load_secrets()
    if isinstance(secrets.get('hooks'), dict) and secrets['hooks'].get('sourceToken'):
        return secrets['hooks']['sourceToken']
    env = secrets.get('env') or {}
    return env.get('HOOKS_SOURCE_TOKEN', '')


def resolve_gateway_port(default: int = 18789) -> int:
    secrets = load_secrets()
    env = secrets.get('env') or {}
    if env.get('GATEWAY_PORT'):
        try:
            return int(env['GATEWAY_PORT'])
        except ValueError:
            pass
    cfg = _load_openclaw_json()
    try:
        return int((cfg.get('gateway') or {}).get('port', default))
    except (TypeError, ValueError):
        return default


def resolve_hooks_path(default: str = '/hooks') -> str:
    cfg = _load_openclaw_json()
    path = (cfg.get('hooks') or {}).get('path', default) or default
    if not path.startswith('/'):
        path = '/' + path
    return path
