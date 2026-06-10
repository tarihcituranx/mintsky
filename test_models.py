import requests
import json
from mintsky.constants import GROQ_API_URL

api_key = ""
with open("/home/turan/.config/mintsky_settings.json", "r") as f:
    api_key = json.load(f).get("groq_api_key", "")

r = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)
for m in r.json().get("data", []):
    print(m.get("id"))
