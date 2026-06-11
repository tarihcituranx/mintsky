import re

with open("mintsky/ui/app.py", "r") as f:
    app = f.read()

# Fix except: ...
app = app.replace('except: self._msg_dialog(dlg,"Hata","Geçersiz miktar."); return', 'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz miktar."); return')
app = app.replace('except: self._msg_dialog(dlg,"Hata","Geçersiz alım fiyatı."); return', 'except ValueError: self._msg_dialog(dlg,"Hata","Geçersiz alım fiyatı."); return')

app = re.sub(r'except:\s*(t_str = "--")', r'except (IndexError, TypeError): \1', app)
app = re.sub(r'except:\s*(dt_fmt = tarih)', r'except (ValueError, TypeError): \1', app)
# Let's fix line 1299
app = app.replace('except:\n                        return None', 'except (json.JSONDecodeError, ValueError):\n                        return None')

# Fix except Exception: pass
app = app.replace('except Exception: pass', 'except Exception as e: print(f"[MintSky] Hata: {e}")')

with open("mintsky/ui/app.py", "w") as f:
    f.write(app)

print("Excepts fixed")
