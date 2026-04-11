# PhotoDedup v1.0.1

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Português e Espanhol / Desplácese hacia abajo para Portugués y Español)*

🇺🇸 **English**

## What's new in v1.0.1
This release improves installation reliability and security, especially for users installing PhotoDedup directly from PowerShell.

### Highlights
- **One-line PowerShell install**: Added `install.ps1` for automatic download and setup without requiring Git.
- **Secure installer option**: Added `install_secure.ps1` with connectivity checks, retry logic, ZIP validation, SHA-256 calculation, and optional hash enforcement.
- **Versioned release installs**: PowerShell installers now accept custom release ZIP URLs and custom install folder names.
- **Improved Windows compatibility**: Installers now resolve the real Desktop path (including redirected OneDrive Desktop).
- **Dependency installer improvements**: `install_dependencies.bat` now shows English messages, improves Python detection/PATH handling, and launches the app after successful installation.
- **Documentation overhaul**: README now includes multilingual quick install guides and secure install examples with hash validation.

### Recommended secure install (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/7d12ee7/install_secure.ps1 | iex"
```

### Standard install
1. Download the Source Code (`zip` or `tar.gz`) below.
2. Extract the files and open a terminal in the folder.
3. Install dependencies: `install_dependencies.bat` (Windows) or `pip install -r requirements.txt`.
4. Run: `python photo_dedup.py`.

---

🇧🇷 **Português (Brasil)**

## O que há de novo na v1.0.1
Esta versão melhora a confiabilidade e a segurança da instalação, especialmente para usuários que instalam o PhotoDedup diretamente pelo PowerShell.

### Destaques
- **Instalação em uma linha no PowerShell**: Adicionado `install.ps1` para download e configuração automática sem exigir Git.
- **Opção de instalador seguro**: Adicionado `install_secure.ps1` com verificação de conectividade, tentativas automáticas, validação de ZIP, cálculo de SHA-256 e verificação opcional de hash.
- **Instalação por releases versionadas**: Instaladores PowerShell agora aceitam URL de ZIP de release e nome de pasta de instalação personalizados.
- **Compatibilidade melhorada no Windows**: Instaladores agora resolvem o caminho real da Área de Trabalho (incluindo redirecionamento via OneDrive).
- **Melhorias no instalador de dependências**: `install_dependencies.bat` agora exibe mensagens em inglês, melhora detecção de Python/PATH e inicia o app após instalação bem-sucedida.
- **Documentação ampliada**: README agora inclui guias multilíngues de instalação rápida e exemplos de instalação segura com validação de hash.

### Instalação segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/7d12ee7/install_secure.ps1 | iex"
```

### Instalação padrão
1. Baixe o Código Fonte (`zip` ou `tar.gz`) abaixo.
2. Extraia os arquivos e abra um terminal na pasta.
3. Instale as dependências: `install_dependencies.bat` (Windows) ou `pip install -r requirements.txt`.
4. Execute: `python photo_dedup.py`.

---

🇪🇸 **Español**

## Novedades en la v1.0.1
Esta versión mejora la fiabilidad y la seguridad de la instalación, especialmente para usuarios que instalan PhotoDedup directamente desde PowerShell.

### Cambios destacados
- **Instalación en una línea con PowerShell**: Se añadió `install.ps1` para descargar y configurar automáticamente sin necesidad de Git.
- **Instalador seguro opcional**: Se añadió `install_secure.ps1` con comprobación de conectividad, reintentos, validación de ZIP, cálculo de SHA-256 y verificación opcional del hash.
- **Instalación por releases versionadas**: Los instaladores de PowerShell ahora aceptan URL de ZIP de release y nombre de carpeta de instalación personalizados.
- **Mejor compatibilidad con Windows**: Los instaladores ahora detectan la ruta real del Escritorio (incluyendo redirección con OneDrive).
- **Mejoras del instalador de dependencias**: `install_dependencies.bat` ahora muestra mensajes en inglés, mejora la detección de Python/PATH y abre el programa tras una instalación exitosa.
- **Documentación ampliada**: El README ahora incluye instalación rápida multilingüe y ejemplos de instalación segura con validación de hash.

### Instalación segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/7d12ee7/install_secure.ps1 | iex"
```

### Instalación estándar
1. Descarga el Código Fuente (`zip` o `tar.gz`) a continuación.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python photo_dedup.py`.