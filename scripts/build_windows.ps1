[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Version = "",

    [Parameter(Mandatory = $false)]
    [switch]$Clean
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

Push-Location $repoRoot
try {
    if ($Clean) {
        if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }
        if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }
    }

    if ([string]::IsNullOrWhiteSpace($Version)) {
        $versionLine = Select-String -Path "src/main/photo_dedup.py" -Pattern '^__version__\s*=\s*"([^"]+)"' | Select-Object -First 1
        if (-not $versionLine) {
            throw "Could not determine version from src/main/photo_dedup.py. Pass -Version explicitly."
        }

        $Version = $versionLine.Matches[0].Groups[1].Value
    }

    Write-Host "[INFO] Building PhotoDedup version: $Version"
    python -m PyInstaller --noconfirm --clean "PhotoDedup.spec"

    $distExePath = Join-Path $repoRoot "dist\PhotoDedup.exe"
    if (-not (Test-Path $distExePath)) {
        throw "Build output executable not found: $distExePath"
    }

    $zipName = "PhotoDedup-$Version-windows.zip"
    $zipPath = Join-Path $repoRoot ("dist\" + $zipName)

    if (Test-Path $zipPath) {
        Remove-Item -Path $zipPath -Force
    }

    Compress-Archive -Path $distExePath -DestinationPath $zipPath -Force
    Write-Host "[OK] Build completed. Artifact: $zipPath"
}
finally {
    Pop-Location
}
