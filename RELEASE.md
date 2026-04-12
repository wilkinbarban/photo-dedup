# PhotoDedup v1.0.5

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Português e Espanhol / Desplácese hacia abajo para Portugués y Español)*

🇺🇸 **English**

## What's new in v1.0.5
This release refines the asset policy for cleaner downloads: novice users now receive only the executable deliverables in release assets.

### Highlights
- **Cleaner release assets**: `install_secure.ps1` is no longer uploaded as a release asset.
- **Executable-focused delivery**: Release assets now include only `PhotoDedup.exe` and `PhotoDedup-vX.Y.Z-windows.zip`.
- **Secure installer still available**: `install_secure.ps1` can be fetched from repository source when needed.

### Recommended secure install (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Standard install
1. Download the Source Code (`zip` or `tar.gz`) below.
2. Extract the files and open a terminal in the folder.
3. Install dependencies: `install_dependencies.bat` (Windows) or `pip install -r requirements.txt`.
4. Run: `python photo_dedup.py`.

---

🇧🇷 **Português (Brasil)**

## O que há de novo na v1.0.5
Esta versao refina a politica de assets para downloads mais limpos: usuarios iniciantes recebem apenas os entregaveis executaveis no release.

### Destaques
- **Assets de release mais limpos**: `install_secure.ps1` nao e mais enviado como asset de release.
- **Entrega focada no executavel**: os assets do release agora incluem apenas `PhotoDedup.exe` e `PhotoDedup-vX.Y.Z-windows.zip`.
- **Instalador seguro ainda disponivel**: `install_secure.ps1` pode ser baixado pelo source do repositorio quando necessario.

### Instalação segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalação padrão
1. Baixe o Código Fonte (`zip` ou `tar.gz`) abaixo.
2. Extraia os arquivos e abra um terminal na pasta.
3. Instale as dependências: `install_dependencies.bat` (Windows) ou `pip install -r requirements.txt`.
4. Execute: `python photo_dedup.py`.

---

🇪🇸 **Español**

## Novedades en la v1.0.5
Esta version refina la politica de assets para descargas mas limpias: usuarios novatos reciben solo los entregables ejecutables en el release.

### Cambios destacados
- **Assets de release mas limpios**: `install_secure.ps1` ya no se sube como asset del release.
- **Entrega enfocada en ejecutables**: los assets del release ahora incluyen solo `PhotoDedup.exe` y `PhotoDedup-vX.Y.Z-windows.zip`.
- **Instalador seguro todavia disponible**: `install_secure.ps1` se puede descargar desde el source del repositorio cuando sea necesario.

### Instalación segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex"
```

### Instalación estándar
1. Descarga el Código Fuente (`zip` o `tar.gz`) a continuación.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python photo_dedup.py`.