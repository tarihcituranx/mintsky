def make_css(scale_val, theme="dark"):
    def fs(n): return int(round(n * scale_val))
    if theme == "light":
        bg,card_bg       = "#f0f4f8","#ffffff"
        card_grad        = "linear-gradient(145deg,#ffffff 0%,#eef2f7 100%)"
        hdr_grad         = "linear-gradient(160deg,#ffffff 0%,#f0f4f8 100%)"
        border           = "#d0d7de"
        text_main        = "#0f172a"
        text_sub         = "#334155"
        text_mut         = "#475569"
        text_accent      = "#0969da"
        entry_bg,btn_bg  = "#ffffff","#f0f3f7"
        btn_hover        = "#e5e9f0"
        btn_active       = "#dde3eb"
        w3_bg            = "#e8edf3"
        groq_bg          = "#e8f4fd"
        groq_border      = "#b8d4f0"
        groq_text        = "#0550ae"
        fin_bg           = "#fff8e7"
        fin_border       = "#f0d070"
        fin_profit       = "#22863a"
        fin_loss         = "#cb2431"
        fin_title        = "#7a5c00"
        pill_shadow      = "rgba(0,0,0,0.08)"
    else:
        bg,card_bg       = "#0a0e17","#141b2d"
        card_grad        = "linear-gradient(145deg,#161e30 0%,#0f1520 100%)"
        hdr_grad         = "linear-gradient(160deg,#161e30 0%,#0a0e17 100%)"
        border           = "#253046"
        text_main        = "#f8fafc"
        text_sub         = "#cbd5e1"
        text_mut         = "#94a3b8"
        text_accent      = "#60a5fa"
        entry_bg,btn_bg  = "#101828","#1e2d42"
        btn_hover        = "#253046"
        btn_active       = "#111c2d"
        w3_bg            = "#111c2f"
        groq_bg          = "#0d1f35"
        groq_border      = "#1e4170"
        groq_text        = "#7cb9ff"
        fin_bg           = "#1a1500"
        fin_border       = "#4a3a00"
        fin_profit       = "#3fb950"
        fin_loss         = "#f85149"
        fin_title        = "#e3b341"
        pill_shadow      = "rgba(0,0,0,0.35)"

    return f"""
* {{ font-family:"Ubuntu","Cantarell",sans-serif; font-size:{fs(15)}px; }}
#main-win {{ background-color:{bg}; }}

/* ─── Header ─── */
.hdr {{ background:{hdr_grad}; padding:{fs(14)}px {fs(18)}px {fs(10)}px {fs(18)}px;
        border-bottom:2px solid {border};
        box-shadow:0 2px 12px {pill_shadow}; }}
.hdr-title {{ font-size:{fs(20)}px; font-weight:900; color:{text_accent};
              letter-spacing:2px; text-shadow:0 1px 4px {pill_shadow}; }}
.search-row {{ margin-top:{fs(8)}px; }}

/* ─── Inputs ─── */
entry {{ background-color:{entry_bg}; color:{text_main}; border:1px solid {border};
         border-radius:8px; padding:{fs(7)}px {fs(12)}px; font-size:{fs(14)}px;
         caret-color:{text_accent}; transition:border-color 0.15s; }}
entry:focus {{ border-color:{text_accent}; background-color:{card_bg};
               box-shadow:0 0 0 3px rgba(96,165,250,0.15); }}

/* ─── Buttons ─── */
.btn-search {{ background:linear-gradient(135deg,#2ecc71,#27ae60); color:#ffffff;
               border:none; border-radius:8px; padding:{fs(7)}px {fs(18)}px;
               font-size:{fs(14)}px; font-weight:bold; min-width:{fs(60)}px;
               box-shadow:0 3px 8px rgba(39,174,96,0.35); }}
.btn-search label {{ color:#ffffff; font-size:{fs(14)}px; font-weight:bold; }}
.btn-search:hover  {{ background:linear-gradient(135deg,#3be07e,#30c26d);
                      box-shadow:0 4px 12px rgba(39,174,96,0.50); }}
.btn-search:active {{ background:linear-gradient(135deg,#25a557,#1f8e4d); }}

.btn-tool {{ background-color:{btn_bg}; color:{text_main}; border:1px solid {border};
             border-radius:8px; padding:{fs(6)}px {fs(10)}px; font-size:{fs(14)}px; min-width:{fs(50)}px;
             box-shadow:0 2px 4px {pill_shadow}; }}
.btn-tool label {{ color:{text_main}; font-size:{fs(14)}px; font-weight:bold; }}
.btn-tool:hover  {{ background-color:{btn_hover}; border-color:{text_accent}; }}
.btn-tool:active {{ background-color:{btn_active}; }}

.btn-ai  {{ background:linear-gradient(135deg,#7c3aed,#5b21b6); color:#ffffff;
            border:1px solid #8b5cf6; border-radius:8px; padding:{fs(6)}px {fs(10)}px; font-size:{fs(14)}px;
            min-width:{fs(50)}px; box-shadow:0 3px 8px rgba(124,58,237,0.35); }}
.btn-ai label {{ color:#ffffff; font-size:{fs(14)}px; font-weight:bold; }}
.btn-ai:hover  {{ background:linear-gradient(135deg,#8b5cf6,#6d28d9);
                  box-shadow:0 4px 12px rgba(124,58,237,0.50); }}
.btn-ai:active {{ background:linear-gradient(135deg,#6d28d9,#5b21b6); }}

.btn-fin {{ background:linear-gradient(135deg,#d4a017,#b8860b); color:#ffffff;
            border:1px solid #c9a227; border-radius:8px; padding:{fs(6)}px {fs(10)}px; font-size:{fs(14)}px;
            min-width:{fs(50)}px; box-shadow:0 3px 8px rgba(184,134,11,0.35); }}
.btn-fin label {{ color:#ffffff; font-size:{fs(14)}px; font-weight:bold; }}
.btn-fin:hover  {{ background:linear-gradient(135deg,#e8b420,#cc9910); }}
.btn-fin:active {{ background:linear-gradient(135deg,#b87b0a,#9a6508); }}

.btn-fav-active {{ background:linear-gradient(135deg,#92400e,#78350f); color:#fbbf24;
                   border:1px solid #d97706; border-radius:8px; padding:{fs(6)}px {fs(10)}px; font-size:{fs(14)}px;
                   min-width:{fs(50)}px; box-shadow:0 3px 8px rgba(217,119,6,0.35); }}
.btn-fav-active label {{ color:#fbbf24; font-size:{fs(14)}px; font-weight:bold; }}
.btn-fav-active:hover {{ background:linear-gradient(135deg,#a45a0e,#8a3f0f); }}

/* ─── Ana kart (şimdiki hava) ─── */
.cur-card {{ background:{card_grad}; border-radius:16px;
             margin:{fs(12)}px {fs(12)}px {fs(6)}px {fs(12)}px; padding:{fs(20)}px;
             border:1px solid {border};
             box-shadow:0 8px 32px {pill_shadow}, 0 2px 8px {pill_shadow}; }}
.cur-city  {{ font-size:{fs(24)}px; font-weight:800; color:{text_main};
              text-shadow:0 1px 4px {pill_shadow}; }}
.cur-cond  {{ font-size:{fs(18)}px; color:{text_sub}; margin-top:{fs(2)}px; font-weight:600; }}
.cur-desc  {{ font-size:{fs(14)}px; color:{text_sub}; margin-top:{fs(4)}px; }}
.cur-temp  {{ font-size:{fs(66)}px; font-weight:200; color:{text_main}; letter-spacing:-3px;
              text-shadow:0 2px 8px {pill_shadow}; }}
.cur-feels {{ font-size:{fs(14)}px; color:{text_sub}; margin-top:-{fs(4)}px; }}
.om-badge  {{ font-size:{fs(12)}px; color:{text_accent}; font-weight:bold; margin-top:{fs(6)}px; }}

/* ─── Pill kartlar ─── */
.pill-box {{ background:linear-gradient(145deg,{card_bg},{entry_bg});
             border-radius:12px; padding:{fs(10)}px {fs(14)}px; margin:3px;
             border:1px solid {border};
             box-shadow:0 4px 12px {pill_shadow}, inset 0 1px 0 rgba(255,255,255,0.06); }}
.pill-key {{ font-size:{fs(13)}px; color:{text_sub}; }}
.pill-val {{ font-size:{fs(15)}px; font-weight:700; color:{text_main}; margin-top:2px; }}

/* ─── Bölüm başlıkları ─── */
.sec-title {{ font-size:{fs(13)}px; font-weight:800; color:{text_mut}; letter-spacing:1.5px;
              margin:{fs(14)}px {fs(12)}px {fs(6)}px {fs(12)}px; }}

/* ─── Saatlik tahmin ─── */
.h-card {{ background:linear-gradient(145deg,{entry_bg},{btn_bg}); border-radius:12px;
           padding:{fs(10)}px; margin:2px; border:1px solid {border};
           min-width:{fs(75)}px;
           box-shadow:0 3px 8px {pill_shadow}, inset 0 1px 0 rgba(255,255,255,0.05); }}
.h-time  {{ font-size:{fs(13)}px; color:{text_sub}; font-weight:700; }}
.h-emoji {{ font-size:{fs(26)}px; }}
.h-temp  {{ font-size:{fs(16)}px; font-weight:700; color:{text_main}; }}
.h-wind  {{ font-size:{fs(12)}px; color:{text_accent}; font-weight:600; }}

/* ─── Günlük tahmin ─── */
.fc-row  {{ background:linear-gradient(135deg,{entry_bg},{btn_bg});
            border-radius:12px; padding:{fs(12)}px {fs(14)}px;
            margin:{fs(3)}px {fs(12)}px; border:1px solid {border};
            box-shadow:0 3px 8px {pill_shadow}; }}
.fc-day  {{ font-size:{fs(15)}px; color:{text_main}; font-weight:700; }}
.fc-cond {{ font-size:{fs(14)}px; color:{text_sub}; }}
.fc-desc {{ font-size:{fs(13)}px; color:{text_mut}; font-style:italic; margin-top:{fs(3)}px; }}
.fc-hi   {{ font-size:{fs(17)}px; font-weight:800; color:{text_main}; }}
.fc-lo   {{ font-size:{fs(15)}px; color:{text_sub}; }}

/* ─── Uyarılar ─── */
.alert-row {{ background:linear-gradient(135deg,rgba(248,81,73,0.10),rgba(248,81,73,0.05));
              border-radius:10px; padding:{fs(10)}px {fs(14)}px;
              margin:{fs(3)}px {fs(12)}px; border:1px solid rgba(248,81,73,0.30);
              box-shadow:0 3px 8px rgba(248,81,73,0.12); }}
.alert-txt {{ font-size:{fs(14)}px; color:#ff7b72; font-weight:600; }}

/* ─── Güncelleme bildirimi ─── */
.update-row {{ background:linear-gradient(135deg,rgba(96,165,250,0.10),rgba(96,165,250,0.05));
               border-radius:10px; padding:{fs(10)}px {fs(14)}px;
               margin:{fs(3)}px {fs(12)}px; border:1px solid rgba(96,165,250,0.30); }}
.update-txt {{ font-size:{fs(14)}px; color:{text_accent}; font-weight:600; }}

/* ─── Finans bölümü ─── */
.fin-card {{ background:linear-gradient(145deg,{fin_bg},{entry_bg});
             border-radius:14px; padding:{fs(12)}px {fs(14)}px;
             margin:{fs(4)}px {fs(12)}px {fs(4)}px {fs(12)}px;
             border:1px solid {fin_border};
             box-shadow:0 4px 16px rgba(212,160,23,0.15),inset 0 1px 0 rgba(255,255,255,0.05); }}
.fin-title {{ font-size:{fs(13)}px; font-weight:800; color:{fin_title}; letter-spacing:1px; }}
.fin-row   {{ border-radius:8px; padding:{fs(6)}px {fs(8)}px; margin-top:{fs(3)}px; }}
.fin-name  {{ font-size:{fs(13)}px; color:{text_sub}; }}
.fin-price {{ font-size:{fs(15)}px; font-weight:700; color:{text_main}; }}
.fin-change-pos {{ font-size:{fs(12)}px; color:{fin_profit}; font-weight:700; }}
.fin-change-neg {{ font-size:{fs(12)}px; color:{fin_loss};   font-weight:700; }}
.fin-change-neu {{ font-size:{fs(12)}px; color:{text_mut};   font-weight:600; }}
.profit-lbl {{ font-size:{fs(15)}px; font-weight:800; color:{fin_profit}; }}
.loss-lbl   {{ font-size:{fs(15)}px; font-weight:800; color:{fin_loss};   }}

/* ─── Widget 3-saatlik ─── */
.w3-card  {{ background:linear-gradient(145deg,{w3_bg},{entry_bg});
             border-radius:12px; padding:{fs(8)}px {fs(12)}px; margin:4px;
             border:1px solid {border}; min-width:{fs(65)}px;
             box-shadow:0 4px 12px {pill_shadow}, inset 0 1px 0 rgba(255,255,255,0.05); }}
.w3-time  {{ font-size:{fs(13)}px; color:{text_sub}; font-weight:700; }}
.w3-emoji {{ font-size:{fs(24)}px; }}
.w3-temp  {{ font-size:{fs(16)}px; font-weight:700; color:{text_main}; }}
.w3-sep   {{ color:{text_mut}; font-size:{fs(20)}px; margin-top:{fs(8)}px; }}

/* ─── Widget finans ─── */
.wfin-box {{ background:linear-gradient(135deg,{fin_bg},{entry_bg});
             border-radius:10px; padding:{fs(6)}px {fs(10)}px; margin:{fs(3)}px;
             border:1px solid {fin_border};
             box-shadow:0 3px 8px rgba(212,160,23,0.12); }}
.wfin-item {{ font-size:{fs(12)}px; color:{text_sub}; }}
.wfin-val  {{ font-size:{fs(14)}px; font-weight:700; color:{fin_title}; }}

/* ─── Groq AI ─── */
.groq-panel {{ background:linear-gradient(145deg,{groq_bg},{entry_bg});
               border-radius:12px; padding:{fs(14)}px {fs(16)}px;
               margin:{fs(8)}px {fs(12)}px;
               border:1px solid {groq_border};
               box-shadow:0 4px 16px rgba(91,33,182,0.15); }}
.groq-title {{ font-size:{fs(14)}px; font-weight:800; color:{groq_text}; }}
.groq-text  {{ font-size:{fs(14)}px; color:{text_main}; }}

/* ─── Status / hata ─── */
.status-lbl {{ font-size:{fs(15)}px; color:{text_sub}; }}
.err-lbl    {{ font-size:{fs(15)}px; color:#f85149; font-weight: bold; }}
.ts-lbl     {{ font-size:{fs(13)}px; color:{text_mut}; font-style:italic; margin-top:{fs(6)}px; }}
.ai-lbl     {{ font-size:{fs(15)}px; color:{text_main}; font-weight: bold; }}
.ai-val     {{ font-size:{fs(14)}px; color:{text_main}; }}
separator   {{ background-color:{border}; margin:{fs(8)}px 0; }}
scrolledwindow {{ background-color:transparent; }}
viewport {{ background-color:transparent; }}
"""
