#!/bin/bash
# Build JARVIS as a macOS application

echo "=================================="
echo "  Building J.A.R.V.I.S. macOS App"
echo "=================================="

# Check for py2app
if ! pip show py2app > /dev/null 2>&1; then
    echo "Installing py2app..."
    pip install py2app
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "Building application..."
python setup.py py2app

if [ -d "dist/JARVIS.app" ]; then
    echo ""
    echo "=================================="
    echo "  Build successful!"
    echo "=================================="
    echo ""
    echo "Application created at: dist/JARVIS.app"
    echo ""
    echo "To run: open dist/JARVIS.app"
    echo "Or drag to Applications folder to install."
else
    echo ""
    echo "Build failed. Check errors above."
    exit 1
fi
