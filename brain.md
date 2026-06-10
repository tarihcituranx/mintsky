## Mimari

MintSky, Linux masaüstü ortamları için tasarlanmış, hafif ve modüler bir hava durumu ve yapay zeka asistanı uygulamasıdır.

- **Arayüz Katmanı:** GTK3 (PyGObject) kullanılarak geliştirilmiştir. Sistem tepsisi entegrasyonu için `AppIndicator3` kullanılır.
- **Veri Katmanı:** Gerçek zamanlı hava durumu verilerini çekmek için harici hava durumu API'leri kullanılır.
- **Yapay Zeka Katmanı:** Groq AI API entegrasyonu ile hava durumu verileri analiz edilerek kullanıcıya doğal dilde özetler ve tavsiyeler sunulur.
- **Otomasyon ve CI/CD:** GitHub Actions iş akışları aracılığıyla dokümantasyon (README.md) otomatik olarak güncellenir ve senkronize edilir.

## Modüller

- **Sistem Tepsisi (AppIndicator):** Uygulamanın arka planda çalışmasını ve sistem tepsisinden anlık hava durumu ikonları ile kontrol edilmesini sağlar.
- **Hava Durumu Servisi:** Konum tabanlı veya manuel girilen şehirler için anlık hava durumu verilerini çeker.
- **Groq AI Entegrasyonu:** Hava durumu verilerini işleyerek akıllı giyim, etkinlik ve seyahat önerileri üretir.
- **Dokümantasyon İş Akışı (`mintsky-docs-update.yaml`):** Depodaki değişiklikleri izleyerek README.md dosyasını dinamik olarak günceller.

## Bilinen Sorunlar

- Bazı Linux dağıtımlarında (özellikle GNOME dışı veya AppIndicator desteği varsayılan olmayan masaüstü ortamlarında) sistem tepsisi ikonunun görünmesi için ek uzantılar (örn. AppIndicator Support) gerekebilir.
- Groq API anahtarı eksik olduğunda yapay zeka özellikleri devre dışı kalmaktadır.

## TODO

- [x] GitHub Actions dokümantasyon iş akışında Typing SVG görselinin ortalanmış HTML etiketi ile değiştirilmesi.
- [x] Dokümantasyon güncelleme iş akışında çakışmaları önlemek için `git pull --rebase` stratejisine geçilmesi.
- [x] Farklı hava durumu sağlayıcıları için fallback (yedek) mekanizması eklenmesi.
- [x] **Telegram Tarzı Dil Paketi Sistemi:** Uygulama arayüzünün dil dosyaları (örn. `tr.json`, `en.json`) üzerinden çalışması ve kullanıcıların kendi dil dosyalarını yükleyip / seçebilmesi.
- [x] **Görme Engelliler İçin Tam Erişilebilirlik (Accessibility):** Linux sistemlerindeki ekran okuyucular (Orca vb.) ile %100 uyumlu çalışması için GTK/Atk etiketlerinin ayarlanması ve uygulamanın tamamen klavye ile (Tab tuşu, kısayollar) yönetilebilir hale getirilmesi.
- [x] **Edge TTS Entegrasyonu:** gTTS yerine Microsoft Edge'in çok daha doğal ve akıcı olan yapay zeka seslendirmelerine (edge-tts kütüphanesi) geçiş yapılması.
- [x] **Dünya Şehirleri Desteği (Global API):** Arama çubuğunda yabancı şehirler aranabilmesi için Nominatim API ile Open-Meteo API entegrasyonunun birleştirilmesi.

## Sürüm Notu

### [V7.0 - Global, Erişilebilir ve Modüler Sürüm]
- **Dünya Şehirleri Desteği:** Sadece Türkiye değil, Nominatim (OpenStreetMap) entegrasyonu sayesinde tüm dünya şehirleri ve ilçeleri aranabilir hale geldi! (Open-Meteo altyapısı ile global hava tahmini desteği).
- **Edge-TTS Sesli Asistan:** Gecikmeli ve robotik gTTS kaldırılarak, yerine Microsoft Edge'in tamamen doğal ve akıcı (EmelNeural vb.) ses modelleri entegre edildi.
- **Erişilebilirlik (A11y - Orca Desteği):** Görme engelli kullanıcılar için butonlara, arama kutularına ve ikonlara `Atk` (Accessibility Toolkit) etiketleri eklendi. Ekran okuyucular artık her elementi doğru okuyabiliyor.
- **i18n Dil Sistemi (Telegram Tarzı):** Projeye `locales/tr.json` ve `en.json` dosyaları eklenerek modüler dil sistemi altyapısı kuruldu. Artık tüm uygulama diller arasında özelleştirilebiliyor.
- **Güvenlik ve Agent Skills Denetimi:** Tüm kod yapısı `Addy Osmani Agent-Skills` prensiplerine göre incelendi. Subprocess shell injection koruması, try-except kalkanları ve JSON önbellek temizlikleri doğrulandı. Hiçbir güvenlik açığı bulunmuyor.

### [Oto-Güncelleme] Dokümantasyon ve CI/CD İyileştirmeleri
- **README Şablon Güncellemesi:** Otomatik oluşturulan README dosyasındaki "Typing SVG" başlığı, daha iyi görsel düzen için ortalanmış HTML `<p align="center"><img ... /></p>` yapısına dönüştürüldü.
- **CI/CD Rebase Stratejisi:** `mintsky-docs-update.yaml` iş akışındaki otomatik commit süreçlerinde olası çakışmaları (conflict) önlemek adına `git pull --rebase` yöntemi entegre edildi.

## Çalışma Prensipleri (Agent Kuralları)

- **Hata Ayıklama ve Geliştirme (Agent Skills):** Yapay zeka asistanları, proje üzerinde hata düzeltmeleri (bug fixes) yaparken, mimariyi incelerken veya yeni özellik eklerken KESİNLİKLE **Addy Osmani agent-skills** prensiplerini ve dizindeki (`AGENT_SKILLS.md`, `.claude/`, `skills/`) yetenekleri kullanmalıdır (Örn: hata çözümlerinde *test-driven-development*, *debugging-and-error-recovery*).

### [Yeni Geliştirme: Groq AI JSON Mode ve Sesli Asistan]
- **Yapılandırılmış Çıktı (JSON Mode):** `constants.py` içindeki `GROQ_SYSTEM` promptu güncellenerek, Groq API'sinden yanıtların düz metin yerine kesin bir JSON formatında gelmesi sağlandı. API isteğine `response_format: {"type": "json_object"}` parametresi eklendi.
- **Arayüz Modernizasyonu:** `app.py` içerisindeki Groq diyalog ekranı baştan aşağı yenilendi. Artık düz bir `Gtk.Label` yerine dinamik oluşturulan `Gtk.Frame` kartları (Giyim, Sağlık, Aktivite vb.) ikonlarıyla birlikte ekrana basılarak çok daha premium ve okunabilir bir görünüm elde edildi.
- **Sesli Asistan (Text-to-Speech):** Groq'un yeni `/v1/audio/speech` yeteneği entegre edildi. Arayüze "🔊 Dinle" butonu eklendi. JSON olarak alınan veriler doğal bir konuşma metnine dönüştürülüp, "playai-tts" (Fritz-PlayAI) modeli kullanılarak sesli okunabilir hale getirildi (Linux `aplay` aracı ile oynatılıyor).
