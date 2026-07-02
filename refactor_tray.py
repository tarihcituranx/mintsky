import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"

with open(file_path, "r") as f:
    code = f.read()

old_menu = """    def _build_tray_menu(self):
        menu = Gtk.Menu()
        show = Gtk.MenuItem.new_with_label("🪟 Pencereyi Göster / Gizle")
        show.connect("activate", self._tray_toggle); menu.append(show)
        
        refresh = Gtk.MenuItem.new_with_label("🌤️ Hava Durumunu Yenile")
        refresh.connect("activate", lambda *_: self._search(force=True))
        menu.append(refresh)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        if self._show_finance:
            fin_item = Gtk.MenuItem.new_with_label("💰 Finans & Portföy")
            fin_item.connect("activate", self._show_portfolio_dialog)
            menu.append(fin_item)
            menu.append(Gtk.SeparatorMenuItem())
            
        update_chk = Gtk.MenuItem.new_with_label("🔄 Güncellemeleri Denetle")
        update_chk.connect("activate", lambda *_: self._check_for_updates_bg(forced=True))
        menu.append(update_chk)
        
        ab = Gtk.MenuItem.new_with_label("ℹ️ Hakkında")
        ab.connect("activate", self._show_about)
        menu.append(ab)
        
        q  = Gtk.MenuItem.new_with_label("❌ Çıkış")
        q.connect("activate",  self._quit)
        menu.append(q)
        
        menu.show_all()
        return menu"""

new_menu = """    def _build_tray_menu(self):
        menu = Gtk.Menu()
        
        def make_item(label, icon_name, callback=None, bold=False):
            item = Gtk.MenuItem()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
            lbl = Gtk.Label(label=label)
            lbl.set_halign(Gtk.Align.START)
            if bold:
                lbl.set_markup(f"<b>{label}</b>")
            box.pack_start(img, False, False, 0)
            box.pack_start(lbl, False, False, 0)
            item.add(box)
            if callback:
                item.connect("activate", callback)
            else:
                item.set_sensitive(False)
            return item

        # App Title Item (Inactive)
        title = make_item(f"MintSky v{VERSIYON}", "weather-few-clouds-symbolic", bold=True)
        menu.append(title)
        menu.append(Gtk.SeparatorMenuItem())

        show = make_item("Pencereyi Göster / Gizle", "window-restore-symbolic", self._tray_toggle)
        menu.append(show)
        
        refresh = make_item("Hava Durumunu Yenile", "view-refresh-symbolic", lambda *_: self._search(force=True))
        menu.append(refresh)
        
        menu.append(Gtk.SeparatorMenuItem())
        
        if self._show_finance:
            fin_item = make_item("Finans & Portföy", "office-chart-line-symbolic", self._show_portfolio_dialog)
            menu.append(fin_item)
            menu.append(Gtk.SeparatorMenuItem())
            
        update_chk = make_item("Güncellemeleri Denetle", "system-software-update-symbolic", lambda *_: self._check_for_updates_bg(forced=True))
        menu.append(update_chk)
        
        ab = make_item("Hakkında", "help-about-symbolic", self._show_about)
        menu.append(ab)
        
        q = make_item("Çıkış", "application-exit-symbolic", self._quit)
        menu.append(q)
        
        menu.show_all()
        return menu"""

if old_menu in code:
    code = code.replace(old_menu, new_menu)
    with open(file_path, "w") as f:
        f.write(code)
    print("Tray menu refactored successfully.")
else:
    print("Could not find the old tray menu code in app.py")
