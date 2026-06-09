#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MintSky — Linux Mint Masaüstü & Görev Çubuğu Uygulaması
MGM resmi API + Open-Meteo yedek/hybrid + Groq AI Hava Danışmanı
Finans Modülü: Truncgil Finance API (Altın, Gümüş, Döviz, Kripto)
Portföy Takibi: Alım fiyatı girişi, kar/zarar hesaplama
Geliştirici : https://github.com/tarihcituranx (Turan Kaya)
Versiyon    : 6.2 (Rate Limit Cache, Finans Yenile, Bugfix)
Lisans      : MIT
"""
import sys
import gi
gi.require_version("Gtk", "3.0")
try:
    gi.require_version("Notify", "0.7")
    from gi.repository import Notify
    HAS_NOTIFY = True
except Exception:
    HAS_NOTIFY = False
from gi.repository import Gtk, GLib, Gdk
try:
    gi.require_version("AppIndicator3", "0.1")
    from gi.repository import AppIndicator3
    HAS_INDICATOR = True
except Exception:
    try:
        gi.require_version("AyatanaAppIndicator3", "0.1")
        from gi.repository import AyatanaAppIndicator3 as AppIndicator3
        HAS_INDICATOR = True
    except Exception:
        HAS_INDICATOR = False
import requests
import threading
import json
import os
import shutil
import time
import webbrowser
import uuid
import concurrent.futures
from datetime import datetime

from mintsky.constants import *
# ─── Sabitler ─────────────────────────────────────────────────────────────
BASE_MGM      = "https://servis.mgm.gov.tr"

def _safe_icon(icon_name):
    try:
        theme = Gtk.IconTheme.get_default()
        sym   = f"{icon_name}-symbolic"
        if theme.has_icon(sym):      return sym
        if theme.has_icon(icon_name): return icon_name
        if theme.has_icon("weather-few-clouds-symbolic"): return "weather-few-clouds-symbolic"
    except Exception: pass
    return "dialog-information"

def yon(derece):
    return YONLER[round(derece/22.5)%16] if derece not in (None,-9999) and derece >= 0 else ""

def fmt_date(iso):
    try:
        dt  = datetime.strptime(iso.split("T")[0], "%Y-%m-%d")
        gun = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][dt.weekday()]
        ay  = ["","Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz",
               "Ağustos","Eylül","Ekim","Kasım","Aralık"][dt.month]
        return f"{gun} {dt.day} {ay}"
    except Exception: return iso

def fmt_time(iso_z):
    try: return datetime.fromisoformat(iso_z.replace("Z","+00:00")).astimezone().strftime("%H:%M")
    except Exception: return str(iso_z)[11:16]

def fmt_dt(iso_z):
    try: return datetime.fromisoformat(iso_z.replace("Z","+00:00")).astimezone().strftime("%d.%m.%Y %H:%M")
    except Exception: return str(iso_z)[:16]

def val(v, fmt="{:.0f}", suffix=""):
    return f"{fmt.format(v)}{suffix}" if v not in (None,-9999) else "—"

def fmt_try(v):
    """TRY formatı: binlik nokta, 2 ondalık"""
    if v is None or v == -9999: return "—"
    if abs(v) >= 1000:
        return f"{v:,.2f} ₺".replace(",",".")
    return f"{v:.2f} ₺"

def fmt_pct(v):
    if v is None: return "—"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"

def hadise_mgm(kod):  return HADISE.get(kod) or ("🌡️", kod or "—", "")
def hadise_wmo(kod):  return WMO_HADISE.get(int(kod),("🌡️","Bilinmiyor","")) if kod is not None else ("🌡️","—","")

# ─── CSS ──────────────────────────────────────────────────────────────────
