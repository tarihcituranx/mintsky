import json
import os

_translations = {}
_current_lang = "tr"

def load_language(lang="tr"):
    global _translations, _current_lang
    _current_lang = lang
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_file = os.path.join(base_dir, "locales", f"{lang}.json")
    if os.path.exists(locale_file):
        with open(locale_file, "r", encoding="utf-8") as f:
            _translations = json.load(f)
    else:
        _translations = {}

def _(key):
    return _translations.get(key, key)
