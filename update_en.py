import json
import os

base_dir = "/home/turan/Belgeler/mintsky/mintsky"
locales_dir = os.path.join(base_dir, "locales")
en_file = os.path.join(locales_dir, "en.json")

with open(en_file, "r", encoding="utf-8") as f:
    en_data = json.load(f)

# Hardcoded translations from user's screenshot and constants
updates = {
    # Buttons
    "btn_fav_remove": "Remove Fav",
    "lbl_hourly_forecast": "HOURLY FORECAST",
    "lbl_daily_forecast": "5-DAY FORECAST",
    
    # Wind directions
    "Kuzey": "North",
    "Kuzey Kuzeydoğu": "North Northeast",
    "Kuzeydoğu": "Northeast",
    "Doğu Kuzeydoğu": "East Northeast",
    "Doğu": "East",
    "Doğu Güneydoğu": "East Southeast",
    "Güneydoğu": "Southeast",
    "Güney Güneydoğu": "South Southeast",
    "Güney": "South",
    "Güney Güneybatı": "South Southwest",
    "Güneybatı": "Southwest",
    "Batı Güneybatı": "West Southwest",
    "Batı": "West",
    "Batı Kuzeybatı": "West Northwest",
    "Kuzeybatı": "Northwest",
    "Kuzey Kuzeybatı": "North Northwest",
    
    # Common weather labels (HADISE / WMO_HADISE)
    "Açık": "Clear",
    "Hava tamamen güneşli ve bulutsuz.": "Completely sunny and cloudless.",
    "Az Bulutlu": "Mostly Clear",
    "Parçalı Bulutlu": "Partly Cloudy",
    "Çok Bulutlu": "Mostly Cloudy",
    "Kapalı": "Overcast",
    "Sisli": "Foggy",
    "Puslu": "Haze",
    "Hafif Yağmurlu": "Light Rain",
    "Yağmurlu": "Rain",
    "Kuvvetli Yağmurlu": "Heavy Rain",
    "Sağanak Yağışlı": "Rain Showers",
    "Kar Yağışlı": "Snow",
    "Hafif Kar Yağışlı": "Light Snow",
    "Yoğun Kar Yağışlı": "Heavy Snow",
    "Karla Karışık Yağmurlu": "Sleet",
    "Gök Gürültülü Sağanak Yağışlı": "Thunderstorm Showers",
    "Duman": "Smoke",
    "Pus": "Haze",
    "Sıcak": "Hot",
    "Soğuk": "Cold",
    "Güneşli": "Sunny",
    "Aralıklı Yağışlı": "Intermittent Rain",
    "Rüzgarlı": "Windy",
    "Fırtına": "Storm",
    "Bilinmiyor": "Unknown",
    "—": "—"
}

for k, v in updates.items():
    if k not in en_data or en_data[k] == k:
        en_data[k] = v

with open(en_file, "w", encoding="utf-8") as f:
    json.dump(en_data, f, indent=4, ensure_ascii=False)

print("Updated en.json with weather descriptions.")
