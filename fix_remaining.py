import re
import os

# --- app.py ---
with open("mintsky/ui/app.py", "r") as f:
    app = f.read()

# M5: finance_api._data read without lock
app = app.replace(
    'if self._show_finance and not self.finance_api._data:',
    'with self.finance_api._lock:\n            has_fin = bool(self.finance_api._data)\n        if self._show_finance and not has_fin:'
)

# M8: Wildcard imports in app.py
app = app.replace(
    "from mintsky.constants import *\nfrom mintsky.utils import *",
    "from mintsky.constants import VERSIYON, BASE_MGM, GITHUB_REPO, GITHUB_API, ICONS, \\\n"
    "    MGM_SIMGELER, UYGULAMA_ADI, ALTIN_KODLAR, DOVIZ_KODLAR, KRIPTO_KODLAR, TRAY_ICONS, \\\n"
    "    HADISE, WMO_HADISE, YONLER, NOM_HEADERS, TIMEOUT, WEATHER_CACHE_TTL, FINANCE_CACHE_TTL, TRAY_FETCH_TTL\n"
    "from mintsky.utils import yon, fmt_date, fmt_time, fmt_dt, val, fmt_try, fmt_pct, hadise_mgm, hadise_wmo, css_str"
)

# M10: Finance refresh button timing
# Replace `self.finance_api.fetch_bg(force=True)` and immediate re-enable
# We just change `_on_fin_refresh` to use `self._force_finance_refresh` or similar
# Wait, let's look at `_on_fin_refresh`
app = app.replace(
    """        def _on_fin_refresh(_):
            btn_fin_refresh.set_sensitive(False)
            btn_fin_refresh.set_label("🔄")
            self.finance_api.fetch_bg(force=True)
            GLib.idle_add(btn_fin_refresh.set_sensitive, True)
            GLib.idle_add(btn_fin_refresh.set_label, "🔄 Yenile")""",
    """        def _on_fin_refresh(_):
            btn_fin_refresh.set_sensitive(False)
            btn_fin_refresh.set_label("🔄")
            def _fin_cb(s, e):
                GLib.idle_add(btn_fin_refresh.set_sensitive, True)
                GLib.idle_add(btn_fin_refresh.set_label, "🔄 Yenile")
            self.finance_api.fetch_bg(force=True, callback=_fin_cb)"""
)

# L3: _move_to_corner monitor index
app = app.replace(
    """        screen = self.get_screen()
        monitor = screen.get_monitor_at_window(self.get_window())
        if monitor:
            geom = monitor.get_geometry()""",
    """        screen = self.get_screen()
        monitor = screen.get_monitor_at_window(self.get_window())
        if monitor is not None:
            geom = screen.get_monitor_geometry(monitor)"""
)

# L4: os._exit(0) -> sys.exit(0)  Wait, Gtk.main_quit() is better.
# Actually for restart, os.execv is fine but let's do sys.exit instead of os._exit
app = app.replace("os._exit(0)", "sys.exit(0)")

# L5: os.system("gtk-update-icon-cache ... &")
app = app.replace(
    'os.system("gtk-update-icon-cache -f ~/.local/share/icons/hicolor/ 2>/dev/null &")',
    'subprocess.Popen(["gtk-update-icon-cache", "-f", os.path.expanduser("~/.local/share/icons/hicolor/")], stderr=subprocess.DEVNULL)'
)

with open("mintsky/ui/app.py", "w") as f:
    f.write(app)


# --- CI Workflows ---

# C6: mintsky-audit.yaml duplicate env
with open(".github/workflows/mintsky-audit.yaml", "r") as f:
    audit = f.read()
# The bug report says duplicate env at lines 3-4.
# We'll just remove the first one using regex.
audit = re.sub(r'^env:\n\s*FORCE_JAVASCRIPT_ACTIONS_TO_NODE24:\s*true\n', '', audit, count=1, flags=re.MULTILINE)

# M16: actionlint curl|bash
audit = audit.replace(
    "bash <(curl -s https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)",
    "bash <(curl -sfL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash) 1.6.27"
)
with open(".github/workflows/mintsky-audit.yaml", "w") as f:
    f.write(audit)


def fix_ci_file(path):
    if not os.path.exists(path): return
    with open(path, "r") as f:
        content = f.read()
    
    # C9: Add env
    if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" not in content:
        content = content.replace("jobs:\n", "env:\n  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true\n\njobs:\n")
    
    # C7: API Key leak
    content = content.replace('"?key=$GEMINI_API_KEY"', '" -H "x-goog-api-key: $GEMINI_API_KEY"')
    content = content.replace("'?key=$GEMINI_API_KEY'", "' -H \"x-goog-api-key: $GEMINI_API_KEY\"")
    
    # C8: skill-update empty brain.md
    if "skill-update" in path:
        content = content.replace(
            "jq -r '.candidates[0].content.parts[0].text // empty' response.json > brain.md",
            'OUTPUT=$(jq -r \'.candidates[0].content.parts[0].text // empty\' response.json)\n          if [ -z "$OUTPUT" ]; then\n            echo "API returned empty or error. Keeping old brain.md."\n          else\n            echo "$OUTPUT" > brain.md\n          fi'
        )
    
    with open(path, "w") as f:
        f.write(content)

fix_ci_file(".github/workflows/mintsky-docs-update.yaml.disabled")
fix_ci_file(".github/workflows/mintsky-skill-update.yaml.disabled")

# DOĞRU-TEST-DOSYASI rename
if os.path.exists(".github/workflows/DOĞRU-TEST-DOSYASI.yaml"):
    fix_ci_file(".github/workflows/DOĞRU-TEST-DOSYASI.yaml")
    os.rename(".github/workflows/DOĞRU-TEST-DOSYASI.yaml", ".github/workflows/mintsky-test.yaml")

print("done remaining")
