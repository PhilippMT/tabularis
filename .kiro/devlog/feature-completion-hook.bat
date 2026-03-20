@echo off
REM Feature Completion Hook (Windows)
REM Automatically captures feature milestones when code is committed
REM Usage: feature-completion-hook.bat "Feature Name" "feature-branch-name"

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "DEVLOG_FILE=%SCRIPT_DIR%DEVLOG.md"

REM Get parameters
set "FEATURE_NAME=%~1"
if "!FEATURE_NAME!"=="" set "FEATURE_NAME=Feature"

REM Get current branch if not specified
if "!FEATURE_BRANCH!"=="" (
    for /f %%a in ('git branch --show-current 2^>nul') do set FEATURE_BRANCH=%%a
)
if "!FEATURE_BRANCH!"=="" set "FEATURE_BRANCH=unknown"

REM Get current date
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set CURRENT_DATE=%%c/%%a/%%b

echo.
echo ========================================
echo Feature Completion Milestone
echo ========================================
echo.

echo Analyzing feature completion...
echo.

REM Get feature branch stats (simplified for Windows)
set COMMITS=0
set FILES=0
set LINES_ADDED=0
set LINES_REMOVED=0

git --version >nul 2>&1
if errorlevel 0 (
    REM Get commit count
    for /f %%a in ('git rev-list --count HEAD 2^>nul') do set COMMITS=%%a
)

echo Feature: !FEATURE_NAME!
echo Branch: !FEATURE_BRANCH!
echo Date: !CURRENT_DATE!
echo Commits: !COMMITS!
echo.

REM Create milestone directory if it doesn't exist
if not exist "!SCRIPT_DIR!.feature-milestones" mkdir "!SCRIPT_DIR!.feature-milestones"

REM Store feature milestone
(
    echo.
    echo ---
    echo.
    echo ### ✨ **Feature Milestone**: !FEATURE_NAME!
    echo **Date**: !CURRENT_DATE!
    echo **Branch**: !FEATURE_BRANCH!
    echo.
    echo **Feature Statistics:**
    echo - **Commits**: !COMMITS!
    echo - **Files Modified**: !FILES!
    echo - **Lines Added**: !LINES_ADDED!
    echo - **Lines Removed**: !LINES_REMOVED!
    echo.
    echo **Status**: Feature implementation complete, ready for code review and testing.
    echo.
) >> "!DEVLOG_FILE!"

echo ✓ Feature milestone recorded
echo.
echo Note: Run 'devlog-update.bat' at the end of your work session to consolidate.
echo.

endlocal
