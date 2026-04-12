<div align="center">
  <img src="assets/Icon.ico" alt="PhotoDedup Logo" width="120" height="120">
  <h1>PhotoDedup</h1>

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/downloads/release/python-3110/)
  [![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
  [![Releases](https://img.shields.io/github/v/release/wilkinbarban/photo-dedup)](https://github.com/wilkinbarban/photo-dedup/releases)
  [![Educational](https://img.shields.io/badge/Purpose-Educational-orange.svg)](#educational-disclaimer--aviso-educativo--aviso-educacional)
</div>

---

> **Educational Disclaimer / Aviso Educativo / Aviso Educacional**
>
> This project is developed strictly for educational purposes to demonstrate Python desktop development with PyQt6, image analysis workflows, background processing, and installer automation.
>
> Este proyecto se desarrolla estrictamente con fines educativos para demostrar desarrollo de aplicaciones de escritorio con Python/PyQt6, analisis de imagenes, procesos en segundo plano y automatizacion de instaladores.
>
> Este projeto e desenvolvido estritamente para fins educacionais para demonstrar desenvolvimento desktop com Python/PyQt6, analise de imagens, processamento em segundo plano e automacao de instaladores.

---

## Language / Idioma / Idioma

- [Español](#español)
- [English](#english)
- [Português (Brasil)](#português-brasil)

---

## Español

### Descripción
PhotoDedup es una aplicación de escritorio para Windows creada con Python y PyQt6 para encontrar fotos duplicadas y organizar medios automáticamente. Detecta duplicados exactos y similares, integra archivos JSON de Google Takeout para restaurar metadatos EXIF y ordena tu biblioteca.

### Características
- Detección de duplicados exactos y visualmente similares.
- Integración con Google Takeout (`*.json`) para restaurar EXIF.
- Organización automática por fecha en estructura `AAAA/MM`.
- Visor de logs en tiempo real.
- Interfaz multilenguaje: Español, English y Português (Brasil).
- Borrado seguro (Papelera del sistema).

### Descargar EXE de Windows
Si prefieres evitar la consola, descarga el ejecutable precompilado desde Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Busca el archivo `PhotoDedup-vX.Y.Z-windows.zip`, descomprímelo y ejecuta `PhotoDedup.exe`.
También puedes descargar directamente `PhotoDedup.exe` (ejecutable único).

### Instalación con un solo comando (PowerShell)

**Opción A - Instalación automática estándar:**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

**Opción B - Instalación automática segura (canal estable):**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` verifica conectividad, reintenta descargas, valida ZIP, calcula SHA-256 y limpia temporales.

### Instalación manual
1. Clona o descarga este repositorio.
2. Ejecuta `install_dependencies.bat` o instala manualmente con `pip install -r requirements.txt`.
3. Ejecuta `python photo_dedup.py`.

---

## English

### Description
PhotoDedup is a Windows desktop application built with Python and PyQt6 to find duplicate photos and organize media automatically. It detects exact and visual duplicates, integrates Google Takeout JSON files to restore EXIF metadata, and structures your library.

### Features
- Exact and visual duplicate detection.
- Google Takeout (`*.json`) integration for EXIF restoration.
- Automatic date-based media organization (`YYYY/MM`).
- Real-time log viewer.
- Multilingual UI: Español, English, and Português (Brasil).
- Safe deletion to Recycle Bin.

### Download Windows EXE
If you prefer not to use the console, download the prebuilt executable from Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Look for `PhotoDedup-vX.Y.Z-windows.zip`, extract it, and run `PhotoDedup.exe`.
You can also download `PhotoDedup.exe` directly (single-file executable).

### One-command install (PowerShell)

**Option A - Standard automatic install:**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

**Option B - Secure automatic install (stable channel):**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` checks connectivity, retries downloads, validates ZIP format, calculates SHA-256, and cleans temp files.

### Manual install
1. Clone or download this repository.
2. Run `install_dependencies.bat` or install manually with `pip install -r requirements.txt`.
3. Run `python photo_dedup.py`.

---

## Português (Brasil)

### Descrição
PhotoDedup e um aplicativo desktop para Windows, desenvolvido com Python e PyQt6, para localizar fotos duplicadas e organizar midias automaticamente. Detecta duplicatas exatas e visuais, integra JSON do Google Takeout para restaurar metadados EXIF e estrutura a biblioteca.

### Recursos
- Deteccao de duplicatas exatas e visuais.
- Integracao com Google Takeout (`*.json`) para restauracao de EXIF.
- Organizacao automatica por data (`AAAA/MM`).
- Visualizador de logs em tempo real.
- Interface multilíngue: Español, English e Português (Brasil).
- Exclusao segura para a Lixeira.

### Download do EXE para Windows
Se preferir nao usar console, baixe o executavel precompilado em Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Procure por `PhotoDedup-vX.Y.Z-windows.zip`, extraia e execute `PhotoDedup.exe`.
Voce tambem pode baixar `PhotoDedup.exe` diretamente (executavel unico).

### Instalacao com um unico comando (PowerShell)

**Opcao A - Instalacao automatica padrao:**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

**Opcao B - Instalacao automatica segura (canal estavel):**
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` verifica conectividade, repete downloads, valida ZIP, calcula SHA-256 e limpa arquivos temporarios.

### Instalacao manual
1. Clone ou baixe este repositorio.
2. Execute `install_dependencies.bat` ou instale manualmente com `pip install -r requirements.txt`.
3. Execute `python photo_dedup.py`.

---

## Project Structure

| File / Folder | Description |
|---|---|
| `photo_dedup.py` | Main application entry point |
| `core/` | Core logic: analysis, models, state, i18n, logging |
| `ui/` | User interface components and screens |
| `assets/` | Icons and visual resources |
| `install_dependencies.bat` | Windows dependency installer |
| `install.ps1` | Standard PowerShell installer |
| `install_secure.ps1` | Secure installer for stable release channel |
| `scripts/build_windows.ps1` | Builds and packages Windows EXE |
| `.github/workflows/build-release-exe.yml` | Builds and uploads release assets |
| `.github/workflows/smoke-test-exe.yml` | Smoke-test for EXE startup/shutdown |

---

## Educational Disclaimer / Aviso Educativo / Aviso Educacional

This software is provided for educational purposes only. Use of this tool must comply with YouTube Terms of Service, copyright laws, and local regulations. The author is not responsible for third-party misuse.

---

## License

This project is licensed under the GNU General Public License v3.0.
See [LICENSE](LICENSE) for full details.

