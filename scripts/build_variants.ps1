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

    $variantResults = @()
    $variants = @("full", "lite")

    for ($index = 0; $index -lt $variants.Count; $index++) {
        $variant = $variants[$index]
        Write-Host "[INFO] Building variant: $variant"
        $env:PHOTO_DEDUP_BUILD_FLAVOR = $variant

        $variantVersion = "$Version-$variant"
        $useClean = $index -eq 0
        & $buildScript -Version $variantVersion -Clean:$useClean -SmokeTest:$SmokeTest -SmokeTimeoutSeconds $SmokeTimeoutSeconds

        $exePath = Join-Path $repoRoot "dist\PhotoDedup.exe"
        if (-not (Test-Path $exePath)) {
            throw "Expected EXE not found after $variant build: $exePath"
        }

        $variantExePath = Join-Path $repoRoot ("dist\PhotoDedup-" + $variant + ".exe")
        Copy-Item -Path $exePath -Destination $variantExePath -Force

        $metricsPath = Join-Path $repoRoot ("dist\build-metrics-" + $variantVersion + ".json")
        if (-not (Test-Path $metricsPath)) {
            throw "Expected metrics not found: $metricsPath"
        }

        $metrics = Get-Content $metricsPath -Raw | ConvertFrom-Json
        $variantResults += [ordered]@{
            variant = $variant
            exe = (Split-Path -Leaf $variantExePath)
            zip = ("PhotoDedup-" + $variantVersion + "-windows.zip")
            exe_size_bytes = $metrics.exe_size_bytes
            zip_size_bytes = $metrics.zip_size_bytes
            smoke_test = $metrics.smoke_test
            smoke_elapsed_ms = $metrics.smoke_elapsed_ms
        }
    }

    Remove-Item Env:PHOTO_DEDUP_BUILD_FLAVOR -ErrorAction SilentlyContinue

    $full = $variantResults | Where-Object { $_.variant -eq "full" } | Select-Object -First 1
    $lite = $variantResults | Where-Object { $_.variant -eq "lite" } | Select-Object -First 1

    $summary = [ordered]@{
        version = $Version
        generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
        variants = $variantResults
        deltas_lite_vs_full = [ordered]@{
            exe_bytes = ($lite.exe_size_bytes - $full.exe_size_bytes)
            zip_bytes = ($lite.zip_size_bytes - $full.zip_size_bytes)
            exe_percent = [math]::Round((($lite.exe_size_bytes - $full.exe_size_bytes) * 100.0) / [double]$full.exe_size_bytes, 2)
            zip_percent = [math]::Round((($lite.zip_size_bytes - $full.zip_size_bytes) * 100.0) / [double]$full.zip_size_bytes, 2)
        }
    }

    $summaryPath = Join-Path $repoRoot ("dist\build-variants-" + $Version + ".json")
    $summary | ConvertTo-Json -Depth 6 | Set-Content -Path $summaryPath -Encoding UTF8

    Write-Host "[OK] Variant build automation complete."
    Write-Host "[INFO] Summary written to: $summaryPath"
}
finally {
    Remove-Item Env:PHOTO_DEDUP_BUILD_FLAVOR -ErrorAction SilentlyContinue
    Pop-Location
}
