"""
Script untuk MENGGANTI TensorFlow dengan PyTorch di notebook.
Python 3.13 TIDAK kompatibel dengan TensorFlow — PyTorch mendukung Python 3.13.

Jalankan: python fix_tensorflow_to_pytorch.py
"""

import json
import os

NOTEBOOK_PATH = "Bitcoin_BigData_Analysis_MasterClass.ipynb"


# ============================================================
# SOURCE CODE BARU — PYTORCH MENGGANTIKAN TENSORFLOW
# ============================================================

NEW_IMPORT_SOURCE = [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.gridspec as gridspec\n",
    "import time\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "from sklearn.preprocessing import MinMaxScaler\n",
    "from sklearn.metrics import mean_squared_error, mean_absolute_error\n",
    "\n",
    "# ============================================================\n",
    "# PyTorch — kompatibel dengan Python 3.13\n",
    "# (TensorFlow hanya support Python 3.9-3.12)\n",
    "# ============================================================\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.optim as optim\n",
    "from torch.utils.data import DataLoader, TensorDataset\n",
    "\n",
    "# Set device (GPU jika tersedia, CPU sebagai fallback)\n",
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "print(f'PyTorch version : {torch.__version__}')\n",
    "print(f'Device          : {device}')\n",
    "print(f'Python version  : {__import__(\"sys\").version}')\n",
    "print('\\n✅ Semua library berhasil di-import!')\n",
]

