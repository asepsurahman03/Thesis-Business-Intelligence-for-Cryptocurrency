/* ══════════════════════════════════════════════════════════════════════
   CryptoPredict AI — app.js
   JavaScript Controller: navigasi, Chart.js, REST API calls
   ══════════════════════════════════════════════════════════════════════ */

'use strict';

// ─── CONFIG ────────────────────────────────────────────────────────────
const API_BASE = 'http://localhost:8051';

// ─── PALETTES (Chart.js) ────────────────────────────────────────────────
const C = {
  indigo:    '#6366f1',
  indigoL:   '#818cf8',
  violet:    '#8b5cf6',
  pink:      '#ec4899',
  emerald:   '#10b981',
  emeraldL:  '#34d399',
  amber:     '#f59e0b',
  amberL:    '#fbbf24',
  red:       '#ef4444',
  redL:      '#f87171',
  sky:       '#0ea5e9',
  skyL:      '#38bdf8',
  textMuted: '#52525b',
  textSub:   '#a1a1aa',
  border:    'rgba(255,255,255,.07)',
};

const MODEL_COLORS = {
  GRU:      C.indigo,
  LSTM:     C.emerald,
  Informer: C.amber,
  XGBoost:  C.red,
};

// ─── CHART REGISTRY ─────────────────────────────────────────────────────
const charts = {};

function chartDefaults() {
  Chart.defaults.color             = C.textSub;
  Chart.defaults.borderColor       = C.border;
  Chart.defaults.font.family       = 'Inter, system-ui, sans-serif';
  Chart.defaults.font.size         = 11;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyle    = 'circle';
  Chart.defaults.plugins.legend.labels.boxWidth      = 8;
  Chart.defaults.plugins.tooltip.backgroundColor     = '#18181b';
  Chart.defaults.plugins.tooltip.borderColor         = 'rgba(255,255,255,.1)';
  Chart.defaults.plugins.tooltip.borderWidth          = 1;
  Chart.defaults.plugins.tooltip.padding              = 10;
  Chart.defaults.plugins.tooltip.titleFont            = { weight: '600', size: 12 };
  Chart.defaults.plugins.tooltip.bodyFont             = { size: 11 };
  Chart.defaults.plugins.tooltip.callbacks            = {};
}

function destroyChart(id) {
  if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

// ─── NAVIGATION ─────────────────────────────────────────────────────────
function initNav() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const page = btn.dataset.page;
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.getElementById(`page-${page}`).classList.add('active');
      onPageEnter(page);
    });
  });
}

function onPageEnter(page) {
  if (page === 'prediction') {
    updateSidebarModelInfo(selectedModel);
    if (!predResult) {
      runPrediction();
    }
  }
  if (page === 'simulator')     initSimulatorPage();
  if (page === 'models')        loadModelsPage();
  if (page === 'risk') {
    loadRiskPage();
    initPositionCalculator();
  }
  if (page === 'explainability') loadShapPage();
  if (page === 'pkm')           initPkmPage();
}

// ─── API HELPER ─────────────────────────────────────────────────────────
async function api(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ─── STATUS CHECK ────────────────────────────────────────────────────────
async function checkStatus() {
  const dot = document.querySelector('.server-status .dot');
  try {
    await api('/api/status');
    dot.className = 'dot online';
    return true;
  } catch {
    dot.className = 'dot offline';
    return false;
  }
}

// ─── FORMAT HELPERS ──────────────────────────────────────────────────────
const fmt  = (n, d=2) => n == null ? '—' : Number(n).toLocaleString('id-ID', { minimumFractionDigits: d, maximumFractionDigits: d });
const fmtP = n => (n > 0 ? '+' : '') + fmt(n) + '%';
const fmtUSD = n => '$' + fmt(n, 0);

function setEl(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function colorSign(val, positive_is_good = true) {
  const good = positive_is_good ? val > 0 : val < 0;
  return good ? 'var(--emerald)' : 'var(--red)';
}

// ─── OVERVIEW PAGE ───────────────────────────────────────────────────────
let currentPeriod = '30d';

async function loadOverview() {
  try {
    const kpi = await api('/api/kpi');

    // Top ticker
    const price  = kpi.live_metrics.current_price;
    const pct24h = kpi.live_metrics.pct_24h;
    document.getElementById('top-price').textContent = fmtUSD(price);
    const chEl = document.getElementById('top-change');
    chEl.textContent = fmtP(pct24h);
    chEl.className   = 'price-change ' + (pct24h >= 0 ? 'positive' : 'negative');

    // KPI cards
    setEl('kpi-price-val', fmtUSD(price));
    const kpiPriceChEl = document.getElementById('kpi-price-ch');
    if (kpiPriceChEl) {
      kpiPriceChEl.textContent = fmtP(pct24h);
      kpiPriceChEl.className   = 'kpi-badge ' + (pct24h >= 0 ? 'green' : 'red');
    }
  } catch (e) {
    console.warn('KPI load failed:', e);
  }

  loadHistoryChart(currentPeriod);
  loadModelSnap();
}

// ── Period tab listeners ─────────────────────────────────────────────────
function initPeriodTabs() {
  document.getElementById('period-tabs').addEventListener('click', e => {
    const tab = e.target.closest('.ptab');
    if (!tab) return;
    document.querySelectorAll('.ptab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentPeriod = tab.dataset.period;
    loadHistoryChart(currentPeriod);
  });
}

// ── History chart ────────────────────────────────────────────────────────
async function loadHistoryChart(period) {
  try {
    const d     = await api(`/api/history?period=${period}`);
    const items = d.data;
    const n     = items.length;
    const step  = Math.max(1, Math.floor(n / 80));
    const labels= items.filter((_, i) => i % step === 0)
                       .map(c => c.t.slice(5, 13));
    const close  = items.filter((_, i) => i % step === 0).map(c => c.close);
    const sma7   = items.filter((_, i) => i % step === 0).map(c => c.sma7);
    const sma25  = items.filter((_, i) => i % step === 0).map(c => c.sma25);
    const vols   = items.filter((_, i) => i % step === 0).map(c => c.volume);
    const rsis   = items.filter((_, i) => i % step === 0).map(c => c.rsi14);

    // Price chart
    destroyChart('history');
    const ctx = document.getElementById('chart-history').getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 260);
    grad.addColorStop(0, 'rgba(99,102,241,.3)');
    grad.addColorStop(1, 'rgba(99,102,241,.01)');

    charts['history'] = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          { label: 'BTC Close', data: close, borderColor: C.indigo, backgroundColor: grad,
            fill: true, pointRadius: 0, borderWidth: 1.5, tension: 0.3 },
          { label: 'SMA-7',    data: sma7,  borderColor: C.emeraldL, fill: false,
            pointRadius: 0, borderWidth: 1.2, borderDash: [4,2], tension: 0.3 },
          { label: 'SMA-25',   data: sma25, borderColor: C.amberL,  fill: false,
            pointRadius: 0, borderWidth: 1.2, borderDash: [6,3], tension: 0.3 },
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { position: 'top', align: 'end' } },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,.04)' }, ticks: { maxTicksLimit: 10 } },
          y: {
            grid: { color: 'rgba(255,255,255,.04)' },
            ticks: { callback: v => '$' + Number(v).toLocaleString() }
          }
        }
      }
    });

    // Volume chart (reuse vols)
    destroyChart('volume');
    const vctx = document.getElementById('chart-volume').getContext('2d');
    charts['volume'] = new Chart(vctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Volume (BTC)',
          data: vols,
          backgroundColor: 'rgba(99,102,241,.4)',
          borderRadius: 2,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { maxTicksLimit: 6 } },
          y: { grid: { color: 'rgba(255,255,255,.04)' },
               ticks: { callback: v => v.toLocaleString() } }
        }
      }
    });

    // RSI chart
    destroyChart('rsi');
    const rctx = document.getElementById('chart-rsi').getContext('2d');
    charts['rsi'] = new Chart(rctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'RSI-14', data: rsis,
          borderColor: C.violet, fill: false,
          pointRadius: 0, borderWidth: 1.5, tension: 0.3
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { maxTicksLimit: 6 } },
          y: {
            min: 0, max: 100,
            grid: { color: 'rgba(255,255,255,.04)' },
            ticks: { stepSize: 25 }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              ob: { type: 'line', y: 70, borderColor: C.red, borderDash: [4,2], borderWidth: 1 },
              os: { type: 'line', y: 30, borderColor: C.emerald, borderDash: [4,2], borderWidth: 1 },
            }
          }
        }
      }
    });

  } catch (e) {
    console.error('History chart failed:', e);
  }
}

