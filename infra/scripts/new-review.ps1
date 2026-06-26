<#
.SYNOPSIS
    Generate a new code review file from the template.

.DESCRIPTION
    Creates a code review file for a specified project/feature using the
    code-review.template.md template.

.EXAMPLE
    ./infra/scripts/new-review.ps1 "auth-service" "jwt-middleware"
    ./infra/scripts/new-review.ps1 "rag-system" "chunking-pipeline"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Project,

    [Parameter(Mandatory=$true)]
    [string]$Feature
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$TemplateFile = "$RootDir/templates/code-review.template.md"

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
  ║   Full-Stack AI Engineer Lab — Review    ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Validate Template ────────────────────

Write-Step "Checking template..."

if (-not (Test-Path $TemplateFile)) {
    Write-Fail "Code review template not found: $TemplateFile"
    exit 1
}

Write-Ok "Template found"

# ─── Step 2: Find Project Directory ───────────────

Write-Step "Locating project..."

$projectDir = Get-ChildItem "$RootDir/projects" -Directory -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -eq $Project } |
    Select-Object -First 1

if (-not $projectDir) {
    Write-Fail "Project not found: $Project"
    Write-Host "  Available projects:" -ForegroundColor Yellow
    Get-ChildItem "$RootDir/projects" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "    - $($_.Name)" -ForegroundColor Gray
    }
    exit 1
}

Write-Ok "Project: $($projectDir.FullName)"

# ─── Step 3: Generate Review File ─────────────────

Write-Step "Generating review file..."

$slug = ConvertTo-Slug $Feature
$date = Get-Date -Format "yyyy-MM-dd"
$reviewFilename = "$slug-ai-review-$date.md"
$reviewPath = "$($projectDir.FullName)/$reviewFilename"

if (Test-Path $reviewPath) {
    Write-Fail "Review file already exists: $reviewPath"
    exit 1
}

# Read template and customize
$template = Get-Content $TemplateFile -Raw

# Replace common placeholders
$date = Get-Date -Format "yyyy-MM-dd"
$content = $template -replace '\{\{PROJECT\}\}', $Project
$content = $content -replace '\{\{FEATURE\}\}', $Feature
$content = $content -replace '\{\{DATE\}\}', $date

# Add header
$header = @"
# Code Review: $Project — $Feature

- **Date**: $date
- **Reviewer**: AI Code Reviewer
- **Project**: $Project
- **Feature**: $Feature
- **Status**: In Progress

---

"@

$fullContent = $header + $content

Set-Content -Path $reviewPath -Value $fullContent -Encoding UTF8

Write-Ok "Created: $reviewPath"

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║        Review File Created!              ║
  ╠══════════════════════════════════════════╣
  ║  File    : $reviewFilename
  ║  Project : $Project
  ║  Feature : $Feature
  ║  Date    : $date
  ╚══════════════════════════════════════════╝

  Edit the review to fill in findings by severity.

"@ -ForegroundColor Green
