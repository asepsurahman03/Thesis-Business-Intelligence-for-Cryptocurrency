"""
apply_revisi19_fixes.py
========================
Memperbaiki 5 isu kritis Revisi_18:

1. Hapus Fig. 3 beserta 3 rujukan + kalimat "No specific macro-shock"
2. Persistence DA: ganti 50% by convention → dijelaskan secara benar bahwa
   persistence flat juga menghasilkan sinyal non-trivial; DA persistence dihitung
   ulang dari data (atau dilaporkan sebagai "not reported separately" dengan penjelasan)
3. Terminologi "stale-forecast signal" mengganti "weekly trend signal"
4. Hapus kalimat Fold 6 Terra-Luna dan Fold 10 FTX dari paragraf fold
5. Operational Boundaries: "hourly sign rule can reverse position" → clarify
   bahwa sinyal dibuat dari lintasan prakiraan awal minggu (stale)
"""

import shutil, os, copy
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

SRC = r"c:\Nusa Putra University\S2 Magister\Thesis\Revisi_18_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx"
DST = r"c:\Nusa Putra University\S2 Magister\Thesis\Revisi_19_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx"
BAK = SRC + ".bak_r19"

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print(f"[backup] {BAK}")

doc = Document(SRC)

def para_text(p):
    return "".join(r.text for r in p.runs)

def replace_in_para(p, old, new):
    full = para_text(p)
    if old not in full:
        return False
    updated = full.replace(old, new)
    for i, r in enumerate(p.runs):
        r.text = updated if i == 0 else ""
    return True

def replace_in_doc(doc, old, new):
    hits = 0
    for p in doc.paragraphs:
        if replace_in_para(p, old, new):
            hits += 1
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if replace_in_para(p, old, new):
                        hits += 1
    return hits

def contains_text(doc, text):
    for p in doc.paragraphs:
        if text in para_text(p):
            return True
    return False

log = []

# ==============================================================
# FIX 1: Hapus Fig. 3 beserta rujukan dan kalimat "No specific macro-shock"
# ==============================================================
print("[1] Menghapus Fig. 3 dan semua rujukannya...")

# 1a. Hapus section "Error Distributions and Macro-Regime Anomalies"
# termasuk heading, teks P72, dan caption P74

OLD_ERRORDIST_HEADING = "Error Distributions and Macro-Regime Anomalies"
NEW_ERRORDIST_HEADING = ""

OLD_ERRORDIST_TEXT = (
    "All four architectures exhibit non-Gaussian residual distributions. "
    "The GRU residual distribution (Fig. 3) computed across all 24 × 168 = 4,032 "
    "out-of-sample predictions is right-skewed (skewness ≈ +1.4), with heavier-than-normal "
    "tails; the LSTM (not shown) shows skewness ≈ +1.7, consistent with its larger RMSE. "
    "This right-skew indicates a systematic tendency to underestimate large positive price moves. "
    "Price-derived technical features are by construction lagging indicators and cannot "
    "capture abrupt regime changes driven by external macro events; "
    "this is a known structural limitation of the feature set [48]. "
    "No specific macro-shock event is identified in the residuals because "
    "no single fold precisely covers the most extreme historical events "
    "in the five-year sample."
)

NEW_ERRORDIST_TEXT = ""  # Dihapus seluruhnya

OLD_FIG3_CAPTION = (
    "GRU residual error distribution across all 24 Walk-Forward folds "
    "(4,032 hourly residuals combined): histogram with kernel density estimate (left) "
    "and Q-Q plot vs. standard normal (right). The distribution is right-skewed "
    "(skewness ≈ +1.4) with heavier-than-normal tails, indicating systematic "
    "underestimation of large positive price moves. "
    "Note: no specific macro-shock event (e.g., Terra-Luna, FTX) is identified "
    "in the residuals, as no single fold precisely covers those dates."
)

NEW_FIG3_CAPTION = ""  # Dihapus

h1 = replace_in_doc(doc, OLD_ERRORDIST_HEADING, NEW_ERRORDIST_HEADING)
h2 = replace_in_doc(doc, OLD_ERRORDIST_TEXT, NEW_ERRORDIST_TEXT)
h3 = replace_in_doc(doc, OLD_FIG3_CAPTION, NEW_FIG3_CAPTION)
log.append(f"  Error dist heading: {h1}, text: {h2}, caption: {h3}")

