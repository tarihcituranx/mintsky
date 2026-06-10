import requests
import json
from mintsky.constants import GROQ_API_URL, GROQ_MODEL, GROQ_SYSTEM
from mintsky.ui.app import MintSkyApp

api_key = ""
with open("/home/turan/.config/mintsky_settings.json", "r") as f:
    api_key = json.load(f).get("groq_api_key", "")

print("API KEY:", api_key[:5] + "...")

r = requests.post(
    GROQ_API_URL,
    headers={"Authorization": f"Bearer {api_key}",
             "Content-Type": "application/json"},
    json={"model": GROQ_MODEL,
          "messages": [
              {"role": "system", "content": GROQ_SYSTEM},
              {"role": "user",   "content": "Ankara 15 derece güneşli"},
          ],
          "response_format": {"type": "json_object"},
          "max_tokens": 600, "temperature": 0.25},
    timeout=20
)
print(r.status_code)
print(r.text)
