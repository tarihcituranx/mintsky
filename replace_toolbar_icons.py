import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# Replace _create_tool_btn
old_create_tool_btn = """    def _create_tool_btn(self, icon, text, tooltip, cb, css_class="btn-tool"):
        btn = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        box.set_margin_top(2); box.set_margin_bottom(2)
        l1 = Gtk.Label(label=f"<span size='large'>{icon}</span>", use_markup=True)
        l2 = Gtk.Label(label=f"<span size='small' color='#8b949e'>{text}</span>", use_markup=True)
        box.pack_start(l1, True, True, 0)
        box.pack_start(l2, True, True, 0)
        btn.add(box)
        self._sc(btn, css_class)
        btn.set_tooltip_text(tooltip)
        btn.connect("clicked", cb)
        return btn"""

new_create_tool_btn = """    def _create_tool_btn(self, icon, text, tooltip, cb, css_class="btn-tool"):
        btn = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        box.set_margin_top(2); box.set_margin_bottom(2)
        if icon.endswith("-symbolic") or icon.startswith("system-") or icon.startswith("view-"):
            l1 = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.LARGE_TOOLBAR)
        else:
            l1 = Gtk.Label(label=f"<span size='large'>{icon}</span>", use_markup=True)
        
        # Use simple label without hardcoded color markup so GTK CSS takes over
        l2 = Gtk.Label(label=text)
        self._sc(l2, "tool-btn-text")
        
        box.pack_start(l1, True, True, 0)
        box.pack_start(l2, True, True, 0)
        btn.add(box)
        self._sc(btn, css_class)
        btn.set_tooltip_text(tooltip)
        btn.connect("clicked", cb)
        return btn"""

code = code.replace(old_create_tool_btn, new_create_tool_btn)

old_toolbar_1 = """        for icon, text, tooltip, cb in [
            ("🔽", _("btn_widget"),   _("btn_widget_tt"),        self._toggle_compact),
            ("🔄", _("btn_refresh"),  _("btn_refresh_tt"),        self._manual_refresh),
            ("📜", _("btn_version"),  _("btn_version_tt"),        self._show_changelog),
            ("ℹ️", _("btn_icons"),    _("btn_icons_tt"),          self._open_mgm_simgeler),
            ("⚙️", _("btn_settings"), _("btn_settings_tt"),       self._show_settings),
        ]:"""
new_toolbar_1 = """        for icon, text, tooltip, cb in [
            ("view-restore-symbolic", _("btn_widget"),   _("btn_widget_tt"),        self._toggle_compact),
            ("view-refresh-symbolic", _("btn_refresh"),  _("btn_refresh_tt"),        self._manual_refresh),
            ("text-x-generic-symbolic", _("btn_version"),  _("btn_version_tt"),        self._show_changelog),
            ("dialog-information-symbolic", _("btn_icons"),    _("btn_icons_tt"),          self._open_mgm_simgeler),
            ("preferences-system-symbolic", _("btn_settings"), _("btn_settings_tt"),       self._show_settings),
        ]:"""
code = code.replace(old_toolbar_1, new_toolbar_1)

old_ai_btn = """        self.btn_ai = self._create_tool_btn("🤖", "AI Danışman", "Yapay zeka hava analizi",
                                             self._show_ai_dialog, "btn-ai")"""
new_ai_btn = """        self.btn_ai = self._create_tool_btn("applications-science-symbolic", "AI Danışman", "Yapay zeka hava analizi",
                                             self._show_ai_dialog, "btn-ai")"""
code = code.replace(old_ai_btn, new_ai_btn)

old_fin_btn = """        self.btn_fin = self._create_tool_btn("💰","Finans","Finans & Portföy Yönetimi",
                                              self._show_portfolio_dialog, "btn-fin")"""
new_fin_btn = """        self.btn_fin = self._create_tool_btn("office-chart-line-symbolic","Finans","Finans & Portföy Yönetimi",
                                              self._show_portfolio_dialog, "btn-fin")"""
code = code.replace(old_fin_btn, new_fin_btn)

old_toolbar_2 = """        for icon, text, tooltip, cb in [
            ("📍","GPS Bul",  "GPS ile konumu bul",         lambda *args: self._fetch_location()),
            ("🏠","Sabitle",  "Bu konumu varsayılan yap",   self._make_default),
        ]:"""
new_toolbar_2 = """        for icon, text, tooltip, cb in [
            ("mark-location-symbolic","GPS Bul",  "GPS ile konumu bul",         lambda *args: self._fetch_location()),
            ("go-home-symbolic","Sabitle",  "Bu konumu varsayılan yap",   self._make_default),
        ]:"""
code = code.replace(old_toolbar_2, new_toolbar_2)

old_fav_btn = """        self.btn_fav = self._create_tool_btn("⭐","Favorile","Bu konumu favorilere ekle/çıkar",
                                              self._toggle_favorite)
        arow.pack_start(self.btn_fav, False, False, 0)
        arow.pack_start(self._create_tool_btn("📋","Liste","Favori listesi",
                                               self._show_favorites_menu), False, False, 0)"""
new_fav_btn = """        self.btn_fav = self._create_tool_btn("bookmark-new-symbolic","Favorile","Bu konumu favorilere ekle/çıkar",
                                              self._toggle_favorite)
        arow.pack_start(self.btn_fav, False, False, 0)
        arow.pack_start(self._create_tool_btn("view-list-symbolic","Liste","Favori listesi",
                                               self._show_favorites_menu), False, False, 0)"""
code = code.replace(old_fav_btn, new_fav_btn)

with open(file_path, "w") as f:
    f.write(code)

print("Toolbar icons replaced successfully.")
