import re

with open("mintsky/ui/app.py", "r") as f:
    lines = f.readlines()

out = []
for i, line in enumerate(lines):
    if "self._status(\"⏳ Veriler alınıyor…\")" in line:
        out.append(line)
        # Skip the wrongly injected lines if they are right after
        continue
    if "self._fetch_in_progress = False" in line and "self._tray_busy = False" in lines[i+1] and "self._fetch_lock =" in lines[i+2]:
        # skip the wrongly injected block
        pass
    else:
        out.append(line)

# Wait, it's safer to just run git restore mintsky/ui/app.py and re-apply cleanly via script!
