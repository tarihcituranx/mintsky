[🇬🇧 English](README_en.md)

![MintSky Başlık](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

<p align="center">
  <a href="https://github.com/tarihcituranx/mintsky/actions"><img src="https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-audit.yaml?branch=main&label=MintSky%20CI" alt="MintSky CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python&logoColor=white" alt="Python 3"></a>
  <a href="https://www.gtk.org/"><img src="https://img.shields.io/badge/GTK-3-orange.svg?style=flat&logo=gnome&logoColor=white" alt="GTK3"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg?style=flat&logo=linux" alt="Platform: Linux"></a>
</p>

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=520&lines=MintSky+-+Linux+Hava+Durumu+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;Sistem+Tepsi+Widget%27i+%F0%9F%94%94;Canlı+Finans+%2B+Portföy+Takibi+%F0%9F%92%B0;Açık+Kaynak+%26+Ücretsiz+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

MintSky, Linux Mint, Ubuntu ve Debian gibi GTK3 destekli Linux masaüstleri için geliştirilmiş bir hava durumu ve masaüstü asistanıdır. Türkiye'de MGM istasyon ölçümlerini ve tahminlerini, Open-Meteo'nun koordinat tabanlı tahminleriyle tamamlar; MSN verileri ise isteğe bağlı kimlik bilgileri sağlandığında ek kaynak olarak kullanılır. Ayrıca Groq yapay zekâsı, Edge-TTS, finans takibi ve portföy özellikleri sunar.

Güncel geliştirme sürümü: **7.4.0**.

## 🌟 Özellikler

### 🌦️ Hava Durumu Motoru
* **MGM + Open-Meteo + isteğe bağlı MSN:** MGM Türkiye istasyon ölçümlerini, günlük/saatlik tahminleri ve uyarıları sağlar; Open-Meteo koordinat tabanlı tahmin ve astronomi verilerini tamamlar. MSN alanları yalnızca geçerli API kimlik bilgileri ayarlıysa kullanılabilir.
* **MGM istasyon ayrıntıları:** İstasyonun ölçüm saati, 10 dakika/1/6/12/24 saat ve gün başından beri yağış birikimi, deniz suyu ve kar ölçümü (istasyonda varsa) gösterilir. MGM'nin takvim gününe ait iklim normali ve tarihsel sıcaklık uçları da mevcut olduğunda sunulur.
* **Anlık veriler:** Sıcaklık, hissedilen, nem, basınç, rüzgâr yönü/hızı ve Beaufort şiddeti, çiğ noktası, bulutluluk ve görüş mesafesi. MGM saatlik tahminindeki azami rüzgâr da gösterilir.
* **UV İndeksi & Yağış:** Open-Meteo'dan anlık UV, yağış miktarı, kar verisi — birden fazla kaynaktan doğrulanır.
* **Saatlik & 5 Günlük Tahmin:** Saatlik sıcaklık, yağış olasılığı, rüzgar ve UV tahmini; 5 günlük gündüz/gece min/max grafikleri.
* **Gün Doğumu/Batımı:** Open-Meteo'dan her gün için güneş saatleri.
* **MGM Alarmları & MeteoAlarm:** Resmî uyarılar güncel API yanıt şemasına göre ilçe/merkez kimliğiyle eşleştirilir. Yeni alarm çıktığında masaüstü bildirimi gelir.
* **Hava Kalitesi (AQI):** MSN API'den alınan anlık Hava Kalitesi İndeksi göstergesi.
* **Konum bulma:** Linux GeoClue konum servisi kullanılabiliyorsa önce ona başvurulur; aksi durumda yaklaşık IP konumu denenir. Koordinatlar MGM'nin en yakın ilçe istasyonuna eşlenir. IP tabanlı konum yaklaşık sonuç verebilir; MGM'de bulunmayan yerlerde Nominatim yedek geocoding sağlar.
* **Türkiye saati:** MGM, Open-Meteo ve MSN ölçüm zamanları arayüzde `Europe/Istanbul` saat dilimine çevrilir ve kaynak adıyla birlikte gösterilir.

### 🤖 Yapay Zeka & Sesli Asistan
* **Groq LLaMA AI:** "Bugün ne giymeliyim?", "Dışarı çıksam mı?" gibi havaya özel yorumlar için Groq API (LLaMA modeli) entegrasyonu. API anahtarı olmadan da çalışır (uyarı gösterir).
* **Edge-TTS Sesli Okuma:** Microsoft Edge altyapısıyla, yapay zekanın ürettiği tavsiyeyi doğal bir insan sesiyle asenkron olarak yüksek sesle okur. Sistem üzerindeki `edge-tts` CLI aracı otomatik bulunur.
* **AI Diyalog Penceresi:** Bağımsız bir pencerede mevcut hava koşullarını göstererek AI yanıtını akar-biçimde sunar.

### 💰 Canlı Finans Modülü (Truncgil Finance API)
* **Altın:** Gram Altın, Çeyrek Altın, Yarım Altın, Tam Altın, Cumhuriyet Altını, Ata Altın, Gümüş ve daha fazlası — seçilebilir.
* **Döviz:** USD, EUR, GBP, JPY, CHF, CAD, AUD, SAR, QAR, SEK, NOK ve daha fazlası — seçilebilir.
* **Kripto Altyapısı:** Bitcoin, Ethereum, Ripple, Solana ve 40+ coin için Truncgil API altyapısı hazır *(portföy UI'ına tam entegrasyon planlanıyor)*.
* **Portföy Takibi:** Altın ve döviz varlıkları için alım fiyatı girerek portföy oluşturun, anlık **kar/zarar** hesabını görün. Alım fiyatı otomatik güncel piyasa fiyatıyla doluyor.
* **2 Dakikalık Cache:** Finans verileri 120 saniyede bir yenilenir, gereksiz API yükü oluşturmaz.

### 🖥️ Arayüz & Kullanılabilirlik
* **Kompakt Widget Modu:** Tek tıkla uygulamayı masaüstü köşesine yerleşik küçük bir widget'a dönüştürün. Kompakt modda anlık sıcaklık ve 3 saatlik tahmin görünür. Normal pencere açılışta büyütülür.
* **Sistem Tepsisi (AppIndicator3 & libnotify):** Uygulamayı kapatsanız da arka planda çalışmaya devam eder. Tepsi ikonuna sağ tıklayınca anlık hava bilgisi, sol tıklayınca uygulama açılır. Mintsky, AyatanaAppIndicator3 (Ubuntu/Mint) ve standart AppIndicator3'ü otomatik algılar.
* **Masaüstü Bildirimleri:** Hava alarmı, uygulama güncellemesi ve önemli hava değişimlerinde libnotify üzerinden şık GTK bildirimleri gönderir.
* **Otomatik Başlatma (Autostart):** Ayarlardan tek tıkla açılışta başlat/durdur. `.desktop` dosyası `~/.config/autostart/` altına otomatik yazılır.
* **Uygulama Olarak Kur:** Sistem menüsüne kalıcı ikon ve `.desktop` girdisi ekler (`/usr/share/applications/`).
* **Otomatik Güncelleme Kontrolü:** Başlangıçta GitHub'daki son sürümle karşılaştırır; yeni sürüm varsa banner gösterir ve tek tıkla güncelleme yapar.
* **Favoriler:** Sık kullandığınız şehirleri favorilere ekleyip tek tıkla yükleyebilirsiniz.
* **Önbellek ve API nezaketi:** Hava/istasyon verileri kısa süreli önbelleklenir; ortak MGM alarm ve merkez sorguları tekrar kullanılabilir. İstemci kendini MintSky olarak tanıtır, zaman aşımı uygular ve 429 yanıtlarında `Retry-After`/bekleme süresine uyar. Proxy, sahte tarayıcı kimliği veya koruma atlatma kullanılmaz.
* **Klavye Kısayolları:** `Ctrl+R` ile yenile, `Ctrl+W` ile kapat ve daha fazlası.
* **Lucide SVG İkonlar & GTK3 Tema Uyumu:** Masaüstü temanıza (karanlık/aydınlık) %100 uyumlu native GTK3 çizimi.

### 🌐 Çoklu Dil (i18n)
Arayüz metinleri JSON dil dosyalarından yüklenir: Türkçe, İngilizce, Almanca, Fransızca, Azerbaycan Türkçesi, Arapça, Farsça ve Çince. Dil değişince arayüzün tamamı yeni dille açılsın diye uygulama kendini yeniden başlatır. Bazı eski diyalog ve açıklamalarda çeviri kapsamı kısmi olabilir.

### ♿ Erişilebilirlik (A11y)
GTK3'ün yerleşik erişilebilirlik altyapısı devrededir. Orca gibi ekran okuyucularla temel klavye desteği mevcuttur.

### 🔐 Güvenlik
* API anahtarları (Groq) sistem **keyring**'ine şifreli olarak kaydedilir, hiçbir zaman JSON ayar dosyasına yazılmaz.
* MSN API kimlik bilgileri ortam değişkenlerinden (`MSN_API_KEY`, `MSN_APP_ID`) okunur — kaynak kodda sabit değer yok.
* Ayar ve portföy dosyaları atomik olarak kaydedilir ve kullanıcıya özel `0600` izinleriyle oluşturulur.
* İstekler normal, tanımlı MintSky istemci kimliğiyle yapılır; servis limitlerini aşmaya veya bot korumalarını atlatmaya yönelik yöntem kullanılmaz.

---

## 📸 Ekran Görüntüleri

<p align="center">
  <img src="assets/scr_main.png" width="48%" alt="MintSky Genel Bakış" />
  <img src="assets/scr_daily.png" width="48%" alt="Saatlik ve Günlük Tahminler" />
</p>
<p align="center">
  <img src="assets/scr_ai.png" width="48%" alt="Yapay Zeka Yorumları ve Detaylar" />
  <img src="assets/scr_finance.png" width="48%" alt="Canlı Finans Modülü" />
</p>

---

## ⚙️ Kurulum & Çalıştırma

### 1. Sistem Bağımlılıkları (Debian / Ubuntu / Linux Mint)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo \
  gir1.2-appindicator3-0.1 gir1.2-notify-0.7 libnotify-bin
```
> **Ubuntu 22.04+ / Linux Mint 22+** kullanıyorsanız `gir1.2-appindicator3-0.1` yerine `gir1.2-ayatanaappindicator3-0.1` gerekebilir. Kod her ikisini de otomatik algılar.

### 2. İndirme ve Kurulum
```bash
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky
pip3 install . --break-system-packages
```
Bu komut `requirements.txt` üzerinden `requests`, `PyGObject`, `groq`, `edge-tts` ve `keyring` paketlerini otomatik kurar.

*(Not: `--break-system-packages` yerine daha güvenli bir yöntem için `pipx install .` veya `python3 -m venv .venv && source .venv/bin/activate && pip install .` kullanabilirsiniz.)*

### 3. Başlatma
```bash
mintsky
# veya masaüstü widget modunda:
mintsky --autostart
```

---

## 🛠️ Yapılandırma

| Ayar | Nasıl? |
|---|---|
| **Groq API Anahtarı** | `Ayarlar → 🤖 AI` sekmesinden ücretsiz [Groq API Key](https://console.groq.com/keys) girin. Keyring'e şifreli kaydedilir. |
| **Konum Sabitleme** | Şehir arayıp "⭐ Sabitle" butonuna basın — her açılışta o konum yüklenir. |
| **Finans Paneli** | `Ayarlar → 💰 Finans` sekmesinden gösterilecek altın, döviz ve kripto seçin. |
| **Dil** | `Ayarlar → ⚙️ Sistem` sekmesinden desteklenen diller arasından seçim yapın. Değişiklik için uygulama yeniden başlatılır. |
| **Otomatik Başlatma** | `Ayarlar → ⚙️ Sistem` sekmesindeki toggle ile açılışta başlatın. |
| **MSN API** | `MSN_API_KEY` ve `MSN_APP_ID` ortam değişkenlerini ayarlayın (isteğe bağlı). Bu değerler yoksa MSN/AQI verisi gelmez; MGM ve Open-Meteo özellikleri çalışmayı sürdürür. |

### Konum ve saat

Otomatik konum GeoClue varsa onu, yoksa IP tabanlı yaklaşık konumu kullanır. Şehir/ilçe araması veya konumu sabitleme daha doğru sonuç verir. Ölçüm zamanları arayüzde Türkiye saatiyle gösterilir.

### Geliştirici kontrolleri

Kaynak ağacından testleri `python3 -m pytest -q` komutuyla çalıştırın. Testler ağdan bağımsızdır; canlı servis yanıtları ayrıca doğrulanmalıdır. Bazı MGM alanlarının boş olması mevsime veya istasyonun ölçüm donanımına bağlı olabilir.

---

## 🚀 Yol Haritası (Planlanan Özellikler)

* **Bukalemun Hibrit Mimari:**
  * GNOME ve Fedora kullanıcıları için native **GTK4/Libadwaita** desteği.
  * Windows ve macOS kullanıcıları için **çapraz platform arayüz (PyQt/Tkinter)** desteği — işletim sistemine göre native arayüz otomatik yüklenir.

---

## 💻 Teknoloji Yığını

| Teknoloji | Tür | Açıklama |
| :--- | :--- | :--- |
| **Python 3.10+** | Ana Dil | Asenkron arka plan görevleri, thread pool |
| **GTK3 (PyGObject)** | Arayüz | Native Linux GUI, AppIndicator3, libnotify |
| **Groq (LLaMA)** | LLM | Üst düzey hızda hava analizi yapan yapay zeka |
| **Edge-TTS** | TTS | Microsoft altyapılı asenkron sesli okuma |
| **MGM API** | Hava | Türkiye resmi meteoroloji verileri + alarm + meteoalarm |
| **Open-Meteo** | Hava (yedek) | UV, saatlik & 5 günlük tahmin, gün doğumu/batımı |
| **MSN Weather** | Hava (ekstra) | AQI, gerçek zamanlı hissedilen sıcaklık |
| **Nominatim (OSM)** | Geocoding | MGM'de kayıtsız konumlar için koordinat çözümleme |
| **Truncgil Finance** | Finans | Gerçek zamanlı altın, döviz, kripto pariteler |
| **keyring** | Güvenlik | API anahtarlarını şifreli sistem deposunda saklar |
| **Pytest & GitHub Actions** | Test & CI | Mock tabanlı senaryo testleri, bandit güvenlik taraması |

---

## 🤝 Katkıda Bulunma

MintSky herkesin katılımına açıktır. Yeni özellik, dil dosyası veya hata düzeltmesi için [Pull Request](https://github.com/tarihcituranx/mintsky/pulls) açabilirsiniz.

> **Yasal Uyarı:** MintSky test amaçlı geliştirilmiş bir uygulamadır; API verilerinden kaynaklanabilecek aksaklıklar için sorumluluk kabul edilmez. Linux Mint 22.3 "Zena" üzerinde geliştirilmiştir, bağımlılıkları karşılayan tüm modern GTK3 destekli dağıtımlarda çalışır.

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
