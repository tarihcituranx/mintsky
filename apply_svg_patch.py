import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# 1. Add get_svg_image to imports
if "get_svg_image" not in code:
    old_import = "from mintsky.utils import yon, fmt_date, fmt_time, fmt_dt, val, fmt_try, fmt_pct, hadise_mgm, hadise_wmo"
    new_import = "from mintsky.utils import yon, fmt_date, fmt_time, fmt_dt, val, fmt_try, fmt_pct, hadise_mgm, hadise_wmo, get_svg_image"
    code = code.replace(old_import, new_import)

# 2. Main Weather Icon (cond)
old_cond = 'cond = Gtk.Label(label=f"{emoji}  {kisa}")\n        self._sc(cond,"cur-cond"); cond.set_halign(Gtk.Align.START)'
new_cond = '''
        cond = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        c_icon = get_svg_image(emoji, size=56)
        c_lbl = Gtk.Label(label=kisa); self._sc(c_lbl,"cur-cond")
        cond.pack_start(c_icon, False, False, 0)
        cond.pack_start(c_lbl, False, False, 0)
        cond.set_halign(Gtk.Align.START)'''
code = code.replace(old_cond, new_cond.lstrip("\n"))

# 3. 3-Hourly Forecast Icon
old_w3 = 'el = Gtk.Label(label=em);    self._sc(el,"w3-emoji"); el.set_halign(Gtk.Align.CENTER)'
new_w3 = 'el = get_svg_image(em, size=24); el.set_halign(Gtk.Align.CENTER)'
code = code.replace(old_w3, new_w3)

# 4. Daily Forecast (MGM)
old_mgm_daily = 'cl  = Gtk.Label(label=f"{em} {ksa}"); self._sc(cl,"fc-cond"); cl.set_halign(Gtk.Align.START)'
new_daily = '''
            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=20)
            c_lb = Gtk.Label(label=ksa); self._sc(c_lb,"fc-cond")
            cl.pack_start(c_ic, False, False, 0); cl.pack_start(c_lb, False, False, 0)
            cl.set_halign(Gtk.Align.START)'''
code = code.replace(old_mgm_daily, new_daily.lstrip("\n"))

# 5. Daily Forecast (OM) uses the exact same string
# Actually the code.replace will replace BOTH MGM and OM daily if they match exactly!
# Yes, they both have exactly 'cl  = Gtk.Label(label=f"{em} {ksa}"); self._sc(cl,"fc-cond"); cl.set_halign(Gtk.Align.START)'

# 6. Finance Widget Flags
old_fin = '''            hdr_box.set_halign(Gtk.Align.CENTER)
            
            nm = Gtk.Label(label=short_name)'''
new_fin = '''            hdr_box.set_halign(Gtk.Align.CENTER)
            
            flag = get_svg_image(kod.lower(), size=16, folder="flags")
            if isinstance(flag, Gtk.Label):
                fallback_icon = "view-list-symbolic" if kod in ALTIN_KODLAR else "money-symbolic"
                flag = Gtk.Image.new_from_icon_name(fallback_icon, Gtk.IconSize.MENU)
            hdr_box.pack_start(flag, False, False, 0)
            
            nm = Gtk.Label(label=short_name)'''
if 'flag = get_svg_image' not in code:
    code = code.replace(old_fin, new_fin)

with open(file_path, "w") as f:
    f.write(code)

print("SVG Graphics Revolution applied.")