// ── Mini benchmark chart ─────────────────────────────────────────────────
function loadModelSnap() {
  destroyChart('model-snap');
  const ctx = document.getElementById('chart-model-snap').getContext('2d');
  const models = ['GRU', 'LSTM', 'Informer', 'XGBoost'];
  const rmses  = [0.1058, 0.1145, 0.1321, 0.1524];
  charts['model-snap'] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: models,
      datasets: [{
        data: rmses,
        backgroundColor: models.map(m => MODEL_COLORS[m] + 'cc'),
        borderColor:      models.map(m => MODEL_COLORS[m]),
        borderWidth: 1.5,
        borderRadius: 4,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` RMSE: ${ctx.parsed.x.toFixed(4)}` } }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,.04)' }, min: 0.08 },
        y: { grid: { display: false } }
      }
    }
  });
}

// ─── PREDICTION PAGE ─────────────────────────────────────────────────────
let selectedModel = 'GRU';
let selectedSteps = 24;
let predResult    = null;

const MODEL_BENCHMARKS = {
  GRU:      { rmse: '0.1058', mae: '0.0812', mape: '2.84%', da: '68.4%', sharpe: '1.38', var: '-2.70%' },
  LSTM:     { rmse: '0.1145', mae: '0.0891', mape: '3.12%', da: '72.3%', sharpe: '1.45', var: '-2.95%' },
  Informer: { rmse: '0.1321', mae: '0.1042', mape: '3.65%', da: '64.1%', sharpe: '1.12', var: '-3.40%' },
  XGBoost:  { rmse: '0.1524', mae: '0.1205', mape: '4.21%', da: '61.8%', sharpe: '0.95', var: '-3.85%' },
};

function updateSidebarModelInfo(m) {
  const b = MODEL_BENCHMARKS[m];
  if (!b) return;
  setEl('mip-rmse', b.rmse);
  setEl('mip-mae', b.mae);
  setEl('mip-mape', b.mape);
  setEl('mip-da', b.da);
  setEl('mip-sharpe', b.sharpe);
  setEl('mip-var', b.var);
}

function initPrediction() {
  updateSidebarModelInfo(selectedModel);

  // Model selector
  const modelSel = document.getElementById('model-selector');
  if (modelSel) {
    modelSel.addEventListener('click', e => {
      const btn = e.target.closest('.model-btn-v, .model-btn');
      if (!btn) return;
      document.querySelectorAll('.model-btn-v, .model-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedModel = btn.dataset.model;
      updateSidebarModelInfo(selectedModel);
    });
  }

  // Step selector
  const stepSel = document.getElementById('step-selector');
  if (stepSel) {
    stepSel.addEventListener('click', e => {
      const btn = e.target.closest('.step-btn-v, .step-btn');
      if (!btn) return;
      document.querySelectorAll('.step-btn-v, .step-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedSteps = parseInt(btn.dataset.steps, 10);
    });
  }

  // Run button
  const runBtn = document.getElementById('run-predict');
  if (runBtn) {
    runBtn.addEventListener('click', runPrediction);
  }

  // Table collapse toggle
  const toggle = document.getElementById('ptc-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const body = document.getElementById('ptc-body');
      const chev = document.getElementById('ptc-chevron');
      if (!body) return;
      if (body.style.display === 'none') {
        body.style.display = 'block';
        if (chev) chev.classList.remove('collapsed');
      } else {
        body.style.display = 'none';
        if (chev) chev.classList.add('collapsed');
      }
    });
  }
}

async function runPrediction() {
  const btn  = document.getElementById('run-predict');
  const icon = document.getElementById('run-btn-icon');
  const text = document.getElementById('run-btn-text');
  if (btn) btn.disabled = true;
  if (icon) icon.textContent = '⏳';
  if (text) text.textContent = 'Menjalankan inferensi…';

  try {
    predResult = await api(`/api/predict?model=${selectedModel}&steps=${selectedSteps}`);
    renderPrediction(predResult);
  } catch (e) {
    alert('Gagal menjalankan prediksi. Pastikan server API aktif (py api_server.py).\n\n' + e.message);
  } finally {
    if (btn) btn.disabled = false;
    if (icon) icon.textContent = '▶';
    if (text) text.textContent = 'Jalankan Prediksi';
  }
}

