param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectCode,

    [Parameter(Mandatory = $true)]
    [string]$TypeCode
)

# Root paths
$root = "C:\AK"
$projectRoot = Join-Path $root "PRJ\$ProjectCode"
$typeFolder = Join-Path $projectRoot "EXP\$TypeCode"

# TYPE → Extension mapping
$typeMap = @{
    "PDF" = "pdf"
    "NWC" = "nwc"
    "NWD" = "nwd"
    "EST" = "xlsx"
    "RPT" = "docx"
    "LOG" = "txt"
    "IMG" = "png"
    "SUB" = "pdf"
    "CUT" = "pdf"
    "DRW" = "pdf"
    "MOD" = "rvt"
}

# Normalize input
$ProjectCode = $ProjectCode.ToUpper()
$TypeCode = $TypeCode.ToUpper()

# Validate project code
if ($ProjectCode -notmatch '^[A-Z]{3}\d{4}$') {
    Write-Error "Invalid project code. Use CLIENTYYNN (example: UAM2501)"
    exit 1
}

# Validate TYPE
if ($TypeCode -notin $typeMap.Keys) {
    Write-Error "Invalid TYPE code. Valid: $($typeMap.Keys -join ', ')"
    exit 1
}

$Extension = $typeMap[$TypeCode]

# Check project exists
if (-not (Test-Path $projectRoot)) {
    Write-Error "Project not found: $projectRoot"
    exit 1
}

# Ensure TYPE folder exists
if (-not (Test-Path $typeFolder)) {
    New-Item -Path $typeFolder -ItemType Directory | Out-Null
}

# Date
$dateCode = Get-Date -Format "yyMMdd"

# Find existing files
$pattern = "^${ProjectCode}_${TypeCode}(\d{3})_${dateCode}\.$Extension$"

$files = Get-ChildItem -Path $typeFolder -File | Where-Object {
    $_.Name -match $pattern
}

# Determine next sequence
$maxSeq = 0
foreach ($file in $files) {
    if ($file.Name -match $pattern) {
        $seq = [int]$matches[1]
        if ($seq -gt $maxSeq) {
            $maxSeq = $seq
        }
    }
}

$nextSeq = "{0:D3}" -f ($maxSeq + 1)

# Build filename
$newName = "${ProjectCode}_${TypeCode}${nextSeq}_${dateCode}.${Extension}"
$newPath = Join-Path $typeFolder $newName

# Create file
New-Item -Path $newPath -ItemType File | Out-Null

Write-Output "Created: $newPath"