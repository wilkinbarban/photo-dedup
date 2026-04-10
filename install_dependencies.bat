@echo off
setlocal enabledelayedexpansion
title Instalador de Dependencias - PhotoDedup
color 0A

echo ===================================================
echo   Instalando dependencias para PhotoDedup...
echo ===================================================
echo.

:CHECK_PYTHON
REM Comprueba si python está disponible en el PATH
python --version >nul 2>&1
if %errorlevel% equ 0 goto PY_OK

color 0E
echo [INFO] No se encontro Python en el sistema.
echo Intentando instalar Python automaticamente usando winget...
echo.

winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    color 0C
echo [ERROR] No se pudo instalar Python automaticamente.
echo Por favor, instala Python manualmente desde https://python.org y asegurate de agregarlo al PATH.
echo.
pause
exit /b
)

echo [INFO] Python se ha instalado (winget reporta exito). Intentando localizar python.exe...
echo.

REM Primero intenta usar where (puede fallar si PATH no se actualizo en esta sesión)
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] python encontrado via where.
    goto PY_OK
)

REM Buscar en rutas comunes de instalacion por usuario y sistema
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
    echo [INFO] python.exe localizado en: "!PY_PATH!\python.exe"
    echo [INFO] Añadiendo carpeta a PATH para la sesion actual...
    set "PATH=!PY_PATH!;!PATH!"
    REM Verifica ahora
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Python disponible en la sesion actual.
        goto PY_OK
    )
)

REM Si llegamos aqui, no podemos detectar python en la sesion actual.
color 0E
echo.
echo [INFO] Python parece instalado pero no esta disponible en esta consola.
echo Para aplicar los cambios en el PATH, cierra esta ventana de terminal, abre uno nuevo y vuelve a ejecutar install_dependencies.bat
echo Si prefieres, puedes añadir manualmente la ruta del python.exe al PATH de usuario y luego reabrir la consola.
echo.
pause
exit /b

:PY_OK
color 0A
echo [INFO] Python detectado:
python --version
echo.

echo [INFO] Actualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    color 0C
echo [ERROR] Fallo al actualizar pip. Revisa la instalacion de Python.
pause
exit /b
)

echo [INFO] Instalando paquetes desde requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    color 0C
echo.
echo ===================================================
echo   [ERROR] Hubo un problema al instalar.
echo   Revisa los mensajes de arriba para mas detalles.
echo ===================================================
echo.
pause
exit /b
)

echo.
echo ===================================================
echo   Instalacion completada con exito!
echo   Ya puedes abrir photo_dedup.py
echo ===================================================
echo.
pause
endlocal
exit /b
