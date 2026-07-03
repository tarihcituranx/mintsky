import os
import re

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fix Hourly Forecast SVGs
code = code.replace('el = Gtk.Label(label=em); self._sc(el,"h-emoji")', 'el = get_svg_image(em, size=24)')

# 2. Fix Tray Menu Data passing
code = code.replace('def _apply_tray_data(self, emoji, temp_txt, sehir, icon_key, kisa_desc):',
                    'def _apply_tray_data(self, emoji, temp_txt, sehir, icon_key, kisa_desc, s_data=None):\n        self._last_s_data = s_data')
code = code.replace('self._apply_tray_data(emoji, ttxt, sehir, h_kod_for_tray, kisa)',
                    'self._apply_tray_data(emoji, ttxt, sehir, h_kod_for_tray, kisa, s_data)')
code = code.replace('GLib.idle_add(self._apply_tray_data, emoji, ttxt, sehir, h_kod, kisa)',
                    'GLib.idle_add(self._apply_tray_data, emoji, ttxt, sehir, h_kod, kisa, s_data)')

# 3. Add details to Tray Menu
old_tray_menu = """    def _build_tray_menu(self):
        menu = Gtk.Menu()
        show = Gtk.MenuItem.new_with_label(f"🪟 {_('tray_show_hide')}")"""
new_tray_menu = """    def _build_tray_menu(self):
        menu = Gtk.Menu()
        if hasattr(self, "_last_s_data") and self._last_s_data:
            s = self._last_s_data
            if "nem" in s:
                nem = s.get("nem", "-")
                ruzgar = s.get("ruzgarHizi", "-")
                hissedilen = s.get("hissedilenSicaklik", s.get("sicaklik", "-"))
                
                m1 = Gtk.MenuItem.new_with_label(f"🌡️ Hissedilen: {hissedilen}°")
                m1.set_sensitive(False); menu.append(m1)
                
                m2 = Gtk.MenuItem.new_with_label(f"💧 Nem: %{nem}")
                m2.set_sensitive(False); menu.append(m2)
                
                m3 = Gtk.MenuItem.new_with_label(f"🌬️ Rüzgar: {ruzgar} km/s")
                m3.set_sensitive(False); menu.append(m3)
                
                menu.append(Gtk.SeparatorMenuItem())
                
        show = Gtk.MenuItem.new_with_label(f"🪟 {_('tray_show_hide')}")"""
code = code.replace(old_tray_menu, new_tray_menu)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)
print("app.py successfully manually patched.")
