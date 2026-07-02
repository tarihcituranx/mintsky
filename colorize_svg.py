import os
import glob

svg_dir = "/home/turan/Belgeler/mintsky/mintsky/assets/weather"
svg_files = glob.glob(os.path.join(svg_dir, "*.svg"))

for file_path in svg_files:
    with open(file_path, "r") as f:
        content = f.read()
    
    # Remove existing fill attributes if any
    import re
    content = re.sub(r'\sfill="[^"]*"', '', content)
    
    # Add fill="#ffffff" to <path> and <polygon> and <circle>
    content = content.replace('<path ', '<path fill="#ffffff" ')
    content = content.replace('<circle ', '<circle fill="#ffffff" ')
    content = content.replace('<polygon ', '<polygon fill="#ffffff" ')
    content = content.replace('<rect ', '<rect fill="#ffffff" ')
    
    with open(file_path, "w") as f:
        f.write(content)

print(f"Updated {len(svg_files)} SVG files to be white for dark theme!")
