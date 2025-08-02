@echo off
echo ===========================================
echo    Permanent PATH Fix for Claude Code
echo ===========================================
echo.

set "LOCAL_BIN=C:\Users\Phill\.local\bin"

echo Target: User-specific PATH modification
echo Path to add: %LOCAL_BIN%
echo.

REM Check if path already exists
echo %PATH% | find /i "%LOCAL_BIN%" >nul
if not errorlevel 1 (
    echo ✓ Path already exists in current session PATH!
    goto :check_permanent
)

echo Current session does not include the path.
echo.

:check_permanent
REM Check permanent PATH via registry
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%B"

echo %USER_PATH% | find /i "%LOCAL_BIN%" >nul
if not errorlevel 1 (
    echo ✓ Path already exists in permanent user PATH!
    echo No registry changes needed.
    goto :verify
)

echo Adding path to permanent user PATH...
setx PATH "%PATH%;%LOCAL_BIN%" /M >nul 2>&1
if errorlevel 1 (
    echo Trying user-level setx...
    setx PATH "%PATH%;%LOCAL_BIN%" >nul 2>&1
    if errorlevel 1 (
        echo ❌ Failed to set permanent PATH
        echo Please run as Administrator or use the PowerShell version
        goto :manual_instructions
    )
)

echo ✓ Successfully added to permanent user PATH!
echo.

:verify
echo ===========================================
echo    Verification
echo ===========================================
echo.

REM Check if directory exists
if exist "%LOCAL_BIN%" (
    echo ✓ Directory exists: %LOCAL_BIN%
) else (
    echo ⚠️ Directory does not exist: %LOCAL_BIN%
    echo Creating directory...
    mkdir "%LOCAL_BIN%" 2>nul
    if exist "%LOCAL_BIN%" (
        echo ✓ Directory created successfully
    ) else (
        echo ❌ Failed to create directory
    )
)

REM Test Claude Code
claude --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Claude Code not found in current session
    echo This is normal - restart your terminal to see changes
) else (
    echo ✓ Claude Code is accessible in current session
)

goto :next_steps

:manual_instructions
echo.
echo ===========================================
echo    Manual Instructions
echo ===========================================
echo.
echo If automatic PATH setting failed, manually add:
echo %LOCAL_BIN%
echo.
echo Via System Properties:
echo 1. Right-click "This PC" ^> Properties
echo 2. Click "Advanced system settings"
echo 3. Click "Environment Variables"
echo 4. In "User variables", select "Path" and click "Edit"
echo 5. Click "New" and add: %LOCAL_BIN%
echo 6. Click OK on all dialogs
echo.

:next_steps
echo ===========================================
echo    Next Steps
echo ===========================================
echo.
echo 1. RESTART your terminal/command prompt
echo 2. Or close and reopen VS Code
echo 3. Test with: claude --version
echo.
echo If you still see PATH warnings after restart:
echo • Run fix-path-permanent.ps1 as Administrator
echo • Or manually add via System Properties
echo.
echo Commands to test after restart:
echo   claude --version
echo   claude --help
echo   claude --dangerously-skip-permissions
echo.
echo ✅ PATH fix complete! Restart your terminal to see changes.
echo.
pause
