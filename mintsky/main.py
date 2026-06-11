import os
import sys

# Bulunduğu dizinin bir üstünü module path'e ekle (mintsky klasöründen çıkış)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from mintsky.ui.app import MintSkyApp
from mintsky.i18n import load_language
from mintsky.utils import core_load_settings

def main():
    import fcntl
    import tempfile
    global _lock_file
    lock_path = os.path.join(tempfile.gettempdir(), 'mintsky_instance.lock')
    _lock_file = open(lock_path, 'w')
    try:
        fcntl.lockf(_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("MintSky zaten arka planda çalışıyor! (Sistem tepsisine veya görev çubuğuna bakın)")
        sys.exit(0)

    cfg = core_load_settings()
    load_language(cfg.get("language", "tr"))
    win = MintSkyApp()
    Gtk.main()

if __name__ == "__main__":
    main()
