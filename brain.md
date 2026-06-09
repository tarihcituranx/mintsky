## Mimari

MintSky, Linux masaüstü ortamları için geliştirilmiş hafif ve modern bir sistem tepsisi (system tray) uygulamasıdır. Python ve GTK3 (PyGObject) tabanlı mimarisi, düşük kaynak tüketimi ve yerel masaüstü entegrasyonu sağlar.

- **Arayüz Katmanı:** GTK3 ve AppIndicator3 (libappindicator) kullanılarak sistem tepsisinde gerçek zamanlı hava durumu ikonları ve menüler sunulur.
- **Yapay Zeka Katmanı:** Groq AI API entegrasyonu ile kullanıcıya hızlı ve akıllı asistan desteği sağlanır.
- **Veri Katmanı:** Gerçek zamanlı hava durumu servislerinden (API) alınan veriler asenkron olarak işlenir ve arayüze aktarılır.
- **CI/CD ve Otomasyon:** GitHub Actions iş akışları ile dokümantasyon ve sürüm yönetim süreçleri otomatikleştirilmiştir.

## Modüller

- **AppIndicator (Sistem Tepsisi):** Uygulamanın arka planda çalışmasını, hava durumu ikonunun dinamik olarak güncellenmesini ve sağ tık menüsünü yönetir.
- **Groq AI Entegrasyonu:** Kullanıcı sorgularını Groq API'sine ileten ve yanıtları işleyen asenkron servis modülü.
- **Hava Durumu Servisi:** Konum tabanlı veya manuel girilen şehirler için anlık hava durumu verilerini çeken modül.
- **GitHub Workflows (`.github/workflows/`):**
  - `mintsky-docs-update.yaml`: Proje dokümantasyonunu (brain.md vb.) otomatik olarak güncelleyen ve senkronize eden CI/CD iş akışı.

## Bilinen Sorunlar

- Eşzamanlı dokümantasyon güncellemelerinde GitHub Actions üzerinde çakışma (conflict) yaşanabiliyordu (Giderildi).

## TODO

- [ ] Groq AI yanıt sürelerini optimize etmek için yerel önbellekleme (caching) mekanizması ekle.
- [ ] Hava durumu verileri için alternatif ücretsiz API sağlayıcıları entegre et.

## Sürüm Notu

### [Oto-Güncelleme] - Dokümantasyon İş Akışı İyileştirmesi
- **CI/CD:** `mintsky-docs-update.yaml` iş akışına `git pull --rebase origin main` adımı eklendi. Bu sayede otomatik doküman güncellemeleri sırasında oluşabilecek push çakışmaları engellendi ve iş akışının kararlılığı artırıldı.
