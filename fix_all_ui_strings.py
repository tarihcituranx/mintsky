import os
import json

app_file = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(app_file, "r") as f:
    code = f.read()

# Replace hardcoded metric labels
replacements = {
    '"💧 Nem"': 'f"💧 {_(\'lbl_humidity\')}"',
    '"💨 Rüzgar"': 'f"💨 {_(\'lbl_wind\')}"',
    '"🔵 Basınç"': 'f"🔵 {_(\'lbl_pressure\')}"',
    '"👁 Görüş"': 'f"👁 {_(\'lbl_visibility\')}"',
    '"🌧 Yağış 1s"': 'f"🌧 {_(\'lbl_precip_1h\')}"',
    '"🌧 Yağış 24s"': 'f"🌧 {_(\'lbl_precip_24h\')}"',
    '"🌊 Deniz"': 'f"🌊 {_(\'lbl_sea\')}"',
    '"☁ Bulutluluk"': 'f"☁ {_(\'lbl_clouds\')}"',
    '"❄ Kar"': 'f"❄ {_(\'lbl_snow\')}"',
    '"🔆 UV İndeksi"': 'f"🔆 {_(\'lbl_uv\')}"',
    '"💨 Rüzgar Gustu"': 'f"💨 {_(\'lbl_wind_gust\')}"',
    '"🌡 Çiğ Noktası"': 'f"🌡 {_(\'lbl_dew_point\')}"',
    '"🌧 Yağış (anlık)"': 'f"🌧 {_(\'lbl_precip_now\')}"',
    '"🌂 Yağış Olas."': 'f"🌂 {_(\'lbl_rain_prob\')}"',
    '"☀ Güneşlenme"': 'f"☀ {_(\'lbl_sunshine\')}"',
    '"🌅 G. Doğuşu"': 'f"🌅 {_(\'pill_sunrise\')}"',
    '"🌇 G. Batışı"': 'f"🌇 {_(\'pill_sunset\')}"',
    
    # Tool buttons
    '"📍","GPS Bul",  "GPS ile konumu bul"': '"📍", _("btn_gps"), _("btn_gps_tt")',
    '"🏠","Sabitle",  "Bu konumu varsayılan yap"': '"🏠", _("btn_pin"), _("btn_pin_tt")',
    '"⭐","Favorile","Bu konumu favorilere ekle/çıkar"': '"⭐", _("btn_fav_add"), _("btn_fav_tt")',
    '"📋","Favorilerim","Favori listelerim"': '"📋", _("btn_list"), _("btn_list_tt")',
    '"💰","Finans","Finans & Portföy Yönetimi"': '"💰", _("btn_finance"), _("btn_finance_tt")',
    
    # Combo entries
    '"İl Seç / Yaz"': '_("search_city")',
    '"İlçe Seç / Yaz"': '_("search_district")',
    
    # Text labels
    '"Hissedilen "': '_("lbl_feels_like") + " "',
    'f"Hissedilen {val(his,suffix=\'°\')}"': 'f"{_(\'lbl_feels_like\')} {val(his,suffix=\'°\')}"',
    'f"Son ölçüm: {fmt_dt(sd[\'veriZamani\'])}"': 'f"{_(\'lbl_last_update\')}: {fmt_dt(sd[\'veriZamani\'])}"',
    
    # Tray menu
    '"🪟 Pencereyi Göster / Gizle"': 'f"🪟 {_(\'tray_show_hide\')}"',
    '"🌤️ Hava Durumunu Yenile"': 'f"🌤️ {_(\'tray_refresh\')}"',
    '"💰 Finans & Portföy"': 'f"💰 {_(\'btn_finance\')}"',
    '"🔄 Güncellemeleri Denetle"': 'f"🔄 {_(\'tray_update\')}"',
}

for old_s, new_s in replacements.items():
    code = code.replace(old_s, new_s)

with open(app_file, "w") as f:
    f.write(code)

print("Replaced all hardcoded Turkish strings in app.py with i18n keys.")
