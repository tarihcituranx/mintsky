import concurrent.futures
import requests
from mintsky.constants import BASE_MGM, MGM_HEADERS, TIMEOUT, BASE_OM

class WeatherAPI:
    @staticmethod
    def safe_json(resp, default=None):
        try: return resp.json() if resp.text.strip() else (default if default is not None else [])
        except Exception: return default if default is not None else []

    @classmethod
    def fetch_weather(cls, il, ilce):
        try:
            req = requests.get(
                f"{BASE_MGM}/web/merkezler?il={il}" + (f"&ilce={ilce}" if ilce else ""),
                headers=MGM_HEADERS, timeout=TIMEOUT)
            merk = cls.safe_json(req)
            if not merk:
                return False, f"'{il}' verisi MGM'den alınamadı veya engellendi.\nLütfen tekrar deneyin.", None

            m = merk[0]
            lat = m.get("enlem") or m.get("lat")
            lon = m.get("boylam") or m.get("lon")
            mid = m["merkezId"]

            urls = {
                "sd":         f"/web/sondurumlar?merkezid={mid}",
                "gd":         f"/web/tahminler/gunluk?istno={m.get('gunlukTahminIstNo')}",
                "sk":         f"/web/tahminler/saatlik?istno={m.get('saatlikTahminIstNo')}",
                "alarmlar":   "/web/alarmlar",
                "meteoalarm": "/web/meteoalarm/today",
            }
            results = {}
            def get_url(key, url):
                return cls.safe_json(requests.get(f"{BASE_MGM}{url}", headers=MGM_HEADERS, timeout=TIMEOUT))
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
                fmap = {ex.submit(get_url, k, v): k for k, v in urls.items()}
                for fut in concurrent.futures.as_completed(fmap):
                    k = fmap[fut]
                    try:    results[k] = fut.result()
                    except: results[k] = []

            om_data = {}
            if lat and lon:
                om_data = cls.fetch_openmeteo(lat, lon)

            sd_data    = results.get("sd",  [{}])[0] if results.get("sd")  else {}
            gd_data    = results.get("gd",  [{}])[0] if results.get("gd")  else {}
            sk_data    = results.get("sk",  [{}])[0] if results.get("sk")  else {}
            alarmlar   = results.get("alarmlar",   [])
            meteoalarm = results.get("meteoalarm", [])

            return True, "", (m, sd_data, gd_data, sk_data, alarmlar, meteoalarm, om_data)
        except Exception as e:
            return False, f"MGM Bağlantı Hatası — Lütfen Yenileyin.\nDetay: {str(e)[:60]}", None

    @classmethod
    def fetch_openmeteo(cls, lat, lon):
        try:
            params = {
                "latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 5,
                "current": ",".join([
                    "temperature_2m","apparent_temperature","relative_humidity_2m",
                    "precipitation","weather_code","surface_pressure",
                    "wind_speed_10m","wind_direction_10m","wind_gusts_10m",
                    "uv_index","visibility","cloud_cover","dew_point_2m",
                ]),
                "hourly": ",".join([
                    "temperature_2m","precipitation_probability",
                    "wind_speed_10m","uv_index","weather_code",
                ]),
                "daily": ",".join([
                    "temperature_2m_max","temperature_2m_min","precipitation_sum",
                    "precipitation_probability_max","uv_index_max",
                    "wind_speed_10m_max","sunshine_duration","weather_code",
                ]),
            }
            r = requests.get(BASE_OM, params=params, timeout=TIMEOUT)
            if r.status_code == 200: return r.json()
        except Exception: pass
        return {}
