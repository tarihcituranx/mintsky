import os
import urllib.request

WEATHER_DIR = "/home/turan/Belgeler/mintsky/mintsky/assets/weather"
os.makedirs(WEATHER_DIR, exist_ok=True)

WEATHER_ICONS = {
    "clear-day": "wi-day-sunny.svg",
    "clear-night": "wi-night-clear.svg",
    "partly-cloudy-day": "wi-day-cloudy.svg",
    "partly-cloudy-night": "wi-night-partly-cloudy.svg",
    "cloudy": "wi-cloudy.svg",
    "overcast": "wi-cloudy.svg",
    "rain": "wi-rain.svg",
    "drizzle": "wi-sprinkle.svg",
    "thunderstorm": "wi-thunderstorm.svg",
    "snow": "wi-snow.svg",
    "fog": "wi-fog.svg",
    "wind": "wi-strong-wind.svg",
    "unknown": "wi-na.svg"
}

BASE_URL = "https://raw.githubusercontent.com/erikflowers/weather-icons/master/svg/"

print("Downloading Erik Flowers weather icons...")
for key, filename in WEATHER_ICONS.items():
    url = BASE_URL + filename
    dest = os.path.join(WEATHER_DIR, f"{key}.svg")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded {key}.")
    except Exception as e:
        print(f"Failed to download {key}: {e}")

print("Done!")
