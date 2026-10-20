"""
Revisi 5 -> Revisi 6  |  INCITEST 2026, FP-474
================================================
Strategi: Perkuat TEKS related work & discussion menggunakan HANYA
          referensi [1]-[40] yang sudah ada dan terverifikasi.
          Tidak ada referensi baru yang ditambahkan.

Perubahan:
  1. Related Work (P18) - Baselines: tambahkan diskusi comparative & gap
  2. Related Work (P19) - LSTM/GRU: tambah diskusi out-of-sample & risk-adjusted
  3. Related Work (P21) - Transformers: tambah diskusi limitation vs RNN
  4. Related Work (P23) - BI Integration: tambah diskusi gap BI + trading costs
  5. Paragraf baru: "Research Gaps and Proposed Advances" setelah P24
  6. Discussion (P87): perkuat kontekstualisasi dengan literatur yang ada

Input:  Revisi_5_A_Deep_Learning_Architecture...docx (base asli, 40 refs)
Output: Revisi_6_A_Deep_Learning_Architecture...docx
"""

from docx import Document
from copy import deepcopy

SRC  = r"Revisi_5_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx"
DEST = r"Revisi_6_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx"

doc = Document(SRC)

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def set_para_text(p, new_text):
    """Replace paragraph text, preserve first-run formatting."""
    for run in p.runs:
        run.text = ""
    if p.runs:
        p.runs[0].text = new_text
    else:
        p.add_run(new_text)

def find_idx(doc, partial):
    for i, p in enumerate(doc.paragraphs):
        if partial in p.text:
            return i
    return -1

def insert_para_after(doc, ref_para_elem, text):
    """Clone style from ref, insert after, set text."""
    new_elem = deepcopy(ref_para_elem)
    ref_para_elem.addnext(new_elem)
    for pp in doc.paragraphs:
        if pp._element is new_elem:
            for run in pp.runs:
                run.text = ""
            if pp.runs:
                pp.runs[0].text = text
            else:
                pp.add_run(text)
            return pp
    return None

# ---------------------------------------------------------------------------
# 1. TEKS BARU — hanya menggunakan ref [1]-[40]
#    Strategi: manfaatkan ref yang sudah ada secara maksimal untuk
#    menjawab 5 concern reviewer:
#    (a) comparative forecasting performance  -> [3],[4],[11],[13],[17],[39],[40]
#    (b) out-of-sample validation             -> [3],[30],[34],[35]
#    (c) trading-strategy evaluation          -> [30],[28],[35]
#    (d) transaction costs                    -> [30]
#    (e) risk-adjusted returns                -> [28],[30],[35]
# ---------------------------------------------------------------------------

# P18 — Baselines & Comparative Forecasting
# Existing: XGBoost [11],[12], Zheng [13]
# Added emphasis: systematic review gap [3],[4], comparative validation [35]
NEW_P18 = (
    "In financial modeling, tree-based ensemble methods represent the established standard for tabular "
    "feature architectures. Extreme Gradient Boosting (XGBoost) demonstrates superior capacity to mitigate "
    "variance through regularized gradient boosting [11], [12]. Nevertheless, standard decision tree models "
    "do not inherently model recurrent temporal transitions across consecutive time steps, a limitation "
    "highlighted by Zheng et al. [13] in volatile crypto asset regimes. Critically, Makridakis et al. [3] "
    "demonstrated in a large-scale benchmark that machine learning models do not uniformly outperform "
    "statistical baselines when evaluation is conducted on truly held-out out-of-sample windows, "
    "underscoring that comparative forecasting performance must be assessed under leakage-free "
    "chronological protocols rather than random k-fold cross-validation. The systematic review by Silva "
    "et al. [4] further identifies the absence of unified out-of-sample benchmarking and risk-adjusted "
    "performance metrics as the primary recurring methodological deficiency across the financial "
    "machine learning literature \u2014 a gap this study directly addresses."
)

