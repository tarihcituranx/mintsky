import os
import json
import pytest

def test_i18n_keys_match():
    locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mintsky", "locales")
    if not os.path.exists(locales_dir):
        pytest.skip("Locales directory not found")

    locale_files = [f for f in os.listdir(locales_dir) if f.endswith(".json")]
    if "tr.json" not in locale_files:
        pytest.skip("Base locale tr.json not found")

    with open(os.path.join(locales_dir, "tr.json"), "r", encoding="utf-8") as f:
        base_keys = set(json.load(f).keys())

    for loc in locale_files:
        if loc == "tr.json":
            continue
        with open(os.path.join(locales_dir, loc), "r", encoding="utf-8") as f:
            loc_keys = set(json.load(f).keys())
        
        missing = base_keys - loc_keys
        
        assert not missing, f"Locale {loc} is missing keys: {missing}"
