#Requires -Version 5.1
<#
.SYNOPSIS
    PhotoDedup - One-command installer and launcher for Windows.

.DESCRIPTION
    Unified installer for local and remote execution. If the script is
    executed outside the project root, it downloads the repository from GitHub
    over HTTPS, validates the extracted structure, installs or updates the
    local copy, and delegates to the local install.ps1.

    In local mode it validates Python 3.14.x, creates or repairs .venv,
    installs requirements.txt, and launches PhotoDedup.

.EXAMPLE
    .\install.ps1

.EXAMPLE
    irm https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install.ps1 | iex

.NOTES
    Platform : Windows 10/11
    Runtime  : Python 3.14.x
    License  : GNU General Public License v3.0
    Author   : Wilkin Barban Rosabal
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Version = "1.1.0"

$Host.UI.RawUI.WindowTitle = "PhotoDedup - Instalando..."
Clear-Host

Write-Host ""
Write-Host "  *** P H O T O D E D U P ***" -ForegroundColor Magenta
Write-Host "  ========================================" -ForegroundColor DarkCyan
Write-Host "   Instalador y Lanzador - Version $Version" -ForegroundColor Gray
Write-Host "  ========================================" -ForegroundColor DarkCyan
Write-Host ""

function Show-Step {
    param([string]$Message)
    Write-Host "  >> $Message..." -ForegroundColor Gray
}

function Show-Error {
    param(
        [string]$Title,
        [string]$Detail,
        [string]$Action
    )
    Write-Host ""
    Write-Host "  [ERROR] $Title" -ForegroundColor Red
    Write-Host "  --------------------------------------------------------" -ForegroundColor Red
    Write-Host "   Detalle : $Detail" -ForegroundColor Yellow
    Write-Host "   Accion  : $Action" -ForegroundColor Cyan
    Write-Host "  --------------------------------------------------------" -ForegroundColor Red
    Write-Host ""
    Read-Host "  Presione Enter para salir..."
    exit 1
}

function Run-WithProgress {
    param(
        [string]$FileName,
        [string]$Arguments,
        [string]$Message
    )

    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = $FileName
    $pinfo.Arguments = $Arguments
    $pinfo.RedirectStandardOutput = $true
    $pinfo.RedirectStandardError = $true
    $pinfo.UseShellExecute = $false
    $pinfo.CreateNoWindow = $true

    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $pinfo

    $stdoutList = New-Object System.Collections.Generic.List[string]
    $stderrList = New-Object System.Collections.Generic.List[string]
    $p.EnableRaisingEvents = $true

    $outEvent = Register-ObjectEvent -InputObject $p -EventName "OutputDataReceived" -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.Add($EventArgs.Data)
            $script:LastRawLine = $EventArgs.Data
        }
    } -MessageData $stdoutList

    $errEvent = Register-ObjectEvent -InputObject $p -EventName "ErrorDataReceived" -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.Add($EventArgs.Data)
        }
    } -MessageData $stderrList

    try {
        $script:LastRawLine = ""
        $p.Start() | Out-Null
        $p.BeginOutputReadLine()
        $p.BeginErrorReadLine()
    }
    catch {
        return @{ Success = $false; Error = $_.Exception.Message }
    }

    $spinner = @('|', '/', '-', '\')
    $i = 0
    while (-not $p.HasExited) {
        $displayMessage = $Message
        $lastLine = $script:LastRawLine
        if ($lastLine) {
            if ($lastLine -match 'Downloading\s+([a-zA-Z0-9_\-\.]+)') {
                $displayMessage = "Descargando $($Matches[1])"
            }
            elseif ($lastLine -match 'Installing collected packages:\s*(.*)') {
                $displayMessage = "Instalando paquetes"
            }
            elseif ($lastLine -match 'Requirement already satisfied:\s*([a-zA-Z0-9_\-\.\:\(\)\ ]+)') {
                $matched = $Matches[1]
                if ($matched -match '^([a-zA-Z0-9_\-]+)') {
                    $displayMessage = "Verificando $($Matches[1])"
                }
            }
        }

        if ($displayMessage.Length -gt 50) {
            $displayMessage = $displayMessage.Substring(0, 47) + "..."
        }

        Write-Host -NoNewline "`r  $($spinner[$i]) $displayMessage..." -ForegroundColor Cyan
        Start-Sleep -Milliseconds 100
        $i = ($i + 1) % $spinner.Count
    }

    Unregister-Event -SourceIdentifier $outEvent.Name -ErrorAction SilentlyContinue
    Unregister-Event -SourceIdentifier $errEvent.Name -ErrorAction SilentlyContinue

    $stdout = $stdoutList -join "`n"
    $stderr = $stderrList -join "`n"
    $exitCode = $p.ExitCode

    Write-Host -NoNewline "`r                                                                              `r"
    if ($exitCode -eq 0) {
        Write-Host "  [OK] $Message [Completado]" -ForegroundColor Green
        return @{ Success = $true; Stdout = $stdout }
    }

    Write-Host "  [FAIL] $Message [Fallo]" -ForegroundColor Red
    return @{ Success = $false; Stdout = $stdout; Stderr = $stderr; ExitCode = $exitCode }
}

