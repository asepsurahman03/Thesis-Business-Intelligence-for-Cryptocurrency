@echo off
chcp 65001 >nul
title CryptoPredict AI Dashboard

echo ======================================================================
echo   CryptoPredict AI — DSS Dashboard Launcher
echo   Capstone Project Magister Informatika Data Science
echo   Universitas Nusa Putra
echo ======================================================================
echo.

REM Cek apakah Python tersedia
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py -3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python tidak ditemukan. Install Python 3.10+ dari python.org
        pause
        exit /b 1
    )
    set PYTHON=py -3
) else (
    set PYTHON=python
)

echo [INFO] Menggunakan Python: %PYTHON%
echo.

REM Cek apakah Flask tersedia
%PYTHON% -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Menginstall dependensi...
    %PYTHON% -m pip install -r requirements.txt --quiet
)

echo [INFO] Menjalankan CryptoPredict AI API Server...
echo [INFO] Dashboard akan otomatis terbuka di browser Anda.
echo [INFO] Tekan Ctrl+C untuk menghentikan server.
echo.
echo ======================================================================

%PYTHON% api_server.py

pause
