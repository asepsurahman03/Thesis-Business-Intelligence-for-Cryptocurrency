#!/usr/bin/env python3
"""
Environment Setup Script for Bitcoin Analysis Notebook
Fixes TensorFlow compatibility issues for Python 3.13
"""

import sys
import subprocess
import os

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13+ detected. TensorFlow compatibility issues may occur.")
        return True
    return False

def install_tensorflow_compatible():
    """Install TensorFlow version compatible with current Python version"""
    print("🔧 Installing compatible TensorFlow version...")
    
    try:
        # Try TensorFlow 2.15.0 (last version with better Python 3.13 support)
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "tensorflow==2.15.0", 
            "--upgrade", 
            "--no-cache-dir"
        ])
        print("✅ TensorFlow 2.15.0 installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ TensorFlow installation failed. Trying CPU-only version...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "tensorflow-cpu==2.15.0", 
                "--upgrade", 
                "--no-cache-dir"
            ])
            print("✅ TensorFlow CPU 2.15.0 installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ TensorFlow CPU installation also failed.")
            return False

def verify_installation():
    """Verify TensorFlow installation"""
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow imported successfully! Version: {tf.__version__}")
        
        # Test basic functionality
        hello = tf.constant('Hello, TensorFlow!')
        print(f"✅ TensorFlow basic test passed: {hello.numpy().decode()}")
        return True
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Starting Bitcoin Analysis Environment Setup")
    print("=" * 50)
    
    # Check Python version
    is_new_python = check_python_version()
    
    # Install compatible TensorFlow
    if is_new_python:
        success = install_tensorflow_compatible()
    else:
        print("✅ Python version should be compatible with standard TensorFlow")
        success = True
    
    # Verify installation
    if success:
        verify_installation()
    
    print("\n" + "=" * 50)
    print("🎯 Setup completed!")
    print("💡 You can now run the Jupyter notebook:")
    print("   jupyter notebook 02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb")

if __name__ == "__main__":
    main()
