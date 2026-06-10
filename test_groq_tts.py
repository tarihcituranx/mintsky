import requests
import json
from mintsky.constants import GROQ_API_URL

api_key = ""
with open("/home/turan/.config/mintsky_settings.json", "r") as f:
    api_key = json.load(f).get("groq_api_key", "")

r = requests.post(
    "https://api.groq.com/openai/v1/audio/speech",
    headers={"Authorization": f"Bearer {api_key}",
             "Content-Type": "application/json"},
    json={
        "model": "canopylabs/orpheus-v1-english",
        "input": "Deneme bir iki üç.",
        "voice": "Nova",
        "response_format": "wav"
    },
    timeout=30
)
print(r.status_code)
if r.status_code != 200:
    print(r.text)
else:
    print("TTS SUCCESS")
