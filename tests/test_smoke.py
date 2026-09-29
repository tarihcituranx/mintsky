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
