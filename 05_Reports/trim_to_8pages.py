# -*- coding: utf-8 -*-
"""
trim_to_8pages.py
Trim the REVISED.docx to ~8 pages by:
  1. Removing BIOGRAPHIES OF AUTHORS section
  2. Trimming Table 3 (Literature Comparison) to 4 rows
  3. Shortening long paragraphs
  4. Removing Deployment Constraints paragraph
"""
import sys
from docx import Document
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

SRC = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

DST = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

doc = Document(SRC)

# ─── Helper ──────────────────────────────────────────────────────────────────
def replace_para_text(para, new_text):
    """Replace paragraph text preserving formatting of first run."""
    fmt_size, fmt_name, fmt_bold = None, None, False
    if para.runs:
        r0 = para.runs[0]
        fmt_size = r0.font.size
        fmt_name = r0.font.name
        fmt_bold = r0.bold
    for run in para.runs:
        run._element.getparent().remove(run._element)
    new_run = para.add_run(new_text)
    if fmt_size: new_run.font.size = fmt_size
    if fmt_name: new_run.font.name = fmt_name
    new_run.bold = fmt_bold

def delete_para(para):
    p = para._element
    p.getparent().remove(p)

def get_text(para):
    return "".join(r.text for r in para.runs).strip()

# ═══════════════════════════════════════════════════════════════════════════════
# FIX A — Trim Table 3 (Literature Comparison): keep header + Livieris + This study rows
# Remove rows: Zheng[13], Silva[4], Nguyen[26] — keep Chen[16], Livieris[38], 2x This study
# ═══════════════════════════════════════════════════════════════════════════════
t3 = doc.tables[3]
# Row indices: 0=header, 1=Chen, 2=Zheng, 3=Silva, 4=Nguyen, 5=Livieris, 6=This study GRU, 7=This study LSTM
rows_to_delete = [2, 3, 4]  # Zheng, Silva, Nguyen
for ri in sorted(rows_to_delete, reverse=True):
    row = t3.rows[ri]
    row._element.getparent().remove(row._element)
print(f"[Fix A] Table 3 trimmed: removed 3 rows (Zheng, Silva, Nguyen). Kept: header + Chen + Livieris + 2x This study.")

# ═══════════════════════════════════════════════════════════════════════════════
# FIX B — Shorten specific long paragraphs
# ═══════════════════════════════════════════════════════════════════════════════
SHORTENING = {
    # Para [24]: Transformer section — long Informer rationale trimmed
    "Transformer architectures, relying on Attention mechanisms": (
        "Transformer architectures relying on self-attention mechanisms [19] have increasingly "
        "been adapted for time-series forecasting [20]. The Informer Transformer [21], utilizing "
        "sparse probabilistic self-attention (O(L log L)), serves as the state-of-the-art baseline "
        "in this study, chosen for its established computational stability in hourly cryptocurrency "
        "environments. However, Transformers may suffer from overfitting during chaotic short-horizon "
        "intervals [24]–[26]."
    ),
    # Para [28]: Dataset scope — cut from 4 reasons to 1 sentence
    "Regarding dataset scope: BTC/USDT was selected as the sole asset for three reasons.": (
        "BTC/USDT was selected as the sole asset because Bitcoin maintains the highest market "
        "capitalization and trading volume among cryptocurrencies, and exclusive reliance on a "
        "single asset acts as a rigorous experimental control to isolate BI pipeline performance "
        "from cross-asset microstructural friction [1], [30]."
    ),
    # Para [15]: BI-ML Framework proposal — shorten
    "To address this gap, this study proposes an \"End-to-End BI-ML Framework.\"": (
        "To address this gap, this study proposes an end-to-end BI-Machine Learning framework "
        "mapping raw API feeds through automated Walk-Forward Validation into a production-ready "
        "Power BI dashboard, comparing XGBoost, LSTM, GRU, and the Informer Transformer on "
        "high-frequency hourly cryptocurrency data."
    ),
    # Para [139]: Deployment Constraints — DELETE (handled separately below)
    # Para [154]: Limitation — shorten
    "A critical limitation that must be explicitly acknowledged is the susceptibility": (
        "A key limitation is all tested models' susceptibility to exogenous volatility events "
        "exceeding ±3\u03c3 deviations from training distributions — events such as the Terra-Luna "
        "collapse — where pure statistical inference fails without macroeconomic contextual signals. "
        "Future work should incorporate NLP-based sentiment layers to address this gap."
    ),
    # Para [161]: Conclusion second para — shorten
    "Regarding model performance, a global Kruskal-Wallis validation": (
        "A global Kruskal-Wallis test (p\u202f<\u202f0.001) and pairwise Diebold-Mariano tests (p\u202f=\u202f0.014) "
        "confirmed GRU as the top RMSE model (0.1058\u202f\u00b1\u202f0.0034), while LSTM achieved the highest "
        "Directional Accuracy (72.3\u202f%) and Sharpe Ratio (1.45), with the Power BI dashboard "
        "achieving an Excellent SUS score of 86.4, validating the framework's institutional utility."
    ),
    # Para [162]: Future research — cut from 4 directions to 2
    "Future research should address four directions.": (
        "Future research should pursue two directions: (1) integrating NLP sentiment signals from "
        "social media and on-chain data to improve resilience during macroeconomic shocks; and "
        "(2) extending the BI pipeline to multi-asset portfolios incorporating altcoins and "
        "cross-market correlation matrices."
    ),
    # Para [153]: Practical implications — shorten
    "From a practical decision-support standpoint, the GRU's tighter RMSE bounds": (
        "From a practical standpoint, the GRU's tighter RMSE bounds provide the most reliable "
        "stop-loss thresholds, while LSTM's superior directional accuracy (72.3\u202f%) makes it "
        "preferable for signal-generation in algorithmic trading applications."
    ),
}

paragraphs_to_delete = []
for para in doc.paragraphs:
    txt = get_text(para)
    for trigger, new_txt in SHORTENING.items():
        if txt.startswith(trigger[:60]):
            replace_para_text(para, new_txt)
            print(f"[Fix B] Shortened: '{trigger[:60]}...'")
            break

# ═══════════════════════════════════════════════════════════════════════════════
# FIX C — Delete "Deployment Constraints" paragraph entirely
# ═══════════════════════════════════════════════════════════════════════════════
for para in doc.paragraphs:
    txt = get_text(para)
    if txt.startswith("Deployment Constraints: Broader institutional"):
        paragraphs_to_delete.append(para)
        print(f"[Fix C] Marked for deletion: 'Deployment Constraints...'")

# ═══════════════════════════════════════════════════════════════════════════════
# FIX D — Remove entire BIOGRAPHIES OF AUTHORS section
#          Everything from "BIOGRAPHIES OF AUTHORS" heading to end of doc
#          (but keep REFERENCES section)
# ═══════════════════════════════════════════════════════════════════════════════
in_bio = False
for para in doc.paragraphs:
    txt = get_text(para)
    if txt == "BIOGRAPHIES OF AUTHORS":
        in_bio = True
    if in_bio:
        paragraphs_to_delete.append(para)

print(f"[Fix D] Marked {len([p for p in paragraphs_to_delete if get_text(p).startswith('BIOGRAPHIES') or in_bio])} biography paragraph(s) for deletion.")

# Execute deletions
for para in paragraphs_to_delete:
    try:
        delete_para(para)
    except Exception:
        pass  # already removed or parent changed
print(f"[Fix D] Biography section removed.")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(DST)
print(f"\nDone. Saved trimmed document to:\n{DST}")
