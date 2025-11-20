#!/usr/bin/env python3
"""
Test script to verify GUI loads with logo properly displayed.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import GUI
from gui import HumanBlurGUI, get_resource_path

def test_logo():
    """Test if logo file can be loaded."""
    logo_path = get_resource_path("logo.png")
    print(f"Logo path: {logo_path}")
    print(f"Logo exists: {logo_path.exists()}")
    if logo_path.exists():
        print(f"Logo size: {logo_path.stat().st_size} bytes")
    return logo_path.exists()

def test_gui_launch():
    """Test GUI launch with logo."""
    print("Testing GUI launch...")
    root = tk.Tk()
    
    # Create GUI instance
    app = HumanBlurGUI(root)
    
    # Check if logo was loaded
    if hasattr(app, 'logo_photo'):
        print("✓ Logo successfully loaded and displayed!")
        print(f"  Logo photo object: {app.logo_photo}")
    else:
        print("✗ Logo was not loaded")
    
    # Schedule window close after 2 seconds
    root.after(2000, root.destroy)
    
    # Run GUI briefly
    root.mainloop()
    print("GUI test completed")

if __name__ == "__main__":
    print("=" * 50)
    print("PyxelNyx GUI Logo Test")
    print("=" * 50)
    print()
    
    # Test 1: Check logo file
    print("Test 1: Checking logo file...")
    logo_exists = test_logo()
    print()
    
    if logo_exists:
        # Test 2: Launch GUI
        print("Test 2: Launching GUI with logo...")
        test_gui_launch()
    else:
        print("✗ Cannot test GUI - logo file not found")
    
    print()
    print("=" * 50)
    print("Test completed")
    print("=" * 50)