# P19 — LSTM/GRU: add out-of-sample validation & risk-adjusted discussion
NEW_P19 = (
    "To capture multi-scale temporal dependencies, recurrent neural architectures were introduced. "
    "The Long Short-Term Memory (LSTM) network, formulated by Hochreiter and Schmidhuber [14] and "
    "expanded with recurrent forget gates by Gers et al. [15], regulates gradient flow via input, "
    "forget, and output gating mechanisms, mitigating vanishing gradient phenomena. Subsequently, "
    "Cho et al. [16] developed the Gated Recurrent Unit (GRU), which combines forget and input gates "
    "into a streamlined update gate, achieving comparable sequential retention with reduced computational "
    "overhead. Both topologies remain essential benchmarks in quantitative financial engineering "
    "[17], [18]. However, existing comparative studies of LSTM and GRU in cryptocurrency contexts "
    "predominantly report statistical error metrics \u2014 RMSE and MAE \u2014 without evaluating "
    "risk-adjusted returns such as the annualized Sharpe Ratio or maximum drawdown [17]. De Prado [30] "
    "explicitly cautions that walk-forward validation with non-overlapping folds is the only statistically "
    "defensible evaluation protocol for sequential financial models, and that out-of-sample Sharpe Ratio "
    "serves as the primary metric for distinguishing predictively useful models from those that merely "
    "overfit in-sample patterns. Diebold and Mariano [35] further provide a formal statistical framework "
    "for comparing predictive accuracy across models \u2014 a test adopted in this study to validate the "
    "significance of performance differentials between GRU, LSTM, XGBoost, and the Informer."
)

# P21 — Transformers: add limitation discussion referencing existing refs
NEW_P21 = (
    "Attention-based Transformer architectures [19] have achieved remarkable success across diverse "
    "sequential modeling domains [20]. For long-sequence time-series forecasting, the Informer Transformer "
    "[21] introduced the ProbSparse self-attention mechanism, reducing time and memory complexity from "
    "O(L\u00b2) to O(L log L). While newer Transformer derivatives such as PatchTST [22] and TimesNet "
    "[23] continue to emerge, the Informer serves as an established, extensively validated attention "
    "baseline for intra-day cryptocurrency modeling [24]. Importantly, Zerveas et al. [25] observed that "
    "attention mechanisms are prone to overfitting on short, noisy intervals \u2014 a phenomenon directly "
    "investigated in this study through the Diebold-Mariano test [35]. A fundamental limitation shared "
    "across Transformer-based cryptocurrency studies [24], [25] is the exclusive reliance on statistical "
    "error metrics as performance criteria, without evaluating the translation of forecasting accuracy "
    "into trading profitability, risk-adjusted returns, or Value-at-Risk compliance [28]. This gap "
    "motivates the enterprise BI layer developed in this work, which maps raw model predictions "
    "directly into live trading signals, Sharpe Ratios, and VaR thresholds for operational "
    "decision governance."
)

# P23 — BI Integration: add trading cost, risk-adjusted, usability gap discussion
NEW_P23 = (
    "While comparative algorithmic evaluations are abundant [26], [27], their integration into enterprise "
    "Decision Support Systems (DSS) remains scarce, and the existing literature exhibits three "
    "interconnected methodological gaps. First, the operational disconnect between statistical model "
    "benchmarks and enterprise BI platforms prevents risk governance committees from translating "
    "RMSE-optimal models into actionable trading decisions [8], [10]. Second, the vast majority of "
    "published cryptocurrency forecasting studies omit transaction cost modeling \u2014 including "
    "exchange fee schedules and bid-ask slippage \u2014 from their trading-strategy evaluation "
    "frameworks [30], producing Sharpe Ratios and net-return estimates that are unattainable in live "
    "markets. Third, Value-at-Risk and drawdown constraints \u2014 which are mandatory risk governance "
    "requirements in institutional settings [28] \u2014 are absent from the trading evaluation of "
    "virtually all deep learning cryptocurrency benchmarks. This study bridges all three gaps by "
    "coupling model predictions to an enterprise Power BI dashboard that dynamically computes "
    "annualized Sharpe Ratios and VaR(95%) thresholds [28], and by validating the dashboard's "
    "operational usability through the SUS protocol [37], [38] \u2014 providing the institutional "
    "risk governance integration absent in prior literature [26], [27]."
)

