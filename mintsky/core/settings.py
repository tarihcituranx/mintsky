import os
import json
from mintsky.constants import CONFIG_DIR, SETTING_FILE

import keyring

def load_settings():
    import shutil
    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}
        if os.path.exists(SETTING_FILE):
            try:
                shutil.copy(SETTING_FILE, SETTING_FILE + ".bak")
                print("[MintSky] Ayar dosyası bozuk, yedeklendi (.bak) ve varsayılanlara dönüldü.")
            except Exception:
                pass
    
    try:
        key = keyring.get_password("mintsky", "groq_api_key")
        if key:
            data["groq_api_key"] = key
    except Exception:
        pass
        
    return data

def save_settings(data):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    keyring_failed = False
    if "groq_api_key" in data:
        key = data.pop("groq_api_key")
        try:
            if key:
                keyring.set_password("mintsky", "groq_api_key", key)
            else:
                keyring.delete_password("mintsky", "groq_api_key")
        except Exception:
            keyring_failed = True
            
    with open(SETTING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        
    return not keyring_failed
