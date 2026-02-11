import urllib.request
import json
import base64
import sys

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'

# Testing gemini-2.0-flash with streamGenerateContent and AUDIO modality
url = f'https://generativelanguage.googleapis.com/v1alpha/models/gemini-2.0-flash:streamGenerateContent?key={api_key}'

payload = {
    'contents': [{'parts': [{'text': 'Say: Hello. Provide an audio response.'}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO']
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print(f"Testing {url} with streaming audio modality...")
    with urllib.request.urlopen(req) as resp:
        for line in resp:
            if line:
                print("CHUNK RECEIVED")
                # print(line.decode())
except urllib.error.HTTPError as e:
    print(f"FAILED: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"ERROR: {e}")
