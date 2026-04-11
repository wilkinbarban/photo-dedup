$ErrorActionPreference = "Stop"

$zipUrl = "https://github.com/wilkinbarban/photo-dedup/archive/refs/heads/main.zip"
$tempZipPath = Join-Path $env:TEMP "photo-dedup-main.zip"
$tempExtractPath = Join-Path $env:TEMP "photo-dedup-main-extract"
$finalPath = Join-Path $env:USERPROFILE "Desktop\photo-dedup-main"

Write-Host "Downloading PhotoDedup..."
Invoke-WebRequest -Uri $zipUrl -OutFile $tempZipPath

Write-Host "Extracting files..."
if (Test-Path $tempExtractPath) {
    Remove-Item -Path $tempExtractPath -Recurse -Force
}
Expand-Archive -Path $tempZipPath -DestinationPath $tempExtractPath -Force

$extractedFolder = Join-Path $tempExtractPath "photo-dedup-main"

if (Test-Path $finalPath) {
    Remove-Item -Path $finalPath -Recurse -Force
}
Move-Item -Path $extractedFolder -Destination $finalPath -Force

Set-Location $finalPath
Write-Host "Starting dependency installer..."
Start-Process "cmd.exe" -ArgumentList "/c install_dependencies.bat"