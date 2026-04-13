[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Version = "",

    [Parameter(Mandatory = $false)]
    [switch]$Clean,

    [Parameter(Mandatory = $false)]
    [string]$DistPath = "dist",

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

        if (Test-Path $DistPath) {
            $removed = $false
            for ($attempt = 1; $attempt -le 5; $attempt++) {
                try {
                    Remove-Item -Path $DistPath -Recurse -Force -ErrorAction Stop
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

            if (-not $removed -and (Test-Path $DistPath)) {
                throw "Could not remove $DistPath directory after multiple attempts."
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

    Write-Host "[INFO] Building PhotoDedup version: $Version (distpath: $DistPath)"
    python -m PyInstaller --noconfirm --clean --distpath "$DistPath" "PhotoDedup.spec"

    $distExePath = Join-Path $repoRoot "$DistPath\PhotoDedup.exe"
    if (-not (Test-Path $distExePath)) {
        throw "Build output executable not found: $distExePath"
    }

    $exeSizeBytes = (Get-Item $distExePath).Length

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
        dist_path = $DistPath
        exe_size_bytes = $exeSizeBytes
        smoke_test = $smokeResult
        smoke_elapsed_ms = $smokeElapsedMs
        smoke_exit_code = $smokeExitCode
        built_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    }

    if ([string]::IsNullOrWhiteSpace($MetricsOut)) {
        $MetricsOut = Join-Path $repoRoot ("$DistPath\build-metrics-" + $Version + ".json")
    }

    $metrics | ConvertTo-Json -Depth 4 | Set-Content -Path $MetricsOut -Encoding UTF8

    Write-Host "[OK] Build completed. EXE: $distExePath"
    Write-Host "[INFO] Metrics written to: $MetricsOut"
    Write-Host "[INFO] EXE size: $exeSizeBytes bytes"
}
finally {
    Pop-Location
}
