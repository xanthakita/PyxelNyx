@echo off
REM Build script for PyxelNyx v3.0 GUI using PyInstaller
REM This script handles the compilation process on Windows

echo ======================================
echo PyxelNyx v3.0 - Build Script
echo ======================================
echo.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo X PyInstaller is not installed.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo X Failed to install PyInstaller. Please install it manually:
        echo    pip install pyinstaller
        exit /b 1
    )
)

echo √ PyInstaller is available
echo.

REM Check if logo.png exists
if not exist "logo.png" (
    echo ! Warning: logo.png not found. The app will build without a logo.
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del /f /q *.pyc 2>nul
del /f /q *.spec.bak 2>nul
echo √ Cleaned build directories
echo.

REM Build using the spec file
echo Building executable using PyxelNyx.spec...
echo.
pyinstaller PyxelNyx.spec --clean

REM Check if build was successful
if errorlevel 0 (
    echo.
    echo ======================================
    echo √ Build completed successfully!
    echo ======================================
    echo.
    echo Your Windows executable is ready:
    echo   Location: dist\PyxelNyx.exe
    echo.
    echo To run the application:
    echo   dist\PyxelNyx.exe
    echo.
    echo.
    echo Build files:
    dir /b dist\
) else (
    echo.
    echo ======================================
    echo X Build failed!
    echo ======================================
    echo.
    echo Please check the error messages above for details.
    echo Common issues:
    echo   1. Missing dependencies - run: pip install -r requirements.txt
    echo   2. Incorrect Python version - requires Python 3.8+
    echo   3. Missing files - ensure all source files are present
    echo.
    exit /b 1
)
