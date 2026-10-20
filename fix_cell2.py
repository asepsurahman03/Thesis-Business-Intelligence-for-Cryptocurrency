import json

NB_PATH = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell2 = nb['cells'][2]

# Bangun source yang benar sebagai list of strings (format notebook)
correct_source = [
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
    "install_if_missing('seaborn', pip_name='seaborn')\n",
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
    "import seaborn as sns\n",
    "import time\n",
    "import warnings\n",
    "import os\n",
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
    "print('Semua library berhasil di-import!')\n"
]

nb['cells'][2]['source'] = correct_source
nb['cells'][2]['outputs'] = []
nb['cells'][2]['execution_count'] = None

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cell 2 berhasil diperbaiki!")

# Verifikasi syntax
import ast
src_text = ''.join(correct_source)
try:
    ast.parse(src_text)
    print("Syntax check: OK - tidak ada error!")
except SyntaxError as e:
    print(f"Syntax check: MASIH ADA ERROR di baris {e.lineno}: {e.msg}")
    print(f"  Text: {repr(e.text)}")
