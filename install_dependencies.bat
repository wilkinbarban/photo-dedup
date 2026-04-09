@echo off
title Instalador de Dependencias - PhotoDedup
color 0A

echo ===================================================
echo   Instalando dependencias para PhotoDedup...
echo ===================================================
echo.

REM Verifica si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [INFO] No se encontro Python en el sistema.
    echo Intentando instalar Python automaticamente usando winget...
    
    winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
    
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] No se pudo instalar Python automaticamente.
        echo Por favor, instala Python manualmente desde python.org y asegurate de agregarlo al PATH.
        echo.
        pause
        exit /b
    ) else (
        echo [INFO] Python se ha instalado correctamente. 
        echo IMPORTANTE: Por favor, cierra esta ventana y vuelve a ejecutar install_dependencies.bat
        echo.
        pause
        exit /b
    )
)

echo [INFO] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INFO] Instalando paquetes desde requirements.txt...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo   Instalacion completada con exito!
    echo   Ya puedes abrir photo_dedup.py
    echo ===================================================
) else (
    color 0C
    echo.
    echo ===================================================
    echo   [ERROR] Hubo un problema al instalar.
    echo   Revisa los mensajes de arriba para mas detalles.
    echo ===================================================
)

echo.
pause
