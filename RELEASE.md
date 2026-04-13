# PhotoDedup v1.0.10

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.0.10
Release date: 2026-04-12

### Highlights
### Fixed
- **Dual-release CI reliability**: Prevented cleanup lock failures between `full` and `lite` builds by running `-Clean` only for the first variant in `scripts/build_variants.ps1`.
- **Smoke-test stability**: Added retry logic in `scripts/build_windows.ps1` when the executable exits early on first launch (transient onefile startup behavior in CI).
- **Cleanup robustness**: Added retry loop for removing `dist` during clean builds to avoid transient file-handle errors on Windows runners.

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

### O que ha de novo na v1.0.10
Data do release: 2026-04-12

### Destaques
### Corrigido
- **Dual-release CI reliability**: Prevented cleanup lock failures between `full` and `lite` builds by running `-Clean` only for the first variant in `scripts/build_variants.ps1`.
- **Smoke-test stability**: Added retry logic in `scripts/build_windows.ps1` when the executable exits early on first launch (transient onefile startup behavior in CI).
- **Cleanup robustness**: Added retry loop for removing `dist` during clean builds to avoid transient file-handle errors on Windows runners.

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

### Novedades en la v1.0.10
Fecha de release: 2026-04-12

### Cambios destacados
### Corregido
- **Dual-release CI reliability**: Prevented cleanup lock failures between `full` and `lite` builds by running `-Clean` only for the first variant in `scripts/build_variants.ps1`.
- **Smoke-test stability**: Added retry logic in `scripts/build_windows.ps1` when the executable exits early on first launch (transient onefile startup behavior in CI).
- **Cleanup robustness**: Added retry loop for removing `dist` during clean builds to avoid transient file-handle errors on Windows runners.

### Instalacion segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacion estandar
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python src/main/photo_dedup.py`.