function Test-Python314Command {
    param([string]$CommandLine)

    try {
        $parts = $CommandLine -split " "
        $cmd = $parts[0]
        $argList = @()
        if ($parts.Length -gt 1) {
            $argList = $parts[1..($parts.Length - 1)]
        }

        $res = & $cmd @argList --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $res -match 'Python\s+([0-9\.]+)') {
            $ver = [version]$Matches[1]
            return ($ver -ge [version]"3.14" -and $ver -lt [version]"3.15")
        }
    }
    catch { }

    return $false
}

function Get-Python314Command {
    $candidates = @("python", "py -3.14")
    foreach ($candidate in $candidates) {
        if (Test-Python314Command $candidate) {
            return $candidate
        }
    }

    return $null
}

$ScriptRootCandidates = @(
    $PSScriptRoot,
    $(if (-not [string]::IsNullOrWhiteSpace($PSCommandPath)) { Split-Path -Parent $PSCommandPath }),
    (Get-Location).Path,
    '.'
)

$ScriptRoot = $null
foreach ($candidate in $ScriptRootCandidates) {
    if (-not [string]::IsNullOrWhiteSpace($candidate)) {
        $ScriptRoot = $candidate.Trim()
        break
    }
}

if ([string]::IsNullOrWhiteSpace($ScriptRoot)) {
    Show-Error "Error de Directorio" "No se pudo determinar el directorio de trabajo." "Ejecute el instalador desde un directorio con permisos de lectura y escritura."
}

$RequiredFiles = @('src\main\photo_dedup.py', 'requirements.txt')
$IsProjectRoot = $true
foreach ($file in $RequiredFiles) {
    if (-not (Test-Path (Join-Path $ScriptRoot $file))) {
        $IsProjectRoot = $false
        break
    }
}

