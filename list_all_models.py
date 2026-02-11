import urllib.request
import json

api_key = 'AIzaSyAHDvVnl6oKj-a57qTi1To4uDZgqm917ZA'
url = f'https://generativelanguage.googleapis.com/v1alpha/models?key={api_key}'

try:
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())
        for model in data.get('models', []):
            methods = model.get('supportedGenerationMethods', [])
            if 'generateContent' in methods:
                print(f"MODEL: {model['name']}")
                print(f"  METHODS: {methods}")
                print(f"  MODALITIES: {model.get('inputTokenLimit')}") # Proxy for details
except Exception as e:
    print(f"ERROR: {e}")
