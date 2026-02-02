# ============================================
# Module 00: Docker Installation Verification
# ============================================
# Run this script to confirm Docker is properly installed.
# Usage: powershell -ExecutionPolicy Bypass -File verify.ps1
# ============================================

$pass = 0
$fail = 0

function Test-Check {
    param (
        [string]$Label,
        [scriptblock]$Command
    )
    Write-Host ("  {0,-30} " -f $Label) -NoNewline
    try {
        $null = & $Command 2>&1
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            Write-Host "PASS" -ForegroundColor Green
            $script:pass++
        } else {
            Write-Host "FAIL" -ForegroundColor Red
            $script:fail++
        }
    } catch {
        Write-Host "FAIL" -ForegroundColor Red
        $script:fail++
    }
}

Write-Host ""
Write-Host "=== Docker Installation Verification ===" -ForegroundColor Cyan
Write-Host ""

Test-Check "Docker CLI installed" { docker --version }
Test-Check "Docker Compose installed" { docker compose version }
Test-Check "Docker daemon running" { docker info }
Test-Check "Can pull images" { docker pull hello-world }
Test-Check "Can run containers" { docker run --rm hello-world }

Write-Host ""
Write-Host "---"
Write-Host "Results: $pass passed, $fail failed"
Write-Host ""

if ($fail -eq 0) {
    Write-Host "All checks passed! You're ready for Module 01." -ForegroundColor Green
} else {
    Write-Host "Some checks failed. See 00-get-docker/README.md for troubleshooting." -ForegroundColor Yellow
}
