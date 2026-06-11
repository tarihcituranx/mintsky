# MintSky — AI Brain Dosyası

## 🦸 AI Superpowers ve Tüm Yetenekler (Skills)
@./AGENT_SKILLS.md
@./skills/api-and-interface-design/SKILL.md
@./skills/brainstorming/SKILL.md
@./skills/browser-testing-with-devtools/SKILL.md
@./skills/ci-cd-and-automation/SKILL.md
@./skills/code-review-and-quality/SKILL.md
@./skills/code-simplification/SKILL.md
@./skills/context-engineering/SKILL.md
@./skills/debugging-and-error-recovery/SKILL.md
@./skills/deprecation-and-migration/SKILL.md
@./skills/dispatching-parallel-agents/SKILL.md
@./skills/documentation-and-adrs/SKILL.md
@./skills/doubt-driven-development/SKILL.md
@./skills/executing-plans/SKILL.md
@./skills/finishing-a-development-branch/SKILL.md
@./skills/frontend-ui-engineering/SKILL.md
@./skills/git-workflow-and-versioning/SKILL.md
@./skills/idea-refine/SKILL.md
@./skills/incremental-implementation/SKILL.md
@./skills/interview-me/SKILL.md
@./skills/performance-optimization/SKILL.md
@./skills/planning-and-task-breakdown/SKILL.md
@./skills/receiving-code-review/SKILL.md
@./skills/requesting-code-review/SKILL.md
@./skills/security-and-hardening/SKILL.md
@./skills/shipping-and-launch/SKILL.md
@./skills/source-driven-development/SKILL.md
@./skills/spec-driven-development/SKILL.md
@./skills/subagent-driven-development/SKILL.md
@./skills/systematic-debugging/SKILL.md
@./skills/test-driven-development/SKILL.md
@./skills/using-agent-skills/SKILL.md
@./skills/using-git-worktrees/SKILL.md
@./skills/using-superpowers/SKILL.md
@./skills/using-superpowers/references/gemini-tools.md
@./skills/verification-before-completion/SKILL.md
@./skills/writing-plans/SKILL.md
@./skills/writing-skills/SKILL.md

> **Tüm yapay zekalar için zorunludur. İstisna yok.**

## ⚡ Her Oturumda Yapılacak İlk ve Son İş

```
OTURUM BAŞI  →  1. brain.md oku (şu an buradasın)
               2. PROJECT_STATUS.md oku — nerede kaldığını öğren
               3. Kullanıcıya özet ver: "Kaldığımız yer: ..."

OTURUM SONU  →  1. PROJECT_STATUS.md güncelle
  veya              - Tamamlananları ✅ listesine taşı
  GÖREV BİTİŞİ      - Devam edenleri güncelle
                    - Sıradaki adımı yaz (spesifik, dosya/satır bazında)
               2. Commit at: "docs: PROJECT_STATUS güncelle"
```

**Bu adımı atlama. Bir sonraki AI senin bıraktığın yerden devam edecek.**

---

---

## 1. Proje Özeti

MintSky, Linux masaüstünde sistem tepsisinde çalışan bir hava durumu + finans uygulamasıdır.

| Alan | Değer |
|---|---|
| **Dil / Çerçeve** | Python 3.8+ / GTK3 (PyGObject) |
| **Platform** | Linux (Debian/Ubuntu) |
| **Gerçek versiyon** | `6.2` — `constants.py` içindeki `VERSIYON` referanstır |
| **Lisans** | MIT |

### Harici servisler

| Servis | Amaç |
|---|---|
| `servis.mgm.gov.tr` | Türkiye hava verisi (birincil) |
| `api.open-meteo.com` | Global hava verisi (yedek/hybrid) |
| `api.groq.com` | Groq LLM — hava durumu yorumu |
| `finance.truncgil.com` | Altın, döviz, kripto fiyatları |
| `api.turkiyeapi.dev` | İl/ilçe listesi (MGM yedek) |
| `api.github.com` | Otomatik güncelleme kontrolü |

---

## 2. Dosya Haritası

```
mintsky/
├── mintsky/
│   ├── main.py          ← Giriş noktası (7 satır, dokunma)
│   ├── constants.py     ← Sabitler — ama GTK import'u da var (BUG, bak §4)
│   ├── utils.py         ← Yardımcı fonksiyonlar — aynı GTK sorunu
│   ├── i18n.py          ← Çeviri motoru (temiz)
│   ├── locales/
│   │   ├── tr.json      ← Türkçe stringler
│   │   └── en.json      ← İngilizce stringler
│   └── ui/
│       ├── app.py       ← 2201 satır god class — projenin en büyük sorunu
│       └── styles.py    ← GTK CSS üretici
│
├── .github/
│   └── workflows/
│       ├── mintsky-audit.yaml         ← Syntax/lint/güvenlik CI
│       ├── auto-release.yaml          ← Otomatik release
│       ├── mintsky-docs-update.yaml   ← Dokümantasyon CI
│       └── mintsky-skill-update.yaml  ← Skills güncelleme
│
├── brain.md       ← Bu dosya
└── CLAUDE.md      ← Kısa özet (bu dosyadan önce okunur)
```

