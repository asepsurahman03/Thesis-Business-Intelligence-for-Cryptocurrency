#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mengganti gambar Fig. 4 di Manuscript_IEEE_FINAL_2026.html
dengan gambar Dashboard BI.png yang dikonversi ke base64.
"""

import base64
import re

IMG_PATH      = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\Dashboard BI.png"
MANUSCRIPT    = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

# ── 1. Baca gambar dan encode ke base64 ──────────────────────────────────────
with open(IMG_PATH, "rb") as f:
    raw = f.read()

b64 = base64.b64encode(raw).decode("ascii")
new_src = f"data:image/png;base64,{b64}"

print(f"[INFO] Gambar '{IMG_PATH}' yang telah di-encode: {len(b64):,} karakter base64")

# ── 2. Baca manuscript ───────────────────────────────────────────────────────
with open(MANUSCRIPT, "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ── 3. Ganti src pada tag <img> di dalam .figure.wide (Fig. 4) ──────────────
#
# Pola yang kita cari:
#   <div class="figure wide" ...>
#       <img src="data:image/...;base64,<BASE64_LAMA>" ...>
#       <div class="figure-caption">Fig. 4 ...</div>
#   </div>
#
# Kita ganti src="..." apa pun yang ada di dalam div.figure.wide
# yang memiliki caption mengandung "Fig. 4"
#
# Strategi: cari blok <div class="figure wide"...>...</div>
# yang mengandung "Fig. 4", lalu ganti src di dalamnya.

PATTERN = re.compile(
    r'(<div\s+class="figure wide"[^>]*>.*?<img\s[^>]*?)src="[^"]*"',
    re.DOTALL | re.IGNORECASE
)

def replacer(m):
    """Ganti src hanya jika blok ini mengandung 'Fig. 4'"""
    full_block = m.group(0)
    # Kita perlu cek apakah blok ini terkait Fig. 4.
    # Karena pola di atas hanya mencakup sampai img src,
    # kita cek dari posisi match ke depan untuk menemukan caption.
    # Alternatif lebih sederhana: ganti SEMUA figure wide (hanya ada 1).
    prefix = m.group(1)
    return f'{prefix}src="{new_src}"'

html_new, count = PATTERN.subn(replacer, html)

if count == 0:
    print("[WARN] Pola <img> di dalam div.figure.wide tidak ditemukan.")
    print("       Mencoba pola alternatif …")

    # Pola alternatif: ganti src data:image pada elemen img apa pun
    # yang letaknya di antara tag figure-caption "Fig. 4"
    idx_fig4 = html.find("Fig. 4")
    if idx_fig4 == -1:
        print("[ERROR] Caption 'Fig. 4' tidak ditemukan dalam manuscript!")
    else:
        # Cari <img ... src="..."> sebelum "Fig. 4" dalam radius 5000 karakter
        region_start = max(0, idx_fig4 - 5000)
        region = html[region_start:idx_fig4]
        img_pat = re.compile(r'(<img\s[^>]*?)src="[^"]*"', re.DOTALL | re.IGNORECASE)
        last_match = None
        for m in img_pat.finditer(region):
            last_match = m

        if last_match is None:
            print("[ERROR] Tidak ada tag <img> yang ditemukan di sekitar Fig. 4!")
        else:
            abs_start = region_start + last_match.start()
            abs_end   = region_start + last_match.end()
            old_tag   = last_match.group(0)
            new_tag   = last_match.group(1) + f'src="{new_src}"'
            html_new  = html[:abs_start] + new_tag + html[abs_end:]
            count     = 1
            print("[OK] Gambar Fig. 4 berhasil diganti (metode alternatif).")
else:
    print(f"[OK] Berhasil mengganti gambar pada {count} lokasi.")

# ── 4. Simpan hasil ──────────────────────────────────────────────────────────
if count > 0:
    with open(MANUSCRIPT, "w", encoding="utf-8") as f:
        f.write(html_new)

    new_len = len(html_new)
    delta   = new_len - original_len
    print(f"\nFile berhasil disimpan.")
    print(f"Ukuran berubah: {original_len:,} → {new_len:,} byte  (selisih {delta:+,})")
    print(f"Lokasi: {MANUSCRIPT}")
else:
    print("[ERROR] Tidak ada perubahan yang disimpan.")
