@echo off
REM Auto Marketing Project Setup Script
echo Setting up Auto Marketing project environment...

REM Ensure the local bin directory is in PATH
set "LOCAL_BIN=C:\Users\Phill\.local\bin"
echo %PATH% | find /i "%LOCAL_BIN%" >nul
if errorlevel 1 (
    echo Adding %LOCAL_BIN% to PATH...
    set "PATH=%PATH%;%LOCAL_BIN%"
    setx PATH "%PATH%" >nul 2>&1
) else (
    echo Local bin directory already in PATH
)

REM Change to project directory
cd /d "C:\Auto Marketing"
echo Current directory: %CD%

REM Check if Claude is available
claude --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Claude command not found. Make sure @anthropic-ai/claude-code is installed.
    echo Run: npm install -g @anthropic-ai/claude-code
) else (
    echo Claude Code is available and ready to use!
    claude --version
)

echo.
echo Setup complete! You can now use Claude commands.
echo.
pause
