$ErrorActionPreference = "Stop"

$zipUrl = "https://github.com/wilkinbarban/photo-dedup/archive/refs/heads/main.zip"
$desktopPath = [Environment]::GetFolderPath("DesktopDirectory")
if ([string]::IsNullOrWhiteSpace($desktopPath)) {
    $desktopPath = Join-Path $env:USERPROFILE "Desktop"
}
$tempZipPath = Join-Path $env:TEMP "photo-dedup-main.zip"
$tempExtractPath = Join-Path $env:TEMP "photo-dedup-main-extract"
$finalPath = Join-Path $desktopPath "photo-dedup-main"

Write-Host "Downloading PhotoDedup..."
Invoke-WebRequest -Uri $zipUrl -OutFile $tempZipPath

Write-Host "Extracting files..."
if (Test-Path $tempExtractPath) {
    Remove-Item -Path $tempExtractPath -Recurse -Force
}
Expand-Archive -Path $tempZipPath -DestinationPath $tempExtractPath -Force

$extractedFolder = Get-ChildItem -Path $tempExtractPath -Directory | Select-Object -First 1
if (-not $extractedFolder) {
    throw "The extracted project folder could not be found."
}

if (-not (Test-Path $desktopPath)) {
    New-Item -Path $desktopPath -ItemType Directory -Force | Out-Null
}

if (Test-Path $finalPath) {
    Remove-Item -Path $finalPath -Recurse -Force
}
Move-Item -Path $extractedFolder.FullName -Destination $finalPath -Force

Set-Location $finalPath
Write-Host "Starting dependency installer..."
Start-Process "cmd.exe" -ArgumentList "/c install_dependencies.bat"