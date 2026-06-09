import json
import os
from datetime import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from mintsky.constants import HADISE, WMO_HADISE, YONLER

def _safe_icon(icon_name):
    try:
        theme = Gtk.IconTheme.get_default()
        sym = f"{icon_name}-symbolic"
        if theme.has_icon(sym): return sym
        if theme.has_icon(icon_name): return icon_name
        if theme.has_icon("weather-few-clouds-symbolic"): return "weather-few-clouds-symbolic"
    except Exception:
        pass
    return "dialog-information"

def yon(derece):
    return YONLER[round(derece / 22.5) % 16] if derece not in (None, -9999) and derece >= 0 else ""

def fmt_date(iso):
    try:
        dt = datetime.strptime(iso.split("T")[0], "%Y-%m-%d")
        gun = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][dt.weekday()]
        ay = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
              "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"][dt.month]
        return f"{gun} {dt.day} {ay}"
    except Exception:
        return iso

def fmt_time(iso_z):
    try:
        return datetime.fromisoformat(iso_z.replace("Z", "+00:00")).astimezone().strftime("%H:%M")
    except Exception:
        return str(iso_z)[11:16]

def fmt_dt(iso_z):
    try:
        return datetime.fromisoformat(iso_z.replace("Z", "+00:00")).astimezone().strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(iso_z)[:16]

def val(v, fmt="{:.0f}", suffix=""):
    return f"{fmt.format(v)}{suffix}" if v not in (None, -9999) else "—"

def hadise_mgm(kod):
    return HADISE.get(kod) or ("🌡️", kod or "—", "")

def hadise_wmo(kod):
    return WMO_HADISE.get(int(kod), ("🌡️", "Bilinmiyor", "")) if kod is not None else ("🌡️", "—", "")

def safe_json(resp, default=None):
    try:
        return resp.json() if resp.text.strip() else (default if default is not None else [])
    except Exception:
        return default if default is not None else []
