[🇬🇧 English](README_en.md)

![MintSky Başlık](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

[![MintSky CI](https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-docs-update.yaml?branch=main&label=MintSky%20CI)](https://github.com/tarihcituranx/mintsky/actions)
[![Python 3](https://img.shields.io/badge/Python-3-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![GTK3](https://img.shields.io/badge/GTK-3-orange.svg?style=flat&logo=gnome&logoColor=white)](https://www.gtk.org/)
[![GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-lightgrey.svg?style=flat&logo=linux)](https://www.linux.org/)

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=450&lines=MintSky+-+Linux+Hava+Durumu+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;Sistem+Tepsisinden+Takip+Et+%F0%9F%94%94;A%C3%A7%C4%B1k+Kaynak+%26+%C3%9Ccretsiz+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

## 🌟 Özellikler

* 🌍 **Dünya Şehirleri (Global API):** Hem MGM üzerinden Türkiye verilerini hem de Open-Meteo üzerinden dünyadaki tüm şehirleri otomatik tanır ve hava durumunu anlık çeker.
* 🤖 **Groq AI & Edge-TTS Asistan:** Hava durumuna göre "bugün ne giymelisin", "şemsiye almalı mısın" gibi yapay zeka tavsiyeleri verir. **Edge-TTS** altyapısıyla bu tavsiyeleri doğal bir insan sesiyle okur!
* 📈 **Finans Modülü:** Canlı altın, döviz ve kripto para takibi ile portföy kar/zarar yönetimi.
* ♿ **Görme Engelli Erişilebilirliği:** Arayüzdeki tüm elementler (butonlar, arama çubukları, sekmeler) `Atk` kütüphanesiyle işaretlenmiş olup Linux Ekran Okuyucuları (Örn: Orca) ile %100 uyumludur. Sadece klavye kullanarak uygulamada gezebilirsiniz.
* 🌐 **Çoklu Dil Desteği (i18n):** Türkçe, İngilizce, Almanca, Fransızca, Arapça, Farsça, Çince ve Azerbaycan Türkçesi dahil olmak üzere toplam 8 dil desteği! Telegram tarzı `.json` uzantılı modüler dil dosyaları ile anında geçiş yapın.
* 🔔 **Sistem Tepsisi (AppIndicator3):** Arka planda hafif ve sessizce çalışarak sistem tepsisinden anlık durum takibi sunar.
* 💬 **Masaüstü Bildirimleri:** `libnotify` entegrasyonu ile kritik hava durumu değişimlerinde anlık bildirimler gönderir.
* 🎨 **GTK3 Arayüzü:** Linux masaüstü ortamlarıyla tam uyumlu, modern, sade ve kullanıcı dostu arayüz.

## 📸 Ekran Görüntüleri

<!-- screenshot here -->
_Ekran görüntüleri yakında eklenecektir._

## ⚙️ Kurulum

MintSky uygulamasını Linux sisteminizde çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

```bash
# 1. Gerekli sistem bağımlılıklarını yükleyin (Debian/Ubuntu tabanlı sistemler için)
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-appindicator3-0.1 libnotify-bin

# 2. Depoyu klonlayın
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky

# 3. Python bağımlılıklarını yükleyin
pip3 install -r requirements.txt

# 4. Uygulamayı çalıştırın
python3 main.py
```

## 🛠️ Yapılandırma

* **Groq API Anahtarı:** Yapay zeka destekli hava durumu yorumları ve önerileri alabilmek için geçerli bir Groq API anahtarına ihtiyacınız vardır. API anahtarınızı uygulama arayüzündeki ayarlar bölümünden tanımlayabilirsiniz.
* **Şehir Ayarları:** Takip etmek istediğiniz şehri ve ilçeyi arayüz üzerinden aratıp varsayılan olarak kaydedebilirsiniz.
* **Tema:** Uygulama, sisteminizin mevcut GTK3 temasıyla otomatik olarak uyumlu şekilde çalışır.

## 💻 Teknoloji Yığını

| Teknoloji | Açıklama |
| --- | --- |
| **Python 3** | Ana programlama dili |
| **GTK3 (PyGObject)** | Kullanıcı arayüzü kütüphanesi |
| **AppIndicator3** | Sistem tepsisi (System Tray) entegrasyonu |
| **Groq AI & Edge-TTS** | Yapay zeka destekli hava durumu yorumlama ve asistanlık |
| **MGM & Open-Meteo** | Hava Durumu API'leri |
| **Truncgil Finance API**| Anlık finans ve borsa verileri |
| **libnotify** | Masaüstü bildirim sistemi |

## 🤝 Katkıda Bulunma

MintSky projesine katkıda bulunmak isterseniz, lütfen bir [Pull Request (PR)](https://github.com/tarihcituranx/mintsky/pulls) açın veya karşılaştığınız hataları bildirmek için bir issue oluşturun. Her türlü katkı, hata bildirimi ve özellik önerisi projenin gelişimi için çok değerlidir!

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
