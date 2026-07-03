import os
import re

utils_file = "/home/turan/Belgeler/mintsky/mintsky/utils.py"
with open(utils_file, "r") as f:
    code = f.read()

code = code.replace('return EMOJI_TO_SVG.get(icon, "unknown"), _(label), _(desc)', 'return icon, _(label), _(desc)')

with open(utils_file, "w") as f:
    f.write(code)

app_file = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(app_file, "r") as f:
    code = f.read()

# 1. Main Weather Icon
old_main = '''        cond = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        c_icon = get_svg_image(emoji, size=56)
        c_lbl = Gtk.Label(label=kisa); self._sc(c_lbl,"cur-cond")
        cond.pack_start(c_icon, False, False, 0)
        cond.pack_start(c_lbl, False, False, 0)
        cond.set_halign(Gtk.Align.START)'''
new_main = '''        cond = Gtk.Label()
        cond.set_markup(f"<span size='35000'>{emoji}</span>  <span size='15000'>{kisa}</span>")
        self._sc(cond,"cur-cond"); cond.set_halign(Gtk.Align.START)'''
code = code.replace(old_main, new_main)

# 2. Hourly Forecast 
old_hourly = '''            el = get_svg_image(em, size=32); el.set_halign(Gtk.Align.CENTER)'''
new_hourly = '''            el = Gtk.Label()
            el.set_markup(f"<span size='20000'>{em}</span>")
            self._sc(el,"h-emoji"); el.set_halign(Gtk.Align.CENTER)'''
code = code.replace(old_hourly, new_hourly)

# 3. Daily Forecast (MGM)
old_mgm_daily = '''            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=20)
            c_lbl = Gtk.Label(label=ksa); self._sc(c_lbl,"fc-cond")
            cl.pack_start(c_ic, False, False, 0); cl.pack_start(c_lbl, False, False, 0)
            cl.set_halign(Gtk.Align.START)'''
new_mgm_daily = '''            cl = Gtk.Label()
            cl.set_markup(f"<span size='12000'>{em}</span>  {ksa}")
            self._sc(cl,"fc-cond"); cl.set_halign(Gtk.Align.START)'''
code = code.replace(old_mgm_daily, new_mgm_daily)

old_mgm_daily_2 = '''            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=20)
            c_lb = Gtk.Label(label=ksa); self._sc(c_lb,"fc-cond")
            cl.pack_start(c_ic, False, False, 0); cl.pack_start(c_lb, False, False, 0)
            cl.set_halign(Gtk.Align.START)'''
code = code.replace(old_mgm_daily_2, new_mgm_daily)

# 4. Daily Forecast (OM)
old_om_daily = '''            cl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            c_ic = get_svg_image(em, size=20)
            c_lbl = Gtk.Label(label=ksa); self._sc(c_lbl,"fc-cond")
            cl.pack_start(c_ic, False, False, 0); cl.pack_start(c_lbl, False, False, 0)
            cl.set_halign(Gtk.Align.START)'''
code = code.replace(old_om_daily, new_mgm_daily)

with open(app_file, "w") as f:
    f.write(code)

print("Reverted SVGs back to Emojis with GTK Markup scaling.")
