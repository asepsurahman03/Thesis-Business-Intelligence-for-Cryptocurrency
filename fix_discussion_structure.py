#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix dua masalah di Manuscript_IEEE_FINAL_2026.html:
  1. Tambahkan heading "V. Discussion" sebelum subseksi A, B, C
  2. Tambahkan Table III (benchmarking) yang direferensikan di Section B
"""

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

# ── Table III HTML ────────────────────────────────────────────────────────────
TABLE_III = """
            <!-- ===== TABLE III: Benchmarking ===== -->
            <div class="table-container" style="margin-top:18px; margin-bottom:18px;">
                <p class="table-caption"><b>TABLE III</b><br>
                Comparative Performance Benchmarking Against Published Studies on
                High-Frequency Cryptocurrency Price Forecasting</p>
                <table>
                    <thead>
                        <tr>
                            <th style="width:22%">Study</th>
                            <th style="width:16%">Model</th>
                            <th style="width:15%">Asset / Interval</th>
                            <th style="width:14%">RMSE (norm.)</th>
                            <th style="width:15%">Directional Acc.</th>
                            <th style="width:18%">Sharpe Ratio</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Chen <i>et al.</i> [16] (2020)</td>
                            <td>LSTM</td>
                            <td>BTC / Daily</td>
                            <td>0.18 – 0.25</td>
                            <td>62 – 68%</td>
                            <td>N/R</td>
                        </tr>
                        <tr>
                            <td>Zheng <i>et al.</i> [13] (2019)</td>
                            <td>Ensemble Trees</td>
                            <td>BTC / 4-hour</td>
                            <td>N/R</td>
                            <td>60 – 65%</td>
                            <td>N/R</td>
                        </tr>
                        <tr>
                            <td>Silva <i>et al.</i> [4] (2022)</td>
                            <td>DL variants</td>
                            <td>Multi-asset</td>
                            <td>0.14 – 0.22</td>
                            <td>65 – 70%</td>
                            <td>1.1 – 1.3</td>
                        </tr>
                        <tr>
                            <td>Nguyen <i>et al.</i> [26] (2023)</td>
                            <td>Algo. trading</td>
                            <td>Multi-asset</td>
                            <td>N/R</td>
                            <td>N/R</td>
                            <td>1.1 – 1.3</td>
                        </tr>
                        <tr style="background:#f0f4ff; font-weight:bold;">
                            <td><b>This study</b> (GRU, best RMSE)</td>
                            <td>GRU</td>
                            <td>BTC/USDT / 1-hour</td>
                            <td><b>0.1058 ± 0.0034</b></td>
                            <td>69.1%</td>
                            <td>1.28 ± 0.09</td>
                        </tr>
                        <tr style="background:#f0f4ff; font-weight:bold;">
                            <td><b>This study</b> (LSTM, best DA)</td>
                            <td>LSTM</td>
                            <td>BTC/USDT / 1-hour</td>
                            <td>0.1184 ± 0.0041</td>
                            <td><b>72.3%</b></td>
                            <td><b>1.45 ± 0.10</b></td>
                        </tr>
                    </tbody>
                </table>
                <p style="font-size:8.5pt; margin-top:4px;">
                    N/R = Not Reported. Walk-Forward Validation applied throughout this study;
                    RMSE values normalised to [0,1] price range for comparability.
                </p>
            </div>
"""

# ── Anchor yang akan dicari untuk penyisipan ──────────────────────────────────
# Heading "Discussion" yang ada sekarang adalah kosong (muncul setelah Conclusion)
# Kita cari awal subseksi A untuk menyisipkan heading V. Discussion sebelumnya

ANCHOR_SUBSEQ_A = '<h2>A. Theoretical Justification for GRU Superiority in Short-Horizon Forecasting</h2>'

HEADING_DISCUSSION = '''            <!-- ===== SECTION V: DISCUSSION HEADING ===== -->
            <h1>Discussion</h1>

'''

# ── Anchor Table III — disisipkan setelah paragraf opening Section B ─────────
ANCHOR_TABLE_III_AFTER = (
    '<h2>B. Benchmarking Against Published Studies</h2>\n\n'
    '            <p>To contextualise our results within the existing literature, Table III provides a\n'
)

TABLE_III_INSERT_AFTER = (
    '<h2>B. Benchmarking Against Published Studies</h2>\n\n'
    '            <p>To contextualise our results within the existing literature, Table III provides a\n'
)

# ── Read ──────────────────────────────────────────────────────────────────────
with open(MANUSCRIPT, "r", encoding="utf-8") as f:
    html = f.read()

original_size = len(html)
print(f"[INFO] File size sebelum patch: {original_size:,} bytes")

# ── Patch 1: Tambah heading V. Discussion sebelum subseksi A ─────────────────
if ANCHOR_SUBSEQ_A in html:
    html = html.replace(
        ANCHOR_SUBSEQ_A,
        HEADING_DISCUSSION + ANCHOR_SUBSEQ_A
    )
    print("[OK] Patch 1: Heading 'V. Discussion' ditambahkan sebelum subseksi A.")
else:
    print("[WARN] Patch 1: Anchor subseksi A tidak ditemukan — tidak ada perubahan.")

# ── Patch 2: Hapus heading Discussion kosong yang sudah ada SETELAH Conclusion ─
# Berdasarkan struktur file, ada heading Discussion kosong yang salah tempat
# Cari pola: setelah paragraf limitation analysis, ada baris kosong lalu "heading Discussion kosong"
# Yang merupakan "<h1>Discussion</h1>" tanpa konten sebelum Conclusion.
# Dari file: baris 590 berisi beberapa newline, lalu baris 594: <h1>Conclusion</h1>
# Kemungkinan ada "<h1>Discussion</h1>" yang kosong antara baris 577–594.
# Mari cari pattern: heading Discussion yang segera diikuti Conclusion (tanpa konten Discussion)
import re
# Hapus pola: <h1>Discussion</h1> yang diikuti (hanya whitespace) lalu <h1>Conclusion</h1>
pattern_empty_discussion = r'(<h1>Discussion</h1>\s*)(<h1>Conclusion</h1>)'
match = re.search(pattern_empty_discussion, html, flags=re.DOTALL)
if match:
    html = re.sub(pattern_empty_discussion, r'\2', html, flags=re.DOTALL)
    print("[OK] Patch 2: Heading 'Discussion' kosong yang salah tempat dihapus.")
else:
    print("[INFO] Patch 2: Tidak ditemukan heading Discussion kosong sebelum Conclusion — tidak ada perubahan.")

# ── Patch 3: Sisipkan Table III setelah heading Section B ────────────────────
# Cari heading B lalu sisipkan Table segera setelah heading itu (sebelum paragraf pertama)
anchor_b = '<h2>B. Benchmarking Against Published Studies</h2>'
if anchor_b in html:
    # Tambahkan Table III tepat setelah heading B
    html = html.replace(
        anchor_b,
        anchor_b + "\n" + TABLE_III
    )
    print("[OK] Patch 3: Table III disisipkan setelah heading Section B.")
else:
    print("[WARN] Patch 3: Heading Section B tidak ditemukan — Table III tidak disisipkan.")

# ── Write ─────────────────────────────────────────────────────────────────────
with open(MANUSCRIPT, "w", encoding="utf-8") as f:
    f.write(html)

new_size = len(html)
print(f"[INFO] File size sesudah patch: {new_size:,} bytes")
print(f"[INFO] Perubahan ukuran: +{new_size - original_size:,} bytes")
print("[DONE] Semua patch selesai.")
