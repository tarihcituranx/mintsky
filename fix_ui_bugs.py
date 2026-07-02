import os

app_file = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(app_file, "r") as f:
    code = f.read()

# Replace btn_ai with btn_ai_advisor
code = code.replace('_("btn_ai"), _("btn_ai_tt")', '_("btn_ai_advisor"), _("btn_ai_advisor_tt")')

# Replace github-symbolic with an emoji label
old_gh = 'gh_icon = Gtk.Image.new_from_icon_name("github-symbolic", Gtk.IconSize.MENU)'
new_gh = 'gh_icon = Gtk.Label(label="👨‍💻")'
code = code.replace(old_gh, new_gh)

with open(app_file, "w") as f:
    f.write(code)

print("Fixed UI bugs: btn_ai key and missing github icon.")
