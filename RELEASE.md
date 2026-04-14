# PhotoDedup v1.0.12

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.0.12
Release date: 2026-04-13

### Highlights
### Added
- **Runtime AI capability gate**: Added runtime detection for optional AI dependencies (`torch` + `torchvision`) so the UI can adapt automatically by build flavor.

### Changed
- **One-click installer architecture**: `install.ps1` now follows a robust local-installer pattern with project-root validation, bootstrap fallback (download/update repository when needed), Python runtime checks (`>=3.8,<3.14`), `.venv` lifecycle handling, dependency installation, and app launch.
- **Secure remote installer flow**: `install_secure.ps1` now follows a secure bootstrap-and-delegate model (download over TLS, basic archive validation, install/update preserving `.venv`, then delegate to local `install.ps1`).
- **Release artifact policy**: Dual-variant build now publishes only executables (`PhotoDedup-full.exe`, `PhotoDedup-lite.exe`); no ZIPs and no `build-variants-vX.Y.Z.json` summary file.

### Fixed
- **Main window icon rendering**: Explicitly set `Icon.ico` on `MainWindow`, fixing cases where only secondary dialogs had the icon.
- **Donation QR rendering**: Switched donation QR path resolution to `resolve_asset_path(...)` with pixmap validity checks, fixing missing `QR_Paypal.png` in packaged/runtime contexts.
- **Lite UI coherence**: In `PhotoDedup-lite.exe`, AI controls are now hidden from the welcome screen when AI runtime dependencies are unavailable, and analysis config is forced to non-AI mode.
- **Smoke test workflow artifact mismatch**: Updated smoke-test workflow to upload the actual generated EXE artifact instead of a removed ZIP path.

### Recommended secure install (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Standard install
1. Download the Source Code (`zip` or `tar.gz`) below.
2. Extract the files and open a terminal in the folder.
3. Install dependencies: `install_dependencies.bat` (Windows) or `pip install -r requirements.txt`.
4. Run: `python src/main/photo_dedup.py`.

---

## Portugues (Brasil)

### O que ha de novo na v1.0.12
Data do release: 2026-04-13

### Destaques
### Adicionado
- **Runtime AI capability gate**: Added runtime detection for optional AI dependencies (`torch` + `torchvision`) so the UI can adapt automatically by build flavor.

### Alterado
- **One-click installer architecture**: `install.ps1` now follows a robust local-installer pattern with project-root validation, bootstrap fallback (download/update repository when needed), Python runtime checks (`>=3.8,<3.14`), `.venv` lifecycle handling, dependency installation, and app launch.
- **Secure remote installer flow**: `install_secure.ps1` now follows a secure bootstrap-and-delegate model (download over TLS, basic archive validation, install/update preserving `.venv`, then delegate to local `install.ps1`).
- **Release artifact policy**: Dual-variant build now publishes only executables (`PhotoDedup-full.exe`, `PhotoDedup-lite.exe`); no ZIPs and no `build-variants-vX.Y.Z.json` summary file.

### Corrigido
- **Main window icon rendering**: Explicitly set `Icon.ico` on `MainWindow`, fixing cases where only secondary dialogs had the icon.
- **Donation QR rendering**: Switched donation QR path resolution to `resolve_asset_path(...)` with pixmap validity checks, fixing missing `QR_Paypal.png` in packaged/runtime contexts.
- **Lite UI coherence**: In `PhotoDedup-lite.exe`, AI controls are now hidden from the welcome screen when AI runtime dependencies are unavailable, and analysis config is forced to non-AI mode.
- **Smoke test workflow artifact mismatch**: Updated smoke-test workflow to upload the actual generated EXE artifact instead of a removed ZIP path.

### Instalacao segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacao padrao
1. Baixe o Codigo Fonte (`zip` ou `tar.gz`) abaixo.
2. Extraia os arquivos e abra um terminal na pasta.
3. Instale as dependencias: `install_dependencies.bat` (Windows) ou `pip install -r requirements.txt`.
4. Execute: `python src/main/photo_dedup.py`.

---

## Espanol

### Novedades en la v1.0.12
Fecha de release: 2026-04-13

### Cambios destacados
### Anadido
- **Runtime AI capability gate**: Added runtime detection for optional AI dependencies (`torch` + `torchvision`) so the UI can adapt automatically by build flavor.

### Cambiado
- **One-click installer architecture**: `install.ps1` now follows a robust local-installer pattern with project-root validation, bootstrap fallback (download/update repository when needed), Python runtime checks (`>=3.8,<3.14`), `.venv` lifecycle handling, dependency installation, and app launch.
- **Secure remote installer flow**: `install_secure.ps1` now follows a secure bootstrap-and-delegate model (download over TLS, basic archive validation, install/update preserving `.venv`, then delegate to local `install.ps1`).
- **Release artifact policy**: Dual-variant build now publishes only executables (`PhotoDedup-full.exe`, `PhotoDedup-lite.exe`); no ZIPs and no `build-variants-vX.Y.Z.json` summary file.

### Corregido
- **Main window icon rendering**: Explicitly set `Icon.ico` on `MainWindow`, fixing cases where only secondary dialogs had the icon.
- **Donation QR rendering**: Switched donation QR path resolution to `resolve_asset_path(...)` with pixmap validity checks, fixing missing `QR_Paypal.png` in packaged/runtime contexts.
- **Lite UI coherence**: In `PhotoDedup-lite.exe`, AI controls are now hidden from the welcome screen when AI runtime dependencies are unavailable, and analysis config is forced to non-AI mode.
- **Smoke test workflow artifact mismatch**: Updated smoke-test workflow to upload the actual generated EXE artifact instead of a removed ZIP path.

### Instalacion segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacion estandar
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python src/main/photo_dedup.py`.
