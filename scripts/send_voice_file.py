#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import requests

config_path = Path.home() / '.openclaw/openclaw.json'
if not config_path.exists():
    raise SystemExit(f'OpenClaw config not found at {config_path}')
config = json.loads(config_path.read_text(encoding='utf-8'))
bot_token = config.get('channels', {}).get('telegram', {}).get('botToken')
if not bot_token:
    raise SystemExit('Telegram bot token missing in openclaw.json')
chat_id = os.environ.get('CHII_TTS_TELEGRAM_TARGET', '8138445887')
file_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not file_arg or not file_arg.exists():
    raise SystemExit('Provide existing voice file path as argument')
caption = sys.argv[2] if len(sys.argv) > 2 else '播客速读'
url = f'https://api.telegram.org/bot{bot_token}/sendVoice'
with file_arg.open('rb') as fh:
    files = {'voice': (file_arg.name, fh)}
    data = {'chat_id': chat_id, 'caption': caption, 'parse_mode': 'HTML'}
    resp = requests.post(url, data=data, files=files, timeout=60)
    resp.raise_for_status()
print(resp.json())
