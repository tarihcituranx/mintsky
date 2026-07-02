import os
import json

app_file = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(app_file, "r") as f:
    code = f.read()

# Replace hardcoded strings in _show_settings
code = code.replace('"🇹🇷 MGM — Meteoroloji Genel Müdürlüğü (Türkiye)"', '_("src_mgm")')
code = code.replace('"🌍 Open-Meteo — Uluslararası açık kaynak"', '_("src_om")')
code = code.replace('"💰  Finans"', 'f"💰  {_(\'settings_tab_finance\')}"')
code = code.replace('"Finans modülünü aktif et  (altın, döviz fiyatları)"', '_("settings_finance_enable")')
code = code.replace('"<b>🥇 Altın / Gümüş / Platin</b>"', 'f"<b>🥇 {_(\'settings_gold\')}</b>"')
code = code.replace('"<b>💵 Döviz Kurları</b>"', 'f"<b>💵 {_(\'settings_fx\')}</b>"')
code = code.replace('"Ücretsiz Groq API anahtarı: "', '_("settings_groq_free") + " "')
code = code.replace('"Test Et"', '_("settings_groq_test")')
code = code.replace('"Groq API Anahtarı"', '_("settings_groq_key")')
code = code.replace('"🌙 Karanlık"', 'f"🌙 {_(\'settings_theme_dark\')}"')
code = code.replace('"☀️ Aydınlık"', 'f"☀️ {_(\'settings_theme_light\')}"')
code = code.replace('"Tema"', '_("settings_theme")')
code = code.replace('"Arayüz Büyüklüğü"', '_("settings_scale")')
code = code.replace('"🚀 Uygulama Menüsüne Kısayol Ekle"', 'f"🚀 {_(\'settings_shortcut\')}"')
code = code.replace('"<small><i>Uygulama menüsünde \'MintSky\' adıyla görünmesini sağlar.\\nİkon dosyası (mintsky.png) ile aynı klasörde çalıştırılmalıdır.</i></small>"', '_("settings_shortcut_desc")')

# Add restart check
old_save = """            self._language       = cb_lang.get_active_id() or "tr"
            self._groq_api_key   = groq_entry.get_text().strip()
            self._fin_altin      = [k for k,c in altin_chks.items() if c.get_active()]
            self._fin_doviz      = [k for k,c in doviz_chks.items() if c.get_active()]
            self._save_settings()
            self._apply_css()"""

new_save = """            old_lang = self._language
            self._language       = cb_lang.get_active_id() or "tr"
            self._groq_api_key   = groq_entry.get_text().strip()
            self._fin_altin      = [k for k,c in altin_chks.items() if c.get_active()]
            self._fin_doviz      = [k for k,c in doviz_chks.items() if c.get_active()]
            self._save_settings()
            self._apply_css()
            if old_lang != self._language:
                self._msg_dialog(None, _("restart_required_title"), _("restart_required_msg"))"""

code = code.replace(old_save, new_save)

with open(app_file, "w") as f:
    f.write(code)

print("app.py strings replaced with i18n keys.")

# Update en.json
en_file = "/home/turan/Belgeler/mintsky/mintsky/locales/en.json"
with open(en_file, "r") as f:
    en_data = json.load(f)

en_data.update({
    "src_mgm": "🇹🇷 MGM — Turkish State Meteorological Service",
    "src_om": "🌍 Open-Meteo — Global Open Source",
    "settings_groq_free": "Free Groq API key:",
    "settings_groq_test": "Test",
    "settings_theme_dark": "Dark",
    "settings_theme_light": "Light",
    "settings_shortcut": "Add to Application Menu",
    "settings_shortcut_desc": "<small><i>Adds a shortcut named 'MintSky' to your app menu.\\nMust be run in the same folder as the icon (mintsky.png).</i></small>",
    "restart_required_title": "Restart Required",
    "restart_required_msg": "Please restart MintSky for the language changes to take full effect."
})

with open(en_file, "w") as f:
    json.dump(en_data, f, indent=2, ensure_ascii=False)

# Update tr.json
tr_file = "/home/turan/Belgeler/mintsky/mintsky/locales/tr.json"
with open(tr_file, "r") as f:
    tr_data = json.load(f)

tr_data.update({
    "src_mgm": "🇹🇷 MGM — Meteoroloji Genel Müdürlüğü (Türkiye)",
    "src_om": "🌍 Open-Meteo — Uluslararası açık kaynak",
    "settings_groq_free": "Ücretsiz Groq API anahtarı:",
    "settings_groq_test": "Test Et",
    "settings_theme_dark": "Karanlık",
    "settings_theme_light": "Aydınlık",
    "settings_shortcut": "Uygulama Menüsüne Kısayol Ekle",
    "settings_shortcut_desc": "<small><i>Uygulama menüsünde 'MintSky' adıyla görünmesini sağlar.\\nİkon dosyası (mintsky.png) ile aynı klasörde çalıştırılmalıdır.</i></small>",
    "restart_required_title": "Yeniden Başlatma Gerekli",
    "restart_required_msg": "Dil değişikliğinin tam olarak uygulanabilmesi için uygulamayı yeniden başlatmanız gerekmektedir."
})

with open(tr_file, "w") as f:
    json.dump(tr_data, f, indent=2, ensure_ascii=False)

print("Locales updated.")
