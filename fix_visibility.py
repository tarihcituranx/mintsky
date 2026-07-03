import os

file_path = "/home/turan/Belgeler/mintsky/mintsky/ui/app.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix toolbar button visibility
code = code.replace('btn.set_tooltip_text(tooltip)\n        btn.connect("clicked", cb)\n        return btn',
                    'btn.set_tooltip_text(tooltip)\n        btn.connect("clicked", cb)\n        btn.show_all()\n        return btn')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)
print("Toolbar buttons visibility patched.")
