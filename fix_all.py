import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r") as f:
    code = f.read()

# 1. Widget Icon Size
old_cond_icon = "cond_icon = get_svg_image(emoji, size=24)"
new_cond_icon = "cond_icon = get_svg_image(emoji, size=56)"
code = code.replace(old_cond_icon, new_cond_icon)

# 2. Finance Widget Items
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

new_render_finance = """        codes = []
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
            short_name = (ALTIN_KODLAR.get(kod, DOVIZ_KODLAR.get(kod, kod)))[:12]
            if short_name == "Gram Altın": short_name = "Gr. Altın"
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

# 3. Widget Mode Rate Limit
old_toggle = """        # Update CSS ve ilk veri çekimi
        self._apply_css()
        GLib.timeout_add(100, lambda *_: self._search(force=True) or False, None)
        self._check_for_updates_bg()"""
new_toggle = """        # Update CSS ve ilk veri çekimi
        self._apply_css()"""
code = code.replace(old_toggle, new_toggle)

# 4. Changelog dialog fix
old_changelog = """        dlg.format_secondary_markup(
            f"<b>v7.0.125 (Bu Sürüm) — Güncel versiyon</b>\\n"
            "• 🌐 <b>Çoklu Dil Desteği (i18n)</b> — Türkçe ve İngilizce dil seçimi eklendi.\\n"
            "• 🌓 <b>Karanlık/Aydınlık Tema</b> — Ayarlar'dan seçilebilen gelişmiş tema altyapısı.\\n"
            "• 🤖 <b>AI Danışman Güncellemesi</b> — AI penceresi karanlık temaya uygun hale getirildi, okunaklılık artırıldı.\\n"
            "• 📡 <b>MGM API Optimizasyonu</b> — İl/ilçe parametreleri ve güncel hadise kodları (GGSY, MSY) %100 uyumlu hale getirildi.\\n"
            "• 📦 <b>API Modülerizasyonu</b> — God Class mimarisi kırıldı, API'ler ayrıştırıldı\\n"
            "• 💰 <b>Finans Modülü</b> — Truncgil Finance API ile altın, gümüş, döviz\\n"
            "  fiyatları, rate-limited önbellekleme\\n"
            "• 📊 <b>Portföy Takibi</b> — Alım fiyatı gir, gram/adet miktarı kaydet, kar/zarar hesapla\\n"
            "• 🔄 <b>GitHub Güncelleme Kontrolü</b> — Yeni sürüm bildirimleri otomatikleşti\\n"
            "• 🎨 <b>Modern 3D CSS</b> — Gradyanlar, drop-shadow filtreler ve büyük arayüz fontları\\n"
            "• ⚡ <b>Optimizasyonlar</b> — Thread güvenliği, Single-Instance (Tekil çalışma) kilidi\\n\\n"
            "<b>v5.0:</b> Groq AI Danışman, Widget düzeltme, Hibrit OM, İkon düzeltme.\\n"
            "<b>v4.x:</b> Concurrent fetch, Open-Meteo hybrid.\\n"
            "<b>v3.x:</b> Widget modu, Tray, MeteoAlarm.\\n\\n"
            f"<small>Geliştirici: Turan Kaya | {GITHUB_REPO}</small>"
        )"""
new_changelog = """        dlg.format_secondary_markup(
            f"<b>v{VERSIYON} (Bu Sürüm) — Güncel versiyon</b>\\n"
            "• 🎨 <b>MintSky Grafik Devrimi</b> — Hava durumu ve finans menüsü SVG ikonlarla tamamen yenilendi.\\n"
            "• 🌐 <b>Çoklu Dil Desteği (i18n)</b> — Yabancı dil destekli altyapı ve gelişmiş çeviriler.\\n"
            "• 🌗 <b>Karanlık/Aydınlık Tema</b> — Ayarlar'dan seçilebilen gelişmiş tema altyapısı.\\n"
            "• 📡 <b>MGM & Open-Meteo Hibrit API</b> — Kesintisiz profesyonel veri ve rate-limit düzeltmeleri.\\n"
            "• 💰 <b>Finans & Portföy Modülü</b> — Altın/döviz fiyatları ve cüzdan takibi (widget destekli).\\n"
            "• 🤖 <b>AI Danışman</b> — Gelişmiş yapay zeka entegrasyonu ile hava durumu analizleri.\\n"
            "• 🔄 <b>Widget & Sistem Tepsisi (Tray)</b> — Artış/azalış oranları ve sistem tepsisi eklentileri.\\n\\n"
            "<b>v5.0 - v7.0:</b> Modüler altyapı, Concurrent Fetch, Tema Motoru, Portföy Takibi.\\n"
            "<b>v3.x - v4.x:</b> Temel API yapısı, Widget modu, MGM optimizasyonu.\\n\\n"
            f"<small>Geliştirici: Turan Kaya | {GITHUB_REPO}</small>"
        )"""
code = code.replace(old_changelog, new_changelog)

with open(file_path, "w") as f:
    f.write(code)

print("All fixes applied successfully.")
