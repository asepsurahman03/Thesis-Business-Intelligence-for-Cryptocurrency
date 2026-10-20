#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Identifikasi gambar pada Fig. 4 dengan membandingkan header base64
antara file saat ini vs Dashboard BI.png asli.
"""
import base64

IMG_PATH = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\Dashboard BI.png"
MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

# Ambil 60 karakter pertama base64 dari Dashboard BI.png
with open(IMG_PATH, "rb") as f:
    reference_b64 = base64.b64encode(f.read()).decode("ascii")[:60]

print(f"Header base64 Dashboard BI.png : {reference_b64}")

# Cari di manuscript
with open(MANUSCRIPT, "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("Fig. 4")
region_start = max(0, idx - 5000)
region_after  = html[idx:idx + 5000]

# Cari src="data:image dalam region setelah Fig. 4
import re
m = re.search(r'src="data:image/png;base64,([^"]{1,80})', region_after)
if m:
    found_b64 = m.group(1)[:60]
    print(f"Header base64 di manuscript    : {found_b64}")
    if found_b64 == reference_b64:
        print("\n✅ COCOK! Gambar di manuscript ADALAH Dashboard BI.png!")
    else:
        print("\n❌ TIDAK COCOK. Gambar di manuscript bukan Dashboard BI.png.")
else:
    print("Tidak ditemukan src=data:image/png di dekat Fig. 4")
