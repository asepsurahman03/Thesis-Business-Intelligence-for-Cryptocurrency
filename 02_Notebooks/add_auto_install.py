"""
Script untuk menambahkan auto-install torch di cell import notebook.
Jalankan: python add_auto_install.py
"""

import json
import os

NOTEBOOK_PATH = "Bitcoin_BigData_Analysis_MasterClass.ipynb"

# Source baru dengan auto-install
NEW_IMPORT_SOURCE = [
    "import sys\n",
    "import subprocess\n",
    "import importlib\n",
    "\n",
    "# ============================================================\n",
    "# Auto-install PyTorch jika belum tersedia di kernel ini\n",
    "# ============================================================\n",
    "def install_if_missing(package, pip_name=None, index_url=None):\n",
    "    pip_name = pip_name or package\n",
    "    try:\n",
    "        importlib.import_module(package)\n",
    "        print(f'  {package}: sudah tersedia')\n",
    "    except ImportError:\n",
    "        print(f'  {package}: menginstall...')\n",
    "        cmd = [sys.executable, '-m', 'pip', 'install', pip_name, '-q']\n",
    "        if index_url:\n",
    "            cmd += ['--index-url', index_url]\n",
    "        subprocess.check_call(cmd)\n",
    "        print(f'  {package}: berhasil diinstall!')\n",
    "\n",
    "print('Memeriksa dependencies...')\n",
    "install_if_missing('torch', pip_name='torch', index_url='https://download.pytorch.org/whl/cpu')\n",
    "print('Semua dependencies siap!')\n",
    "print()\n",
    "\n",
    "# ============================================================\n",
    "# Import library utama\n",
    "# ============================================================\n",
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
    "# PyTorch - kompatibel dengan Python 3.13\n",
    "# (TensorFlow hanya support Python 3.9-3.12)\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.optim as optim\n",
    "from torch.utils.data import DataLoader, TensorDataset\n",
    "\n",
    "# Set device (GPU jika tersedia, CPU sebagai fallback)\n",
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "print(f'PyTorch version : {torch.__version__}')\n",
    "print(f'Device          : {device}')\n",
    "print(f'Python version  : {sys.version.split()[0]}')\n",
    "print('\\nSemua library berhasil di-import!')\n",
]


def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_notebook(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Notebook disimpan: {path}")


def update_import_cell(nb):
    """Update cell import dengan auto-install torch."""
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell.get('source', []))

        # Cari cell yang berisi import torch atau import pandas
        if ('import torch' in source or
                ('import pandas' in source and 'import numpy' in source)):
            nb['cells'][i]['source'] = NEW_IMPORT_SOURCE
            nb['cells'][i]['outputs'] = []
            nb['cells'][i]['execution_count'] = None
            print(f"Cell import (index {i}) berhasil diperbarui dengan auto-install torch!")
            return nb

    print("Cell import tidak ditemukan. Menambahkan di posisi awal...")
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": NEW_IMPORT_SOURCE,
        "outputs": []
    }
    # Insert setelah cell markdown pertama (header)
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            nb['cells'].insert(i + 1, new_cell)
            print(f"Cell import ditambahkan di posisi {i+1}")
            return nb

    nb['cells'].insert(0, new_cell)
    return nb


def main():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"File tidak ditemukan: {NOTEBOOK_PATH}")
        return

    print(f"Membaca notebook: {NOTEBOOK_PATH}")
    nb = load_notebook(NOTEBOOK_PATH)
    print(f"Jumlah cells: {len(nb['cells'])}")

    nb = update_import_cell(nb)

    save_notebook(nb, NOTEBOOK_PATH)
    print("\nNotebook berhasil diperbarui!")
    print("\nPerubahan:")
    print("  - Auto-install torch jika belum tersedia di kernel")
    print("  - Import lengkap: pandas, numpy, sklearn, torch")
    print("  - Deteksi GPU/CPU otomatis")
    print("\nCara pakai:")
    print("  1. Buka notebook di Jupyter")
    print("  2. Jalankan Cell 1 (Import) - torch akan otomatis terinstall jika perlu")
    print("  3. Lanjutkan menjalankan cell berikutnya")


if __name__ == "__main__":
    main()
