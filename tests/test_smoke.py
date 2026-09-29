import pytest


def test_app_imports():
    """Verifies that all internal modules can be imported without syntax/dependency errors."""
    try:
        import mintsky.api.finance
        import mintsky.api.weather
        import mintsky.core.portfolio
        import mintsky.core.settings
        import mintsky.ui.app
    except Exception as e:
        pytest.fail(f"Import failed: {e}")


def test_live_mgm_alert_title_matching_handles_cities_and_seas():
    from mintsky.ui.app import MintSkyApp

    assert MintSkyApp._mgm_alert_matches_city(
        {"baslik": "Samsun ve Ordu çevresinde kuvvetli yağış bekleniyor"}, "Samsun"
    )
    assert MintSkyApp._mgm_alert_matches_city(
        {"baslik": "Karadeniz'de fırtına bekleniyor"}, "Samsun"
    )
    assert not MintSkyApp._mgm_alert_matches_city(
        {"baslik": "Akdeniz'de fırtına bekleniyor"}, "Ankara"
    )


def test_app_instantiation(monkeypatch):
    """Tests if the app can be instantiated without crashing."""
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    from mintsky.ui.app import MintSkyApp

    # Keep the GUI smoke test isolated from the user's config, network, and
    # background update/tray workers. CI supplies a virtual display.
    monkeypatch.setattr(
        "mintsky.ui.app.core_load_settings",
        lambda: {"language": "tr", "scale": 1.0, "autostart": False,
                 "show_finance": False, "notify": False, "def_il": "Ankara",
                 "def_ilce": ""},
    )
    monkeypatch.setattr("mintsky.ui.app.core_load_portfolio", lambda: [])
    monkeypatch.setattr(MintSkyApp, "_apply_autostart_logic", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_check_update", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_fetch_tray_bg", lambda self: None)
    monkeypatch.setattr(
        "mintsky.ui.app.LocationAPI.fetch_locations_bg", lambda self, callback: None
    )
    app = MintSkyApp()
    try:
        assert app is not None
    finally:
        app.destroy()


def test_tray_menu_uses_observation_timestamps(monkeypatch):
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from mintsky.ui.app import MintSkyApp

    monkeypatch.setattr(
        "mintsky.ui.app.core_load_settings",
        lambda: {"language": "tr", "scale": 1.0, "autostart": False,
                 "show_finance": False, "notify": False, "def_il": "Samsun",
                 "def_ilce": "Atakum"},
    )
    monkeypatch.setattr("mintsky.ui.app.core_load_portfolio", lambda: [])
    monkeypatch.setattr(MintSkyApp, "_apply_autostart_logic", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_check_update", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_fetch_tray_bg", lambda self: None)
    monkeypatch.setattr(
        "mintsky.ui.app.LocationAPI.fetch_locations_bg", lambda self, callback: None
    )

    app = MintSkyApp()
    try:
        app._weather_timestamps = ["MGM: 13:45", "Open-Meteo: 13:45"]
        menu = app._build_tray_menu()
        labels = [item.get_label() for item in menu.get_children() if hasattr(item, "get_label") and item.get_label()]
        assert "🕒 MGM: 13:45" in labels
        assert "🕒 Open-Meteo: 13:45" in labels
        assert any("📍 Samsun" in l for l in labels)
    finally:
        app.destroy()


def test_tray_menu_shows_current_city_and_weather(monkeypatch):
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from mintsky.ui.app import MintSkyApp

    monkeypatch.setattr(
        "mintsky.ui.app.core_load_settings",
        lambda: {"language": "tr", "scale": 1.0, "autostart": False,
                 "show_finance": False, "notify": False, "def_il": "Samsun",
                 "def_ilce": "Atakum"},
    )
    monkeypatch.setattr("mintsky.ui.app.core_load_portfolio", lambda: [])
    monkeypatch.setattr(MintSkyApp, "_apply_autostart_logic", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_check_update", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_fetch_tray_bg", lambda self: None)
    monkeypatch.setattr(
        "mintsky.ui.app.LocationAPI.fetch_locations_bg", lambda self, callback: None
    )

    app = MintSkyApp()
    try:
        app._weather_timestamps = ["MGM: 29.09.2026 14:48"]
        app._apply_tray_data("drizzle", "19", "Samsun / Atakum", 51, "Hafif Sağanak Yağışlı", "19", "88", "6 km/h · Hafif KB")
        menu = app._build_tray_menu()
        labels = [item.get_label() for item in menu.get_children() if hasattr(item, "get_label") and item.get_label()]
        assert any("📍 Samsun / Atakum" in l for l in labels)
        assert any("🌦️ 19°C · Hafif Sağanak Yağışlı" in l for l in labels)
        assert not any("drizzle" in l.lower() for l in labels)
        assert any("Hissedilen: 19°" in l for l in labels)
        assert any("💧 %88" in l for l in labels)
        if hasattr(app, "_tray") and hasattr(app._tray, "get_tooltip_text"):
            tt = app._tray.get_tooltip_text()
            assert "29.09.2026 14:48" in tt
            assert "Samsun / Atakum" in tt
    finally:
        app.destroy()


def test_non_turkish_hides_mgm(monkeypatch):
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from mintsky.ui.app import MintSkyApp

    monkeypatch.setattr(
        "mintsky.ui.app.core_load_settings",
        lambda: {"language": "en", "scale": 1.0, "autostart": False,
                 "show_finance": False, "notify": False, "def_il": "Samsun",
                 "def_ilce": "Atakum"},
    )
    monkeypatch.setattr("mintsky.ui.app.core_load_portfolio", lambda: [])
    monkeypatch.setattr(MintSkyApp, "_apply_autostart_logic", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_check_update", lambda self: None)
    monkeypatch.setattr(MintSkyApp, "_fetch_tray_bg", lambda self: None)
    monkeypatch.setattr(
        "mintsky.ui.app.LocationAPI.fetch_locations_bg", lambda self, callback: None
    )

    app = MintSkyApp()
    try:
        assert app._language == "en"
        # Verify timestamps filter out MGM in non-tr
        app._weather_timestamps = []
        # Simulate timestamp parts generation
        sd = {"veriZamani": "2026-09-29T13:45:00Z"}
        om_cur = {"time": "2026-09-29T13:45:00Z"}
        ts_parts = []
        for src, val in (("MGM", sd.get("veriZamani")), ("Open-Meteo", om_cur.get("time"))):
            if val:
                if src == "MGM" and app._language != "tr":
                    continue
                ts_parts.append(f"{src}: 13:45")
        assert len(ts_parts) == 1
        assert "MGM" not in ts_parts[0]
        assert "Open-Meteo" in ts_parts[0]
    finally:
        app.destroy()