### Threading modeli

```
Ana thread (GTK main loop)
├── GLib.timeout_add_seconds(1800, tray_update)    ← Her 30 dk
├── GLib.timeout_add_seconds(120,  finance_refresh) ← Her 2 dk
├── daemon Thread: hava verisi çekimi
├── daemon Thread: finans verisi çekimi
├── daemon Thread: güncelleme kontrolü
└── daemon Thread: tray arka plan çekimi

KURAL: GTK widget'larına sadece GLib.idle_add() üzerinden dokun.
```

### Cache TTL değerleri

| Sabit | Değer | Açıklama |
|---|---|---|
| `WEATHER_CACHE_TTL` | 300 sn | Hava durumu cache süresi |
| `FINANCE_CACHE_TTL` | 120 sn | Finans cache süresi |
| `TRAY_FETCH_TTL` | 1800 sn | Tray arka plan çekimi |
| `TIMEOUT` | 12 sn | Tüm HTTP istekleri |

---

## 3. GitHub Actions — Güncel Sürümler

> Bu bilgiler Haziran 2026'da araştırılmıştır. Workflow değiştirirken daima bu tabloyu baz al, eski sürüm yazma.

| Action | **Kullanılacak sürüm** | Notlar |
|---|---|---|
| `actions/checkout` | **`@v6`** | v6.0.2 en güncel (Ocak 2026) |
| `actions/setup-python` | **`@v6`** | Node 24 gerektirir, runner v2.327.1+ |
| `softprops/action-gh-release` | **`@v3`** | Node 24'e geçti (Nisan 2026). v2 = Node 20 eski |

### ⚠️ Kritik: Node 24 geçişi

GitHub, **16 Haziran 2026** itibarıyla runner'larda Node 24'ü varsayılan yapıyor.
Node 20 tabanlı action'lar bu tarihten sonra uyarı/hata verebilir.

- `mintsky-audit.yaml` zaten `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` içeriyor ✅
- `auto-release.yaml` hâlâ `softprops/action-gh-release@v2` (Node 20) kullanıyor → **v3'e yükselt** 🔴
- `auto-release.yaml` ve `mintsky-skill-update.yaml` hâlâ `actions/checkout@v4` kullanıyor → **v6'ya yükselt** 🔴

### Workflow değiştirirken uygula

```yaml
# YANLIŞ
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
- uses: softprops/action-gh-release@v2

# DOĞRU
- uses: actions/checkout@v6
- uses: actions/setup-python@v6
- uses: softprops/action-gh-release@v3
```

---

## 4. Bilinen Kritik Sorunlar

Bunları bilerek çalış. Değiştirdiğin kod bu sorunları kötüleştirmesin.

### 🔴 S1 — God class (en büyük sorun)
`mintsky/ui/app.py` = **2201 satır, 104 metot, 1 sınıf**.
API çağrıları, UI oluşturma, finans, portföy, tray, AI, ayarlar hepsi `MintSkyApp(Gtk.Window)` içinde.
`api/` ve `core/` klasörleri boş duruyor — oralar dolmalı.
**Kural:** `app.py`'ye yeni metot ekleme. Yeni kod yeni modüle gider.

### 🔴 S2 — constants.py ve utils.py GTK import'u yapıyor
Sabit dosyalarının GTK'ya bağımlılığı olmamalı. Test ortamında GTK yoksa her import patlıyor.

### 🔴 S3 — BASE_MGM sabiti iki yerde tanımlı
Hem `constants.py` hem `utils.py` içinde `BASE_MGM = "https://servis.mgm.gov.tr"` var.

### 🟠 S4 — setup.py versiyonu yanlış
`setup.py` → `version="5.0"`, `constants.py` → `VERSIYON = "6.2"`. Gerçek versiyon **6.2**.

### 🟠 S5 — Wildcard import
`utils.py` içinde `from mintsky.constants import *` — ne geldiği belirsiz.

### 🟠 S6 — Exception yutma
`except Exception: pass` yaygın kullanım. Hatalar sessizce kayboluyor.

### 🟡 S7 — i18n kullanılmıyor
`i18n.py` ve `locales/` var ama `app.py` hardcoded Türkçe string kullanıyor.

---

## 5. Kodlama Kuralları — Mutlak

### GTK / Thread güvenliği

