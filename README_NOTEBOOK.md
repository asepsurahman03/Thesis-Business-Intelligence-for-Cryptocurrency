# Bitcoin Big Data Analysis Notebook

## Overview
This notebook implements a comprehensive Bitcoin price prediction analysis using machine learning approaches. It's designed to work with Python 3.13+ and handles TensorFlow compatibility issues gracefully.

## Features
- **Big Data Processing**: Handles 5-year hourly Bitcoin datasets (~43,800+ records)
- **Feature Engineering**: Technical indicators (RSI, MACD, Bollinger Bands, Volatility)
- **Multiple ML Backends**: 
  - TensorFlow (if available)
  - PyTorch (if available) 
  - Scikit-learn (fallback - always works)
- **Model Comparison**: LSTM vs GRU alternatives with performance metrics
- **Academic Visualization**: Times New Roman formatting for research papers

## Quick Start

### 1. Setup Environment
```bash
# Install required packages
pip install -r requirements.txt

# Or install core packages manually
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### 2. Run the Notebook
```bash
# Start Jupyter
jupyter notebook

# Navigate to and open:
# 02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb
```

## Model Backends

### Primary: Scikit-learn (Always Works)
The notebook automatically falls back to scikit-learn models if deep learning frameworks aren't available:
- **LSTM Alternative**: RandomForestRegressor (200 estimators)
- **GRU Alternative**: GradientBoostingRegressor (150 estimators)

### Optional: Deep Learning Frameworks
If you want to use actual LSTM/GRU networks:

#### TensorFlow Installation
```bash
# For Python < 3.13
pip install tensorflow>=2.15.0

# For Python 3.13+ (may have compatibility issues)
pip install tensorflow-cpu>=2.15.0
```

#### PyTorch Installation
```bash
# CPU version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU version (if you have CUDA)
pip install torch torchvision torchaudio
```

## File Structure
```
├── 01_Data/                    # Bitcoin datasets
├── 02_Notebooks/              # Analysis notebook
├── 03_Models/                 # Saved models (.joblib, .keras, .pth)
├── 04_Visualizations/         # Generated plots
├── 05_Reports/               # Results and comparisons
└── requirements.txt          # Dependencies
```

## Troubleshooting

### TensorFlow Import Errors
If you encounter `ModuleNotFoundError: No module named 'tensorflow.python'`:
1. The notebook will automatically fall back to scikit-learn models
2. Or install a compatible TensorFlow version for your Python version
3. Consider using PyTorch as an alternative

### Virtual Environment Issues
If packages aren't found:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install packages in the environment
pip install -r requirements.txt
```

## Model Outputs
- **Performance Metrics**: RMSE, MAE, MAPE
- **Training Time**: Comparison of computational efficiency
- **Visualization**: Price predictions vs actual values
- **Residual Analysis**: Error distribution analysis

## Academic Features
- Times New Roman font formatting
- Mathematical equations for technical indicators
- Big Data 5V principles implementation
- Business Intelligence perspective integration

## Research Applications
This notebook supports:
- **Thesis Research**: Academic-grade analysis and visualization
- **Investment Analysis**: Data-driven decision support
- **Algorithm Trading**: Model-based prediction systems
- **Big Data Studies**: Volume, Velocity, Variety, Veracity, Value analysis

## Citation
If you use this notebook in your research, please cite it appropriately in your academic work.

---
**Note**: The notebook is designed to be robust and will work even without deep learning frameworks, making it suitable for various Python environments and research scenarios.
