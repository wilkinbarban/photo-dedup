# PhotoDedup v1.0.6

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.0.6
Release date: 2026-04-12

### Highlights
### Added
- **Canonical src architecture**: Introduced `src/main`, `src/modules`, and `src/interfaces` as the final runtime structure, with `src/main/photo_dedup.py` as the canonical app entrypoint.
- **Maintenance script namespace**: Moved maintenance utilities to `scripts/maintenance/` (`update_analyzer.py`, `update_texts.py`) to keep the project root clean.

### Changed
- **Packaging and CI path alignment**: Updated `PhotoDedup.spec`, `scripts/build_windows.ps1`, and `.github/workflows/publish-release-from-tag.yml` to resolve version/build entrypoint from `src/main/photo_dedup.py`.
- **Installer/runtime commands**: Updated installer and release docs to launch the app via `python src/main/photo_dedup.py`.

### Fixed
- **Legacy module removal**: Removed compatibility wrappers and deleted deprecated `core/` and `ui/` trees after migration validation.

### Documentation
- Updated `README.md`, `CONTRIBUTING.md`, `RELEASE.md`, and `RELEASE.template.md` to reflect the final `src/`-based structure and commands.

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

### O que ha de novo na v1.0.6
Data do release: 2026-04-12

### Destaques
### Adicionado
- **Canonical src architecture**: Introduced `src/main`, `src/modules`, and `src/interfaces` as the final runtime structure, with `src/main/photo_dedup.py` as the canonical app entrypoint.
- **Maintenance script namespace**: Moved maintenance utilities to `scripts/maintenance/` (`update_analyzer.py`, `update_texts.py`) to keep the project root clean.

### Alterado
- **Packaging and CI path alignment**: Updated `PhotoDedup.spec`, `scripts/build_windows.ps1`, and `.github/workflows/publish-release-from-tag.yml` to resolve version/build entrypoint from `src/main/photo_dedup.py`.
- **Installer/runtime commands**: Updated installer and release docs to launch the app via `python src/main/photo_dedup.py`.

### Corrigido
- **Legacy module removal**: Removed compatibility wrappers and deleted deprecated `core/` and `ui/` trees after migration validation.

### Documentacao
- Updated `README.md`, `CONTRIBUTING.md`, `RELEASE.md`, and `RELEASE.template.md` to reflect the final `src/`-based structure and commands.

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

### Novedades en la v1.0.6
Fecha de release: 2026-04-12

### Cambios destacados
### Anadido
- **Canonical src architecture**: Introduced `src/main`, `src/modules`, and `src/interfaces` as the final runtime structure, with `src/main/photo_dedup.py` as the canonical app entrypoint.
- **Maintenance script namespace**: Moved maintenance utilities to `scripts/maintenance/` (`update_analyzer.py`, `update_texts.py`) to keep the project root clean.

### Cambiado
- **Packaging and CI path alignment**: Updated `PhotoDedup.spec`, `scripts/build_windows.ps1`, and `.github/workflows/publish-release-from-tag.yml` to resolve version/build entrypoint from `src/main/photo_dedup.py`.
- **Installer/runtime commands**: Updated installer and release docs to launch the app via `python src/main/photo_dedup.py`.

### Corregido
- **Legacy module removal**: Removed compatibility wrappers and deleted deprecated `core/` and `ui/` trees after migration validation.

### Documentacion
- Updated `README.md`, `CONTRIBUTING.md`, `RELEASE.md`, and `RELEASE.template.md` to reflect the final `src/`-based structure and commands.

### Instalacion segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacion estandar
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python src/main/photo_dedup.py`.
