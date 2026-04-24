@echo off
title HeadphoneAI - Starting...
color 0A

echo.
echo  ================================================
echo    HeadphoneAI - RAG + MCP + LLM Demo
echo  ================================================
echo.

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo.
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

echo  [1/3] Python found. Checking dependencies...
echo.

:: Install dependencies quietly
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  [ERROR] Failed to install dependencies.
    echo  Try running: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo  [2/3] Dependencies ready.
echo.
echo  [3/3] Starting server...
echo.
echo  ------------------------------------------------
echo   App will open at: http://localhost:8009
echo   Press Ctrl+C in this window to stop.
echo  ------------------------------------------------
echo.

:: Open browser after 3 seconds
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8009"

:: Start FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8009

pause