# 1b. Hapus semua rujukan "(Fig. 3)" di teks lain
h = replace_in_doc(doc, "(Fig. 3)", "")
h += replace_in_doc(doc, "Fig. 3", "")
h += replace_in_doc(doc, " observed in Fig. 3", "")
log.append(f"  Fig.3 references removed: {h}")

# 1c. Hapus rujukan [48] yang hanya muncul di konteks Error Distributions
# (jika masih ada, biarkan — jangan hapus referensi yang dipakai di bagian lain)

# 1d. Hapus kalimat "The residual right-skew observed in... is consistent"
h = replace_in_doc(doc,
    "The residual right-skew observed in Fig. 3 is consistent with this limitation. ",
    "This is a structural limitation of the current feature set. "
)
h += replace_in_doc(doc,
    "The residual right-skew observed in  is consistent with this limitation. ",
    "This is a structural limitation of the current feature set. "
)
log.append(f"  Residual right-skew ref removed: {h}")

# ==============================================================
# FIX 2: Persistence DA — ganti 50% by convention dengan penjelasan benar
# ==============================================================
print("[2] Memperbaiki persistence DA (bukan 50% by convention)...")

OLD_PERSIST = (
    "(a) Persistence (Naïve Flat): for each 168-hour test window, the persistence "
    "baseline sets ŷ_{t+h} = y_{T_train} for all h = 1,...,168 (i.e., the last "
    "observed normalized close price is repeated flat for the entire test window). "
    "This is the appropriate naïve benchmark when RMSE is evaluated across all 168 "
    "forecast steps together. It achieved normalized RMSE = 0.2341 and "
    "Directional Accuracy = 50.0% by convention (a flat forecast has no directional signal). "
    "All four ML models produce lower RMSE than this flat baseline."
)

NEW_PERSIST = (
    "(a) Persistence (Naïve Flat): for each 168-hour test window, the persistence "
    "baseline sets ŷ_{t+h} = y_{T_train} for all h = 1,...,168 (i.e., the last "
    "observed normalized close price is repeated flat for the entire test window). "
    "This is the appropriate naïve benchmark when RMSE is evaluated across all 168 "
    "forecast steps together. It achieved normalized RMSE = 0.2341. "
    "Important note on persistence DA: applying the same signal rule "
    "s_t = sign(ŷ_t − y_{t−1}) to the flat persistence forecast yields "
    "s_t = sign(y_{T_train} − y_{t−1}), which is a non-trivial signal that bets the price "
    "will revert to y_{T_train} at every hour. This signal is data-dependent — "
    "its DA depends on whether BTC prices mean-revert or trend during each 168-hour window. "
    "The persistence DA is therefore not reported as a fixed number; "
    "readers should compare model DAs against the ARIMA and buy-and-hold baselines "
    "in Table II, which are computed under the same signal rule. "
    "All four ML models produce lower RMSE than the flat persistence baseline."
)

h = replace_in_doc(doc, OLD_PERSIST, NEW_PERSIST)
log.append(f"  Persistence DA explanation: {h}")

# Juga perbaiki caption Fig. 4 yang masih menyebut "DA = 50.0%"
h = replace_in_doc(doc,
    "persistence (random-walk) baseline, DA = 50.0%;",
    "ARIMA baseline (DA = 51.8%, SR = 0.41);"
)
log.append(f"  Fig4 caption persistence DA: {h}")

# Juga perbaiki di teks lain jika ada
h = replace_in_doc(doc,
    "persistence (random-walk) baseline, DA = 50.0%",
    "ARIMA baseline (DA = 51.8%, SR = 0.41)"
)
log.append(f"  Other persistence DA ref: {h}")

# ==============================================================
# FIX 3: Terminologi "stale-forecast signal" — ganti "weekly trend signal"
# ==============================================================
print("[3] Mengganti terminologi ke 'stale-forecast signal'...")

# Ganti di Layer 4 paragraph
OLD_LAYER4_WEEKLY = (
    "Layer 4 translates predictions ŷt into weekly trend signals for the 168-hour "
    "test window: st = sign(ŷt − yt−1) ∈ {+1, −1}, where +1 denotes a long "
    "position and −1 a protective/short allocation. "
    "The hourly strategy return is Rtstrategy = st · rt, where rt = ln(Pt / Pt−1) "
    "is the realized logarithmic return of BTC/USDT. "
    "Important caveat: because predictions ŷt are generated by recursive "
    "(autoregressive) unrolling from the start of each 168-hour test window, "
    "ŷt at step h carries cumulative propagation error from steps 1,...,h−1. "
    "The signal st = sign(ŷt − yt−1) therefore reflects the model's weekly "
    "directional view rather than a true one-step-ahead prediction using "
    "the actual yt−1. Consequently, the Directional Accuracy, Sharpe Ratio, "
    "and VaR reported here measure the gross utility of the model's weekly "
    "trend signal — not the performance of an hour-by-hour executable strategy. "
    "A genuine per-hour signal would require rolling one-step-ahead inference "
    "using actual observed prices at each step; this is planned as a future extension."
)

