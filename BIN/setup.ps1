$base = "C:\ak"

$folders = @(
    "prj",
    "exp",
    "bin",
    "log"
)

New-Item -Path $base -ItemType Directory -Force

foreach ($folder in $folders) {
    New-Item -Path "$base\$folder" -ItemType Directory -Force
}

Write-Output "Akribes structure created successfully 3ltr."