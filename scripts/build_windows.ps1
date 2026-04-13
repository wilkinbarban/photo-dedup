[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Version = "",

    [Parameter(Mandatory = $false)]
    [switch]$Clean,

    [Parameter(Mandatory = $false)]
    [switch]$SmokeTest,

    [Parameter(Mandatory = $false)]
    [ValidateRange(3, 120)]
    [int]$SmokeTimeoutSeconds = 12,

    [Parameter(Mandatory = $false)]
    [string]$MetricsOut = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

Push-Location $repoRoot
try {
    if ($Clean) {
        if (Test-Path "build") {
            Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
        }

        if (Test-Path "dist") {
            $removed = $false
            for ($attempt = 1; $attempt -le 5; $attempt++) {
                try {
                    Remove-Item -Path "dist" -Recurse -Force -ErrorAction Stop
                    $removed = $true
                    break
                }
                catch {
                    if ($attempt -eq 5) {
                        throw
                    }
                    Start-Sleep -Milliseconds 500
                }
            }

            if (-not $removed -and (Test-Path "dist")) {
                throw "Could not remove dist directory after multiple attempts."
            }
        }
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

    $exeSizeBytes = (Get-Item $distExePath).Length
    $zipSizeBytes = (Get-Item $zipPath).Length

    $smokeResult = "not_run"
    $smokeElapsedMs = 0
    $smokeExitCode = $null

    if ($SmokeTest) {
        Write-Host "[INFO] Running smoke test ($SmokeTimeoutSeconds s timeout)..."

        $attemptPassed = $false
        for ($attempt = 1; $attempt -le 2; $attempt++) {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            $proc = Start-Process -FilePath $distExePath -PassThru
            try {
                Wait-Process -Id $proc.Id -Timeout $SmokeTimeoutSeconds -ErrorAction Stop
                $smokeResult = "exited_early"
                if ($proc.HasExited) {
                    $smokeExitCode = $proc.ExitCode
                }
            }
            catch [System.TimeoutException] {
                $smokeResult = "running_after_timeout"
                $attemptPassed = $true
            }
            finally {
                if (-not $proc.HasExited) {
                    Stop-Process -Id $proc.Id -Force
                }
                $sw.Stop()
                $smokeElapsedMs = $sw.ElapsedMilliseconds
            }

            if ($attemptPassed) {
                break
            }

            if ($attempt -lt 2) {
                Write-Host "[WARN] Smoke attempt $attempt exited early (ExitCode=$smokeExitCode). Retrying once..."
                Start-Sleep -Milliseconds 750
            }
        }

        if (-not $attemptPassed) {
            throw "Smoke test failed: executable exited before $SmokeTimeoutSeconds seconds on both attempts. ExitCode=$smokeExitCode"
        }

        Write-Host "[OK] Smoke test passed. Result=$smokeResult ElapsedMs=$smokeElapsedMs"
    }

    $metrics = [ordered]@{
        version = $Version
        exe_size_bytes = $exeSizeBytes
        zip_size_bytes = $zipSizeBytes
        smoke_test = $smokeResult
        smoke_elapsed_ms = $smokeElapsedMs
        smoke_exit_code = $smokeExitCode
        built_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    }

    if ([string]::IsNullOrWhiteSpace($MetricsOut)) {
        $MetricsOut = Join-Path $repoRoot ("dist\build-metrics-" + $Version + ".json")
    }

    $metrics | ConvertTo-Json -Depth 4 | Set-Content -Path $MetricsOut -Encoding UTF8

    Write-Host "[OK] Build completed. Artifact: $zipPath"
    Write-Host "[INFO] Metrics written to: $MetricsOut"
    Write-Host "[INFO] EXE size: $exeSizeBytes bytes"
    Write-Host "[INFO] ZIP size: $zipSizeBytes bytes"
}
finally {
    Pop-Location
}
