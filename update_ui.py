import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# 1. Change "Liste" to "Favorilerim"
old_list = 'self._create_tool_btn("📋","Liste","Favori listesi"'
new_list = 'self._create_tool_btn("📋","Favorilerim","Favori listelerim"'
code = code.replace(old_list, new_list)

# 2. Update Header for Version & GitHub 
old_hdr = """        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        title = Gtk.Label(label=UYGULAMA_ADI.upper())
        self._sc(title,"hdr-title"); title.set_halign(Gtk.Align.START)
        ver_lbl = Gtk.Label(label=f"<span size='small' color='#5a6a85'>v{VERSIYON}</span>")
        ver_lbl.set_use_markup(True)
        title_row.pack_start(title, False, False, 0)
        title_row.pack_start(ver_lbl, False, False, 4)
        title_row.pack_start(Gtk.Box(), True, True, 0)  # spacer"""

new_hdr = """        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title = Gtk.Label(label=UYGULAMA_ADI.upper())
        self._sc(title,"hdr-title"); title.set_halign(Gtk.Align.START)
        
        # Sürüm no (okunaklı ve açık mavi)
        ver_lbl = Gtk.Label()
        ver_lbl.set_markup(f"<span size='medium' weight='bold' color='#79c0ff'>v{VERSIYON}</span>")
        ver_lbl.set_margin_start(4)
        
        # Geliştirici (GitHub logo + isim)
        gh_icon = Gtk.Image.new_from_icon_name("github-symbolic", Gtk.IconSize.MENU)
        dev_lbl = Gtk.Label()
        dev_lbl.set_markup("<span size='small' color='#8b949e'><b>Turan Kaya</b></span>")
        
        dev_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        dev_box.set_valign(Gtk.Align.CENTER)
        dev_box.pack_start(gh_icon, False, False, 0)
        dev_box.pack_start(dev_lbl, False, False, 0)

        # Üst kısımda başlık ve sürüm, altında geliştirici
        title_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        title_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        title_top.pack_start(title, False, False, 0)
        title_top.pack_start(ver_lbl, False, False, 0)
        title_col.pack_start(title_top, False, False, 0)
        title_col.pack_start(dev_box, False, False, 0)

        title_row.pack_start(title_col, False, False, 0)
        title_row.pack_start(Gtk.Box(), True, True, 0)  # spacer"""

code = code.replace(old_hdr, new_hdr)

with open(file_path, "w") as f:
    f.write(code)

print("UI enhancements applied.")
