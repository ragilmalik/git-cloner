@echo off
REM RagilmalikGitCloner - Build Script (PORTABLE VERSION WITH BUNDLED GIT)
REM Builds the Windows executable with bundled MinGit

echo ========================================================================
echo RagilmalikGitCloner - Portable Build Script
echo ========================================================================
echo.

echo This script will build a TRULY PORTABLE .exe with bundled Git!
echo No Git installation needed on target machines!
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate: venv\Scripts\activate
    echo Then install: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check for MinGit
echo.

echo [2/5] Checking for MinGit (portable Git)...

if not exist "git_portable\" (
    echo.
    echo [NOTICE] MinGit not found! Downloading now...
    echo This is a one-time download (~50 MB)
    echo.
    python download_mingit.py

    if errorlevel 1 (
        echo.
        echo [ERROR] MinGit download failed!
        echo Please run manually: python download_mingit.py
        pause
        exit /b 1
    )
) else (
    echo [OK] MinGit found: git_portable\
)

REM Install/update dependencies
echo.

echo [3/5] Installing/updating dependencies...
pip install -r requirements.txt --quiet

REM Clean previous build
echo.

echo [4/5] Cleaning previous build...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist
if exist "RagilmalikGitCloner.spec" del RagilmalikGitCloner.spec

REM Build executable
echo.

echo [5/5] Building portable executable...
echo This may take 3-5 minutes...
echo.
pyinstaller build_exe.spec

REM Check if build succeeded
if exist "dist\RagilmalikGitCloner\RagilmalikGitCloner.exe" (
    echo.
    echo ========================================================================
    echo [SUCCESS] Portable build completed!
    echo ========================================================================
    echo.
    echo Executable location: dist\RagilmalikGitCloner\
    echo.
    dir "dist\RagilmalikGitCloner" /s
    echo.
    echo ========================================================================
    echo IMPORTANT: The ENTIRE folder must be kept together!
    echo ========================================================================
    echo.
    echo Distribution structure:
    echo   dist\RagilmalikGitCloner\
    echo   ├── RagilmalikGitCloner.exe    (Application)
    echo   └── git_portable\         (Bundled Git)
    echo.
    echo Total size: ~130-150 MB
    echo.
    echo This folder is TRULY PORTABLE:
    echo   - Copy the entire dist\RagilmalikGitCloner\ folder to any Windows 10+ PC
    echo   - No Python installation needed
    echo   - No Git installation needed
    echo   - Just run RagilmalikGitCloner.exe!
    echo.
    echo You can now test the application:
    echo   cd dist\RagilmalikGitCloner
    echo   RagilmalikGitCloner.exe
    echo.
) else (
    echo.
    echo ========================================================================
    echo [ERROR] Build failed!
    echo ========================================================================
    echo Please check the error messages above.
    echo.
)

pause