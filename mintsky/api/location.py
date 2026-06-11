import os
import json
import threading
import requests
from mintsky.constants import BASE_MGM, MGM_HEADERS, TIMEOUT, CONFIG_DIR, LOC_FILE

class LocationAPI:
    def fetch_locations_bg(self, callback):
        """Fetches locations in background and returns sorted_provinces and locs dictionary."""
        def _do():
            success, locs = self._fetch_locations()
            if success and callback:
                sorted_provinces = sorted(locs.keys())
                callback(sorted_provinces, locs)
        threading.Thread(target=_do, daemon=True).start()

    def _fetch_locations(self):
        for attempt in [self._try_mgm_ililce, self._try_cache, self._try_turkiyeapi]:
            success, locs = attempt()
            if success:
                return True, locs
        return False, {}

    def _try_mgm_ililce(self):
        try:
            r = requests.get(f"{BASE_MGM}/web/merkezler/ililcesi", headers=MGM_HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            locs = {}
            for item in r.json():
                il = item.get("il","")
                ilce = item.get("ilce","")
                if il:
                    locs.setdefault(il, [])
                    if ilce and ilce not in locs[il]:
                        locs[il].append(ilce)
            for il in locs:
                locs[il].sort()
            self._save_locs(locs)
            return True, locs
        except Exception as e:
            print(f"[LocationAPI] MGM Error: {e}")
            return False, {}

    def _try_cache(self):
        try:
            if os.path.exists(LOC_FILE):
                with open(LOC_FILE, "r", encoding="utf-8") as f:
                    locs = json.load(f)
                return True, locs
        except Exception as e:
            print(f"[LocationAPI] Cache Error: {e}")
        return False, {}

    def _try_turkiyeapi(self):
        try:
            r = requests.get("https://api.turkiyeapi.dev/v1/provinces", timeout=10)
            r.raise_for_status()
            locs = {
                p.get("name"): sorted([d.get("name") for d in p.get("districts", [])])
                for p in r.json().get("data", [])
            }
            self._save_locs(locs)
            return True, locs
        except Exception as e:
            print(f"[LocationAPI] TurkiyeAPI Error: {e}")
            return False, {}

    def _save_locs(self, locs):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(LOC_FILE, "w", encoding="utf-8") as f:
            json.dump(locs, f, ensure_ascii=False, indent=2)
