import os
import json
from mintsky.constants import CONFIG_DIR, SETTING_FILE, DEFAULT_FINANCE_ALTIN, DEFAULT_FINANCE_DOVIZ, DEFAULT_FINANCE_KRIPTO

def load_settings():
    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(data):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(SETTING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
