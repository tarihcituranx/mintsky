import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from mintsky.ui.app import MintSkyApp

def main():
    win = MintSkyApp()
    Gtk.main()

if __name__ == "__main__":
    main()