```python
# YANLIŞ — arka plan thread'inden direkt widget değiştirme → CRASH
def background_thread(self):
    self.label.set_text("yeni değer")

# DOĞRU
def background_thread(self):
    GLib.idle_add(self.label.set_text, "yeni değer")
```

### HTTP istekleri

```python
# Her istekte timeout zorunlu
r = requests.get(url, headers=MGM_HEADERS, timeout=TIMEOUT)

# Hata fırlatma — sessiz yutma değil
try:
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()
except requests.RequestException as e:
    print(f"[MintSky] API hatası [{url}]: {e}")
    return None
```

### Finans verisi thread güvenliği

```python
# Paylaşımlı veri her zaman lock ile oku/yaz
with self._finance_lock:
    data = self._finance_data.copy()  # kopyala, lock dışında kullan
```

### Import kuralları

```python
# YANLIŞ
from mintsky.constants import *

# DOĞRU — sadece kullandığını import et
from mintsky.constants import HADISE, MGM_HEADERS, TIMEOUT
```

### i18n — yeni string eklerken

```python
from mintsky.i18n import _

# YANLIŞ
label.set_text("Hava Durumu")

# DOĞRU
label.set_text(_("lbl_weather"))
# ve locales/tr.json + locales/en.json'a ekle
```

### Commit formatı

```
<tip>(<kapsam>): <özet>

tip:    feat | fix | refactor | test | docs | chore | perf
kapsam: api | ui | core | ci | constants | i18n | finance | tray

Örnekler:
  feat(api): MGM API'yi ayrı modüle taşı
  fix(finance): rate limit cache sıfırlanma hatası
  chore(ci): action sürümlerini v6/v3'e yükselt
```

---

## 6. CI Kalite Kapıları

Push etmeden önce yerel çalıştır:

```bash
black mintsky/ setup.py          # Kod formatı
isort mintsky/ setup.py          # Import sırası
flake8 mintsky/ --select=E9,F63,F7,F82  # Kritik lint
bandit -r mintsky/ -f custom     # Güvenlik
```

| Kontrol | Araç | Sonuç |
|---|---|---|
| Syntax | `py_compile` | ❌ başarısız → merge engellenir |
| Kritik lint (E9/F63/F7/F82) | `flake8` | ❌ başarısız → merge engellenir |
| Format | `black` | ⚠️ uyarı (engellemez) |
| Import sırası | `isort` | ⚠️ uyarı (engellemez) |
| Güvenlik | `bandit` | ⚠️ uyarı (engellemez) |

---

## 7. Yapay Zekaların Sık Yaptığı Hatalar

Bu listede gördüğün şeyi yapma:

1. **`app.py`'ye yeni metot ekleme** → Yeni modüle taşı (§4-S1)
2. **`constants.py`'ye GTK import'u ekleme** → Yasak (§4-S2)
3. **Thread'den direkt widget güncelleme** → `GLib.idle_add()` kullan (§5)
4. **`except Exception: pass` yazma** → En azından logla (§4-S6)
5. **Wildcard import kullanma** → Spesifik import et (§5)
6. **Workflow'a eski action sürümü yazma** → §3 tablosuna bak
7. **Hardcoded Türkçe string ekle** → `i18n._()` kullan (§5)
8. **`setup.py` versiyonunu güncellemeyi unut** → `6.2` olmalı (§4-S4)
9. **Tüm değişikliği tek commit'e sıkıştır** → Atomic commit yaz
10. **`BASE_MGM`'i yeniden tanımla** → `constants.py`'deki kullan

---

## 8. Proje Durumu — Oturum Sürekliliği

> AI'ın hafızası yoktur. Oturumlar arası bağlamı `PROJECT_STATUS.md` taşır.

### Kural — Her oturumda

**Oturum başında:**
1. `brain.md` oku (zaten yapıyorsun)
2. `PROJECT_STATUS.md` oku — nerede kaldığını öğren
3. Eksik bağlam varsa kullanıcıya sor, tahmin etme

**Oturum sonunda veya görev tamamlanınca:**
1. `PROJECT_STATUS.md`'yi güncelle
2. Ne yapıldı, ne yarım kaldı, bir sonraki adım ne — hepsini yaz
3. Commit at: `docs: PROJECT_STATUS güncelle`

### PROJECT_STATUS.md formatı

```markdown
# MintSky — Proje Durumu

**Son güncelleme:** YYYY-MM-DD
**Güncel dal:** main / feature/xxx
**Versiyon:** 6.2

## ✅ Tamamlananlar
- [tarih] Yapılan şey

## 🔄 Devam Edenler
- Şu an üzerinde çalışılan şey (dosya/fonksiyon adıyla)
- Neden yarım kaldı

## ⏭️ Sıradaki Adım
Bir sonraki AI oturumunda ilk yapılacak şey (spesifik ol)

## 🚧 Açık Kararlar
- Henüz karar verilmemiş teknik seçimler

## 📝 Notlar
Önemli ama kategori dışı kalan şeyler
```

