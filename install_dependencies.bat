@echo offsetlocal enabledelayedexpansiontitle Instalador de Dependencias - PhotoDedupcolor 0A

echo ===================================================echo   Instalando dependencias para PhotoDedup…echo ===================================================echo.

:CHECK_PYTHONREM Comprueba si python está disponible en el PATHpython –version >nul 2>&1if %errorlevel% equ 0 goto PY_OK

color 0Eecho [INFO] No se encontro Python en el sistema.echo Intentando instalar Python automaticamente usando winget…echo.

winget install –id Python.Python.3.11 -e –source winget –accept-package-agreements –accept-source-agreementsif %errorlevel% neq 0 (color 0Cecho [ERROR] No se pudo instalar Python automaticamente.echo Por favor, instala Python manualmente desde https://python.org y asegurate de agregarlo al PATH.echo.pauseexit /b)

echo [INFO] Python se ha instalado (winget reporta exito). Intentando localizar python.exe…echo.

REM Primero intenta usar where (puede fallar si PATH no se actualizo en esta sesión)where python >nul 2>&1if %errorlevel% equ 0 (echo [INFO] python encontrado via where.goto PY_OK)

REM Buscar en rutas comunes de instalacion por usuario y sistemaset “PY_PATH=”for %%D in (”%LOCALAPPDATA%\Programs\Python*” “%ProgramFiles%\Python*” “%ProgramFiles(x86)%\Python*”) do (for /d %%P in (%%~D) do (if exist “%%P\python.exe” (set “PY_PATH=%%P”goto :FOUND_PY_PATH))):FOUND_PY_PATHif defined PY_PATH (echo [INFO] python.exe localizado en: “!PY_PATH!\python.exe”echo [INFO] Añadiendo carpeta a PATH para la sesion actual…set “PATH=!PY_PATH!;!PATH!”REM Verifica ahorapython –version >nul 2>&1if %errorlevel% equ 0 (echo [INFO] Python disponible en la sesion actual.goto PY_OK))

REM Si llegamos aqui, no podemos detectar python en la sesion actual.color 0Eecho.echo [INFO] Python parece instalado pero no esta disponible en esta consola.echo Para aplicar los cambios en el PATH, cierra esta ventana de terminal, abre uno nuevo y vuelve a ejecutar install_dependencies.batecho Si prefieres, puedes añadir manualmente la ruta del python.exe al PATH de usuario y luego reabrir la consola.echo.pauseexit /b

:PY_OKcolor 0Aecho [INFO] Python detectado:python –versionecho.

echo [INFO] Actualizando pip…python -m pip install –upgrade pipif %errorlevel% neq 0 (color 0Cecho [ERROR] Fallo al actualizar pip. Revisa la instalacion de Python.pauseexit /b)

echo [INFO] Instalando paquetes desde requirements.txt…pip install -r requirements.txtif %errorlevel% neq 0 (color 0Cecho.echo ===================================================echo   [ERROR] Hubo un problema al instalar.echo   Revisa los mensajes de arriba para mas detalles.echo ===================================================echo.pauseexit /b)

echo.echo ===================================================echo   Instalacion completada con exito!echo   Ya puedes abrir photo_dedup.pyecho ===================================================echo.pauseendlocalexit /b