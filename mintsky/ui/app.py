#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MintSky — Linux Mint Masaüstü & Görev Çubuğu Uygulaması
MGM resmi API + Open-Meteo yedek/hybrid + Groq AI Hava Danışmanı
Finans Modülü: Truncgil Finance API (Altın, Gümüş, Döviz, Kripto)
Portföy Takibi: Alım fiyatı girişi, kar/zarar hesaplama
Geliştirici : https://github.com/tarihcituranx (Turan Kaya)
Versiyon    : 7.4.0
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
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GLib, Gtk

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
import json
import math
import os
import shutil
import subprocess
import threading
import time
import uuid
import webbrowser
from datetime import datetime

import requests

from mintsky.api.finance import FinanceAPI
from mintsky.api.location import LocationAPI
from mintsky.api.weather import WeatherAPI
from mintsky.constants import (
    ALTIN_EMOJIS,
    ALTIN_KODLAR,
    APP_DIR,
    APP_FILE,
    AUTOSTART_DIR,
    AUTOSTART_FILE,
    BASE_MGM,
    CONFIG_DIR,
    DEFAULT_FINANCE_ALTIN,
    DEFAULT_FINANCE_DOVIZ,
    DEFAULT_FINANCE_KRIPTO,
    DOVIZ_EMOJIS,
    DOVIZ_KODLAR,
    FAV_FILE,
    FINANCE_CACHE_TTL,
    GELISTIRICI,
    GITHUB_REPO,
    GROQ_MODEL,
    GROQ_SYSTEM,
    ICON_DIR,
    METEOALARM_SEVIYE,
    MGM_HEADERS,
    MGM_SIMGELER,
    NOM_HEADERS,
    PILL_TOOLTIPS,
    TIMEOUT,
    TRAY_FETCH_TTL,
    TRAY_ICONS,
    UYGULAMA_ADI,
    VERSIYON,
    WEATHER_CACHE_TTL,
    WMO_TRAY,
)
from mintsky.core.portfolio import load_portfolio as core_load_portfolio
from mintsky.core.portfolio import save_portfolio as core_save_portfolio
from mintsky.core.settings import load_settings as core_load_settings
from mintsky.core.settings import save_settings as core_save_settings
from mintsky.i18n import _
from mintsky.ui.styles import make_css
from mintsky.utils import (
    fmt_date,
    fmt_dt,
    fmt_pct,
    fmt_time,
    fmt_try,
    get_svg_image,
    hadise_mgm,
    hadise_wmo,
    svg_to_emoji,
    val,
    wind_level_key,
    yon,
)


def _safe_icon(icon_name):
    try:
        from gi.repository import Gtk

        theme = Gtk.IconTheme.get_default()
        sym = f"{icon_name}-symbolic"
        if theme.has_icon(sym):
            return sym
        if theme.has_icon(icon_name):
            return icon_name
        if theme.has_icon("weather-few-clouds-symbolic"):
            return "weather-few-clouds-symbolic"
    except Exception as e:
        print(f"[MintSky] Hata: {e}")
    return "dialog-information"

class MintSkyAboutDialog(Gtk.Dialog):
    def __init__(self, parent=None, language="tr"):
        super().__init__(
            title=_("app_about") if _("app_about") != "app_about" else "MintSky Hakkında",
            transient_for=parent,
            modal=True,
            destroy_with_parent=True,
        )
        self.get_style_context().add_class("mintsky-dialog")
        self.set_default_size(500, 530)
        self.set_resizable(False)
        if parent:
            self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)

        # HeaderBar (Modern Cinnamon / GTK Başlığı)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(UYGULAMA_ADI)
        hb.set_subtitle(f"Modern Hava Durumu & Finans • v{VERSIYON}")
        self.set_titlebar(hb)

        content = self.get_content_area()
        content.set_spacing(0)
        content.set_border_width(0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(14)
        main_box.set_margin_bottom(16)

        # 1. Logo
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mintsky.png"
        )
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mintsky.png")
        if os.path.exists(icon_path):
            try:
                from gi.repository import GdkPixbuf

                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    icon_path, 64, 64, True
                )
                img = Gtk.Image.new_from_pixbuf(pixbuf)
            except Exception:
                img = Gtk.Image.new_from_icon_name("weather-clear", Gtk.IconSize.DIALOG)
        else:
            img = Gtk.Image.new_from_icon_name("weather-clear", Gtk.IconSize.DIALOG)
        img.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(img, False, False, 0)

        # 2. Başlık ve Versiyon Rozeti
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_box.set_halign(Gtk.Align.CENTER)

        lbl_title = Gtk.Label(label=UYGULAMA_ADI)
        lbl_title.get_style_context().add_class("about-title")
        title_box.pack_start(lbl_title, False, False, 0)

        lbl_badge = Gtk.Label()
        lbl_badge.set_markup(
            f'<span font_weight="bold" font_size="9000" foreground="#ffffff" background="#0284c7">  v{VERSIYON}  </span>'
        )
        title_box.pack_start(lbl_badge, False, False, 0)
        main_box.pack_start(title_box, False, False, 0)

        lbl_sub = Gtk.Label(
            label="Linux için Modern Açık Kaynaklı Hava Durumu & Finans İstemcisi"
        )
        lbl_sub.set_halign(Gtk.Align.CENTER)
        lbl_sub.get_style_context().add_class("dim-label")
        main_box.pack_start(lbl_sub, False, False, 0)

        # 3. Bilgi Kartı (Geliştirici & Lisans)
        card = Gtk.Frame()
        card.get_style_context().add_class("about-card")
        card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        card_box.set_margin_start(14)
        card_box.set_margin_end(14)
        card_box.set_margin_top(8)
        card_box.set_margin_bottom(8)

        # Geliştirici Satırı
        row_dev = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lbl_dev_k = Gtk.Label(label="Geliştirici:")
        lbl_dev_k.get_style_context().add_class("dim-label")
        row_dev.pack_start(lbl_dev_k, False, False, 0)

        btn_dev = Gtk.LinkButton(
            uri=GELISTIRICI, label="Turan KAYA (@tarihcituranx)"
        )
        row_dev.pack_end(btn_dev, False, False, 0)
        card_box.pack_start(row_dev, False, False, 0)

        card_box.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 1
        )

        # Lisans Satırı
        row_lic = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lbl_lic_k = Gtk.Label(label="Lisans:")
        lbl_lic_k.get_style_context().add_class("dim-label")
        row_lic.pack_start(lbl_lic_k, False, False, 0)

        lbl_lic_v = Gtk.Label(label="MIT Lisansı • Özgür ve Açık Kaynak")
        lbl_lic_v.get_style_context().add_class("about-val")
        row_lic.pack_end(lbl_lic_v, False, False, 0)
        card_box.pack_start(row_lic, False, False, 0)

        card.add(card_box)
        main_box.pack_start(card, False, False, 0)

        # 4. Veri Sağlayıcıları Kartı
        src_frame = Gtk.Frame()
        src_frame.get_style_context().add_class("about-disclaimer")
        src_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        src_box.set_margin_start(12)
        src_box.set_margin_end(12)
        src_box.set_margin_top(8)
        src_box.set_margin_bottom(8)

        lbl_src_h = Gtk.Label(label="🛰️ VERİ VE ENTEGRASYON SERVİSLERİ")
        lbl_src_h.get_style_context().add_class("about-section-header")
        lbl_src_h.set_halign(Gtk.Align.START)
        src_box.pack_start(lbl_src_h, False, False, 0)

        if language == "tr":
            sources_text = (
                "• MGM (Meteoroloji Genel Müdürlüğü): Türkiye resmi anlık gözlemleri ve tahminleri.\n"
                "• Open-Meteo & WMO: Küresel yüksek çözünürlüklü hava modeli ve saatlik tahminler.\n"
                "• MSN Weather: Microsoft Weather Falcon meteoroloji servisi.\n"
                "• Truncgil Finans: Serbest piyasa canlı altın, döviz kurları ve kripto verileri.\n"
                "• Groq Cloud AI: Llama 3 ultra-hızlı yapay zeka hava danışmanı."
            )
        else:
            sources_text = (
                "• Open-Meteo & WMO: Global high-resolution meteorological models.\n"
                "• MSN Weather: Microsoft Weather Falcon service.\n"
                "• Truncgil Finance: Live exchange rates, precious metals and crypto data.\n"
                "• Groq Cloud AI: Llama 3 ultra-fast AI weather consultant."
            )

        lbl_src_body = Gtk.Label()
        lbl_src_body.set_text(sources_text)
        lbl_src_body.set_line_wrap(True)
        lbl_src_body.set_max_width_chars(52)
        lbl_src_body.set_halign(Gtk.Align.START)
        lbl_src_body.get_style_context().add_class("about-src-text")
        src_box.pack_start(lbl_src_body, False, False, 0)

        src_frame.add(src_box)
        main_box.pack_start(src_frame, False, False, 0)

        # 5. Alt Butonlar (Sürüm Notları & Kapat)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_box.set_halign(Gtk.Align.CENTER)

        btn_changes = Gtk.Button(label="📋 Sürüm Notları")
        btn_changes.get_style_context().add_class("btn-tool")
        btn_changes.connect("clicked", lambda _: self.response(Gtk.ResponseType.APPLY))
        btn_box.pack_start(btn_changes, False, False, 0)

        btn_close = Gtk.Button(label="Kapat")
        btn_close.get_style_context().add_class("about-btn")
        btn_close.connect("clicked", lambda _: self.response(Gtk.ResponseType.CLOSE))
        btn_box.pack_start(btn_close, False, False, 0)

        main_box.pack_start(btn_box, False, False, 4)

        content.pack_start(main_box, True, True, 0)
        self.show_all()


