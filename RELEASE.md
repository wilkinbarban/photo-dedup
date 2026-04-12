# PhotoDedup v1.0.7

*(Auto-generated from CHANGELOG. Do not edit manually.)*

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Portugues e Espanhol / Desplacese hacia abajo para Portugues y Espanol)*

## English

### What's new in v1.0.7
Release date: 2026-04-12

### Highlights
### Changed
- **Release reliability**: Updated CI triggers so release build and smoke-test workflows run from tag-based publication flow without GitHub token event-chaining issues.

### Fixed
- **Runtime import bootstrap**: Added startup path bootstrap in `src/main/photo_dedup.py` to guarantee `src.*` imports resolve correctly when launching the entrypoint directly and in frozen runtime.

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

### O que ha de novo na v1.0.7
Data do release: 2026-04-12

### Destaques
### Alterado
- **Release reliability**: Updated CI triggers so release build and smoke-test workflows run from tag-based publication flow without GitHub token event-chaining issues.

### Corrigido
- **Runtime import bootstrap**: Added startup path bootstrap in `src/main/photo_dedup.py` to guarantee `src.*` imports resolve correctly when launching the entrypoint directly and in frozen runtime.

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

### Novedades en la v1.0.7
Fecha de release: 2026-04-12

### Cambios destacados
### Cambiado
- **Release reliability**: Updated CI triggers so release build and smoke-test workflows run from tag-based publication flow without GitHub token event-chaining issues.

### Corregido
- **Runtime import bootstrap**: Added startup path bootstrap in `src/main/photo_dedup.py` to guarantee `src.*` imports resolve correctly when launching the entrypoint directly and in frozen runtime.

### Instalacion segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalacion estandar
1. Descarga el Codigo Fuente (`zip` o `tar.gz`) a continuacion.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python src/main/photo_dedup.py`.
