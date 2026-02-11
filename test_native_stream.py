import urllib.request
import json
import base64
import sys

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'

# Testing gemini-2.5-flash-native-audio-latest with streamGenerateContent
url = f'https://generativelanguage.googleapis.com/v1alpha/models/gemini-2.5-flash-native-audio-latest:streamGenerateContent?key={api_key}'

payload = {
    'contents': [{'parts': [{'text': 'Say: Hello. This is a streaming test.'}]}],
    'generationConfig': {
        'responseModalities': ['AUDIO']
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    print(f"Testing {url} with streaming...")
    with urllib.request.urlopen(req) as resp:
        # streamGenerateContent returns a stream of JSON objects
        for line in resp:
            if line:
                print("CHUNK RECEIVED")
                # print(line.decode())
except urllib.error.HTTPError as e:
    print(f"FAILED: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"ERROR: {e}")
