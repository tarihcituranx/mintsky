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
- [ ] Çoklu dil desteğinin (Türkçe/İngilizce) uygulama arayüzüne tam entegrasyonu.
- [ ] Farklı hava durumu sağlayıcıları için fallback (yedek) mekanizması eklenmesi.

## Sürüm Notu

### [Oto-Güncelleme] Dokümantasyon ve CI/CD İyileştirmeleri
- **README Şablon Güncellemesi:** Otomatik oluşturulan README dosyasındaki "Typing SVG" başlığı, daha iyi görsel düzen için ortalanmış HTML `<p align="center"><img ... /></p>` yapısına dönüştürüldü.
- **CI/CD Rebase Stratejisi:** `mintsky-docs-update.yaml` iş akışındaki otomatik commit süreçlerinde olası çakışmaları (conflict) önlemek adına `git pull --rebase` yöntemi entegre edildi.

## Çalışma Prensipleri (Agent Kuralları)

- **Hata Ayıklama ve Geliştirme (Agent Skills):** Yapay zeka asistanları, proje üzerinde hata düzeltmeleri (bug fixes) yaparken, mimariyi incelerken veya yeni özellik eklerken KESİNLİKLE **Addy Osmani agent-skills** prensiplerini ve dizindeki (`AGENT_SKILLS.md`, `.claude/`, `skills/`) yetenekleri kullanmalıdır (Örn: hata çözümlerinde *test-driven-development*, *debugging-and-error-recovery*).
