# =========================
# AOE ADMIN SETUP SCRIPT
# =========================

Write-Host "Starting AOE Setup..." -ForegroundColor Cyan


if (!(Test-Path "C:\AK")) {
    New-Item -ItemType Directory -Path "C:\AK"
}

$folders = @("AG","BIN","LOG","PRJ")

foreach ($f in $folders) {
    $path = "C:\AK\$f"
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path
    }
}

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*C:\AK\BIN*") {
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$currentPath;C:\AK\BIN",
        "User"
    )
    Write-Host "Added BIN to PATH"
}

attrib +h C:\AK\AG
attrib +h C:\AK\BIN
attrib +h C:\AK\LOG

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Akribes Projects.lnk")
$Shortcut.TargetPath = "C:\AK\PRJ"
$Shortcut.Save()

Write-Host "Desktop shortcut created"

Write-Host "----------------------------------"
Write-Host "AOE Setup Complete" -ForegroundColor Green
Write-Host "Use 'Akribes Projects' on Desktop"
Write-Host "----------------------------------"
