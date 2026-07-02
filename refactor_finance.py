import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"

with open(file_path, "r") as f:
    code = f.read()

# Replace _add_fin_row
code = code.replace(
"""    def _add_fin_row(self, container, kod, rate_data, emoji, name):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.get_style_context().add_class("fin-row")

        name_lbl = Gtk.Label(label=f"{emoji} {name}")
        name_lbl.get_style_context().add_class("fin-name")
        name_lbl.set_halign(Gtk.Align.START)
        row.pack_start(name_lbl, True, True, 0)""",
"""    def _add_fin_row(self, container, kod, rate_data, emoji, name):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.get_style_context().add_class("fin-row")

        if kod in DOVIZ_KODLAR:
            icon = get_svg_image(kod.lower(), size=16, folder="flags")
        else:
            icon = Gtk.Label(label=emoji)
        
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        name_box.pack_start(icon, False, False, 0)
        
        name_lbl = Gtk.Label(label=name)
        name_lbl.get_style_context().add_class("fin-name")
        name_lbl.set_halign(Gtk.Align.START)
        name_box.pack_start(name_lbl, False, False, 0)
        row.pack_start(name_box, True, True, 0)""")

with open(file_path, "w") as f:
    f.write(code)

print("Done refactoring finance rows.")
