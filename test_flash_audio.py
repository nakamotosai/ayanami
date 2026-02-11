import urllib.request
import json
import base64
import sys

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'

# Testing base gemini-2.5-flash with AUDIO modality
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}'

payload = {
    'contents': [{'parts': [{'text': 'Say: Hello. Give me an audio response.'}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO']
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print(f"Testing {url} with AUDIO modality...")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print("SUCCESS")
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"FAILED: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"ERROR: {e}")
