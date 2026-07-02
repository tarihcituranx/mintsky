import os
import json

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
en_file = os.path.join(locales_dir, "en.json")
tr_file = os.path.join(locales_dir, "tr.json")

with open(en_file, "r") as f:
    en_data = json.load(f)
with open(tr_file, "r") as f:
    tr_data = json.load(f)

# The keys we just added
new_keys = [
    "src_mgm", "src_om", "settings_groq_free", "settings_groq_test",
    "settings_theme_dark", "settings_theme_light", "settings_shortcut",
    "settings_shortcut_desc", "restart_required_title", "restart_required_msg",
    "settings_finance_enable", "settings_gold", "settings_fx", "settings_theme", "settings_scale"
]

# Ensure they exist in en.json if missed
en_data.update({
    "settings_finance_enable": "Enable Finance Module (Gold, FX)",
    "settings_gold": "Gold / Silver / Platinum",
    "settings_fx": "FX Rates",
    "settings_theme": "Theme",
    "settings_scale": "UI Scale"
})
with open(en_file, "w") as f:
    json.dump(en_data, f, indent=2, ensure_ascii=False)

tr_data.update({
    "settings_finance_enable": "Finans modülünü aktif et (altın, döviz fiyatları)",
    "settings_gold": "Altın / Gümüş / Platin",
    "settings_fx": "Döviz Kurları",
    "settings_theme": "Tema",
    "settings_scale": "Arayüz Büyüklüğü"
})
with open(tr_file, "w") as f:
    json.dump(tr_data, f, indent=2, ensure_ascii=False)

# Populate missing keys in all other languages with English fallback
for file in os.listdir(locales_dir):
    if file.endswith(".json") and file not in ["en.json", "tr.json"]:
        filepath = os.path.join(locales_dir, file)
        with open(filepath, "r") as f:
            data = json.load(f)
        
        updated = False
        for key in new_keys:
            if key not in data:
                data[key] = en_data.get(key, key)
                updated = True
        
        if updated:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {file} with fallback English keys.")

print("All language files populated.")
