import sys
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