NEW_LAYER4_STALE = (
    "Layer 4 computes a stale-forecast signal for each of the 168 hours in the "
    "test window: st = sign(ŷt − yt−1) ∈ {+1, −1}, where +1 denotes a long "
    "position and −1 a protective/short allocation, and ŷt is the recursive "
    "prediction generated from the fixed forecast trajectory computed at the "
    "start of the 168-hour window. "
    "The term 'stale' reflects that ŷt at horizon h was produced using "
    "predicted (not actual) values at steps 1,...,h−1; it is not updated "
    "as actual prices arrive. "
    "The per-hour strategy return is Rtstrategy = st · rt, where "
    "rt = ln(Pt / Pt−1) is the realized log-return of BTC/USDT. "
    "Because the signal trajectory is fixed at the start of each test window, "
    "this is equivalent to a 168-step directional commitment based on the "
    "model's initial forecast path. Directional Accuracy, Sharpe Ratio, "
    "and VaR are computed from these stale-forecast signals and measure "
    "the gross utility of the model's weekly directional view "
    "— not the performance of a true hour-by-hour executable strategy. "
    "A genuine per-hour signal would require rolling one-step-ahead inference "
    "using actual observed prices; this is planned as a future extension."
)

h = replace_in_doc(doc, OLD_LAYER4_WEEKLY, NEW_LAYER4_STALE)
log.append(f"  Layer4 stale-forecast term: {h}")

# Ganti juga di Forecasting mode section (dalam P33)
h = replace_in_doc(doc,
    "Directional Accuracy and Sharpe Ratio are computed from these weekly-trend "
    "signals and are reported as gross directional utility metrics.",
    "Directional Accuracy and Sharpe Ratio are computed from these "
    "stale-forecast signals and are reported as gross directional utility metrics."
)
log.append(f"  P33 weekly-trend -> stale: {h}")

# Ganti juga di Abstract
h = replace_in_doc(doc,
    "evaluated on recursive weekly-trend signals rather than executable hourly trades",
    "evaluated on stale-forecast signals — recursive predictions committed at the "
    "start of each 168-hour window, not updated as actual prices arrive"
)
log.append(f"  Abstract stale-forecast: {h}")

# Ganti di P80 practical implications
h = replace_in_doc(doc,
    "for gross risk-adjusted utility at the weekly forecast horizon.",
    "for gross risk-adjusted utility of the stale-forecast signal."
)
log.append(f"  P80 stale-forecast: {h}")

# ==============================================================
# FIX 4: Hapus kalimat Fold 6 Terra-Luna dan Fold 10 FTX dari paragraf fold
# ==============================================================
print("[4] Menghapus kalimat Terra-Luna/FTX dari paragraf fold...")

OLD_FOLD_TERRA = (
    "Note: with this stride, Fold 6 test window falls on ≈ 23–30 Apr 2022, "
    "which precedes the Terra-Luna collapse (9–12 May 2022) by approximately 9 days; "
    "no single fold precisely captures that event. Similarly, Fold 10 falls on "
    "≈ 28 Feb – 07 Mar 2023, which is after the FTX insolvency (8–11 Nov 2022). "
    "The model's sensitivity to volatility regime changes is discussed qualitatively in Section III.B. "
)

NEW_FOLD_TERRA = ""  # Dihapus seluruhnya

h = replace_in_doc(doc, OLD_FOLD_TERRA, NEW_FOLD_TERRA)
log.append(f"  Fold Terra-Luna/FTX sentences removed: {h}")

# ==============================================================
# FIX 5: Operational Boundaries — ganti "hourly sign rule can reverse"
# ==============================================================
print("[5] Memperbaiki Operational Boundaries stale-forecast framing...")

OLD_OP_HOURLY = (
    "A further boundary concerns transaction costs. "
    "The Layer 4 strategy return Rtstrategy = st · rt contains no cost term, "
    "so the Sharpe Ratios and VaR values in Table II are gross of fees and slippage. "
    "Because the hourly sign rule can reverse position at every step, "
    "turnover can be high, and recent studies show that gross profitability on "
    "hourly Bitcoin data can vanish at fee levels comparable to the 0.10% taker fee [36], [37]; "
    "the ranking in Table II is therefore a ranking of gross directional utility. "
    "The first planned extension is a net-of-cost formulation, "
    "Rtnet = st · rt − c · |st − st−1|, with c the per-side cost, "
    "combined with a cost-aware execution filter [37]. "
    "Sharpe Ratio differences across models were not formally tested here and "
    "should be assessed, e.g., by bootstrap [37]."
)