class MintSkyApp(Gtk.Window):
    def __init__(self):
        super().__init__(title=_("app_title"))
        self.set_name("main-win")

        self.script_path = os.path.abspath(sys.argv[0])

        # Logo genelde repodaki ana dizindedir (mintsky/mintsky.png yerine ./mintsky.png)
        possible_icon1 = os.path.join(os.path.dirname(self.script_path), "mintsky.png")
        possible_icon2 = os.path.join(
            os.path.dirname(os.path.dirname(self.script_path)), "mintsky.png"
        )
        self.icon_path = (
            possible_icon1 if os.path.exists(possible_icon1) else possible_icon2
        )

        if os.path.exists(self.icon_path):
            self.set_icon_from_file(self.icon_path)
            Gtk.Window.set_default_icon_from_file(self.icon_path)

        self._start_as_widget = "--autostart" in sys.argv
        self._load_settings()
        self._load_portfolio()

        # ── Hava durumu önbelleği ──────────────────────────────────────────
        self._weather_cache = None  # render'a giden 7-tuple
        self._weather_cache_ts = 0.0
        self._weather_cache_key = ""  # "il|ilce"
        self._fetch_in_progress = False  # eş zamanlı fetch engeli
        self._weather_request_id = 0
        self._finance_section = None

        # ── Finans API ─────────────────────────────────────────────────────
        self.finance_api = FinanceAPI()
        self.location_api = LocationAPI()

        # ── Güncelleme ─────────────────────────────────────────────────────
        self._update_info = None

        self._provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self._provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        self._apply_css()
        self._apply_autostart_logic()

        self.set_default_size(
            int(500 * self._get_scale()), int(880 * self._get_scale())
        )
        self.set_resizable(True)
        self.set_border_width(0)

        self._cur_il = ""
        self._cur_ilce = ""
        self._cur_lat = None
        self._cur_lon = None
        self._location_data = {}
        self._last_api_call = 0.0
        self._last_tray_fetch = 0.0
        self._is_compact = False
        self._tray_busy = False
        self._last_bg_hadise = None
        self._last_bg_alarms = []
        self._last_render_data = {}

        self._build_ui()
        self._build_tray()

        self.connect("key-press-event", self._on_key_press)
        self.connect("delete-event", self._on_delete)

        self.il_entry.set_text(self._def_il)
        self.ilce_entry.set_text(self._def_ilce)

        def _loc_cb(sorted_provinces, locs):
            GLib.idle_add(self._apply_turkiye_api, sorted_provinces, locs)

        self.location_api.fetch_locations_bg(callback=_loc_cb)
        threading.Thread(target=self._check_update, daemon=True).start()

        self.show_all()
        if not self._start_as_widget:
            self.maximize()
        GLib.idle_add(self._initial_search)
        self._tray_update_loop()
        GLib.timeout_add_seconds(60, self._tray_update_loop)
        # Finans: her 2 dakikada güncelle
        GLib.timeout_add_seconds(120, self._schedule_finance_refresh)

    @staticmethod
    def _format_wind(speed, direction=""):
        try:
            numeric_speed = float(speed)
            if not (-9998 < numeric_speed < 10000):
                return "—"
        except (TypeError, ValueError):
            return "—"
        level = _(wind_level_key(numeric_speed))
        return f"{numeric_speed:.0f} km/h · {level} {direction}".strip()

    @staticmethod
    def _mgm_alert_matches_city(alert, city):
        title = str(alert.get("baslik", ""))
        if str(alert.get("il", "")).casefold() == city.casefold():
            return True
        if city.casefold() in title.casefold():
            return True
        coastal_regions = {
            "karadeniz": {
                "Artvin", "Rize", "Trabzon", "Giresun", "Ordu", "Samsun",
                "Sinop", "Kastamonu", "Bartın", "Zonguldak", "Düzce", "Sakarya",
            },
            "marmara": {
                "İstanbul", "Tekirdağ", "Edirne", "Kırklareli", "Bursa",
                "Balıkesir", "Çanakkale", "Kocaeli", "Sakarya", "Yalova",
            },
            "kuzey ege": {"Çanakkale", "Balıkesir", "İzmir"},
            "güney ege": {"İzmir", "Aydın", "Muğla"},
            "akdeniz": {"Antalya", "Mersin", "Adana", "Hatay"},
        }
        title_folded = title.casefold()
        return any(
            region in title_folded
            and city.casefold() in {name.casefold() for name in cities}
            for region, cities in coastal_regions.items()
        )

    # ──────────────────── Başlangıç ────────────────────────────────────────
    def _initial_search(self):
        self._search(force=True)
        if self._start_as_widget and not self._is_compact:
            GLib.timeout_add(400, self._toggle_compact)
        return False

    # ──────────────────── Klavye ───────────────────────────────────────────
    def _on_key_press(self, widget, event):
        keyval = event.keyval
        ctrl = bool(event.state & Gdk.ModifierType.CONTROL_MASK)
        if keyval == Gdk.KEY_Escape:
            self.hide()
            return True
        if keyval == Gdk.KEY_F5 or (ctrl and keyval in (Gdk.KEY_r, Gdk.KEY_R)):
            self._manual_refresh()
            return True
        if ctrl and keyval in (Gdk.KEY_f, Gdk.KEY_F):
            self.il_entry.grab_focus()
            return True
        return False

    # ──────────────────── Widget Modu ──────────────────────────────────────
    def _on_compact_button_press(self, widget, event):
        if self._is_compact:
            if event.button == 1:
                self._toggle_compact()
            elif event.button == 3:
                self.begin_move_drag(
                    event.button, int(event.x_root), int(event.y_root), event.time
                )

    def _toggle_compact(self, *args):
        self._is_compact = not self._is_compact
        if self._is_compact:
            self.unmaximize()
            self.hdr.hide()
            self.scroll_win.hide()
            self.set_decorated(False)
            self.set_keep_above(True)
            self.set_skip_taskbar_hint(True)
            self.stick()
            self.set_opacity(0.90)
            GLib.idle_add(self._apply_widget_geometry)
        else:
            self.set_opacity(1.0)
            self.hdr.show()
            self.scroll_win.show()
            self.set_decorated(True)
            self.set_keep_above(False)
            self.set_skip_taskbar_hint(False)
            self.unstick()
            self.resize(int(500 * self._get_scale()), int(880 * self._get_scale()))
        GLib.idle_add(self._render_from_cache)

        # Update CSS ve ilk veri çekimi
        self._apply_css()
        return False

    def _apply_widget_geometry(self):
        self.resize(1, 1)
        GLib.timeout_add(60, self._move_to_corner)
        return False

    # ─── Önbellekten render ────────────────────────────────────────────────
    def _render_from_cache(self):
        """Önbellekte veri varsa API atmadan render et; yoksa force-fetch yap."""
        if self._weather_cache is None:
            self._search(force=True)
        else:
            self._render(*self._weather_cache)
        return False

    def _cache_is_fresh(self, key):
        return (
            self._weather_cache is not None
            and self._weather_cache_key == key
            and time.time() - self._weather_cache_ts < WEATHER_CACHE_TTL
        )

    def _move_to_corner(self):
        screen = self.get_screen()
        monitor = screen.get_monitor_at_window(self.get_window())
        if monitor:
            geom = monitor.get_geometry()
            w, h = self.get_size()
            if w > 450:
                w = 360
            self.move(geom.x + geom.width - w - 20, geom.y + 40)
        return False

    # ──────────────────── Türkiye İl/İlçe API ──────────────────────────────
    def _apply_turkiye_api(self, sorted_provinces, locs):
        self._location_data = locs
        cur_il, cur_ilce = self.il_entry.get_text(), self.ilce_entry.get_text()
        self.il_combo.remove_all()
        for p in sorted_provinces:
            self.il_combo.append_text(p)
        self.il_entry.set_text(cur_il)
        self._on_il_changed(self.il_combo)
        self.ilce_entry.set_text(cur_ilce)

    def _on_il_changed(self, combo):
        il = self.il_entry.get_text().strip()
        cur_ilce = self.ilce_entry.get_text()
        self.ilce_combo.remove_all()
        if il in self._location_data:
            for d in self._location_data[il]:
                self.ilce_combo.append_text(d)
        self.ilce_entry.set_text(cur_ilce)

    # ──────────────────── Ayarlar ──────────────────────────────────────────
    def _load_settings(self):
        d = core_load_settings()
        self._theme = d.get("theme", "dark")
        self._language = d.get("language", "tr")
        self._manual_scale = d.get("scale", 1.2)
        self._autostart = d.get("autostart", False)
        self._def_il = d.get("def_il", "Samsun")
        self._def_ilce = d.get("def_ilce", "Atakum")
        self._notify_enabled = d.get("notify", True)
        self._api_source = d.get("api_source", "mgm")
        self._show_extra = d.get("show_extra", False)
        self._show_saatlik = d.get("show_saatlik", True)
        self._show_gunluk = d.get("show_gunluk", True)
        self._groq_api_key = d.get("groq_api_key", "")
        self._show_finance = d.get("show_finance", False)
        self._fin_altin = d.get("fin_altin", DEFAULT_FINANCE_ALTIN)
        self._fin_altin = ["GUMUS" if x == "GUM" else x for x in self._fin_altin]
        self._fin_doviz = d.get("fin_doviz", DEFAULT_FINANCE_DOVIZ)
        self._fin_kripto = d.get("fin_kripto", DEFAULT_FINANCE_KRIPTO)

    def _save_settings(self):
        success = core_save_settings(
            {
                "theme": self._theme,
                "language": self._language,
                "scale": self._manual_scale,
                "autostart": self._autostart,
                "def_il": self._def_il,
                "def_ilce": self._def_ilce,
                "notify": self._notify_enabled,
                "api_source": self._api_source,
                "show_extra": self._show_extra,
                "show_saatlik": self._show_saatlik,
                "show_gunluk": self._show_gunluk,
                "groq_api_key": self._groq_api_key,
                "show_finance": self._show_finance,
                "fin_altin": self._fin_altin,
                "fin_doviz": self._fin_doviz,
                "fin_kripto": self._fin_kripto,
            }
        )
        if not success and self._groq_api_key:
            self._msg_dialog(
                self,
                "Uyarı",
                "Sistemde güvenli parola deposu (keyring) bulunamadı. API anahtarı kaydedilemedi.",
            )

    # ──────────────────── Portföy ──────────────────────────────────────────
    def _load_portfolio(self):
        self._portfolio = core_load_portfolio()

    def _save_portfolio(self):
        core_save_portfolio(self._portfolio)

    # ──────────────────── Finans API ───────────────────────────────────────
    def _schedule_finance_refresh(self):
        """GLib timer callback — arka planda finans güncelle"""
        if self._show_finance:
            def _cb(success):
                if success:
                    GLib.idle_add(self._refresh_finance_section)
            self.finance_api.fetch_bg(force=False, callback=_cb)
        return True  # devam et

    def _force_finance_refresh(self, btn=None):
        """Kullanıcı 'Yenile' butonuna bastı — önbelleği sıfırla ve çek."""
        if btn:
            btn.set_label("⏳")
            btn.set_sensitive(False)
        self.finance_api.reset_cache()

        def _cb(success):
            if btn:
                GLib.idle_add(
                    lambda: (btn.set_label("🔄 Yenile"), btn.set_sensitive(True))
                    or False
                )
            if success:
                GLib.idle_add(self._refresh_finance_section)

        self.finance_api.fetch_bg(force=True, callback=_cb)

    def _on_finance_fetched(self, success):
        if success:
            GLib.idle_add(self._refresh_finance_section)

    def _refresh_finance_section(self):
        if not self._show_finance or self._is_compact or not hasattr(self, "content"):
            return False
        with self.finance_api._lock:
            rates = dict(self.finance_api._data)
        if rates:
            self._render_finance_main(rates)
            self._finance_section.show_all()
        return False

    # ──────────────────── Portföy hesaplama ────────────────────────────────
    def _calc_portfolio_pnl(self):
        """Toplam portföy değeri ve kar/zarar"""
        from decimal import Decimal, InvalidOperation

        total_cost = Decimal("0.0")
        total_current = Decimal("0.0")
        details = []
        for item in self._portfolio:
            kod = item.get("kod", "")
            try:
                amount = Decimal(str(item.get("amount", 0)))
                buy_price = Decimal(str(item.get("buy_price", 0)))
            except InvalidOperation:
                amount = Decimal("0.0")
                buy_price = Decimal("0.0")

            cur_price_val = self.finance_api.get_rate_price(kod)

            cost = amount * buy_price
            if cur_price_val is not None:
                try:
                    cur_price = Decimal(str(cur_price_val))
                except InvalidOperation:
                    cur_price = Decimal("0.0")
                current = amount * cur_price
                pnl = current - cost
                pnl_pct = (
                    (pnl / cost * Decimal("100"))
                    if cost > Decimal("0")
                    else Decimal("0")
                )
                total_cost += cost
                total_current += current
                details.append(
                    {
                        "kod": kod,
                        "name": item.get("name", kod),
                        "amount": float(amount),
                        "buy_price": float(buy_price),
                        "cur_price": float(cur_price),
                        "cost": float(cost),
                        "current": float(current),
                        "pnl": float(pnl),
                        "pnl_pct": float(pnl_pct),
                    }
                )
            else:
                details.append(
                    {
                        "kod": kod,
                        "name": item.get("name", kod),
                        "amount": float(amount),
                        "buy_price": float(buy_price),
                        "cur_price": None,
                        "cost": float(cost),
                        "current": None,
                        "pnl": None,
                        "pnl_pct": None,
                    }
                )

        from decimal import Decimal

        total_pnl = total_current - total_cost if total_cost > Decimal("0") else None
        total_pnl_pct = (
            (total_pnl / total_cost * Decimal("100"))
            if (total_cost > Decimal("0") and total_pnl is not None)
            else None
        )
        return (
            float(total_cost),
            float(total_current),
            (float(total_pnl) if total_pnl is not None else None),
            (float(total_pnl_pct) if total_pnl_pct is not None else None),
            details,
        )

    # ──────────────────── GitHub Güncelleme Kontrolü ───────────────────────
    def _check_update(self):
        try:
            import re

            import requests

            raw_url = "https://raw.githubusercontent.com/tarihcituranx/mintsky/main/mintsky/constants.py"
            r = requests.get(raw_url, timeout=10)
            if r.status_code == 200:
                match = re.search(r'VERSIYON\s*=\s*["\']([^"\']+)["\']', r.text)
                if match:
                    tag = match.group(1)
                    url = f"{GITHUB_REPO}/releases/latest"
                    if tag and tag != VERSIYON and self._is_newer(tag, VERSIYON):
                        self._update_info = (tag, url)
                        GLib.idle_add(self._show_update_banner)
                        if self._notify_enabled and HAS_NOTIFY:

                            def _show_notif():
                                n = Notify.Notification.new(
                                    "🔄 MintSky Güncellemesi",
                                    f"Yeni sürüm hazır: v{tag}\nGitHub'dan indirip güncelleyebilirsiniz.",
                                    _safe_icon("software-update-available"),
                                )
                                n.set_urgency(1)
                                n.show()
                                return False

                            GLib.idle_add(_show_notif)
        except Exception as e:
            print(f"[MintSky] Hata: {e}")

    def _is_newer(self, remote, local):
        try:

            def v2t(v):
                return tuple(int(x) for x in v.split("."))

            return v2t(remote) > v2t(local)
        except Exception:
            return False

    def _show_update_banner(self):
        """Güncelleme çubuğu (arama satırının altında)"""
        if not self._update_info:
            return False
        tag, url = self._update_info
        if hasattr(self, "_update_bar") and self._update_bar.get_parent():
            return False
        self._update_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._update_bar.get_style_context().add_class("update-row")
        self._update_bar.set_margin_top(4)
        lbl = Gtk.Label()
        lbl.set_markup(
            f"<b>🔄 Yeni sürüm mevcut: v{tag}</b>  "
            f'<a href="{url}">GitHub\'dan indir</a>'
        )
        lbl.set_use_markup(True)
        lbl.get_style_context().add_class("update-txt")
        lbl.set_halign(Gtk.Align.START)
        self._update_bar.pack_start(lbl, True, True, 0)

        btn_update = Gtk.Button(label="📥 Otomatik Güncelle")
        btn_update.connect("clicked", self._do_in_app_update)
        self._sc(btn_update, "btn-tool")
        self._update_bar.pack_start(btn_update, False, False, 0)

        btn_kapat = Gtk.Button(label="✕")
        btn_kapat.connect("clicked", lambda *_: self.hdr.remove(self._update_bar))
        self._sc(btn_kapat, "btn-tool")
        self._update_bar.pack_start(btn_kapat, False, False, 0)
        self.hdr.pack_start(self._update_bar, False, False, 0)
        self.hdr.show_all()
        return False

    def _do_in_app_update(self, btn):
        btn.set_sensitive(False)
        btn.set_label("⏳ " + _("Güncelleniyor..."))

        def _bg():
            import subprocess

            try:
                repo_dir = os.path.dirname(os.path.dirname(self.script_path))
                subprocess.run(
                    ["git", "pull", "origin", "main"],
                    cwd=repo_dir,
                    check=True,
                    capture_output=True,
                )

                GLib.idle_add(
                    self._msg_dialog,
                    self,
                    "Başarılı",
                    "MintSky güncellendi! Uygulama otomatik olarak yeniden başlatılıyor...",
                )
                # 2 saniye bekle ve yeni süreci başlatarak eskisini öldür
                import time

                time.sleep(2)
                subprocess.Popen([sys.executable, self.script_path] + sys.argv[1:])
                sys.exit(0)

            except Exception as e:
                GLib.idle_add(
                    self._msg_dialog,
                    self,
                    "Hata",
                    f"Güncelleme başarısız (Git kurulu olmayabilir veya erişim reddedildi):\n{e}",
                )
                GLib.idle_add(
                    lambda: (btn.set_label("❌ Hata"), btn.set_sensitive(True)) or False
                )

        import threading

        threading.Thread(target=_bg, daemon=True).start()

    # ──────────────────── Autostart / Kurulum ──────────────────────────────
    def _apply_autostart_logic(self):
        try:
            if self._autostart:
                os.makedirs(AUTOSTART_DIR, exist_ok=True)
                with open(AUTOSTART_FILE, "w") as f:
                    f.write(
                        f"[Desktop Entry]\nType=Application\n"
                        f'Exec=python3 "{self.script_path}" --autostart\n'
                        f"Hidden=false\nNoDisplay=false\n"
                        f"X-GNOME-Autostart-enabled=true\n"
                        f"Name={UYGULAMA_ADI}\nIcon=mintsky\n"
                        f"Comment=MintSky Hava Durumu\n"
                    )
            else:
                if os.path.exists(AUTOSTART_FILE):
                    os.remove(AUTOSTART_FILE)
        except Exception as e:
            print("Autostart hatası:", e)

    def _install_as_app(self, *args):
        try:
            if os.path.exists(self.icon_path):
                os.makedirs(ICON_DIR, exist_ok=True)
                shutil.copy2(self.icon_path, os.path.join(ICON_DIR, "mintsky.png"))
            os.makedirs(APP_DIR, exist_ok=True)
            with open(APP_FILE, "w") as f:
                f.write(
                    f"[Desktop Entry]\nVersion=1.0\nType=Application\n"
                    f"Name={UYGULAMA_ADI}\nComment={_('app_comment')}\n"
                    f'Exec=python3 "{self.script_path}"\nIcon=mintsky\n'
                    f"Terminal=false\nCategories=Utility;Weather;\nStartupNotify=true\n"
                )
            subprocess.Popen(
                [
                    "gtk-update-icon-cache",
                    "-f",
                    os.path.expanduser("~/.local/share/icons/hicolor/"),
                ],
                stderr=subprocess.DEVNULL,
            )
            self._status(_("msg_installed"))
        except Exception as e:
            self._status(f"{_('error')}: {e}", True)

    def _get_scale(self):
        return self._manual_scale

    def _apply_css(self):
        self._provider.load_from_data(
            make_css(self._get_scale(), self._theme).encode("utf-8")
        )

    # ──────────────────── UI Yardımcıları ──────────────────────────────────
    def _create_tool_btn(self, icon, text, tooltip, cb, css_class="btn-tool"):
        btn = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_margin_start(4)
        box.set_margin_end(4)
        box.set_margin_top(2)
        box.set_margin_bottom(2)
        if (
            icon.endswith("-symbolic")
            or icon.startswith("system-")
            or icon.startswith("view-")
            or icon.startswith("preferences-")
            or icon.startswith("help-")
            or icon.startswith("go-")
            or icon.startswith("dialog-")
            or icon.startswith("text-")
            or icon.startswith("non-starred-")
            or icon.startswith("starred-")
            or icon.startswith("find-")
        ):
            l1 = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON)
        else:
            l1 = Gtk.Label(label=f"<span size='medium'>{icon}</span>", use_markup=True)

        l2 = Gtk.Label(label=text)
        self._sc(l2, "tool-btn-text")

        box.pack_start(l1, False, False, 0)
        box.pack_start(l2, False, False, 0)
        btn.add(box)
        self._sc(btn, css_class)
        btn.set_tooltip_text(tooltip)
        btn.connect("clicked", cb)
        return btn

    # ──────────────────── Ana UI ───────────────────────────────────────────
    def _build_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(root)

        self.hdr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.hdr.get_style_context().add_class("hdr")

        # ── 1. Satır: Başlık, Versiyon Rozeti, Geliştirici & Üst Araç Butonları ──
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        left_brand = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        left_brand.set_valign(Gtk.Align.CENTER)

        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mintsky.png"
        )
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mintsky.png")
        if os.path.exists(icon_path):
            try:
                from gi.repository import GdkPixbuf

                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 26, 26, True)
                app_logo = Gtk.Image.new_from_pixbuf(pb)
            except Exception:
                app_logo = Gtk.Label(label="🌤️")
        else:
            app_logo = Gtk.Label(label="🌤️")
        left_brand.pack_start(app_logo, False, False, 0)

        title = Gtk.Label(label=UYGULAMA_ADI)
        self._sc(title, "hdr-title")
        title.set_halign(Gtk.Align.START)
        left_brand.pack_start(title, False, False, 0)

        ver_lbl = Gtk.Label()
        ver_lbl.set_markup(f"<span weight='bold'>v{VERSIYON}</span>")
        self._sc(ver_lbl, "badge-version")
        ver_lbl.set_valign(Gtk.Align.CENTER)
        left_brand.pack_start(ver_lbl, False, False, 0)

        dev_lbl = Gtk.Label()
        dev_lbl.set_markup("<span size='small' color='#94a3b8'>• <b>Turan Kaya</b></span>")
        dev_lbl.set_valign(Gtk.Align.CENTER)
        left_brand.pack_start(dev_lbl, False, False, 0)

        title_row.pack_start(left_brand, False, False, 0)
        title_row.pack_start(Gtk.Box(), True, True, 0)  # spacer

        # Sağ araç butonları
        right_tools = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        right_tools.set_valign(Gtk.Align.CENTER)

        btn_widget = self._create_tool_btn(
            "view-restore-symbolic",
            _("btn_widget"),
            _("btn_widget_tt"),
            self._toggle_compact,
        )
        right_tools.pack_start(btn_widget, False, False, 0)

        btn_refresh = self._create_tool_btn(
            "view-refresh-symbolic",
            _("btn_refresh"),
            _("btn_refresh_tt"),
            self._manual_refresh,
        )
        right_tools.pack_start(btn_refresh, False, False, 0)

        if self._language == "tr":
            btn_icons = self._create_tool_btn(
                "dialog-information-symbolic",
                _("btn_icons"),
                _("btn_icons_tt"),
                self._open_mgm_simgeler,
            )
            right_tools.pack_start(btn_icons, False, False, 0)

        self.btn_ai = self._create_tool_btn(
            "🤖",
            _("btn_ai_advisor"),
            _("btn_ai_advisor_tt"),
            self._show_ai_dialog,
            "btn-ai",
        )
        right_tools.pack_start(self.btn_ai, False, False, 0)

        self.btn_fin = self._create_tool_btn(
            "💰",
            _("btn_finance"),
            _("btn_finance_tt"),
            self._show_portfolio_dialog,
            "btn-fin",
        )
        right_tools.pack_start(self.btn_fin, False, False, 0)

        btn_settings = self._create_tool_btn(
            "preferences-system-symbolic",
            _("btn_settings"),
            _("btn_settings_tt"),
            self._show_settings,
        )
        right_tools.pack_start(btn_settings, False, False, 0)

        btn_about = self._create_tool_btn(
            "help-about-symbolic",
            _("app_about") if _("app_about") != "app_about" else "Hakkında",
            "MintSky Hakkında",
            self._show_about,
        )
        right_tools.pack_start(btn_about, False, False, 0)

        title_row.pack_start(right_tools, False, False, 0)
        self.hdr.pack_start(title_row, False, False, 0)

        # ── 2. Satır: Konum Araçları & Şehir Arama (Dengeli Tek Satır) ──
        srow = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        srow.get_style_context().add_class("search-row")

        # Sol grup: Hızlı Konum & Favori İşlemleri
        loc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)

        btn_gps = self._create_tool_btn(
            "system-run-symbolic",
            _("btn_gps"),
            _("btn_gps_tt"),
            lambda *args: self._fetch_location(),
        )
        loc_box.pack_start(btn_gps, False, False, 0)

        btn_pin = self._create_tool_btn(
            "go-home-symbolic",
            _("btn_pin"),
            _("btn_pin_tt"),
            self._make_default,
        )
        loc_box.pack_start(btn_pin, False, False, 0)

        self.btn_fav = self._create_tool_btn(
            "non-starred-symbolic",
            _("btn_fav_add"),
            _("btn_fav_tt"),
            self._toggle_favorite,
        )
        loc_box.pack_start(self.btn_fav, False, False, 0)

        btn_fav_list = self._create_tool_btn(
            "view-list-bullet-symbolic",
            _("btn_list"),
            _("btn_list_tt"),
            self._show_favorites_menu,
        )
        loc_box.pack_start(btn_fav_list, False, False, 0)

        srow.pack_start(loc_box, False, False, 0)

        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        sep.set_margin_start(4)
        sep.set_margin_end(4)
        srow.pack_start(sep, False, False, 0)

        # Sağ grup: Şehir/İlçe Seçimi ve Arama
        self.il_combo = Gtk.ComboBoxText.new_with_entry()
        self.il_entry = self.il_combo.get_child()
        self.il_entry.set_placeholder_text(_("search_city"))
        self.il_entry.connect("activate", lambda *_: self._search(force=True))
        self.il_combo.connect("changed", self._on_il_changed)

        self.ilce_combo = Gtk.ComboBoxText.new_with_entry()
        self.ilce_entry = self.ilce_combo.get_child()
        self.ilce_entry.set_placeholder_text(_("search_district"))
        self.ilce_entry.connect("activate", lambda *_: self._search(force=True))

        btn_ara = Gtk.Button(label=_("btn_search"))
        self._sc(btn_ara, "btn-search")
        btn_ara.connect("clicked", lambda *_: self._search(force=True))

        srow.pack_start(self.il_combo, True, True, 0)
        srow.pack_start(self.ilce_combo, True, True, 0)
        srow.pack_start(btn_ara, False, False, 0)

        self.hdr.pack_start(srow, False, False, 0)
        root.pack_start(self.hdr, False, False, 0)

        self.compact_event_box = Gtk.EventBox()
        self.compact_event_box.connect(
            "button-press-event", self._on_compact_button_press
        )
        self.compact_event_box.set_tooltip_text(
            "Widget Modu\n• SOL TIK: Büyüt\n• SAĞ TIK (Basılı Tut): Sürükle"
        )
        self.compact_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.compact_event_box.add(self.compact_content)
        root.pack_start(self.compact_event_box, False, False, 0)

        self.scroll_win = Gtk.ScrolledWindow()
        self.scroll_win.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scroll_win.add(self.content)
        root.pack_start(self.scroll_win, True, True, 0)

        self._status("İl ve ilçe seçerek veya yazarak arama yapın.")

    def _open_mgm_simgeler(self, *args):
        webbrowser.open(MGM_SIMGELER)

    def _manual_refresh(self, *args):
        now = time.time()
        if now - self._last_api_call < 10:
            self._status(
                f"Lütfen {10-int(now-self._last_api_call)} saniye bekleyin.", error=True
            )
            return
        self._search(force=True)

    def _make_default(self, *args):
        if not self._cur_il:
            return
        self._def_il, self._def_ilce = self._cur_il, self._cur_ilce
        self._save_settings()
        self._tray_update_loop()
        self._status(
            f"Varsayılan konum:\n{self._def_il} / {self._def_ilce}\n\n"
            "Görev çubuğu bu konumu takip edecek."
        )
        GLib.timeout_add(1500, self._render_from_cache)

    # ──────────────────── Ayarlar Diyaloğu (Sekmeli) ──────────────────────
    def _show_settings(self, *args):
        old_api_source = self._api_source

        dlg = Gtk.Dialog(title=f"⚙️ {_('settings_title')}", transient_for=self, flags=0)
        dlg.add_buttons(
            _("settings_cancel"),
            Gtk.ResponseType.CANCEL,
            f"💾 {_('settings_save')}",
            Gtk.ResponseType.OK,
        )
        dlg.set_default_size(680, 400)
        dlg.set_resizable(False)

        root = dlg.get_content_area()
        root.set_spacing(0)
        root.set_margin_top(0)

        # ── Yatay Notebook ──────────────────────────────────────────────────
        nb = Gtk.Notebook()
        nb.set_tab_pos(Gtk.PositionType.TOP)
        nb.set_margin_top(8)
        nb.set_margin_bottom(4)
        nb.set_margin_start(8)
        nb.set_margin_end(8)
        root.pack_start(nb, True, True, 0)

        def _tab(label_text):
            """Sekme içeriği için marjinli dikey kutu + sekme etiketi döndürür."""
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            page.set_margin_top(14)
            page.set_margin_bottom(14)
            page.set_margin_start(16)
            page.set_margin_end(16)
            tab_lbl = Gtk.Label(label=label_text)
            return page, tab_lbl

        def _row(label_text, widget, page):
            """Sağ-sol etiket + widget satırı."""
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            lbl = Gtk.Label(label=label_text)
            lbl.set_halign(Gtk.Align.START)
            lbl.set_xalign(0)
            lbl.set_size_request(160, -1)
            row.pack_start(lbl, False, False, 0)
            row.pack_start(widget, True, True, 0)
            page.pack_start(row, False, False, 0)

        def _sep(page):
            page.pack_start(
                Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
            )

        # ════════════════════════════════════════════════════════════════════
        # SEKME 1 — HAVA DURUMU
        # ════════════════════════════════════════════════════════════════════
        p1, t1 = _tab(f"☁️  {_('settings_tab_weather')}")

        cb_src = Gtk.ComboBoxText()
        if self._language == "tr":
            cb_src.append("mgm", _("src_mgm"))
        cb_src.append("openmeteo", _("src_om"))
        cb_src.append("msn", _("src_msn"))
        active_src = self._api_source
        if self._language != "tr" and active_src == "mgm":
            active_src = "openmeteo"
        cb_src.set_active_id(active_src)
        _row(_("settings_src"), cb_src, p1)
        _sep(p1)

        chk_saat = Gtk.CheckButton.new_with_label(
            f"🕐 {_('settings_hourly')} (48 saat)"
        )
        chk_gun = Gtk.CheckButton.new_with_label(f"📅 {_('settings_daily')}")
        chk_extra = Gtk.CheckButton.new_with_label(
            f"🔬 {_('settings_extra')}  (UV, yağış, kar, çiğ noktası…)"
        )
        chk_saat.set_active(self._show_saatlik)
        chk_gun.set_active(self._show_gunluk)
        chk_extra.set_active(self._show_extra)

        bolum_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        for w in (chk_saat, chk_gun, chk_extra):
            bolum_box.pack_start(w, False, False, 0)
        _row(_("settings_show_sections"), bolum_box, p1)

        nb.append_page(p1, t1)

        # ════════════════════════════════════════════════════════════════════
        # SEKME 2 — FİNANS
        # ════════════════════════════════════════════════════════════════════
        p2, t2 = _tab(f"💰  {_('settings_tab_finance')}")

        chk_fin = Gtk.CheckButton.new_with_label(_("settings_finance_enable"))
        chk_fin.set_active(self._show_finance)
        p2.pack_start(chk_fin, False, False, 0)
        _sep(p2)

        # Altın — yatay 3 sütun grid
        altin_lbl = Gtk.Label()
        altin_lbl.set_markup(f"<b>🥇 {_('settings_gold')}</b>")
        altin_lbl.set_halign(Gtk.Align.START)
        p2.pack_start(altin_lbl, False, False, 0)
        altin_grid = Gtk.Grid()
        altin_grid.set_column_spacing(12)
        altin_grid.set_row_spacing(2)
        altin_chks = {}
        for idx, (kod, ad) in enumerate(ALTIN_KODLAR.items()):
            chk = Gtk.CheckButton.new_with_label(f"{ALTIN_EMOJIS.get(kod,'🪙')} {ad}")
            chk.set_active(kod in self._fin_altin)
            altin_chks[kod] = chk
            altin_grid.attach(chk, idx % 3, idx // 3, 1, 1)
        p2.pack_start(altin_grid, False, False, 0)
        _sep(p2)

        # Döviz — yatay 3 sütun grid
        doviz_lbl = Gtk.Label()
        doviz_lbl.set_markup(f"<b>💵 {_('settings_fx')}</b>")
        doviz_lbl.set_halign(Gtk.Align.START)
        p2.pack_start(doviz_lbl, False, False, 0)
        doviz_grid = Gtk.Grid()
        doviz_grid.set_column_spacing(12)
        doviz_grid.set_row_spacing(2)
        doviz_chks = {}
        for idx, (kod, ad) in enumerate(DOVIZ_KODLAR.items()):
            chk = Gtk.CheckButton.new_with_label(f"{DOVIZ_EMOJIS.get(kod,'🏳')} {ad}")
            chk.set_active(kod in self._fin_doviz)
            doviz_chks[kod] = chk
            doviz_grid.attach(chk, idx % 3, idx // 3, 1, 1)
        p2.pack_start(doviz_grid, False, False, 0)

        nb.append_page(p2, t2)

        # ════════════════════════════════════════════════════════════════════
        # SEKME 3 — AI & GÖRÜNÜM
        # ════════════════════════════════════════════════════════════════════
        p3, t3 = _tab(f"🤖  {_('settings_tab_ai')}")

        groq_note = Gtk.Label()
        groq_note.set_markup(
            _("settings_groq_free") + " "
            "<a href='https://console.groq.com'>console.groq.com</a>"
        )
        groq_note.set_halign(Gtk.Align.START)
        groq_note.set_use_markup(True)
        p3.pack_start(groq_note, False, False, 0)

        key_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        groq_entry = Gtk.Entry()
        groq_entry.set_placeholder_text("gsk_xxxxxxxxxxxxxxxxxxxx")
        groq_entry.set_visibility(False)
        groq_entry.set_text(self._groq_api_key)
        groq_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, "view-conceal-symbolic"
        )
        groq_entry.connect(
            "icon-press", lambda e, *_: e.set_visibility(not e.get_visibility())
        )
        key_box.pack_start(groq_entry, True, True, 0)
        btn_test = Gtk.Button(label=_("settings_groq_test"))
        self._sc(btn_test, "btn-tool")

        def _test_groq(*args):
            k = groq_entry.get_text().strip()
            if not k:
                self._msg_dialog(
                    dlg, "API Anahtarı Eksik", "Groq API anahtarı gerekli."
                )
                return
            btn_test.set_label("…")
            btn_test.set_sensitive(False)

            def _do():
                ok, msg = self._test_groq_key(k)
                GLib.idle_add(
                    lambda: (
                        btn_test.set_label(_("settings_groq_test")),
                        btn_test.set_sensitive(True),
                        self._msg_dialog(dlg, "Groq Test", msg),
                    )
                    or False
                )

            threading.Thread(target=_do, daemon=True).start()

        btn_test.connect("clicked", _test_groq)
        key_box.pack_start(btn_test, False, False, 0)
        _row(_("settings_groq_key"), key_box, p3)
        _sep(p3)

        cb_theme = Gtk.ComboBoxText()
        cb_theme.append("dark", f"🌙 {_('settings_theme_dark')}")
        cb_theme.append("light", f"☀️ {_('settings_theme_light')}")
        cb_theme.set_active_id(self._theme)
        _row(_("settings_theme"), cb_theme, p3)

        adj = Gtk.Adjustment(
            value=self._manual_scale,
            lower=0.5,
            upper=5.0,
            step_increment=0.1,
            page_increment=0.5,
        )
        scale_sl = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale_sl.set_digits(1)
        scale_sl.set_value_pos(Gtk.PositionType.RIGHT)
        for tick in (0.5, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0):
            scale_sl.add_mark(tick, Gtk.PositionType.BOTTOM, None)
        _row(_("settings_scale"), scale_sl, p3)

        nb.append_page(p3, t3)

        # ════════════════════════════════════════════════════════════════════
        # SEKME 4 — SİSTEM
        # ════════════════════════════════════════════════════════════════════
        p4, t4 = _tab(f"⚙️  {_('settings_tab_system')}")

        chk_notify = Gtk.CheckButton.new_with_label(_("settings_notify"))
        chk_auto = Gtk.CheckButton.new_with_label(_("settings_autostart"))
        chk_notify.set_active(self._notify_enabled)
        chk_auto.set_active(self._autostart)
        p4.pack_start(chk_notify, False, False, 0)
        p4.pack_start(chk_auto, False, False, 0)
        _sep(p4)

        cb_lang = Gtk.ComboBoxText()
        cb_lang.append("tr", "🇹🇷 Türkçe")
        cb_lang.append("en", "🇬🇧 English")
        cb_lang.append("de", "🇩🇪 Deutsch (German)")
        cb_lang.append("fr", "🇫🇷 Français (French)")
        cb_lang.append("az", "🇦🇿 Azərbaycan dili (Azerbaijani)")
        cb_lang.append("ar", "🇸🇦 العربية (Arabic)")
        cb_lang.append("fa", "🇮🇷 فارسی (Persian)")
        cb_lang.append("zh", "🇨🇳 中文 (Chinese)")
        cb_lang.set_active_id(self._language)
        _row(_("settings_lang"), cb_lang, p4)
        _sep(p4)

        btn_install = Gtk.Button(label=f"🚀 {_('settings_shortcut')}")
        self._sc(btn_install, "btn-search")
        btn_install.connect("clicked", self._install_as_app)
        btn_install.set_halign(Gtk.Align.START)
        p4.pack_start(btn_install, False, False, 0)

        inst_note = Gtk.Label()
        inst_note.set_markup(
            "<small><i>Uygulama menüsünde 'MintSky' adıyla görünmesini sağlar.\n"
            "İkon dosyası (mintsky.png) ile aynı klasörde çalıştırılmalıdır.</i></small>"
        )
        inst_note.set_halign(Gtk.Align.START)
        inst_note.set_line_wrap(True)
        p4.pack_start(inst_note, False, False, 0)

        nb.append_page(p4, t4)

        # ── Göster ──────────────────────────────────────────────────────────
        dlg.show_all()
        if dlg.run() == Gtk.ResponseType.OK:
            self._api_source = cb_src.get_active_id()
            self._theme = cb_theme.get_active_id()
            self._autostart = chk_auto.get_active()
            self._notify_enabled = chk_notify.get_active()
            self._manual_scale = scale_sl.get_value()
            self._show_extra = chk_extra.get_active()
            self._show_saatlik = chk_saat.get_active()
            self._show_gunluk = chk_gun.get_active()
            self._show_finance = chk_fin.get_active()
            old_lang = self._language
            self._language = cb_lang.get_active_id() or "tr"
            self._groq_api_key = groq_entry.get_text().strip()
            self._fin_altin = [k for k, c in altin_chks.items() if c.get_active()]
            self._fin_doviz = [k for k, c in doviz_chks.items() if c.get_active()]
            self._save_settings()
            self._apply_css()
            if old_lang != self._language:
                dlg.destroy()
                GLib.timeout_add(150, self._restart_for_language_change)
                return
            self._apply_autostart_logic()
            with self.finance_api._lock:
                has_fin = bool(self.finance_api._data)
            if self._show_finance and not has_fin:
                self.finance_api.fetch_bg(callback=self._on_finance_fetched)
            if self._api_source != old_api_source:
                self._weather_cache = None
                GLib.idle_add(lambda: self._search(force=True))
            else:
                GLib.idle_add(self._render_from_cache)
        dlg.destroy()

    def _restart_for_language_change(self):
        """Reload translated interface strings after a language change."""
        try:
            os.execv(
                sys.executable,
                [sys.executable, self.script_path, *sys.argv[1:]],
            )
        except OSError as exc:
            print(f"[MintSky] Dil değişikliğinden sonra yeniden başlatılamadı: {exc}")
        return False

    # ──────────────────── Portföy Yönetim Diyaloğu ─────────────────────────
    def _show_portfolio_dialog(self, *args):
        """Portföy yönetimi: ekle/sil/görüntüle"""
        if self._show_finance:
            # Finans verisi yoksa önce çek
            if not self.finance_api._data:
                self.finance_api.fetch_bg()

        dlg = Gtk.Dialog(
            title="💰 Finans & Portföy Yönetimi", transient_for=self, flags=0
        )
        dlg.add_button("Kapat", Gtk.ResponseType.CLOSE)
        dlg.set_default_size(580, 520)
        box = dlg.get_content_area()
        box.set_spacing(8)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(14)
        box.set_margin_end(14)

        # Finans modülü uyarısı
        if not self._show_finance:
            note = Gtk.Label()
            note.set_markup(
                "⚠️ <b>Finans modülü kapalı.</b> Ayarlar'dan 'Finans Modülü'nü aktif edin."
            )
            note.set_halign(Gtk.Align.START)
            note.set_use_markup(True)
            box.pack_start(note, False, False, 0)

        # ── Portföy özeti ──
        self._lbl_section(box, "📊 PORTFÖY ÖZETİ")

        pnl_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        pnl_box.get_style_context().add_class("fin-card")

        def _refresh_pnl():
            for w in pnl_box.get_children():
                pnl_box.remove(w)
            tc, cur, pnl, pnl_pct, details = self._calc_portfolio_pnl()
            if not details:
                e = Gtk.Label(
                    label="Henüz portföy kalemi yok.\nAşağıdan ekleyebilirsiniz."
                )
                e.set_halign(Gtk.Align.CENTER)
                pnl_box.pack_start(e, False, False, 8)
            else:
                for d in details:
                    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                    row.get_style_context().add_class("fin-row")
                    name_lbl = Gtk.Label(label=f"{d['name']} × {d['amount']:.4g}")
                    name_lbl.get_style_context().add_class("fin-name")
                    name_lbl.set_halign(Gtk.Align.START)
                    row.pack_start(name_lbl, True, True, 0)
                    if d["cur_price"] is not None:
                        cur_lbl = Gtk.Label(label=fmt_try(d["current"]))
                        cur_lbl.get_style_context().add_class("fin-price")
                        row.pack_start(cur_lbl, False, False, 0)
                        sign = "+" if d["pnl"] >= 0 else ""
                        cls = "fin-change-pos" if d["pnl"] >= 0 else "fin-change-neg"
                        p_lbl = Gtk.Label(
                            label=f"{sign}{fmt_try(d['pnl'])} ({fmt_pct(d['pnl_pct'])})"
                        )
                        p_lbl.get_style_context().add_class(cls)
                        row.pack_start(p_lbl, False, False, 0)
                    else:
                        na = Gtk.Label(label="Fiyat bekleniyor…")
                        na.get_style_context().add_class("fin-change-neu")
                        row.pack_start(na, False, False, 0)
                    pnl_box.pack_start(row, False, False, 0)

                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                pnl_box.pack_start(sep, False, False, 4)
                tot_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                tot_lbl = Gtk.Label(label="TOPLAM")
                tot_lbl.get_style_context().add_class("fin-title")
                tot_row.pack_start(tot_lbl, True, True, 0)
                if pnl is not None:
                    tv_lbl = Gtk.Label(label=fmt_try(cur))
                    tv_lbl.get_style_context().add_class("fin-price")
                    tot_row.pack_start(tv_lbl, False, False, 0)
                    sign = "+" if pnl >= 0 else ""
                    cls = "profit-lbl" if pnl >= 0 else "loss-lbl"
                    tp_lbl = Gtk.Label(
                        label=f"{sign}{fmt_try(pnl)} ({fmt_pct(pnl_pct)})"
                    )
                    tp_lbl.get_style_context().add_class(cls)
                    tot_row.pack_start(tp_lbl, False, False, 0)
                pnl_box.pack_start(tot_row, False, False, 0)
            pnl_box.show_all()

        _refresh_pnl()
        box.pack_start(pnl_box, False, False, 0)

        # ── Kale listesi ──
        self._lbl_section(box, "📋 PORTFÖY KALEMLERİ")

        scroll_p = Gtk.ScrolledWindow()
        scroll_p.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll_p.set_min_content_height(140)
        port_list_box = Gtk.ListBox()
        port_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll_p.add(port_list_box)
        box.pack_start(scroll_p, True, True, 0)

        def _rebuild_list():
            for row in port_list_box.get_children():
                port_list_box.remove(row)
            for i, item in enumerate(self._portfolio):
                row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
                row_box.set_margin_top(4)
                row_box.set_margin_bottom(4)
                row_box.set_margin_start(8)
                row_box.set_margin_end(8)
                info = Gtk.Label()
                info.set_markup(
                    f"<b>{item.get('name',item['kod'])}</b>  "
                    f"× {item['amount']:.4g}  "
                    f"@ <i>{fmt_try(item['buy_price'])}</i>  "
                    f"<span color='#5a6a85'>{item.get('buy_date','')}</span>"
                )
                info.set_halign(Gtk.Align.START)
                info.set_use_markup(True)
                row_box.pack_start(info, True, True, 0)
                cur_p = self.finance_api.get_rate_price(item["kod"])
                if cur_p is not None:
                    pnl_v = (cur_p - float(item["buy_price"])) * float(item["amount"])
                    sign = "+" if pnl_v >= 0 else ""
                    color = "#3fb950" if pnl_v >= 0 else "#f85149"
                    pl_lbl = Gtk.Label()
                    pl_lbl.set_markup(
                        f"<span color='{color}'><b>{sign}{fmt_try(pnl_v)}</b></span>"
                    )
                    pl_lbl.set_use_markup(True)
                    row_box.pack_start(pl_lbl, False, False, 0)
                del_btn = Gtk.Button(label="🗑")
                self._sc(del_btn, "btn-tool")
                del_btn.set_tooltip_text("Bu kalemi sil")
                idx_capture = i

                def _del(_, idx=idx_capture):
                    self._portfolio.pop(idx)
                    self._save_portfolio()
                    _rebuild_list()
                    _refresh_pnl()

                del_btn.connect("clicked", _del)
                row_box.pack_start(del_btn, False, False, 0)
                port_list_box.add(row_box)
            port_list_box.show_all()

        _rebuild_list()

        # ── Yeni kalem ekle ──
        self._lbl_section(box, "➕ YENİ KALEM EKLE")

        add_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        # Tür seçimi
        cb_type = Gtk.ComboBoxText()
        all_codes = [(k, f"🪙 {v}") for k, v in ALTIN_KODLAR.items()] + [
            (k, f"{DOVIZ_EMOJIS.get(k,'🏳')} {v}") for k, v in DOVIZ_KODLAR.items()
        ]
        for kod, ad in all_codes:
            cb_type.append(kod, ad)
        cb_type.set_active(0)
        add_box.pack_start(cb_type, True, True, 0)

        # Miktar
        entry_amt = Gtk.Entry()
        entry_amt.set_placeholder_text("Miktar (ör: 10.5)")
        entry_amt.set_max_width_chars(10)
        add_box.pack_start(entry_amt, False, False, 0)

        # Alım fiyatı
        entry_price = Gtk.Entry()
        entry_price.set_placeholder_text("Alım fiyatı (₺)")
        entry_price.set_max_width_chars(12)

        # Alım fiyatını otomatik doldur
        def _on_type_changed(_):
            kod = cb_type.get_active_id()
            if not kod:
                return
            cur_p = self.finance_api.get_rate_price(kod)
            if cur_p is not None:
                entry_price.set_text(f"{cur_p:.2f}")

        cb_type.connect("changed", _on_type_changed)
        _on_type_changed(None)
        add_box.pack_start(entry_price, False, False, 0)

        # Tarih
        entry_date = Gtk.Entry()
        entry_date.set_text(datetime.now().strftime("%Y-%m-%d"))
        entry_date.set_max_width_chars(11)
        add_box.pack_start(entry_date, False, False, 0)

        btn_add = Gtk.Button(label="Ekle")
        self._sc(btn_add, "btn-search")

        def _add_item(*args):
            kod = cb_type.get_active_id()
            try:
                amt = float(entry_amt.get_text().replace(",", "."))
            except ValueError:
                self._msg_dialog(dlg, "Hata", "Geçersiz miktar.")
                return
            try:
                bp = float(entry_price.get_text().replace(",", "."))
            except ValueError:
                self._msg_dialog(dlg, "Hata", "Geçersiz alım fiyatı.")
                return
            # İsim bul
            all_names = {**ALTIN_KODLAR, **DOVIZ_KODLAR}
            name = all_names.get(kod, kod)
            self._portfolio.append(
                {
                    "id": str(uuid.uuid4())[:8],
                    "kod": kod,
                    "name": name,
                    "amount": amt,
                    "buy_price": bp,
                    "buy_date": entry_date.get_text().strip(),
                }
            )
            self._save_portfolio()
            entry_amt.set_text("")
            _rebuild_list()
            _refresh_pnl()

        btn_add.connect("clicked", _add_item)
        add_box.pack_start(btn_add, False, False, 0)
        box.pack_start(add_box, False, False, 0)

        # Yardım notu
        hint = Gtk.Label()
        hint.set_markup(
            "<small><i>💡 Alım fiyatı alanı seçilen ürünün güncel fiyatı ile otomatik dolar. "
            "Geçmiş alımlar için el ile girin.</i></small>"
        )
        hint.set_halign(Gtk.Align.START)
        hint.set_use_markup(True)
        hint.set_line_wrap(True)
        box.pack_start(hint, False, False, 0)

        box.show_all()
        dlg.connect("response", lambda d, r: d.destroy())
        dlg.show_all()

    def _lbl_section(self, box, text):
        lbl = Gtk.Label()
        lbl.set_markup(f"<b>{text}</b>")
        lbl.set_halign(Gtk.Align.START)
        box.pack_start(lbl, False, False, 0)

    def _msg_dialog(self, parent, title, msg):
        d = Gtk.MessageDialog(
            transient_for=parent,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        d.format_secondary_text(msg)
        d.connect("response", lambda dialog, response: dialog.destroy())
        d.show_all()

    # ──────────────────── Sürüm Notları ────────────────────────────────────
    def _show_changelog(self, *args):
        dlg = Gtk.Dialog(
            title=f"MintSky v{VERSIYON} — Sürüm Notları",
            transient_for=self,
            modal=True,
            destroy_with_parent=True,
        )
        dlg.get_style_context().add_class("mintsky-dialog")
        dlg.set_default_size(520, 500)
        dlg.set_resizable(False)
        if self:
            dlg.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        else:
            dlg.set_position(Gtk.WindowPosition.CENTER)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(f"MintSky v{VERSIYON}")
        hb.set_subtitle("Yenilikler & Geliştirmeler")
        dlg.set_titlebar(hb)

        content = dlg.get_content_area()
        content.set_spacing(0)
        content.set_border_width(0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(14)
        main_box.set_margin_bottom(16)

        card = Gtk.Frame()
        card.get_style_context().add_class("about-card")
        c_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        c_box.set_margin_start(14)
        c_box.set_margin_end(14)
        c_box.set_margin_top(10)
        c_box.set_margin_bottom(10)

        h_lbl = Gtk.Label(label=f"🚀 v{VERSIYON} İyileştirmeleri")
        h_lbl.get_style_context().add_class("about-changelog-header")
        h_lbl.set_halign(Gtk.Align.START)
        c_box.pack_start(h_lbl, False, False, 0)

        b_lbl = Gtk.Label()
        b_lbl.get_style_context().add_class("about-changelog-text")
        b_lbl.set_markup(
            "• 🎨 <b>Modern Arayüz &amp; Toolbar:</b> Butonlar yatay ve orantılı hale getirildi, boşluklar giderildi.\n"
            "• ℹ️ <b>Yeni Modern Hakkında Diyaloğu:</b> Kart tabanlı tasarım ve detaylı servis açıklamaları.\n"
            "• 🕒 <b>Gelişmiş Sistem Tepsisi (Tray):</b> Canlı ölçüm saatleri, anlık hava durumu ve hissedilen sıcaklık hover desteği.\n"
            "• 🌍 <b>Çoklu Dil &amp; MGM İzolasyonu:</b> MGM öğeleri yalnızca Türkçe dilinde gösterilecek şekilde optimize edildi.\n"
            "• 🌬️ <b>Doğru Hava Terimleri:</b> Nem, görüş mesafesi, rüzgar hamlesi ve çiğ noktası çevirileri düzeltildi."
        )
        b_lbl.set_line_wrap(True)
        b_lbl.set_max_width_chars(52)
        b_lbl.set_halign(Gtk.Align.START)
        c_box.pack_start(b_lbl, False, False, 0)
        card.add(c_box)
        main_box.pack_start(card, False, False, 0)

        card_past = Gtk.Frame()
        card_past.get_style_context().add_class("about-disclaimer")
        p_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        p_box.set_margin_start(14)
        p_box.set_margin_end(14)
        p_box.set_margin_top(8)
        p_box.set_margin_bottom(8)

        ph_lbl = Gtk.Label(label="📦 Geçmiş Sürümler")
        ph_lbl.get_style_context().add_class("about-section-header")
        ph_lbl.set_halign(Gtk.Align.START)
        p_box.pack_start(ph_lbl, False, False, 0)

        pt_lbl = Gtk.Label()
        pt_lbl.set_markup(
            "<small><b>v5.0 - v7.0:</b> Modüler altyapı, Concurrent Fetch, Tema Motoru, Portföy Takibi.\n"
            "<b>v3.x - v4.x:</b> Temel API yapısı, Widget modu, MGM optimizasyonu.</small>"
        )
        pt_lbl.set_line_wrap(True)
        pt_lbl.set_max_width_chars(52)
        pt_lbl.set_halign(Gtk.Align.START)
        p_box.pack_start(pt_lbl, False, False, 0)
        card_past.add(p_box)
        main_box.pack_start(card_past, False, False, 0)

        btn_close = Gtk.Button(label="Kapat")
        btn_close.get_style_context().add_class("about-btn")
        btn_close.set_halign(Gtk.Align.CENTER)
        btn_close.connect("clicked", lambda _: dlg.response(Gtk.ResponseType.CLOSE))
        main_box.pack_start(btn_close, False, False, 4)

        content.pack_start(main_box, True, True, 0)

        dlg.show_all()
        dlg.run()
        dlg.destroy()

    def _show_about(self, *args):
        dlg = MintSkyAboutDialog(parent=self, language=self._language)
        res = dlg.run()
        dlg.destroy()
        if res == Gtk.ResponseType.APPLY:
            self._show_changelog()

    def _check_for_updates_bg(self, forced=False):
        def _check():
            try:
                import re

                import requests

                raw_url = "https://raw.githubusercontent.com/tarihcituranx/mintsky/main/mintsky/constants.py"
                r = requests.get(raw_url, timeout=5)
                if r.status_code == 200:
                    match = re.search(r'VERSIYON\s*=\s*["\']([^"\']+)["\']', r.text)
                    if match:
                        latest = match.group(1)
                        if latest > VERSIYON:
                            download_url = f"{GITHUB_REPO}/releases/latest"
                            GLib.idle_add(self._ask_update, latest, download_url)
                        elif forced:
                            GLib.idle_add(self._notify_no_update)
                    elif forced:
                        GLib.idle_add(self._notify_no_update)
                elif forced:
                    GLib.idle_add(self._notify_update_error, f"HTTP {r.status_code}")
            except Exception as e:
                if forced:
                    GLib.idle_add(self._notify_update_error, str(e))

        threading.Thread(target=_check, daemon=True).start()

    def _notify_no_update(self):
        dlg = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=_("Uygulama Güncel"),
        )
        dlg.format_secondary_text(
            _("MintSky'ın en güncel versiyonunu (v{VERSIYON}) kullanıyorsunuz.").format(
                VERSIYON=VERSIYON
            )
        )
        dlg.connect("response", lambda d, r: d.destroy())
        dlg.show_all()

    def _notify_update_error(self, err):
        dlg = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=_("Güncelleme Kontrolü Başarısız"),
        )
        dlg.format_secondary_text(_("Bağlantı hatası: {err}").format(err=err))
        dlg.connect("response", lambda d, r: d.destroy())
        dlg.show_all()

    def _ask_update(self, latest, url):
        dlg = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("Yeni Sürüm Mevcut: {latest}").format(latest=latest),
        )
        dlg.format_secondary_text(
            _(
                "MintSky'ın yeni bir versiyonu ({latest}) var. İndirme sayfasına gitmek ister misiniz?\n\nİndirme bağlatısından Linux için derlenmiş hazır 'MintSky-Linux-x86_64.tar.gz' paketini indirebilirsiniz."
            ).format(latest=latest)
        )

        def _on_res(d, res):
            if res == Gtk.ResponseType.YES:
                import webbrowser

                webbrowser.open(url)
            d.destroy()

        dlg.connect("response", _on_res)
        dlg.show_all()

    # ──────────────────── Groq AI ──────────────────────────────────────────
    def _test_groq_key(self, key):
        try:
            from groq import Groq

            client = Groq(api_key=key, timeout=10)
            _dummy = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": "Merhaba, çalışıyor musun?"}],
                max_tokens=20,
            )
            return True, "✅ Bağlantı başarılı! API anahtarı geçerli."
        except Exception as e:
            err_msg = str(e)
            if "AuthenticationError" in err_msg or "401" in err_msg:
                return False, "❌ Geçersiz API anahtarı. Lütfen kontrol edin."
            return False, f"❌ Bağlantı hatası: {err_msg[:80]}"

    def _build_weather_context(self, custom_q=""):
        d = self._last_render_data
        if not d:
            return ""
        now_str = datetime.now().strftime("%d %B %Y, %H:%M")
        lines = [
            f"Konum: {d.get('sehir', '?')}",
            f"Tarih/Saat: {now_str}",
            f"Hava Durumu: {d.get('kisa', '?')}",
            f"Sıcaklık: {d.get('sicak_str', '?')}",
        ]
        if d.get("his_str"):
            lines.append(f"Hissedilen: {d['his_str']}")
        if d.get("nem"):
            lines.append(f"Nem: %{d['nem']:.0f}")
        if d.get("ruzgar"):
            lines.append(f"Rüzgar: {d['ruzgar']}")
        if d.get("basinc"):
            lines.append(f"Basınç: {d['basinc']:.0f} hPa")
        if d.get("gorus"):
            g = d["gorus"]
            lines.append(
                f"Görüş: {g/1000:.1f} km" if g >= 1000 else f"Görüş: {g:.0f} m"
            )
        if d.get("uv") is not None:
            lines.append(f"UV İndeksi: {d['uv']:.1f}")
        if d.get("yagis_olas") is not None:
            lines.append(f"Yağış Olasılığı: %{d['yagis_olas']:.0f}")
        if d.get("gustu") is not None:
            lines.append(f"Rüzgar Gustu: {self._format_wind(d['gustu'])}")
        if d.get("uyarilar"):
            lines.append("Aktif Uyarılar: " + ", ".join(d["uyarilar"]))
        if d.get("tahmin_3s"):
            lines.append("Önümüzdeki 3 Saat:")
            for t_str, em, tmp in d["tahmin_3s"]:
                lines.append(f"  {t_str} — {em} {tmp}")
        context = "\n".join(lines)
        context += f"\n\n{'Kullanıcı Sorusu: ' + custom_q if custom_q else 'Lütfen bu hava koşullarına göre pratik tavsiyeler ver.'}"
        return context

    def _call_groq(self, context):
        from groq import Groq

        try:
            client = Groq(api_key=self._groq_api_key, timeout=20)
            r = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": GROQ_SYSTEM},
                    {"role": "user", "content": context},
                ],
                max_tokens=600,
                temperature=0.25,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            err_msg = str(e)
            if "AuthenticationError" in err_msg or "401" in err_msg:
                raise PermissionError("Geçersiz Groq API anahtarı.")
            raise RuntimeError(f"Groq API hatası: {err_msg[:120]}")

    def _show_ai_dialog(self, *args):
        if not self._groq_api_key:
            self._msg_dialog(
                self,
                "API Anahtarı Yok",
                "Groq API anahtarını Ayarlar → Groq AI bölümünden ekleyin.\n"
                "Ücretsiz anahtar: https://console.groq.com",
            )
            return
        if not self._last_render_data:
            self._msg_dialog(
                self,
                "Veri Yok",
                "Önce bir konum arayın; AI veriyi okuyarak tavsiye üretir.",
            )
            return

        dlg = Gtk.Dialog(title="🤖 Groq AI Hava Danışmanı", transient_for=self, flags=0)
        dlg.set_name("main-win")
        dlg.add_button("Kapat", Gtk.ResponseType.CLOSE)
        dlg.set_default_size(500, 480)
        box = dlg.get_content_area()
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(14)
        box.set_margin_bottom(14)
        box.set_spacing(8)

        sehir_lbl = Gtk.Label(label=f"📍 {self._last_render_data.get('sehir','')}")
        self._sc(sehir_lbl, "ai-lbl")
        sehir_lbl.set_halign(Gtk.Align.START)
        box.pack_start(sehir_lbl, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        self._ai_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scroll.add(self._ai_box)
        box.pack_start(scroll, True, True, 0)
        box.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
        )

        q_lbl = Gtk.Label(label=_("ai_custom_question"))
        self._sc(q_lbl, "ai-lbl")
        q_lbl.set_halign(Gtk.Align.START)
        box.pack_start(q_lbl, False, False, 0)
        q_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        q_entry = Gtk.Entry()
        q_entry.set_placeholder_text("...")
        q_row.pack_start(q_entry, True, True, 0)
        btn_sor = Gtk.Button(label=_("ai_btn_ask"))
        self._sc(btn_sor, "btn-search")
        q_row.pack_start(btn_sor, False, False, 0)

        btn_dinle = Gtk.Button(label=f"🔊 {_('ai_btn_listen')}")
        self._sc(btn_dinle, "btn-suggest")
        q_row.pack_start(btn_dinle, False, False, 0)
        btn_dinle.set_sensitive(False)

        box.pack_start(q_row, False, False, 0)
        box.show_all()

        def _play_audio(*args):
            if not hasattr(self, "_last_ai_text"):
                return
            btn_dinle.set_sensitive(False)

            def _tts_thread():
                try:
                    import os
                    import shutil
                    import subprocess
                    import tempfile

                    voices = {
                        "tr": "tr-TR-EmelNeural",
                        "en": "en-US-ChristopherNeural",
                        "de": "de-DE-KillianNeural",
                        "fr": "fr-FR-HenriNeural",
                        "ar": "ar-SA-HamedNeural",
                        "fa": "fa-IR-FaridNeural",
                        "zh": "zh-CN-YunxiNeural",
                        "az": "az-AZ-BabekNeural",
                    }
                    v = voices.get(self._language, "en-US-ChristopherNeural")

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                        tmp_path = f.name

                    edge_bin = shutil.which("edge-tts") or os.path.expanduser(
                        "~/.local/bin/edge-tts"
                    )
                    subprocess.run(
                        [
                            edge_bin,
                            "--text",
                            self._last_ai_text,
                            "--voice",
                            v,
                            "--write-media",
                            tmp_path,
                        ],
                        check=True,
                    )

                    # Sesi Çal
                    try:
                        if os.system("command -v paplay >/dev/null 2>&1") == 0:
                            subprocess.run(["paplay", tmp_path], check=True, timeout=60)
                        else:
                            subprocess.run(["aplay", tmp_path], check=True, timeout=60)
                    finally:
                        # Temizlik
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
                except Exception as e:
                    print("TTS Hatası:", e)
                finally:
                    GLib.idle_add(lambda: btn_dinle.set_sensitive(True) or False)

            threading.Thread(target=_tts_thread, daemon=True).start()

        btn_dinle.connect("clicked", _play_audio)
        box.show_all()

        def _run_ai(custom_q=""):
            btn_sor.set_sensitive(False)
            btn_dinle.set_sensitive(False)
            for child in self._ai_box.get_children():
                self._ai_box.remove(child)
            loading_lbl = Gtk.Label(label=_("ai_loading"))
            self._sc(loading_lbl, "ai-lbl")
            loading_lbl.set_halign(Gtk.Align.START)
            self._ai_box.pack_start(loading_lbl, False, False, 0)
            self._ai_box.show_all()

            context = self._build_weather_context(custom_q)

            def _do():
                err = None
                try:
                    result_raw = self._call_groq(context)
                    try:
                        import json

                        result_dict = json.loads(result_raw)
                    except:
                        result_dict = {"Yanıt": result_raw}
                except Exception as e:
                    err = f"❌ Hata: {e}"

                def _update_ui():
                    for child in self._ai_box.get_children():
                        self._ai_box.remove(child)
                    if err:
                        lbl = Gtk.Label(label=err)
                        self._sc(lbl, "err-lbl")
                        lbl.set_halign(Gtk.Align.START)
                        lbl.set_line_wrap(True)
                        self._ai_box.pack_start(lbl, False, False, 0)
                    else:
                        icons = {
                            "Giyim": "👕",
                            "Aktivite": "🏃",
                            "Sağlık": "⚕️",
                            "Yol": "🚗",
                            "Yanıt": "💬",
                        }
                        reading_text = "Hava durumu tavsiyeleri şu şekilde: "
                        for k, v in result_dict.items():
                            reading_text += f"{k} için, {v} "
                            frame = Gtk.Frame()
                            frame.set_shadow_type(Gtk.ShadowType.IN)
                            vbox = Gtk.Box(
                                orientation=Gtk.Orientation.VERTICAL, spacing=4
                            )
                            vbox.set_margin_start(8)
                            vbox.set_margin_end(8)
                            vbox.set_margin_top(8)
                            vbox.set_margin_bottom(8)

                            icon = icons.get(k, "📌")
                            title_lbl = Gtk.Label()
                            title_lbl.set_markup(f"<b>{icon} {k}</b>")
                            self._sc(title_lbl, "ai-lbl")
                            title_lbl.set_halign(Gtk.Align.START)

                            val_lbl = Gtk.Label(label=str(v))
                            self._sc(val_lbl, "ai-val")
                            val_lbl.set_halign(Gtk.Align.START)
                            val_lbl.set_line_wrap(True)
                            val_lbl.set_selectable(True)

                            vbox.pack_start(title_lbl, False, False, 0)
                            vbox.pack_start(val_lbl, False, False, 0)
                            frame.add(vbox)
                            self._ai_box.pack_start(frame, False, False, 0)
                    self._ai_box.show_all()
                    btn_sor.set_sensitive(True)
                    if not err:
                        self._last_ai_text = reading_text
                        btn_dinle.set_sensitive(True)
                    return False

                GLib.idle_add(_update_ui)

            threading.Thread(target=_do, daemon=True).start()

        btn_sor.connect("clicked", lambda *_: _run_ai(q_entry.get_text().strip()))
        q_entry.connect("activate", lambda *_: _run_ai(q_entry.get_text().strip()))
        threading.Thread(target=lambda: _run_ai(""), daemon=True).start()
        dlg.run()
        dlg.destroy()

    # ──────────────────── Tray ─────────────────────────────────────────────
    def _build_tray(self):
        self._weather_icon_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "weather"
        )
        Gtk.IconTheme.get_default().append_search_path(self._weather_icon_dir)
        if HAS_INDICATOR:
            self._indicator = AppIndicator3.Indicator.new(
                "MintSky",
                _safe_icon("weather-clear"),
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
            self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self._indicator.set_menu(self._build_tray_menu())
        else:
            self._tray = Gtk.StatusIcon()
            self._tray.set_from_icon_name(_safe_icon("weather-clear"))
            self._tray.connect("activate", self._tray_toggle)
            self._tray.connect("popup-menu", self._tray_popup)

    def _build_tray_menu(self):
        menu = Gtk.Menu()

        # ── 1. Mevcut Tanımlı / Aktif Konum & Anlık Hava Durumu Başlığı ──
        cur_city = getattr(self, "_tray_sehir", None)
        if not cur_city:
            cur_city = f"{self._def_il} / {self._def_ilce}" if self._def_ilce else self._def_il

        is_def = (
            getattr(self, "_cur_il", "") == self._def_il
            and (not self._def_ilce or getattr(self, "_cur_ilce", "") == self._def_ilce)
        )
        tag_str = " (Tanımlı Konum)" if is_def else ""

        m_city = Gtk.MenuItem.new_with_label(f"📍 {cur_city}{tag_str}")
        m_city.connect("activate", self._tray_toggle)
        menu.append(m_city)

        temp_str = getattr(self, "_tray_temp", None)
        desc_str = getattr(self, "_tray_desc", None)
        emoji_str = svg_to_emoji(getattr(self, "_tray_emoji", "🌤️"))
        if temp_str and temp_str not in ("-", "--", None):
            cond_label = f"{emoji_str} {temp_str}°C"
            if desc_str and desc_str not in ("-", "--", None):
                cond_label += f" · {desc_str}"
            m_cond = Gtk.MenuItem.new_with_label(cond_label)
            m_cond.connect("activate", self._tray_toggle)
            menu.append(m_cond)

        # Detaylar: Hissedilen, Nem, Rüzgar
        details = []
        his_str = getattr(self, "_tray_hissedilen", None)
        if his_str and his_str not in ("-", "--", None):
            details.append(f"🌡️ Hissedilen: {his_str}°")
        nem_str = getattr(self, "_tray_nem", None)
        if nem_str and nem_str not in ("-", "--", None):
            details.append(f"💧 %{nem_str}")
        ruzgar_str = getattr(self, "_tray_ruzgar", None)
        if ruzgar_str and ruzgar_str not in ("-", "--", None):
            details.append(f"🌬️ {ruzgar_str}")

        if details:
            m_det = Gtk.MenuItem.new_with_label("   ".join(details))
            m_det.set_sensitive(False)
            menu.append(m_det)

        # Ekstra hava parametreleri (Basınç, UV, Yağış Olasılığı)
        if getattr(self, "_last_render_data", None):
            extra = []
            if self._last_render_data.get("basinc"):
                extra.append(f"⏱️ {self._last_render_data['basinc']:.0f} hPa")
            if self._last_render_data.get("uv") is not None:
                extra.append(f"☀️ UV {self._last_render_data['uv']:.1f}")
            if self._last_render_data.get("yagis_olas") is not None and self._last_render_data["yagis_olas"] > 0:
                extra.append(f"🌧️ %{self._last_render_data['yagis_olas']:.0f} Yağış")
            if extra:
                m_extra = Gtk.MenuItem.new_with_label("   ".join(extra))
                m_extra.set_sensitive(False)
                menu.append(m_extra)

        # MGM Aktif Uyarılar (Varsa ve Türkçe ise):
        if getattr(self, "_last_render_data", None) and self._language == "tr":
            uyarilar = self._last_render_data.get("uyarilar", [])
            if uyarilar:
                menu.append(Gtk.SeparatorMenuItem())
                for u in uyarilar[:2]:
                    u_title = u.get("baslik", "Meteorolojik Uyarı")
                    m_warn = Gtk.MenuItem.new_with_label(f"⚠️ {u_title}")
                    m_warn.connect("activate", self._tray_toggle)
                    menu.append(m_warn)

        menu.append(Gtk.SeparatorMenuItem())

        # ── 2. Canlı Ölçüm Saatleri ──
        ts_list = getattr(self, "_weather_timestamps", [])
        if ts_list:
            for ts_item in ts_list:
                m_time = Gtk.MenuItem.new_with_label(f"🕒 {ts_item}")
                m_time.set_sensitive(False)
                menu.append(m_time)
            menu.append(Gtk.SeparatorMenuItem())
        elif hasattr(self, "_last_tray_fetch") and self._last_tray_fetch > 0:
            import datetime

            last_dt = datetime.datetime.fromtimestamp(self._last_tray_fetch).strftime(
                "%H:%M:%S"
            )
            m_time = Gtk.MenuItem.new_with_label(f"🕒 {_('lbl_last_update')}: {last_dt}")
            m_time.set_sensitive(False)
            menu.append(m_time)
            menu.append(Gtk.SeparatorMenuItem())

        # ── 3. Hızlı Konum & Favoriler ──
        def_loc_str = f"{self._def_il} / {self._def_ilce}" if self._def_ilce else self._def_il
        if getattr(self, "_cur_il", None) and (self._cur_il != self._def_il or (self._cur_ilce and self._cur_ilce != self._def_ilce)):
            m_back_def = Gtk.MenuItem.new_with_label(f"📌 Tanımlı Şehre Dön ({def_loc_str})")
            m_back_def.connect("activate", lambda *_: self._load_default_city())
            menu.append(m_back_def)

        # Favori Şehirler Alt Menüsü:
        favs = self._get_favs() if hasattr(self, "_get_favs") else []
        if favs:
            fav_item = Gtk.MenuItem.new_with_label("⭐ Favori Konumlar")
            fav_sub = Gtk.Menu()
            fav_item.set_submenu(fav_sub)
            for f in favs:
                lbl = f"{f['il']} / {f['ilce']}" if f.get("ilce") else f["il"]
                it = Gtk.MenuItem.new_with_label(f"📍 {lbl}")
                it.connect("activate", lambda _, fav=f: self._load_favorite_and_present(fav))
                fav_sub.append(it)
            menu.append(fav_item)

        # GPS ile Konum Bul:
        m_gps = Gtk.MenuItem.new_with_label("🧭 GPS ile Konumumu Bul")
        m_gps.connect("activate", lambda *_: (self._fetch_location(), self.show(), self.present()))
        menu.append(m_gps)

        menu.append(Gtk.SeparatorMenuItem())

        # ── 4. Canlı Piyasa & Finans (Eğer Finans Etkinse) ──
        if self._show_finance and hasattr(self, "finance_api") and getattr(self.finance_api, "_data", None):
            rates = self.finance_api._data
            if rates:
                fin_item = Gtk.MenuItem.new_with_label(f"💰 {_('btn_finance')} (Canlı Kurlar)")
                fin_sub = Gtk.Menu()
                fin_item.set_submenu(fin_sub)

                quick_keys = [
                    ("USD", "💵 Dolar"),
                    ("EUR", "💶 Euro"),
                    ("GRA", "🪙 Gram Altın"),
                    ("BTC", "₿ Bitcoin"),
                ]
                for code, label_name in quick_keys:
                    if code in rates and isinstance(rates[code], dict):
                        val_txt = rates[code].get("alis") or rates[code].get("fiyat") or rates[code].get("satis") or "-"
                        unit = "$" if code == "BTC" else "₺"
                        r_it = Gtk.MenuItem.new_with_label(f"{label_name}: {val_txt} {unit}")
                        r_it.set_sensitive(False)
                        fin_sub.append(r_it)

                fin_sub.append(Gtk.SeparatorMenuItem())
                port_it = Gtk.MenuItem.new_with_label("💼 Portföy Yönetimi & Detaylar...")
                port_it.connect("activate", lambda *_: self._show_portfolio_dialog())
                fin_sub.append(port_it)

                menu.append(fin_item)
                menu.append(Gtk.SeparatorMenuItem())

        # ── 5. Temel Uygulama İşlemleri ──
        show = Gtk.MenuItem.new_with_label(f"🪟 {_('tray_show_hide')}")
        show.connect("activate", self._tray_toggle)
        menu.append(show)

        refresh = Gtk.MenuItem.new_with_label(f"🌤️ {_('tray_refresh')}")
        refresh.connect("activate", lambda *_: self._search(force=True))
        menu.append(refresh)

        if hasattr(self, "_show_groq_ai_dialog") and getattr(self, "_groq_key", None):
            ai_item = Gtk.MenuItem.new_with_label("🤖 Groq AI Danışmanı")
            ai_item.connect("activate", lambda *_: self._show_groq_ai_dialog())
            menu.append(ai_item)

        update_chk = Gtk.MenuItem.new_with_label(f"🔄 {_('tray_update')}")
        update_chk.connect(
            "activate", lambda *_: self._check_for_updates_bg(forced=True)
        )
        menu.append(update_chk)

        settings_it = Gtk.MenuItem.new_with_label(f"⚙️ {_('btn_settings')}")
        settings_it.connect("activate", self._show_settings)
        menu.append(settings_it)

        ab = Gtk.MenuItem.new_with_label(f"ℹ️ {_('app_about') if _('app_about') != 'app_about' else 'Hakkında'}")
        ab.connect("activate", self._show_about)
        menu.append(ab)

        q = Gtk.MenuItem.new_with_label(f"❌ {_('tray_quit') if _('tray_quit') != 'tray_quit' else 'Çıkış'}")
        q.connect("activate", self._quit)
        menu.append(q)

        menu.show_all()
        return menu

    def _load_default_city(self):
        self.il_entry.set_text(self._def_il)
        self.ilce_entry.set_text(self._def_ilce)
        self._search(force=True)
        self.show()
        self.present()

    def _load_favorite_and_present(self, fav):
        self._load_favorite(None, fav)
        self.show()
        self.present()

    def _apply_tray_data(
        self,
        emoji,
        temp_txt,
        sehir,
        icon_key,
        kisa_desc,
        his_txt="-",
        nem_txt="-",
        ruzgar_txt="-",
    ):
        clean_emoji = svg_to_emoji(emoji)
        self._tray_emoji = clean_emoji
        self._tray_temp = temp_txt
        self._tray_sehir = sehir
        self._tray_desc = kisa_desc
        self._tray_hissedilen = his_txt
        self._tray_nem = nem_txt
        self._tray_ruzgar = ruzgar_txt
        raw = (
            WMO_TRAY.get(icon_key, "weather-clear")
            if isinstance(icon_key, int)
            else TRAY_ICONS.get(icon_key, "weather-clear")
        )
        icon_name = _safe_icon(raw)
        tooltip_text = f"MintSky | {sehir}\n{clean_emoji} {temp_txt}° | {kisa_desc}"
        tooltip_text += f"\n🌡️ {_('lbl_feels_like')}: {his_txt}°\n💧 {_('lbl_humidity')}: %{nem_txt}\n🌬️ {_('lbl_wind')}: {ruzgar_txt}"

        ts_list = getattr(self, "_weather_timestamps", [])
        if ts_list:
            for ts in ts_list:
                tooltip_text += f"\n🕒 {ts}"
        elif hasattr(self, "_last_tray_fetch") and self._last_tray_fetch > 0:
            last_dt = datetime.fromtimestamp(self._last_tray_fetch).strftime("%d.%m.%Y %H:%M")
            tooltip_text += f"\n🕒 {_('lbl_last_update')}: {last_dt}"
        else:
            now_dt = datetime.now().strftime("%d.%m.%Y %H:%M")
            tooltip_text += f"\n🕒 {_('lbl_last_update')}: {now_dt}"

        title_text = f"{sehir} {temp_txt}° · {kisa_desc}"
        if his_txt not in ("-", "--", None) and str(his_txt).strip() != str(temp_txt).strip():
            title_text += f" ({_('lbl_feels_like')}: {his_txt}°)"

        if HAS_INDICATOR:
            self._indicator.set_icon_full(icon_name, tooltip_text)
            self._indicator.set_title(title_text)
            # Menüyü yenile
            self._indicator.set_menu(self._build_tray_menu())
        else:
            self._tray.set_from_icon_name(icon_name)
            self._tray.set_tooltip_text(tooltip_text)

    def _tray_toggle(self, *args):
        if self.get_visible():
            self.hide()
        else:
            self.show()
            self.present()

    def _tray_popup(self, icon, button, t):
        self._build_tray_menu().popup(
            None, None, Gtk.StatusIcon.position_menu, icon, button, t
        )

    def _on_delete(self, *args):
        self.hide()
        return True

    def _quit(self, *args):
        Gtk.main_quit()

    # ──────────────────── Tray Arka Plan Güncelleme ─────────────────────────
    def _tray_update_loop(self):
        now = time.time()
        # TTL dolmadıysa ve daha önce başarılı çekim olduysa atla
        if self._tray_busy:
            return True
        if (
            now - self._last_tray_fetch < TRAY_FETCH_TTL
            and self._last_bg_hadise is not None
        ):
            return True
        threading.Thread(target=self._fetch_tray_bg, daemon=True).start()
        return True

    def _fetch_tray_bg(self):
        self._tray_busy = True
        il, ilce = self._def_il, self._def_ilce
        if not il:
            self._tray_busy = False
            return
        try:
            success, msg, data = WeatherAPI.fetch_weather(il, ilce)
            if not success or not data:
                self._tray_busy = False
                return

            merkez, sd, gd, sk, alarmlar_r, meteoalarm, om_data, msn_data = data
            if not sd and not om_data and not msn_data:
                self._tray_busy = False
                return

            msn_cur = {}
            if msn_data and "responses" in msn_data and msn_data["responses"]:
                try:
                    msn_cur = msn_data["responses"][0]["weather"][0]["current"]
                except Exception:
                    pass

            om_cur = om_data.get("current", {}) if om_data else {}
            use_msn = self._api_source == "msn" and msn_cur
            use_om = (
                (self._api_source == "openmeteo" and om_cur)
                or (not sd and om_cur and not use_msn)
                or (self._language != "tr" and om_cur and not use_msn)
            )

            if use_msn:
                cap = msn_cur.get("cap", "")
                emoji, kisa = "🌤️", cap
                sicak = msn_cur.get("temp", -9999)
                his = msn_cur.get("feels", -9999)
                h_kod = 0
                nem = msn_cur.get("rh", -9999)
                r_hiz = msn_cur.get("windSpd", -9999)
                r_yon_txt = ""
            elif use_om:
                wmo_kod = om_cur.get("weather_code")
                is_night = om_cur.get("is_day", 1) == 0
                emoji, kisa, _dummy = hadise_wmo(wmo_kod, is_night)
                sicak = om_cur.get("temperature_2m", -9999)
                his = om_cur.get("apparent_temperature", -9999)
                h_kod = wmo_kod or 0
                nem = om_cur.get("relative_humidity_2m", -9999)
                r_hiz = om_cur.get("wind_speed_10m", -9999)
                r_yon = om_cur.get("wind_direction_10m")
                r_yon_txt = yon(r_yon) if r_yon is not None else ""
            else:
                h_kod = sd.get("hadiseKodu", "") if sd else ""
                now_h = datetime.now().hour
                is_night = now_h < 6 or now_h >= 19
                emoji, kisa, _dummy = hadise_mgm(h_kod, is_night)
                sicak = sd.get("sicaklik", -9999) if sd else -9999
                his = sd.get("hissedilenSicaklik", -9999) if sd else -9999
                nem = sd.get("nem", -9999) if sd else -9999
                r_yon_val = sd.get("ruzgarYon", -9999) if sd else -9999
                r_yon_txt = yon(r_yon_val) if r_yon_val not in (-9999, None) else ""
                r_hiz = sd.get("ruzgarHiz", -9999) if sd else -9999

            ttxt = f"{sicak:.0f}" if sicak not in (-9999, None) else "--"
            sehir = f"{il} / {ilce}" if ilce else il
            hissedilen_bg = f"{his:.0f}" if his not in (-9999, None) else "--"
            nem_bg = f"{nem:.0f}" if nem not in (-9999, None) else "--"
            ruzgar_bg = (
                self._format_wind(r_hiz, r_yon_txt)
                if r_hiz not in (-9999, None)
                else "--"
            )

            timestamp_parts = []
            for source, value in (
                ("MGM", sd.get("veriZamani", "") if sd else ""),
                ("Open-Meteo", om_cur.get("time", "") if om_cur else ""),
                ("MSN", msn_cur.get("created", "") if msn_cur else ""),
            ):
                if value:
                    if source == "MGM" and self._language != "tr":
                        continue
                    timestamp_parts.append(f"{source}: {fmt_dt(value)}")
            self._weather_timestamps = timestamp_parts

            GLib.idle_add(
                self._apply_tray_data,
                emoji,
                ttxt,
                sehir,
                h_kod,
                kisa,
                hissedilen_bg,
                nem_bg,
                ruzgar_bg,
            )
            self._last_tray_fetch = time.time()

            aktif = []
            if self._language == "tr":
                for a in alarmlar_r if isinstance(alarmlar_r, list) else []:
                    if not isinstance(a, dict):
                        continue
                    if a.get("il", "").upper() == il.upper():
                        aktif.append(a.get("baslik"))
                for ma in meteoalarm or []:
                    if (
                        ma.get("il", "").upper() == il.upper()
                        and int(ma.get("seviye", 1)) >= 2
                    ):
                        aktif.append(f"{ma.get('etkinlik') or 'MeteoAlarm'}")

            if self._last_bg_hadise is None:
                self._last_bg_hadise = h_kod
                self._last_bg_alarms = aktif
                self._tray_busy = False
                return

            msgs = []
            if self._last_bg_hadise != h_kod:
                msgs.append(f"Hava durumu değişti: {kisa}")
            yeni = [a for a in aktif if a not in self._last_bg_alarms]
            if yeni:
                msgs.append("⚠️ Yeni uyarı: " + ", ".join(yeni))

            if msgs and self._notify_enabled and HAS_NOTIFY:
                icon = _safe_icon(
                    "weather-storm"
                    if yeni
                    else (
                        WMO_TRAY.get(h_kod, "weather-clear")
                        if isinstance(h_kod, int)
                        else TRAY_ICONS.get(h_kod, "weather-clear")
                    )
                )
                title = (
                    f"⚠️ MintSky Hava Uyarısı — {sehir}"
                    if yeni
                    else f"☁️ MintSky Hava — {sehir}"
                )
                body = "\n".join(msgs) + f"\n🌡 Sıcaklık: {ttxt}°C"
                n = Notify.Notification.new(title, body, icon)
                n.set_urgency(2 if yeni else 1)
                GLib.idle_add(n.show)

            self._last_bg_hadise = h_kod
            self._last_bg_alarms = aktif
        except Exception as e:
            print(f"[MintSky] Hata: {e}")
        finally:
            self._tray_busy = False

    # ──────────────────── Konum GPS ────────────────────────────────────────
    def _fetch_location(self):
        self._status("📡 Konum alınıyor…")
        threading.Thread(target=self._location_thread, daemon=True).start()

    def _location_thread(self):
        try:
            # Linux masaüstülerinde GPS donanımı çoğunlukla yoktur. Önce GeoClue
            # (izin verildiyse Wi-Fi/ağ tabanlı sistem konumu), sonra HTTPS IP
            # konumu kullanılır. IP sonucu yaklaşık olabilir.
            coords = self._geoclue_coordinates()
            if coords:
                lat, lon = coords
                data = {}
            else:
                response = requests.get("https://ipapi.co/json/", timeout=8)
                response.raise_for_status()
                data = response.json()
                lat, lon = data.get("latitude"), data.get("longitude")
                if data.get("error") or lat is None or lon is None:
                    raise ValueError("Konum sağlayıcısı koordinat döndürmedi")
            nearest = WeatherAPI.find_nearest_location(lat, lon)
            if nearest:
                GLib.idle_add(
                    self._apply_location,
                    nearest.get("il", ""),
                    nearest.get("ilce", ""),
                )
                return
            addr = (
                requests.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "format": "json",
                        "accept-language": self._language or "tr",
                        "zoom": 10,
                    },
                    headers=NOM_HEADERS,
                    timeout=8,
                )
                .json()
                .get("address", {})
            )
            il = (
                (
                    addr.get("province")
                    or addr.get("state")
                    or data.get("region", "")
                    or data.get("city", "")
                )
                .replace(" ili", "")
                .replace(" İli", "")
                .strip()
            )
            ilce = (
                (
                    addr.get("county")
                    or addr.get("town")
                    or addr.get("city_district")
                    or data.get("city", "")
                    or ""
                )
                .replace(" İlçesi", "")
                .replace(" ilçesi", "")
                .replace(" Merkez", "")
                .strip()
            )
            GLib.idle_add(self._apply_location, il, ilce)
        except Exception as e:
            GLib.idle_add(self._location_failed, str(e))

    def _geoclue_coordinates(self):
        """Return system location when GeoClue is available and permits access."""
        try:
            from gi.repository import Gio, GLib as _GLib

            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            manager = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None,
                "org.freedesktop.GeoClue2", "/org/freedesktop/GeoClue2/Manager",
                "org.freedesktop.GeoClue2.Manager", None,
            )
            object_path = manager.call_sync(
                "GetClient", None, Gio.DBusCallFlags.NONE, 5000, None
            ).unpack()[0]
            client = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None, "org.freedesktop.GeoClue2",
                object_path, "org.freedesktop.GeoClue2.Client", None,
            )
            client.call_sync(
                "org.freedesktop.DBus.Properties.Set",
                _GLib.Variant("(ssv)", ("org.freedesktop.GeoClue2.Client", "DesktopId", _GLib.Variant("s", "mintsky"))),
                Gio.DBusCallFlags.NONE, 5000, None,
            )
            client.call_sync(
                "org.freedesktop.DBus.Properties.Set",
                _GLib.Variant("(ssv)", ("org.freedesktop.GeoClue2.Client", "RequestedAccuracyLevel", _GLib.Variant("u", 6))),
                Gio.DBusCallFlags.NONE, 5000, None,
            )
            client.call_sync("Start", None, Gio.DBusCallFlags.NONE, 5000, None)
            location_path = None
            for _ in range(20):
                location_variant = client.get_cached_property("Location")
                if location_variant:
                    location_path = location_variant.unpack()
                    if location_path != "/":
                        break
                time.sleep(0.25)
            if not location_path or location_path == "/":
                return None
            location = Gio.DBusProxy.new_sync(
                bus, Gio.DBusProxyFlags.NONE, None, "org.freedesktop.GeoClue2",
                location_path, "org.freedesktop.GeoClue2.Location", None,
            )
            lat = location.get_cached_property("Latitude").unpack()
            lon = location.get_cached_property("Longitude").unpack()
            return (lat, lon) if -90 <= lat <= 90 and -180 <= lon <= 180 else None
        except Exception:
            return None

    def _location_failed(self, error):
        self._status(f"Konum alınamadı ({error}). İl/ilçeyi elle seçebilirsiniz.", True)
        return False

    def _apply_location(self, il, ilce):
        self.il_entry.set_text(il)
        self.ilce_entry.set_text(ilce)
        self._search(force=True)

    # ──────────────────── Favoriler ────────────────────────────────────────
    def _get_favs(self):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _toggle_favorite(self, *args):
        if not self._cur_il:
            return
        favs = self._get_favs()
        entry = {"il": self._cur_il, "ilce": self._cur_ilce}
        exists = any(
            f["il"] == entry["il"] and f.get("ilce", "") == entry["ilce"] for f in favs
        )
        favs = (
            [
                f
                for f in favs
                if not (f["il"] == entry["il"] and f.get("ilce", "") == entry["ilce"])
            ]
            if exists
            else favs + [entry]
        )
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, ensure_ascii=False, indent=2)
        self._refresh_fav_button(not exists)

    def _refresh_fav_button(self, is_fav):
        ctx = self.btn_fav.get_style_context()
        icon = self.btn_fav.get_child().get_children()[0]
        lbl = self.btn_fav.get_child().get_children()[1]
        if is_fav:
            ctx.remove_class("btn-tool")
            ctx.add_class("btn-fav-active")
            lbl.set_markup("<span size='small'>Fav'dan Çıkar</span>")
            if isinstance(icon, Gtk.Image):
                icon.set_from_icon_name("starred-symbolic", Gtk.IconSize.DND)
        else:
            ctx.remove_class("btn-fav-active")
            ctx.add_class("btn-tool")
            lbl.set_markup("<span size='small' color='#8b949e'>Favorile</span>")
            if isinstance(icon, Gtk.Image):
                icon.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.DND)

    def _sync_fav_button(self):
        self._refresh_fav_button(
            any(
                f["il"] == self._cur_il and f.get("ilce", "") == self._cur_ilce
                for f in self._get_favs()
            )
        )

    def _show_favorites_menu(self, widget):
        favs = self._get_favs()
        menu = Gtk.Menu()
        if not favs:
            it = Gtk.MenuItem.new_with_label("Henüz favori yok")
            it.set_sensitive(False)
            menu.append(it)
        else:
            for f in favs:
                lbl = f"{f['il']} / {f['ilce']}" if f.get("ilce") else f["il"]
                it = Gtk.MenuItem.new_with_label(lbl)
                it.connect("activate", self._load_favorite, f)
                menu.append(it)
            menu.append(Gtk.SeparatorMenuItem())
            clr = Gtk.MenuItem.new_with_label("🗑 Tüm Favorileri Sil")
            clr.connect("activate", self._clear_favorites)
            menu.append(clr)
        menu.show_all()
        menu.popup_at_widget(
            widget, Gdk.Gravity.SOUTH_WEST, Gdk.Gravity.NORTH_WEST, None
        )

    def _load_favorite(self, _, fav):
        self.il_entry.set_text(fav.get("il", ""))
        self.ilce_entry.set_text(fav.get("ilce", ""))
        self._search(force=True)  # farklı konum = taze fetch

    def _clear_favorites(self, *args):
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        self._sync_fav_button()

    # ──────────────────── Temel UI Yardımcıları ────────────────────────────
    def _clear(self):
        for w in self.compact_content.get_children():
            self.compact_content.remove(w)
        for w in self.content.get_children():
            self.content.remove(w)

    def _status(self, msg, error=False):
        self._clear()
        lbl = Gtk.Label(label=msg)
        self._sc(lbl, "err-lbl" if error else "status-lbl")
        lbl.set_halign(Gtk.Align.CENTER)
        lbl.set_margin_top(60)
        lbl.set_line_wrap(True)
        lbl.set_max_width_chars(40)
        self.compact_content.pack_start(lbl, False, False, 0)
        self.compact_content.show_all()

    @staticmethod
    def _sc(widget, *classes):
        for c in classes:
            widget.get_style_context().add_class(c)

    def _section_title(self, text):
        lbl = Gtk.Label(label=text)
        self._sc(lbl, "sec-title")
        lbl.set_halign(Gtk.Align.START)
        self.content.pack_start(lbl, False, False, 0)

    @staticmethod
    def _safe_json(resp, default=None):
        try:
            return (
                resp.json()
                if resp.text.strip()
                else (default if default is not None else [])
            )
        except Exception:
            return default if default is not None else []

    def _make_pill(self, key, value, tooltip=None):
        pill = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self._sc(pill, "pill-box")

        # Lucide SVG İkon Eşleştirmeleri
        lucide_map = {
            "💧🌡️": "thermometer",
            "🌬️⚡": "gust",
            "💧": "droplets",
            "🌬️": "wind",
            "🎚️": "gauge",
            "👁": "eye",
            "🌧": "cloud-rain",
            "🌊": "waves",
            "☁": "cloud",
            "❄": "cloud-snow",
            "🔆": "sun",
            "🌂": "umbrella",
            "☀": "sun",
            "🌅": "sunrise",
            "🌇": "sunset",
        }

        clean_key = key
        matched_icon = None
        for emoji_key, sys_icon in lucide_map.items():
            if key.startswith(emoji_key):
                matched_icon = sys_icon
                clean_key = key.replace(emoji_key, "").strip(" \ufe0f")
                break

        k_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        if matched_icon:
            img = get_svg_image(matched_icon, size=24, folder="pills")
            if img:
                self._sc(img, "pill-key")
                k_box.pack_start(img, False, False, 0)

        kl = Gtk.Label(label=clean_key)
        self._sc(kl, "pill-key")
        kl.set_halign(Gtk.Align.START)
        k_box.pack_start(kl, False, False, 0)

        vl = Gtk.Label(label=value)
        self._sc(vl, "pill-val")
        vl.set_halign(Gtk.Align.START)

        pill.pack_start(k_box, False, False, 0)
        pill.pack_start(vl, False, False, 0)

        tt = tooltip or PILL_TOOLTIPS.get(clean_key) or PILL_TOOLTIPS.get(key)
        if tt:
            pill.set_has_tooltip(True)
            pill.set_tooltip_text(tt)
        return pill

    # ──────────────────── Ana Arama ────────────────────────────────────────
    # ─── ANA ARAMA — Önbellekli ────────────────────────────────────────────
    def _search(self, *_, force=False):
        il = self.il_entry.get_text().strip()
        ilce = self.ilce_entry.get_text().strip()
        if not il:
            self._status("Lütfen en az il adı girin.", error=True)
            return False

        key = f"{il}|{ilce}"

        # Önbellek tazeyse ve aynı konumsa — API atmadan render et
        if not force and self._cache_is_fresh(key):
            GLib.idle_add(self._render_from_cache)
            return False

        # Eş zamanlı fetch varsa yeni istek açma (force değilse)
        if self._fetch_in_progress and not force:
            return False

        self._status("⏳ Veriler alınıyor…")
        self._last_api_call = time.time()
        self._fetch_in_progress = True
        self._weather_request_id += 1
        request_id = self._weather_request_id

        with self.finance_api._lock:
            has_fin = bool(self.finance_api._data)
        if self._show_finance and not has_fin:
            self.finance_api.fetch_bg(callback=self._on_finance_fetched)

        def _fetch(il, ilce):
            try:
                success, message, data_content = WeatherAPI.fetch_weather(il, ilce)
            except Exception as e:
                print(f"Fetch hatası: {e}")
                success, message, data_content = False, str(e), None

            GLib.idle_add(
                self._finish_weather_search,
                request_id,
                key,
                success,
                message,
                data_content,
            )

        threading.Thread(target=_fetch, args=(il, ilce), daemon=True).start()
        return False

    def _finish_weather_search(self, request_id, key, success, message, data):
        """Apply only the newest network result, on GTK's main thread."""
        if request_id != self._weather_request_id:
            return False
        self._fetch_in_progress = False
        if not success or not data:
            self._status(message or "Hava durumu verisi alınamadı.", error=True)
            return False

        self._weather_cache = data
        self._weather_cache_ts = time.time()
        self._weather_cache_key = key
        self._render(*data)
        return False

    # ──────────────────── Render ───────────────────────────────────────────
    def _render(self, merkez, sd, gd, sk, alarmlar, meteoalarm, om_data, msn_data={}):
        self._clear()
        il = merkez.get("il", "")
        ilce = merkez.get("ilce", "")
        sehir = f"{il} / {ilce}" if ilce else il
        self._cur_il, self._cur_ilce = il, ilce
        self._sync_fav_button()

        msn_cur = {}
        if msn_data and "responses" in msn_data and msn_data["responses"]:
            try:
                msn_cur = msn_data["responses"][0]["weather"][0]["current"]
            except:
                pass

        om_cur = om_data.get("current", {}) if om_data else {}
        use_msn = self._api_source == "msn" and msn_cur
        use_om = (
            (self._api_source == "openmeteo" and om_cur)
            or (not sd and om_cur and not use_msn)
            or (self._language != "tr" and om_cur and not use_msn)
        )

        if use_msn:
            cap = msn_cur.get("cap", "")
            emoji, kisa, uzun = "🌤️", cap, cap
            sicak = msn_cur.get("temp", -9999)
            his = msn_cur.get("feels", -9999)
            h_kod_for_tray = 0
            if sd is None or not isinstance(sd, dict):
                sd = {}
            sd["nem"] = msn_cur.get("rh", -9999)
            sd["ruzgarHiz"] = msn_cur.get("windSpd", -9999)
            sd["denizeIndirgenmisBasinc"] = msn_cur.get("baro", -9999)
            sd["gorus"] = msn_cur.get("vis", -9999)
            om_cur["uv_index"] = msn_cur.get("uv", -9999)
        elif use_om:
            wmo_kod = om_cur.get("weather_code")
            is_night = om_cur.get("is_day", 1) == 0
            emoji, kisa, uzun = hadise_wmo(wmo_kod, is_night)
            sicak = om_cur.get("temperature_2m", -9999)
            his = om_cur.get("apparent_temperature", -9999)
            h_kod_for_tray = wmo_kod or 0
        else:
            h_kod = sd.get("hadiseKodu", "")
            now_h = datetime.now().hour
            is_night = now_h < 6 or now_h >= 19
            emoji, kisa, uzun = hadise_mgm(h_kod, is_night)
            sicak = sd.get("sicaklik", -9999)
            his = sd.get("hissedilenSicaklik", -9999)
            h_kod_for_tray = h_kod

        uyarilar = []
        if self._language == "tr":
            uyarilar = [
                a.get("baslik", "")
                for a in alarmlar
                if a.get("il", "").upper() == il.upper()
            ]
            for ma in meteoalarm or []:
                if ma.get("il", "").upper() == il.upper() and int(ma.get("seviye", 1)) >= 2:
                    uyarilar.append(f"{ma.get('etkinlik') or 'MeteoAlarm'}")

        mgm_tahminler = sk.get("tahmin", []) if (not use_om and self._language == "tr") else []
        om_hourly = om_data.get("hourly", {}) if om_data else {}
        om_times = om_hourly.get("time", [])

        tahmin_3s = []
        if mgm_tahminler:
            for item in mgm_tahminler[:3]:
                h_str = fmt_time(item.get("tarih", ""))
                h_int = int(h_str.split(":")[0]) if ":" in h_str else 12
                em, ksa, _dummy2 = hadise_mgm(
                    item.get("hadise", ""), (h_int < 6 or h_int >= 19)
                )
                nem_h = item.get("nem", "-")
                tahmin_3s.append(
                    (
                        h_str,
                        em,
                        val(item.get("sicaklik", -9999), suffix="°"),
                        ksa,
                        nem_h,
                    )
                )
        elif om_times:
            now_h = datetime.now().strftime("%Y-%m-%dT%H:")
            st = next(
                (i for i, t in enumerate(om_times) if t.startswith(now_h[:13])), 0
            )
            temps_h = om_hourly.get("temperature_2m", [])
            wcodes_h = om_hourly.get("weather_code", [])
            for i in range(st, min(st + 3, len(om_times))):
                is_night_h = (
                    (om_hourly.get("is_day", [])[i] == 0)
                    if i < len(om_hourly.get("is_day", []))
                    else False
                )
                em, ksa, _dummy2 = hadise_wmo(
                    wcodes_h[i] if i < len(wcodes_h) else None, is_night_h
                )
                nem_h = (
                    om_hourly.get("relative_humidity_2m", [])[i]
                    if i < len(om_hourly.get("relative_humidity_2m", []))
                    else "-"
                )
                tahmin_3s.append(
                    (
                        om_times[i][11:16],
                        em,
                        val(temps_h[i] if i < len(temps_h) else -9999, suffix="°"),
                        ksa,
                        nem_h,
                    )
                )

        def get_best(sd_key, om_key, msn_key):
            v = None
            if use_msn:
                v = msn_cur.get(msn_key) if msn_key else None
                if v in (None, -9999, "") and om_cur and om_key:
                    v = om_cur.get(om_key)
                if v in (None, -9999, "") and sd and sd_key:
                    v = sd.get(sd_key)
            elif use_om:
                v = om_cur.get(om_key) if om_key else None
                if v in (None, -9999, "") and msn_cur and msn_key:
                    v = msn_cur.get(msn_key)
                if v in (None, -9999, "") and sd and sd_key:
                    v = sd.get(sd_key)
            else:
                v = sd.get(sd_key) if sd and sd_key else None
                if v in (None, -9999, "") and om_cur and om_key:
                    v = om_cur.get(om_key)
                if v in (None, -9999, "") and msn_cur and msn_key:
                    v = msn_cur.get(msn_key)
            return v if v not in (None, -9999, "") else None

        uv_val = get_best(None, "uv_index", "uv")
        aqi_val = msn_cur.get("aqi") if msn_cur else None
        nem_val = get_best("nem", "relative_humidity_2m", "rh")
        ruzgar_hiz = get_best("ruzgarHiz", "wind_speed_10m", "windSpd")
        r_yon_val = get_best("ruzgarYon", "wind_direction_10m", "windDir")
        ruzgar_yon = yon(r_yon_val) if r_yon_val is not None else ""
        basinc = get_best("denizeIndirgenmisBasinc", "surface_pressure", "baro")
        gorus_v = get_best("gorus", "visibility", "vis")
        # MSN reports visibility in km, while MGM and Open-Meteo use metres.
        if use_msn and msn_cur.get("vis") not in (None, -9999, ""):
            try:
                gorus_v = float(msn_cur["vis"]) * 1000
            except (TypeError, ValueError):
                gorus_v = None
        gustu = get_best(None, "wind_gusts_10m", "windGust")

        yag_olas = (
            om_hourly.get("precipitation_probability", [None])[0]
            if om_hourly.get("precipitation_probability")
            else None
        )

        self._last_render_data = {
            "sehir": sehir,
            "kisa": kisa,
            "h_kod": h_kod_for_tray,
            "sicak_str": val(sicak, suffix="°C"),
            "his_str": (val(his, suffix="°C") if his not in (-9999, None) else ""),
            "nem": nem_val,
            "ruzgar": self._format_wind(ruzgar_hiz, ruzgar_yon),
            "basinc": basinc if basinc not in (-9999, None) else None,
            "gorus": gorus_v if gorus_v not in (-9999, None) else None,
            "uv": uv_val,
            "yagis_olas": yag_olas,
            "gustu": gustu,
            "uyarilar": uyarilar,
            "tahmin_3s": tahmin_3s,
        }

        # ── Ana hava kartı ──
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self._sc(card, "cur-card")
        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lcol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        city_lbl = Gtk.Label(label=sehir)
        self._sc(city_lbl, "cur-city")
        city_lbl.set_halign(Gtk.Align.START)
        lcol.pack_start(city_lbl, False, False, 0)

        cond = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        c_icon = get_svg_image(emoji, size=56)
        c_lbl = Gtk.Label(label=kisa)
        self._sc(c_lbl, "cur-cond")
        cond.pack_start(c_icon, False, False, 0)
        cond.pack_start(c_lbl, False, False, 0)
        cond.set_halign(Gtk.Align.START)
        if uzun:
            cond.set_tooltip_text(uzun)
        lcol.pack_start(cond, False, False, 0)

        if uzun:
            desc = Gtk.Label(label=uzun)
            self._sc(desc, "cur-desc")
            desc.set_halign(Gtk.Align.START)
            desc.set_line_wrap(True)
            desc.set_max_width_chars(38)
            lcol.pack_start(desc, False, False, 0)
        if use_msn:
            lbl_txt = f"🛰 <span font_weight='bold'>MSN</span> {_('settings_tab_weather') if self._language != 'tr' else 'Hava Durumu'}"
        elif use_om or self._language != "tr":
            lbl_txt = "🛰 <span font_weight='bold'>Open-Meteo</span> API"
        else:
            lbl_txt = "🛰 <span font_weight='bold'>MGM</span>"
            if om_cur:
                lbl_txt += " + <span font_weight='bold'>Open-Meteo</span>"
            if msn_cur:
                lbl_txt += " + <span font_weight='bold'>MSN</span>"

        src_badge = Gtk.Label()
        src_badge.set_markup(lbl_txt)
        self._sc(src_badge, "om-badge")
        src_badge.set_halign(Gtk.Align.START)
        lcol.pack_start(src_badge, False, False, 0)
        top.pack_start(lcol, True, True, 0)

        rcol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        rcol.set_halign(Gtk.Align.END)
        t_lbl = Gtk.Label(label=val(sicak, suffix="°"))
        self._sc(t_lbl, "cur-temp")
        t_lbl.set_halign(Gtk.Align.END)
        t_lbl.set_tooltip_text(f"Anlık Sıcaklık: {val(sicak,suffix='°C')}")
        rcol.pack_start(t_lbl, False, False, 0)
        if his not in (-9999, None):
            f_lbl = Gtk.Label(label=f"{_('lbl_feels_like')} {val(his,suffix='°')}")
            self._sc(f_lbl, "cur-feels")
            f_lbl.set_halign(Gtk.Align.END)
            rcol.pack_start(f_lbl, False, False, 0)
        top.pack_start(rcol, False, False, 0)
        card.pack_start(top, False, False, 0)

        timestamp_parts = []
        for source, value in (
            ("MGM", sd.get("veriZamani", "") if sd else ""),
            ("Open-Meteo", om_cur.get("time", "") if om_cur else ""),
            ("MSN", msn_cur.get("created", "") if msn_cur else ""),
        ):
            if value:
                if source == "MGM" and self._language != "tr":
                    continue
                timestamp_parts.append(f"{source}: {fmt_dt(value)}")
        self._weather_timestamps = timestamp_parts

        ttxt = f"{sicak:.0f}" if sicak not in (-9999, None) else "--"
        h_str = f"{his:.0f}" if his not in (-9999, None) else "--"
        n_str = f"{nem_val:.0f}" if nem_val not in (-9999, None) else "--"
        r_str = (
            self._format_wind(ruzgar_hiz, ruzgar_yon)
            if ruzgar_hiz not in (-9999, None)
            else "--"
        )
        self._apply_tray_data(
            emoji, ttxt, sehir, h_kod_for_tray, kisa, h_str, n_str, r_str
        )

        self.compact_content.pack_start(card, False, False, 0)

        # ── Widget: 3 saatlik tahmin ──
        if self._is_compact and self._show_saatlik and tahmin_3s:
            w3_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            w3_box.set_halign(Gtk.Align.CENTER)
            w3_box.set_margin_top(4)
            w3_box.set_margin_bottom(4)
            for idx, (t_str, em, tmp, ksa, nem_h) in enumerate(tahmin_3s):
                bx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                self._sc(bx, "w3-card")
                bx.set_halign(Gtk.Align.CENTER)
                tl = Gtk.Label(label=t_str)
                self._sc(tl, "w3-time")
                tl.set_halign(Gtk.Align.CENTER)
                el = get_svg_image(em, size=46)
                el.set_halign(Gtk.Align.CENTER)
                vl = Gtk.Label(label=tmp)
                self._sc(vl, "w3-temp")
                vl.set_halign(Gtk.Align.CENTER)
                hl = Gtk.Label(label=ksa)
                self._sc(hl, "w3-desc")
                hl.set_halign(Gtk.Align.CENTER)
                nl = Gtk.Label(label=f"💧 Nem: %{nem_h}")
                self._sc(nl, "w3-nem")
                nl.set_halign(Gtk.Align.CENTER)
                bx.pack_start(tl, False, False, 0)
                bx.pack_start(el, False, False, 0)
                bx.pack_start(vl, False, False, 0)
                bx.pack_start(hl, False, False, 0)
                bx.pack_start(nl, False, False, 0)
                w3_box.pack_start(bx, False, False, 0)
                if idx < len(tahmin_3s) - 1:
                    sep_lbl = Gtk.Label(label="›")
                    self._sc(sep_lbl, "w3-sep")
                    w3_box.pack_start(sep_lbl, False, False, 0)
            self.compact_content.pack_start(w3_box, False, False, 0)

        # ── Widget: Finans mini panel ──
        if self._is_compact and self._show_finance:
            with self.finance_api._lock:
                fin_rates = dict(self.finance_api._data)
            if fin_rates:
                self._render_finance_widget(fin_rates)

        # ── Pill kartlar ──
        all_pills = []

        # 1. Nem & Yağış Grubu
        if nem_val not in (-9999, None):
            all_pills.append((f"💧 {_('lbl_humidity')}", f"%{nem_val:.0f}"))
        if om_cur and om_cur.get("dew_point_2m") is not None and self._show_extra:
            all_pills.append(
                (f"💧🌡️ {_('lbl_dew_point')}", f"{om_cur['dew_point_2m']:.1f}°C")
            )
        if yag_olas is not None and self._show_extra:
            all_pills.append((f"🌂 {_('lbl_rain_prob')}", f"%{yag_olas:.0f}"))

        # 2. Rüzgar & Hava Grubu
        if ruzgar_hiz not in (-9999, None):
            all_pills.append(
                (f"🌬️ {_('lbl_wind')}", self._format_wind(ruzgar_hiz, ruzgar_yon))
            )
        if gustu is not None and self._show_extra:
            all_pills.append((f"🌬️⚡ {_('lbl_wind_gust')}", self._format_wind(gustu)))
        if basinc not in (-9999, None):
            all_pills.append((f"🎚️ {_('lbl_pressure')}", f"{basinc:.0f} hPa"))

        # 3. Gökyüzü Grubu
        if self._show_extra:
            if om_cur and om_cur.get("cloud_cover") is not None:
                all_pills.append(
                    (f"☁ {_('lbl_clouds')}", f"%{om_cur['cloud_cover']:.0f}")
                )
            elif (
                sd.get("kapalilik", -9999) not in (-9999, None)
                and sd.get("kapalilik") > 0
            ):
                all_pills.append(
                    (f"☁ {_('lbl_clouds')}", f"%{sd['kapalilik'] * 12.5:.0f}")
                )

        if gorus_v not in (-9999, None):
            all_pills.append(
                (
                    f"👁 {_('lbl_visibility')}",
                    f"{gorus_v/1000:.0f} km" if gorus_v >= 1000 else f"{gorus_v:.0f} m",
                )
            )

        if uv_val is not None and self._show_extra:
            uv_lbl = f"{uv_val:.1f}"
            if uv_val <= 2:
                uv_lbl += f" ({_('Düşük')})"
            elif uv_val <= 5:
                uv_lbl += f" ({_('Orta')})"
            elif uv_val <= 7:
                uv_lbl += f" ({_('Yüksek')})"
            elif uv_val <= 10:
                uv_lbl += f" ({_('Çok Yüksek')})"
            else:
                uv_lbl += f" ({_('Aşırı')})"
            all_pills.append((f"🔆 {_('lbl_uv')}", uv_lbl))

        if aqi_val is not None and self._show_extra:
            aqi_lbl = f"{aqi_val:.0f}"
            if aqi_val <= 50:
                aqi_lbl += f" ({_('İyi')})"
            elif aqi_val <= 100:
                aqi_lbl += f" ({_('Orta')})"
            elif aqi_val <= 150:
                aqi_lbl += f" ({_('Hassas')})"
            elif aqi_val <= 200:
                aqi_lbl += f" ({_('Kötü')})"
            elif aqi_val <= 300:
                aqi_lbl += f" ({_('Çok Kötü')})"
            else:
                aqi_lbl += f" ({_('Tehlikeli')})"

            aqi_tt = (
                f"0-50: {_('İyi')}\n"
                f"51-100: {_('Orta')}\n"
                f"101-150: {_('Hassas')}\n"
                f"151-200: {_('Kötü')}\n"
                f"201-300: {_('Çok Kötü')}\n"
                f"300+: {_('Tehlikeli')}"
            )
            all_pills.append((f"😷 {_('lbl_aqi')}", aqi_lbl, aqi_tt))

        # 4. Güneş & Astronomi Grubu
        if self._show_extra:
            sun_list = (
                om_data.get("daily", {}).get("sunshine_duration", []) if om_data else []
            )
            if sun_list and sun_list[0] is not None:
                all_pills.append(
                    (f"☀ {_('lbl_sunshine')}", f"{sun_list[0]/3600:.1f} saat")
                )
            sunrise_list = (
                om_data.get("daily", {}).get("sunrise", []) if om_data else []
            )
            if sunrise_list and sunrise_list[0]:
                all_pills.append((f"🌅 {_('pill_sunrise')}", f"{sunrise_list[0][-5:]}"))
            sunset_list = om_data.get("daily", {}).get("sunset", []) if om_data else []
            if sunset_list and sunset_list[0]:
                all_pills.append((f"🌇 {_('pill_sunset')}", f"{sunset_list[0][-5:]}"))

        # 5. Ekstralar (Deniz Suyu, Kar, Anlık Yağış)
        if self._show_extra:
            if (
                om_cur
                and om_cur.get("precipitation") is not None
                and om_cur["precipitation"] > 0
            ):
                all_pills.append(
                    (f"🌧 {_('lbl_precip_now')}", f"{om_cur['precipitation']:.1f} mm")
                )
            elif (
                sd.get("yagis1Saat", -9999) not in (-9999, None)
                and sd.get("yagis1Saat") > 0
            ):
                all_pills.append(
                    (f"🌧 {_('lbl_precip_1h')}", f"{sd['yagis1Saat']:.1f} mm")
                )

            if (
                sd.get("yagis24Saat", -9999) not in (-9999, None)
                and sd.get("yagis24Saat") > 0
            ):
                all_pills.append(
                    (f"🌧 {_('lbl_precip_24h')}", f"{sd['yagis24Saat']:.1f} mm")
                )

            if self._language == "tr":
                # MGM station observations expose shorter accumulation windows
                # than the other providers. Show only measured, non-zero values.
                for field, label_key in (
                    ("yagis00Now", "lbl_precip_since_midnight"),
                    ("yagis10Dk", "lbl_precip_10m"),
                    ("yagis6Saat", "lbl_precip_6h"),
                    ("yagis12Saat", "lbl_precip_12h"),
                ):
                    try:
                        amount = float(sd.get(field, -9999))
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(amount) and amount > 0:
                        all_pills.append((f"🌧 {_(label_key)}", f"{amount:.1f} mm"))

                climate = sd.get("_ucdegerler") or {}
                try:
                    average_low = float(climate["minOrt"])
                    average_high = float(climate["maxOrt"])
                    record_low = float(climate["min"])
                    record_high = float(climate["max"])
                    climate_values = (average_low, average_high, record_low, record_high)
                    if all(math.isfinite(value) and value != -9999 for value in climate_values):
                        climate_text = f"{average_low:.0f}–{average_high:.0f}°C"
                        climate_tip = (
                            f"{_('lbl_climate_tooltip')}\n"
                            f"{_('lbl_climate_records')}: {record_low:.0f}–{record_high:.0f}°C"
                        )
                        all_pills.append(
                            (f"🌡️ {_('lbl_climate_norm')}", climate_text, climate_tip)
                        )
                except (KeyError, TypeError, ValueError):
                    pass

            deniz = sd.get("denizSicaklik", -9999)
            if deniz not in (-9999, None) and deniz > 0:
                sea_time = sd.get("denizVeriZamani")
                sea_tip = None
                if sea_time:
                    sea_tip = (
                        f"{_('lbl_measurement_time')} ({_('lbl_turkey_time')}): "
                        f"{fmt_dt(sea_time)}"
                    )
                all_pills.append(
                    (f"🌊 {_('lbl_sea')}", f"{deniz:.0f}°C", sea_tip)
                )

            kar = sd.get("karYukseklik", -9999)
            if kar not in (-9999, None) and kar > 0:
                all_pills.append((f"❄ {_('lbl_snow')}", f"{kar:.0f} cm"))

        if all_pills:
            grid = Gtk.Grid()
            grid.set_column_spacing(4)
            grid.set_row_spacing(4)
            grid.set_column_homogeneous(True)
            grid.set_margin_start(12)
            grid.set_margin_end(12)
            for i, item in enumerate(all_pills):
                grid.attach(self._make_pill(*item), i % 3, i // 3, 1, 1)
            self.content.pack_start(grid, False, False, 0)

        if timestamp_parts:
            timestamp_text = " · ".join(timestamp_parts)
            ts = Gtk.Label(
                label=(
                    f"{_('lbl_last_update')} ({_('lbl_turkey_time')}): "
                    f"{timestamp_text}"
                )
            )
            self._sc(ts, "ts-lbl")
            ts.set_halign(Gtk.Align.END)
            ts.set_margin_end(12)
            self.content.pack_start(ts, False, False, 0)

        # ── Uyarılar ──
        if self._language == "tr":
            aktif_mgm = []
            for alert in alarmlar if isinstance(alarmlar, list) else []:
                if not isinstance(alert, dict):
                    continue
                if il and self._mgm_alert_matches_city(alert, il):
                    aktif_mgm.append(alert)
            aktif_ma = WeatherAPI.meteoalerts_for_center(
                meteoalarm, merkez.get("merkezId")
            )
            if aktif_mgm or aktif_ma:
                self._section_title("⚠  AKTİF UYARILAR (Kaynak: MGM)")
                for a in aktif_mgm[:4]:
                    self._add_alert_row(a.get("baslik", ""))
                for ma in aktif_ma[:2]:
                    level_number = {"yellow": "2", "orange": "3", "red": "4"}.get(
                        ma["level"], "1"
                    )
                    severity = METEOALARM_SEVIYE.get(level_number, "")
                    self._add_alert_row(
                        f"{severity} — {ma['description']}\nMeteoAlarm"
                    )

        # ── Saatlik tahmin ──
        if self._show_saatlik:
            if self._language == "tr" and mgm_tahminler:
                self._render_hourly_mgm(mgm_tahminler)
            elif om_times:
                self._render_hourly_om(om_hourly, om_times)

        # ── Günlük tahmin ──
        if self._show_gunluk:
            if self._language == "tr" and not use_om and gd:
                self._render_daily_mgm(gd)
            elif om_data.get("daily"):
                self._render_daily_om(om_data["daily"])

        # ── Finans bölümü (ana pencere) ──
        if self._show_finance and not self._is_compact:
            with self.finance_api._lock:
                fin_rates = dict(self.finance_api._data)
            self._render_finance_main(fin_rates)

        self.compact_content.show_all()
        if not self._is_compact:
            self.content.show_all()
        return False

    # ──────────────────── Finans Render ────────────────────────────────────
    def _render_finance_widget(self, rates):
        """Widget modunda mini finans satırı"""
        # Öncelikli olarak Gram Altın, Dolar ve Euro'yu göster (Kullanıcı seçmişse)
        codes = []
        if "GRA" in self._fin_altin:
            codes.append("GRA")
        if "USD" in self._fin_doviz:
            codes.append("USD")
        if "EUR" in self._fin_doviz:
            codes.append("EUR")

        # Seçili olan diğerlerini de boşluk kalırsa ekle (Maksimum 5 öğe)
        for c in self._fin_altin + self._fin_doviz:
            if c not in codes and len(codes) < 5:
                codes.append(c)

        if not codes:
            return

        wfin = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        wfin.get_style_context().add_class("wfin-box")
        wfin.set_halign(Gtk.Align.FILL)
        wfin.set_margin_start(8)
        wfin.set_margin_end(8)
        wfin.set_margin_bottom(4)

        shown = 0
        for kod in codes:
            if kod not in rates:
                continue
            r = rates[kod]
            price = r.get("Buying") or r.get("Selling") or r.get("TRY_Price")
            if price is None:
                continue
            _dummy = r.get("Change", 0) or 0
            if kod == "USD":
                short_name = "ABD Doları"
            elif kod == "EUR":
                short_name = "Euro"
            elif kod == "GRA":
                short_name = "Gram Altın"
            else:
                short_name = (ALTIN_KODLAR.get(kod, DOVIZ_KODLAR.get(kod, kod)))[:10]

            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            col.set_halign(Gtk.Align.CENTER)

            hdr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            hdr_box.set_halign(Gtk.Align.CENTER)

            # Altın/Döviz flag SVG
            flag = get_svg_image(kod.lower(), size=16, folder="flags")
            if not flag:
                # Altın veya bayrağı olmayan para birimi için fallback
                fallback_icon = (
                    "view-list-symbolic" if kod in ALTIN_KODLAR else "money-symbolic"
                )
                flag = Gtk.Image.new_from_icon_name(fallback_icon, Gtk.IconSize.MENU)

            nm = Gtk.Label(label=short_name)
            nm.get_style_context().add_class("wfin-item")
            hdr_box.pack_start(flag, False, False, 0)
            hdr_box.pack_start(nm, False, False, 0)

            # Değişim (Yüzde)
            change = r.get("Change", 0) or 0
            try:
                chg_f = float(str(change).replace("%", "").replace(",", "."))
            except ValueError:
                chg_f = 0.0
            sign = "+" if chg_f > 0 else ""
            color = "#3fb950" if chg_f > 0 else ("#f85149" if chg_f < 0 else "gray")

            p_lbl = f"{price:,.0f}₺" if price >= 1 else f"{price:.4f}₺"
            vl = Gtk.Label()
            vl.set_markup(
                f"{p_lbl} <span color='{color}' font_size='10000'>{sign}{chg_f:.1f}%</span>"
            )
            vl.get_style_context().add_class("wfin-val")
            col.pack_start(hdr_box, False, False, 0)
            col.pack_start(vl, False, False, 0)
            wfin.pack_start(col, True, True, 0)
            shown += 1

        # Portföy P&L özeti
        if self._portfolio:
            _dummy1, cur, pnl, pnl_pct, _dummy2 = self._calc_portfolio_pnl()
            if pnl is not None:
                sep = Gtk.Label(label="│")
                sep.get_style_context().add_class("wfin-item")
                wfin.pack_start(sep, False, False, 0)
                sign = "+" if pnl >= 0 else ""
                color = "#3fb950" if pnl >= 0 else "#f85149"
                pnl_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                pnl_col.set_halign(Gtk.Align.CENTER)
                pl = Gtk.Label(label="Portföy")
                pl.get_style_context().add_class("wfin-item")
                pv = Gtk.Label()
                pv.set_markup(
                    f"<span color='{color}'><b>{sign}{pnl_pct:.1f}%</b></span>"
                )
                pv.set_use_markup(True)
                pnl_col.pack_start(pl, False, False, 0)
                pnl_col.pack_start(pv, False, False, 0)
                wfin.pack_start(pnl_col, False, False, 0)

        # Son Güncelleme Saati
        sep2 = Gtk.Label(label="│")
        sep2.get_style_context().add_class("wfin-item")
        wfin.pack_start(sep2, False, False, 0)

        ts_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        ts_col.set_halign(Gtk.Align.CENTER)
        ts_lbl1 = Gtk.Label(label="Son Veri")
        ts_lbl1.get_style_context().add_class("wfin-item")
        if self.finance_api._last_fetch > 0:
            if (
                hasattr(self.finance_api, "_update_date")
                and self.finance_api._update_date
            ):
                try:
                    dt = datetime.strptime(
                        self.finance_api._update_date, "%Y-%m-%d %H:%M:%S"
                    )
                    ts_str = dt.strftime("%d.%m %H:%M")
                except:
                    ts_str = self.finance_api._update_date[-5:]
            else:
                ts_str = datetime.fromtimestamp(self.finance_api._last_fetch).strftime(
                    "%H:%M"
                )
        else:
            ts_str = "—"
        ts_lbl2 = Gtk.Label()
        ts_lbl2.set_markup(f"<span font_size='10000'>{ts_str}</span>")
        ts_lbl2.get_style_context().add_class("wfin-val")
        ts_col.pack_start(ts_lbl1, False, False, 0)
        ts_col.pack_start(ts_lbl2, False, False, 0)
        wfin.pack_start(ts_col, False, False, 0)

        if shown > 0:
            self.compact_content.pack_start(wfin, False, False, 0)

    def _render_finance_main(self, rates):
        old_section = self._finance_section
        if old_section is not None and old_section.get_parent() is self.content:
            self.content.remove(old_section)

        self._finance_section = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0
        )
        self.content.pack_start(self._finance_section, False, False, 0)
        parent_content = self.content
        self.content = self._finance_section
        try:
            self._render_finance_content(rates)
        finally:
            self.content = parent_content

    def _render_finance_content(self, rates):
        """Ana pencerede tam finans bölümü"""
        # ── Bölüm başlığı + Yenile butonu ──
        sec_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sec_row.set_margin_start(12)
        sec_row.set_margin_end(12)
        sec_row.set_margin_top(14)
        sec_lbl = Gtk.Label(label="💰  FİNANS (Truncgil Finance)")
        self._sc(sec_lbl, "sec-title")
        sec_lbl.set_halign(Gtk.Align.START)
        sec_row.pack_start(sec_lbl, True, True, 0)

        # Timestamp etiketi
        ts_lbl = Gtk.Label()
        self._sc(ts_lbl, "ts-lbl")
        ts_lbl.set_halign(Gtk.Align.END)
        if self.finance_api._last_fetch > 0:
            if (
                hasattr(self.finance_api, "_update_date")
                and self.finance_api._update_date
            ):
                # "2026-08-05 19:16:04" formatında geliyor, Türkçeye çevirelim
                try:
                    dt = datetime.strptime(
                        self.finance_api._update_date, "%Y-%m-%d %H:%M:%S"
                    )
                    ts_str = dt.strftime("%d.%m.%Y %H:%M:%S")
                except:
                    ts_str = self.finance_api._update_date
            else:
                ts_str = datetime.fromtimestamp(self.finance_api._last_fetch).strftime(
                    "%d.%m.%Y %H:%M:%S"
                )
            ts_lbl.set_text(f"🕐 Son Güncelleme: {ts_str}")
        else:
            ts_lbl.set_text("🕐 —")
        sec_row.pack_start(ts_lbl, False, False, 0)

        # Yenile butonu
        btn_ref = Gtk.Button(label="🔄 Yenile")
        self._sc(btn_ref, "btn-fin")
        btn_ref.set_tooltip_text(
            f"Finans verilerini şimdi yenile\n"
            f"(Min. yenileme: {FINANCE_CACHE_TTL} sn — "
            f"son istek atılmayacak)"
        )

        btn_ref.connect("clicked", self._force_finance_refresh)
        sec_row.pack_start(btn_ref, False, False, 0)
        self.content.pack_start(sec_row, False, False, 0)

        if not rates:
            loading = Gtk.Label(label="⏳ Finans verileri yükleniyor…")
            loading.get_style_context().add_class("status-lbl")
            loading.set_margin_start(12)
            self.content.pack_start(loading, False, False, 0)
            return

        # ── Altın bölümü ──
        altin_kodlar = [k for k in self._fin_altin if k in rates]
        if altin_kodlar:
            fin_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            fin_card.get_style_context().add_class("fin-card")
            title_lbl = Gtk.Label(label="🪙 ALTIN PİYASASI")
            title_lbl.get_style_context().add_class("fin-title")
            title_lbl.set_halign(Gtk.Align.START)
            fin_card.pack_start(title_lbl, False, False, 0)
            for kod in altin_kodlar:
                self._add_fin_row(
                    fin_card,
                    kod,
                    rates[kod],
                    ALTIN_EMOJIS.get(kod, "🪙"),
                    ALTIN_KODLAR.get(kod, kod),
                )
            self.content.pack_start(fin_card, False, False, 0)

        # ── Döviz bölümü ──
        doviz_kodlar = [k for k in self._fin_doviz if k in rates]
        if doviz_kodlar:
            fin_card2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            fin_card2.get_style_context().add_class("fin-card")
            title_lbl2 = Gtk.Label(label="💱 DÖVİZ KURLARI")
            title_lbl2.get_style_context().add_class("fin-title")
            title_lbl2.set_halign(Gtk.Align.START)
            fin_card2.pack_start(title_lbl2, False, False, 0)
            for kod in doviz_kodlar:
                self._add_fin_row(
                    fin_card2,
                    kod,
                    rates[kod],
                    DOVIZ_EMOJIS.get(kod, "🏳"),
                    DOVIZ_KODLAR.get(kod, kod),
                )
            self.content.pack_start(fin_card2, False, False, 0)

        # ── Portföy özeti ──
        if self._portfolio:
            self._render_portfolio_summary()

    def _add_fin_row(self, container, kod, rate_data, emoji, name):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.get_style_context().add_class("fin-row")

        name_lbl = Gtk.Label(label=f"{emoji} {name}")
        name_lbl.get_style_context().add_class("fin-name")
        name_lbl.set_halign(Gtk.Align.START)
        row.pack_start(name_lbl, True, True, 0)

        buying = rate_data.get("Buying")
        selling = rate_data.get("Selling")
        change = rate_data.get("Change", 0) or 0

        if buying is not None and buying > 0:
            price_str = f"{buying:,.2f} ₺" if buying >= 1 else f"{buying:.6f} ₺"
        elif selling is not None and selling > 0:
            price_str = f"{selling:,.2f} ₺" if selling >= 1 else f"{selling:.6f} ₺"
        else:
            price_str = "—"

        price_lbl = Gtk.Label(label=price_str)
        price_lbl.get_style_context().add_class("fin-price")
        row.pack_start(price_lbl, False, False, 0)

        # Değişim yüzdesi
        if change != 0:
            sign = "+" if change > 0 else ""
            cls = "fin-change-pos" if change > 0 else "fin-change-neg"
        else:
            sign, cls = "", "fin-change-neu"
        chg_lbl = Gtk.Label(label=f"{sign}{change:.2f}%")
        chg_lbl.get_style_context().add_class(cls)
        row.pack_start(chg_lbl, False, False, 0)

        container.pack_start(row, False, False, 0)

    def _render_portfolio_summary(self):
        """Ana pencerede portföy özet kartı"""
        tc, cur, pnl, pnl_pct, details = self._calc_portfolio_pnl()
        if not details:
            return

        pf_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        pf_card.get_style_context().add_class("fin-card")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pf_title = Gtk.Label(label="📊 PORTFÖYÜm")
        pf_title.get_style_context().add_class("fin-title")
        pf_title.set_halign(Gtk.Align.START)
        header.pack_start(pf_title, True, True, 0)

        if pnl is not None:
            sign = "+" if pnl >= 0 else ""
            color = "#3fb950" if pnl >= 0 else "#f85149"
            pnl_lbl = Gtk.Label()
            pnl_lbl.set_markup(
                f"<span color='{color}'><b>{sign}{fmt_try(pnl)} ({fmt_pct(pnl_pct)})</b></span>"
            )
            pnl_lbl.set_use_markup(True)
            header.pack_start(pnl_lbl, False, False, 0)
        pf_card.pack_start(header, False, False, 0)

        for d in details:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row.get_style_context().add_class("fin-row")
            nm = Gtk.Label(label=f"{d['name']} × {d['amount']:.4g}")
            nm.get_style_context().add_class("fin-name")
            nm.set_halign(Gtk.Align.START)
            row.pack_start(nm, True, True, 0)
            if d["cur_price"] is not None:
                cv = Gtk.Label(label=fmt_try(d["current"]))
                cv.get_style_context().add_class("fin-price")
                row.pack_start(cv, False, False, 0)
                sign = "+" if d["pnl"] >= 0 else ""
                cls = "fin-change-pos" if d["pnl"] >= 0 else "fin-change-neg"
                pl = Gtk.Label(label=f"{sign}{fmt_pct(d['pnl_pct'])}")
                pl.get_style_context().add_class(cls)
                row.pack_start(pl, False, False, 0)
            else:
                na = Gtk.Label(label="Fiyat bekleniyor")
                na.get_style_context().add_class("fin-change-neu")
                row.pack_start(na, False, False, 0)
            pf_card.pack_start(row, False, False, 0)

        btn_manage = Gtk.Button(label="✏️ Portföyü Düzenle")
        self._sc(btn_manage, "btn-fin")
        btn_manage.set_halign(Gtk.Align.END)
        btn_manage.connect("clicked", self._show_portfolio_dialog)
        pf_card.pack_start(btn_manage, False, False, 0)

        self.content.pack_start(pf_card, False, False, 0)

    # ──────────────────── Saatlik / Günlük Tahmin ──────────────────────────
    def _render_hourly_mgm(self, tahminler):
        self._section_title(_("🕐  SAATLİK TAHMİN (Kaynak: MGM + Open-Meteo)"))
        hs = self._make_hscroll()
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        h_box.set_margin_bottom(4)
        for item in tahminler[:16]:
            hc = self._make_hcard()
            h_str = fmt_time(item.get("tarih", ""))
            h_int = int(h_str.split(":")[0]) if ":" in h_str else 12
            tl = Gtk.Label(label=h_str)
            self._sc(tl, "h-time")
            tl.set_halign(Gtk.Align.CENTER)
            em, ks, uz = hadise_mgm(item.get("hadise", ""), (h_int < 6 or h_int >= 19))
            el = get_svg_image(em, size=32)
            el.set_halign(Gtk.Align.CENTER)
            if uz:
                el.set_tooltip_text(f"{ks}\n{uz}")
            ttl = Gtk.Label(label=val(item.get("sicaklik", -9999), suffix="°"))
            self._sc(ttl, "h-temp")
            ttl.set_halign(Gtk.Align.CENTER)
            c_lbl = Gtk.Label(label=ks)
            self._sc(c_lbl, "h-wind")
            c_lbl.set_halign(Gtk.Align.CENTER)
            c_lbl.set_line_wrap(True)
            c_lbl.set_justify(Gtk.Justification.CENTER)
            c_lbl.set_max_width_chars(12)
            rh = item.get("ruzgarHizi", -9999)
            wl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
            wl_box.set_halign(Gtk.Align.CENTER)
            if rh not in (-9999, None):
                wl_ic = get_svg_image("wind", size=14, folder="pills")
                wl_lbl = Gtk.Label(label=self._format_wind(rh))
                self._sc(wl_lbl, "h-wind")
                wl_box.pack_start(wl_ic, False, False, 0)
                wl_box.pack_start(wl_lbl, False, False, 0)

            hc.pack_start(tl, False, False, 0)
            hc.pack_start(el, False, False, 0)
            hc.pack_start(ttl, False, False, 0)
            hc.pack_start(c_lbl, False, False, 0)
            hc.pack_start(wl_box, False, False, 0)
            max_wind = item.get("maksimumRuzgarHizi", -9999)
            if max_wind not in (-9999, None):
                gust_lbl = Gtk.Label(label=f"↗ {self._format_wind(max_wind)}")
                self._sc(gust_lbl, "w3-nem")
                gust_lbl.set_tooltip_text(_("lbl_wind_gust"))
                hc.pack_start(gust_lbl, False, False, 0)
            h_box.pack_start(hc, False, False, 0)
        hs.add(h_box)
        self.content.pack_start(hs, False, False, 0)

    def _render_hourly_om(self, om_hourly, om_times):
        self._section_title(_("🕐  SAATLİK TAHMİN (Kaynak: Open-Meteo)"))
        hs = self._make_hscroll()
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        h_box.set_margin_bottom(4)
        temps = om_hourly.get("temperature_2m", [])
        winds = om_hourly.get("wind_speed_10m", [])
        wcodes = om_hourly.get("weather_code", [])
        probs = om_hourly.get("precipitation_probability", [])
        now_h = datetime.now().strftime("%Y-%m-%dT%H:")
        start = next((i for i, t in enumerate(om_times) if t.startswith(now_h[:13])), 0)
        for i in range(start, min(start + 24, len(om_times))):
            hc = self._make_hcard()
            try:
                t_str = om_times[i][11:16]
            except (IndexError, TypeError):
                t_str = "--"
            tl = Gtk.Label(label=t_str)
            self._sc(tl, "h-time")
            tl.set_halign(Gtk.Align.CENTER)
            is_night_h = (
                (om_hourly.get("is_day", [])[i] == 0)
                if i < len(om_hourly.get("is_day", []))
                else False
            )
            em, ks, uz = hadise_wmo(wcodes[i] if i < len(wcodes) else None, is_night_h)
            el = get_svg_image(em, size=32)
            el.set_halign(Gtk.Align.CENTER)
            if uz:
                el.set_tooltip_text(f"{ks}\n{uz}")
            tmp = temps[i] if i < len(temps) else -9999
            ttl = Gtk.Label(label=val(tmp, suffix="°"))
            self._sc(ttl, "h-temp")
            ttl.set_halign(Gtk.Align.CENTER)
            c_lbl = Gtk.Label(label=ks)
            self._sc(c_lbl, "h-wind")
            c_lbl.set_halign(Gtk.Align.CENTER)
            c_lbl.set_line_wrap(True)
            c_lbl.set_justify(Gtk.Justification.CENTER)
            c_lbl.set_max_width_chars(12)
            wsp = winds[i] if i < len(winds) else -9999
            wl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
            wl_box.set_halign(Gtk.Align.CENTER)
            if wsp not in (-9999, None):
                wl_ic = get_svg_image("wind", size=14, folder="pills")
                wl_lbl = Gtk.Label(label=self._format_wind(wsp))
                self._sc(wl_lbl, "h-wind")
                wl_box.pack_start(wl_ic, False, False, 0)
                wl_box.pack_start(wl_lbl, False, False, 0)

            hc.pack_start(tl, False, False, 0)
            hc.pack_start(el, False, False, 0)
            hc.pack_start(ttl, False, False, 0)
            hc.pack_start(c_lbl, False, False, 0)
            hc.pack_start(wl_box, False, False, 0)
            if i < len(probs) and probs[i] is not None:
                pl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
                pl_box.set_halign(Gtk.Align.CENTER)
                pl_ic = get_svg_image("droplet", size=14, folder="pills")
                pl_lbl = Gtk.Label(label=f"%{probs[i]:.0f}")
                self._sc(pl_lbl, "h-wind")
                pl_box.pack_start(pl_ic, False, False, 0)
                pl_box.pack_start(pl_lbl, False, False, 0)
                hc.pack_start(pl_box, False, False, 0)
            h_box.pack_start(hc, False, False, 0)
        hs.add(h_box)
        self.content.pack_start(hs, False, False, 0)

    def _render_daily_mgm(self, gd):
        self._section_title(_("📅  5 GÜNLÜK TAHMİN (Kaynak: MGM + Open-Meteo)"))
        fc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fc_box.set_margin_bottom(20)
        for i in range(1, 6):
            tarih = gd.get(f"tarihGun{i}")
            if not tarih:
                continue
            outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            self._sc(outer, "fc-row")
            top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            dl = Gtk.Label(label=fmt_date(tarih))
            self._sc(dl, "fc-day")
            dl.set_halign(Gtk.Align.START)
            em, ksa, uzn = hadise_mgm(gd.get(f"hadiseGun{i}", ""))
            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=32)
            c_lb = Gtk.Label(label=ksa)
            self._sc(c_lb, "fc-cond")
            cl.pack_start(c_ic, False, False, 0)
            cl.pack_start(c_lb, False, False, 0)
            cl.set_halign(Gtk.Align.START)
            if uzn:
                cl.set_tooltip_text(uzn)
            rh2 = gd.get(f"ruzgarHizGun{i}", -9999)
            rl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            rl_box.set_halign(Gtk.Align.END)
            if rh2 not in (-9999, None):
                rl_ic = get_svg_image("wind", size=16, folder="pills")
                rl_lbl = Gtk.Label(label=self._format_wind(rh2))
                self._sc(rl_lbl, "fc-cond")
                rl_box.pack_start(rl_ic, False, False, 0)
                rl_box.pack_start(rl_lbl, False, False, 0)
            tb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            hl = Gtk.Label(label=val(gd.get(f"enYuksekGun{i}", -9999), suffix="°"))
            self._sc(hl, "fc-hi")
            ll = Gtk.Label(label=val(gd.get(f"enDusukGun{i}", -9999), suffix="°"))
            self._sc(ll, "fc-lo")
            tb.pack_start(hl, False, False, 0)
            tb.pack_start(ll, False, False, 0)
            top_row.pack_start(dl, False, False, 0)
            top_row.pack_start(cl, True, True, 0)
            top_row.pack_start(rl_box, False, False, 0)
            top_row.pack_start(tb, False, False, 0)
            outer.pack_start(top_row, False, False, 0)
            if uzn:
                dl2 = Gtk.Label(label=uzn)
                self._sc(dl2, "fc-desc")
                dl2.set_halign(Gtk.Align.START)
                dl2.set_line_wrap(True)
                dl2.set_max_width_chars(60)
                outer.pack_start(dl2, False, False, 0)
            fc_box.pack_start(outer, False, False, 0)
        self.content.pack_start(fc_box, False, False, 0)

    def _render_daily_om(self, daily):
        self._section_title(_("📅  5 GÜNLÜK TAHMİN (Kaynak: Open-Meteo)"))
        fc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fc_box.set_margin_bottom(20)
        dates = daily.get("time", [])
        hi_arr = daily.get("temperature_2m_max", [])
        lo_arr = daily.get("temperature_2m_min", [])
        wc_arr = daily.get("weather_code", [])
        rh_arr = daily.get("wind_speed_10m_max", [])
        pr_arr = daily.get("precipitation_sum", [])
        pp_arr = daily.get("precipitation_probability_max", [])
        uv_arr = daily.get("uv_index_max", [])
        for i, tarih in enumerate(dates[:5]):
            outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            self._sc(outer, "fc-row")
            top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            try:
                dt_fmt = fmt_date(tarih + "T00:00:00")
            except (ValueError, TypeError):
                dt_fmt = tarih
            dl = Gtk.Label(label=dt_fmt)
            self._sc(dl, "fc-day")
            dl.set_halign(Gtk.Align.START)
            em, ksa, uzn = hadise_wmo(wc_arr[i] if i < len(wc_arr) else None)
            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=32)
            c_lb = Gtk.Label(label=ksa)
            self._sc(c_lb, "fc-cond")
            cl.pack_start(c_ic, False, False, 0)
            cl.pack_start(c_lb, False, False, 0)
            cl.set_halign(Gtk.Align.START)
            if uzn:
                cl.set_tooltip_text(uzn)
            rh2 = rh_arr[i] if i < len(rh_arr) else None
            rl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            rl_box.set_halign(Gtk.Align.END)
            if rh2 is not None:
                rl_ic = get_svg_image("wind", size=16, folder="pills")
                rl_lbl = Gtk.Label(label=self._format_wind(rh2))
                self._sc(rl_lbl, "fc-cond")
                rl_box.pack_start(rl_ic, False, False, 0)
                rl_box.pack_start(rl_lbl, False, False, 0)
            tb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            hl = Gtk.Label(
                label=val(hi_arr[i] if i < len(hi_arr) else -9999, suffix="°")
            )
            self._sc(hl, "fc-hi")
            ll = Gtk.Label(
                label=val(lo_arr[i] if i < len(lo_arr) else -9999, suffix="°")
            )
            self._sc(ll, "fc-lo")
            tb.pack_start(hl, False, False, 0)
            tb.pack_start(ll, False, False, 0)
            top_row.pack_start(dl, False, False, 0)
            top_row.pack_start(cl, True, True, 0)
            top_row.pack_start(rl_box, False, False, 0)
            top_row.pack_start(tb, False, False, 0)
            outer.pack_start(top_row, False, False, 0)
            pr = pr_arr[i] if i < len(pr_arr) else None
            pp = pp_arr[i] if i < len(pp_arr) else None
            uv = uv_arr[i] if i < len(uv_arr) else None
            if pr is not None or pp is not None or uv is not None:
                ex_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                ex_box.set_halign(Gtk.Align.START)

                def add_extra(icon_name, text):
                    b = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
                    ic = get_svg_image(icon_name, size=14, folder="pills")
                    lb = Gtk.Label(label=text)
                    self._sc(lb, "fc-desc")
                    b.pack_start(ic, False, False, 0)
                    b.pack_start(lb, False, False, 0)
                    ex_box.pack_start(b, False, False, 0)

                if pr is not None and pr > 0:
                    add_extra("cloud-rain", f"{pr:.1f} mm")
                if pp is not None:
                    add_extra("umbrella", f"%{pp:.0f}")
                if uv is not None:
                    add_extra("sun", f"UV {uv:.1f}")

                ex_box.set_tooltip_text(
                    "Yağış (mm) / Yağış olasılığı (%) / UV İndeksi maks"
                )
                outer.pack_start(ex_box, False, False, 0)
            fc_box.pack_start(outer, False, False, 0)
        self.content.pack_start(fc_box, False, False, 0)

    # ──────────────────── Yardımcı render ─────────────────────────────────
    def _make_hscroll(self):
        hs = Gtk.ScrolledWindow()
        hs.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        hs.set_min_content_height(int(165 * self._get_scale()))
        hs.set_margin_start(12)
        hs.set_margin_end(12)
        return hs

    def _make_hcard(self):
        hc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._sc(hc, "h-card")
        hc.set_halign(Gtk.Align.CENTER)
        return hc

    def _add_alert_row(self, metin):
        arow = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._sc(arow, "alert-row")
        lbl = Gtk.Label(label=metin)
        self._sc(lbl, "alert-txt")
        lbl.set_halign(Gtk.Align.START)
        lbl.set_line_wrap(True)
        lbl.set_max_width_chars(55)
        arow.pack_start(lbl, False, False, 0)
        self.content.pack_start(arow, False, False, 0)
