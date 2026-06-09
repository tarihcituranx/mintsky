[🇹🇷 Türkçe](README.md)

![MintSky Header](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=MintSky&fontSize=70&fontColor=ffffff)

[![CI](https://img.shields.io/github/actions/workflow/status/tarihcituranx/mintsky/mintsky-docs-update.yaml?branch=main&label=MintSky%20CI)](https://github.com/tarihcituranx/mintsky/actions)
![Python 3](https://img.shields.io/badge/Python-3-3776AB?style=flat&logo=python&logoColor=white)
![GTK3](https://img.shields.io/badge/GTK-3-7FE717?style=flat&logo=gnome&logoColor=white)
![GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)
![Platform: Linux](https://img.shields.io/badge/Platform-Linux-E34F26?style=flat&logo=linux&logoColor=white)

<p align="center"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=764BA2&width=450&lines=MintSky+-+Linux+Weather+%F0%9F%8C%A4%EF%B8%8F;GTK3+%2B+Groq+AI+%F0%9F%A4%96;Track+from+System+Tray+%F0%9F%94%94;Open+Source+%26+Free+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" /></p>

## 🌟 Features

* 🌤️ **Real-Time Weather:** Track current weather conditions, temperature, and forecasts for your city.
* 🤖 **Groq AI Integration:** Get smart, AI-generated weather summaries, outdoor activity suggestions, and clothing recommendations.
* 🔔 **System Tray Support:** Runs quietly in the background using `AppIndicator3` with native system tray integration.
* 💬 **Desktop Notifications:** Receive instant weather alerts and updates via `libnotify`.
* 🎨 **Modern GTK3 Interface:** A clean, lightweight, and native user interface designed specifically for Linux desktop environments.

## 📸 Screenshots

> *Screenshots of the main window and system tray menu will be displayed here.*

| Main Dashboard | System Tray Menu |
| :---: | :---: |
| _[Screenshot Placeholder - Main UI]_ | _[Screenshot Placeholder - Tray]_ |

## 🚀 Installation

Follow these steps to install and run MintSky on your Linux system.

### 1. Install System Dependencies

For Debian/Ubuntu-based distributions:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-appindicator3-0.1 libnotify-bin
```

### 2. Clone the Repository

```bash
git clone https://github.com/tarihcituranx/mintsky.git
cd mintsky
```

### 3. Install Python Packages

```bash
pip3 install -r requirements.txt
```

### 4. Run the Application

```bash
python3 main.py
```

## ⚙️ Configuration

Upon the first launch, MintSky will generate a configuration file where you can customize your experience:

* **API Key:** Insert your Groq API key to enable AI-powered weather insights.
* **City Settings:** Set your default location for localized weather reports.
* **Theme Preferences:** Toggle between light and dark modes to match your system theme.

## 🛠️ Technology Stack

| Technology | Type | Description |
| :--- | :--- | :--- |
| **Python 3** | Language | Core application logic |
| **GTK3 (PyGObject)** | GUI Framework | Native Linux user interface |
| **AppIndicator3** | System Tray | Background execution and tray icon management |
| **libnotify** | Notifications | Native desktop notification delivery |
| **Groq API** | AI Engine | LLM-powered personalized weather summaries |
| **Requests** | Networking | API communication and data fetching |

## 🤝 Contributing

Contributions are welcome! If you want to improve MintSky, please feel free to fork the repository, make your changes, and submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

👉 [Submit a Pull Request](https://github.com/tarihcituranx/mintsky/pulls)

![MintSky Footer](https://capsule-render.vercel.app/api?type=waving&color=0:764ba2,100:667eea&height=120&section=footer)
