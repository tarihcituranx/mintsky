## Mimari

MintSky, Linux masaüstü ortamları için geliştirilmiş, hafif ve modüler bir Python/GTK3 uygulamasıdır. Sistem kaynaklarını minimum düzeyde tüketerek arka planda çalışacak şekilde tasarlanmıştır.

*   **Arayüz ve Entegrasyon:** Kullanıcı arayüzü PyGObject (GTK3) ile oluşturulmuştur. Sistem tepsisi (system tray) entegrasyonu için `AppIndicator3` (veya modern dağıtımlarda `AyatanaAppIndicator3`) kullanılır. Masaüstü bildirimleri ise `libnotify` aracılığıyla sisteme iletilir.
*   **Veri Katmanı:** Gerçek zamanlı hava durumu verileri, HTTP istekleri (`requests` kütüphanesi) aracılığıyla güvenilir hava durumu servislerinden çekilir.
*   **Yapay Zeka Entegrasyonu:** Groq AI API'si kullanılarak, anlık hava durumu verileri analiz edilir ve kullanıcıya doğal dilde, kişiselleştirilmiş hava durumu yorumları ve giyim/aktivite önerileri sunulur.
*   **Asenkron Yapı:** Ağ istekleri ve AI analiz süreçleri, GTK ana arayüz döngüsünü (main loop) bloke etmemek için asenkron iş parçacıkları (threading) veya GLib kaynakları kullanılarak arka planda yürütülür.

## Modüller

*   **`main.py`:** Uygulamanın ana giriş noktasıdır. GTK döngüsünü başlatır, sinyal yönetimini gerçekleştirir ve modüller arası koordinasyonu sağlar.
*   **`indicator.py`:** Sistem tepsisi ikonunu, sağ tık menüsünü ve menü elemanlarının (hava durumu özeti, hızlı yenileme, ayarlar, çıkış) dinamik güncellenmesini yönetir.
*   **`weather.py`:** Hava durumu API'sine istek atma, JSON yanıtlarını ayrıştırma ve sıcaklık, nem, rüzgar gibi temel verileri normalize etme işlevlerini üstlenir.
*   **`ai_client.py`:** Groq AI API'si ile iletişimi sağlar. Hava durumu verilerini anlamlı bir prompt haline getirerek yapay zekadan Türkçe özet ve tavsiyeler alır.
*   **`config.py`:** Kullanıcı tercihlerini (şehir, API anahtarları, güncelleme sıklığı, tema) yerel diskte (örn. `~/.config/mintsky/config.json`) güvenli bir şekilde saklar ve yükler.
*   **`notification.py`:** Hava durumundaki ani değişiklikleri veya AI tarafından üretilen günlük özetleri sistem bildirimi olarak kullanıcıya sunar.

## Bilinen Sorunlar

*   **AppIndicator Bağımlılığı:** Bazı minimalist pencere yöneticilerinde (i3, Sway vb.) veya saf GNOME ortamlarında `gir1.2-appindicator3` kütüphanesi kurulu olmadığında uygulama başlatılamayabilir.
*   **Wayland Uyumluluğu:** Wayland oturumlarında sistem tepsisi ikonunun konumlandırılması veya görünürlüğü, kullanılan masaüstü ortamının (DE) tepsi uzantılarına bağlı olarak değişiklik gösterebilir.
*   **API Limiti ve Kesintiler:** Groq API veya hava durumu servis sağlayıcısının yanıt vermediği durumlarda, arayüzde geçici donmaları önlemek adına hata yakalama mekanizmaları bulunsa da kullanıcıya sunulan veriler güncellenemeyebilir.

## TODO

- [ ] Wayland ortamlarında daha kararlı çalışması için Ayatana AppIndicator geçişini tamamen standartlaştırmak.
- [ ] Ayarlar penceresine entegre bir "Groq API Anahtarı Test Et" butonu eklemek.
- [ ] İnternet bağlantısı koptuğunda uygulamanın çevrimdışı modda son başarılı verileri göstermesini sağlamak.
- [ ] Hava durumu ikon setlerini yerelleştirmek ve GTK temasıyla uyumlu (koyu/açık mod) sembolik ikonlar kullanmak.

## Sürüm Notu

*   **v0.1.1:** GitHub Actions dokümantasyon iş akışları (`mintsky-docs-update.yaml`) güncellendi. `jq` JSON oluşturma süreçlerinde karşılaşılan tırnak işareti kaçış (escaping) hatalarını önlemek amacıyla sistem talimatları (system instructions) Bash `cat << 'EOF'` yapısına taşındı. Bu sayede dokümantasyon güncelleme otomasyonunun kararlılığı artırıldı.
