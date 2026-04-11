[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$RepoZipUrl = "https://github.com/wilkinbarban/photo-dedup/archive/refs/heads/main.zip",

    [Parameter(Mandatory = $false)]
    [string]$InstallFolderName = "photo-dedup-main",

    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 10)]
    [int]$MaxRetries = 3,

    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 30)]
    [int]$RetryDelaySeconds = 3,

    [Parameter(Mandatory = $false)]
    [string]$ExpectedZipSha256 = "",

    [Parameter(Mandatory = $false)]
    [switch]$SkipHashCheck
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$desktopPath = [Environment]::GetFolderPath("DesktopDirectory")
if ([string]::IsNullOrWhiteSpace($desktopPath)) {
    $desktopPath = Join-Path $env:USERPROFILE "Desktop"
}
$desktopTarget = Join-Path $desktopPath $InstallFolderName
$tempRoot = Join-Path $env:TEMP ("photo-dedup-install-" + [Guid]::NewGuid().ToString("N"))
$zipPath = Join-Path $tempRoot "photo-dedup.zip"
$extractPath = Join-Path $tempRoot "extract"

$allowedHosts = @("github.com", "raw.githubusercontent.com", "codeload.github.com")

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message"
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Test-InternetConnection {
    param([string]$Url)

    try {
        Invoke-WebRequest -Uri $Url -Method Head -UseBasicParsing -TimeoutSec 15 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Download-WithRetry {
    param(
        [string]$Url,
        [string]$OutputFile,
        [int]$Retries,
        [int]$DelaySeconds
    )

    for ($attempt = 1; $attempt -le $Retries; $attempt++) {
        try {
            Write-Info "Download attempt $attempt of $Retries..."
            Invoke-WebRequest -Uri $Url -OutFile $OutputFile -UseBasicParsing -TimeoutSec 90
            return
        }
        catch {
            if (Test-Path $OutputFile) {
                Remove-Item -Path $OutputFile -Force -ErrorAction SilentlyContinue
            }

            if ($attempt -eq $Retries) {
                throw "Download failed after $Retries attempts. Last error: $($_.Exception.Message)"
            }

            Write-Warn "Download failed: $($_.Exception.Message)"
            Write-Info "Retrying in $DelaySeconds seconds..."
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}

function Test-ZipSignature {
    param([string]$FilePath)

    if (-not (Test-Path $FilePath)) {
        throw "ZIP file does not exist: $FilePath"
    }

    $fileInfo = Get-Item -Path $FilePath
    if ($fileInfo.Length -lt 4) {
        throw "Downloaded ZIP file is invalid or too small."
    }

    $stream = [System.IO.File]::OpenRead($FilePath)
    try {
        $bytes = New-Object byte[] 4
        $null = $stream.Read($bytes, 0, 4)
        $isZip = ($bytes[0] -eq 0x50 -and $bytes[1] -eq 0x4B)
        if (-not $isZip) {
            throw "Downloaded file does not appear to be a ZIP archive."
        }
    }
    finally {
        $stream.Dispose()
    }
}

function Get-Sha256 {
    param([string]$FilePath)

    return (Get-FileHash -Path $FilePath -Algorithm SHA256).Hash.ToLowerInvariant()
}

try {
    # Use modern TLS for secure HTTPS requests.
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    if (-not [string]::IsNullOrWhiteSpace($PSCommandPath) -and (Test-Path $PSCommandPath)) {
        $signature = Get-AuthenticodeSignature -FilePath $PSCommandPath
        if ($signature.Status -ne "Valid") {
            Write-Warn "This script is not Authenticode-signed or has an invalid signature."
            Write-Warn "Continue only if you trust the source repository."
        }
    }
    else {
        Write-Warn "Script signature check skipped (running from in-memory content)."
    }

    $repoUri = [Uri]$RepoZipUrl
    if ($allowedHosts -notcontains $repoUri.Host) {
        throw "Blocked download host: $($repoUri.Host)"
    }

    if (-not (Test-InternetConnection -Url "https://github.com")) {
        throw "No internet connection (or GitHub is unreachable). Check your network and try again."
    }

    New-Item -Path $tempRoot -ItemType Directory -Force | Out-Null
    New-Item -Path $extractPath -ItemType Directory -Force | Out-Null

    Write-Info "Downloading project ZIP from: $RepoZipUrl"
    Download-WithRetry -Url $RepoZipUrl -OutputFile $zipPath -Retries $MaxRetries -DelaySeconds $RetryDelaySeconds

    Write-Info "Validating downloaded file format..."
    Test-ZipSignature -FilePath $zipPath

    $downloadedHash = Get-Sha256 -FilePath $zipPath
    Write-Info "Downloaded ZIP SHA-256: $downloadedHash"

    if (-not $SkipHashCheck) {
        if ([string]::IsNullOrWhiteSpace($ExpectedZipSha256)) {
            Write-Warn "ExpectedZipSha256 was not provided. Hash was calculated but not enforced."
            Write-Warn "For stronger integrity, rerun with -ExpectedZipSha256 <hash>."
        }
        else {
            $expectedHash = $ExpectedZipSha256.Trim().ToLowerInvariant()
            if ($downloadedHash -ne $expectedHash) {
                throw "SHA-256 mismatch. Expected $expectedHash but got $downloadedHash"
            }
            Write-Info "SHA-256 hash validation passed."
        }
    }

    Write-Info "Extracting project files..."
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

    $extractedProjectFolder = Get-ChildItem -Path $extractPath -Directory | Select-Object -First 1
    if (-not $extractedProjectFolder) {
        throw "The extracted project folder could not be found."
    }

    if (-not (Test-Path $desktopPath)) {
        New-Item -Path $desktopPath -ItemType Directory -Force | Out-Null
    }

    if (Test-Path $desktopTarget) {
        Write-Info "Removing existing desktop folder: $desktopTarget"
        Remove-Item -Path $desktopTarget -Recurse -Force
    }

    Write-Info "Moving files to desktop..."
    Move-Item -Path $extractedProjectFolder.FullName -Destination $desktopTarget -Force

    Write-Info "Starting dependency installer..."
    $process = Start-Process "cmd.exe" -ArgumentList "/c install_dependencies.bat" -WorkingDirectory $desktopTarget -PassThru -Wait
    if ($process.ExitCode -ne 0) {
        throw "Dependency installer exited with code $($process.ExitCode)."
    }

    Write-Host "[OK] Installation flow finished successfully." -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    if (Test-Path $tempRoot) {
        Remove-Item -Path $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
