#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MintSky — Linux Mint Masaüstü & Görev Çubuğu Uygulaması
MGM resmi API + Open-Meteo yedek/hybrid + Groq AI Hava Danışmanı
Finans Modülü: Truncgil Finance API (Altın, Gümüş, Döviz, Kripto)
Portföy Takibi: Alım fiyatı girişi, kar/zarar hesaplama
Geliştirici : https://github.com/tarihcituranx (Turan Kaya)
Versiyon    : 7.0
Lisans      : MIT
"""
import os
# ─── Sabitler ─────────────────────────────────────────────────────────────
BASE_MGM      = "https://servis.mgm.gov.tr"

BASE_OM       = "https://api.open-meteo.com/v1/forecast"
GROQ_API_URL  = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL    = "llama-3.3-70b-versatile"
FINANCE_API   = "https://finance.truncgil.com/api/today.json"
GITHUB_API    = "https://api.github.com/repos/tarihcituranx/mintsky/releases/latest"
GITHUB_REPO   = "https://github.com/tarihcituranx/mintsky"

MGM_HEADERS   = {
    "Origin": "https://www.mgm.gov.tr",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}
NOM_HEADERS   = {"User-Agent": "MintSkyApp/7.0 (github.com/tarihcituranx)"}
TIMEOUT           = 12
WEATHER_CACHE_TTL = 300   # saniye — widget/ayar geçişi API atılmaz, önbellekten render
FINANCE_CACHE_TTL = 120   # saniye — Truncgil API minimum yenileme aralığı
TRAY_FETCH_TTL    = 1800  # saniye — tray arka plan çekimi (30 dk)

CONFIG_DIR      = os.path.expanduser("~/.config")
FAV_FILE        = os.path.join(CONFIG_DIR, "mintsky_favorites.json")
SETTING_FILE    = os.path.join(CONFIG_DIR, "mintsky_settings.json")
LOC_FILE        = os.path.join(CONFIG_DIR, "mintsky_locations.json")
PORTFOLIO_FILE  = os.path.join(CONFIG_DIR, "mintsky_portfolio.json")
AUTOSTART_DIR   = os.path.expanduser("~/.config/autostart")
AUTOSTART_FILE  = os.path.join(AUTOSTART_DIR, "mintsky.desktop")
APP_DIR         = os.path.expanduser("~/.local/share/applications")
APP_FILE        = os.path.join(APP_DIR, "mintsky.desktop")
ICON_DIR        = os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps")

GELISTIRICI   = "https://github.com/tarihcituranx"
MGM_SIMGELER  = "https://www.mgm.gov.tr/site/yardim1.aspx?=Simgeler99"
UYGULAMA_ADI  = "MintSky"
VERSIYON = "7.1.7"

# ─── Finans: gösterilecek kodlar ve türkçe isimleri ─────────────────────
ALTIN_KODLAR = {
    "GRA": "Gram Altın", "GUM": "Gümüş (gr)", "BRE": "Brent Petrol", "ONS": "Altın ONS",
    "HAS": "Has Gram Altın", "CEY": "Çeyrek Altın", "YAR": "Yarım Altın", "TAM": "Tam Altın",
    "CUM": "Cumhuriyet Altını", "ATA": "Ata Altını", "ODA": "14 Ayar Altın", "OSA": "18 Ayar Altın",
    "YIA": "22 Ayar Bilezik", "IKI": "İki Buçuk Altın", "BES": "Beşli Altın", "GRE": "Gremse Altın",
    "RES": "Reşat Altın", "HAM": "Hamit Altın", "GPL": "Gram Platin"
}
DOVIZ_KODLAR = {
    "USD": "Amerikan Doları", "EUR": "Euro", "GBP": "İngiliz Sterlini", "CHF": "İsviçre Frangı",
    "CAD": "Kanada Doları", "RUB": "Rus Rublesi", "AED": "BAE Dirhemi", "AUD": "Avustralya Doları",
    "DKK": "Danimarka Kronu", "SEK": "İsveç Kronu", "NOK": "Norveç Kronu", "JPY": "100 Japon Yeni",
    "KWD": "Kuveyt Dinarı", "ZAR": "Güney Afrika Randı", "BHD": "Bahreyn Dinarı", "LYD": "Libya Dinarı",
    "SAR": "Suudi Arabistan Riyali", "IQD": "Irak Dinarı", "ILS": "İsrail Şekeli", "IRR": "İran Riyali",
    "INR": "Hindistan Rupisi", "MXN": "Meksika Pesosu", "HUF": "Macar Forinti", "NZD": "Yeni Zelanda Doları",
    "BRL": "Brezilya Reali", "IDR": "Endonezya Rupiahi", "CZK": "Çek Korunası", "PLN": "Polonya Zlotisi",
    "RON": "Romanya Leyi", "CNY": "Çin Yuanı", "ARS": "Arjantin Pesosu", "ALL": "Arnavutluk Leki",
    "AZN": "Azerbaycan Manatı", "BAM": "Bosna-Hersek Markı", "CLP": "Şili Pesosu", "COP": "Kolombiya Pesosu",
    "CRC": "Kostarika Kolonu", "DZD": "Cezayir Dinarı", "EGP": "Mısır Lirası", "HKD": "Hong Kong Doları",
    "ISK": "İzlanda Kronası", "JOD": "Ürdün Dinarı", "KRW": "Güney Kore Wonu", "KZT": "Kazak Tengesi",
    "LBP": "Lübnan Lirası", "LKR": "Sri Lanka Rupisi", "MAD": "Fas Dirhemi", "MDL": "Moldovya Leusu",
    "MKD": "Makedon Dinarı", "MYR": "Malezya Ringgiti", "OMR": "Umman Riyali", "PEN": "Peru İnti",
    "PHP": "Filipinler Pesosu", "PKR": "Pakistan Rupisi", "QAR": "Katar Riyali", "RSD": "Sırbistan Dinarı",
    "SGD": "Singapur Doları", "SYP": "Suriye Lirası", "THB": "Tayland Bahtı", "TWD": "Yeni Tayvan Doları",
    "UAH": "Ukrayna Grivnası", "UYU": "Uruguay Pesosu", "GEL": "Gürcistan Larisi", "TND": "Tunus Dinarı",
    "BGN": "Bulgar Levası"
}
KRIPTO_KODLAR = {
    "BTC": "Bitcoin", "ETH": "Ethereum", "XRP": "Ripple", "USDT": "Tether", "SOL": "Solana",
    "BNB": "BNB", "DOGE": "Dogecoin", "USDC": "USD Coin", "ADA": "Cardano", "STETH": "Lido Staked Ether",
    "TRX": "TRON", "LINK": "Chainlink", "AVAX": "Avalanche", "SUI": "Sui", "WBTC": "Wrapped Bitcoin",
    "XLM": "Stellar", "WSTETH": "Wrapped stETH", "HBAR": "Hedera", "TON": "Toncoin", "SHIB": "Shiba Inu",
    "DOT": "Polkadot", "WETH": "WETH", "LTC": "Litecoin", "LEO": "LEO Token", "BCH": "Bitcoin Cash",
    "BGB": "Bitget Token", "TRUMP": "Official Trump", "UNI": "Uniswap", "HYPE": "Hyperliquid",
    "PEPE": "Pepe", "WEETH": "Wrapped eETH", "USDS": "USDS", "NEAR": "NEAR Protocol", "USDE": "Ethena USDe",
    "AAVE": "Aave", "APT": "Aptos", "ICP": "Internet Computer", "ONDO": "Ondo", "ETC": "Ethereum Classic",
    "WBT": "WhiteBIT Coin", "VET": "VeChain", "XMR": "Monero", "POL": "POL (ex-MATIC)", "CRO": "Cronos",
    "RENDER": "Render", "ALGO": "Algorand", "MNT": "Mantle", "OKB": "OKB", "OM": "MANTRA", "DAI": "Dai"
}

ALTIN_EMOJIS = {
    "GRA":"🥇","GUM":"🥈","CEY":"🏅","YAR":"🏅","TAM":"🏅",
    "HAS":"🥇","ODA":"💍","OSA":"💍","YIA":"📿","GPL":"⚪",
    "CUM":"🪙","ATA":"🪙",
}
DOVIZ_EMOJIS = {
    "USD":"🇺🇸","EUR":"🇪🇺","GBP":"🇬🇧","CHF":"🇨🇭",
    "JPY":"🇯🇵","AUD":"🇦🇺","CAD":"🇨🇦","SAR":"🇸🇦",
    "RUB":"🇷🇺","AED":"🇦🇪",
}

DEFAULT_FINANCE_ALTIN  = ["GRA","GUM","CEY","TAM"]
DEFAULT_FINANCE_DOVIZ  = ["USD","EUR","GBP"]
DEFAULT_FINANCE_KRIPTO = []

GROQ_SYSTEM = (
    "Sen yalnızca meteoroloji ve hava durumu konusunda uzmanlaşmış bir yapay zeka "
    "danışmanısın. Görevin: sana verilen ANLIK HAVA VERİLERİNE dayanarak kısa, "
    "pratik ve doğru Türkçe öneriler sunmak.\n\n"
    "YANIT VEREBİLECEĞİN KONULAR (yalnızca bunlar):\n"
    "• Giyim önerileri (sıcaklık, hissedilen, rüzgar)\n"
    "• Dışarı çıkma zamanlaması ve aktivite önerileri (yağış, fırtına, UV)\n"
    "• Sağlık uyarıları (aşırı sıcak/soğuk, yüksek nem, UV)\n"
    "• Araç ve yol koşulu uyarıları (buzlanma, sis, fırtına)\n"
    "• Açık hava/tarım çalışmalarına yönelik öneriler\n"
    "• Aktif MGM uyarılarının pratik etkisi\n\n"
    "YASAK KONULAR: Politika, haberler, tarih, genel bilgi, programlama veya "
    "hava durumuyla ilgisiz her şey.\n\n"
    "FORMAT: 3-6 madde, kısa ve öz Türkçe, emoji ile."
)

# ─── MGM Hadise Sözlüğü ───────────────────────────────────────────────────
HADISE = {
    "A":    ("☀️",  "Açık",                                   "Hava tamamen güneşli ve bulutsuz."),
    "SCK":  ("🌡️", "Sıcak",                                  "Hava sıcaklığı mevsim normallerinin üzerinde."),
    "SGK":  ("🧊",  "Soğuk",                                  "Hava sıcaklığı mevsim normallerinin altında."),
    "AB":   ("🌤️", "Az Bulutlu",                              "Gökyüzünün az bir kısmı bulutlu, genelde güneşli."),
    "PB":   ("⛅",  "Parçalı Bulutlu",                        "Gökyüzünün yaklaşık yarısı bulutlu."),
    "CB":   ("☁️",  "Çok Bulutlu",                            "Gökyüzü bulutlarla kaplı, güneş zor görünüyor."),
    "DMN":  ("🌫️", "Duman",                                   "Hava dumanlı, görüş mesafesi azalmış."),
    "PUS":  ("🌫️", "Pus",                                    "Havada ince pus var, görüş hafif kısıtlı."),
    "SIS":  ("🌁",  "Sis",                                    "Yoğun sis, görüş mesafesi oldukça düşük."),
    "HY":   ("🌦️", "Hafif Yağmurlu",                         "Hafif ve aralıklı yağmur bekleniyor."),
    "Y":    ("🌧️", "Yağmurlu",                               "Sürekli ve orta şiddetli yağmur."),
    "KY":   ("⛈️",  "Kuvvetli Yağmurlu",                     "Şiddetli ve yoğun yağmur."),
    "HSY":  ("🌦️", "Hafif Sağanak Yağışlı",                  "Kısa süreli, hafif sağanak yağış."),
    "SY":   ("🌧️", "Sağanak Yağışlı",                       "Kısa süreli fakat kuvvetli sağanak yağış."),
    "KSY":  ("⛈️",  "Kuvvetli Sağanak Yağışlı",              "Şiddetli ve ani sağanak yağış."),
    "HKY":  ("🌨️", "Hafif Kar Yağışlı",                      "Hafif şiddette kar yağışı."),
    "K":    ("❄️",  "Kar Yağışlı",                           "Orta şiddetli kar yağışı."),
    "YKY":  ("❄️",  "Yoğun Kar Yağışlı",                    "Çok yoğun kar yağışı ve birikim."),
    "YYSY": ("🌦️", "Yer Yer Sağanak Yağışlı",                "Bölgesel olarak sağanak yağış geçişleri."),
    "MSY":  ("🌦️", "Mevzi Sağanak Yağışlı",                  "Kısa süreli mevzi sağanak yağış."),
    "D":    ("🌨️", "Dolu",                                   "Bölgesel dolu yağışı."),
    "GSY":  ("⛈️",  "Gökgürültülü Sağanak Yağışlı",          "Gök gürültüsü ve şimşekle birlikte sağanak."),
    "GGSY": ("⛈️",  "Gökgürültülü Sağanak Yağışlı",          "Gök gürültüsü ve şimşekle birlikte sağanak."),
    "KGSY": ("🌩️", "Kuvvetli Gökgürültülü Sağanak Yağışlı",  "Şiddetli fırtına, yıldırım ve yoğun sağanak."),
    "KGY":  ("🌩️", "Kuvvetli Gökgürültülü Sağanak Yağışlı",  "Şiddetli fırtına, yıldırım ve yoğun sağanak."),
    "KKY":  ("🌨️", "Karla Karışık Yağmurlu",                 "Yağmur ve kar bir arada yağıyor."),
    "R":    ("💨",  "Rüzgarlı",                               "Kuvvetli rüzgar esiyor."),
    "KF":   ("🌪️", "Toz veya Kum Fırtınası",                 "Toz ve kum fırtınası nedeniyle görüş çok kısıtlı."),
    "GKR":  ("🎐",  "Güneyli Kuvvetli Rüzgar",                "Güney yönlerden kuvvetli rüzgar (Lodos vb.)."),
    "KKR":  ("🎐",  "Kuzeyli Kuvvetli Rüzgar",                "Kuzey yönlerden kuvvetli rüzgar (Poyraz vb.)."),
}

WMO_HADISE = {
    0:  ("☀️",  "Açık",                    "Hava açık ve güneşli."),
    1:  ("🌤️", "Çoğunlukla Açık",         "Gökyüzü büyük ölçüde açık."),
    2:  ("⛅",  "Parçalı Bulutlu",         "Bulutlanma artıyor."),
    3:  ("☁️",  "Kapalı",                 "Gökyüzü tamamen bulutlu."),
    45: ("🌫️", "Sisli",                   "Sis var, görüş kısıtlı."),
    48: ("🌫️", "Dondurucu Sis",           "Buzlanma oluşturan yoğun sis."),
    51: ("🌦️", "Hafif Çisenti",           "Hafif çisenti yağıyor."),
    53: ("🌦️", "Orta Çisenti",            "Orta yoğunlukta çisenti."),
    55: ("🌦️", "Yoğun Çisenti",           "Yoğun çisenti."),
    61: ("🌧️", "Hafif Yağmur",            "Hafif yağmur yağıyor."),
    63: ("🌧️", "Orta Yağmur",             "Orta şiddetli yağmur."),
    65: ("🌧️", "Kuvvetli Yağmur",         "Şiddetli yağmur."),
    66: ("🌨️", "Dondurucu Hafif Yağmur",  "Yüzeyde buz oluşturan hafif yağmur."),
    67: ("🌨️", "Dondurucu Yağmur",        "Yüzeyde buz oluşturan yağmur."),
    71: ("❄️",  "Hafif Kar",              "Hafif kar yağışı."),
    73: ("❄️",  "Orta Kar",               "Orta şiddetli kar."),
    75: ("❄️",  "Yoğun Kar",              "Yoğun kar yağışı ve birikim."),
    77: ("🌨️", "Kar Taneleri",            "Buz kristalleri veya kar taneleri."),
    80: ("🌦️", "Hafif Sağanak",           "Kısa süreli hafif sağanak."),
    81: ("🌧️", "Orta Sağanak",            "Kısa süreli orta sağanak."),
    82: ("⛈️",  "Şiddetli Sağanak",       "Şiddetli sağanak yağış."),
    85: ("❄️",  "Hafif Kar Sağanağı",     "Kısa süreli hafif kar sağanağı."),
    86: ("❄️",  "Yoğun Kar Sağanağı",    "Şiddetli kar sağanağı."),
    95: ("⛈️",  "Fırtına",               "Gökgürültülü fırtına."),
    96: ("⛈️",  "Hafif Dolulu Fırtına",  "Hafif dolu eşliğinde fırtına."),
    99: ("⛈️",  "Kuvvetli Dolulu Fırtına","Yoğun dolu ile şiddetli fırtına."),
}

PILL_TOOLTIPS = {
    "💧 Nem":           "Bağıl Nem (%)\\nHavadaki su buharının oranı.\\n✦ %40–60 konforlu • %60+ bunaltıcı",
    "💨 Rüzgar":        "Rüzgar Hızı ve Yönü (km/s)",
    "🔵 Basınç":        "Denize İndirgenmiş Basınç (hPa)\\n✦ Normal ~1013 hPa",
    "👁 Görüş":         "Yatay Görüş Mesafesi\\n✦ <1 km: Yoğun sis • 10 km+: Açık",
    "🌧 Yağış 1s":      "Son 1 Saatlik Yağış (mm)",
    "🌧 Yağış 24s":     "Son 24 Saatlik Toplam Yağış (mm)",
    "🌊 Deniz":         "Deniz Yüzeyi Sıcaklığı (°C)",
    "☁ Bulutluluk":     "Gökyüzü Bulut Örtüsü (okta/yüzde)",
    "❄ Kar":            "Yerde Biriken Kar Kalınlığı (cm)",
    "🔆 UV İndeksi":    "UV Işıma İndeksi\\n✦ 0–2: Düşük • 3–5: Orta • 6–7: Yüksek • 8+: Çok Yüksek",
    "🌂 Yağış Olas.":   "Yağış Olasılığı %\\n✦ <30%: Olası değil • 80%+: Çok muhtemel",
    "💨 Rüzgar Gustu":  "Anlık En Yüksek Rüzgar Hızı (km/s)",
    "🌡 Çiğ Noktası":   "Çiğ Noktası Sıcaklığı (°C)",
    "☀ Güneşlenme":     "Günlük Güneşlenme Süresi (saat)",
    "🌡 Hissedilen":    "Hissedilen (Apparent) Sıcaklık (°C)",
}

TRAY_ICONS = {
    "A":"weather-clear","SCK":"weather-clear","SGK":"weather-snow",
    "AB":"weather-few-clouds","PB":"weather-clouds","CB":"weather-overcast",
    "DMN":"weather-fog","PUS":"weather-fog","SIS":"weather-fog",
    "HY":"weather-showers-scattered","Y":"weather-showers","KY":"weather-storm",
    "HSY":"weather-showers-scattered","SY":"weather-showers","KSY":"weather-storm",
    "HKY":"weather-snow","K":"weather-snow","YKY":"weather-snow",
    "YYSY":"weather-showers-scattered","D":"weather-snow","MSY":"weather-showers-scattered",
    "GSY":"weather-storm","GGSY":"weather-storm","KGSY":"weather-storm","KGY":"weather-storm",
    "KKY":"weather-snow",
    "R":"weather-wind","KF":"weather-fog",
    "GKR":"weather-windy","KKR":"weather-windy",
}

WMO_TRAY = {
    0:"weather-clear",1:"weather-few-clouds",2:"weather-clouds",
    3:"weather-overcast",45:"weather-fog",48:"weather-fog",
    51:"weather-showers-scattered",53:"weather-showers-scattered",55:"weather-showers",
    61:"weather-showers-scattered",63:"weather-showers",65:"weather-storm",
    71:"weather-snow",73:"weather-snow",75:"weather-snow",
    80:"weather-showers-scattered",81:"weather-showers",82:"weather-storm",
    95:"weather-storm",96:"weather-storm",99:"weather-storm",
}

YONLER = ["K","KKD","KD","DKD","D","DGD","GD","GGD","G","GGB","GB","BGB","B","BBK","BK","KBK"]
METEOALARM_SEVIYE = {"1":"Yeşil","2":"Sarı ⚠","3":"Turuncu ⚠⚠","4":"Kırmızı 🔴"}

# ─── Yardımcı Fonksiyonlar ────────────────────────────────────────────────
