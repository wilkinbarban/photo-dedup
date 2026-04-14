[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Version = "",

    [Parameter(Mandatory = $false)]
    [switch]$SmokeTest,

    [Parameter(Mandatory = $false)]
    [ValidateRange(3, 120)]
    [int]$SmokeTimeoutSeconds = 12
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
$buildScript = Join-Path $scriptRoot "build_windows.ps1"

Push-Location $repoRoot
try {
    if ([string]::IsNullOrWhiteSpace($Version)) {
        $versionLine = Select-String -Path "src/main/photo_dedup.py" -Pattern '^__version__\s*=\s*"([^"]+)"' | Select-Object -First 1
        if (-not $versionLine) {
            throw "Could not determine version from src/main/photo_dedup.py. Pass -Version explicitly."
        }
        $Version = $versionLine.Matches[0].Groups[1].Value
    }

    $variants = @("full", "lite")

    # Ensure dist/ output folder exists for final renamed EXE files
    $distOut = Join-Path $repoRoot "dist"
    if (-not (Test-Path $distOut)) {
        New-Item -ItemType Directory -Path $distOut | Out-Null
    }

    foreach ($variant in $variants) {
        Write-Host "[INFO] Building variant: $variant"
        $env:PHOTO_DEDUP_BUILD_FLAVOR = $variant

        $variantVersion = "$Version-$variant"
        # Each variant builds into its own directory to avoid file-lock conflicts
        $variantDistPath = "dist-$variant"
        & $buildScript -Version $variantVersion -Clean -DistPath $variantDistPath -SmokeTest:$SmokeTest -SmokeTimeoutSeconds $SmokeTimeoutSeconds

        $exePath = Join-Path $repoRoot "$variantDistPath\PhotoDedup.exe"
        if (-not (Test-Path $exePath)) {
            throw "Expected EXE not found after $variant build: $exePath"
        }

        $variantExePath = Join-Path $repoRoot "dist\PhotoDedup-$variant.exe"
        Copy-Item -Path $exePath -Destination $variantExePath -Force

        $metricsPath = Join-Path $repoRoot "$variantDistPath\build-metrics-$variantVersion.json"
        if (-not (Test-Path $metricsPath)) {
            throw "Expected metrics not found: $metricsPath"
        }

        $metrics = Get-Content $metricsPath -Raw | ConvertFrom-Json
        Write-Host "[INFO] PhotoDedup-$variant.exe size: $($metrics.exe_size_bytes) bytes"
    }

    Remove-Item Env:PHOTO_DEDUP_BUILD_FLAVOR -ErrorAction SilentlyContinue

    Write-Host "[OK] Variant build automation complete."
}
finally {
    Remove-Item Env:PHOTO_DEDUP_BUILD_FLAVOR -ErrorAction SilentlyContinue
    Pop-Location
}
