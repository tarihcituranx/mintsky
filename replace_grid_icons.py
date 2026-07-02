import os
import re

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# Replace _make_pill
old_make_pill = """    def _make_pill(self, key, value, tooltip=None):
        pill = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self._sc(pill, "pill-box")
        kl = Gtk.Label(label=key);   self._sc(kl, "pill-key"); kl.set_halign(Gtk.Align.START)
        vl = Gtk.Label(label=value); self._sc(vl, "pill-val"); vl.set_halign(Gtk.Align.START)
        pill.pack_start(kl, False, False, 0)
        pill.pack_start(vl, False, False, 0)
        tt = tooltip or PILL_TOOLTIPS.get(key)
        if tt: pill.set_has_tooltip(True); pill.set_tooltip_text(tt)
        return pill"""

new_make_pill = """    def _make_pill(self, key, value, tooltip=None, icon_name=None):
        pill = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self._sc(pill, "pill-box")
        
        k_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        if icon_name:
            if icon_name.endswith(".svg"):
                img = get_svg_image(icon_name.replace(".svg",""), size=16)
            else:
                img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
            k_box.pack_start(img, False, False, 0)
            
        kl = Gtk.Label(label=key);   self._sc(kl, "pill-key"); kl.set_halign(Gtk.Align.START)
        k_box.pack_start(kl, False, False, 0)
        
        vl = Gtk.Label(label=value); self._sc(vl, "pill-val"); vl.set_halign(Gtk.Align.START)
        
        pill.pack_start(k_box, False, False, 0)
        pill.pack_start(vl, False, False, 0)
        tt = tooltip or PILL_TOOLTIPS.get(key)
        if tt: pill.set_has_tooltip(True); pill.set_tooltip_text(tt)
        return pill"""

code = code.replace(old_make_pill, new_make_pill)

# Now replace the tuples in _render
# From: pills_temel.append(("💧 Nem", f"%{nem_val:.0f}"))
# To:   pills_temel.append(("Nem", f"%{nem_val:.0f}", "dialog-information-symbolic"))

replacements = {
    '("💧 Nem"': '("Nem"',
    '("💨 Rüzgar"': '("Rüzgar"',
    '("🔵 Basınç"': '("Basınç"',
    '("👁 Görüş"': '("Görüş"',
    '("🌧 Yağış 1s"': '("Yağış 1s"',
    '("🌧 Yağış 24s"': '("Yağış 24s"',
    '("🌊 Deniz"': '("Deniz"',
    '("☁ Bulutluluk"': '("Bulutluluk"',
    '("❄ Kar"': '("Kar"',
    '("🔆 UV İndeksi"': '("UV İndeksi"',
    '("💨 Rüzgar Gustu"': '("Rüzgar Gustu"',
    '("🌡 Çiğ Noktası"': '("Çiğ Noktası"',
    '("🌧 Yağış (anlık)"': '("Yağış (anlık)"',
    '("🌂 Yağış Olas."': '("Yağış Olas."',
    '("☀ Güneşlenme"': '("Güneşlenme"',
    '("🌅 G. Doğuşu"': '("G. Doğuşu"',
    '("🌇 G. Batışı"': '("G. Batışı"',
}

for old_str, new_str in replacements.items():
    code = code.replace(old_str, new_str)

# Now update the append calls to include the icon names
# This is tricky using string replacement, but we can map the new keys to icons in _make_pill directly!
# Let's revert the above replacements and handle it in _make_pill dynamically based on the emoji!

# Actually, the string replacement for tuples failed if I try to add the 3rd element without regex.
# Let's just modify the new_make_pill to auto-extract the emoji and map it to a system icon!

new_make_pill_auto = """    def _make_pill(self, key, value, tooltip=None):
        pill = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self._sc(pill, "pill-box")
        
        # Emoji to system icon mapping
        icon_map = {
            "💧": "weather-showers-scattered-symbolic",
            "💨": "weather-storm-symbolic",
            "🔵": "dialog-information-symbolic",
            "👁": "weather-fog-symbolic",
            "🌧": "weather-showers-symbolic",
            "🌊": "weather-storm-symbolic",
            "☁": "weather-overcast-symbolic",
            "❄": "weather-snow-symbolic",
            "🔆": "weather-clear-symbolic",
            "🌡": "dialog-warning-symbolic",
            "🌂": "weather-showers-symbolic",
            "☀": "weather-clear-symbolic",
            "🌅": "weather-clear-symbolic",
            "🌇": "weather-clear-night-symbolic",
        }
        
        k_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        clean_key = key
        
        parts = key.split(' ', 1)
        if len(parts) == 2 and len(parts[0]) <= 2 and parts[0] in icon_map:
            icon_char, title = parts
            img = Gtk.Image.new_from_icon_name(icon_map[icon_char], Gtk.IconSize.MENU)
            # Add style context to the image for nice muted colors if needed, but symbolic icons adapt automatically!
            k_box.pack_start(img, False, False, 0)
            clean_key = title
            
        kl = Gtk.Label(label=clean_key)
        self._sc(kl, "pill-key")
        kl.set_halign(Gtk.Align.START)
        k_box.pack_start(kl, False, False, 0)
        
        vl = Gtk.Label(label=value)
        self._sc(vl, "pill-val")
        vl.set_halign(Gtk.Align.START)
        
        pill.pack_start(k_box, False, False, 0)
        pill.pack_start(vl, False, False, 0)
        
        tt = tooltip or PILL_TOOLTIPS.get(key)
        if tt:
            pill.set_has_tooltip(True)
            pill.set_tooltip_text(tt)
        return pill"""

# re-read file to discard the failed replacements
with open(file_path, "r") as f:
    code = f.read()
code = code.replace(old_make_pill, new_make_pill_auto)

with open(file_path, "w") as f:
    f.write(code)

print("Icons replaced in grid via auto mapping.")
