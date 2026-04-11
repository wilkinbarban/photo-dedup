# PhotoDedup

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Português e Espanhol / Desplácese hacia abajo para Portugués y Español)*

🇺🇸 **English** | [🇧🇷 Português](#-português) | [🇪🇸 Español](#-español)

PhotoDedup is an intelligent duplicate photo finder and automated media organizer. Built with Python and PyQt6, it not only detects exact and similar duplicate images but also integrates deeply with Google Takeout JSON files to restore lost EXIF metadata and organize your photo and video library automatically.

## ⚡ Quick Install

Quick Installation: Run this command in PowerShell to download and install automatically.

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

For a safer installation flow, you can use the secure installer:

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` adds extra validation before running the installer. It checks GitHub connectivity, retries failed downloads, validates that the downloaded file is a ZIP archive, calculates its SHA-256 hash, allows optional hash verification, and cleans up temporary files if something fails.

To enforce SHA-256 validation, run this exact command:

```powershell
powershell -ExecutionPolicy Bypass -Command "&([scriptblock]::Create((iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1).Content)) -RepoZipUrl https://github.com/wilkinbarban/photo-dedup/archive/refs/tags/v1.0.0.zip -InstallFolderName photo-dedup-v1.0.0 -ExpectedZipSha256 eae1b914b7af0e7ea8466eb32fc5f6f34a68af8018fc836be40a270f1a3ab753"
```

Note: this example targets the versioned `v1.0.0` release ZIP, so the hash remains stable for that release.

## 🪟 Download Windows EXE

If you prefer not to use the console, download the prebuilt Windows executable from Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Look for the asset named `PhotoDedup-vX.Y.Z-windows.zip`, extract it, and run `PhotoDedup.exe`.

## 🚀 Features

*   **Intelligent Duplicate Detection**: Find exact duplicates based on file size/content or visually similar images using perceptual hashing and advanced AI-powered similarity checks (`MobileNetV2`).
*   **Google Takeout Integration**: Automatically associates `*.json` or `*.supplemen.json` files with your media. Restores `photoTakenTime`, `geoData` (GPS), and descriptions directly into the EXIF data.
*   **Automatic Media Organizer**: Renames files to a standard format (`YYYY-MM-DD_HH-MM-SS.ext`) and moves them into structured directories: `/YYYY/MM/`. Safely moves processed JSON files to a dedicated `/Json/` folder.
*   **Real-Time Log Viewer**: Monitor progress, background tasks, and errors directly from the UI.
*   **Multilingual Interface**: The application natively supports English, Spanish, and Brazilian Portuguese.
*   **Safe Deletion**: Duplicates are moved to the system's Recycle Bin/Trash, preventing accidental permanent loss.
*   **High Performance**: Utilizes multiple CPU cores and built-in caching (`cache.json` and `embeddings.pkl`) to speed up subsequent scans.

## 📦 Installation

1.  Clone this repository: `git clone https://github.com/wilkinbarban/photo-dedup`
2.  Install dependencies:
    *   **Windows**: Run `install_dependencies.bat`.
    *   **PowerShell (automatic)**: Run `install.ps1` for the standard one-line installer.
    *   **PowerShell (secure)**: Run `install_secure.ps1` to add connectivity checks, download retries, ZIP validation, and optional SHA-256 verification.
    *   **Manual**: `pip install -r requirements.txt`

## 💻 Usage

1.  Run `python photo_dedup.py`
2.  Select your preferred language at startup.
3.  Select the root folder containing your media and (optionally) Google Takeout JSON files.
4.  Choose your settings (Mode, Threshold, AI Level) and click **"Start"**.

## ☕ Support the Project

In the application's main screen, you'll find a **"Buy me a coffee"** button. Clicking it displays a PayPal QR code for voluntary donations. Your support is greatly appreciated!

## 🤝 Contributing & License

Contributions are welcome via the [issues page](https://github.com/wilkinbarban/photo-dedup/issues).
Licensed under the **GNU General Public License v3.0 (GPLv3)**.

---

# 🇧🇷 Português

🇺🇸 [English](#photodedup) | 🇧🇷 **Português** | [🇪🇸 Español](#-español)

PhotoDedup é um localizador inteligente de fotos duplicadas e organizador de mídia automatizado. Construído com Python e PyQt6, ele não apenas detecta imagens duplicadas exatas e semelhantes, mas também se integra profundamente com arquivos JSON do Google Takeout para restaurar metadados EXIF perdidos e organizar sua biblioteca automaticamente.

## ⚡ Instalação Rápida

Instalação Rápida: Execute este comando no PowerShell para baixar e instalar automaticamente.

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

Para um fluxo de instalação mais seguro, você pode usar o instalador seguro:

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` adiciona validações extras antes de executar o instalador. Ele verifica a conectividade com o GitHub, repete o download em caso de falha, valida se o arquivo baixado é realmente um ZIP, calcula o hash SHA-256, permite verificação opcional do hash e limpa os arquivos temporários se algo falhar.

Para exigir a validação SHA-256, execute este comando exato:

```powershell
powershell -ExecutionPolicy Bypass -Command "&([scriptblock]::Create((iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1).Content)) -RepoZipUrl https://github.com/wilkinbarban/photo-dedup/archive/refs/tags/v1.0.0.zip -InstallFolderName photo-dedup-v1.0.0 -ExpectedZipSha256 eae1b914b7af0e7ea8466eb32fc5f6f34a68af8018fc836be40a270f1a3ab753"
```

Observação: este exemplo usa o ZIP versionado da release `v1.0.0`, então o hash permanece estável para essa release.

## 🪟 Download do EXE para Windows

Se você prefere não usar console, baixe o executável do Windows já compilado em Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Procure o arquivo `PhotoDedup-vX.Y.Z-windows.zip`, extraia e execute `PhotoDedup.exe`.

## 🚀 Funcionalidades

*   **Detecção Inteligente de Duplicatas**: Encontre duplicatas exatas ou imagens visualmente semelhantes usando hash perceptivo e análises avançadas com Inteligência Artificial (`MobileNetV2`).
*   **Integração com Google Takeout**: Associa automaticamente arquivos JSON às suas mídias, restaurando `photoTakenTime`, `geoData` (GPS) e descrições diretamente nos dados EXIF.
*   **Organizador de Mídia Automático**: Renomeia arquivos para um formato padrão (`AAAA-MM-DD_HH-MM-SS.ext`) e os move para diretórios estruturados: `/AAAA/MM/`. Arquivos JSON processados são movidos para uma pasta `/Json/`.
*   **Visualizador de Logs em Tempo Real**: Monitore o progresso, tarefas em segundo plano e erros diretamente da interface.
*   **Interface Multilíngue**: O aplicativo suporta nativamente Inglês, Espanhol e Português do Brasil.
*   **Exclusão Segura**: Duplicatas são movidas para a Lixeira do sistema, evitando perdas acidentais.
*   **Alto Desempenho**: Utiliza múltiplos núcleos de CPU e cache integrado para acelerar verificações subsequentes.

## 📦 Instalação

1.  Clone este repositório: `git clone https://github.com/wilkinbarban/photo-dedup`
2.  Instale as dependências:
    *   **Windows**: Execute `install_dependencies.bat`.
    *   **PowerShell (automático)**: Execute `install.ps1` para a instalação padrão em uma linha.
    *   **PowerShell (seguro)**: Execute `install_secure.ps1` para adicionar verificação de conectividade, repetição de download, validação de ZIP e verificação opcional de SHA-256.
    *   **Manual**: `pip install -r requirements.txt`

## 💻 Como Usar

1.  Execute `python photo_dedup.py`
2.  Selecione seu idioma preferido na inicialização.
3.  Selecione a pasta raiz contendo suas mídias e arquivos JSON do Google Takeout.
4.  Escolha as configurações (Modo, Limite, Nível de IA) e clique em **"Iniciar"**.

## ☕ Apoie o Projeto

Na tela principal do aplicativo, você encontrará um botão **"Buy me a coffee"**. Ao clicar nele, um QR code do PayPal será exibido para doações voluntárias. Seu apoio é muito apreciado!

## 🤝 Contribuição e Licença

Contribuições são bem-vindas na [página de issues](https://github.com/wilkinbarban/photo-dedup/issues).
Licenciado sob a **GNU General Public License v3.0 (GPLv3)**.

---

# 🇪🇸 Español

🇺🇸 [English](#photodedup) | [🇧🇷 Português](#-português) | 🇪🇸 **Español**

PhotoDedup es un buscador inteligente de fotos duplicadas y organizador automático de medios. Creado con Python y PyQt6, no solo detecta imágenes duplicadas exactas o similares, sino que se integra profundamente con los archivos JSON de Google Takeout para restaurar metadatos EXIF perdidos y organizar tu biblioteca automáticamente.

## ⚡ Instalación Rápida

Puedes instalar todo sin necesidad de Git: abre PowerShell, pega este comando y ejecútalo.

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex"
```

Si prefieres un flujo de instalación más seguro, puedes usar el instalador seguro:

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

`install_secure.ps1` agrega validaciones extra antes de ejecutar el instalador. Comprueba la conectividad con GitHub, reintenta la descarga si falla, valida que el archivo descargado sea realmente un ZIP, calcula su hash SHA-256, permite una verificación opcional del hash y limpia los archivos temporales si algo sale mal.

Para forzar la validación SHA-256, ejecuta este comando exacto:

```powershell
powershell -ExecutionPolicy Bypass -Command "&([scriptblock]::Create((iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1).Content)) -RepoZipUrl https://github.com/wilkinbarban/photo-dedup/archive/refs/tags/v1.0.0.zip -InstallFolderName photo-dedup-v1.0.0 -ExpectedZipSha256 eae1b914b7af0e7ea8466eb32fc5f6f34a68af8018fc836be40a270f1a3ab753"
```

Nota: este ejemplo usa el ZIP versionado de la release `v1.0.0`, así que el hash se mantiene estable para esa release.

## 🪟 Descargar EXE de Windows

Si prefieres no usar consola, descarga el ejecutable de Windows ya compilado desde Releases:

https://github.com/wilkinbarban/photo-dedup/releases/latest

Busca el archivo `PhotoDedup-vX.Y.Z-windows.zip`, descomprímelo y ejecuta `PhotoDedup.exe`.

## 🚀 Características

*   **Detección Inteligente de Duplicados**: Encuentra duplicados exactos o imágenes visualmente similares usando hashing perceptivo y análisis avanzados con Inteligencia Artificial (`MobileNetV2`).
*   **Integración con Google Takeout**: Asocia automáticamente archivos JSON con tus medios, restaurando `photoTakenTime`, `geoData` (GPS) y descripciones directamente en los datos EXIF.
*   **Organizador Automático de Medios**: Renombra archivos a un formato estándar (`AAAA-MM-DD_HH-MM-SS.ext`) y los mueve a directorios estructurados: `/AAAA/MM/`. Los JSON procesados se guardan en una carpeta `/Json/`.
*   **Visor de Logs en Tiempo Real**: Monitorea el progreso, tareas en segundo plano y errores directamente desde la interfaz.
*   **Interfaz Multilingüe**: La aplicación soporta de forma nativa Inglés, Español y Portugués de Brasil.
*   **Borrado Seguro**: Los duplicados se mueven a la Papelera de Reciclaje del sistema para evitar pérdidas accidentales permanentes.
*   **Alto Rendimiento**: Utiliza múltiples núcleos de CPU y almacenamiento en caché (`cache.json` y `embeddings.pkl`) para acelerar los análisis futuros.

## 📦 Instalación

1.  Clona este repositorio: `git clone https://github.com/wilkinbarban/photo-dedup`
2.  Instala las dependencias:
    *   **Windows**: Ejecuta `install_dependencies.bat`.
    *   **PowerShell (automático)**: Ejecuta `install.ps1` para la instalación estándar en una sola línea.
    *   **PowerShell (seguro)**: Ejecuta `install_secure.ps1` para añadir comprobación de conectividad, reintentos de descarga, validación de ZIP y verificación opcional de SHA-256.
    *   **Manual**: `pip install -r requirements.txt`

## 💻 Uso

1.  Ejecuta `python photo_dedup.py`
2.  Selecciona tu idioma preferido al iniciar.
3.  Selecciona la carpeta raíz que contiene tus medios y los archivos JSON de Google Takeout.
4.  Elige tu configuración (Modo, Umbral, Nivel de IA) y haz clic en **"Iniciar"**.

## ☕ Apoya el Proyecto

En la pantalla principal de la aplicación, encontrarás un botón **"Buy me a coffee"**. Al hacer clic, se mostrará un código QR de PayPal para donaciones voluntarias. ¡Tu apoyo es muy apreciado!

## 🤝 Contribuciones y Licencia

Las contribuciones son bienvenidas a través de la [página de issues](https://github.com/wilkinbarban/photo-dedup/issues).
Licenciado bajo la **GNU General Public License v3.0 (GPLv3)**.

