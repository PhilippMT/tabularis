@echo off
REM Development Log Auto-Update Script (Windows)
REM Automatically captures and summarizes daily development progress
REM Usage: devlog-update.bat

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "DEVLOG_FILE=%SCRIPT_DIR%DEVLOG.md"

echo.
echo ========================================
echo Development Log Update System
echo ========================================
echo.

REM Get current date
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set DATE=%%c/%%a/%%b
for /f "tokens=1 delims= " %%a in ('time /t') do set TIME=%%a

echo.
echo Please provide information about today's work:
echo.

set /p WORK_FOCUS="1. What did you work on today? (Features, bugs, refactoring, etc.): "
set /p HOURS_SPENT="2. How much time did you spend? (Total hours): "
if "!HOURS_SPENT!"=="" set HOURS_SPENT=0

set /p ACCOMPLISHMENTS="3. What were your main accomplishments?: "
set /p CHALLENGES="4. Any challenges or blockers? (Optional - press Enter to skip): "
set /p DECISIONS="5. Key technical decisions made? (Optional): "
set /p NEXT_STEPS="6. What's planned for the next session?: "
set /p LEARNINGS="7. Any new learnings or insights? (Optional): "
set /p KIRO_USAGE="8. Which Kiro prompts were most helpful? (Optional): "

echo.
echo Analyzing git activity...
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo Note: Git not found or not in PATH - skipping git analysis
    set COMMITS=0
    set LINES_ADDED=0
    set LINES_REMOVED=0
) else (
    REM Get commits for today
    for /f %%a in ('git log --since=%DATE% --oneline 2^>nul ^| find /c /v ""') do set COMMITS=%%a
    if "!COMMITS!"=="" set COMMITS=0
    
    REM Get basic statistics (simplified for Windows batch)
    set LINES_ADDED=0
    set LINES_REMOVED=0
)

echo Today's Commits: !COMMITS!
echo Lines added: !LINES_ADDED!
echo Lines removed: !LINES_REMOVED!
echo.

REM Create temporary entry file
setlocal enabledelayedexpansion
(
    echo.
    echo ## !DATE! - !WORK_FOCUS! [!HOURS_SPENT!h]
    echo.
    echo ### 📊 **Daily Metrics**
    echo - **Time Spent**: !HOURS_SPENT! hours
    echo - **Commits Made**: !COMMITS!
    echo - **Lines Added**: !LINES_ADDED!
    echo - **Lines Removed**: !LINES_REMOVED!
    echo - **Net Lines**: !LINES_ADDED-LINES_REMOVED!
    echo.
    echo ### 🎯 **Accomplishments**
    echo - !ACCOMPLISHMENTS!
    echo.
    echo ### 💻 **Technical Progress**
    echo **Recent Commits:**
    echo - Commits: !COMMITS!
    echo - Files modified: [will update]
    echo.
    echo ### 🚧 **Challenges ^& Solutions**
    if "!CHALLENGES!"=="" (
        echo No significant challenges today.
    ) else (
        echo !CHALLENGES!
    )
    echo.
    echo ### 🧠 **Key Decisions**
    if "!DECISIONS!"=="" (
        echo No major architectural decisions made today.
    ) else (
        echo !DECISIONS!
    )
    echo.
    echo ### 📚 **Learnings ^& Insights**
    if "!LEARNINGS!"=="" (
        echo Continued building on existing knowledge.
    ) else (
        echo !LEARNINGS!
    )
    echo.
    echo ### ⚡ **Kiro CLI Usage**
    if "!KIRO_USAGE!"=="" (
        echo Standard prompt usage during development.
    ) else (
        echo !KIRO_USAGE!
    )
    echo.
    echo ### 📋 **Next Session Plan**
    echo - !NEXT_STEPS!
    echo.
    echo ---
    echo.
) > "%TEMP%\devlog_entry.txt"

REM Append entry to DEVLOG.md
echo Appending entry to devlog...
echo.

type "%TEMP%\devlog_entry.txt" >> "!DEVLOG_FILE!"

echo ========================================
echo Development log updated successfully!
echo ========================================
echo.
echo 📊 Today's Summary:
echo Focus: !WORK_FOCUS!
echo Time: !HOURS_SPENT!h
echo Commits: !COMMITS!
echo Code changes: +!LINES_ADDED!, -!LINES_REMOVED!
echo.

endlocal
