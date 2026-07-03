import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

old_fav = """    def _refresh_fav_button(self, is_fav):
        icon = self.btn_fav.get_child().get_children()[0]
        lbl = self.btn_fav.get_child().get_children()[1]
        if is_fav:
            if isinstance(icon, Gtk.Label): icon.set_markup("<span size='large'>🌟</span>")
            else: icon.set_from_icon_name("starred-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lbl.set_text(_("btn_fav_remove"))
            self.btn_fav.set_tooltip_text("Bu konumu favorilerden çıkar")
        else:
            if isinstance(icon, Gtk.Label): icon.set_markup("<span size='large'>⭐</span>")
            else: icon.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            lbl.set_text(_("btn_fav_add"))
            self.btn_fav.set_tooltip_text(_("btn_fav_tt"))"""

new_fav = """    def _refresh_fav_button(self, is_fav):
        childs = self.btn_fav.get_child().get_children()
        icon = childs[0] if len(childs) > 0 else None
        lbl = childs[1] if len(childs) > 1 else None
        if is_fav:
            if isinstance(icon, Gtk.Label): icon.set_markup("<span size='large'>🌟</span>")
            elif icon: icon.set_from_icon_name("starred-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            if lbl: lbl.set_text(_("btn_fav_remove"))
            self.btn_fav.set_tooltip_text("Bu konumu favorilerden çıkar")
        else:
            if isinstance(icon, Gtk.Label): icon.set_markup("<span size='large'>⭐</span>")
            elif icon: icon.set_from_icon_name("non-starred-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
            if lbl: lbl.set_text(_("btn_fav_add"))
            self.btn_fav.set_tooltip_text(_("btn_fav_tt"))"""

if old_fav in code:
    code = code.replace(old_fav, new_fav)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Fav button crash fixed via python script.")
else:
    print("Could not find old_fav in code. Maybe already fixed or slightly different.")
