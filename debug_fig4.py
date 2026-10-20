#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open(r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("Fig. 4")
print(f"Posisi Fig. 4: {idx}")
# Tampilkan 1500 karakter sebelum caption
region = html[max(0, idx-1500):idx+200]
print("--- REGION SEBELUM DAN SESUDAH Fig. 4 ---")
print(repr(region[:300]))
print("...")
print(repr(region[-200:]))
print("\n--- Cari semua src=data: di HTML ---")
import re
matches = list(re.finditer(r'src="data:image', html))
print(f"Jumlah tag img dengan data:image base64: {len(matches)}")
for m in matches:
    print(f"  Posisi: {m.start()}, … src=\"data:image/png;base64,{html[m.start()+len('src=\"data:image/png;base64,'):m.start()+len('src=\"data:image/png;base64,')+30]}...\"")
