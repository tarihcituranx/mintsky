import re
import os

# --- i18n.py ---
with open("mintsky/i18n.py", "r") as f:
    i18n = f.read()
i18n = i18n.replace(
    "_translations = json.load(f)",
    "try:\n                _translations = json.load(f)\n            except (json.JSONDecodeError, ValueError):\n                print(f'[MintSky] i18n: {lang}.json parse hatası')\n                _translations = {}"
)
with open("mintsky/i18n.py", "w") as f:
    f.write(i18n)

# --- app.py ---
with open("mintsky/ui/app.py", "r") as f:
    app = f.read()

# C1
app = app.replace("self._btn_refresh_clicked", "lambda *_: self._search(force=True) or False")

# C2
app = app.replace("self._get_rate_price", "self.finance_api.get_rate_price")

# C3 & C5 (Notification threading & nesting)
app = app.replace("""
                    if self._notify_enabled and HAS_NOTIFY:
                        n = Notify.Notification.new(
                            "🔄 MintSky Güncellemesi",
                            f"Yeni sürüm hazır: v{tag}\\nGitHub'dan indirip güncelleyebilirsiniz.",
                            _safe_icon("software-update-available")
                        )
                        GLib.idle_add(n.show)
""", """
                        if self._notify_enabled and HAS_NOTIFY:
                            def _show_notif():
                                n = Notify.Notification.new(
                                    "🔄 MintSky Güncellemesi",
                                    f"Yeni sürüm hazır: v{tag}\\nGitHub'dan indirip güncelleyebilirsiniz.",
                                    _safe_icon("software-update-available")
                                )
                                n.show()
                                return False
                            GLib.idle_add(_show_notif)
""")

app = app.replace("""
                if self._notify_enabled and HAS_NOTIFY:
                    n = Notify.Notification.new(title, body, icon)
                    n.set_urgency(2 if yeni else 1)
                    GLib.idle_add(n.show)
""", """
                if self._notify_enabled and HAS_NOTIFY:
                    def _show_notif_tray(t=title, b=body, i=icon, y=yeni):
                        n = Notify.Notification.new(t, b, i)
                        n.set_urgency(2 if y else 1)
                        n.show()
                        return False
                    GLib.idle_add(_show_notif_tray)
""")

# C4
app = app.replace('threading.Thread(target=lambda: _run_ai(""), daemon=True).start()', '_run_ai("")')

# M1, M2
app = app.replace(
    "self._fetch_in_progress = False\n        self._tray_busy = False",
    "self._fetch_in_progress = False\n        self._tray_busy = False\n        self._fetch_lock = threading.Lock()\n        self._tray_lock = threading.Lock()"
)
app = app.replace("if self._tray_busy: return\n        self._tray_busy = True", "with self._tray_lock:\n            if self._tray_busy: return\n            self._tray_busy = True")
app = app.replace("if not il: self._tray_busy = False; return", "if not il: return")
app = app.replace("if not data: self._tray_busy = False; return", "if not data: return")
app = app.replace("finally: self._tray_busy = False", "finally:\n            with self._tray_lock:\n                self._tray_busy = False")

# M3 & M4 (fetch thread safety)
old_fetch = """        def _fetch():
            self._fetch_in_progress = True
            try:
                data = self.weather_api.fetch_weather(il, ilce)
                if not data:
                    GLib.idle_add(self._status, "Hata", True)
                    return
                m, sd, gd, sk, alarmlar, meteoalarm, om_data = data
                self._cur_lat = m.get("enlem") or m.get("lat")
                self._cur_lon = m.get("boylam") or m.get("lon")

                self._weather_cache    = data
                self._weather_cache_ts = time.time()
                self._weather_cache_key= c_key

                GLib.idle_add(self._render, data)
            except Exception: pass
            self._fetch_in_progress = False"""

new_fetch = """        def _fetch():
            with self._fetch_lock:
                self._fetch_in_progress = True
            try:
                data = self.weather_api.fetch_weather(il, ilce)
                if not data:
                    GLib.idle_add(self._status, "Hata", True)
                    return
                m, sd, gd, sk, alarmlar, meteoalarm, om_data = data
                
                def _update_cache(d=data, k=c_key, m_dict=m):
                    self._cur_lat = m_dict.get("enlem") or m_dict.get("lat")
                    self._cur_lon = m_dict.get("boylam") or m_dict.get("lon")
                    self._weather_cache    = d
                    self._weather_cache_ts = time.time()
                    self._weather_cache_key= k
                    self._render(d)
                    return False
                
                GLib.idle_add(_update_cache)
            except Exception as e: print(f"Fetch hatası: {e}")
            finally:
                with self._fetch_lock:
                    self._fetch_in_progress = False"""

app = app.replace(old_fetch, new_fetch)

app = app.replace("if self._fetch_in_progress and not force:", "with self._fetch_lock:\n            if self._fetch_in_progress and not force:\n                return False")
app = app.replace("self._fetch_in_progress = True", "with self._fetch_lock:\n            self._fetch_in_progress = True")

# M6
app = re.sub(r'except:\s*self\._msg_dialog\(dlg,"Hata","Geçersiz miktar\."\);\s*return', r'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz miktar."); return', app)
app = re.sub(r'except:\s*self\._msg_dialog\(dlg,"Hata","Geçersiz alım fiyatı\."\);\s*return', r'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz alım fiyatı."); return', app)
app = app.replace('except: return None', 'except (json.JSONDecodeError, ValueError): return None')
app = app.replace('except: t_str = "--"', 'except (IndexError, TypeError): t_str = "--"')
app = app.replace('except: dt_fmt = tarih', 'except (ValueError, TypeError): dt_fmt = tarih')

# M7
app = app.replace('except Exception: pass', 'except Exception as e: print(f"Hata: {e}")')

# M9
app = app.replace('seviye = int(ma.get("seviye", 1))', 'try: seviye = int(ma.get("seviye", 1))\n            except (ValueError, TypeError): seviye = 1')

# L1, L2
app = app.replace('import sqlite3\n', '')
app = app.replace('import urllib.request\n', '')
app = app.replace('import urllib.error\n', '')

# L6
app = app.replace('if latest > VERSIYON:', 'if self._is_newer(latest, VERSIYON):')

# L7
app = app.replace('PORTFÖYÜm', 'PORTFÖYÜM')

# L8
app = app.replace('elif om_data.get("daily"):', 'elif om_data and om_data.get("daily"):')

# L9
if 'Notify.init' not in app:
    app = app.replace('gi.require_version("Notify", "0.7")\nfrom gi.repository import Notify', 'gi.require_version("Notify", "0.7")\nfrom gi.repository import Notify\nNotify.init("mintsky")')

# L10 & L11
old_tts = """                # Sesi Çal
                if os.system("command -v paplay >/dev/null 2>&1") == 0:
                    subprocess.run(["paplay", tmp_path], check=True)
                else:
                    subprocess.run(["aplay", tmp_path], check=True)
                
                # Temizlik
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)"""

new_tts = """                # Sesi Çal
                try:
                    if os.system("command -v paplay >/dev/null 2>&1") == 0:
                        subprocess.run(["paplay", tmp_path], check=True, timeout=60)
                    else:
                        subprocess.run(["aplay", tmp_path], check=True, timeout=60)
                finally:
                    # Temizlik
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)"""

app = app.replace(old_tts, new_tts)
app = re.sub(r'subprocess\.run\(\[(edge_bin|backup_player)(.*?)\)', r'subprocess.run([\1\2), timeout=60', app)

with open("mintsky/ui/app.py", "w") as f:
    f.write(app)

print("done script")
