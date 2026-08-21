[🇹🇷 Türkçe](README.md)

![MintSky Header](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

<p align="center">
  <a href="https://github.com/tarihcituranx/mintsky/actions"><img src="https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-audit.yaml?branch=main&label=MintSky%20CI" alt="MintSky CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3"></a>
  <a href="https://www.gtk.org/"><img src="https://img.shields.io/badge/GTK-3-7FE717?style=flat&logo=gnome&logoColor=white" alt="GTK3"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"></a>
  <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Platform-Linux-E34F26?style=flat&logo=linux&logoColor=white" alt="Platform: Linux"></a>
</p>

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=450&lines=MintSky+-+Linux+Weather+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;Track+from+System+Tray+%F0%9F%94%94;Open+Source+%26+Free+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

MintSky is a next-generation, **GTK3-based desktop weather and assistant application** designed specifically for Linux desktop environments (Linux Mint, Ubuntu, Debian derivatives). It combines MGM (Turkey), Open-Meteo, and MSN Weather APIs with a smart fallback mechanism. It acts as a full-fledged personal assistant using the built-in Groq LLaMA AI and Edge-TTS to provide and *speak* context-aware weather recommendations.

## 🌟 Features

* 🌍 **Smart Multi-API Engine & AQI:** Automatically switches between Open-Meteo (Global), MGM (Turkish official data), and **MSN Weather (Extra Sensors)**. Protects your health with interactive Air Quality Index (AQI) alerts.
* 🤖 **Groq AI & Edge-TTS Assistant:** Provides smart AI-powered recommendations based on the weather, like "what to wear today" or "should you take an umbrella". Powered by **Edge-TTS**, it reads these suggestions to you in one of the most natural-sounding human voices!
* 📈 **Live Finance Module:** Track real-time gold, foreign exchange (USD, EUR), and cryptocurrency markets via the Truncgil API. Calculate the instant profit/loss status of your personal portfolio.
* 🎨 **Lucide Vector Design & Smooth GTK3 Interface:** A sleek, fully native GUI equipped with modern Lucide SVG icons and full system dark/light mode integration. Common desktop issues like scrolling glitches and layout overflows are completely resolved.
* ♿ **100% Accessibility (A11y):** All UI buttons, inputs, and tabs are tagged with the `Atk` library for visually impaired users. It is perfectly compatible with all Linux screen readers (e.g., Orca) and fully keyboard-navigable.
* 🌐 **8 Different Languages (i18n):** Native support for English, Turkish, German, French, Arabic, Persian, Chinese, and Azerbaijani. Highly extensible via modular `.json` localization files (similar to Telegram).
* 🔔 **System Tray & Notifications (AppIndicator3 & libnotify):** Runs silently in the background with minimal RAM/CPU footprint, and alerts you to sudden weather changes with stylish desktop notifications.

## 📸 Screenshots

<p align="center">
  <img src="assets/scr_main.png" width="48%" alt="MintSky Overview" />
  <img src="assets/scr_daily.png" width="48%" alt="Hourly and Daily Forecasts" />
</p>
<p align="center">
  <img src="assets/scr_ai.png" width="48%" alt="AI Comments and Details" />
  <img src="assets/scr_finance.png" width="48%" alt="Live Finance Module" />
</p>

## ⚙️ Installation & Usage

It is quite easy to install MintSky on your system.

### 1. System Dependencies (Debian / Ubuntu / Linux Mint)
Open your terminal and install the PyGObject, GTK3 libraries, and system extensions:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-appindicator3-0.1 libnotify-bin
```

### 2. Download and Install
Clone the repository to your computer and install it via `pip`:
```bash
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky
pip3 install . --break-system-packages
```
*(Note: If you encounter a `pip` error regarding an externally managed environment, you can safely use the `--break-system-packages` flag or opt for `pipx` or a virtual environment `venv` depending on your preference.)*

### 3. Launch
Once the installation is complete, you can start the application by running:
```bash
mintsky
```

## 🛠️ Basic Configuration

* **Groq API Key:** To enable AI recommendations, get a free [Groq API Key](https://console.groq.com/keys) and enter it in the `Settings` tab. (Your keys are securely encrypted on your device using your OS keyring).
* **Pin Location:** After searching for a city, click the "Pin" (Sabitle) button to load that location's data by default on every startup.
* **Finance Dashboard:** Access live markets from the `Finance` button at the top right, and configure your portfolio assets via the settings screen.

## 💻 Technology Stack

| Technology | Type | Description |
| :--- | :--- | :--- |
| **Python 3** | Core Language | Application logic and operations |
| **GTK3 (PyGObject)** | GUI Framework | Native Linux user interface library |
| **AppIndicator3** | System | Background execution and tray integration |
| **Groq LLaMA** | LLM Engine | Ultra-fast LLM for weather context analysis |
| **Edge-TTS** | Speech | Natural text-to-speech engine via Microsoft |
| **MGM & Open-Meteo & MSN** | Weather APIs | Multi-provider architecture with dynamic fall-backs |
| **Truncgil API** | Finance API | Instant local and global market rates |
| **Pytest & GitHub Actions** | Test & CI | Comprehensive API mocking and continuous integration |

## 🤝 Contributing

MintSky is an open project welcoming community contributions. If you want to add a new feature, expand the translation files, or fix a bug, feel free to open a [Pull Request (PR)](https://github.com/tarihcituranx/mintsky/pulls).

> **Disclaimer:** MintSky is a weather and finance tracking application developed for testing purposes; no liability is accepted for any material or moral damages arising from API data inaccuracies. It is primarily developed on Linux Mint 22.3 "Zena," but it runs flawlessly on all modern distributions that satisfy the GTK dependencies.

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
