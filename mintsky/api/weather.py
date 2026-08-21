import concurrent.futures
import os

import requests

from mintsky.constants import BASE_MGM, BASE_OM, MGM_HEADERS, TIMEOUT

session = requests.Session()
session.headers.update(MGM_HEADERS)


class WeatherAPI:
    @staticmethod
    def safe_json(resp, default=None):
        try:
            return (
                resp.json()
                if resp.text.strip()
                else (default if default is not None else [])
            )
        except Exception:
            return default if default is not None else []

    @classmethod
    def fetch_weather(cls, il, ilce):
        try:
            req = session.get(
                f"{BASE_MGM}/web/merkezler?il={il}" + (f"&ilce={ilce}" if ilce else ""),
                timeout=TIMEOUT,
            )
            merk = cls.safe_json(req)
            if not merk:
                import urllib.parse

                q = urllib.parse.quote(f"{ilce} {il}".strip())
                from mintsky.constants import NOM_HEADERS

                nom_req = session.get(
                    f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1",
                    headers=NOM_HEADERS,
                    timeout=TIMEOUT,
                )
                nom_data = cls.safe_json(nom_req)
                if not nom_data:
                    return False, f"'{il}' verisi bulunamadı.", None

                try:
                    lat_str = nom_data[0].get("lat")
                    lon_str = nom_data[0].get("lon")
                    if not lat_str or not lon_str:
                        return False, "Koordinat verisi geçersiz.", None
                    m = {
                        "il": nom_data[0].get("display_name", il).split(",")[0],
                        "ilce": "",
                        "enlem": float(lat_str),
                        "boylam": float(lon_str),
                        "merkezId": 0,
                    }
                except (IndexError, ValueError, TypeError):
                    return False, "Konum bulunamadı veya veri bozuk.", None

                om_data = cls.fetch_openmeteo(m["enlem"], m["boylam"])
                msn_data = cls.fetch_msn(m["enlem"], m["boylam"])
                return True, "", (m, {}, {}, {}, [], [], om_data, msn_data)

            if not merk or not isinstance(merk, list) or len(merk) == 0:
                return False, "MGM API boş veya geçersiz yanıt döndürdü.", None

            m = merk[0]
            lat = m.get("enlem") or m.get("lat")
            lon = m.get("boylam") or m.get("lon")
            mid = m["merkezId"]

            urls = {
                "sd": f"/web/sondurumlar?merkezid={mid}",
                "gd": f"/web/tahminler/gunluk?istno={m.get('gunlukTahminIstNo')}",
                "sk": f"/web/tahminler/saatlik?istno={m.get('saatlikTahminIstNo')}",
                "alarmlar": "/web/alarmlar",
                "meteoalarm": "/web/meteoalarm/today",
            }
            results = {}

            def get_url(key, url):
                return cls.safe_json(
                    requests.get(
                        f"{BASE_MGM}{url}", headers=MGM_HEADERS, timeout=TIMEOUT
                    )
                )

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
                fmap = {ex.submit(get_url, k, v): k for k, v in urls.items()}
                for fut in concurrent.futures.as_completed(fmap):
                    k = fmap[fut]
                    try:
                        results[k] = fut.result()
                    except:
                        results[k] = []

            om_data = {}
            if lat and lon:
                om_data = cls.fetch_openmeteo(lat, lon)
            msn_data = cls.fetch_msn(lat, lon)

            def get_first(d, k):
                val = d.get(k)
                return val[0] if isinstance(val, list) and len(val) > 0 else {}

            sd_data = get_first(results, "sd")
            gd_data = get_first(results, "gd")
            sk_data = get_first(results, "sk")

            alarmlar = results.get("alarmlar")
            alarmlar = alarmlar if isinstance(alarmlar, list) else []
            meteoalarm = results.get("meteoalarm")
            meteoalarm = meteoalarm if isinstance(meteoalarm, list) else []

            return (
                True,
                "",
                (m, sd_data, gd_data, sk_data, alarmlar, meteoalarm, om_data, msn_data),
            )
        except Exception as e:
            return (
                False,
                f"MGM Bağlantı Hatası — Lütfen Yenileyin.\nDetay: {str(e)[:60]}",
                None,
            )

    @classmethod
    def fetch_msn(cls, lat, lon):
        try:
            url = "https://api.msn.com/weatherfalcon/weather/current"
            params = {
                "apikey": os.environ.get("MSN_API_KEY", ""),
                "appId": os.environ.get("MSN_APP_ID", ""),
                "latLongList": f"{lat},{lon}",
                "units": "C",
                "locale": "tr-tr",
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://www.msn.com/",
                "Origin": "https://www.msn.com",
            }
            r = session.get(url, params=params, headers=headers, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {}

    @classmethod
    def fetch_openmeteo(cls, lat, lon):

        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "timezone": "auto",
                "forecast_days": 5,
                "current": ",".join(
                    [
                        "temperature_2m",
                        "apparent_temperature",
                        "relative_humidity_2m",
                        "precipitation",
                        "weather_code",
                        "surface_pressure",
                        "wind_speed_10m",
                        "wind_direction_10m",
                        "wind_gusts_10m",
                        "uv_index",
                        "visibility",
                        "cloud_cover",
                        "dew_point_2m",
                        "is_day",
                    ]
                ),
                "hourly": ",".join(
                    [
                        "temperature_2m",
                        "precipitation_probability",
                        "wind_speed_10m",
                        "uv_index",
                        "weather_code",
                        "is_day",
                    ]
                ),
                "daily": ",".join(
                    [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "precipitation_probability_max",
                        "uv_index_max",
                        "wind_speed_10m_max",
                        "sunshine_duration",
                        "weather_code",
                        "sunrise",
                        "sunset",
                    ]
                ),
            }
            r = session.get(BASE_OM, params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {}
