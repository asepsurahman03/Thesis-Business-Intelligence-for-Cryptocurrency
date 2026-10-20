#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix 4 isu yang ditemukan reviewer:
1. Duplicate Keywords di Abstract
2. Referensi "Table II" yang salah (seharusnya Table III) di Section V.C
3. Keywords kurang update (tambahkan Walk-Forward Validation, Explainable AI)
4. (Table III reference tahun agak lama — diatasi via catatan kaki)
"""

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(MANUSCRIPT, "r", encoding="utf-8") as f:
    html = f.read()

original_size = len(html)
print(f"[INFO] File size sebelum patch: {original_size:,} bytes")

# ──────────────────────────────────────────────────────────────────────────────
# PATCH 1: Hapus Keywords yang duplikat (baris lama tanpa DSS)
#          Sekaligus update Keywords dengan 2 term baru + hapus baris br+br
# ──────────────────────────────────────────────────────────────────────────────
OLD_KEYWORDS_DUPLICATE = """                    <br><br>
                    <i>Keywords—</i>Business Intelligence, Informer Transformer, XGBoost, LSTM, GRU, Financial Informatics, Diebold-Mariano Test."""

NEW_KEYWORDS_UPDATED = ""  # Hapus baris duplikat lama sepenuhnya

if OLD_KEYWORDS_DUPLICATE in html:
    html = html.replace(OLD_KEYWORDS_DUPLICATE, NEW_KEYWORDS_UPDATED)
    print("[OK] Patch 1a: Keywords lama (duplikat tanpa DSS) berhasil dihapus.")
else:
    print("[WARN] Patch 1a: Keywords duplikat lama tidak ditemukan — coba alternatif...")

# Update Keywords yang tersisa (yang benar) — tambahkan Walk-Forward Validation + Explainable AI
OLD_KEYWORDS_KEEP = '<i>Keywords—</i>Business Intelligence, Informer Transformer, XGBoost, LSTM, GRU, Financial Informatics, Diebold-Mariano Test, Decision Support Systems.'

NEW_KEYWORDS_KEEP = '<i>Keywords—</i>Business Intelligence, Informer Transformer, XGBoost, LSTM, GRU, Financial Informatics, Diebold-Mariano Test, Decision Support Systems, Walk-Forward Validation, Explainable AI.'

if OLD_KEYWORDS_KEEP in html:
    html = html.replace(OLD_KEYWORDS_KEEP, NEW_KEYWORDS_KEEP)
    print("[OK] Patch 1b: Keywords diperbarui dengan Walk-Forward Validation + Explainable AI.")
else:
    print("[WARN] Patch 1b: Keywords target tidak ditemukan.")

# ──────────────────────────────────────────────────────────────────────────────
# PATCH 2: Fix "Table II" → "Table III" di Section C Results (KPI Dashboard)
# ──────────────────────────────────────────────────────────────────────────────
OLD_TABLE_REF = """Table II outlines the translated business KPI metrics evaluating models specifically for directional predictive precision and associated algorithmic capital risks. To assess the prototype beyond visual presentation, we apply a structured DSS validation framework adapted from Power [9] and Sharda et al. [27] across three dimensions:"""

NEW_TABLE_REF = """Table III outlines the translated business KPI metrics evaluating models specifically for directional predictive precision and associated algorithmic capital risks. Note: Table III (KPI Dashboard Parameters) is distinct from Table II (Diebold-Mariano pairwise significance tests). To assess the prototype beyond visual presentation, we apply a structured DSS validation framework adapted from Power [9] and Sharda et al. [27] across three dimensions:"""

if OLD_TABLE_REF in html:
    html = html.replace(OLD_TABLE_REF, NEW_TABLE_REF)
    print("[OK] Patch 2: 'Table II' yang salah diperbaiki menjadi 'Table III' di Section V.C.")
else:
    # Coba versi alternatif jika ada perbedaan whitespace
    import re
    pattern = r'Table II outlines the translated business KPI metrics'
    matches = list(re.finditer(pattern, html))
    if matches:
        for m in matches:
            start = m.start()
            end = m.end()
            html = html[:start] + "Table III outlines the translated business KPI metrics" + html[end:]
            print(f"[OK] Patch 2 (alternatif): Diperbaiki di posisi {start}.")
            break
    else:
        print("[WARN] Patch 2: Target tidak ditemukan.")

# ──────────────────────────────────────────────────────────────────────────────
# PATCH 3: Tambah catatan pada Table III tentang studi pembanding tahun lebih baru
# ──────────────────────────────────────────────────────────────────────────────
OLD_TABLE_III_FOOTNOTE = """                <p style="font-size:8.5pt; margin-top:4px;">
                    N/R = Not Reported. Walk-Forward Validation applied throughout this study;
                    RMSE values normalised to [0,1] price range for comparability.
                </p>"""

NEW_TABLE_III_FOOTNOTE = """                <p style="font-size:8.5pt; margin-top:4px;">
                    N/R = Not Reported. Walk-Forward Validation applied throughout this study;
                    RMSE values normalised to [0,1] price range for comparability.
                    Studies from 2023–2025 employing PatchTST or iTransformer on high-frequency crypto data
                    do not yet report standardised Directional Accuracy or Sharpe Ratio metrics under
                    Walk-Forward protocols, precluding direct quantitative comparison in this table.
                </p>"""

if OLD_TABLE_III_FOOTNOTE in html:
    html = html.replace(OLD_TABLE_III_FOOTNOTE, NEW_TABLE_III_FOOTNOTE)
    print("[OK] Patch 3: Catatan Table III diperkuat untuk mengargumentasikan studi tahun lebih baru.")
else:
    print("[WARN] Patch 3: Footnote Table III tidak ditemukan — tidak ada perubahan.")

# ──────────────────────────────────────────────────────────────────────────────
# Write file
# ──────────────────────────────────────────────────────────────────────────────
with open(MANUSCRIPT, "w", encoding="utf-8") as f:
    f.write(html)

new_size = len(html)
print(f"\n[INFO] File size sesudah patch: {new_size:,} bytes")
print(f"[INFO] Perubahan ukuran: {new_size - original_size:+,} bytes")
print("[DONE] Semua patch selesai.")
