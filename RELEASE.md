# PhotoDedup v1.0.3

*(Scroll down for Portuguese and Spanish versions / Role para baixo para Português e Espanhol / Desplácese hacia abajo para Portugués y Español)*

🇺🇸 **English**

## What's new in v1.0.3
This release strengthens the Windows distribution pipeline and makes the secure installer available through a stable release channel for non-technical users.

### Highlights
- **Stable secure installer channel**: `install_secure.ps1` is now published as a release asset, enabling stable install commands via `releases/latest/download`.
- **Automated smoke testing for EXE**: Added a Windows smoke-test workflow to validate executable startup and controlled shutdown.
- **Improved release assets**: Published releases now include both `PhotoDedup-vX.Y.Z-windows.zip` and `install_secure.ps1`.
- **User-focused documentation updates**: README now includes multilingual direct-download instructions for Windows EXE and updated secure installer commands.

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

## O que há de novo na v1.0.3
Esta versão fortalece o pipeline de distribuição para Windows e disponibiliza o instalador seguro por um canal estável de release para usuários não técnicos.

### Destaques
- **Canal estável para instalador seguro**: `install_secure.ps1` agora é publicado como asset do release, permitindo comandos estáveis com `releases/latest/download`.
- **Teste automatizado de fumaça do EXE**: Novo workflow em Windows para validar inicialização do executável e encerramento controlado.
- **Assets de release aprimorados**: Releases publicados agora incluem `PhotoDedup-vX.Y.Z-windows.zip` e `install_secure.ps1`.
- **Documentação focada no usuário final**: README com instruções multilíngues para download direto do EXE e comandos atualizados do instalador seguro.

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

## Novedades en la v1.0.3
Esta versión fortalece el pipeline de distribución para Windows y habilita un canal estable del instalador seguro para usuarios no técnicos.

### Cambios destacados
- **Canal estable para instalador seguro**: `install_secure.ps1` ahora se publica como asset del release, permitiendo comandos estables con `releases/latest/download`.
- **Smoke-test automatizado del EXE**: Nuevo workflow en Windows para validar el arranque del ejecutable y su cierre controlado.
- **Assets de release mejorados**: Los releases publicados ahora incluyen `PhotoDedup-vX.Y.Z-windows.zip` e `install_secure.ps1`.
- **Documentación orientada al usuario final**: README con instrucciones multilingües para descarga directa del EXE y comandos actualizados del instalador seguro.

### Instalación segura recomendada (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing https://github.com/wilkinbarban/photo-dedup/releases/latest/download/install_secure.ps1 | iex"
```

### Instalación estándar
1. Descarga el Código Fuente (`zip` o `tar.gz`) a continuación.
2. Extrae los archivos y abre una terminal en la carpeta.
3. Instala las dependencias: `install_dependencies.bat` (Windows) o `pip install -r requirements.txt`.
4. Ejecuta: `python photo_dedup.py`.