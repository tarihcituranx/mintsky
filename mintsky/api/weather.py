import concurrent.futures
import math
import os
import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from mintsky.constants import BASE_MGM, BASE_OM, MGM_HEADERS, TIMEOUT

session = requests.Session()
session.headers.update(MGM_HEADERS)
retry_policy = Retry(
    total=2,
    connect=2,
    read=1,
    status=2,
    backoff_factor=0.8,
    status_forcelist=(429, 500, 502, 503, 504),
    respect_retry_after_header=True,
    allowed_methods=frozenset(("GET",)),
)
session.mount("https://", HTTPAdapter(max_retries=retry_policy))


class WeatherAPI:
    _response_cache = {}
    _response_cache_lock = threading.Lock()

    @classmethod
    def _get_json(cls, url, *, params=None, cache_key=None, cache_ttl=0):
        now = time.monotonic()
        if cache_key and cache_ttl:
            with cls._response_cache_lock:
                cached = cls._response_cache.get(cache_key)
                if cached and now - cached[0] < cache_ttl:
                    return cached[1]
        response = session.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = cls.safe_json(response)
        if cache_key and cache_ttl:
            with cls._response_cache_lock:
                cls._response_cache[cache_key] = (time.monotonic(), data)
                if len(cls._response_cache) > 256:
                    oldest = min(cls._response_cache, key=lambda key: cls._response_cache[key][0])
                    cls._response_cache.pop(oldest, None)
        return data

    @staticmethod
    def meteoalerts_for_center(alerts, center_id):
        """Normalize current MGM MeteoAlarm schema for a single center."""
        try:
            center_id = int(center_id)
        except (TypeError, ValueError):
            return []
        matched = []
        for alert in alerts if isinstance(alerts, list) else []:
            towns = alert.get("towns", {})
            texts = alert.get("text", {})
            weather = alert.get("weather", {})
            if not all(isinstance(value, dict) for value in (towns, texts, weather)):
                continue
            for level in ("red", "orange", "yellow"):
                region_ids = towns.get(level, [])
                if not isinstance(region_ids, list):
                    continue
                try:
                    covers_center = center_id in {int(value) for value in region_ids}
                except (TypeError, ValueError):
                    covers_center = False
                if not covers_center:
                    continue
                description = texts.get(level)
                if not isinstance(description, str) or not description.strip():
                    continue
                phenomena = weather.get(level, [])
                matched.append(
                    {
                        "level": level,
                        "description": description.strip(),
                        "phenomena": phenomena if isinstance(phenomena, list) else [],
                        "begin": alert.get("begin", ""),
                        "end": alert.get("end", ""),
                    }
                )
                break
        return matched

    @staticmethod
    def nearest_center(centers, latitude, longitude):
        """Return the closest valid MGM center for the given coordinates."""
        nearest = None
        nearest_distance = float("inf")
        for center in centers if isinstance(centers, list) else []:
            try:
                lat = float(center["enlem"])
                lon = float(center["boylam"])
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue
                lat1, lat2 = math.radians(latitude), math.radians(lat)
                dlat = lat2 - lat1
                dlon = math.radians(lon - longitude)
                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                distance = 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                if distance < nearest_distance:
                    nearest, nearest_distance = center, distance
            except (KeyError, TypeError, ValueError):
                continue
        return nearest

    @classmethod
    def find_nearest_location(cls, latitude, longitude):
        """Resolve coordinates to the nearest province/district using MGM data."""
        try:
            province_centers = cls._get_json(
                f"{BASE_MGM}/web/merkezler/iller",
                cache_key="mgm:province-centers",
                cache_ttl=86400,
            )
            province_center = cls.nearest_center(
                province_centers, float(latitude), float(longitude)
            )
            if not province_center or not province_center.get("il"):
                return None

            city_centers = cls._get_json(
                f"{BASE_MGM}/web/merkezler",
                params={"il": province_center["il"]},
                cache_key=f"mgm:city-centers:{province_center['il']}",
                cache_ttl=3600,
            )
            return cls.nearest_center(city_centers, float(latitude), float(longitude)) or province_center
        except (requests.RequestException, TypeError, ValueError) as exc:
            print(f"[MintSky MGM konum] {exc}")
            return None

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
            merk = cls._get_json(
                f"{BASE_MGM}/web/merkezler",
                params={"il": il, **({"ilce": ilce} if ilce else {})},
            )
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

            turkey_today = datetime.now(ZoneInfo("Europe/Istanbul"))
            urls = {
                "sd": f"/web/sondurumlar?merkezid={mid}",
                "gd": f"/web/tahminler/gunluk?istno={m.get('gunlukTahminIstNo')}",
                "sk": f"/web/tahminler/saatlik?istno={m.get('saatlikTahminIstNo')}",
                "alarmlar": "/web/alarmlar",
                "meteoalarm": "/web/meteoalarm/today",
                "ucdeger": (
                    f"/web/ucdegerler?merkezid={mid}"
                    f"&ay={turkey_today.month}&gun={turkey_today.day}"
                ),
            }
            results = {}

            def get_url(key, url):
                cache_ttl = {
                    "gd": 600,
                    "sk": 300,
                    "alarmlar": 120,
                    "meteoalarm": 120,
                    "ucdeger": 21600,
                }.get(key, 0)
                cache_key = f"mgm:{url}" if cache_ttl else None
                return cls._get_json(
                    f"{BASE_MGM}{url}", cache_key=cache_key, cache_ttl=cache_ttl
                )

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
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
            sd_data["_ucdegerler"] = get_first(results, "ucdeger")
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
