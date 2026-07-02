import os
import json

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
en_file = os.path.join(locales_dir, "en.json")
tr_file = os.path.join(locales_dir, "tr.json")

with open(en_file, "r") as f:
    en_data = json.load(f)
with open(tr_file, "r") as f:
    tr_data = json.load(f)

# Update English
en_data.update({
    "lbl_precip_1h": "Precip 1h",
    "lbl_precip_24h": "Precip 24h",
    "lbl_snow": "Snow",
    "lbl_precip_now": "Precip (now)",
    "btn_gps_tt": "Find location via GPS",
    "btn_pin_tt": "Set this location as default",
    "btn_fav_tt": "Add/remove this location to favorites",
    "btn_list_tt": "My favorite lists",
    "search_city": "Select / Type City",
    "search_district": "Select / Type District",
    "lbl_last_update": "Last update",
    "tray_show_hide": "Show / Hide Window",
    "tray_refresh": "Refresh Weather",
    "tray_update": "Check for Updates"
})
with open(en_file, "w") as f:
    json.dump(en_data, f, indent=2, ensure_ascii=False)

# Update Turkish
tr_data.update({
    "lbl_humidity": "Nem",
    "lbl_wind": "Rüzgar",
    "lbl_pressure": "Basınç",
    "lbl_visibility": "Görüş",
    "lbl_precip_1h": "Yağış 1s",
    "lbl_precip_24h": "Yağış 24s",
    "lbl_sea": "Deniz",
    "lbl_clouds": "Bulutluluk",
    "lbl_snow": "Kar",
    "lbl_uv": "UV İndeksi",
    "lbl_wind_gust": "Rüzgar Gustu",
    "lbl_dew_point": "Çiğ Noktası",
    "lbl_precip_now": "Yağış (anlık)",
    "lbl_rain_prob": "Yağış Olas.",
    "lbl_sunshine": "Güneşlenme",
    "pill_sunrise": "G. Doğuşu",
    "pill_sunset": "G. Batışı",
    "btn_gps_tt": "GPS ile konumu bul",
    "btn_pin_tt": "Bu konumu varsayılan yap",
    "btn_fav_tt": "Bu konumu favorilere ekle/çıkar",
    "btn_list_tt": "Favori listelerim",
    "search_city": "İl Seç / Yaz",
    "search_district": "İlçe Seç / Yaz",
    "lbl_last_update": "Son ölçüm",
    "tray_show_hide": "Pencereyi Göster / Gizle",
    "tray_refresh": "Hava Durumunu Yenile",
    "tray_update": "Güncellemeleri Denetle"
})
with open(tr_file, "w") as f:
    json.dump(tr_data, f, indent=2, ensure_ascii=False)

print("en.json and tr.json updated.")
