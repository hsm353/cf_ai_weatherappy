@echo off
echo ========================================
echo Weather Chat Assistant - Local Server
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
pip show Flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting server...
echo.
echo Visit: http://localhost:8787
echo Press Ctrl+C to stop the server
echo.

python app.py
