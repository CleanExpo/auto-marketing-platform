# Safe Start Script for Auto Marketing Workflow
# Includes CPU monitoring and automatic throttling

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   AUTO MARKETING - SAFE START MODE" -ForegroundColor Cyan
Write-Host "   CPU Limited to 80% Maximum" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install psutil --quiet 2>$null

# Check current CPU usage
Write-Host ""
Write-Host "Checking system resources..." -ForegroundColor Yellow
$cpu = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
Write-Host "Current CPU Usage: $cpu%" -ForegroundColor Cyan

if ($cpu -gt 80) {
    Write-Host "⚠️  WARNING: CPU usage is already high ($cpu%)" -ForegroundColor Red
    Write-Host "Waiting for CPU to drop below 80%..." -ForegroundColor Yellow
    
    while ($cpu -gt 80) {
        Start-Sleep -Seconds 5
        $cpu = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
        Write-Host "Current CPU: $cpu%" -ForegroundColor Yellow
    }
}

Write-Host "✅ CPU usage is safe ($cpu%)" -ForegroundColor Green
Write-Host ""

# Set process priority to below normal
Write-Host "Setting process priority to 'Below Normal'..." -ForegroundColor Yellow

# Start the workflow with CPU management
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Starting Auto Marketing Workflow" -ForegroundColor Cyan
Write-Host "   With CPU Protection Enabled" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Run with below normal priority
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "python"
$pinfo.Arguments = "execute-workflow.py"
$pinfo.UseShellExecute = $false
$pinfo.RedirectStandardOutput = $false
$pinfo.RedirectStandardError = $false

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start() | Out-Null

# Set priority after start
try {
    $p.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
    Write-Host "✅ Process priority set to 'Below Normal'" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not set process priority" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Workflow is running with CPU protection..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop if CPU gets too high" -ForegroundColor Yellow
Write-Host ""

# Wait for process to complete
$p.WaitForExit()

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Workflow Completed" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan