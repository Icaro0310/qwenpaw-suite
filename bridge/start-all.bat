@echo off
setlocal
cd /d "%~dp0"

if not defined BRIDGE_HOST set "BRIDGE_HOST=127.0.0.1"
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
if errorlevel 1 exit /b 1

.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Starting the local bridge on %BRIDGE_HOST%:5000. Press Ctrl+C to stop.
echo Remote binding requires BRIDGE_API_KEY; CORS is disabled unless configured.
.venv\Scripts\python.exe bridge.py