---

## 9. Değişiklik Günlüğü

| Tarih | Değişiklik |
|---|---|
| 2026-06-11 | İlk oluşturma — tam repo analizi + GitHub Actions canlı araştırması |
| 2026-06-11 | §8 eklendi — PROJECT_STATUS.md oturum sürekliliği kuralı |


---

## ⚙️ Güvenlik Zinciri — Nasıl Çalışır

Bu sistem birden fazla katmanda çalışır. Hangi AI aracı kullanılırsa kullanılsın
en az biri tetiklenir:

```
Claude Code   → CLAUDE.md  (otomatik yüklenir)
Cursor        → .cursor/rules (otomatik yüklenir)
Gemini CLI    → GEMINI.md  (otomatik yüklenir)
OpenCode      → AGENTS.md  (otomatik yüklenir)
Diğer araçlar → AGENTS.md  (çoğu araç okur)
                    ↓
              brain.md  (ikinci katman)
                    ↓
         PROJECT_STATUS.md  (hafıza)
```

Her dosya aynı şeyi söyler:
**"Önce brain.md oku, sonra PROJECT_STATUS.md oku, bitince PROJECT_STATUS.md güncelle."**

---

## 10. Agent Skills (Yapay Zeka Becerileri) ve İşlevleri

Proje klasöründeki `AGENT_SKILLS.md` ve `skills/` dizini, bu projedeki AI asistanlarının (Gemini, Claude, Cursor vb.) kıdemli bir yazılım mühendisi (Senior Software Engineer) gibi davranmasını sağlayan kuralları ve iş akışlarını (SOP) barındırır.

### AI Ajanlarına Göre Hızlı Başlangıç (Quick Start)
- **Claude Code:** `/plugin install agent-skills@addy-agent-skills`
- **Cursor:** İlgili `SKILL.md` dosyalarını `.cursor/rules/` içine kopyalayın.
- **Gemini CLI:** `gemini skills install ./skills/`
- **Windsurf:** Kuralları Windsurf ayarlarınıza dahil edin.
- **OpenCode:** `AGENTS.md` ve `skill` aracı aracılığıyla otomatik kullanılır.

### Beceriler (Skills) Ne İşe Yarar?
Yüzlerce satırlık `skills` dosyalarının temel özeti ve kullanım amaçları şunlardır:

| Beceri (Skill) | İşlevi ve Amacı | Ne Zaman Kullanılır? |
|--------|---------|-----------------------|
| `using-agent-skills` | Gelen isteği doğru beceri iş akışıyla haritalandırır. | Oturuma başlarken, yön bulurken |
| `interview-me` | "Beni sorgula" (grill me). Kullanıcının asıl niyetini anlamak için adım adım mülakat yapar. | İsterler belirsiz veya yetersiz olduğunda |
| `idea-refine` | Muğlak fikirleri yapılandırılmış, somut projelere dönüştürür. | Kaba bir konsepti olgunlaştırırken |
| `spec-driven-development` | Kodlamadan önce testleri, sınırları ve hedefleri barındıran spesifikasyon (PRD) yazar. | Büyük bir özelliğe / refactor'e başlarken |
| `planning-and-task-breakdown` | Spesifikasyonu, birbirine bağımlı ve test edilebilir küçük görevlere böler (Task breakdown). | Uygulanabilir birimlere ihtiyaç duyulduğunda |
| `incremental-implementation` | Kodu dikey dilimler halinde, her adımda test ederek ve doğrulayarak inşa eder. | Birden fazla dosyayı etkileyen değişikliklerde |
| `test-driven-development` | Kırmızı-Yeşil-Refactor döngüsünü zorunlu kılar (Test piramidi). | Yeni logic yazarken veya bug çözerken |
| `verification-before-completion` | İşi "Bitti" ilan etmeden önce kanıt (ör: `py_compile`, `flake8`) sunmayı zorunlu kılar. | Her `commit`, `push` veya görev sonlandırması öncesinde |
| `code-review-and-quality` | Temiz kod prensipleri ve en iyi pratikler ekseninde kodu inceler. | Pull Request (PR) birleşmeden önce |
| `performance-optimization` | Gecikmeleri bulup optimize eder (ör: `requests.Session()` kullanımı). | Sistem yavaşladığında veya refactor'de |

Bu yetenekler, yapay zekanın sadece "kod üreten bir makine" olmaktan çıkıp mimari düşünen, hata önleyen, testleri zorunlu kılan gerçek bir "Pair Programmer" olmasını sağlamak için `brain.md` sistemine bağlanmıştır.
