import os
import sys

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


def test_app_instantiation():
    """Tests if the app can be instantiated without crashing."""
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    from mintsky.ui.app import MintSkyApp

    try:
        app = MintSkyApp()
        assert app is not None
        app.destroy()
    except Exception as e:
        pytest.fail(f"App instantiation failed: {e}")
