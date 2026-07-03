import os
import re

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

code = code.replace('"Fav\'dan Çıkar"', '_("btn_fav_remove")')

code = code.replace(
    'self._section_title("⏰  SAATLİK TAHMİN (Kaynak: MGM)")',
    'self._section_title(f"⏰  {_(\'lbl_hourly_forecast\')} (MGM)")'
)

code = code.replace(
    'self._section_title("⏰  SAATLİK TAHMİN (Kaynak: Open-Meteo)")',
    'self._section_title(f"⏰  {_(\'lbl_hourly_forecast\')} (Open-Meteo)")'
)

code = code.replace(
    'self._section_title("📅  5 GÜNLÜK TAHMİN (Kaynak: MGM)")',
    'self._section_title(f"📅  {_(\'lbl_daily_forecast\')} (MGM)")'
)

code = code.replace(
    'self._section_title("📅  5 GÜNLÜK TAHMİN (Kaynak: Open-Meteo)")',
    'self._section_title(f"📅  {_(\'lbl_daily_forecast\')} (Open-Meteo)")'
)

with open(file_path, "w") as f:
    f.write(code)

print("Hardcoded Turkish texts translated in app.py")
