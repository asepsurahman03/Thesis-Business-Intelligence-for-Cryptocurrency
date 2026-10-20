#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open(r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html", "r", encoding="utf-8") as f:
    html = f.read()

# Cari posisi Fig. 4 caption
idx = html.find("Fig. 4")
if idx == -1:
    print("TIDAK ADA caption Fig. 4")
else:
    # Ambil 200 karakter sebelum caption (untuk lihat tag img)
    region = html[max(0, idx-500):idx+80]
    # Hanya tampilkan apakah ada data:image/png;base64 di dekatnya
    start_b64 = region.find("data:image/png;base64,")
    if start_b64 != -1:
        snippet = region[start_b64:start_b64+60]
        print(f"[OK] Gambar Fig. 4 berhasil diganti. Preview src: {snippet}...")
    else:
        print("[WARN] Tidak ada data:image/png di sekitar Fig. 4")
    print(f"\nCaption ditemukan di posisi: {idx}")

print(f"\nTotal ukuran HTML: {len(html):,} byte")
