# PhotoDedup v1.1.0

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.1.0
Release date: 2026-05-24

### Highlights
### Changed
- Runtime policy now targets Python `3.14.x`, matching the installed local Python used for development and validation from this version onward.
- Dependency bounds in `requirements.txt`, build-only dependencies in `requirements-build.txt`, Windows installers, build scripts, and GitHub Actions were updated for the Python 3.14 runtime line.
- Unified the previous `install.ps1` + `install_secure.ps1` flow into a single `install.ps1` that works as both remote bootstrapper and local installer/launcher.
- Standardized the local cloned-repository launcher as `Iniciar.bat`, replacing both the earlier `Install.bat` naming and the dependency-only `install_dependencies.bat` path.
- Removed the external funding UI behavior and related assets from the desktop interface.
- Redesigned the PyQt6 interface with a stronger shared visual system: refreshed palette, reusable theme helpers, updated welcome/progress/results screens, and cleaner duplicate review cards.
- Reworked README structure for clearer ES/EN/PT onboarding, executable edition guidance, local validation, and error behavior documentation.

### Fixed
- Added support for Google Takeout `*.supplemental-metadata.json` sidecar files so JSON metadata is detected, EXIF enrichment runs, and photo/JSON organization is triggered for the common Takeout naming pattern.
- Skipped direct EXIF writes for HEIC/HEIF files, avoiding noisy `piexif` errors while still using Takeout JSON metadata for date-based organization.
- Expanded Google Takeout sidecar matching for truncated `.suppl*` names, numbered metadata files, `*.jpg..json` files, Live Photo videos that share HEIC sidecar metadata, and orphan Takeout JSON files.
- Fixed partial Google Takeout re-runs so truncated JSON names already moved into `Json` are still matched, numbered Live Photo videos are organized, JSON sidecars already in `Json` are not renamed again, and media without matching JSON no longer remains in the root folder.
- Improved recoverable error handling for cache/config/history loading, analysis failures, QR fallback, per-file move/delete/export failures, and empty-folder scans.
- Replaced several mojibake-prone UI labels with clean synchronized ES/EN/PT text overrides.

### One-command install (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

### Windows SmartScreen notice
Current executables are not code-signed. Windows may show an unknown publisher warning. If you trust the official GitHub Releases source, open `More info` and then `Run anyway`.

### Local install
1. Download the Source Code (`zip` or `tar.gz`) below.
2. Extract the files and open a terminal in the folder.
3. Run `Iniciar.bat` on Windows, or use Python `3.14.x` and install dependencies manually with `pip install -r requirements.txt`.
4. Manual run command: `python src/main/photo_dedup.py`.

---

## Portugues (Brasil)

### O que ha de novo na v1.1.0
Data do release: 2026-05-24

### Destaques
### Alterado
- Runtime policy now targets Python `3.14.x`, matching the installed local Python used for development and validation from this version onward.
- Dependency bounds in `requirements.txt`, build-only dependencies in `requirements-build.txt`, Windows installers, build scripts, and GitHub Actions were updated for the Python 3.14 runtime line.
- Unified the previous `install.ps1` + `install_secure.ps1` flow into a single `install.ps1` that works as both remote bootstrapper and local installer/launcher.
- Standardized the local cloned-repository launcher as `Iniciar.bat`, replacing both the earlier `Install.bat` naming and the dependency-only `install_dependencies.bat` path.
- Removed the external funding UI behavior and related assets from the desktop interface.
- Redesigned the PyQt6 interface with a stronger shared visual system: refreshed palette, reusable theme helpers, updated welcome/progress/results screens, and cleaner duplicate review cards.
- Reworked README structure for clearer ES/EN/PT onboarding, executable edition guidance, local validation, and error behavior documentation.

