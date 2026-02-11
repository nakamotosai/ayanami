import urllib.request
import json
import base64
import sys
import os

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}'

text = "Aoede: 叽～主人，我是 Aoede。我想测试一下双人对话是否工作。\nCharon: 我是 Charon，听到我的声音了吗？[laugh]"

payload = {
    'contents': [{'parts': [{'text': text}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO'],
        'speechConfig': {
            'multiSpeakerVoiceConfig': {
                'speakerVoiceConfigs': [
                    {'speaker': 'Aoede', 'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': 'Aoede'}}},
                    {'speaker': 'Charon', 'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': 'Charon'}}}
                ]
            }
        }
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print("正在请求 Gemini API (Single Call Multi-Speaker)...")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        audio_data = base64.b64decode(data['candidates'][0]['content']['parts'][0]['inlineData']['data'])
        with open('basic_demo.wav', 'wb') as f:
            f.write(audio_data)
        print("SUCCESS: 写入 basic_demo.wav")
except Exception as e:
    print(f"FAILED: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode())