if (-not $IsProjectRoot) {
    Write-Host "  [!] Archivos de proyecto no encontrados en el directorio actual." -ForegroundColor Yellow
    Write-Host "  [INFO] Entrando a modo Bootstrapper remoto: descargando repositorio..." -ForegroundColor Cyan

    $RepoOwner = 'wilkinbarban'
    $RepoName = 'photo-dedup'
    $Branch = 'main'
    $ArchiveUrl = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"
    $DesktopDir = [Environment]::GetFolderPath('Desktop')
    if ([string]::IsNullOrWhiteSpace($DesktopDir)) {
        $DesktopDir = Join-Path $HOME 'Desktop'
    }
    $InstallDir = if ($env:PHOTO_DEDUP_INSTALL_DIR) { $env:PHOTO_DEDUP_INSTALL_DIR } else { Join-Path $DesktopDir $RepoName }
    $TempZip = Join-Path $env:TEMP "$RepoName-$Branch.zip"
    $TempExtract = Join-Path $env:TEMP "$RepoName-bootstrap-$(Get-Random)"

    $dlArgs = "-NoProfile -Command `"Invoke-WebRequest -Uri '$ArchiveUrl' -OutFile '$TempZip' -UseBasicParsing`""
    $dlRes = Run-WithProgress "powershell" $dlArgs "Descargando repositorio de GitHub"
    if (-not $dlRes.Success) {
        Show-Error "Fallo de Descarga" "No se pudo descargar el repositorio desde GitHub." "Verifique su conexion a Internet y que github.com sea accesible."
    }

    $zipSize = (Get-Item $TempZip).Length
    if ($zipSize -lt 1024) {
        Remove-Item -Force $TempZip -ErrorAction SilentlyContinue
        Show-Error "Integridad Invalida" "El archivo descargado es invalido o corrupto." "Vuelva a intentar la ejecucion."
    }

    $null = New-Item -ItemType Directory -Path $TempExtract -Force
    $extArgs = "-NoProfile -Command `"Expand-Archive -Path '$TempZip' -DestinationPath '$TempExtract' -Force`""
    $extRes = Run-WithProgress "powershell" $extArgs "Extrayendo repositorio"
    Remove-Item -Force $TempZip -ErrorAction SilentlyContinue

    if (-not $extRes.Success) {
        Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue
        Show-Error "Extraccion Fallida" "No se pudo descomprimir el archivo del repositorio." "Asegurese de contar con espacio en disco."
    }

    $ExtractedRoot = Join-Path $TempExtract "$RepoName-$Branch"
    if (-not (Test-Path $ExtractedRoot)) {
        Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue
        Show-Error "Estructura Invalida" "La carpeta esperada tras la extraccion no existe." "Vuelva a intentar la ejecucion."
    }

    Show-Step "Instalando archivos del repositorio"
    if (Test-Path $InstallDir) {
        Write-Host "  [!] Carpeta destino existente. Actualizando archivos en-lugar..." -ForegroundColor Yellow
        Get-ChildItem -Path $ExtractedRoot | Where-Object { $_.Name -ne '.venv' } | ForEach-Object {
            $dest = Join-Path $InstallDir $_.Name
            Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
        }
    }
    else {
        Move-Item -Path $ExtractedRoot -Destination $InstallDir
    }

    Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue

    $LocalInstaller = Join-Path $InstallDir 'install.ps1'
    if (-not (Test-Path $LocalInstaller)) {
        Show-Error "Script Faltante" "El script install.ps1 no se encontro en el directorio instalado." "Reporte este error al autor del proyecto."
    }

    Write-Host "  [OK] Repositorio instalado con exito." -ForegroundColor Green
    Write-Host "  [INFO] Delegando arranque al instalador local..." -ForegroundColor Cyan
    Set-Location $InstallDir
    & $LocalInstaller
    exit $LASTEXITCODE
}

Show-Step "Verificando entorno de Python 3.14"
$pythonCmd = Get-Python314Command

if (-not $pythonCmd) {
    Write-Host "  [!] Python 3.14.x no detectado en el sistema." -ForegroundColor Yellow

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Show-Error "Python No Encontrado" "No se encontro Python 3.14.x ni winget." "Instale manualmente Python 3.14 desde https://www.python.org/downloads/ y agreguelo al PATH."
    }

    $installRes = Run-WithProgress "winget" "install --id Python.Python.3.14 --accept-source-agreements --accept-package-agreements" "Instalando Python 3.14"
    if (-not $installRes.Success) {
        Show-Error "Instalacion de Python Fallida" "Fallo al instalar Python 3.14 mediante winget." "Instale Python 3.14 manualmente desde el sitio web de Python."
    }

    $env:PATH = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('PATH', 'User')
    $pythonCmd = Get-Python314Command
    if (-not $pythonCmd) {
        Show-Error "Reinicio de Consola Requerido" "Python fue instalado, pero la terminal actual aun no reconoce el comando." "Cierre todas las consolas abiertas y vuelva a ejecutar install.ps1."
    }
}

