[🇹🇷 Türkçe](README.md)

![MintSky Header](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

<p align="center">
  <a href="https://github.com/tarihcituranx/mintsky/actions"><img src="https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-audit.yaml?branch=main&label=MintSky%20CI" alt="MintSky CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python&logoColor=white" alt="Python 3"></a>
  <a href="https://www.gtk.org/"><img src="https://img.shields.io/badge/GTK-3-orange.svg?style=flat&logo=gnome&logoColor=white" alt="GTK3"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg?style=flat&logo=linux" alt="Platform: Linux"></a>
</p>

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=520&lines=MintSky+-+Linux+Weather+App+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;System+Tray+Widget+%F0%9F%94%94;Live+Finance+%2B+Portfolio+%F0%9F%92%B0;Open+Source+%26+Free+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

MintSky is a **next-generation GTK3 desktop weather and assistant application** built specifically for Linux desktop environments (especially Linux Mint, Ubuntu, Debian derivatives). It combines data from the Turkish Meteorological Service (MGM), Open-Meteo, and MSN Weather through an intelligent fallback chain. Beyond weather, it's a full desktop assistant with Groq LLaMA AI, Edge-TTS voice reading, live finance tracking, and portfolio management.

## 🌟 Features

### 🌦️ Weather Engine
* **Triple API + Smart Fallback:** MGM (Turkish official), Open-Meteo (global backup), and MSN Weather API work in a chain. If one fails, the next one takes over automatically.
* **Real-time Data:** Temperature, feels-like, humidity, pressure, wind speed/direction/gust, dew point, cloud cover, visibility.
* **UV Index & Precipitation:** Real-time UV, precipitation amount, and snow data from Open-Meteo — cross-validated across multiple sources.
* **Hourly & 5-Day Forecast:** Hourly temperature, precipitation probability, wind, and UV forecasts; 5-day day/night min/max graphs.
* **Sunrise / Sunset:** Daily sun times from Open-Meteo for every forecast day.
* **MGM Alarms & MeteoAlarm:** Official meteorological alerts (storms, floods, frost, etc.) displayed in real time. Desktop notification fires when a new alarm appears.
* **Air Quality (AQI):** Real-time Air Quality Index from MSN Weather API.
* **Nominatim Fallback:** For locations not registered in MGM, OpenStreetMap Nominatim resolves coordinates and feeds Open-Meteo + MSN for forecasts.

### 🤖 AI & Voice Assistant
* **Groq LLaMA AI:** Clothing advice, outdoor activity recommendations, and weather-specific insights via Groq API (LLaMA model). Works without an API key too (shows a warning).
* **Edge-TTS Voice Reading:** Reads AI advice aloud asynchronously using Microsoft Edge TTS in a natural human voice. The system `edge-tts` CLI is found automatically.
* **AI Dialog Window:** A standalone window streams the AI response while showing current weather conditions.

### 💰 Live Finance Module (Truncgil Finance API)
* **Gold & Precious Metals:** Gram Gold, Quarter Gold, Half Gold, Full Gold, Republic Gold, Silver and more — selectable per user preference.
* **Currency:** USD, EUR, GBP, JPY, CHF, CAD, AUD, SAR, SEK, NOK and more — selectable.
* **Crypto Infrastructure:** Truncgil API infrastructure for 40+ coins (Bitcoin, Ethereum, Solana, etc.) is in place *(full portfolio UI integration planned)*.
* **Portfolio Tracking:** Build a portfolio of gold and currency assets with purchase prices; see real-time **profit/loss** calculation. Purchase price field auto-fills with current market price.
* **2-Minute Cache:** Finance data refreshes every 120 seconds, keeping API load minimal.

### 🖥️ Interface & Usability
* **Compact Widget Mode:** One click transforms the app into a pinned desktop corner widget. In compact mode: current temperature + 3-hour forecast are shown.
* **System Tray (AppIndicator3 & libnotify):** Runs silently in the background. Right-click tray icon for weather summary, left-click to open. Auto-detects AyatanaAppIndicator3 (Ubuntu/Mint) and classic AppIndicator3.
* **Desktop Notifications:** Sends clean GTK notifications via libnotify for weather alarms, app updates, and major weather changes.
* **Autostart:** One-click enable/disable startup at login. A `.desktop` file is automatically written to `~/.config/autostart/`.
* **Install as App:** Adds a permanent icon and `.desktop` entry to the system menu (`~/.local/share/applications/`).
* **Auto Update Check:** Checks GitHub for the latest version on startup; shows a banner and offers one-click update if newer.
* **Favorites:** Save frequently visited cities and load them with one click.
* **Cache System:** Weather data is cached for `WEATHER_CACHE_TTL` seconds — window resizing or re-opening is instant.
* **Keyboard Shortcuts:** `Ctrl+R` to refresh, `Escape` to hide, `Ctrl+F` to focus city search.
* **Lucide SVG Icons & GTK3 Theme Compatibility:** 100% native GTK3 rendering, adapts to your desktop theme (dark/light).

### 🌐 Multi-Language (i18n)
All UI text is driven by JSON locale files. **Turkish** and **English** are fully supported. Infrastructure exists for German, French, Arabic, Persian, Chinese, and Azerbaijani. Language can be changed instantly from Settings. TTS voice automatically matches the selected language (8 voice profiles).

### ♿ Accessibility (A11y)
GTK3's built-in accessibility layer is active. Basic keyboard navigation and screen reader (e.g. Orca) support is available via GTK3 defaults.

### 🔐 Security
* API keys (Groq) are stored encrypted in the system **keyring** — never written to the JSON settings file.
* MSN API credentials are read from environment variables (`MSN_API_KEY`, `MSN_APP_ID`) — no hardcoded values in source.
* Portfolio file permissions are set to `0o600` (owner-read only).

---

## 📸 Screenshots

<p align="center">
  <img src="assets/scr_main.png" width="48%" alt="MintSky Overview" />
  <img src="assets/scr_daily.png" width="48%" alt="Hourly & Daily Forecasts" />
</p>
<p align="center">
  <img src="assets/scr_ai.png" width="48%" alt="AI Insights & Details" />
  <img src="assets/scr_finance.png" width="48%" alt="Live Finance Module" />
</p>

---

## ⚙️ Installation

### 1. System Dependencies (Debian / Ubuntu / Linux Mint)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo \
  gir1.2-appindicator3-0.1 gir1.2-notify-0.7 libnotify-bin
```
> **Ubuntu 22.04+ / Linux Mint 22+** users may need `gir1.2-ayatanaappindicator3-0.1` instead of `gir1.2-appindicator3-0.1`. The app detects both automatically.

### 2. Clone & Install
```bash
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky
pip3 install . --break-system-packages
```
This automatically installs `requests`, `PyGObject`, `groq`, `edge-tts`, and `keyring` from `requirements.txt`.

*(For a safer approach use `pipx install .` or `python3 -m venv .venv && source .venv/bin/activate && pip install .`)*

### 3. Run
```bash
mintsky
# or in desktop widget mode:
mintsky --autostart
```

---

## 🛠️ Configuration

| Setting | How |
|---|---|
| **Groq API Key** | `Settings → 🤖 AI` tab — get a free [Groq API Key](https://console.groq.com/keys). Stored encrypted in keyring. |
| **Pin Location** | Search a city and press "⭐ Pin" — loads that location on every startup. |
| **Finance Panel** | `Settings → 💰 Finance` tab — select gold instruments, currencies to display. |
| **Language** | `Settings → ⚙️ System` tab — TR / EN selection. |
| **Autostart** | Toggle in `Settings → ⚙️ System` to launch at login. |
| **MSN API** | Set `MSN_API_KEY` and `MSN_APP_ID` environment variables (optional, needed for AQI). |

---

## 🚀 Roadmap (Planned Features)

* **Chameleon Hybrid Architecture:**
  * Native **GTK4/Libadwaita** support for GNOME and Fedora users.
  * Native **Cross-Platform GUI (PyQt/Tkinter)** for Windows and macOS — UI loads automatically based on the host OS.
* **Crypto Portfolio UI:** Full portfolio management UI for the 40+ supported cryptocurrencies.

---

## 💻 Technology Stack

| Technology | Type | Description |
| :--- | :--- | :--- |
| **Python 3.10+** | Core | Async background tasks, thread pool |
| **GTK3 (PyGObject)** | UI | Native Linux GUI, AppIndicator3, libnotify |
| **Groq (LLaMA)** | LLM | Ultra-fast AI weather analysis |
| **Edge-TTS** | TTS | Microsoft-backed async voice synthesis |
| **MGM API** | Weather | Turkish official data + alarms + MeteoAlarm |
| **Open-Meteo** | Weather (fallback) | UV, hourly & 5-day forecast, sunrise/sunset |
| **MSN Weather** | Weather (extra) | AQI, real-time feels-like temperature |
| **Nominatim (OSM)** | Geocoding | Coordinate resolution for unlisted locations |
| **Truncgil Finance** | Finance | Real-time gold, currency, crypto rates |
| **keyring** | Security | Encrypted API key storage in OS secure store |
| **Pytest & GitHub Actions** | Test & CI | Mock-based scenario tests, bandit security scan |

---

## 🤝 Contributing

MintSky is open to everyone. Open a [Pull Request](https://github.com/tarihcituranx/mintsky/pulls) to add features, new locale files, or bug fixes.

> **Disclaimer:** MintSky is developed for personal use and testing. No liability is accepted for inaccuracies in API data. Developed on Linux Mint 22.3 "Zena" — runs on any modern GTK3-compatible Linux distribution.

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
