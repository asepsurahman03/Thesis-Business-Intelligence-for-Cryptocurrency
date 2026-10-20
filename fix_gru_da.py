#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seragamkan angka GRU Directional Accuracy dari 69.1% → 69.8%
sesuai data tabel Table II KPI di manuscript.
"""

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(MANUSCRIPT, "r", encoding="utf-8") as f:
    html = f.read()

# Ganti 69.1% yang ada di Table III dengan 69.8%
old = "<td>69.1%</td>"
new = "<td>69.8%</td>"

count = html.count(old)
print(f"Ditemukan '{old}' sebanyak {count} kali")

html = html.replace(old, new)

with open(MANUSCRIPT, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Angka 69.1% → 69.8% berhasil diseragamkan di Table III.")
