import os
import json

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
locales = [f for f in os.listdir(locales_dir) if f.endswith(".json")]

prof_translations = {
    "source_om": {
        "tr": "Veri Sağlayıcı: Open-Meteo",
        "en": "Data Provider: Open-Meteo",
    },
    "source_mgm": {
        "tr": "Veri Sağlayıcı: T.C. Meteoroloji Genel Müdürlüğü",
        "en": "Data Provider: Turkish State Meteorological Service",
    },
    "source_mgm_om_supported": {
        "tr": "& Open-Meteo",
        "en": "& Open-Meteo",
    }
}

for loc in locales:
    lang = loc.replace(".json", "")
    path = os.path.join(locales_dir, loc)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, trans_dict in prof_translations.items():
        data[key] = trans_dict.get(lang, trans_dict["en"])
            
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Professional translations updated.")
