#!/usr/bin/env python3
import base64, re

IMG  = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\Dashboard BI.png"
HTML = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(IMG, "rb") as f:
    ref = base64.b64encode(f.read()).decode("ascii")

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

idx    = html.find("Fig. 4")
region = html[idx : idx + 5000]
m = re.search(r'src="data:image/png;base64,([A-Za-z0-9+/=]+)"', region)
if m:
    found = m.group(1)
    print("Match :", found == ref)
    print("Len ref:", len(ref), "| Len found:", len(found))
else:
    print("Image not found near Fig. 4")
