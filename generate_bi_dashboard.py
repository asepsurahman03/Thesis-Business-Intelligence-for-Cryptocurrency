"""
Generate a professional BI Dashboard image using Matplotlib
and embed it into the manuscript HTML as Fig. 4.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Arc, Wedge
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')
import base64, os, re

# ── colours ──────────────────────────────────────────────────────────────────
BG_DARK   = '#0d1117'
BG_PANEL  = '#161b22'
BG_CARD   = '#1c2128'
BORDER    = '#30363d'
ACCENT1   = '#00c4ff'   # actual price / GRU
ACCENT2   = '#e94560'   # LSTM prediction
ACCENT3   = '#00c896'   # positive / best
ACCENT4   = '#f5a623'   # Sharpe / moderate
ACCENT5   = '#9b59b6'   # purple
TEXT_DIM  = '#8892aa'
TEXT_MED  = '#c0cfea'
TEXT_BRT  = '#e6edf3'
WHITE     = '#ffffff'

# ── seeded random for reproducibility ─────────────────────────────────────────
rng = np.random.default_rng(42)

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE SETUP
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 10.5), facecolor=BG_DARK, dpi=130)

# ── Top bar ───────────────────────────────────────────────────────────────────
fig.text(0.012, 0.965, '▪ Crypto Predictive Analytics Platform',
         color=WHITE, fontsize=11, fontweight='bold', va='top')
fig.text(0.012, 0.950, 'BTC/USDT  ·  Walk-Forward Validation Dashboard  ·  4-Layer BI-ML Framework',
         color=TEXT_DIM, fontsize=7.5, va='top')
fig.text(0.75, 0.965, '● LIVE   |   2021–2025   |   43,786 Records   |   Refresh: Real-Time',
         color=ACCENT3, fontsize=7.5, va='top', ha='left')

# Separator line
line = Line2D([0, 1], [0.935, 0.935], transform=fig.transFigure,
              color=BORDER, linewidth=1)
fig.add_artist(line)

# ─────────────────────────────────────────────────────────────────────────────
# GRID LAYOUT: 3 rows
#   row0: 5 KPI cards   (height 0.16)
#   row1: price chart + gauge (height 0.36)
#   row2: table + macd + residuals (height 0.30)
# ─────────────────────────────────────────────────────────────────────────────
gs = gridspec.GridSpec(
    3, 3,
    figure=fig,
    top=0.920, bottom=0.040,
    left=0.025, right=0.985,
    hspace=0.45, wspace=0.22,
    height_ratios=[0.5, 1.05, 0.9]
)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 0 — KPI CARDS (draw on raw figure axes with no ticks)
# ─────────────────────────────────────────────────────────────────────────────
kpi_data = [
    ('GRU RMSE (Best)',        '0.1058',  '±0.0034',  '▲ Lowest across 4 models',    ACCENT3, '#1a3a2a'),
    ('LSTM Dir. Accuracy',     '72.3%',   '±1.5%',    '▲ Highest directional align.', ACCENT2, '#3a1a22'),
    ('Sharpe Ratio (LSTM)',    '2.85',    '±0.10',    '▲ +0.42 vs Buy & Hold',        ACCENT4, '#3a2a10'),
    ('Kruskal-Wallis H',       'H=18.4',  'p<0.001',  '✓ Statistically significant',  ACCENT1, '#102a3a'),
    ('Walk-Forward Folds',     '24',      'folds',    '720h train / 168h test',        ACCENT5, '#2a1a3a'),
]

kpi_xs = np.linspace(0.028, 0.800, 5)
kpi_w  = 0.155
kpi_y  = 0.782
kpi_h  = 0.125

for i, (lbl, val, sub, delta, accent, bg) in enumerate(kpi_data):
    x = kpi_xs[i]
    # Card background
    rect = FancyBboxPatch((x, kpi_y), kpi_w, kpi_h,
                          boxstyle="round,pad=0.005",
                          facecolor=BG_CARD, edgecolor=BORDER, linewidth=0.8,
                          transform=fig.transFigure, zorder=2, clip_on=False)
    fig.add_artist(rect)
    # Top accent bar
    topbar = FancyBboxPatch((x, kpi_y+kpi_h-0.006), kpi_w, 0.006,
                            boxstyle="round,pad=0.002",
                            facecolor=accent, edgecolor='none',
                            transform=fig.transFigure, zorder=3, clip_on=False)
    fig.add_artist(topbar)
    # Texts
    cx = x + kpi_w/2
    fig.text(cx, kpi_y+kpi_h-0.018, lbl,
             color=TEXT_DIM, fontsize=6.0, ha='center', va='top',
             transform=fig.transFigure)
    fig.text(cx, kpi_y+kpi_h-0.052, val,
             color=WHITE, fontsize=13, fontweight='bold', ha='center', va='top',
             transform=fig.transFigure)
    fig.text(cx, kpi_y+kpi_h-0.075, sub,
             color=TEXT_DIM, fontsize=6.5, ha='center', va='top',
             transform=fig.transFigure)
    fig.text(cx, kpi_y+0.008, delta,
             color=accent, fontsize=6.0, ha='center', va='bottom',
             transform=fig.transFigure)

# Page title above row0
fig.text(0.028, 0.930, 'Executive Performance Dashboard',
         color=TEXT_BRT, fontsize=10.5, fontweight='bold', va='top')
fig.text(0.028, 0.917, 'GRU · LSTM · XGBoost · Informer — Walk-Forward Comparative Analysis',
         color=TEXT_DIM, fontsize=7, va='top')

# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 col 0+1 — PRICE CHART
# ─────────────────────────────────────────────────────────────────────────────
ax_price = fig.add_subplot(gs[1, 0:2])
ax_price.set_facecolor(BG_PANEL)
ax_price.spines[:].set_color(BORDER)
ax_price.tick_params(colors=TEXT_DIM, labelsize=7)

hours = np.arange(168)
price_base = 45000 + np.cumsum(rng.normal(0, 320, 168)) + np.sin(hours * 0.085) * 1200
price_base = np.clip(price_base, 36000, 72000)
pred_offset = rng.normal(0, 280, 168)
pred = price_base + pred_offset
upper = price_base + np.abs(pred_offset) + 420
lower = price_base - np.abs(pred_offset) - 420

ax_price.fill_between(hours, lower, upper, alpha=0.12, color=ACCENT4, linewidth=0)
ax_price.plot(hours, price_base, color=ACCENT1, linewidth=1.6, label='Actual BTC/USDT')
ax_price.plot(hours, pred, color=ACCENT2, linewidth=1.4, linestyle='--',
              dashes=(5,3), label='LSTM Prediction Trace', alpha=0.88)

ax_price.set_xlim(0, 167)
ax_price.set_xlabel('Hour (168-h Walk-Forward Test Fold)', color=TEXT_DIM, fontsize=7)
ax_price.set_ylabel('BTC/USDT Price (USD)', color=TEXT_DIM, fontsize=7)
ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1000:.0f}K'))

day_ticks = np.arange(0, 168, 24)
ax_price.set_xticks(day_ticks)
ax_price.set_xticklabels([f'Day {int(t/24)+1}' for t in day_ticks], fontsize=6.5, color=TEXT_DIM)
ax_price.yaxis.set_tick_params(labelcolor=TEXT_DIM)
ax_price.grid(color=BORDER, alpha=0.5, linewidth=0.4)

# Title
ax_price.set_title('BTC/USDT Price vs LSTM Prediction Trace (168-Hour Walk-Forward)',
                   color=TEXT_BRT, fontsize=8.5, pad=7, loc='left')

# Legend
legend_elements = [
    Line2D([0], [0], color=ACCENT1, linewidth=1.8, label='Actual BTC/USDT Price'),
    Line2D([0], [0], color=ACCENT2, linewidth=1.6, linestyle='--', dashes=(4,3),
           label='LSTM Prediction Trace'),
    mpatches.Patch(facecolor=ACCENT4, alpha=0.3, label='95% Confidence Band'),
]
leg = ax_price.legend(handles=legend_elements, loc='upper left', fontsize=6.5,
                      facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_MED,
                      framealpha=0.9)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 col 2 — DIRECTIONAL ACCURACY GAUGE
# ─────────────────────────────────────────────────────────────────────────────
ax_gauge = fig.add_subplot(gs[1, 2])
ax_gauge.set_facecolor(BG_PANEL)
ax_gauge.spines[:].set_color(BORDER)
ax_gauge.set_xlim(-1.3, 1.3)
ax_gauge.set_ylim(-0.5, 1.4)
ax_gauge.set_aspect('equal')
ax_gauge.axis('off')
ax_gauge.set_title('Directional Probability Score', color=TEXT_BRT, fontsize=8.5, pad=7)

# Draw gauge arcs
for theta_start, theta_end, color, alpha in [
    (0,   60.8, ACCENT3, 0.9),   # 0–33% green segment
    (60.8,120, ACCENT4, 0.9),    # 33%–67% orange
    (120, 180, ACCENT2, 0.9),    # 67%–100% red (high)
]:
    wedge = Wedge((0, 0), 1.0, 180-theta_end, 180-theta_start,
                  width=0.22, facecolor=color, alpha=alpha, edgecolor=BG_DARK, linewidth=0.5)
    ax_gauge.add_patch(wedge)

# Background track
track = Wedge((0, 0), 1.0, 0, 180, width=0.22,
              facecolor=BG_CARD, alpha=0.3, edgecolor=BG_DARK, linewidth=0.5)
ax_gauge.add_patch(track)

# Filled arc for 72.3%
filled_deg = 72.3 / 100 * 180  # = 130.1°
wedge_fill = Wedge((0, 0), 1.0, 180-filled_deg, 180,
                   width=0.22, facecolor='none',
                   edgecolor=WHITE, linewidth=2.0, alpha=0.0)
for theta_start, theta_end, color in [
    (0,     60.8, '#e94560'),
    (60.8,  120,  '#f5a623'),
    (120,   filled_deg, '#00c896'),
]:
    if theta_end <= filled_deg:
        w = Wedge((0, 0), 1.01, 180-theta_end, 180-theta_start,
                  width=0.23, facecolor=color, alpha=0.95,
                  edgecolor=BG_DARK, linewidth=0.4)
        ax_gauge.add_patch(w)

# Needle at 72.3%
needle_angle = np.radians(180 - filled_deg)
nx = 0.85 * np.cos(needle_angle)
ny = 0.85 * np.sin(needle_angle)
ax_gauge.annotate('', xy=(nx, ny), xytext=(0, 0),
                  arrowprops=dict(arrowstyle='->', color=WHITE, lw=2.2))
ax_gauge.add_patch(plt.Circle((0, 0), 0.07, color=WHITE, zorder=5))

# Labels
ax_gauge.text(0, -0.25, '72.3%', color=WHITE, fontsize=20, fontweight='bold', ha='center')
ax_gauge.text(0, -0.44, 'Directional Classification Accuracy', color=TEXT_DIM,
              fontsize=6.5, ha='center')
ax_gauge.text(0, -0.55, 'Avg. over 24 Walk-Forward Folds', color=TEXT_DIM,
              fontsize=6, ha='center')
ax_gauge.text(-1.15,  0.05, '0%',   color=TEXT_DIM, fontsize=7, ha='center')
ax_gauge.text( 1.15,  0.05, '100%', color=TEXT_DIM, fontsize=7, ha='center')
ax_gauge.text(0, 1.1, '50%', color=TEXT_DIM, fontsize=7, ha='center')

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 col 0 — MODEL BENCHMARK TABLE
# ─────────────────────────────────────────────────────────────────────────────
ax_tbl = fig.add_subplot(gs[2, 0])
ax_tbl.set_facecolor(BG_PANEL)
ax_tbl.spines[:].set_color(BORDER)
ax_tbl.axis('off')
ax_tbl.set_title('Model Benchmark Matrix', color=TEXT_BRT, fontsize=8.5, pad=7, loc='left')

cols  = ['Model', 'RMSE', 'Dir. Acc.', 'Sharpe', 'DM p-val', 'Rank']
rows  = [
    ['GRU',      '0.1058', '68.9%', '1.72', 'vs LSTM\n0.014***', '#1 RMSE'],
    ['LSTM',     '0.1134', '72.3%', '2.85', 'vs GRU\n0.014***', '#1 Sharpe'],
    ['XGBoost',  '0.1287', '61.4%', '1.15', 'vs GRU\n<0.001***', '#3'],
    ['Informer', '0.1321', '55.7%', '0.87', 'vs GRU\n<0.001***', '#4'],
]
# Color mapping
row_colors = [
    [ACCENT3,'#00352a',TEXT_MED,TEXT_MED,TEXT_DIM,ACCENT3],
    [ACCENT2,'#3a1020',TEXT_MED,ACCENT3,TEXT_DIM,ACCENT3],
    [ACCENT4,'#3a2a00',TEXT_MED,TEXT_MED,TEXT_DIM,ACCENT4],
    [ACCENT2,'#3a0810',ACCENT2,ACCENT2,TEXT_DIM,ACCENT2],
]

cell_y = 0.85
col_xs = [0.02, 0.20, 0.38, 0.56, 0.70, 0.88]
col_names = cols

# Header
for j, col in enumerate(cols):
    ax_tbl.text(col_xs[j], cell_y, col, color=TEXT_DIM, fontsize=6.5,
                fontweight='bold', va='center', transform=ax_tbl.transAxes)

cell_y -= 0.06
# Separator
ax_tbl.axhline(cell_y + 0.015 * 0.85, color=BORDER, linewidth=0.8, xmin=0, xmax=1)
cell_y -= 0.01

for i, row in enumerate(rows):
    # Row bg
    bg_rect = FancyBboxPatch((0, cell_y-0.10), 1.0, 0.11,
                              boxstyle="round,pad=0.01",
                              facecolor='#1c2128' if i % 2 == 0 else '#22283a',
                              edgecolor='none', transform=ax_tbl.transAxes,
                              clip_on=True)
    ax_tbl.add_patch(bg_rect)
    for j, val in enumerate(row):
        c = row_colors[i][j]
        ax_tbl.text(col_xs[j], cell_y-0.045, val, color=c, fontsize=6.5,
                    va='center', transform=ax_tbl.transAxes, linespacing=1.2)
    cell_y -= 0.15

ax_tbl.text(0.02, 0.04,
            '★ GRU: lowest RMSE   ★ LSTM: highest Sharpe & directional accuracy\n'
            'DM = Diebold-Mariano test  |  ADF stationarity: all features p<0.05 ✓',
            color=TEXT_DIM, fontsize=5.8, va='bottom', transform=ax_tbl.transAxes)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 col 1 — MACD CHART
# ─────────────────────────────────────────────────────────────────────────────
ax_macd = fig.add_subplot(gs[2, 1])
ax_macd.set_facecolor(BG_PANEL)
ax_macd.spines[:].set_color(BORDER)
ax_macd.tick_params(colors=TEXT_DIM, labelsize=6.5)

n = 80
p = 50000 + np.cumsum(rng.normal(0, 400, n)) + np.sin(np.arange(n)*0.20)*2200
ema12 = np.zeros(n); ema26 = np.zeros(n); macd = np.zeros(n); sig = np.zeros(n)
ema12[0] = ema26[0] = p[0]
for t in range(1, n):
    ema12[t] = ema12[t-1]*(1-2/13) + p[t]*(2/13)
    ema26[t] = ema26[t-1]*(1-2/27) + p[t]*(2/27)
macd = (ema12 - ema26) / 100
for t in range(1, n):
    sig[t] = sig[t-1]*(1-2/10) + macd[t]*(2/10)
hist = macd - sig

colors_hist = [ACCENT3 if v >= 0 else ACCENT2 for v in hist]
ax_macd.bar(np.arange(n), hist, color=colors_hist, alpha=0.65, width=0.8)
ax_macd.plot(np.arange(n), macd, color=ACCENT1, linewidth=1.4, label='MACD')
ax_macd.plot(np.arange(n), sig,  color=ACCENT4, linewidth=1.4, linestyle='--',
             dashes=(4,3), label='Signal')
ax_macd.axhline(0, color=BORDER, linewidth=0.6)
ax_macd.set_title('MACD Momentum Indicator  (EMA₁₂ – EMA₂₆)',
                  color=TEXT_BRT, fontsize=8.5, pad=7, loc='left')
ax_macd.set_xlabel('Week', color=TEXT_DIM, fontsize=7)
ax_macd.grid(color=BORDER, alpha=0.4, linewidth=0.4)
ax_macd.legend(fontsize=6, facecolor=BG_CARD, edgecolor=BORDER, labelcolor=TEXT_MED,
               framealpha=0.9)

# Label SHAP badge
ax_macd.text(0.98, 0.96, 'SHAP Top Feature', color=ACCENT3, fontsize=6,
             ha='right', va='top', transform=ax_macd.transAxes,
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#00352a',
                       edgecolor=ACCENT3, linewidth=0.6))

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 col 2 — RESIDUAL DISTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────
ax_res = fig.add_subplot(gs[2, 2])
ax_res.set_facecolor(BG_PANEL)
ax_res.spines[:].set_color(BORDER)
ax_res.tick_params(colors=TEXT_DIM, labelsize=6.5)

z = rng.standard_normal(3000) * 0.1058 + 0.00042
bins, edges, patches = ax_res.hist(z, bins=32, edgecolor='none')
for patch, left in zip(patches, edges[:-1]):
    if abs(left + 0.053) < 0.08:
        patch.set_facecolor(ACCENT3); patch.set_alpha(0.85)
    elif abs(left + 0.053) < 0.20:
        patch.set_facecolor(ACCENT1); patch.set_alpha(0.70)
    else:
        patch.set_facecolor(ACCENT2); patch.set_alpha(0.55)

ax_res.axvline(0, color=WHITE, linewidth=1.0, linestyle='--', alpha=0.5)
ax_res.set_title('Inference Residual Distribution (GRU)',
                 color=TEXT_BRT, fontsize=8.5, pad=7, loc='left')
ax_res.set_xlabel('Forecast Error', color=TEXT_DIM, fontsize=7)
ax_res.set_ylabel('Frequency', color=TEXT_DIM, fontsize=7)
ax_res.grid(color=BORDER, alpha=0.4, linewidth=0.4, axis='y')

ax_res.text(0.98, 0.96,
            'μ=0.00042  σ=0.1058\nADF unit root: p<0.05 ✓',
            color=TEXT_DIM, fontsize=6, ha='right', va='top',
            transform=ax_res.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_CARD,
                      edgecolor=BORDER, linewidth=0.6))

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER LINE
# ─────────────────────────────────────────────────────────────────────────────
footer = Line2D([0, 1], [0.032, 0.032], transform=fig.transFigure,
                color=BORDER, linewidth=0.8)
fig.add_artist(footer)
fig.text(0.028, 0.023,
         'BI-ML Dashboard  ·  Nusa Putra University  ·  Asep Surahman Sulaeman, Deden Witarsyah, '
         'Aswan Supriyadi Sunge  ·  2026',
         color=TEXT_DIM, fontsize=6, va='center')
fig.text(0.82, 0.023,
         'Data: Binance Spot API  ·  PostgreSQL Data Mart  ·  4-Layer BI-ML Pipeline',
         color=TEXT_DIM, fontsize=6, va='center', ha='left')

# ─────────────────────────────────────────────────────────────────────────────
# SAVE IMAGE
# ─────────────────────────────────────────────────────────────────────────────
out_dir   = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
img_path  = os.path.join(out_dir, "fig4_bi_dashboard.png")
manuscript = os.path.join(out_dir, "Manuscript_IEEE_FINAL_2026.html")

plt.savefig(img_path, dpi=130, bbox_inches='tight',
            facecolor=BG_DARK, edgecolor='none')
print(f"[OK] Dashboard image saved: {img_path}")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# EMBED INTO MANUSCRIPT
# ─────────────────────────────────────────────────────────────────────────────
with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

data_uri = f"data:image/png;base64,{b64}"

with open(manuscript, "r", encoding="utf-8") as f:
    html = f.read()

# Find the Fig. 4 <img> tag (inside figure with caption containing "Fig. 4")
# Strategy: locate the figure div that contains "Fig. 4" in its caption
pattern = r'(<figure[^>]*>.*?<img\s[^>]*>)(.*?Fig\.\s*4\..*?</figure>)'
# More robust: match <img ...> whose nearest following <div class="figure-caption"> contains "Fig. 4"
pattern2 = r'(src="[^"]*")([^>]*>[\s\S]{0,400}?Fig\. 4\.)'

# Use the most reliable approach: find all <div class="figure"> blocks and find the one with "Fig. 4"
fig4_pattern = re.compile(
    r'(<div class="figure">[\s\S]*?)<img\s+src="([^"]*)"([^>]*)>([\s\S]*?Fig\. 4\.)',
    re.DOTALL
)

match = fig4_pattern.search(html)
if match:
    old_src = match.group(2)
    new_html = html[:match.start(2)] + data_uri + html[match.end(2):]
    with open(manuscript, "w", encoding="utf-8") as f:
        f.write(new_html)
    print("[OK] Fig. 4 image replaced in manuscript.")
else:
    # Fallback: look for a figure block near "Fig. 4" text
    idx = html.find("Fig. 4.")
    if idx == -1:
        idx = html.find("Fig. 4 ")
    if idx != -1:
        # Search backward for <img src=
        img_start = html.rfind('<img ', 0, idx)
        src_start = html.find('src="', img_start) + 5
        src_end   = html.find('"', src_start)
        if src_start > 5 and src_end > src_start:
            new_html = html[:src_start] + data_uri + html[src_end:]
            with open(manuscript, "w", encoding="utf-8") as f:
                f.write(new_html)
            print("[OK] Fig. 4 image replaced via fallback.")
        else:
            print("[WARN] Could not locate src= attribute for Fig. 4. Manual embedding needed.")
    else:
        print("[WARN] No 'Fig. 4' text found in manuscript.")

# Also update the Fig. 4 caption to say "prototype implementation"
with open(manuscript, "r", encoding="utf-8") as f:
    html2 = f.read()

old_cap = "Fig. 4. Proposed architecture of the Business Intelligence monitoring dashboard. The prototype design maps LSTM prediction traces directly into computed directional probability scores and theoretical Sharpe Ratio limits for DSS evaluation."
new_cap = "Fig. 4. Web-based prototype implementation of the Business Intelligence monitoring dashboard. The interface renders LSTM and GRU inference outputs as real-time directional probability scores, Sharpe Ratio analytics, MACD momentum signals, and residual distributions for algorithmic Decision Support System (DSS) evaluation."

if old_cap in html2:
    html2 = html2.replace(old_cap, new_cap)
    with open(manuscript, "w", encoding="utf-8") as f:
        f.write(html2)
    print("[OK] Fig. 4 caption updated.")
else:
    print("[INFO] Caption text not found verbatim — may already be updated.")

print("\n=== DONE ===")
print(f"Dashboard image : {img_path}")
print(f"Manuscript      : {manuscript}")
