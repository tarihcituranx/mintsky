import os
import json
import re

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
locales = [f for f in os.listdir(locales_dir) if f.endswith(".json")]

translations = {
    "source_om": {
        "tr": "Veri Kaynağı: Open-Meteo",
        "en": "Data Source: Open-Meteo",
        "de": "Datenquelle: Open-Meteo",
        "fr": "Source de données : Open-Meteo",
        "ar": "مصدر البيانات: أوبن-ميتيو",
        "fa": "منبع داده: اپن‌متیو",
        "zh": "数据源：Open-Meteo",
        "az": "Məlumat Mənbəyi: Open-Meteo"
    },
    "source_mgm": {
        "tr": "Veri Kaynağı: Meteoroloji Genel Müdürlüğü (MGM)",
        "en": "Data Source: Turkish State Meteorological Service (MGM)",
        "de": "Datenquelle: Türkischer Staatlicher Wetterdienst (MGM)",
        "fr": "Source de données : Service météorologique de l'État turc (MGM)",
        "ar": "مصدر البيانات: خدمة الأرصاد الجوية الحكومية التركية (MGM)",
        "fa": "منبع داده: سازمان هواشناسی دولتی ترکیه (MGM)",
        "zh": "数据源：土耳其国家气象局（MGM）",
        "az": "Məlumat Mənbəyi: Türkiyə Dövlət Meteorologiya Xidməti (MGM)"
    },
    "source_mgm_om_supported": {
        "tr": "(Open-Meteo Destekli)",
        "en": "(Supported by Open-Meteo)",
        "de": "(Unterstützt von Open-Meteo)",
        "fr": "(Soutenu par Open-Meteo)",
        "ar": "(بدعم من أوبن-ميتيو)",
        "fa": "(پشتیبانی شده توسط اپن‌متیو)",
        "zh": "(由 Open-Meteo 支持)",
        "az": "(Open-Meteo Dəstəkli)"
    },
    "pill_sunrise": {
        "tr": "Gün Doğumu",
        "en": "Sunrise",
        "de": "Sonnenaufgang",
        "fr": "Lever du soleil",
        "ar": "شروق الشمس",
        "fa": "طلوع خورشید",
        "zh": "日出",
        "az": "Gün Doğumu"
    },
    "pill_sunset": {
        "tr": "Gün Batımı",
        "en": "Sunset",
        "de": "Sonnenuntergang",
        "fr": "Coucher du soleil",
        "ar": "غروب الشمس",
        "fa": "غروب خورشید",
        "zh": "日落",
        "az": "Gün Batımı"
    },
    "pill_precip_prob": {
        "tr": "Yağış Olasılığı",
        "en": "Precip. Prob.",
        "de": "Niederschlagswahrscheinlichkeit",
        "fr": "Prob. de précip.",
        "ar": "احتمال هطول الأمطار",
        "fa": "احتمال بارش",
        "zh": "降水概率",
        "az": "Yağış Ehtimalı"
    }
}

for loc in locales:
    lang = loc.replace(".json", "")
    path = os.path.join(locales_dir, loc)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, trans_dict in translations.items():
        if key not in data:
            data[key] = trans_dict.get(lang, trans_dict["en"])
            
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Translations added.")

# Now patch app.py
app_py_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(app_py_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Replace source badge
old_badge = """        src_badge = Gtk.Label(
            label=("📡 Open-Meteo" if use_om else "📡 MGM") +
                  ("  +OM" if (not use_om and om_cur) else ""))"""

new_badge = """        if use_om:
            lbl_txt = _("source_om")
        else:
            lbl_txt = _("source_mgm")
            if om_cur:
                lbl_txt += " " + _("source_mgm_om_supported")

        src_badge = Gtk.Label(label=lbl_txt)"""

app_code = app_code.replace(old_badge, new_badge)

# Replace pills text with _()
app_code = app_code.replace('("🌅 Gün Doğumu",', '(_("pill_sunrise"),')
app_code = app_code.replace('("🌇 Gün Batımı",', '(_("pill_sunset"),')
app_code = app_code.replace('("🌂 Yağış Olasılığı",', '(_("pill_precip_prob"),')

with open(app_py_path, "w", encoding="utf-8") as f:
    f.write(app_code)

print("app.py patched with i18n.")
