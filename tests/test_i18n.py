import json
import os

import pytest

from mintsky import i18n


def test_i18n_keys_match():
    locales_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "mintsky", "locales"
    )
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


def test_supported_locales_are_valid_and_share_the_same_keys():
    locale_dir = os.path.join(os.path.dirname(i18n.__file__), "locales")
    with open(os.path.join(locale_dir, "tr.json"), encoding="utf-8") as stream:
        base = json.load(stream)
    for language in i18n.SUPPORTED_LANGUAGES:
        with open(os.path.join(locale_dir, f"{language}.json"), encoding="utf-8") as stream:
            values = json.load(stream)
        assert set(base).issubset(values)
        assert all(isinstance(value, str) and value for value in values.values())


def test_invalid_language_falls_back_without_path_access():
    i18n.load_language("../../etc/passwd")
    try:
        assert i18n._current_lang == "tr"
        assert i18n._("app_title") == "MintSky"
    finally:
        i18n.load_language("tr")


def test_english_weather_labels_are_sensible():
    i18n.load_language("en")
    try:
        assert i18n._("btn_search") == "Search"
        assert i18n._("lbl_humidity") == "Humidity"
        assert i18n._("lbl_visibility") == "Visibility"
        assert i18n._("settings_theme") == "Theme"
    finally:
        i18n.load_language("tr")


def test_weather_labels_are_not_mistranslated_in_locales():
    checks = {
        "de": {"lbl_humidity": "Luftfeuchtigkeit", "lbl_visibility": "Sichtweite", "lbl_dew_point": "Taupunkt"},
        "fr": {"lbl_humidity": "Humidité", "lbl_visibility": "Visibilité", "lbl_dew_point": "Point de rosée"},
        "zh": {"lbl_humidity": "湿度", "lbl_visibility": "能见度", "lbl_dew_point": "露点"},
        "ar": {"lbl_humidity": "الرطوبة", "lbl_visibility": "مدى الرؤية", "lbl_dew_point": "نقطة الندى"},
        "tr": {"lbl_rain_prob": "Yağış İhtimali", "wind_violent_storm": "Şiddetli fırtına"},
    }
    for lang, expected in checks.items():
        i18n.load_language(lang)
        try:
            for key, exp_val in expected.items():
                assert i18n._(key) == exp_val, f"Failed for {lang} {key}"
        finally:
            i18n.load_language("tr")
