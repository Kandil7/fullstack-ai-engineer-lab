<#
.SYNOPSIS
    Generate a new Architecture Decision Record (ADR) with numbered filename.

.DESCRIPTION
    Creates a new ADR file from the ADR template with the next sequential number.
    The ADR is placed in docs/decisions/ with format: NNNN-slug.md.

.EXAMPLE
    ./infra/scripts/new-adr.ps1 "Adopt keyset pagination"
    ./infra/scripts/new-adr.ps1 "Use Redis for session cache"
    ./infra/scripts/new-adr.ps1 "Switch to Qdrant for vector DB" -Status accepted
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Title,
    [ValidateSet("proposed", "accepted", "deprecated", "superseded")]
    [string]$Status = "proposed"
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$DecisionsDir = "$RootDir/docs/decisions"
$TemplateFile = "$RootDir/templates/adr.template.md"

# ─── Helpers ───────────────────────────────────────

function Write-Step {
    param([string]$Message)
    Write-Host "`n► $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "  ✗ $Message" -ForegroundColor Red
}

function ConvertTo-Slug {
    param([string]$Text)
    $Text.ToLower() -replace '[^a-z0-9\s-]', '' -replace '\s+', '-' -replace '-+', '-' -replace '^-|-$', ''
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Full-Stack AI Engineer Lab — New ADR   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Find Next Number ─────────────────────

Write-Step "Finding next ADR number..."

if (-not (Test-Path $DecisionsDir)) {
    New-Item -ItemType Directory -Path $DecisionsDir -Force | Out-Null
}

$existingAdrs = Get-ChildItem "$DecisionsDir/*.md" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '^\d{4}-' } |
    Sort-Object Name

if ($existingAdrs.Count -gt 0) {
    $lastAdr = $existingAdrs[-1].Name
    $lastNumber = [int]($lastAdr -replace '^(\d+)-.*$', '$1')
    $nextNumber = $lastNumber + 1
} else {
    $nextNumber = 1
}

$numberStr = $nextNumber.ToString("0000")
Write-Ok "Next ADR number: $numberStr"

# ─── Step 2: Generate Filename ────────────────────

Write-Step "Generating filename..."

$slug = ConvertTo-Slug $Title
$filename = "$numberStr-$slug.md"
$filepath = "$DecisionsDir/$filename"

Write-Ok "Filename: $filename"

# ─── Step 3: Check for Existing ADR ───────────────

if (Test-Path $filepath) {
    Write-Fail "ADR already exists: $filepath"
    exit 1
}

# ─── Step 4: Create ADR from Template ─────────────

Write-Step "Creating ADR from template..."

if (-not (Test-Path $TemplateFile)) {
    Write-Fail "ADR template not found: $TemplateFile"
    exit 1
}

$template = Get-Content $TemplateFile -Raw

# Replace placeholders
$date = Get-Date -Format "yyyy-MM-dd"
$content = $template -replace '\{\{TITLE\}\}', $Title
$content = $content -replace '\{\{NUMBER\}\}', $numberStr
$content = $content -replace '\{\{STATUS\}\}', $Status
$content = $content -replace '\{\{DATE\}\}', $date
$content = $content -replace '\{\{SLUG\}\}', $slug

# Set content
Set-Content -Path $filepath -Value $content -Encoding UTF8

Write-Ok "Created: $filepath"

# ─── Step 5: Update Decision Log ──────────────────

Write-Step "Updating decision log..."

$decisionLog = "$RootDir/registries/decision-log.yaml"

$logEntry = @"
  - id: ADR-$numberStr
    title: "$Title"
    path: docs/decisions/$filename
    status: $Status
    date: $date
"@

if (Test-Path $decisionLog) {
    Add-Content -Path $decisionLog -Value $logEntry -Encoding UTF8
    Write-Ok "Decision log updated"
} else {
    $logContent = @"
# Decision Log — Architecture Decision Records
version: 1
decisions:
$logEntry"@
    Set-Content -Path $decisionLog -Value $logContent -Encoding UTF8
    Write-Ok "Decision log created"
}

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║           ADR Created!                   ║
  ╠══════════════════════════════════════════╣
  ║  File  : $filename
  ║  Title : $Title
  ║  Status: $Status
  ║  Date  : $date
  ╚══════════════════════════════════════════╝

  Edit the ADR to fill in Context, Decision, and Consequences.

"@ -ForegroundColor Green
