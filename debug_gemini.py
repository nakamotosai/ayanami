import urllib.request
import json
import base64
import sys

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}'

payload = {
    'contents': [{'parts': [{'text': 'Say cheerfully: Have a wonderful day!'}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO'],
        'speechConfig': {
            'voiceConfig': {
                'prebuiltVoiceConfig': {
                    'voiceName': 'Aoede'
                }
            }
        }
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print("SUCCESS")
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"FAILED: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"ERROR: {e}")
