# PhotoDedup v1.0.9

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.0.9
Release date: 2026-04-12

### Highlights
### Added
- **Dual build automation**: Added `scripts/build_variants.ps1` to generate `full` and `lite` Windows builds in one command, run smoke tests, and write a comparison report in JSON.

### Changed
- **Release artifacts (dual assets)**: Release pipeline now publishes both variants (`PhotoDedup-full.exe` / `PhotoDedup-lite.exe`) and their ZIP packages.
- **Build script telemetry**: `scripts/build_windows.ps1` now supports integrated smoke testing and writes build metrics JSON files.
- **Packaging flavors**: `PhotoDedup.spec` now supports `full` and `lite` modes using `PHOTO_DEDUP_BUILD_FLAVOR`.

### Fixed
- **Lite runtime resilience**: Added fallback to hash-only detection when AI dependencies are unavailable in lite builds.

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

### O que ha de novo na v1.0.9
Data do release: 2026-04-12

### Destaques
### Adicionado
- **Dual build automation**: Added `scripts/build_variants.ps1` to generate `full` and `lite` Windows builds in one command, run smoke tests, and write a comparison report in JSON.

### Alterado
- **Release artifacts (dual assets)**: Release pipeline now publishes both variants (`PhotoDedup-full.exe` / `PhotoDedup-lite.exe`) and their ZIP packages.
- **Build script telemetry**: `scripts/build_windows.ps1` now supports integrated smoke testing and writes build metrics JSON files.
- **Packaging flavors**: `PhotoDedup.spec` now supports `full` and `lite` modes using `PHOTO_DEDUP_BUILD_FLAVOR`.

### Corrigido
- **Lite runtime resilience**: Added fallback to hash-only detection when AI dependencies are unavailable in lite builds.

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

### Novedades en la v1.0.9
Fecha de release: 2026-04-12

### Cambios destacados
### Anadido
- **Dual build automation**: Added `scripts/build_variants.ps1` to generate `full` and `lite` Windows builds in one command, run smoke tests, and write a comparison report in JSON.

### Cambiado
- **Release artifacts (dual assets)**: Release pipeline now publishes both variants (`PhotoDedup-full.exe` / `PhotoDedup-lite.exe`) and their ZIP packages.
- **Build script telemetry**: `scripts/build_windows.ps1` now supports integrated smoke testing and writes build metrics JSON files.
- **Packaging flavors**: `PhotoDedup.spec` now supports `full` and `lite` modes using `PHOTO_DEDUP_BUILD_FLAVOR`.

### Corregido
- **Lite runtime resilience**: Added fallback to hash-only detection when AI dependencies are unavailable in lite builds.

### Instalacion segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacion estandar
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python src/main/photo_dedup.py`.