### Corrigido
- Added support for Google Takeout `*.supplemental-metadata.json` sidecar files so JSON metadata is detected, EXIF enrichment runs, and photo/JSON organization is triggered for the common Takeout naming pattern.
- Skipped direct EXIF writes for HEIC/HEIF files, avoiding noisy `piexif` errors while still using Takeout JSON metadata for date-based organization.
- Expanded Google Takeout sidecar matching for truncated `.suppl*` names, numbered metadata files, `*.jpg..json` files, Live Photo videos that share HEIC sidecar metadata, and orphan Takeout JSON files.
- Fixed partial Google Takeout re-runs so truncated JSON names already moved into `Json` are still matched, numbered Live Photo videos are organized, JSON sidecars already in `Json` are not renamed again, and media without matching JSON no longer remains in the root folder.
- Improved recoverable error handling for cache/config/history loading, analysis failures, QR fallback, per-file move/delete/export failures, and empty-folder scans.
- Replaced several mojibake-prone UI labels with clean synchronized ES/EN/PT text overrides.

### Instalacao com um comando (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

### Aviso do Windows SmartScreen
Os executaveis atuais nao possuem assinatura de codigo. O Windows pode mostrar um aviso de fornecedor desconhecido. Se voce confia na origem oficial do GitHub Releases, abra `Mais informacoes` e depois `Executar assim mesmo`.

### Instalacao local
1. Baixe o Codigo Fonte (`zip` ou `tar.gz`) abaixo.
2. Extraia os arquivos e abra um terminal na pasta.
3. Execute `Iniciar.bat` no Windows, ou use Python `3.14.x` e instale as dependencias manualmente com `pip install -r requirements.txt`.
4. Comando manual: `python src/main/photo_dedup.py`.

---

## Espanol

### Novedades en la v1.1.0
Fecha de release: 2026-05-24

### Cambios destacados
### Cambiado
- Runtime policy now targets Python `3.14.x`, matching the installed local Python used for development and validation from this version onward.
- Dependency bounds in `requirements.txt`, build-only dependencies in `requirements-build.txt`, Windows installers, build scripts, and GitHub Actions were updated for the Python 3.14 runtime line.
- Unified the previous `install.ps1` + `install_secure.ps1` flow into a single `install.ps1` that works as both remote bootstrapper and local installer/launcher.
- Standardized the local cloned-repository launcher as `Iniciar.bat`, replacing both the earlier `Install.bat` naming and the dependency-only `install_dependencies.bat` path.
- Removed the external funding UI behavior and related assets from the desktop interface.
- Redesigned the PyQt6 interface with a stronger shared visual system: refreshed palette, reusable theme helpers, updated welcome/progress/results screens, and cleaner duplicate review cards.
- Reworked README structure for clearer ES/EN/PT onboarding, executable edition guidance, local validation, and error behavior documentation.

### Corregido
- Added support for Google Takeout `*.supplemental-metadata.json` sidecar files so JSON metadata is detected, EXIF enrichment runs, and photo/JSON organization is triggered for the common Takeout naming pattern.
- Skipped direct EXIF writes for HEIC/HEIF files, avoiding noisy `piexif` errors while still using Takeout JSON metadata for date-based organization.
- Expanded Google Takeout sidecar matching for truncated `.suppl*` names, numbered metadata files, `*.jpg..json` files, Live Photo videos that share HEIC sidecar metadata, and orphan Takeout JSON files.
- Fixed partial Google Takeout re-runs so truncated JSON names already moved into `Json` are still matched, numbered Live Photo videos are organized, JSON sidecars already in `Json` are not renamed again, and media without matching JSON no longer remains in the root folder.
- Improved recoverable error handling for cache/config/history loading, analysis failures, QR fallback, per-file move/delete/export failures, and empty-folder scans.
- Replaced several mojibake-prone UI labels with clean synchronized ES/EN/PT text overrides.

### Instalacion con un solo comando (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

### Aviso de Windows SmartScreen
Los ejecutables actuales no estan firmados con certificado de firma de codigo. Windows puede mostrar un aviso de editor desconocido. Si confias en el origen oficial de GitHub Releases, abre `Mas informacion` y luego `Ejecutar de todas formas`.

### Instalacion local
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Ejecuta `Iniciar.bat` en Windows, o usa Python `3.14.x` e instala las dependencias manualmente con `pip install -r requirements.txt`.
4. Comando manual: `python src/main/photo_dedup.py`.
