# Auto Marketing Project Setup Script
Write-Host "Setting up Auto Marketing project environment..." -ForegroundColor Green

# Ensure the local bin directory is in PATH
$localBin = "C:\Users\Phill\.local\bin"
$currentPath = $env:PATH

if ($currentPath -notlike "*$localBin*") {
    Write-Host "Adding $localBin to PATH..." -ForegroundColor Yellow
    $newPath = "$currentPath;$localBin"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)
    $env:PATH = $newPath
    Write-Host "PATH updated successfully!" -ForegroundColor Green
} else {
    Write-Host "Local bin directory already in PATH" -ForegroundColor Green
}

# Change to project directory
Set-Location "C:\Auto Marketing"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan

# Check if Claude is available
try {
    $claudeVersion = & claude --version 2>$null
    if ($claudeVersion) {
        Write-Host "Claude Code is available and ready to use!" -ForegroundColor Green
        Write-Host "Version: $claudeVersion" -ForegroundColor Cyan
    }
} catch {
    Write-Host "WARNING: Claude command not found. Make sure @anthropic-ai/claude-code is installed." -ForegroundColor Red
    Write-Host "Run: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
}

Write-Host "`nSetup complete! You can now use Claude commands." -ForegroundColor Green
Write-Host "Key files created:" -ForegroundColor Cyan
Write-Host "  - CLAUDE.md (Claude instructions)" -ForegroundColor White
Write-Host "  - setup.bat (Batch setup script)" -ForegroundColor White
Write-Host "  - setup.ps1 (PowerShell setup script)" -ForegroundColor White
