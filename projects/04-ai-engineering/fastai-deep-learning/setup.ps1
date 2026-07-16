<#
.SYNOPSIS
    Set up the fast.ai Deep Learning track environment (Windows / PowerShell).

.DESCRIPTION
    Creates a local virtual environment, installs a CPU-only PyTorch build to
    avoid the multi-GB CUDA download, then installs the rest of the pinned
    dependencies. fastai + torch are large; this is intentionally a separate,
    opt-in step from the rest of the repo.

    nbdev's full workflow (docs via Quarto) is only fully supported on macOS,
    Linux, or Windows-via-WSL. On native Windows the Python package and the
    export/test commands work; Quarto docs rendering is best run under WSL.

.EXAMPLE
    ./setup.ps1                 # CPU-only install (recommended on Windows)
    ./setup.ps1 -Gpu            # Install default (CUDA) PyTorch wheels
    ./setup.ps1 -SkipHeavy      # nbdev + tooling only, no torch/fastai
#>
[CmdletBinding()]
param(
    [switch]$Gpu,
    [switch]$SkipHeavy
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here

try {
    $venv = Join-Path $here ".venv"
    if (-not (Test-Path $venv)) {
        Write-Host "Creating virtual environment at .venv ..." -ForegroundColor Cyan
        python -m venv $venv
    }

    $py = Join-Path $venv "Scripts\python.exe"
    & $py -m pip install --upgrade pip

    if ($SkipHeavy) {
        Write-Host "Installing nbdev + tooling only (no torch/fastai) ..." -ForegroundColor Cyan
        & $py -m pip install nbdev==2.3.13 jupyterlab==4.2.5 ipykernel==6.29.5 `
            black==24.8.0 isort==5.13.2 ruff==0.6.8 pytest==8.3.3 python-dotenv==1.0.1
    }
    else {
        if ($Gpu) {
            Write-Host "Installing PyTorch (default CUDA wheels) ..." -ForegroundColor Yellow
            & $py -m pip install torch==2.4.1 torchvision==0.19.1
        }
        else {
            Write-Host "Installing CPU-only PyTorch (avoids ~2 GB CUDA download) ..." -ForegroundColor Cyan
            & $py -m pip install torch==2.4.1 torchvision==0.19.1 `
                --index-url https://download.pytorch.org/whl/cpu
        }
        Write-Host "Installing remaining pinned dependencies ..." -ForegroundColor Cyan
        & $py -m pip install -r (Join-Path $here "requirements.txt")
    }

    Write-Host "`nVerifying install ..." -ForegroundColor Cyan
    & $py -c "import nbdev; print('nbdev', nbdev.__version__)"
    if (-not $SkipHeavy) {
        & $py -c "import torch, fastai; print('torch', torch.__version__, '| fastai', fastai.__version__)"
    }

    Write-Host "`nDone. Register the Jupyter kernel with:" -ForegroundColor Green
    Write-Host "  .venv\Scripts\python.exe -m ipykernel install --user --name fastai-dl" -ForegroundColor Green
}
finally {
    Pop-Location
}
