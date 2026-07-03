import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mintsky.utils import hadise_mgm, get_svg_image
from mintsky.i18n import load_language

def test_lang(lang):
    load_language(lang)
    em, ks, uz = hadise_mgm("A", False)
    print(f"[{lang}] hadise_mgm('A') -> em='{em}', ks='{ks}', uz='{uz}'")
    icon = get_svg_image(em, size=32)
    print(f"[{lang}] get_svg_image returns: {type(icon)}")

test_lang("tr")
test_lang("en")
