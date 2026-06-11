import time
import threading
import requests
from mintsky.constants import FINANCE_API, FINANCE_CACHE_TTL, TIMEOUT

class FinanceAPI:
    def __init__(self):
        self._data = {}
        self._last_fetch = 0.0
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
            r = requests.get(FINANCE_API, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            with self._lock:
                self._data = data.get("Rates", {})
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
            if r.get("Type") == "CryptoCurrency":
                return r.get("TRY_Price")
            return r.get("Buying") or r.get("Selling")

    def reset_cache(self):
        with self._lock:
            self._last_fetch = 0.0
