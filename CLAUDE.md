# MintSky — Claude Talimatları

## ZORUNLU — Konuşmadan önce yap

Kullanıcı sana herhangi bir şey söylemeden önce şu iki dosyayı oku:

1. `brain.md` — mimari, kurallar, bilinen sorunlar
2. `PROJECT_STATUS.md` — nerede kaldığımız, sıradaki adım

Okuduktan sonra kullanıcıya tek cümleyle özetle:
> "Kaldığımız yer: [PROJECT_STATUS.md'deki sıradaki adım]. Devam edelim mi?"

**Bu adımı atlama. Kullanıcı senden bir şey istemiş olsa bile önce oku.**

---

## ZORUNLU — Görev bitiminde yap

Her görev tamamlandığında veya kullanıcı oturumu kapatmadan önce:

1. `PROJECT_STATUS.md` güncelle:
   - Tamamlananı ✅ listesine taşı
   - Yarım kalanı ve neden durduğunu yaz
   - Sıradaki adımı spesifik yaz (dosya adı, fonksiyon adı, satır numarası)
2. Commit at: `docs: PROJECT_STATUS güncelle`

**Bunu yapmazsan bir sonraki AI sıfırdan başlar. Kullanıcıyı tekrar tekrar açıklamak zorunda bırakırsın.**

---

## Proje

MintSky — Linux GTK3 hava durumu + finans masaüstü uygulaması.
Detaylar: `brain.md`
