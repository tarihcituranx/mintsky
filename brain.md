# MintSky Proje Mimarisi ve Agent-Skills Workflow Rehberi

## 🏛️ Yeni Modüler Mimari İskeleti

MintSky, bakımını kolaylaştırmak ve sürdürülebilirliği artırmak için monolitik (tek dosya) yapıdan modüler bir mimariye geçirilmiştir. Yeni yapı aşağıdaki gibidir:

```text
mintsky-repo/
├── mintsky/
│   ├── __init__.py
│   ├── main.py                # Uygulama giriş noktası (entry point)
│   ├── constants.py           # Sabitler (API URL'leri, WMO/MGM Hadise kodları, Emoji sözlükleri)
│   ├── utils.py               # Yardımcı fonksiyonlar (Tarih formatlama, ikon seçimi vs.)
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py             # GTK App Sınıfı, Arayüz mantığı, thread'ler
│   │   └── styles.py          # CSS temalandırma ve dizayn
│   ├── api/                   # (Gelecek geliştirme için rezerve) MGM, OpenMeteo ve Groq API'leri
│   └── core/                  # (Gelecek geliştirme için rezerve) Veri işleme
├── .github/
│   └── workflows/
│       └── python-app.yml     # Modern Python CI/CD boru hattı (GitHub Actions v4/v5)
├── README.md
├── requirements.txt           # Bağımlılıklar listesi
└── setup.py                   # Uygulama kurulum yapılandırması
```

### 🐛 Yapılan Hata Ayıklamalar (Debugging)
1. **Güvenli JSON Parse İşlemi:** Orijinal koddaki JSON parse sırasında çıkabilecek potansiyel çökmelere karşı `safe_json` metodolojisi oluşturuldu. API yanıt vermediğinde veya geçersiz yanıt döndüğünde uygulama çökmeden boş liste (`[]`) ile yola devam ediyor.
2. **Dict/List Uyumluluğu:** MeteoAlarm gibi kaynaklarda dict yerine farklı obje tipi dönme durumunda yaşanacak crash senaryosu önlendi.

---

## 🤖 Addy Osmani `agent-skills` İş Akışı (Workflow) Entegrasyonu

Projenin refactoring sürecinde, [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) repository'sindeki en iyi yazılım mühendisliği prensipleri temel alınmıştır.

### `/spec` (Planlama ve Mimarinin Çıkarılması)
- **Problem:** Orijinal projenin tek bir devasa Python dosyası (`MintSky.py`) olması, ölçeklenmeyi ve yeni özellik eklemeyi zorlaştırıyordu.
- **Karar:** GTK mantığının (`app.py`), yardımcı araçların (`utils.py`), sabitlerin (`constants.py`) ve stillerin (`styles.py`) ayrı dosyalara çıkarılmasına karar verildi.

### `/build` (Modülerleştirme ve Kodlama)
- **Incremental Implementation (Adım Adım Geliştirme):** Dosyalar parçalanırken, mevcut GTK sınıflarının birbirine bağlılıkları (coupling) çözüldü. Constants ve Utils importları, ana `MintSkyApp` dosyasına temiz bir şekilde bağlandı.
- **Feature Flags / Safe Defaults:** Uygulamanın API anahtarı olmadan çalışabilmesi (Groq AI için) gibi safe default (güvenli varsayılan) yapıları korundu.

### `/test` (Statik Doğrulama)
- Uygulamanın syntax hatalarına (`E9, F63, F7, F82`) karşı korunması adına GitHub Actions entegrasyonu sağlandı. Python 3.12 ile ortam testleri otomatize edildi.
- `python3 -m py_compile` ile statik sözdizimi doğrulandı.

### `/review` & `/code-simplify` (Basitleştirme ve Gözden Geçirme)
- 1724 satırlık kod incelendi, modüller kendi sorumluluklarına (Single Responsibility Principle) çekildi.
- CSS oluşturma ve sabit değerler ana mantıktan ayrıştırılarak UI sınıfı sadeleştirildi.

### `/ship` (Gönderim)
- Kodların Git reposuna eklenmesi, gereksinim (`requirements.txt`) ve CI/CD (`python-app.yml`) dosyalarının hazırlanması tamamlanıp üretime (production) hazır hale getirildi.
