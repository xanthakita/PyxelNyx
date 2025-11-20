#!/usr/bin/env python3
"""
Simple test to verify logo file and path resolution.
"""

import sys
from pathlib import Path

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for both development and PyInstaller frozen mode.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # Running in normal Python environment
        base_path = Path(__file__).parent
    
    return base_path / relative_path

def test_logo():
    """Test if logo file can be loaded."""
    print("=" * 60)
    print("PyxelNyx GUI Logo Path Test")
    print("=" * 60)
    print()
    
    logo_path = get_resource_path("logo.png")
    print(f"✓ Logo path resolution: {logo_path}")
    print(f"✓ Logo exists: {logo_path.exists()}")
    
    if logo_path.exists():
        size_bytes = logo_path.stat().st_size
        size_kb = size_bytes / 1024
        print(f"✓ Logo file size: {size_kb:.1f} KB ({size_bytes} bytes)")
        
        # Try to load with PIL
        try:
            from PIL import Image
            img = Image.open(logo_path)
            print(f"✓ Logo dimensions: {img.size[0]}x{img.size[1]} pixels")
            print(f"✓ Logo format: {img.format}")
            print(f"✓ Logo mode: {img.mode}")
            print()
            print("=" * 60)
            print("✓ ALL TESTS PASSED - Logo is ready to display!")
            print("=" * 60)
            return True
        except Exception as e:
            print(f"✗ Error loading logo image: {e}")
            return False
    else:
        print("✗ Logo file not found!")
        return False

if __name__ == "__main__":
    success = test_logo()
    sys.exit(0 if success else 1)
