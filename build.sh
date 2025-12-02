#!/bin/bash
# Build script for PyxelNyx v3.0 GUI using PyInstaller
# This script handles the compilation process on macOS and Linux

echo "======================================"
echo "PyxelNyx v3.0 - Build Script"
echo "======================================"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller is not installed."
    echo "Installing PyInstaller..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyInstaller. Please install it manually:"
        echo "   pip install pyinstaller"
        exit 1
    fi
fi

echo "✓ PyInstaller is available"
echo ""

# Check if logo.png exists
if [ ! -f "logo.png" ]; then
    echo "⚠️  Warning: logo.png not found. The app will build without a logo."
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist __pycache__ *.pyc
rm -rf *.spec.bak
echo "✓ Cleaned build directories"
echo ""

# Build using the spec file
echo "Building executable using PyxelNyx.spec..."
echo ""
pyinstaller PyxelNyx.spec --clean

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Build completed successfully!"
    echo "======================================"
    echo ""
    
    # Platform-specific instructions
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Your macOS application is ready:"
        echo "  Location: dist/PyxelNyx.app"
        echo ""
        echo "To run the application:"
        echo "  open dist/PyxelNyx.app"
        echo ""
        echo "To remove quarantine attribute (if needed):"
        echo "  xattr -cr dist/PyxelNyx.app"
    else
        echo "Your Linux executable is ready:"
        echo "  Location: dist/PyxelNyx"
        echo ""
        echo "To run the application:"
        echo "  ./dist/PyxelNyx"
        echo ""
        echo "Make sure it's executable:"
        echo "  chmod +x dist/PyxelNyx"
    fi
    
    echo ""
    echo "📦 Build files:"
    ls -lh dist/
else
    echo ""
    echo "======================================"
    echo "❌ Build failed!"
    echo "======================================"
    echo ""
    echo "Please check the error messages above for details."
    echo "Common issues:"
    echo "  1. Missing dependencies - run: pip install -r requirements.txt"
    echo "  2. Incorrect Python version - requires Python 3.8+"
    echo "  3. Missing files - ensure all source files are present"
    echo ""
    exit 1
fi
