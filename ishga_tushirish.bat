@echo off
chcp 65001 >nul
title TasvirLab — Professional AI Veb-Platformasi
echo ========================================================
echo   🎬 TasvirLab — AI Ta'limiy Video Studiyasi (Web)
echo ========================================================
echo.
cd /d "%~dp0"

echo [1/3] Python muhiti tekshirilmoqda...
if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
) else (
    set "PY_CMD=python"
)

echo [2/3] Brauzer ochilmoqda (http://localhost:8000)...
start http://localhost:8000

echo [3/3] Server ishga tushirilmoqda (Port: 8000)...
echo.
echo Dasturni to'xtatish uchun ushbu oynada CTRL+C tugmalarini bosing.
echo ========================================================
echo.
%PY_CMD% -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
