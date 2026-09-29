import threading
import time

import requests

from mintsky.constants import FINANCE_API, FINANCE_CACHE_TTL, TIMEOUT

session = requests.Session()


def parse_price(value):
    """Parse API price strings without treating a decimal point as grouping."""
    if value is None or value == "":
        return None
    try:
        if isinstance(value, str):
            value = value.strip().replace("\u00a0", "").replace(" ", "")
            if "," in value and "." in value:
                decimal_separator = "," if value.rfind(",") > value.rfind(".") else "."
                grouping_separator = "." if decimal_separator == "," else ","
                value = value.replace(grouping_separator, "")
                if decimal_separator == ",":
                    value = value.replace(",", ".")
            else:
                value = value.replace(",", ".")
        price = float(value)
        return price if price == price and abs(price) != float("inf") else None
    except (TypeError, ValueError, OverflowError):
        return None


class FinanceAPI:
    def __init__(self):
        self._data = {}
        self._last_fetch = 0.0
        self._update_date = ""
        self._lock = threading.Lock()
        self._fetching = False

    def fetch_bg(self, force=False, callback=None):
        """Arka planda finans çekimi yapar ve tamamlandığında callback(success) çağırır."""

        def _do():
            success, _ = self.fetch(force=force)
            if callback:
                callback(success)

        threading.Thread(target=_do, daemon=True).start()

    def fetch(self, force=False):
        """Rate-limited finans çekimi. force=True ise önbellek atlanır."""
        now = time.time()
        with self._lock:
            if not force and (now - self._last_fetch < FINANCE_CACHE_TTL):
                return False, self._data
            if self._fetching:
                return False, self._data
            self._fetching = True

        success = False
        try:
            r = session.get(FINANCE_API, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            rates = data.get("Rates") if isinstance(data, dict) else None
            if not isinstance(rates, dict) or not rates:
                raise ValueError("Finance API returned an invalid Rates object")
            clean_rates = {
                code: values
                for code, values in rates.items()
                if isinstance(code, str) and isinstance(values, dict)
            }
            if not clean_rates:
                raise ValueError("Finance API returned no usable rates")
            with self._lock:
                self._data = clean_rates
                meta = data.get("Meta_Data")
                self._update_date = (
                    meta.get("Update_Date", "") if isinstance(meta, dict) else ""
                )
                self._last_fetch = time.time()
                self._fetching = False
            success = True
        except Exception as e:
            print(f"[MintSky Finans API] Hatası: {e}")
            with self._lock:
                self._fetching = False

        return success, self._data

    def get_rate_price(self, kod):
        """Bir kodun güncel alış fiyatını döndür (TRY)"""
        with self._lock:
            if not self._data or kod not in self._data:
                return None
            r = self._data[kod]
            try:
                if r.get("Type") == "CryptoCurrency":
                    val = r.get("TRY_Price")
                else:
                    val = r.get("Buying") or r.get("Selling")
                return parse_price(val)
            except Exception:
                return None

    def reset_cache(self):
        with self._lock:
            self._last_fetch = 0.0
