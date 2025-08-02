# Permanent PATH Fix for Claude Code
# This script permanently adds C:\Users\Phill\.local\bin to your PATH
# Run as Administrator for system-wide fix, or as user for user-specific fix

param(
    [switch]$SystemWide = $false
)

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Permanent PATH Fix for Claude Code" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$localBinPath = "C:\Users\Phill\.local\bin"

# Determine the target (User or Machine)
$target = if ($SystemWide) { [EnvironmentVariableTarget]::Machine } else { [EnvironmentVariableTarget]::User }
$targetName = if ($SystemWide) { "System-wide" } else { "User-specific" }

Write-Host "Target: $targetName PATH modification" -ForegroundColor Yellow
Write-Host "Path to add: $localBinPath" -ForegroundColor Yellow
Write-Host ""

# Get current PATH
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", $target)
    Write-Host "Current PATH length: $($currentPath.Length) characters" -ForegroundColor Cyan
    
    # Check if the path is already in PATH
    if ($currentPath -like "*$localBinPath*") {
        Write-Host "✓ Path already exists in $targetName PATH!" -ForegroundColor Green
        Write-Host "No changes needed." -ForegroundColor Green
    } else {
        Write-Host "Adding path to $targetName PATH..." -ForegroundColor Yellow
        
        # Add the path
        $newPath = if ($currentPath.EndsWith(";")) {
            "$currentPath$localBinPath"
        } else {
            "$currentPath;$localBinPath"
        }
        
        # Set the new PATH
        [Environment]::SetEnvironmentVariable("PATH", $newPath, $target)
        
        Write-Host "✓ Successfully added to $targetName PATH!" -ForegroundColor Green
        
        # Also update current session
        $env:PATH = "$env:PATH;$localBinPath"
        Write-Host "✓ Updated current session PATH" -ForegroundColor Green
    }
    
} catch {
    Write-Host "❌ Error modifying PATH: $($_.Exception.Message)" -ForegroundColor Red
    if (-not $SystemWide) {
        Write-Host "Try running as Administrator with -SystemWide parameter" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Verification" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Verify the change
$verifyPath = [Environment]::GetEnvironmentVariable("PATH", $target)
if ($verifyPath -like "*$localBinPath*") {
    Write-Host "✓ Verification successful! Path is in $targetName PATH" -ForegroundColor Green
} else {
    Write-Host "❌ Verification failed! Path not found in $targetName PATH" -ForegroundColor Red
}

# Test if the directory exists
if (Test-Path $localBinPath) {
    Write-Host "✓ Directory exists: $localBinPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  Directory does not exist: $localBinPath" -ForegroundColor Yellow
    Write-Host "Creating directory..." -ForegroundColor Yellow
    try {
        New-Item -Path $localBinPath -ItemType Directory -Force | Out-Null
        Write-Host "✓ Directory created successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create directory: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Next Steps" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. RESTART your terminal/PowerShell for changes to take effect" -ForegroundColor Yellow
Write-Host "2. Or close and reopen VS Code" -ForegroundColor Yellow
Write-Host "3. Test with: claude --version" -ForegroundColor Yellow
Write-Host ""

Write-Host "If you still see PATH warnings after restart:" -ForegroundColor Cyan
Write-Host "• Run this script with -SystemWide parameter as Administrator" -ForegroundColor White
Write-Host "• Or manually add via System Properties > Environment Variables" -ForegroundColor White
Write-Host ""

Write-Host "Commands to test after restart:" -ForegroundColor Green
Write-Host "  claude --version" -ForegroundColor White
Write-Host "  claude --help" -ForegroundColor White
Write-Host "  claude --dangerously-skip-permissions" -ForegroundColor White
Write-Host ""

# Show current session info
Write-Host "Current session PATH includes:" -ForegroundColor Cyan
$env:PATH -split ';' | Where-Object { $_ -like "*local*" -or $_ -like "*claude*" -or $_ -like "*npm*" } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ PATH fix complete! Restart your terminal to see changes." -ForegroundColor Green
