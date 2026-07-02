import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# 1. Increase cond_icon size
old_cond_icon = "cond_icon = get_svg_image(emoji, size=24)"
new_cond_icon = "cond_icon = get_svg_image(emoji, size=56)"
code = code.replace(old_cond_icon, new_cond_icon)

# 2. Fix Finance Widget
old_render_finance = """        codes = self._fin_altin + self._fin_doviz
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
            flag = get_svg_image(kod.lower(), size=16, folder="flags")
            # Altın veya bayrağı olmayan para birimi için fallback get_svg_image içinde '?' olarak döner ama 
            # widget içinde bunu Gtk.Image.new_from_icon_name ile değiştirmemiz gerekebilir.
            # Ancak get_svg_image Gtk.Label dönüyorsa (bulunamadıysa), kontrol edelim:
            if isinstance(flag, Gtk.Label):
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

new_render_finance = """        # Take up to 2 golds and 2 currencies to balance the widget by default, or just let it show max 4 from the combined list if one is empty
        # If user explicitly configured, we respect it, but we still limit to 4 so it doesn't overflow
        codes = []
        if len(self._fin_altin) > 0 and len(self._fin_doviz) > 0:
            codes = self._fin_altin[:2] + self._fin_doviz[:2]
        else:
            codes = (self._fin_altin + self._fin_doviz)[:4]
            
        if not codes: return

        wfin = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        wfin.get_style_context().add_class("wfin-box")
        wfin.set_halign(Gtk.Align.FILL)
        wfin.set_margin_start(8); wfin.set_margin_end(8)
        wfin.set_margin_bottom(4)

        shown = 0
        for kod in codes:
            if kod not in rates: continue
            r = rates[kod]
            price = r.get("Buying") or r.get("Selling") or r.get("TRY_Price")
            if price is None: continue
            
            change_val = r.get("Change", 0) or 0
            # Gram Altın gibi kelimeleri kesmemesi için limiti kaldırdık veya 12'ye çıkardık
            short_name = (ALTIN_KODLAR.get(kod, DOVIZ_KODLAR.get(kod, kod)))[:12]
            if short_name == "Gram Altın": short_name = "Gr. Altın" # Özel kısaltma
            elif short_name == "Çeyrek Altın": short_name = "Çeyrek"
            elif short_name == "Tam Altın": short_name = "Tam Altın"
            elif short_name == "Amerikan Dol": short_name = "Dolar"
            
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            col.set_halign(Gtk.Align.CENTER)
            
            hdr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            hdr_box.set_halign(Gtk.Align.CENTER)
            
            flag = get_svg_image(kod.lower(), size=16, folder="flags")
            if isinstance(flag, Gtk.Label):
                fallback_icon = "view-list-symbolic" if kod in ALTIN_KODLAR else "money-symbolic"
                flag = Gtk.Image.new_from_icon_name(fallback_icon, Gtk.IconSize.MENU)
                
            nm = Gtk.Label(label=short_name)
            nm.get_style_context().add_class("wfin-item")
            hdr_box.pack_start(flag, False, False, 0)
            hdr_box.pack_start(nm, False, False, 0)
            
            # Değer ve değişim yan yana
            val_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            val_box.set_halign(Gtk.Align.CENTER)
            vl = Gtk.Label(label=f"{price:,.0f}₺" if price >= 1 else f"{price:.4f}₺")
            vl.get_style_context().add_class("wfin-val")
            val_box.pack_start(vl, False, False, 0)
            
            if change_val != 0:
                c_lbl = Gtk.Label()
                sign_str = "▲" if change_val > 0 else "▼"
                c_color = "#3fb950" if change_val > 0 else "#f85149"
                c_lbl.set_markup(f"<span color='{c_color}' font_size='x-small'>{sign_str}%{abs(change_val):.1f}</span>")
                val_box.pack_start(c_lbl, False, False, 0)
            
            col.pack_start(hdr_box, False, False, 0)
            col.pack_start(val_box, False, False, 0)
            wfin.pack_start(col, True, True, 0)
            shown += 1"""

code = code.replace(old_render_finance, new_render_finance)

with open(file_path, "w") as f:
    f.write(code)

print("Patch applied for icon size and finance widget items.")
