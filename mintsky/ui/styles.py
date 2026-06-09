def make_css(scale_val, theme="dark"):
    def fs(n): return int(round(n * scale_val))
    if theme == "light":
        bg,card_bg       = "#f6f8fa","#ffffff"
        card_grad        = "linear-gradient(135deg,#ffffff 0%,#f0f3f6 100%)"
        hdr_grad         = "linear-gradient(160deg,#ffffff 0%,#f6f8fa 100%)"
        border           = "#d0d7de"
        text_main        = "#24292f"
        text_sub         = "#57606a"
        text_mut         = "#8c959f"
        text_accent      = "#0969da"
        entry_bg,btn_bg  = "#ffffff","#f3f4f6"
        btn_hover        = "#ebecf0"
        btn_active       = "#e5e7eb"
        w3_bg            = "#edf0f3"
        groq_bg          = "#e8f4fd"
        groq_border      = "#b8d4f0"
        groq_text        = "#0550ae"
    else:
        bg,card_bg       = "#0d1117","#1c2128"
        card_grad        = "linear-gradient(135deg,#161b22 0%,#1c2128 100%)"
        hdr_grad         = "linear-gradient(160deg,#161b22 0%,#0d1117 100%)"
        border           = "#30363d"
        text_main        = "#e6edf3"
        text_sub         = "#c9d1d9"
        text_mut         = "#8b949e"
        text_accent      = "#58a6ff"
        entry_bg,btn_bg  = "#161b22","#21262d"
        btn_hover        = "#30363d"
        btn_active       = "#161b22"
        w3_bg            = "#1a2030"
        groq_bg          = "#0d2137"
        groq_border      = "#1f4e7a"
        groq_text        = "#79c0ff"

    return f"""
/* ===================== MINTSKY GLOBAL ===================== */
* {{
    font-family: "Segoe UI", Ubuntu, Cantarell, sans-serif;
    font-size: {fs(13)}px;
    color: {text_main};
    outline: none;
    box-shadow: none;
}}

/* ===================== ANA PENCERE ===================== */
window, .main-window {{
    background-color: {bg};
    border-radius: 12px;
}}

/* ===================== HEADER ===================== */
.header-box {{
    background: {hdr_grad};
    border-bottom: 1px solid {border};
    padding: {fs(12)}px {fs(16)}px;
    border-radius: 12px 12px 0 0;
}}

.app-title {{
    font-size: {fs(16)}px;
    font-weight: bold;
    color: {text_main};
}}

.app-subtitle {{
    font-size: {fs(11)}px;
    color: {text_mut};
}}

/* ===================== KARTLAR ===================== */
.card {{
    background: {card_grad};
    border: 1px solid {border};
    border-radius: 8px;
    padding: {fs(12)}px;
    margin: {fs(6)}px;
}}

.card-bg {{
    background-color: {card_bg};
    border: 1px solid {border};
    border-radius: 8px;
    padding: {fs(10)}px;
}}

/* ===================== WEATHER / W3 ===================== */
.weather-box {{
    background-color: {w3_bg};
    border: 1px solid {border};
    border-radius: 8px;
    padding: {fs(10)}px {fs(14)}px;
}}

.weather-temp {{
    font-size: {fs(32)}px;
    font-weight: bold;
    color: {text_accent};
}}

.weather-desc {{
    font-size: {fs(12)}px;
    color: {text_sub};
    margin-top: {fs(2)}px;
}}

.weather-meta {{
    font-size: {fs(11)}px;
    color: {text_mut};
}}

/* ===================== GROQ AI ===================== */
.groq-box {{
    background-color: {groq_bg};
    border: 1px solid {groq_border};
    border-radius: 8px;
    padding: {fs(10)}px {fs(14)}px;
    margin-top: {fs(6)}px;
}}

.groq-label {{
    font-size: {fs(12)}px;
    font-weight: 600;
    color: {groq_text};
}}

.groq-response {{
    font-size: {fs(13)}px;
    color: {text_main};
    margin-top: {fs(4)}px;
}}

/* ===================== BUTONLAR ===================== */
button {{
    background-color: {btn_bg};
    border: 1px solid {border};
    border-radius: 6px;
    color: {text_main};
    font-size: {fs(13)}px;
    padding: {fs(5)}px {fs(12)}px;
    transition: background-color 150ms ease;
}}

button:hover {{
    background-color: {btn_hover};
    border-color: {text_accent};
    color: {text_accent};
}}

button:active {{
    background-color: {btn_active};
}}

button.accent {{
    background-color: {text_accent};
    border-color: {text_accent};
    color: #ffffff;
    font-weight: 600;
}}

button.accent:hover {{
    opacity: 0.85;
}}

/* ===================== ENTRY ===================== */
entry {{
    background-color: {entry_bg};
    border: 1px solid {border};
    border-radius: 6px;
    color: {text_main};
    font-size: {fs(13)}px;
    padding: {fs(6)}px {fs(10)}px;
    caret-color: {text_accent};
}}

entry:focus {{
    border-color: {text_accent};
}}

entry placeholder {{
    color: {text_mut};
}}

/* ===================== SCROLLBAR ===================== */
scrollbar {{
    background-color: transparent;
    border: none;
}}

scrollbar slider {{
    background-color: {border};
    border-radius: 4px;
    min-width: 5px;
    min-height: 5px;
    margin: 2px;
}}

scrollbar slider:hover {{
    background-color: {text_mut};
}}

/* ===================== ETİKETLER ===================== */
.label-main {{
    font-size: {fs(14)}px;
    color: {text_main};
}}

.label-sub {{
    font-size: {fs(12)}px;
    color: {text_sub};
}}

.label-muted {{
    font-size: {fs(11)}px;
    color: {text_mut};
}}

.label-accent {{
    font-size: {fs(13)}px;
    font-weight: 600;
    color: {text_accent};
}}

/* ===================== AYIRICI ===================== */
separator {{
    background-color: {border};
    min-height: 1px;
    margin: {fs(4)}px 0;
}}

/* ===================== CHECKBUTTON / SWITCH ===================== */
checkbutton, radiobutton {{
    color: {text_main};
    font-size: {fs(13)}px;
    padding: {fs(2)}px;
}}

switch {{
    border-radius: 14px;
}}

switch:checked {{
    background-color: {text_accent};
}}

/* ===================== TOOLTIP ===================== */
tooltip {{
    background-color: {card_bg};
    border: 1px solid {border};
    border-radius: 6px;
    color: {text_sub};
    font-size: {fs(12)}px;
    padding: {fs(4)}px {fs(8)}px;
}}
"""
