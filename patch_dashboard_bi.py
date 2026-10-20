"""
Replace Fig. 4 image in manuscript with 'Dashboard BI.png'
"""
import base64, re, os

img_path  = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\Dashboard BI.png"
manuscript = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

# Load and encode image
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

data_uri = f"data:image/png;base64,{b64}"
print(f"[OK] Image loaded: {os.path.getsize(img_path)/1024:.1f} KB")

# Load manuscript
with open(manuscript, "r", encoding="utf-8") as f:
    html = f.read()

# Find the figure block containing "Fig. 4"
fig4_pattern = re.compile(
    r'(<div class="figure">[\s\S]*?)<img\s+src="([^"]*)"([^>]*)>([\s\S]*?Fig\. 4\.)',
    re.DOTALL
)

match = fig4_pattern.search(html)
if match:
    new_html = html[:match.start(2)] + data_uri + html[match.end(2):]
    with open(manuscript, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("[OK] Fig. 4 successfully replaced with 'Dashboard BI.png'")
else:
    # Fallback: search backward from "Fig. 4." text
    idx = html.find("Fig. 4.")
    if idx == -1:
        idx = html.find("Fig. 4 ")
    if idx != -1:
        img_start = html.rfind('<img ', 0, idx)
        src_start = html.find('src="', img_start) + 5
        src_end   = html.find('"', src_start)
        if src_start > 5 and src_end > src_start:
            new_html = html[:src_start] + data_uri + html[src_end:]
            with open(manuscript, "w", encoding="utf-8") as f:
                f.write(new_html)
            print("[OK] Fig. 4 replaced via fallback method.")
        else:
            print("[ERROR] Could not find img src for Fig. 4")
    else:
        print("[ERROR] Fig. 4 marker not found in manuscript")