# Model LSTM & GRU menggunakan PyTorch
NEW_MODEL_SOURCE = [
    "# ============================================================\n",
    "# Business Intelligence — Deep Learning Model (PyTorch)\n",
    "# LSTM vs GRU — Comparative Study\n",
    "# ============================================================\n",
    "\n",
    "# --- Definisi Model PyTorch ---\n",
    "class LSTMModel(nn.Module):\n",
    "    \"\"\"LSTM Model untuk prediksi harga Bitcoin\"\"\"\n",
    "    def __init__(self, input_size, hidden_size=50, num_layers=2, dropout=0.2):\n",
    "        super(LSTMModel, self).__init__()\n",
    "        self.hidden_size = hidden_size\n",
    "        self.num_layers = num_layers\n",
    "        self.lstm = nn.LSTM(\n",
    "            input_size, hidden_size,\n",
    "            num_layers=num_layers,\n",
    "            dropout=dropout,\n",
    "            batch_first=True\n",
    "        )\n",
    "        self.fc = nn.Linear(hidden_size, 1)\n",
    "\n",
    "    def forward(self, x):\n",
    "        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)\n",
    "        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)\n",
    "        out, _ = self.lstm(x, (h0, c0))\n",
    "        out = self.fc(out[:, -1, :])\n",
    "        return out\n",
    "\n",
    "\n",
    "class GRUModel(nn.Module):\n",
    "    \"\"\"GRU Model untuk prediksi harga Bitcoin\"\"\"\n",
    "    def __init__(self, input_size, hidden_size=50, num_layers=2, dropout=0.2):\n",
    "        super(GRUModel, self).__init__()\n",
    "        self.hidden_size = hidden_size\n",
    "        self.num_layers = num_layers\n",
    "        self.gru = nn.GRU(\n",
    "            input_size, hidden_size,\n",
    "            num_layers=num_layers,\n",
    "            dropout=dropout,\n",
    "            batch_first=True\n",
    "        )\n",
    "        self.fc = nn.Linear(hidden_size, 1)\n",
    "\n",
    "    def forward(self, x):\n",
    "        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)\n",
    "        out, _ = self.gru(x, h0)\n",
    "        out = self.fc(out[:, -1, :])\n",
    "        return out\n",
    "\n",
    "\n",
    "# --- Training Function ---\n",
    "def train_model(model, X_train, y_train, epochs=10, batch_size=64, lr=0.001):\n",
    "    \"\"\"\n",
    "    Training loop untuk LSTM/GRU model.\n",
    "    Returns: history dict dengan training loss per epoch.\n",
    "    \"\"\"\n",
    "    model = model.to(device)\n",
    "    criterion = nn.MSELoss()\n",
    "    optimizer = optim.Adam(model.parameters(), lr=lr)\n",
    "\n",
    "    # Convert numpy arrays ke PyTorch tensors\n",
    "    X_t = torch.FloatTensor(X_train).to(device)\n",
    "    y_t = torch.FloatTensor(y_train).reshape(-1, 1).to(device)\n",
    "\n",
    "    dataset = TensorDataset(X_t, y_t)\n",
    "    loader  = DataLoader(dataset, batch_size=batch_size, shuffle=False)\n",
    "\n",
    "    history = {'loss': []}\n",
    "\n",
    "    model.train()\n",
    "    for epoch in range(epochs):\n",
    "        epoch_loss = 0.0\n",
    "        for X_batch, y_batch in loader:\n",
    "            optimizer.zero_grad()\n",
    "            output = model(X_batch)\n",
    "            loss = criterion(output, y_batch)\n",
    "            loss.backward()\n",
    "            optimizer.step()\n",
    "            epoch_loss += loss.item() * len(X_batch)\n",
    "\n",
    "        avg_loss = epoch_loss / len(X_train)\n",
    "        history['loss'].append(avg_loss)\n",
    "        print(f'  Epoch [{epoch+1:2d}/{epochs}]  Loss: {avg_loss:.6f}')\n",
    "\n",
    "    return history\n",
    "\n",
    "\n",
    "# --- Predict Function ---\n",
    "def predict_model(model, X_test):\n",
    "    \"\"\"Prediksi menggunakan model yang sudah di-training.\"\"\"\n",
    "    model.eval()\n",
    "    with torch.no_grad():\n",
    "        X_t = torch.FloatTensor(X_test).to(device)\n",
    "        preds = model(X_t).cpu().numpy()\n",
    "    return preds\n",
    "\n",
    "\n",
    "# --- MAPE Function ---\n",
    "def mean_absolute_percentage_error(y_true, y_pred):\n",
    "    y_true = np.array(y_true)\n",
    "    y_pred = np.array(y_pred)\n",
    "    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100\n",
    "\n",
    "\n",
    "# --- Training & Evaluation Loop ---\n",
    "results = []\n",
    "\n",
    "models_to_train = {\n",
    "    'LSTM': LSTMModel(input_size=X_train.shape[2]),\n",
    "    'GRU' : GRUModel(input_size=X_train.shape[2]),\n",
    "}\n",
    "\n",
    "trained_models = {}\n",
    "\n",
    "for m_type, model in models_to_train.items():\n",
    "    print(f'\\n{'='*50}')\n",
    "    print(f'  Training Model: {m_type} (PyTorch)')\n",
    "    print(f'{'='*50}')\n",
    "\n",
    "    start = time.time()\n",
    "    history = train_model(model, X_train, y_train, epochs=10, batch_size=64)\n",
    "    dur = time.time() - start\n",
    "\n",
    "    # Evaluasi\n",
    "    preds = predict_model(model, X_test)\n",
    "    rmse  = np.sqrt(mean_squared_error(y_test, preds))\n",
    "    mae   = mean_absolute_error(y_test, preds)\n",
    "    mape  = mean_absolute_percentage_error(y_test, preds.flatten())\n",
    "\n",
    "    results.append({\n",
    "        'Model'    : m_type,\n",
    "        'RMSE'     : rmse,\n",
    "        'MAE'      : mae,\n",
    "        'MAPE (%)'  : mape,\n",
    "        'Waktu (s)': dur,\n",
    "        'Predictions': preds,\n",
    "        'History'   : history,\n",
    "        'ModelObj'  : model,\n",
    "    })\n",
    "\n",
    "    trained_models[m_type] = model\n",
    "    print(f'\\n  ✅ {m_type} selesai | RMSE: {rmse:.4f} | MAPE: {mape:.2f}% | Waktu: {dur:.1f}s')\n",
    "\n",
    "# Tampilkan hasil perbandingan\n",
    "results_df = pd.DataFrame(results).drop(['Predictions', 'History', 'ModelObj'], axis=1)\n",
    "print('\\n' + '='*60)\n",
    "print('  COMPARISON RESULTS — LSTM vs GRU (PyTorch)')\n",
    "print('='*60)\n",
    "print(results_df.to_string(index=False))\n",
]


