# -*- coding: utf-8 -*-
"""
fix_remaining_citations.py
Fix uncited references [17], [22], [23], [25]:
  - [22] PatchTST & [23] TimesNet: insert into Transformer paragraph
  - [17] Gers et al.: insert into LSTM/GRU paragraph
  - [25] Baqee et al.: insert into short-horizon overfitting sentence
"""
import sys, re
from docx import Document

sys.stdout.reconfigure(encoding='utf-8')

FNAME = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Deep Learning Framework for Cryptocurrency Price Prediction Using Business Intelligence.docx"

doc = Document(FNAME)

def replace_text(para, new_text):
    fmt_size, fmt_name, fmt_bold = None, None, False
    if para.runs:
        r0 = para.runs[0]
        fmt_size = r0.font.size
        fmt_name = r0.font.name
        fmt_bold = r0.bold
    for run in para.runs:
        run._element.getparent().remove(run._element)
    nr = para.add_run(new_text)
    if fmt_size: nr.font.size = fmt_size
    if fmt_name: nr.font.name = fmt_name
    nr.bold = fmt_bold

def gettxt(para):
    return "".join(r.text for r in para.runs).strip()

for para in doc.paragraphs:
    txt = gettxt(para)

    # ── [22] PatchTST, [23] TimesNet, [25] Baqee ─────────────────────────────
    # Current text of Transformer para (para 21):
    # "Transformer architectures relying on self-attention mechanisms [19] have
    #  increasingly been adapted for time-series forecasting [20]. The Informer
    #  Transformer [21], utilizing sparse probabilistic self-attention (O(L log L)),
    #  serves as the state-of-the-art baseline in this study, chosen for its
    #  established computational stability in hourly cryptocurrency environments.
    #  However, Transformers may suffer from overfitting during chaotic short-horizon
    #  intervals [24]–[26]."
    if txt.startswith("Transformer architectures relying on self-attention mechanisms [19]"):
        new = (
            "Transformer architectures relying on self-attention mechanisms [19] have increasingly "
            "been adapted for time-series forecasting [20]. The Informer Transformer [21], utilizing "
            "sparse probabilistic self-attention (O(L log L)), serves as the primary Transformer "
            "baseline in this study. While newer architectures such as PatchTST [22] and "
            "TimesNet [23] represent the current vanguard in multivariate modeling, the Informer "
            "provides a well-established, computationally stable benchmark. Transformers may "
            "nonetheless suffer from overfitting during chaotic short-horizon intervals "
            "such as 1-hour crypto data [24], [25], [26]."
        )
        replace_text(para, new)
        print("[Fix] [22] PatchTST, [23] TimesNet, [25] Baqee added to Transformer paragraph.")

    # ── [17] Gers et al. ─────────────────────────────────────────────────────
    # Current LSTM/GRU para includes [14], [15], [16]-[18]
    # "Tree-based models such as Extreme Gradient Boosting (XGBoost) model tabular
    #  financial data effectively [11], [12] but lack temporal sequence memory [13].
    #  The Long Short-Term Memory (LSTM) [14] and Gated Recurrent Unit (GRU) [15]
    #  address this via internal gating mechanisms and are widely applied to
    #  crypto-asset tracking [16]–[18]."
    if txt.startswith("Tree-based models such as Extreme Gradient Boosting"):
        new = (
            "Tree-based models such as Extreme Gradient Boosting (XGBoost) model tabular "
            "financial data effectively [11], [12] but lack temporal sequence memory [13]. "
            "The Long Short-Term Memory (LSTM) [14] addresses vanishing gradients via forget "
            "gates [17], while the Gated Recurrent Unit (GRU) [15] offers a simplified gating "
            "mechanism. Both are widely applied to crypto-asset tracking [16], [18]."
        )
        replace_text(para, new)
        print("[Fix] [17] Gers et al. inserted into LSTM/GRU paragraph.")

# ── Final citation audit ──────────────────────────────────────────────────────
doc.save(FNAME)
doc2 = Document(FNAME)
body_text = ""
in_refs = False
for p in doc2.paragraphs:
    if p.text.strip() == "REFERENCES":
        in_refs = True
    if not in_refs:
        body_text += p.text + " "

found = sorted(set(re.findall(r'\[(\d+)\]', body_text)), key=int)
missing = [r for r in range(1, 41) if str(r) not in found]
print(f"\nCitations in body : {found}")
print(f"Still uncited     : {missing if missing else 'NONE -- all 40 cited!'}")
print(f"\nSaved: {FNAME}")
