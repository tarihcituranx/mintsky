#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MintSky — Linux Mint Masaüstü & Görev Çubuğu Uygulaması
MGM resmi API + Open-Meteo yedek/hybrid + Groq AI Hava Danışmanı
Finans Modülü: Truncgil Finance API (Altın, Gümüş, Döviz, Kripto)
Portföy Takibi: Alım fiyatı girişi, kar/zarar hesaplama
Geliştirici : https://github.com/tarihcituranx (Turan Kaya)
Versiyon    : 7.1.9
Lisans      : MIT
"""

import json
import math
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gi

gi.require_version("GdkPixbuf", "2.0")
gi.require_version("Gtk", "3.0")
from gi.repository import GdkPixbuf, Gtk

from .constants import HADISE, WMO_HADISE, YONLER
from .i18n import _

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
TR_TIMEZONE = ZoneInfo("Europe/Istanbul")


def _format_tr_time(value, pattern):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is not None:
        dt = dt.astimezone(TR_TIMEZONE)
    return dt.strftime(pattern)


def get_svg_image(icon_name, size=24, folder="weather"):
    """SVG dosyasını yükler ve belirtilen boyuta ölçekler."""
    if not icon_name or icon_name == "unknown":
        return Gtk.Label(label="?")
    path = os.path.join(ASSETS_DIR, folder, f"{icon_name}.svg")
    if not os.path.exists(path):
        return Gtk.Label(label="?")
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, size, size, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        return image
    except Exception:
        return Gtk.Label(label="?")


def yon(derece):
    if derece is None or derece == -9999 or not isinstance(derece, (int, float)):
        return ""
    if derece >= 0:
        val = YONLER[round(derece / 22.5) % 16]
        try:
            return _(val)
        except NameError:
            return val
    return ""


def fmt_date(iso):
    try:
        dt = datetime.strptime(iso.split("T")[0], "%Y-%m-%d")
        gun = [
            _("Pazartesi"),
            _("Salı"),
            _("Çarşamba"),
            _("Perşembe"),
            _("Cuma"),
            _("Cumartesi"),
            _("Pazar"),
        ][dt.weekday()]
        ay = [
            "",
            _("Ocak"),
            _("Şubat"),
            _("Mart"),
            _("Nisan"),
            _("Mayıs"),
            _("Haziran"),
            _("Temmuz"),
            _("Ağustos"),
            _("Eylül"),
            _("Ekim"),
            _("Kasım"),
            _("Aralık"),
        ][dt.month]
        return f"{dt.day} {ay} {gun}"
    except (ValueError, TypeError, AttributeError):
        return iso


def fmt_time(iso_z):
    try:
        return _format_tr_time(iso_z, "%H:%M")
    except (ValueError, TypeError, AttributeError):
        return str(iso_z)


def fmt_dt(iso_z):
    try:
        return _format_tr_time(iso_z, "%d.%m.%Y %H:%M")
    except (ValueError, TypeError, AttributeError):
        return str(iso_z)


def val(v, fmt="{:.0f}", suffix=""):
    return f"{fmt.format(v)}{suffix}" if v not in (None, -9999) else "—"


def fmt_try(v):
    """TRY formatı: binlik nokta, 2 ondalık"""
    if v is None or v == -9999:
        return "—"
    return f"{v:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(v):
    if v is None:
        return "—"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"


def wind_level_key(speed):
    """Return the localized Beaufort-style label key used by the MGM guide."""
    try:
        speed = float(speed)
        if not math.isfinite(speed) or speed < 0:
            return None
    except (TypeError, ValueError):
        return None
    thresholds = (
        (2, "wind_calm"),
        (6, "wind_breeze"),
        (12, "wind_light"),
        (20, "wind_mild"),
        (29, "wind_moderate"),
        (39, "wind_fresh"),
        (50, "wind_strong"),
        (62, "wind_near_gale"),
        (75, "wind_gale"),
        (89, "wind_strong_gale"),
        (103, "wind_storm"),
    )
    return next((key for limit, key in thresholds if speed < limit), "wind_hurricane")


EMOJI_TO_SVG = {
    "☀️": "clear-day",
    "🌙": "clear-night",
    "🌤️": "partly-cloudy-day",
    "⛅": "partly-cloudy-day",
    "🌙☁️": "partly-cloudy-night",
    "☁️": "cloudy",
    "🌁": "fog",
    "🌫️": "fog",
    "🌧️": "rain",
    "🌦️": "drizzle",
    "⛈️": "thunderstorm",
    "🌨️": "snow",
    "❄️": "snow",
    "🌡️": "unknown",
}


def hadise_mgm(kod, is_night=False):
    icon, label, desc = HADISE.get(kod) or ("🌡️", kod or "—", "")
    if is_night:
        icon = icon.replace("☀️", "🌙").replace("🌤️", "🌙☁️").replace("⛅", "☁️")
    return EMOJI_TO_SVG.get(icon, "unknown"), _(label), _(desc)


def hadise_wmo(kod, is_night=False):
    if kod is None:
        return ("unknown", "—", "")
    try:
        icon, label, desc = WMO_HADISE.get(int(kod), ("🌡️", "Bilinmiyor", ""))
    except (ValueError, TypeError):
        icon, label, desc = ("🌡️", str(kod), "")
    if is_night:
        icon = icon.replace("☀️", "🌙").replace("🌤️", "🌙☁️").replace("⛅", "☁️")
    return EMOJI_TO_SVG.get(icon, "unknown"), _(label), _(desc)


# ─── CSS ──────────────────────────────────────────────────────────────────
