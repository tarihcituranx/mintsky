import os
import sys

# Bulunduğu dizinin bir üstünü module path'e ekle (mintsky klasöründen çıkış)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from mintsky.ui.app import MintSkyApp
from mintsky.i18n import load_language

def main():
    load_language("tr")
    win = MintSkyApp()
    Gtk.main()

if __name__ == "__main__":
    main()
