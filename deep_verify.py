#!/usr/bin/env python3
import base64, re

IMG  = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\Dashboard BI.png"
HTML = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(IMG, "rb") as f:
    raw = f.read()
ref = base64.b64encode(raw).decode("ascii")

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

idx     = html.find("Fig. 4")
print(f"Fig. 4 posisi: {idx}")
print(f"Panjang ref base64: {len(ref):,}")

# Cari `src="data:image/png;base64,` setelah Fig. 4
src_idx = html.find('src="data:image/png;base64,', idx)
print(f"Posisi src= setelah Fig.4: {src_idx}")

if src_idx != -1:
    # Ambil 100 karakter dari awal base64
    b64_start = src_idx + len('src="data:image/png;base64,')
    snippet   = html[b64_start : b64_start + 100]
    ref_snippet = ref[:100]
    print(f"\nSnippet dari manuscript: {snippet}")
    print(f"Snippet dari ref       : {ref_snippet}")
    print(f"\nCocok: {snippet == ref_snippet}")