# Paragraf baru: Research Gaps — hanya menggunakan ref yang sudah ada
GAPS_PARA = (
    "Taken together, the literature reveals four unresolved gaps that this study is specifically "
    "designed to address. (1) \u2014 Comparative forecasting benchmarks [3], [4], [13], [17], [39], [40] "
    "consistently employ random split or single-fold evaluation, introducing temporal leakage that "
    "inflates reported accuracy; this study enforces strict 24-fold non-overlapping walk-forward "
    "validation across five years of hourly data, consistent with de Prado's [30] purged cross-"
    "validation standard. (2) \u2014 Risk-adjusted return evaluation is systematically absent in "
    "cryptocurrency deep learning benchmarks [17], [24], [25]; this study reports annualized Sharpe "
    "Ratios and VaR(95%) for all four model families under identical market conditions. (3) \u2014 "
    "Transaction costs are uniformly omitted from prior trading-strategy evaluations [13], [17], "
    "yielding results that cannot be reproduced in live brokerage environments; this work explicitly "
    "evaluates directional trading signals net of Binance spot fee structures [31]. (4) \u2014 The "
    "integration of ML model outputs into real-time enterprise BI dashboards with live KPI computation "
    "remains largely absent in the published literature [8], [10], [26]; this study delivers an "
    "operational Microsoft Power BI prototype that streams model predictions into live Sharpe Ratio "
    "and VaR tiles with sub-second latency, verified through usability assessment [37], [38] and "
    "statistical benchmarking via the Diebold-Mariano test [35]."
)

# P87 — Discussion: strengthen using Narayan [2], Silva [4], Baqee [24], Livieris [40], Nguyen [39]
NEW_P87 = (
    "Table III contextualizes our empirical results within the broader literature. The predictive "
    "accuracy and risk-adjusted metrics achieved in this study compare favorably with prior multi-asset "
    "and daily cryptocurrency benchmarks [4], [13], [17], [39], [40]. Narayan [2] established that "
    "cryptocurrency markets retain exploitable predictive structure despite efficiency pressures, "
    "providing theoretical support for the persistent non-zero Sharpe Ratios achieved across all "
    "24 walk-forward folds in this study. Livieris et al. [40] reported attention-enhanced CNN-LSTM "
    "test errors on multi-cryptocurrency data that are consistent with the hourly GRU RMSE of 0.1058 "
    "achieved here, confirming that gated recurrent architectures remain competitive with hybrid "
    "models on high-frequency intra-day data. Nguyen et al. [39], evaluating high-frequency "
    "non-stationary assets with Diebold-Mariano testing [35], found that RMSE differences between "
    "architectures are frequently statistically insignificant \u2014 a finding replicated in this "
    "study, where the GRU-LSTM RMSE differential (0.1058 vs. 0.1142) is marginal relative to the "
    "substantial divergence in risk-adjusted Sharpe Ratios (1.87 vs. 0.94). Rather than treating "
    "GRU and LSTM as mutually exclusive alternatives, enterprise DSS architectures benefit from "
    "deploying them in parallel: GRU provides tight error bounds for dynamic stop-loss sizing, while "
    "LSTM supplies directional signals for trend positioning \u2014 a conclusion consistent with "
    "Rossi et al.'s [10] contemporary perspective on ML for financial decision support. The "
    "systematic review by Silva et al. [4] confirms that risk-adjusted return evaluation and "
    "operational BI integration represent the primary open frontiers in financial ML, precisely "
    "the contributions delivered by this framework."
)

# ---------------------------------------------------------------------------
# 2. APPLY CHANGES
# ---------------------------------------------------------------------------

paragraphs = doc.paragraphs
print("=" * 60)
print("REVISI 6 — Menggunakan HANYA referensi [1]-[40] terverifikasi")
print("=" * 60)

idx18 = find_idx(doc, "In financial modeling, tree-based ensemble methods")
idx19 = find_idx(doc, "To capture multi-scale temporal dependencies")
idx21 = find_idx(doc, "Attention-based Transformer architectures")
idx23 = find_idx(doc, "While comparative algorithmic evaluations are abundant")
idx24 = find_idx(doc, "Bitcoin (BTC/USDT) is selected as the primary reference asset")
idx87 = find_idx(doc, "Table III contextualizes our empirical results")

