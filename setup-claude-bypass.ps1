# Claude Code Setup with Bypass Permissions
# Run with: powershell -ExecutionPolicy Bypass -File setup-claude-bypass.ps1

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Claude Code Setup with Bypass Mode" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location "C:\Auto Marketing"
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Check if Claude is installed
Write-Host "[1/6] Checking Claude Code installation..." -ForegroundColor Yellow
try {
    $claudeVersion = & claude --version 2>$null
    if ($claudeVersion) {
        Write-Host "✓ Claude Code is installed: $claudeVersion" -ForegroundColor Green
    } else {
        throw "Claude not found"
    }
} catch {
    Write-Host "Installing Claude Code..." -ForegroundColor Yellow
    try {
        & npm install -g @anthropic-ai/claude-code
        Write-Host "✓ Claude Code installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install Claude Code" -ForegroundColor Red
        Write-Host "Please run: npm install -g @anthropic-ai/claude-code" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Configure PATH
Write-Host "[2/6] Configuring PATH..." -ForegroundColor Yellow
$localBin = "C:\Users\Phill\.local\bin"
$currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)

if ($currentPath -notlike "*$localBin*") {
    Write-Host "Adding local bin to PATH..." -ForegroundColor Yellow
    try {
        $newPath = "$currentPath;$localBin"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)
        $env:PATH = "$env:PATH;$localBin"
        Write-Host "✓ PATH updated successfully" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Failed to update PATH" -ForegroundColor Red
    }
} else {
    Write-Host "✓ PATH already configured" -ForegroundColor Green
}

# Install project dependencies
Write-Host "[3/6] Installing project dependencies..." -ForegroundColor Yellow
try {
    & npm install
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Some dependencies may have failed to install" -ForegroundColor Red
}

# Build the project
Write-Host "[4/6] Building TypeScript project..." -ForegroundColor Yellow
try {
    & npm run build
    Write-Host "✓ Project built successfully" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Build may have failed" -ForegroundColor Red
}

# Check environment configuration
Write-Host "[5/6] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ Environment file exists" -ForegroundColor Green
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "ANTHROPIC_API_KEY") {
        Write-Host "✓ API key configured" -ForegroundColor Green
    } else {
        Write-Host "WARNING: API key not found in .env" -ForegroundColor Red
    }
} else {
    Write-Host "WARNING: .env file not found" -ForegroundColor Red
}

# Test Claude Code
Write-Host "[6/6] Testing Claude Code..." -ForegroundColor Yellow
try {
    $claudeHelp = & claude --help 2>$null
    if ($claudeHelp) {
        Write-Host "✓ Claude Code is working" -ForegroundColor Green
    } else {
        throw "Claude test failed"
    }
} catch {
    Write-Host "ERROR: Claude Code test failed" -ForegroundColor Red
    Write-Host "You may need to restart your terminal or computer" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "You can now run Claude Code with bypass permissions:" -ForegroundColor Green
Write-Host ""
Write-Host "  claude --dangerously-skip-permissions" -ForegroundColor White
Write-Host "  claude --dangerously-skip-permissions --verbose" -ForegroundColor White
Write-Host ""

Write-Host "SECURITY WARNING:" -ForegroundColor Red
Write-Host "These commands bypass permission checks. Use only in" -ForegroundColor Yellow
Write-Host "a secure, isolated environment!" -ForegroundColor Yellow
Write-Host ""

Write-Host "Available npm commands:" -ForegroundColor Green
Write-Host "  npm run dev       - Start development server" -ForegroundColor White
Write-Host "  npm run build     - Build for production" -ForegroundColor White
Write-Host "  npm run start     - Start production server" -ForegroundColor White
Write-Host "  npm run dev:watch - Start with auto-reload" -ForegroundColor White
Write-Host ""

Write-Host "To test immediately, run:" -ForegroundColor Cyan
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""

# Pause for user to read
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
