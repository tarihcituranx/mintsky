[🇬🇧 English](README_en.md)

![MintSky Başlık](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

<p align="center">
  <a href="https://github.com/tarihcituranx/mintsky/actions"><img src="https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-audit.yaml?branch=main&label=MintSky%20CI" alt="MintSky CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3-blue.svg?style=flat&logo=python&logoColor=white" alt="Python 3"></a>
  <a href="https://www.gtk.org/"><img src="https://img.shields.io/badge/GTK-3-orange.svg?style=flat&logo=gnome&logoColor=white" alt="GTK3"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg?style=flat&logo=linux" alt="Platform: Linux"></a>
</p>

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=450&lines=MintSky+-+Linux+Hava+Durumu+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;Sistem+Tepsisinden+Takip+Et+%F0%9F%94%94;A%C3%A7%C4%B1k+Kaynak+%26+%C3%9Ccretsiz+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

MintSky, Linux masaüstü ortamları (özellikle Linux Mint, Ubuntu, Debian türevleri) için özel olarak geliştirilmiş **GTK3 tabanlı yeni nesil bir hava durumu ve asistan uygulamasıdır.** MGM (Türkiye), Open-Meteo ve MSN Weather API'lerini akıllı fallback (yedekleme) sistemiyle harmanlar. Yalnızca havayı değil; entegre Groq LLaMA yapay zekası ve Edge-TTS ile size *hava durumuna özel tavsiyeler okuyan* tam donanımlı kişisel asistanınızdır.

## 🌟 Özellikler

* 🌍 **Akıllı Çoklu API Motoru & AQI:** MGM (Türkiye resmi verileri), Open-Meteo (Global yedek) ve **MSN Hava Durumu (Ekstra Sensörler)** sistemleri arasında otomatik geçiş yapar. İnteraktif Hava Kalitesi (AQI) uyarıları ile sağlığınızı korur.
* 🤖 **Groq AI & Edge-TTS Asistan:** Hava durumuna göre "bugün ne giymelisin", "şemsiye almalı mısın" gibi yapay zeka destekli akıllı tavsiyeler verir. **Edge-TTS** altyapısıyla bu tavsiyeleri en doğal insan seslerinden biriyle size okur!
* 📈 **Canlı Finans Modülü:** Gerçek zamanlı altın (gram, çeyrek vb.), döviz (Dolar, Euro) ve kripto para piyasalarını Truncgil API'si üzerinden takip edin. Kişisel portföyünüzün anlık kar/zarar durumunu hesaplayın.
* 🎨 **Lucide Vektörel Tasarım & Pürüzsüz GTK3 Arayüz:** Masaüstüyle bütünleşik karanlık/aydınlık tema desteği ve modern Lucide SVG ikonlarıyla donatılmış akıcı, scroll ve pencere taşması gibi sorunların tarihe karıştığı bir arayüz.
* ♿ **%100 Erişilebilirlik (A11y):** Görme engelli kullanıcılar için arayüzdeki butonlar, metin girişleri ve sekmeler `Atk` kütüphanesiyle donatılmıştır. Tüm ekran okuyucularıyla (Örn: Orca) sadece klavye üzerinden pürüzsüzce kullanılabilir.
* 🌐 **8 Farklı Dil Desteği (i18n):** Türkçe, İngilizce, Almanca, Fransızca, Arapça, Farsça, Çince ve Azerbaycan Türkçesi dil seçenekleri. Telegram benzeri `.json` uzantılı yerelleştirme modülleri ile geliştirilmeye açıktır.
* 🔔 **Sistem Tepsisi & Bildirimler (AppIndicator3 & libnotify):** Arka planda RAM ve işlemci dostu şekilde çalışır, hava değişimlerinde sessiz ve şık masaüstü bildirimleri ile sizi uyarır.

## 📸 Ekran Görüntüleri

<p align="center">
  <img src="assets/scr_main.png" width="48%" alt="MintSky Genel Bakış" />
  <img src="assets/scr_daily.png" width="48%" alt="Saatlik ve Günlük Tahminler" />
</p>
<p align="center">
  <img src="assets/scr_ai.png" width="48%" alt="Yapay Zeka Yorumları ve Detaylar" />
  <img src="assets/scr_finance.png" width="48%" alt="Canlı Finans Modülü" />
</p>

## ⚙️ Kurulum & Çalıştırma

MintSky uygulamasını kurmak oldukça basittir. 

### 1. Sistem Bağımlılıkları (Debian / Ubuntu / Linux Mint)
Terminalinizi açın ve PyGObject ve GTK3 kütüphaneleri ile sistem eklentilerini kurun:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-appindicator3-0.1 libnotify-bin
```

### 2. İndirme ve Kurulum
Depoyu bilgisayarınıza kopyalayın ve `pip` üzerinden kullanıcı dizinine kurun:
```bash
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky
pip3 install . --break-system-packages
```
*(Not: `pip` hatası alıyorsanız güncel Linux dağıtımlarındaki Python paket yönetimi güvenliğinden dolayı `--break-system-packages` bayrağını kullanabilirsiniz. Daha güvenli bir yöntem isterseniz `pipx` veya `venv` tercih edebilirsiniz.)*

### 3. Başlatma
Kurulum bittikten sonra uygulamayı direkt çalıştırabilirsiniz:
```bash
mintsky
```

## 🛠️ Temel Yapılandırma

* **Groq API Anahtarı:** Yapay zekanın tavsiye vermesi için arayüzdeki `Ayarlar` sekmesinden ücretsiz bir [Groq API Key](https://console.groq.com/keys) edinip sisteme girmelisiniz. (Anahtarlarınız cihazınızda keyring ile şifrelenerek güvende tutulur).
* **Konum Sabitleme:** Şehir araması yaptıktan sonra "Sabitle" butonuna basarsanız her açılışta o lokasyonun verileri yüklenir.
* **Finans Paneli:** Sağ üstteki `Finans` butonundan piyasalara göz atabilirsiniz, ayarlar ekranından portföy entegrasyonlarını yapabilirsiniz.

## 🚀 Yol Haritası (Planlanan Özellikler)

* **Bukalemun Hibrit Mimari:** 
  * GNOME ve Fedora kullanıcıları için native **GTK4/Libadwaita** desteği.
  * Windows ve macOS kullanıcıları için **çapraz platform arayüz (PyQt/Tkinter)** desteği (Uygulamanın çalıştırıldığı işletim sistemine göre native arayüz otomatik yüklenecek).

## 💻 Teknoloji Yığını

| Teknoloji | Tür | Açıklama |
| :--- | :--- | :--- |
| **Python 3** | Ana Dil | Sistemin kalbi ve mantıksal operasyonlar |
| **GTK3 (PyGObject)** | Arayüz | Native Linux GUI kütüphanesi |
| **AppIndicator3** | Sistem | Arka plan ve tepsi entegrasyonu |
| **Groq LLaMA** | LLM | Üst düzey hızda çalışan, havayı analiz eden LLM |
| **Edge-TTS** | Konuşma | Microsoft altyapısıyla doğal metin okuma servisi |
| **MGM & Open-Meteo & MSN** | Hava API | Dinamik fall-back özellikli çoklu sağlayıcı mimarisi |
| **Truncgil API** | Finans API | Anlık Türkiye döviz ve altın kurları |
| **Pytest & GitHub Actions** | Test & CI | Kapsamlı senaryo mocklama ve sürekli entegrasyon |

## 🤝 Katkıda Bulunma

MintSky, herkesin katılımına ve gelişimine açık bir projedir. Yeni bir özellik eklemek, dil dosyasını genişletmek veya bug çözmek isterseniz bir [Pull Request (PR)](https://github.com/tarihcituranx/mintsky/pulls) oluşturabilirsiniz. 

> **Yasal Uyarı (Disclaimer):** MintSky test amaçlı geliştirilmiş bir hava durumu ve finans takip uygulamasıdır; API verilerindeki aksaklıklardan doğacak hiçbir maddi veya manevi zarar kabul edilmez. Linux Mint 22.3 "Zena" üzerinde geliştirilmiştir ancak bağımlılıkları karşılayan tüm modern GTK destekli dağıtımlarda çalışır.

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