def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_notebook(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"✅ Notebook disimpan: {path}")


def find_cell_by_content(cells, keywords, cell_type='code'):
    """Temukan index cell berdasarkan kata kunci dalam source."""
    for i, cell in enumerate(cells):
        if cell['cell_type'] != cell_type:
            continue
        source = ''.join(cell.get('source', []))
        if all(kw in source for kw in keywords):
            return i
    return -1


def fix_imports_cell(nb):
    """Ganti cell import TensorFlow dengan PyTorch."""
    idx = find_cell_by_content(
        nb['cells'],
        ['tensorflow', 'Sequential'],  # cari cell dengan keyword ini
        cell_type='code'
    )
    if idx == -1:
        idx = find_cell_by_content(
            nb['cells'],
            ['import tensorflow'],
            cell_type='code'
        )
    if idx == -1:
        # Coba cari cell dengan 'from tensorflow'
        idx = find_cell_by_content(
            nb['cells'],
            ['from tensorflow'],
            cell_type='code'
        )

    if idx >= 0:
        nb['cells'][idx]['source'] = NEW_IMPORT_SOURCE
        nb['cells'][idx].pop('outputs', None)
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Import cell (index {idx}) diperbarui: TensorFlow → PyTorch")
    else:
        print("⚠️  Import cell tidak ditemukan, skip.")
    return nb


def fix_model_training_cell(nb):
    """Ganti cell training TensorFlow dengan implementasi PyTorch."""
    # Cari cell dengan build_model atau model.fit (TensorFlow style)
    keywords_list = [
        ['build_model', 'LSTM'],
        ['def build_model', 'Sequential'],
        ['model.fit', 'X_train'],
        ['model = Sequential'],
    ]

    idx = -1
    for keywords in keywords_list:
        idx = find_cell_by_content(nb['cells'], keywords, cell_type='code')
        if idx >= 0:
            break

    if idx >= 0:
        nb['cells'][idx]['source'] = NEW_MODEL_SOURCE
        nb['cells'][idx].pop('outputs', None)
        nb['cells'][idx]['outputs'] = []
        nb['cells'][idx]['execution_count'] = None
        print(f"✅ Model training cell (index {idx}) diperbarui: TF → PyTorch")
    else:
        print("⚠️  Model training cell tidak ditemukan.")
    return nb


def fix_notebook():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"❌ File tidak ditemukan: {NOTEBOOK_PATH}")
        return

    print(f"📂 Membaca notebook: {NOTEBOOK_PATH}")
    nb = load_notebook(NOTEBOOK_PATH)

    # Backup
    backup = NOTEBOOK_PATH.replace('.ipynb', '_tf_backup.ipynb')
    save_notebook(nb, backup)
    print(f"💾 Backup: {backup}")

    # Fix imports
    nb = fix_imports_cell(nb)

    # Fix model training
    nb = fix_model_training_cell(nb)

    # Simpan
    save_notebook(nb, NOTEBOOK_PATH)

    print("\n🎉 Notebook berhasil diperbarui!")
    print("\nRingkasan Perubahan:")
    print("  • TensorFlow → PyTorch (kompatibel Python 3.13)")
    print("  • Sequential/LSTM/GRU (Keras) → nn.LSTM/nn.GRU (PyTorch)")
    print("  • model.fit() → custom training loop")
    print("  • model.predict() → inference dengan torch.no_grad()")
    print("\nPastikan PyTorch sudah terinstall:")
    print("  pip install torch")


if __name__ == "__main__":
    fix_notebook()
