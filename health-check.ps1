#!/usr/bin/env pwsh
# Auto Marketing Agent - Complete Health Check Script

Write-Host "🏥 Auto Marketing Agent - Health Check Starting..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Yellow

$errors = @()
$warnings = @()

# Check if we're in the correct directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: Not in project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Project Structure Check..." -ForegroundColor Cyan

# Check required files
$requiredFiles = @(
    "package.json",
    "tsconfig.json", 
    "src/index.ts",
    ".env"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing" -ForegroundColor Red
        $errors += "Missing file: $file"
    }
}

# Check required directories
$requiredDirs = @("src", "dist")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir -PathType Container) {
        Write-Host "  ✅ $dir/ directory exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dir/ directory missing" -ForegroundColor Red
        $errors += "Missing directory: $dir"
    }
}

Write-Host "`n🔧 Dependencies Check..." -ForegroundColor Cyan

# Check if node_modules exists
if (Test-Path "node_modules" -PathType Container) {
    Write-Host "  ✅ node_modules installed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  node_modules missing - running npm install..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Failed to install dependencies" -ForegroundColor Red
        $errors += "Failed to install dependencies"
    }
}

Write-Host "`n📝 TypeScript Compilation Check..." -ForegroundColor Cyan

# Clean and build
Write-Host "  🧹 Cleaning previous build..." -ForegroundColor Gray
npm run clean 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠️  Clean command failed (this is okay if dist doesn't exist)" -ForegroundColor Yellow
}

Write-Host "  🔨 Building TypeScript..." -ForegroundColor Gray
npm run build
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ TypeScript compilation successful" -ForegroundColor Green
    
    # Check if dist/index.js was created
    if (Test-Path "dist/index.js") {
        Write-Host "  ✅ Output file dist/index.js created" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Output file dist/index.js not found" -ForegroundColor Red
        $errors += "Build output not created"
    }
} else {
    Write-Host "  ❌ TypeScript compilation failed" -ForegroundColor Red
    $errors += "TypeScript compilation failed"
}

Write-Host "`n🔍 Type Checking..." -ForegroundColor Cyan
npm run type-check
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Type checking passed" -ForegroundColor Green
} else {
    Write-Host "  ❌ Type checking failed" -ForegroundColor Red
    $errors += "Type checking failed"
}

Write-Host "`n🌐 Environment Variables Check..." -ForegroundColor Cyan

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "PORT=\d+") {
        Write-Host "  ✅ PORT configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  PORT not configured" -ForegroundColor Yellow
        $warnings += "PORT not configured in .env"
    }
    
    if ($envContent -match "ANTHROPIC_API_KEY=sk-") {
        Write-Host "  ✅ ANTHROPIC_API_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  ANTHROPIC_API_KEY not properly configured" -ForegroundColor Yellow
        $warnings += "ANTHROPIC_API_KEY not properly configured"
    }
    
    if ($envContent -match "NODE_ENV=") {
        Write-Host "  ✅ NODE_ENV configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  NODE_ENV not configured" -ForegroundColor Yellow
        $warnings += "NODE_ENV not configured"
    }
} else {
    Write-Host "  ❌ .env file missing" -ForegroundColor Red
    $errors += ".env file missing"
}

Write-Host "`n🚀 Application Startup Test..." -ForegroundColor Cyan

# Test if the application starts (quick test)
Write-Host "  🧪 Testing application startup..." -ForegroundColor Gray

$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    node dist/index.js
}

Start-Sleep -Seconds 3

if ($job.State -eq "Running") {
    Write-Host "  ✅ Application starts successfully" -ForegroundColor Green
    Stop-Job $job
    Remove-Job $job
} else {
    Write-Host "  ❌ Application failed to start" -ForegroundColor Red
    $jobOutput = Receive-Job $job -ErrorAction SilentlyContinue
    if ($jobOutput) {
        Write-Host "  Error output: $jobOutput" -ForegroundColor Red
    }
    Remove-Job $job -Force
    $errors += "Application startup failed"
}

Write-Host "`n📊 Health Check Summary" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Yellow

if ($errors.Count -eq 0) {
    Write-Host "🎉 HEALTH CHECK PASSED!" -ForegroundColor Green
    Write-Host "   Your Auto Marketing Agent is healthy and ready to run!" -ForegroundColor Green
} else {
    Write-Host "❌ HEALTH CHECK FAILED!" -ForegroundColor Red
    Write-Host "   Found $($errors.Count) error(s):" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "   • $error" -ForegroundColor Red
    }
}

if ($warnings.Count -gt 0) {
    Write-Host "`n⚠️  Warnings ($($warnings.Count)):" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "   • $warning" -ForegroundColor Yellow
    }
}

Write-Host "`n🛠️  Available Commands:" -ForegroundColor Cyan
Write-Host "   npm run dev          - Start development server" -ForegroundColor White
Write-Host "   npm run dev:watch    - Start with auto-reload" -ForegroundColor White
Write-Host "   npm run build        - Build for production" -ForegroundColor White
Write-Host "   npm run start        - Start production server" -ForegroundColor White
Write-Host "   npm run type-check   - Check TypeScript types" -ForegroundColor White
Write-Host "   npm run format       - Format code with Prettier" -ForegroundColor White

Write-Host "`n✨ To start development:" -ForegroundColor Green
Write-Host "   npm run dev" -ForegroundColor White

if ($errors.Count -eq 0) {
    exit 0
} else {
    exit 1
}
