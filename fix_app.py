import re

with open("mintsky/ui/app.py", "r") as f:
    code = f.read()

# C1
code = code.replace("GLib.timeout_add(100, self._btn_refresh_clicked, None)", "GLib.timeout_add(100, lambda *_: self._search(force=True) or False)")

# C2
code = code.replace("self._get_rate_price", "self.finance_api.get_rate_price")

# C4
code = code.replace('threading.Thread(target=lambda: _run_ai(""), daemon=True).start()', '_run_ai("")')

# M6
code = re.sub(r'except:\s*self\._msg_dialog\(dlg,"Hata","Geçersiz miktar\."\);\s*return', r'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz miktar."); return', code)
code = re.sub(r'except:\s*self\._msg_dialog\(dlg,"Hata","Geçersiz alım fiyatı\."\);\s*return', r'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz alım fiyatı."); return', code)
code = code.replace("except: return None", "except (json.JSONDecodeError, ValueError): return None")
code = code.replace('except: t_str = "--"', 'except (IndexError, TypeError): t_str = "--"')
code = code.replace("except: dt_fmt = tarih", "except (ValueError, TypeError): dt_fmt = tarih")

# M7
code = code.replace("except Exception: pass", "except Exception as e: print(f'Hata: {e}')")

# L1 & L2 (unused/duplicate imports)
code = code.replace("import sqlite3\n", "")
code = code.replace("import urllib.request\n", "")
code = code.replace("import urllib.error\n", "")

# L6
code = code.replace("if latest > VERSIYON:", "if self._is_newer(latest, VERSIYON):")

# L7
code = code.replace("PORTFÖYÜm", "PORTFÖYÜM")

# L8
code = code.replace('elif om_data.get("daily"):', 'elif om_data and om_data.get("daily"):')

# L9
if 'Notify.init("mintsky")' not in code:
    code = code.replace('gi.require_version("Notify", "0.7")\nfrom gi.repository import Notify', 'gi.require_version("Notify", "0.7")\nfrom gi.repository import Notify\nNotify.init("mintsky")')

# L11
code = code.replace('subprocess.run([edge_bin', 'subprocess.run([edge_bin', 1) # wait, we can just regex
code = re.sub(r'subprocess\.run\(\[(edge_bin|player|backup_player).*?\)', r'\g<0>, timeout=60', code)

with open("mintsky/ui/app.py", "w") as f:
    f.write(code)
print("done first batch")