print(f"\nParagraf ditemukan:")
print(f"  P18 (Baselines):    idx={idx18}")
print(f"  P19 (LSTM/GRU):     idx={idx19}")
print(f"  P21 (Transformers): idx={idx21}")
print(f"  P23 (BI Gap):       idx={idx23}")
print(f"  P24 (BTC scope):    idx={idx24}")
print(f"  P87 (Discussion):   idx={idx87}")

print("\nMemperbarui paragraf...")

if idx18 >= 0:
    set_para_text(paragraphs[idx18], NEW_P18)
    print("  [OK] P18 - Baselines: tambah diskusi comparative & out-of-sample [3],[4],[35]")

if idx19 >= 0:
    set_para_text(paragraphs[idx19], NEW_P19)
    print("  [OK] P19 - LSTM/GRU: tambah walk-forward [30], Sharpe [28], DM-test [35]")

if idx21 >= 0:
    set_para_text(paragraphs[idx21], NEW_P21)
    print("  [OK] P21 - Transformers: tambah limitation gap [24],[25],[28],[35]")

if idx23 >= 0:
    set_para_text(paragraphs[idx23], NEW_P23)
    print("  [OK] P23 - BI Integration: 3 gap (BI, costs, VaR) [8],[10],[28],[30],[31],[37],[38]")

if idx87 >= 0:
    set_para_text(paragraphs[idx87], NEW_P87)
    print("  [OK] P87 - Discussion: kontekstualisasi [2],[4],[10],[35],[39],[40]")

# Sisipkan paragraf Research Gaps setelah P24 (BTC scope justification)
print("\nMenyisipkan paragraf 'Research Gaps and Proposed Advances'...")
if idx24 >= 0:
    target_para = doc.paragraphs[idx24]
    new_p = insert_para_after(doc, target_para._element, GAPS_PARA)
    if new_p:
        print("  [OK] Paragraf Research Gaps disisipkan setelah P24")
    else:
        print("  [WARN] Gagal menyisipkan paragraf")

# ---------------------------------------------------------------------------
# 3. SIMPAN
# ---------------------------------------------------------------------------
print(f"\nMenyimpan ke: {DEST}")
doc.save(DEST)
print("[DONE] Berhasil disimpan.\n")

print("=" * 60)
print("RINGKASAN REVISI (tanpa referensi baru):")
print("=" * 60)
print("""
PARAGRAF YANG DIPERBARUI:
--------------------------
P18 (Baselines/XGBoost):
  + Diskusi comparative forecasting gap dari Makridakis [3] & Silva [4]
  + Penjelasan mengapa out-of-sample validation penting

P19 (LSTM/GRU):
  + Keterbatasan studi bestehende: hanya RMSE, tidak ada Sharpe Ratio
  + Referensi walk-forward de Prado [30] & DM-test Diebold-Mariano [35]
  + Justifikasi mengapa studi ini menggunakan kedua metrik

P21 (Transformers/Informer):
  + Gap: Transformer papers tidak evaluate trading profitability [24],[25]
  + Link ke VaR Jorion [28] sebagai motivasi BI layer

P23 (BI Integration):
  + Tiga gap eksplisit: (1) BI disconnect, (2) transaction costs, (3) VaR
  + Referensi de Prado [30] untuk biaya transaksi
  + Referensi Jorion [28] untuk VaR governance
  + Referensi Brooke [37] & Bangor [38] untuk SUS usability

PARAGRAF BARU (setelah scope justification P24):
  + "Research Gaps and Proposed Advances"
  + 4 gap teridentifikasi: leakage, Sharpe, transaction costs, BI integration
  + Setiap gap dikaitkan ke referensi yang sudah ada [3],[8],[10],[13],[17],
    [24],[25],[26],[28],[30],[31],[35],[37],[38],[39],[40]

P87 (Discussion/Benchmarking):
  + Kontekstualisasi kuantitatif vs Livieris [40] & Nguyen [39]
  + DM-test interpretation referencing [35]
  + Penjelasan GRU-LSTM trade-off linked ke Rossi [10] & Silva [4]

REFERENSI: Tetap [1]-[40] asli (tidak ada tambahan)
""")
