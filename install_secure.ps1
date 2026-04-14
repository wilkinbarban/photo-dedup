#Requires -Version 5.1
<#+
.SYNOPSIS
    Photo Dedup - Secure remote installer for Windows.

.DESCRIPTION
    Downloads Photo Dedup from GitHub over HTTPS, validates basic archive
    integrity, installs/updates local files, then delegates to local
    install.ps1 for environment setup and app launch.

    One-click use:
    irm https://raw.githubusercontent.com/wilkinbarban/photo-dedup/main/install_secure.ps1 | iex
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Write-Step { param([string]$Msg) Write-Host "[....] $Msg" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Msg) Write-Host "[ OK ] $Msg" -ForegroundColor Green }
function Write-Warn { param([string]$Msg) Write-Host "[WARN] $Msg" -ForegroundColor Yellow }
function Write-Fail { param([string]$Msg) Write-Host "[FAIL] $Msg" -ForegroundColor Red }
function Write-Info { param([string]$Msg) Write-Host "[INFO] $Msg" -ForegroundColor Gray }

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  Photo Dedup - Secure Remote Installer" -ForegroundColor Cyan
Write-Host "  Educational project - GPL-3.0 License" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

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
$tempExtract = Join-Path $env:TEMP "$repoName-extract-$(Get-Random)"

Write-Step "Downloading repository from GitHub..."
Write-Info "Source : $archiveUrl"
Write-Info "Target : $installDir"
Write-Host ""

try {
    Invoke-WebRequest -Uri $archiveUrl -OutFile $tempZip -UseBasicParsing
}
catch {
    Write-Fail "Download failed: $_"
    Write-Info "Check your internet connection and that github.com is reachable."
    exit 1
}

$zipSize = (Get-Item $tempZip).Length
if ($zipSize -lt 1024) {
    Write-Fail "Downloaded archive appears invalid (size: $zipSize bytes). Aborting."
    Remove-Item -Force $tempZip -ErrorAction SilentlyContinue
    exit 1
}
Write-Ok "Archive downloaded ($([math]::Round($zipSize / 1KB, 1)) KB)."

Write-Step "Extracting archive..."
$null = New-Item -ItemType Directory -Path $tempExtract -Force
Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
Remove-Item -Force $tempZip -ErrorAction SilentlyContinue

$extractedRoot = Join-Path $tempExtract "$repoName-$branch"
if (-not (Test-Path $extractedRoot)) {
    Write-Fail "Expected folder '$extractedRoot' not found after extraction."
    Remove-Item -Recurse -Force $tempExtract -ErrorAction SilentlyContinue
    exit 1
}
Write-Ok "Extracted successfully."

Write-Step "Installing to: $installDir"
if (Test-Path $installDir) {
    Write-Warn "Directory already exists. Updating in-place (existing .venv preserved)."
    Get-ChildItem -Path $extractedRoot | Where-Object { $_.Name -ne '.venv' } | ForEach-Object {
        $dest = Join-Path $installDir $_.Name
        Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
    }
}
else {
    Move-Item -Path $extractedRoot -Destination $installDir
}

Remove-Item -Recurse -Force $tempExtract -ErrorAction SilentlyContinue
Write-Ok "Files installed."

Write-Host ""
Write-Step "Running installer from local copy..."
$localInstaller = Join-Path $installDir 'install.ps1'

if (-not (Test-Path $localInstaller)) {
    Write-Fail "install.ps1 not found in $installDir. Repository may be incomplete."
    exit 1
}

Set-Location $installDir
& $localInstaller
exit $LASTEXITCODE
