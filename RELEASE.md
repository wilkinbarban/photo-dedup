# PhotoDedup v1.0.4

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Português e Espanhol / Desplácese hacia abajo para Portugués y Español)*

🇺🇸 **English**

## What's new in v1.0.4
This release focuses on zero-friction distribution for novice users by publishing a standalone single-file executable and aligning CI validation to that packaging mode.

### Highlights
- **Standalone EXE published**: Release assets now include direct `PhotoDedup.exe` download for users who do not want extraction steps.
- **Single-file packaging mode**: PyInstaller moved to `onefile`, bundling runtime components into one executable.
- **Smoke test aligned to onefile output**: CI now validates startup of `dist/PhotoDedup.exe`.
- **User-focused documentation updates**: README now highlights direct standalone EXE download in ES/EN/PT.

### Recommended secure install (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

### Standard install
1. Download the Source Code (`zip` or `tar.gz`) below.
2. Extract the files and open a terminal in the folder.
3. Install dependencies: `install_dependencies.bat` (Windows) or `pip install -r requirements.txt`.
4. Run: `python photo_dedup.py`.

---

🇧🇷 **Português (Brasil)**

## O que há de novo na v1.0.4
Esta versao prioriza distribuicao sem atrito para usuarios iniciantes, publicando um executavel unico e alinhando a validacao de CI para esse modo.

### Destaques
- **EXE standalone publicado**: Os assets do release agora incluem `PhotoDedup.exe` para download direto sem etapa de extracao.
- **Empacotamento em arquivo unico**: PyInstaller migrado para `onefile`, com dependencias de runtime empacotadas no executavel.
- **Smoke test alinhado ao onefile**: CI agora valida inicializacao de `dist/PhotoDedup.exe`.
- **Documentacao focada no usuario final**: README destaca download direto do EXE standalone em ES/EN/PT.

### Instalação segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

### Instalação padrão
1. Baixe o Código Fonte (`zip` ou `tar.gz`) abaixo.
2. Extraia os arquivos e abra um terminal na pasta.
3. Instale as dependências: `install_dependencies.bat` (Windows) ou `pip install -r requirements.txt`.
4. Execute: `python photo_dedup.py`.

---

🇪🇸 **Español**

## Novedades en la v1.0.4
Esta version se centra en distribucion sin friccion para usuarios novatos, publicando un ejecutable unico y alineando la validacion de CI con ese modo.

### Cambios destacados
- **EXE standalone publicado**: Los assets del release ahora incluyen `PhotoDedup.exe` para descarga directa sin pasos de extraccion.
- **Empaquetado en archivo unico**: PyInstaller migrado a `onefile`, con dependencias de runtime dentro del ejecutable.
- **Smoke-test alineado con onefile**: CI ahora valida el arranque de `dist/PhotoDedup.exe`.
- **Documentacion orientada al usuario final**: README destaca la descarga directa del EXE standalone en ES/EN/PT.

### Instalación segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

### Instalación estándar
1. Descarga el Código Fuente (`zip` o `tar.gz`) a continuación.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python photo_dedup.py`.