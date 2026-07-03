import os
import re

svg_dir = "/home/turan/Belgeler/mintsky/mintsky/assets/pills"
colors = {
    "droplets.svg": "#4db8ff",
    "wind.svg": "#a5d8ff",
    "zap.svg": "#ffd43b",
    "gauge.svg": "#adb5bd",
    "eye.svg": "#ced4da",
    "cloud-rain.svg": "#74c0fc",
    "anchor.svg": "#339af0",
    "cloud.svg": "#e9ecef",
    "cloud-snow.svg": "#f8f9fa",
    "sun.svg": "#fcc419",
    "thermometer.svg": "#ff8787",
    "umbrella.svg": "#b197fc",
    "sunrise.svg": "#ffa94d",
    "sunset.svg": "#ff922b",
    "droplet.svg": "#4db8ff"
}

for filename in os.listdir(svg_dir):
    if not filename.endswith(".svg"): continue
    path = os.path.join(svg_dir, filename)
    with open(path, "r") as f:
        content = f.read()
    
    # Reset stroke width to 2.5 for better visibility
    content = re.sub(r'stroke-width="[\d\.]+"', 'stroke-width="2.5"', content)
    if 'stroke-width' not in content:
        content = content.replace('<svg', '<svg stroke-width="2.5"')
    
    # Apply color
    color = colors.get(filename, "#f8f9fa")
    content = re.sub(r'stroke="[^"]+"', f'stroke="{color}"', content)
    
    with open(path, "w") as f:
        f.write(content)
print("SVGs updated.")
