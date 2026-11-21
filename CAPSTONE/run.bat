@echo off
setlocal enabledelayedexpansion
title Bus Pass Automation System - Quick Launcher

echo ======================================================================
echo        BUS PASS AUTOMATION SYSTEM - FAST LAUNCHER (SIMATS)
echo   Saveetha Institute of Medical and Technical Sciences
echo   Team: YOKAVISHWA A, ELAMARAN S, PUNITH KUMAR N
echo   Guide: Mr Jegadeesh K
echo ======================================================================
echo.

:: 1. Detect Python
set "PY_EXEC="
python -c "import sys" >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_EXEC=python"
    goto :FoundPy
)

py -c "import sys" >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_EXEC=py"
    goto :FoundPy
)

if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set "PY_EXEC=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    goto :FoundPy
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PY_EXEC=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :FoundPy
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY_EXEC=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :FoundPy
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_EXEC=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :FoundPy
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PY_EXEC=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    goto :FoundPy
)

:FoundPy
if "%PY_EXEC%"=="" (
    echo [ERROR] Python not found. Please install Python 3.
    pause
    exit /b 1
)

echo [OK] Using Python: %PY_EXEC%
echo.

:: 2. Optional C++ compilation if g++ is present
if not exist "bus_pass_engine.exe" (
    where g++ >nul 2>&1
    if !errorlevel! equ 0 (
        echo [*] Auto-compiling C++ OOP Engine (bus_pass_engine.cpp)...
        g++ -O2 -std=c++17 bus_pass_engine.cpp -o bus_pass_engine.exe
    )
)

echo Select how you want to launch your project:
echo.
echo   [1] Fast Web GUI in Browser (Recommended: 0s wait, no downloads needed)
echo   [2] Streamlit Web App (Requires streamlit)
echo   [3] Console Menu Terminal (Exact match to PPT Slides 6, 8, 10)
echo.

choice /C 123 /T 3 /D 1 /M "Auto-starting Option 1 in 3 seconds (or press 1, 2, 3): "
set "CH=!errorlevel!"

if "!CH!"=="1" goto :LaunchFastWeb
if "!CH!"=="2" goto :LaunchStreamlit
if "!CH!"=="3" goto :LaunchConsole

:LaunchFastWeb
echo.
echo [*] Launching Instant Web GUI on Localhost with alternate port handling...
"%PY_EXEC%" server.py
goto :End

:LaunchStreamlit
echo.
echo [*] Checking Streamlit installation...
"%PY_EXEC%" -c "import streamlit" >nul 2>&1
if !errorlevel! neq 0 (
    echo [*] Installing streamlit...
    "%PY_EXEC%" -m pip install streamlit pandas -q
)
echo [*] Detecting alternate port if 8501 is busy...
set "APP_PORT=8501"
for /L %%P in (8501,1,8520) do (
    netstat -ano | findstr /R /C:":%%P .*LISTENING" >nul 2>&1
    if !errorlevel! neq 0 (
        set "APP_PORT=%%P"
        goto :StartSt
    )
)
:StartSt
echo [OK] Launching Streamlit on http://localhost:!APP_PORT!
"%PY_EXEC%" -m streamlit run app.py --server.port !APP_PORT! --server.headless false
goto :End

:LaunchConsole
echo.
echo [*] Launching Console Menu Program...
"%PY_EXEC%" bus_pass.py
goto :End

:End
pause
