@echo off
echo ==========================================
echo   Claude Code Setup with Bypass Mode
echo ==========================================
echo.

REM Set working directory
cd /d "C:\Auto Marketing"
echo Current directory: %CD%
echo.

REM Check if Claude is installed
echo [1/6] Checking Claude Code installation...
claude --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Claude Code not found. Installing...
    npm install -g @anthropic-ai/claude-code
    if errorlevel 1 (
        echo FAILED to install Claude Code
        pause
        exit /b 1
    )
) else (
    echo ✓ Claude Code is installed
)

REM Add local bin to PATH if not already there
echo [2/6] Configuring PATH...
echo %PATH% | find /i "C:\Users\Phill\.local\bin" >nul
if errorlevel 1 (
    echo Adding local bin to PATH...
    setx PATH "%PATH%;C:\Users\Phill\.local\bin" >nul 2>&1
    set "PATH=%PATH%;C:\Users\Phill\.local\bin"
    echo ✓ PATH updated
) else (
    echo ✓ PATH already configured
)

REM Install project dependencies
echo [3/6] Installing project dependencies...
npm install
if errorlevel 1 (
    echo WARNING: Some dependencies failed to install
) else (
    echo ✓ Dependencies installed
)

REM Build the project
echo [4/6] Building TypeScript project...
npm run build
if errorlevel 1 (
    echo WARNING: Build failed
) else (
    echo ✓ Project built successfully
)

REM Check environment configuration
echo [5/6] Checking environment configuration...
if exist ".env" (
    echo ✓ Environment file exists
    findstr /c:"ANTHROPIC_API_KEY" .env >nul
    if errorlevel 1 (
        echo WARNING: API key not found in .env
    ) else (
        echo ✓ API key configured
    )
) else (
    echo WARNING: .env file not found
)

REM Test Claude Code
echo [6/6] Testing Claude Code...
claude --help >nul 2>&1
if errorlevel 1 (
    echo ERROR: Claude Code test failed
) else (
    echo ✓ Claude Code is working
)

echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo You can now run Claude Code with bypass permissions:
echo.
echo   claude --dangerously-skip-permissions
echo   claude --dangerously-skip-permissions --verbose
echo.
echo SECURITY WARNING:
echo These commands bypass permission checks. Use only in
echo a secure, isolated environment!
echo.
echo Available npm commands:
echo   npm run dev       - Start development server
echo   npm run build     - Build for production
echo   npm run start     - Start production server
echo.
pause
