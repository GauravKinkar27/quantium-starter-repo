Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Starting Quantium Automated CI Test Suite Wrapper" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Activate the virtual environment safely
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Virtual environment found. Activating..." -ForegroundColor Green
    .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Error: Virtual environment (.venv) missing." -ForegroundColor Red
    exit 1
}

# 2. Run the test suite
Write-Host "Running unit testing module assertions..." -ForegroundColor Yellow
pytest test_app.py
$TEST_RESULT = $LASTEXITCODE

# 3. Return the correct system exit codes for CI/CD engines
Write-Host "====================================================" -ForegroundColor Cyan
if ($TEST_RESULT -eq 0) {
    Write-Host "SUCCESS: All test assertions passed flawlessly!" -ForegroundColor Green
    Write-Host "====================================================" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "FAILURE: Test suite failed with exit code $TEST_RESULT." -ForegroundColor Red
    Write-Host "====================================================" -ForegroundColor Cyan
    exit 1
}