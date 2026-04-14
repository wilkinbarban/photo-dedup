#Requires -Version 5.1
<#+
.SYNOPSIS
    Photo Dedup - One-click installer and launcher for Windows.

.DESCRIPTION
    Validates Python (>=3.8, <3.14; prefers 3.11), creates or reuses
    a local .venv, installs dependencies, and launches Photo Dedup.

    If executed outside the project root (for example from a remote
    invocation context), the script enters bootstrap mode:
    downloads the repository ZIP, installs/updates on Desktop, and
    delegates to the local install.ps1.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Write-Step  { param([string]$Msg) Write-Host "[....] $Msg" -ForegroundColor Cyan }
function Write-Ok    { param([string]$Msg) Write-Host "[ OK ] $Msg" -ForegroundColor Green }
function Write-Warn  { param([string]$Msg) Write-Host "[WARN] $Msg" -ForegroundColor Yellow }
function Write-Fail  { param([string]$Msg) Write-Host "[FAIL] $Msg" -ForegroundColor Red }
function Write-Info  { param([string]$Msg) Write-Host "[INFO] $Msg" -ForegroundColor Gray }

# Resolve a safe base path for file operations. In irm|iex flows,
# PSScriptRoot/PSCommandPath may be empty.
$scriptRootCandidates = @(
    $PSScriptRoot,
    $(if (-not [string]::IsNullOrWhiteSpace($PSCommandPath)) { Split-Path -Parent $PSCommandPath }),
    (Get-Location).Path,
    '.'
)

$scriptRoot = $null
foreach ($candidate in $scriptRootCandidates) {
    if (-not [string]::IsNullOrWhiteSpace($candidate)) {
        $scriptRoot = $candidate.Trim()
        break
    }
}

if ([string]::IsNullOrWhiteSpace($scriptRoot)) {
    Write-Fail "Unable to resolve a valid working directory."
    exit 1
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  Photo Dedup - Installer / Launcher (Windows)" -ForegroundColor Cyan
Write-Host "  Educational project - GPL-3.0 License" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# Bootstrap mode if this script is not running from project root.
$requiredFiles = @('src\main\photo_dedup.py', 'requirements.txt')
$isProjectRoot = $true
foreach ($file in $requiredFiles) {
    if (-not (Test-Path (Join-Path $scriptRoot $file))) {
        $isProjectRoot = $false
        break
    }
}

if (-not $isProjectRoot) {
    Write-Warn "Project files were not found next to install.ps1."
    Write-Info "Switching to bootstrap mode: downloading repository from GitHub..."

    $repoOwner = 'wilkinbarban'
    $repoName = 'photo-dedup'
    $branch = 'main'
    $archiveUrl = "https://github.com/$repoOwner/$repoName/archive/refs/heads/$branch.zip"
    $desktopDir = [Environment]::GetFolderPath('Desktop')
    if ([string]::IsNullOrWhiteSpace($desktopDir)) {
        $desktopDir = Join-Path $HOME 'Desktop'
    }
    $installDir = if ($env:PHOTO_DEDUP_INSTALL_DIR) { $env:PHOTO_DEDUP_INSTALL_DIR } else { Join-Path $desktopDir $repoName }
    $tempZip = Join-Path $env:TEMP "$repoName-$branch.zip"
    $tempExtract = Join-Path $env:TEMP "$repoName-bootstrap-$(Get-Random)"

    Write-Step "Downloading repository archive..."
    Invoke-WebRequest -Uri $archiveUrl -OutFile $tempZip -UseBasicParsing

    $zipSize = (Get-Item $tempZip).Length
    if ($zipSize -lt 1024) {
        Write-Fail "Downloaded archive appears invalid (size: $zipSize bytes)."
        Remove-Item -Force $tempZip -ErrorAction SilentlyContinue
        exit 1
    }

    Write-Step "Extracting repository archive..."
    $null = New-Item -ItemType Directory -Path $tempExtract -Force
    Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
    Remove-Item -Force $tempZip -ErrorAction SilentlyContinue

    $extractedRoot = Join-Path $tempExtract "$repoName-$branch"
    if (-not (Test-Path $extractedRoot)) {
        Write-Fail "Expected folder '$extractedRoot' not found after extraction."
        Remove-Item -Recurse -Force $tempExtract -ErrorAction SilentlyContinue
        exit 1
    }

    Write-Step "Installing repository to: $installDir"
    if (Test-Path $installDir) {
        Write-Warn "Target already exists. Updating in-place (existing .venv preserved)."
        Get-ChildItem -Path $extractedRoot | Where-Object { $_.Name -ne '.venv' } | ForEach-Object {
            $dest = Join-Path $installDir $_.Name
            Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
        }
    }
    else {
        Move-Item -Path $extractedRoot -Destination $installDir
    }

    Remove-Item -Recurse -Force $tempExtract -ErrorAction SilentlyContinue

    $localInstaller = Join-Path $installDir 'install.ps1'
    if (-not (Test-Path $localInstaller)) {
        Write-Fail "install.ps1 not found in $installDir after bootstrap."
        exit 1
    }

    Write-Ok "Repository ready. Delegating to local installer..."
    Set-Location $installDir
    & $localInstaller
    exit $LASTEXITCODE
}

Write-Step "Locating compatible Python runtime (>=3.8, <3.14; prefer 3.11)..."

$pythonCmd = $null
try {
    $null = & py -3.11 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = @('py', '-3.11')
        Write-Ok "Python 3.11 found via py launcher."
    }
}
catch { }

