#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

STATE = Path('/home/ubuntu/.openclaw/cron/model-watch.json')
CFG = Path('/home/ubuntu/.openclaw/openclaw.json')
LOG = Path('/tmp/openclaw/model-watch.log')


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(LOG.read_text() + f'[{ts}] {msg}\n' if LOG.exists() else f'[{ts}] {msg}\n')


def load_cfg():
    data = json.loads(CFG.read_text(encoding='utf-8'))
    defaults = data.get('agents', {}).get('defaults', {}).get('model', {}).get('primary')
    main = None
    for agent in data.get('agents', {}).get('list', []):
        if agent.get('id') == 'main':
            main = agent.get('model')
            break
    return defaults, main


def load_state():
    if not STATE.exists():
        return None, None
    try:
        data = json.loads(STATE.read_text(encoding='utf-8'))
        return data.get('defaults'), data.get('main')
    except Exception:
        return None, None


def save_state(defaults, main):
    STATE.write_text(json.dumps({'defaults': defaults, 'main': main}, ensure_ascii=False), encoding='utf-8')


def restart_gateway():
    subprocess.run(['systemctl', '--user', 'restart', 'openclaw-gateway.service'], check=False)


def main():
    if not CFG.exists():
        log('openclaw.json missing, skip')
        return
    defaults, main_model = load_cfg()
    s_defaults, s_main = load_state()
    if defaults != s_defaults or main_model != s_main:
        log(f'model change detected defaults={s_defaults}->{defaults}, main={s_main}->{main_model}; restarting gateway')
        save_state(defaults, main_model)
        restart_gateway()
    else:
        # touch state if empty
        if s_defaults is None and s_main is None:
            save_state(defaults, main_model)

if __name__ == '__main__':
    main()