Write-Host "  [OK] Python base detectado ($pythonCmd)" -ForegroundColor Green

$venvDir = Join-Path $ScriptRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$venvPip = Join-Path $venvDir 'Scripts\pip.exe'
$recreateVenv = $false

if (Test-Path $venvPython) {
    try {
        $res = & $venvPython --version 2>&1
        if ($res -match 'Python\s+([0-9\.]+)') {
            $ver = [version]$Matches[1]
            if ($ver -lt [version]"3.14" -or $ver -ge [version]"3.15") {
                $recreateVenv = $true
            }
        }
        else {
            $recreateVenv = $true
        }
    }
    catch {
        $recreateVenv = $true
    }
}

if ($recreateVenv) {
    Write-Host "  [!] Entorno virtual incompatible detectado. Recreando .venv..." -ForegroundColor Yellow
    Remove-Item -Path $venvDir -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $venvPython)) {
    $parts = $pythonCmd -split " "
    $cmd = $parts[0]
    $venvArgs = if ($parts.Length -gt 1) { "$($parts[1]) -m venv `"$venvDir`"" } else { "-m venv `"$venvDir`"" }
    $venvRes = Run-WithProgress $cmd $venvArgs "Creando entorno virtual (.venv)"
    if (-not $venvRes.Success) {
        Show-Error "Error de Entorno Virtual" "No se pudo crear la carpeta .venv." "Verifique permisos de escritura o ejecute: python -m venv .venv"
    }
}
else {
    Write-Host "  [OK] Entorno virtual detectado (.venv)" -ForegroundColor Green
}

Show-Step "Comprobando dependencias del sistema"
$env:PIP_USER = "no"

$pipUpgrade = Run-WithProgress $venvPython "-m pip install --no-input --upgrade pip" "Actualizando instalador pip"
if (-not $pipUpgrade.Success) {
    Show-Error "Error de pip" "No se pudo actualizar pip dentro del entorno virtual." "Revise la conexion o ejecute manualmente: .venv\Scripts\python.exe -m pip install --upgrade pip"
}

$ReqPath = Join-Path $ScriptRoot "requirements.txt"
if (-not (Test-Path $ReqPath)) {
    Show-Error "Dependencias No Encontradas" "requirements.txt no existe en el proyecto instalado." "Verifique que el repositorio se haya descargado completo."
}

$depsRes = Run-WithProgress $venvPip "install --no-input -r `"$ReqPath`"" "Instalando dependencias de Python"
if (-not $depsRes.Success) {
    $logFile = Join-Path $venvDir "install.log"
    ($depsRes.Stdout + "`n" + $depsRes.Stderr) | Out-File -FilePath $logFile -Encoding utf8
    Show-Error "Error en Dependencias" "Fallo al instalar paquetes de requirements.txt." "Consulte el log: $logFile`nIntente manualmente: .venv\Scripts\pip.exe install -r requirements.txt"
}

Write-Host ""
Write-Host "  >>> Iniciando PhotoDedup..." -ForegroundColor Magenta
Write-Host ""

try {
    $proc = Start-Process -FilePath $venvPython -ArgumentList "-m src.main.photo_dedup" -NoNewWindow -PassThru -Wait
    $exitCode = $proc.ExitCode
    if ($exitCode -ne 0) {
        Show-Error "Ejecucion Fallida" "La aplicacion finalizo con codigo de error ($exitCode)." "Consulte los mensajes anteriores o los logs de la aplicacion."
    }
}
catch {
    Show-Error "Fallo Critico al Iniciar" $_.Exception.Message "Compruebe que .venv no este danado y vuelva a ejecutar install.ps1."
}
