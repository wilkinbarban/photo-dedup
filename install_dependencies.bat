@echo off
setlocal enabledelayedexpansion
title Dependency Installer - PhotoDedup
color 0A

echo ===================================================
echo   Installing dependencies for PhotoDedup...
echo ===================================================
echo.

:CHECK_PYTHON
REM Check if python is available in PATH
python --version >nul 2>&1
if %errorlevel% equ 0 goto PY_OK

color 0E
echo [INFO] Python was not found on this system.
echo Trying to install Python automatically using winget...
echo.

winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python could not be installed automatically.
    echo Please install Python manually from https://python.org and make sure it is added to PATH.
    echo.
    pause
    exit /b
)

echo [INFO] Python installed (winget reported success). Trying to locate python.exe...
echo.

REM First try using where (may fail if PATH was not updated in this session)
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] python found via where.
    goto PY_OK
)

REM Search in common installation paths (per-user and system)
set "PY_PATH="
for %%D in ("%LOCALAPPDATA%\Programs\Python\*" "%ProgramFiles%\Python*" "%ProgramFiles(x86)%\Python*") do (
    for /d %%P in (%%~D) do (
        if exist "%%P\python.exe" (
            set "PY_PATH=%%P"
            goto :FOUND_PY_PATH
        )
    )
)
:FOUND_PY_PATH
if defined PY_PATH (
    echo [INFO] python.exe found at: "!PY_PATH!\python.exe"
    echo [INFO] Adding folder to PATH for the current session...
    set "PATH=!PY_PATH!;!PATH!"
    REM Verify now
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Python is available in the current session.
        goto PY_OK
    )
)

REM If we get here, Python cannot be detected in the current session.
color 0E
echo.
echo [INFO] Python appears to be installed but is not available in this console.
echo To apply PATH changes, close this terminal window, open a new one and run install_dependencies.bat again.
echo If you prefer, add the python.exe path manually to your user PATH and reopen the console.
echo.
pause
exit /b

:PY_OK
color 0A
echo [INFO] Python detected:
python --version
echo.

echo [INFO] Updating pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Failed to update pip. Check your Python installation.
    pause
    exit /b
)

echo [INFO] Installing packages from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ===================================================
    echo   [ERROR] There was a problem during installation.
    echo   Check the messages above for more details.
    echo ===================================================
    echo.
    pause
    exit /b
)

echo.
echo ===================================================
echo   Installation completed successfully!
echo   Launching photo_dedup.py...
echo ===================================================

start "" python photo_dedup.py

if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] The program could not be launched automatically.
    echo Please run: python photo_dedup.py
)

echo.
pause
endlocal
exit /b
