import os
import json

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
en_file = os.path.join(locales_dir, "en.json")

with open(en_file, "r") as f:
    en_data = json.load(f)

for file in os.listdir(locales_dir):
    if file.endswith(".json") and file != "en.json":
        filepath = os.path.join(locales_dir, file)
        with open(filepath, "r") as f:
            data = json.load(f)
        
        updated = False
        for key, val in en_data.items():
            if key not in data:
                data[key] = val
                updated = True
        
        if updated:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {file} with missing English keys.")

print("Sync complete.")