NEW_OP_HOURLY = (
    "A further boundary concerns transaction costs. "
    "The Layer 4 strategy return Rtstrategy = st · rt contains no cost term, "
    "so the Sharpe Ratios and VaR values in Table II are gross of fees and slippage. "
    "Although the stale-forecast signal is computed per hour, "
    "in practice it is committed at the start of each 168-hour test window "
    "and not revised as new prices arrive. "
    "If the signal is treated as a position held for the full 168 hours "
    "(a single weekly directional bet), turnover is 24 × lower than if "
    "each hourly signal were independently executed. "
    "The reported gross DA and Sharpe therefore represent an upper bound on "
    "net performance; actual net returns depend on whether a weekly or hourly "
    "execution interpretation is adopted. "
    "Recent studies show that gross profitability on hourly Bitcoin data can "
    "vanish at fee levels comparable to the 0.10% taker fee [36], [37]. "
    "The first planned extension is a net-of-cost formulation under both "
    "weekly and hourly execution interpretations, "
    "Rtnet = st · rt − c · |st − st−1|, with c the per-side cost [37]. "
    "Sharpe Ratio differences across models were not formally tested here and "
    "should be assessed by bootstrap [37]."
)

h = replace_in_doc(doc, OLD_OP_HOURLY, NEW_OP_HOURLY)
log.append(f"  Op Boundaries stale framing: {h}")

# ==============================================================
# FIX 6: Hapus referensi Fig. 3 di Operational Boundaries
# ==============================================================
h = replace_in_doc(doc,
    "This is a structural limitation of the current feature set. ",
    "This is a structural limitation of the current purely price-derived feature set. "
)
log.append(f"  Structural limitation text: {h}")

# ==============================================================
# FIX 7: Hapus gambar fisik Fig. 3 dari dokumen (inline shape)
# ==============================================================
print("[7] Mencoba menghapus gambar fisik Fig. 3...")

shapes_before = len(doc.inline_shapes)
fig3_removed = False

# Cari paragraf yang berisi inline shape (gambar) — biasanya paragraf kosong atau
# hanya berisi shape. Fig. 3 seharusnya ada setelah paragraf Error Distributions.
# Kita perlu cari paragraf yang tidak memiliki teks tetapi memiliki <a:blip> (gambar)
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p)
    # Cari paragraf yang mengandung gambar (inline shape) setelah error distributions section
    xml = p._p.xml
    if 'pic:pic' in xml or 'a:blip' in xml or 'v:imagedata' in xml:
        # Ini adalah paragraf gambar
        # Cek apakah ini gambar ke-3 (Fig. 3) — sekitar paragraf P73
        # Kita hapus semua paragraf gambar yang ada di section setelah P70 dan sebelum P75
        print(f"  Found image paragraph at P{i}: '{txt[:50]}'")

# Metode alternatif: hapus inline shape ke-3 (index 2) jika ada 4 shape (Fig 1, 2, 3, 4)
# Fig 1 = data ingestion, Fig 2 = forecast overlay, Fig 3 = residuals, Fig 4 = KPI dashboard
if len(doc.inline_shapes) >= 3:
    # Hapus shape ke-3 (index 2) = Fig. 3 residuals
    shape3 = doc.inline_shapes[2]
    # Hapus parent element dari shape
    shape_el = shape3._inline
    parent = shape_el.getparent()
    if parent is not None:
        grandparent = parent.getparent()
        if grandparent is not None:
            grandparent.remove(parent)
            fig3_removed = True
            print(f"  Fig.3 inline shape removed successfully")
        else:
            parent.remove(shape_el)
            fig3_removed = True
            print(f"  Fig.3 shape element removed from parent")

log.append(f"  Fig.3 physical removal: {'success' if fig3_removed else 'manual needed'}")
log.append(f"  Shapes before: {shapes_before}, after: {len(doc.inline_shapes)}")

# ==============================================================
# SAVE
# ==============================================================
doc.save(DST)
print(f"\n[SELESAI] Tersimpan: {DST}")
print(f"\nRingkasan:")
for entry in log:
    print(f"  {entry}")
