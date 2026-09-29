@echo off
chcp 65001 >nul 2>&1
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     QwenPaw Local Services - Starting...        ║
echo ╚══════════════════════════════════════════════════╝
echo.

REM --- Check Ollama ---
echo [1/5] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo   ! Ollama not running. Starting...
    start /B ollama serve
    timeout /t 3 /nobreak >nul
    ollama list >nul 2>&1
    if %errorlevel% neq 0 (
        echo   ERROR: Cannot start Ollama. Start manually with: ollama serve
        pause
        exit /b 1
    )
)
echo   OK - Ollama running
echo.

REM --- Check Docker ---
echo [2/5] Checking Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo   ! Docker not available - using direct Python mode
    set USE_DOCKER=0
) else (
    echo   OK - Docker available
    set USE_DOCKER=1
)
echo.

REM --- Start Bridge ---
echo [3/5] Starting Bridge...
cd /d C:\Users\%USERNAME%\qwenpaw-bridge
if "%USE_DOCKER%"=="1" (
    docker compose up -d
    if %errorlevel% neq 0 (
        echo   ! Docker failed, falling back to Python...
        start /B python bridge.py
    ) else (
        echo   OK - Bridge container started
    )
) else (
    start /B python bridge.py
    echo   OK - Bridge started (Python direct)
)
echo   URL: http://localhost:5000
echo.

REM --- Start Healthcheck ---
echo [4/5] Starting Healthcheck...
cd /d C:\Users\%USERNAME%\qwenpaw-orchestrator
if "%USE_DOCKER%"=="1" (
    docker compose up -d
    if %errorlevel% neq 0 (
        echo   ! Docker failed, falling back to Python...
        start /B python healthcheck.py
    ) else (
        echo   OK - Healthcheck container started
    )
) else (
    start /B python healthcheck.py
    echo   OK - Healthcheck started (Python direct)
)
echo.

REM --- Start ngrok ---
echo [5/5] Starting ngrok tunnel...
cd /d C:\Users\%USERNAME%\qwenpaw-bridge
start "ngrok" ngrok.exe http 5000
echo   OK - ngrok starting (check window for public URL)
echo.

REM --- Wait and show status ---
timeout /t 5 /nobreak >nul

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     QwenPaw Local Services - RUNNING            ║
echo ╠══════════════════════════════════════════════════╣
echo ║  Bridge:      http://localhost:5000              ║
echo ║  Ollama:      http://localhost:11434             ║
echo ║  Healthcheck: Running                           ║
echo ║  ngrok:       Check ngrok window for URL        ║
echo ╚══════════════════════════════════════════════════╝
echo.

REM --- Test bridge ---
echo Testing bridge...
curl -s http://localhost:5000/health 2>nul
echo.
echo.

echo Press any key to stop all services...
pause

echo.
echo Stopping all services...

echo [1/3] Stopping containers...
cd /d C:\Users\%USERNAME%\qwenpaw-bridge
docker compose down 2>nul
cd /d C:\Users\%USERNAME%\qwenpaw-orchestrator
docker compose down 2>nul

echo [2/3] Stopping ngrok...
taskkill /F /IM ngrok.exe 2>nul

echo [3/3] Stopping Python processes...
taskkill /F /FI "WINDOWTITLE eq QwenPaw*" 2>nul

echo.
echo All services stopped.
pause
