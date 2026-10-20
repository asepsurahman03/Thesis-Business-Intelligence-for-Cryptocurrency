import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

nb_path = r'02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

print(f"Reading notebook: {nb_path}")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

print("Executing notebook... This may take a few minutes (training PyTorch models on 5-year data).")
try:
    ep.preprocess(nb, {'metadata': {'path': r'02_Notebooks'}})
    print("Execution successful!")
except Exception as e:
    print(f"Error executing notebook: {e}")
    import traceback
    traceback.print_exc()

# Save notebook with new outputs regardless of error
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook saved.")
