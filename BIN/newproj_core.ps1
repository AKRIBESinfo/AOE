param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectCode
)

$root = "C:\AK"
$projectRoot = Join-Path $root "PRJ\$ProjectCode"

$ProjectCode = $ProjectCode.ToUpper()

if ($ProjectCode -notmatch '^[A-Z]{3}\d{4}$') {
    Write-Error "Invalid project code. Use CLIENTYYNN format, for example: SAM2600"
    exit 1
}

if (Test-Path $projectRoot) {
    Write-Warning "Project already exists: $projectRoot"
    exit 0
}

$folders = @(
    "IMP\RAW",
    "IMP\REF",
    "EXP\DRW",
    "EXP\EST",
    "EXP\COORD",
    "EXP\RFI",
    "EXP\SUB",
    "EXP\IMG",
    "EXP\MISC"
)

New-Item -Path $projectRoot -ItemType Directory -Force | Out-Null

foreach ($folder in $folders) {
    New-Item -Path (Join-Path $projectRoot $folder) -ItemType Directory -Force | Out-Null
}

$infoFile = Join-Path $projectRoot "PROJECT_INFO.txt"

@"
AOE v0.1
Project Code: $ProjectCode
Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Project Structure:
- IMP = preserved imports
  - RAW = untouched incoming files
  - REF = curated reference files kept in original naming

- EXP = deliverable outputs
  - DRW   = drawings
  - EST   = estimates
  - COORD = coordination files
  - RFI   = request-for-information documents
  - SUB   = submittals
  - IMG   = images, scans, renderings
  - MISC  = overflow / uncommon deliverables

Naming Standard:
PROJECTCODE_TYPESEQ_YYMMDD.ext

Examples:
${ProjectCode}_DRW001_$(Get-Date -Format "yyMMdd").pdf
${ProjectCode}_EST001_$(Get-Date -Format "yyMMdd").xlsx
${ProjectCode}_NWC001_$(Get-Date -Format "yyMMdd").nwc
${ProjectCode}_IMG001_$(Get-Date -Format "yyMMdd").jpg
"@ | Set-Content -Path $infoFile

Write-Output "AOE v0.1 project created successfully: $projectRoot"