import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"

with open(file_path, "r") as f:
    code = f.read()

# Replace fc-cond in MGM
code = code.replace(
"""            dl  = Gtk.Label(label=fmt_date(tarih)); self._sc(dl,"fc-day"); dl.set_halign(Gtk.Align.START)
            em,ksa,uzn = hadise_mgm(gd.get(f"hadiseGun{i}",""))
            cl  = Gtk.Label(label=f"{em} {ksa}"); self._sc(cl,"fc-cond"); cl.set_halign(Gtk.Align.START)
            if uzn: cl.set_tooltip_text(uzn)""",
"""            dl  = Gtk.Label(label=fmt_date(tarih)); self._sc(dl,"fc-day"); dl.set_halign(Gtk.Align.START)
            em,ksa,uzn = hadise_mgm(gd.get(f"hadiseGun{i}",""))
            
            cl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            cl_icon = get_svg_image(em, size=20)
            cl_lbl = Gtk.Label(label=ksa); self._sc(cl_lbl,"fc-cond"); cl_lbl.set_halign(Gtk.Align.START)
            cl_box.pack_start(cl_icon, False, False, 0)
            cl_box.pack_start(cl_lbl, False, False, 0)
            if uzn: cl_box.set_tooltip_text(uzn)
            
            cl = cl_box  # rebind cl so pack_start below works""")

# Replace fc-cond in OM
code = code.replace(
"""            dl  = Gtk.Label(label=dt_fmt); self._sc(dl,"fc-day"); dl.set_halign(Gtk.Align.START)
            em,ksa,uzn = hadise_wmo(wc_arr[i] if i<len(wc_arr) else None)
            cl  = Gtk.Label(label=f"{em} {ksa}"); self._sc(cl,"fc-cond"); cl.set_halign(Gtk.Align.START)
            if uzn: cl.set_tooltip_text(uzn)""",
"""            dl  = Gtk.Label(label=dt_fmt); self._sc(dl,"fc-day"); dl.set_halign(Gtk.Align.START)
            em,ksa,uzn = hadise_wmo(wc_arr[i] if i<len(wc_arr) else None)
            
            cl_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            cl_icon = get_svg_image(em, size=20)
            cl_lbl = Gtk.Label(label=ksa); self._sc(cl_lbl,"fc-cond"); cl_lbl.set_halign(Gtk.Align.START)
            cl_box.pack_start(cl_icon, False, False, 0)
            cl_box.pack_start(cl_lbl, False, False, 0)
            if uzn: cl_box.set_tooltip_text(uzn)
            
            cl = cl_box""")

with open(file_path, "w") as f:
    f.write(code)

print("Done refactoring daily forecasts.")
