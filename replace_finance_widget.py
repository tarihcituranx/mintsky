import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

old_render = """    def _render_finance_widget(self, rates):
        \"\"\"Widget modunda mini finans satırı\"\"\"
        codes = self._fin_altin + self._fin_doviz
        if not codes: return

        wfin = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        wfin.get_style_context().add_class("wfin-box")
        wfin.set_halign(Gtk.Align.FILL)
        wfin.set_margin_start(8); wfin.set_margin_end(8)
        wfin.set_margin_bottom(4)

        shown = 0
        for kod in codes[:4]:  # widget'ta max 4
            if kod not in rates: continue
            r = rates[kod]
            price = r.get("Buying") or r.get("Selling") or r.get("TRY_Price")
            if price is None: continue
            _dummy = r.get("Change", 0) or 0
            em = ALTIN_EMOJIS.get(kod, DOVIZ_EMOJIS.get(kod,""))
            short_name = (ALTIN_KODLAR.get(kod, DOVIZ_KODLAR.get(kod, kod)))[:8]
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            col.set_halign(Gtk.Align.CENTER)
            nm = Gtk.Label(label=f"{em} {short_name}")
            nm.get_style_context().add_class("wfin-item")
            vl = Gtk.Label(label=f"{price:,.0f}₺" if price >= 1 else f"{price:.4f}₺")
            vl.get_style_context().add_class("wfin-val")
            col.pack_start(nm, False, False, 0)
            col.pack_start(vl, False, False, 0)
            wfin.pack_start(col, True, True, 0)
            shown += 1"""

new_render = """    def _render_finance_widget(self, rates):
        \"\"\"Widget modunda mini finans satırı\"\"\"
        codes = self._fin_altin + self._fin_doviz
        if not codes: return

        wfin = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        wfin.get_style_context().add_class("wfin-box")
        wfin.set_halign(Gtk.Align.FILL)
        wfin.set_margin_start(8); wfin.set_margin_end(8)
        wfin.set_margin_bottom(4)

        shown = 0
        for kod in codes[:4]:  # widget'ta max 4
            if kod not in rates: continue
            r = rates[kod]
            price = r.get("Buying") or r.get("Selling") or r.get("TRY_Price")
            if price is None: continue
            _dummy = r.get("Change", 0) or 0
            short_name = (ALTIN_KODLAR.get(kod, DOVIZ_KODLAR.get(kod, kod)))[:8]
            
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            col.set_halign(Gtk.Align.CENTER)
            
            hdr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            hdr_box.set_halign(Gtk.Align.CENTER)
            
            # Altın/Döviz flag SVG
            img_path = f"assets/flags/{kod.lower()}.svg"
            flag = get_svg_image(img_path, size=16, is_absolute=False)
            if not flag:
                # Altın veya bayrağı olmayan para birimi için fallback
                fallback_icon = "view-list-symbolic" if kod in ALTIN_KODLAR else "money-symbolic"
                flag = Gtk.Image.new_from_icon_name(fallback_icon, Gtk.IconSize.MENU)
                
            nm = Gtk.Label(label=short_name)
            nm.get_style_context().add_class("wfin-item")
            hdr_box.pack_start(flag, False, False, 0)
            hdr_box.pack_start(nm, False, False, 0)
            
            vl = Gtk.Label(label=f"{price:,.0f}₺" if price >= 1 else f"{price:.4f}₺")
            vl.get_style_context().add_class("wfin-val")
            col.pack_start(hdr_box, False, False, 0)
            col.pack_start(vl, False, False, 0)
            wfin.pack_start(col, True, True, 0)
            shown += 1"""

code = code.replace(old_render, new_render)

# Now let's fix Çiğ Noktası in `_make_pill`. I'll just change the fallback for 🌡 to dialog-information-symbolic.
code = code.replace('"🌡": "dialog-warning-symbolic",', '"🌡": "dialog-information-symbolic",')

with open(file_path, "w") as f:
    f.write(code)

print("Finance widget updated and Dew Point fixed.")
