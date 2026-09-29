import json
import os

_translations = {}
_current_lang = "tr"
SUPPORTED_LANGUAGES = ("tr", "en", "de", "fr", "az", "ar", "fa", "zh")


def load_language(lang="tr"):
    global _translations, _current_lang
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if lang not in SUPPORTED_LANGUAGES:
        lang = "tr"

    locale_file = os.path.join(base_dir, "locales", f"{lang}.json")
    try:
        with open(locale_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
        if not isinstance(translations, dict) or not translations:
            raise ValueError("locale root must be a non-empty object")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"[MintSky] Dil dosyası yüklenemedi ({lang}): {exc}")
        lang = "tr"
        try:
            with open(os.path.join(base_dir, "locales", "tr.json"), "r", encoding="utf-8") as f:
                translations = json.load(f)
        except (OSError, json.JSONDecodeError, ValueError):
            translations = {}

    _translations = translations
    _current_lang = lang


def _(key):
    return _translations.get(key, key)
