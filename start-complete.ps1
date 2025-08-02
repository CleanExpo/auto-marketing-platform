# Auto Marketing Agent - Complete Startup Script
# This script fixes PATH issues and starts Claude Code with bypass permissions

Write-Host "🚀 Starting Auto Marketing Agent with Claude Code..." -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location "C:\Auto Marketing"

# Function to add to PATH if not already there
function Add-ToPath {
    param([string]$PathToAdd)
    
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
    if ($currentPath -notlike "*$PathToAdd*") {
        Write-Host "🔧 Adding $PathToAdd to PATH..." -ForegroundColor Yellow
        $newPath = "$currentPath;$PathToAdd"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)
        $env:PATH = "$env:PATH;$PathToAdd"
        Write-Host "✅ PATH updated successfully" -ForegroundColor Green
    } else {
        Write-Host "✅ PATH already contains $PathToAdd" -ForegroundColor Green
    }
}

# Fix common PATH issues
Write-Host "🔍 Checking and fixing PATH configuration..." -ForegroundColor Cyan
Add-ToPath "C:\Users\Phill\.local\bin"
Add-ToPath "$env:APPDATA\npm"  # npm global packages
Add-ToPath "C:\Program Files\nodejs"  # Node.js

# Create the local bin directory if it doesn't exist
$localBin = "C:\Users\Phill\.local\bin"
if (-not (Test-Path $localBin)) {
    Write-Host "📁 Creating local bin directory..." -ForegroundColor Yellow
    New-Item -Path $localBin -ItemType Directory -Force | Out-Null
    Write-Host "✅ Directory created: $localBin" -ForegroundColor Green
}

# Check if Claude Code is installed
Write-Host "🤖 Checking Claude Code installation..." -ForegroundColor Cyan
try {
    $claudeVersion = & claude --version 2>$null
    if ($claudeVersion) {
        Write-Host "✅ Claude Code installed: $claudeVersion" -ForegroundColor Green
    } else {
        throw "Not found"
    }
} catch {
    Write-Host "📦 Installing Claude Code..." -ForegroundColor Yellow
    & npm install -g @anthropic-ai/claude-code
    Write-Host "✅ Claude Code installed" -ForegroundColor Green
}

# Verify project setup
Write-Host "🏗️ Verifying project setup..." -ForegroundColor Cyan

if (Test-Path "package.json") {
    Write-Host "✅ package.json found" -ForegroundColor Green
} else {
    Write-Host "❌ package.json not found!" -ForegroundColor Red
    exit 1
}

if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️ .env file not found - API key may not be configured" -ForegroundColor Yellow
}

if (Test-Path "src\index.ts") {
    Write-Host "✅ TypeScript source found" -ForegroundColor Green
} else {
    Write-Host "⚠️ src\index.ts not found" -ForegroundColor Yellow
}

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing npm dependencies..." -ForegroundColor Yellow
    & npm install
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# Build the project
Write-Host "🔨 Building TypeScript project..." -ForegroundColor Cyan
& npm run build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build successful" -ForegroundColor Green
} else {
    Write-Host "⚠️ Build had issues, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup complete! Ready to start..." -ForegroundColor Green
Write-Host ""

# Show available options
Write-Host "Choose an option:" -ForegroundColor Cyan
Write-Host "1. Start development server only" -ForegroundColor White
Write-Host "2. Start Claude Code (bypass permissions)" -ForegroundColor White
Write-Host "3. Start both (recommended)" -ForegroundColor White
Write-Host "4. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🚀 Starting development server..." -ForegroundColor Green
        & npm run dev
    }
    "2" {
        Write-Host "🤖 Starting Claude Code with bypass permissions..." -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️ SECURITY WARNING: Bypass mode disables safety checks!" -ForegroundColor Red
        Write-Host "Use only in secure, isolated environments!" -ForegroundColor Red
        Write-Host ""
        $confirm = Read-Host "Continue? (y/N)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            & claude --dangerously-skip-permissions --verbose
        } else {
            Write-Host "Operation cancelled." -ForegroundColor Yellow
        }
    }
    "3" {
        Write-Host "🚀 Starting development server in background..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-Command", "cd 'C:\Auto Marketing'; npm run dev" -NoNewWindow
        
        Start-Sleep -Seconds 3
        
        Write-Host "🤖 Starting Claude Code with bypass permissions..." -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️ SECURITY WARNING: Bypass mode disables safety checks!" -ForegroundColor Red
        Write-Host "Use only in secure, isolated environments!" -ForegroundColor Red
        Write-Host ""
        $confirm = Read-Host "Continue? (y/N)"
        if ($confirm -eq "y" -or $confirm -eq "Y") {
            & claude --dangerously-skip-permissions --verbose
        } else {
            Write-Host "Operation cancelled." -ForegroundColor Yellow
        }
    }
    "4" {
        Write-Host "👋 Goodbye!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📚 Useful commands:" -ForegroundColor Cyan
Write-Host "  npm run dev          - Start development server" -ForegroundColor White
Write-Host "  npm run build        - Build for production" -ForegroundColor White
Write-Host "  claude --help        - Claude Code help" -ForegroundColor White
Write-Host "  claude /status       - Check Claude status" -ForegroundColor White