if (-not $pythonCmd) {
    try {
        $null = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $null = & python -c "import sys; raise SystemExit(0 if (3,8) <= sys.version_info < (3,14) else 1)" 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = @('python')
                Write-Ok "Compatible Python found in PATH."
            }
            else {
                Write-Warn "Python in PATH is outside supported range (>=3.8, <3.14)."
            }
        }
    }
    catch { }
}

if (-not $pythonCmd) {
    Write-Info "No compatible Python found. Attempting automatic install via winget..."
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Fail "winget is not available. Install Python 3.11 manually from https://www.python.org/downloads/."
        exit 1
    }

    & winget install --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "winget installation failed. Please install Python 3.11 manually."
        exit 1
    }

    $env:PATH = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine') + ';' +
                [System.Environment]::GetEnvironmentVariable('PATH', 'User')

    try {
        $null = & py -3.11 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = @('py', '-3.11')
            Write-Ok "Python 3.11 installed and ready."
        }
    }
    catch { }

    if (-not $pythonCmd) {
        Write-Warn "Python was installed but is not yet visible in this session."
        Write-Info "Close this terminal and run install.ps1 again."
        exit 1
    }
}

Write-Host ""
Write-Step "Setting up virtual environment (.venv)..."

$venvDir = Join-Path $scriptRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$venvPip = Join-Path $venvDir 'Scripts\pip.exe'

if (Test-Path $venvPython) {
    $null = & $venvPython -c "import sys; raise SystemExit(0 if (3,8) <= sys.version_info < (3,14) else 1)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "Existing .venv uses an incompatible Python version. Recreating..."
        Remove-Item -Recurse -Force $venvDir
    }
}

if (-not (Test-Path $venvPython)) {
    Write-Info "Creating isolated virtual environment..."
    if ($pythonCmd.Count -gt 1) {
        & $pythonCmd[0] $pythonCmd[1] -m venv $venvDir
    }
    else {
        & $pythonCmd[0] -m venv $venvDir
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Failed to create virtual environment."
        exit 1
    }
    Write-Ok "Virtual environment created."
}
else {
    Write-Ok "Virtual environment already exists."
}

Write-Host ""
Write-Step "Installing dependencies..."

& $venvPython -m pip install --upgrade pip --quiet
& $venvPip install -r (Join-Path $scriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Dependency installation failed. Check output above."
    exit 1
}
Write-Ok "All dependencies are up to date."

Write-Host ""
Write-Ok "Launching Photo Dedup..."
Write-Host ""

& $venvPython -m src.main.photo_dedup

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Fail "Application exited unexpectedly (exit code $LASTEXITCODE)."
    exit $LASTEXITCODE
}