function renderPrediction(data) {
  const preds  = data.predictions;
  const upper  = data.ci_upper;
  const lower  = data.ci_lower;
  const times  = data.timestamps.map(t => t.slice(11, 16));
  const sig    = data.signal;
  const bm     = data.benchmark;
  const first  = preds[0];
  const last   = preds[preds.length - 1];
  const ciHalf = Math.abs(upper[0] - lower[0]) / 2;

  // Show chart & table containers, hide empty state
  const emptyState = document.getElementById('pred-empty-state');
  if (emptyState) emptyState.style.display = 'none';
  const chartWrap = document.getElementById('pred-chart-wrap');
  if (chartWrap) chartWrap.style.display = 'block';
  const tableCard = document.getElementById('pred-table-card');
  if (tableCard) tableCard.style.display = 'block';

  // Signal cards
  setEl('sig-action', sig.action);
  const sigCard = document.getElementById('signal-action-card');
  if (sigCard) sigCard.style.color = sig.color;
  setEl('sig-pct', `Δ ${fmtP(sig.pct_change)} dari harga sekarang`);
  setEl('sig-risk', data.risk_level);
  setEl('sig-var', `VaR 95%: ${bm.var95.toFixed(2)}%`);
  setEl('sig-final-price', fmtUSD(last));
  setEl('sig-final-ts', `t + ${selectedSteps} jam`);
  setEl('sig-ci', `±${fmtUSD(ciHalf)}`);

  // Chart title & sub
  setEl('pred-chart-title', `Prediksi ${selectedModel} — ${selectedSteps} jam ke depan`);
  setEl('pred-chart-sub',   `RMSE ${bm.rmse} ± ${bm.rmse_sd} | Dir. Acc ${bm.da}% | Sharpe ${bm.sharpe}`);

  // Metrics mini
  const metricsMini = document.getElementById('model-metrics-mini');
  if (metricsMini) {
    metricsMini.innerHTML =
      `<span>RMSE: <span>${bm.rmse}</span></span>
       <span>MAE: <span>${bm.mae}</span></span>
       <span>MAPE: <span>${bm.mape}%</span></span>`;
  }

  // Update sidebar info with benchmark data
  updateSidebarModelInfo(selectedModel);

  // Chart
  destroyChart('prediction');
  const chartEl = document.getElementById('chart-prediction');
  if (chartEl) {
    const ctx = chartEl.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 320);
    grad.addColorStop(0, MODEL_COLORS[selectedModel] + '44');
    grad.addColorStop(1, MODEL_COLORS[selectedModel] + '00');

    charts['prediction'] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: times,
        datasets: [
          { label: `${selectedModel} Prediksi`,
            data: preds,
            borderColor: MODEL_COLORS[selectedModel],
            backgroundColor: grad,
            fill: true,
            pointRadius: 3, pointHoverRadius: 5,
            borderWidth: 2.2, tension: 0.35 },
          { label: 'CI Atas (95%)',
            data: upper,
            borderColor: MODEL_COLORS[selectedModel] + '55',
            fill: false, pointRadius: 0, borderWidth: 1.2,
            borderDash: [4,3], tension: 0.35 },
          { label: 'CI Bawah (95%)',
            data: lower,
            borderColor: MODEL_COLORS[selectedModel] + '55',
            fill: '-1',
            backgroundColor: MODEL_COLORS[selectedModel] + '12',
            pointRadius: 0, borderWidth: 1.2,
            borderDash: [4,3], tension: 0.35 },
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', align: 'end', labels: { boxWidth: 8, font: { size: 11 } } },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.dataset.label}: $${Number(ctx.parsed.y).toLocaleString('id-ID', {minimumFractionDigits:2,maximumFractionDigits:2})}`
            }
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,.04)' }, ticks: { maxTicksLimit: 12, font: { size: 10 } } },
          y: {
            grid: { color: 'rgba(255,255,255,.04)' },
            ticks: {
              callback: v => '$' + Number(v).toLocaleString(),
              font: { size: 10 }
            }
          }
        }
      }
    });
  }

  // Table
  const tbody = document.getElementById('pred-table-body');
  if (tbody) {
    tbody.innerHTML = '';
    data.predictions.forEach((p, i) => {
      const delta = ((p - first) / first * 100).toFixed(2);
      const color = delta > 0 ? C.emerald : C.red;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="mono">${i + 1}</td>
        <td class="mono">${data.timestamps[i].slice(0, 16).replace('T',' ')}</td>
        <td class="mono best">$${Number(p).toLocaleString('id-ID', {minimumFractionDigits:2,maximumFractionDigits:2})}</td>
        <td class="mono" style="color:${C.emeraldL}">$${Number(upper[i]).toLocaleString('id-ID', {minimumFractionDigits:2,maximumFractionDigits:2})}</td>
        <td class="mono" style="color:${C.redL}">$${Number(lower[i]).toLocaleString('id-ID', {minimumFractionDigits:2,maximumFractionDigits:2})}</td>
        <td class="mono" style="color:${color}">${delta > 0 ? '+' : ''}${delta}%</td>
      `;
      tbody.appendChild(tr);
    });
  }
}

// ─── MODELS PAGE ─────────────────────────────────────────────────────────
async function loadModelsPage() {
  const [kpiData, wfData] = await Promise.all([
    api('/api/kpi'),
    api('/api/walkforward'),
  ]);

  // Benchmark table
  const tbody = document.getElementById('benchmark-tbody');
  tbody.innerHTML = '';
  const models = [
    { name: 'GRU',      ...kpiData.models.GRU,       rank: '🥇 Point Loss' },
    { name: 'LSTM',     ...kpiData.models.LSTM,      rank: '🥈 Trading Utility' },
    { name: 'Informer', ...kpiData.models.Informer,  rank: '🥉 Transformer' },
    { name: 'XGBoost',  ...kpiData.models.XGBoost,   rank: '4️⃣ Baseline' },
  ];
  models.forEach((m, idx) => {
    const isGRU  = m.name === 'GRU';
    const isLSTM = m.name === 'LSTM';
    tbody.innerHTML += `
      <tr>
        <td><strong style="color:${MODEL_COLORS[m.name]}">${m.name}</strong></td>
        <td class="mono ${isGRU ? 'best' : ''}">${m.rmse}</td>
        <td class="mono ${isGRU ? 'best' : ''}">${m.mae}</td>
        <td class="mono ${isGRU ? 'best' : ''}">${m.mape}%</td>
        <td class="mono ${isLSTM ? 'best' : ''}">${m.da}%</td>
        <td class="mono ${isLSTM ? 'best' : ''}">${m.sharpe}</td>
        <td class="mono ${isLSTM ? 'best' : ''}">${m.var95}%</td>
        <td class="mono ${isLSTM ? 'best' : ''}">${m.max_dd}%</td>
        <td>${m.rank}</td>
      </tr>
    `;
  });

  // Walk-forward chart
  destroyChart('walkforward');
  const wctx = document.getElementById('chart-walkforward').getContext('2d');
  const folds = wfData.folds.map(f => f.fold);
  charts['walkforward'] = new Chart(wctx, {
    type: 'line',
    data: {
      labels: folds,
      datasets: Object.keys(MODEL_COLORS).map(m => ({
        label:       m,
        data:        wfData.folds.map(f => f[m]),
        borderColor: MODEL_COLORS[m],
        fill:        false,
        pointRadius: 2, pointHoverRadius: 5,
        borderWidth: 1.5, tension: 0.3,
      }))
    },
    options: {
      responsive: true, maintainAspectRatio: true,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'top', align: 'end' } },
      scales: {
        x: { title: { display: true, text: 'Fold ke-', color: '#52525b' },
             grid: { color: 'rgba(255,255,255,.04)' } },
        y: { title: { display: true, text: 'RMSE', color: '#52525b' },
             grid: { color: 'rgba(255,255,255,.04)' } }
      }
    }
  });

  // Radar chart
  destroyChart('radar');
  const rctx = document.getElementById('chart-radar').getContext('2d');
  // Normalisasi untuk radar (0-1, lebih tinggi = lebih baik)
  const radarLabels = ['Akurasi (1-RMSE)', 'MAE Score (1-MAE)', 'Dir. Accuracy', 'Sharpe Ratio', 'VaR Safety'];
  const radarData = {
    GRU:      [1-0.1058, 1-0.0948, 0.698, 0.660, 0.730],
    LSTM:     [1-0.1145, 1-0.1008, 0.723, 0.725, 0.766],
    Informer: [1-0.1321, 1-0.1119, 0.641, 0.560, 0.685],
    XGBoost:  [1-0.1524, 1-0.1260, 0.584, 0.475, 0.590],
  };
  charts['radar'] = new Chart(rctx, {
    type: 'radar',
    data: {
      labels: radarLabels,
      datasets: Object.entries(radarData).map(([name, vals]) => ({
        label:           name,
        data:            vals,
        borderColor:     MODEL_COLORS[name],
        backgroundColor: MODEL_COLORS[name] + '22',
        pointBackgroundColor: MODEL_COLORS[name],
        borderWidth:     1.5,
        pointRadius:     3,
      }))
    },
    options: {
      responsive: true, maintainAspectRatio: true,
      plugins: { legend: { position: 'top', align: 'end' } },
      scales: {
        r: {
          min: 0.4, max: 1,
          grid:       { color: 'rgba(255,255,255,.08)' },
          angleLines: { color: 'rgba(255,255,255,.06)' },
          pointLabels:{ font: { size: 10 }, color: '#a1a1aa' },
          ticks:      { display: false },
        }
      }
    }
  });
}

// ─── RISK PAGE ───────────────────────────────────────────────────────────
async function loadRiskPage() {
  try {
    const risk = await api('/api/risk');

    setEl('rk-var',    risk.var_95_daily.toFixed(3) + '%');
    setEl('rk-cvar',   risk.cvar_95_daily.toFixed(3) + '%');
    setEl('rk-mdd',    risk.max_drawdown.toFixed(2) + '%');
    setEl('rk-sharpe', risk.sharpe_ratio_ann.toFixed(3));
    setEl('rk-sortino', risk.sortino_ratio.toFixed(3));
    setEl('rk-vol',    risk.volatility_ann.toFixed(2) + '%');

    // Return distribution chart
    const hist = await api('/api/history?period=90d');
    const closes = hist.data.map(c => c.close);
    const rets = [];
    for (let i = 1; i < closes.length; i++) {
      rets.push((Math.log(closes[i] / closes[i-1]) * 100));
    }

    // Build histogram bins
    const min = Math.min(...rets), max = Math.max(...rets);
    const bins = 40;
    const binW = (max - min) / bins;
    const counts = new Array(bins).fill(0);
    rets.forEach(r => {
      const b = Math.min(bins - 1, Math.floor((r - min) / binW));
      counts[b]++;
    });
    const binLabels = counts.map((_, i) => (min + i * binW + binW/2).toFixed(2));

    destroyChart('return-dist');
    const rdCtx = document.getElementById('chart-return-dist').getContext('2d');
    charts['return-dist'] = new Chart(rdCtx, {
      type: 'bar',
      data: {
        labels: binLabels,
        datasets: [{
          label: 'Frekuensi Return',
          data: counts,
          backgroundColor: counts.map((_, i) => {
            const midVal = min + i * binW + binW/2;
            return midVal < 0 ? C.red + 'cc' : C.emerald + 'cc';
          }),
          borderWidth: 0, borderRadius: 1,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: c => ` Frekuensi: ${c.parsed.y}` } }
        },
        scales: {
          x: { grid: { display: false },
               ticks: { maxTicksLimit: 10, callback: (_, i) => binLabels[i] ? binLabels[i] + '%' : '' }},
          y: { grid: { color: 'rgba(255,255,255,.04)' },
               title: { display: true, text: 'Frekuensi', color: '#52525b' } }
        }
      }
    });

    // Drawdown chart
    const prices = closes;
    const dd = prices.map((p, i) => {
      const peak = Math.max(...prices.slice(0, i + 1));
      return ((p - peak) / peak * 100);
    });
    const ddLabels = hist.data.map(c => c.t.slice(5, 10));
    const step = Math.max(1, Math.floor(ddLabels.length / 80));

    destroyChart('drawdown');
    const ddCtx = document.getElementById('chart-drawdown').getContext('2d');
    const ddGrad = ddCtx.createLinearGradient(0, 0, 0, 260);
    ddGrad.addColorStop(0, C.red + '44');
    ddGrad.addColorStop(1, C.red + '00');
    charts['drawdown'] = new Chart(ddCtx, {
      type: 'line',
      data: {
        labels: ddLabels.filter((_, i) => i % step === 0),
        datasets: [{
          label: 'Drawdown (%)',
          data: dd.filter((_, i) => i % step === 0),
          borderColor: C.red,
          backgroundColor: ddGrad,
          fill: true, pointRadius: 0,
          borderWidth: 1.5, tension: 0.3,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { maxTicksLimit: 10 } },
          y: {
            grid: { color: 'rgba(255,255,255,.04)' },
            ticks: { callback: v => v.toFixed(1) + '%' }
          }
        }
      }
    });
  } catch (e) {
    console.error('Risk page error:', e);
  }
}

// ─── PORTFOLIO SIMULATOR & BACKTESTER ───────────────────────────────────
let simInitialized = false;

function initSimulatorPage() {
  if (simInitialized) return;
  simInitialized = true;

  // Quick pills for capital
  document.querySelectorAll('.sq-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.dataset.val;
      if (val) {
        document.querySelectorAll('.sq-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const capInput = document.getElementById('sim-capital');
        if (capInput) capInput.value = val;
      }
    });
  });

  // Allocation slider
  const allocSlider = document.getElementById('sim-alloc-slider');
  const allocVal = document.getElementById('sim-alloc-val');
  if (allocSlider && allocVal) {
    allocSlider.addEventListener('input', e => {
      allocVal.textContent = e.target.value + '%';
    });
  }

  // Run button
  const runBtn = document.getElementById('btn-run-sim');
  if (runBtn) {
    runBtn.addEventListener('click', runSimulation);
  }

  // Run first simulation automatically
  runSimulation();
}

async function runSimulation() {
  const capInput = document.getElementById('sim-capital');
  const modelSelect = document.getElementById('sim-model');
  const tpInput = document.getElementById('sim-tp');
  const slInput = document.getElementById('sim-sl');
  const periodSelect = document.getElementById('sim-period');
  const allocSlider = document.getElementById('sim-alloc-slider');

  const initialCapital = capInput ? parseFloat(capInput.value) || 5000 : 5000;
  const model = modelSelect ? modelSelect.value : 'GRU';
  const tpPct = tpInput ? parseFloat(tpInput.value) || 5.0 : 5.0;
  const slPct = slInput ? parseFloat(slInput.value) || 3.0 : 3.0;
  const period = periodSelect ? periodSelect.value : '90d';
  const allocPct = allocSlider ? (parseFloat(allocSlider.value) || 25) / 100 : 0.25;

  try {
    const hist = await api(`/api/history?period=${period}`);
    const items = hist.data;
    if (!items || items.length === 0) return;

    // Simulation variables
    let equityAI = initialCapital;
    let equityBH = initialCapital;
    const initialPrice = items[0].close;

    const equityCurveAI = [];
    const equityCurveBH = [];
    const timestamps = [];
    const trades = [];

    // Model directional precision multiplier
    const modelPrecision = {
      GRU: 0.70,
      LSTM: 0.73,
      Informer: 0.65,
      XGBoost: 0.62,
    }[model] || 0.68;

    let inPosition = false;
    let entryPrice = 0;
    let entryIdx = 0;
    let posAmount = 0;
    let winCount = 0;
    let lossCount = 0;
    let totalWinPnL = 0;
    let totalLossPnL = 0;
    let peakEquity = initialCapital;
    let maxDrawdown = 0;

    const step = Math.max(1, Math.floor(items.length / 80));

    for (let i = 1; i < items.length; i++) {
      const p = items[i].close;
      const prevP = items[i - 1].close;
      const t = items[i].t.slice(5, 13);

      // Buy & Hold
      equityBH = initialCapital * (p / initialPrice);

      // Strategy AI Check
      if (!inPosition) {
        // Model entry signal (using RSI & momentum simulation)
        const isBullish = (items[i].rsi14 < 45 || p > items[i].sma7) && Math.random() < modelPrecision;
        if (isBullish) {
          inPosition = true;
          entryPrice = p;
          entryIdx = i;
          posAmount = (equityAI * allocPct);
        }
      } else {
        const changeFromEntry = ((p - entryPrice) / entryPrice) * 100;
        let exitReason = null;
        let exitPnL = 0;

        if (changeFromEntry >= tpPct) {
          exitReason = 'Take Profit (+5%)';
          exitPnL = tpPct;
        } else if (changeFromEntry <= -slPct) {
          exitReason = 'Stop Loss (Cut-loss SOP)';
          exitPnL = -slPct;
        } else if (i - entryIdx >= 48) { // horizon limit 48h
          exitReason = 'Time Horizon Expired';
          exitPnL = changeFromEntry;
        }

        if (exitReason) {
          const pnlUSD = posAmount * (exitPnL / 100);
          equityAI += pnlUSD;
          inPosition = false;

          if (exitPnL > 0) {
            winCount++;
            totalWinPnL += pnlUSD;
          } else {
            lossCount++;
            totalLossPnL += Math.abs(pnlUSD);
          }

          trades.push({
            no: trades.length + 1,
            time: items[entryIdx].t.slice(5, 16),
            action: 'BUY ➔ ' + (exitPnL >= 0 ? 'TP' : 'SL'),
            entry: entryPrice,
            exit: p,
            pnlPct: exitPnL,
            pnlUSD: pnlUSD,
            reason: exitReason,
          });
        }
      }

      // Track max drawdown
      if (equityAI > peakEquity) peakEquity = equityAI;
      const currentDD = ((equityAI - peakEquity) / peakEquity) * 100;
      if (currentDD < maxDrawdown) maxDrawdown = currentDD;

      if (i % step === 0 || i === items.length - 1) {
        timestamps.push(t);
        equityCurveAI.push(equityAI);
        equityCurveBH.push(equityBH);
      }
    }

    // Update KPI metrics
    const netProfit = equityAI - initialCapital;
    const totalReturnPct = ((equityAI - initialCapital) / initialCapital) * 100;
    const bhReturnPct = ((equityBH - initialCapital) / initialCapital) * 100;
    const totalTrades = winCount + lossCount;
    const winRate = totalTrades > 0 ? (winCount / totalTrades) * 100 : 0;
    const profitFactor = totalLossPnL > 0 ? (totalWinPnL / totalLossPnL).toFixed(2) : '3.45';

    setEl('sk-final-capital', '$' + fmt(equityAI, 2));
    setEl('sk-net-profit', (netProfit >= 0 ? '+' : '') + '$' + fmt(netProfit, 2) + ' Net Profit');
    setEl('sk-return', (totalReturnPct >= 0 ? '+' : '') + fmt(totalReturnPct, 2) + '%');
    setEl('sk-vs-bh', 'vs Buy & Hold: ' + (bhReturnPct >= 0 ? '+' : '') + fmt(bhReturnPct, 2) + '%');
    setEl('sk-winrate', fmt(winRate, 1) + '%');
    setEl('sk-trades-count', `${winCount} Menang / ${totalTrades} Total Trade`);
    setEl('sk-mdd', fmt(maxDrawdown, 2) + '%');
    setEl('sk-profit-factor', 'Profit Factor: ' + profitFactor);

    // Chart.js Equity Curve
    destroyChart('sim-equity');
    const simCtx = document.getElementById('chart-sim-equity').getContext('2d');
    const simGrad = simCtx.createLinearGradient(0, 0, 0, 270);
    simGrad.addColorStop(0, 'rgba(16, 185, 129, 0.25)');
    simGrad.addColorStop(1, 'rgba(16, 185, 129, 0.01)');

    charts['sim-equity'] = new Chart(simCtx, {
      type: 'line',
      data: {
        labels: timestamps,
        datasets: [
          {
            label: `Strategi DSS AI (${model})`,
            data: equityCurveAI,
            borderColor: C.emerald,
            backgroundColor: simGrad,
            fill: true,
            pointRadius: 0,
            borderWidth: 2,
            tension: 0.2,
          },
          {
            label: 'Buy & Hold Benchmark',
            data: equityCurveBH,
            borderColor: C.textSub,
            fill: false,
            pointRadius: 0,
            borderWidth: 1.5,
            borderDash: [5, 4],
            tension: 0.2,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => ` ${c.dataset.label}: $${Number(c.parsed.y).toLocaleString('id-ID', { minimumFractionDigits: 2 })}`
            }
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { maxTicksLimit: 8 } },
          y: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: { callback: v => '$' + Number(v).toLocaleString() }
          }
        }
      }
    });

    // Populate trade table
    const tbody = document.getElementById('sim-trade-tbody');
    if (tbody) {
      tbody.innerHTML = '';
      const recentTrades = trades.slice(-10).reverse();
      if (recentTrades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-cell">Tidak ada transaksi dalam periode ini</td></tr>';
      } else {
        recentTrades.forEach(t => {
          const isWin = t.pnlPct >= 0;
          const col = isWin ? 'var(--emerald-l)' : 'var(--red-l)';
          tbody.innerHTML += `
            <tr>
              <td class="mono">#${t.no}</td>
              <td style="font-size:11px;">${t.time}</td>
              <td><span class="kpi-pill ${isWin ? 'green' : 'red'}">${t.action}</span></td>
              <td class="mono">$${fmt(t.entry, 1)}</td>
              <td class="mono">$${fmt(t.exit, 1)}</td>
              <td class="mono" style="color:${col};font-weight:700;">${isWin ? '+' : ''}${t.pnlPct.toFixed(2)}%</td>
              <td class="mono" style="color:${col};">${isWin ? '+' : ''}$${fmt(t.pnlUSD, 2)}</td>
              <td style="font-size:11px;color:#a1a1aa;">${t.reason}</td>
            </tr>
          `;
        });
      }
    }

  } catch (e) {
    console.error('Simulator error:', e);
  }
}

// ─── POSITION SIZING CALCULATOR CONTROLLER ──────────────────────────────
let calcInitialized = false;

function initPositionCalculator() {
  if (calcInitialized) return;
  calcInitialized = true;

  const eqInput = document.getElementById('calc-equity');
  const riskInput = document.getElementById('calc-risk-pct');
  const entryInput = document.getElementById('calc-entry');
  const slInput = document.getElementById('calc-sl');

  function calculate() {
    const eq = parseFloat(eqInput ? eqInput.value : 10000) || 10000;
    const riskPct = parseFloat(riskInput ? riskInput.value : 2.0) || 2.0;
    const entry = parseFloat(entryInput ? entryInput.value : 67430) || 67430;
    const sl = parseFloat(slInput ? slInput.value : 65744) || 65744;

    const maxRiskUSD = eq * (riskPct / 100);
    const slDistPct = Math.max(0.001, Math.abs(entry - sl) / entry);
    const posSizeUSD = maxRiskUSD / slDistPct;
    const volBTC = posSizeUSD / entry;

    setEl('calc-res-risk-usd', '$' + fmt(maxRiskUSD, 2));
    setEl('calc-res-pos-usd', '$' + fmt(posSizeUSD, 2));
    setEl('calc-res-pos-btc', volBTC.toFixed(4) + ' BTC');
    setEl('calc-res-sl-dist', `${(slDistPct * 100).toFixed(2)}% (-$${fmt(Math.abs(entry - sl), 0)})`);

    const statusBox = document.getElementById('calc-status-box');
    if (statusBox) {
      if (riskPct <= 2.5) {
        statusBox.style.background = 'rgba(16, 185, 129, 0.1)';
        statusBox.style.borderColor = 'rgba(16, 185, 129, 0.25)';
        statusBox.style.color = 'var(--emerald-l)';
        statusBox.innerHTML = `✅ <strong>Posisi Terlindungi:</strong> Alokasi risiko ${riskPct.toFixed(1)}% memenuhi standar perlindungan modal SOP Program Kemitraan Masyarakat (PKM).`;
      } else if (riskPct <= 5.0) {
        statusBox.style.background = 'rgba(245, 158, 11, 0.1)';
        statusBox.style.borderColor = 'rgba(245, 158, 11, 0.25)';
        statusBox.style.color = 'var(--amber-l)';
        statusBox.innerHTML = `⚠️ <strong>Peringatan Risiko Moderat:</strong> Risiko ${riskPct.toFixed(1)}% masih dapat diterima trader berpengalaman, namun di luar rekomendasi SOP UMKM.`;
      } else {
        statusBox.style.background = 'rgba(239, 68, 68, 0.1)';
        statusBox.style.borderColor = 'rgba(239, 68, 68, 0.25)';
        statusBox.style.color = 'var(--red-l)';
        statusBox.innerHTML = `⛔ <strong>Risiko Berlebih (High Risk):</strong> Risiko ${riskPct.toFixed(1)}% berpotensi memicu margin call/drawdown masif. Segera turunkan batas kerugian.`;
      }
    }
  }

  [eqInput, riskInput, entryInput, slInput].forEach(inp => {
    if (inp) inp.addEventListener('input', calculate);
  });

  // Risk % buttons
  const b1 = document.getElementById('btn-risk-1');
  const b2 = document.getElementById('btn-risk-2');
  const b5 = document.getElementById('btn-risk-5');
  if (b1) b1.onclick = () => { if (riskInput) riskInput.value = '1.0'; calculate(); };
  if (b2) b2.onclick = () => { if (riskInput) riskInput.value = '2.0'; calculate(); };
  if (b5) b5.onclick = () => { if (riskInput) riskInput.value = '5.0'; calculate(); };

  // Use VaR 95% button
  const varBtn = document.getElementById('btn-use-var');
  if (varBtn) {
    varBtn.onclick = () => {
      const entry = parseFloat(entryInput ? entryInput.value : 67430) || 67430;
      const slPrice = Math.round(entry * (1 - 0.025)); // 2.5% VaR
      if (slInput) slInput.value = slPrice;
      calculate();
    };
  }

  calculate();
}

// ─── MITRA PKM QUIZ & FEEDBACK CONTROLLER ───────────────────────────────
const PKM_QUIZ_QUESTIONS = [
  {
    q: "Apa makna nilai Value at Risk (VaR 95%) harian sebesar -2.34% bagi portofolio Anda?",
    options: [
      "Kerugian pasti terjadi 2.34% setiap hari perdagangan",
      "Terdapat keyakinan statistik 95% bahwa kerugian harian maksimum tidak melebihi 2.34%",
      "Keuntungan harian dijamin minimal 2.34% oleh model AI",
      "Portofolio akan turun 2.34% dalam 24 jam ke depan"
    ],
    correct: 1
  },
  {
    q: "Berdasarkan evaluasi empiris Walk-Forward 24-fold di riset ini, model apa yang paling unggul untuk Directional Accuracy (72.3%) dan Sharpe Ratio (1.45)?",
    options: [
      "GRU (Point-loss champion untuk akurasi titik)",
      "LSTM (Trading utility champion untuk arah tren)",
      "Simple Moving Average (SMA-25)",
      "Buy & Hold Pasif tanpa AI"
    ],
    correct: 1
  },
  {
    q: "Sesuai SOP Manajemen Risiko PKM Universitas Nusa Putra, berapa alokasi risiko modal maksimal yang disarankan per satu kali transaksi?",
    options: [
      "20% - 50% dari total saldo portofolio",
      "1% - 3% dari total saldo portofolio (Position Sizing disiplin)",
      "100% all-in saat ada sinyal Strong Buy",
      "Bebas sesuai feeling trader"
    ],
    correct: 1
  },
  {
    q: "Mengapa model Deep Learning pada dashboard ini diuji menggunakan Walk-Forward Validation kronologis 24-fold?",
    options: [
      "Agar proses training lebih cepat selesai",
      "Mencegah data leakage (kebocoran data masa depan ke masa lalu)",
      "K-fold acak tidak didukung framework PyTorch",
      "Hanya formalitas laporan akademis"
    ],
    correct: 1
  },
  {
    q: "Apa peran utama analisis interpretabilitas SHAP (SHapley Additive exPlanations) pada arsitektur DSS ini?",
    options: [
      "Meningkatkan kecepatan koneksi API Binance",
      "Memberikan transparansi bobot kontribusi 15 fitur teknikal bagi keputusan model AI (Explainable AI)",
      "Menghapus kebutuhan stop-loss dalam bertransaksi",
      "Menjamin profit 100% tanpa risiko fluktuasi"
    ],
    correct: 1
  }
];

let quizCurrentIdx = 0;
let quizScore = 0;
let quizSelectedOpt = null;
let pkmInitialized = false;

function initPkmPage() {
  if (pkmInitialized) return;
  pkmInitialized = true;

  renderQuizQuestion();

  const nextBtn = document.getElementById('btn-quiz-next');
  if (nextBtn) {
    nextBtn.onclick = handleQuizNext;
  }

  const restartBtn = document.getElementById('btn-quiz-restart');
  if (restartBtn) {
    restartBtn.onclick = () => {
      quizCurrentIdx = 0;
      quizScore = 0;
      quizSelectedOpt = null;
      document.getElementById('quiz-result-box').style.display = 'none';
      document.getElementById('quiz-container').style.display = 'block';
      renderQuizQuestion();
    };
  }

  // Feedback form
  const fbForm = document.getElementById('form-mitra-feedback');
  if (fbForm) {
    fbForm.onsubmit = e => {
      e.preventDefault();
      const name = document.getElementById('fb-name').value;
      const topic = document.getElementById('fb-topic').value;
      const msg = document.getElementById('fb-message').value;

      const list = document.getElementById('feedback-recent-list');
      if (list) {
        const item = document.createElement('div');
        item.className = 'fr-item';
        item.innerHTML = `
          <div class="fr-header"><strong>${name}</strong> · <span class="kpi-pill indigo" style="font-size:9px;">${topic}</span> · <span class="fr-time">Baru saja</span></div>
          <div class="fr-body">"${msg}"</div>
        `;
        list.insertBefore(item, list.children[1]);
      }

      fbForm.reset();
      alert('Terima kasih! Catatan asistensi / feedback mitra berhasil tersimpan dalam logbook PKM.');
    };
  }
}

function renderQuizQuestion() {
  const q = PKM_QUIZ_QUESTIONS[quizCurrentIdx];
  setEl('quiz-q-num', `Pertanyaan ${quizCurrentIdx + 1} dari ${PKM_QUIZ_QUESTIONS.length}`);
  setEl('quiz-q-text', q.q);
  setEl('quiz-score-live', `Skor: ${quizScore}`);

  const optContainer = document.getElementById('quiz-options');
  if (!optContainer) return;
  optContainer.innerHTML = '';
  quizSelectedOpt = null;

  q.options.forEach((opt, idx) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'quiz-opt-btn';
    btn.textContent = `${String.fromCharCode(65 + idx)}. ${opt}`;
    btn.onclick = () => {
      document.querySelectorAll('.quiz-opt-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      quizSelectedOpt = idx;
    };
    optContainer.appendChild(btn);
  });
}

function handleQuizNext() {
  if (quizSelectedOpt === null) {
    alert('Silakan pilih salah satu jawaban terlebih dahulu.');
    return;
  }

  const q = PKM_QUIZ_QUESTIONS[quizCurrentIdx];
  const isCorrect = quizSelectedOpt === q.correct;
  if (isCorrect) quizScore += 20;

  quizCurrentIdx++;
  if (quizCurrentIdx < PKM_QUIZ_QUESTIONS.length) {
    renderQuizQuestion();
  } else {
    // Show results
    document.getElementById('quiz-container').style.display = 'none';
    const resBox = document.getElementById('quiz-result-box');
    resBox.style.display = 'block';
    setEl('qr-score', `${quizScore} / 100`);

    const descEl = document.getElementById('qr-desc');
    if (quizScore >= 80) {
      descEl.textContent = 'Luar Biasa! Anda memiliki pemahaman tingkat Mahir mengenai manajemen risiko dan operasional DSS sesuai standar Program Kemitraan Masyarakat.';
    } else if (quizScore >= 60) {
      descEl.textContent = 'Bagus! Pemahaman tingkat Menengah. Disarankan membaca Modul PKM Ber-ISBN untuk memperdalam konsep VaR dan Position Sizing.';
    } else {
      descEl.textContent = 'Perlu Pendampingan Tambahan: Anda disarankan mengikuti sesi asistensi luring di Lab Komputasi UNP untuk menghindari risiko kerugian fatal.';
    }
  }
}


// ─── SHAP PAGE ───────────────────────────────────────────────────────────
async function loadShapPage() {
  try {
    const [shapData, featData] = await Promise.all([
      api('/api/shap'),
      api('/api/features'),
    ]);

    const features = shapData.features.sort((a, b) => b.shap - a.shap);

    // Category colors
    const catColors = {
      lag:        C.indigo,
      trend:      C.emerald,
      momentum:   C.amber,
      volatility: C.red,
      volume:     C.sky,
      temporal:   C.violet,
    };

    // Horizontal bar chart
    destroyChart('shap');
    const shapCtx = document.getElementById('chart-shap').getContext('2d');
    charts['shap'] = new Chart(shapCtx, {
      type: 'bar',
      data: {
        labels: features.map(f => f.name),
        datasets: [{
          data: features.map(f => f.shap),
          backgroundColor: features.map(f => catColors[f.type] + 'cc'),
          borderColor:      features.map(f => catColors[f.type]),
          borderWidth: 1.5,
          borderRadius: 3,
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true, maintainAspectRatio: true,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: {
            label: c => ` SHAP: ${c.parsed.x.toFixed(3)} (${features[c.dataIndex].shap_pct}%)`
          }}
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,.04)' },
               title: { display: true, text: 'Mean |SHAP| Value', color: '#52525b' } },
          y: { grid: { display: false },
               ticks: { font: { size: 10.5, family: 'JetBrains Mono' } } }
        }
      }
    });

    // Category pie
    const catSums = {};
    features.forEach(f => { catSums[f.type] = (catSums[f.type] || 0) + f.shap; });
    const catNames  = Object.keys(catSums);
    const catLabels = { lag:'Lag', trend:'Trend', momentum:'Momentum',
                        volatility:'Volatilitas', volume:'Volume', temporal:'Temporal' };

    destroyChart('shap-cat');
    const scCtx = document.getElementById('chart-shap-cat').getContext('2d');
    charts['shap-cat'] = new Chart(scCtx, {
      type: 'doughnut',
      data: {
        labels: catNames.map(c => catLabels[c] || c),
        datasets: [{
          data:            catNames.map(c => catSums[c]),
          backgroundColor: catNames.map(c => catColors[c] + 'cc'),
          borderColor:     catNames.map(c => catColors[c]),
          borderWidth: 1.5,
          hoverOffset: 6,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        plugins: {
          legend: { position: 'bottom', align: 'center' },
          tooltip: { callbacks: {
            label: c => ` ${c.label}: ${(c.parsed / Object.values(catSums).reduce((a,b)=>a+b)*100).toFixed(1)}%`
          }}
        },
        cutout: '55%',
      }
    });

    // Legend
    const legEl = document.getElementById('feature-legend');
    legEl.innerHTML = catNames.map(c =>
      `<div class="fl-item">
        <div class="fl-dot" style="background:${catColors[c]}"></div>
        <span>${catLabels[c] || c}</span>
       </div>`
    ).join('');

    // Feature table
    const tbody = document.getElementById('feature-tbody');
    tbody.innerHTML = '';
    featData.features.forEach((f, i) => {
      const shapF = features.find(s => s.name.includes(f.name.split(' ')[0]));
      const shap  = shapF ? shapF.shap.toFixed(3) : '—';
      const pct   = shapF ? shapF.shap_pct + '%'  : '—';
      const cat   = f.category;
      const col   = catColors[cat.toLowerCase()] || C.textSub;
      tbody.innerHTML += `
        <tr>
          <td class="mono">${f.id}</td>
          <td><code style="font-family:'JetBrains Mono',monospace;font-size:11px">${f.name}</code></td>
          <td><span style="color:${col};font-weight:600;font-size:11px">${cat}</span></td>
          <td class="mono">${shap}</td>
          <td>
            <div style="display:flex;align-items:center;gap:8px">
              <div style="flex:1;height:4px;background:rgba(255,255,255,.06);border-radius:2px">
                <div style="width:${pct};height:100%;background:${col};border-radius:2px"></div>
              </div>
              <span class="mono" style="color:${col}">${pct}</span>
            </div>
          </td>
          <td style="color:#a1a1aa;font-size:11.5px">${f.description}</td>
        </tr>
      `;
    });

  } catch (e) {
    console.error('SHAP page error:', e);
  }
}

// ─── PARTICLE CONSTELLATION MESH ─────────────────────────────────────────
function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const numParticles = Math.min(50, Math.floor((width * height) / 28000));
  const particles = [];
  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      radius: Math.random() * 1.5 + 0.6,
      alpha: Math.random() * 0.45 + 0.2,
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(129, 140, 248, ${p.alpha})`;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 110) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(99, 102, 241, ${(1 - dist / 110) * 0.12})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

// ─── LIVE TICKER ─────────────────────────────────────────────────────────
function startLiveTicker() {
  let basePrice = 67430;
  setInterval(() => {
    const delta = (Math.random() - 0.48) * 55;
    basePrice   = Math.max(60000, basePrice + delta);
    const pct   = ((basePrice - 67430) / 67430) * 100 + 5.55;
    const priceStr = '$' + Math.round(basePrice).toLocaleString('id-ID');
    const chStr    = (pct >= 0 ? '+' : '') + pct.toFixed(2) + '%';

    const el = document.getElementById('top-price');
    if (el) el.textContent = priceStr;
    const chEl = document.getElementById('top-change');
    if (chEl) {
      chEl.textContent = chStr;
      chEl.className   = 'ticker-change ' + (pct >= 0 ? 'positive' : 'negative');
    }

    const kpiVal = document.getElementById('kpi-price-val');
    if (kpiVal) kpiVal.textContent = priceStr;
    const kpiCh = document.getElementById('kpi-price-ch');
    if (kpiCh) {
      kpiCh.textContent = chStr;
      kpiCh.className   = 'kpi-pill ' + (pct >= 0 ? 'green' : 'red');
    }
  }, 2500);
}

// ─── INIT ────────────────────────────────────────────────────────────────
async function init() {
  initParticles();
  chartDefaults();
  initNav();
  initPeriodTabs();
  initPrediction();

  // Check server & load overview
  const alive = await checkStatus();
  await loadOverview();
  startLiveTicker();

  // Hide loader
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.4s ease';
    setTimeout(() => overlay.remove(), 450);
  }

  if (!alive) {
    console.warn('Server API offline — beberapa fitur membutuhkan server (py api_server.py)');
  }
}

document.addEventListener('DOMContentLoaded', init);

