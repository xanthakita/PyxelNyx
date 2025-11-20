#!/usr/bin/env python3
"""
Test script to verify logo.png displays correctly in the PyxelNyx GUI.
"""
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def get_resource_path(relative_path):
    """Get absolute path to resource."""
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent
    return base_path / relative_path


def test_logo_display():
    """Test that the logo can be loaded and displayed."""
    print("=" * 60)
    print("PyxelNyx Logo Display Test")
    print("=" * 60)
    
    # Check if logo file exists
    logo_path = get_resource_path("logo.png")
    print(f"\n1. Checking logo path: {logo_path}")
    
    if not logo_path.exists():
        print(f"   ❌ ERROR: Logo file not found at {logo_path}")
        return False
    else:
        print(f"   ✅ Logo file exists")
        print(f"   Size: {logo_path.stat().st_size / 1024:.2f} KB")
    
    # Test loading the image
    print("\n2. Testing image loading with PIL...")
    try:
        logo_img = Image.open(logo_path)
        print(f"   ✅ Successfully loaded image")
        print(f"   Original size: {logo_img.size[0]}x{logo_img.size[1]} pixels")
        print(f"   Format: {logo_img.format}")
        print(f"   Mode: {logo_img.mode}")
    except Exception as e:
        print(f"   ❌ ERROR loading image: {e}")
        return False
    
    # Test thumbnail resize
    print("\n3. Testing thumbnail resize to 80x80...")
    try:
        logo_img_copy = logo_img.copy()
        logo_img_copy.thumbnail((80, 80), Image.Resampling.LANCZOS)
        print(f"   ✅ Successfully resized to {logo_img_copy.size[0]}x{logo_img_copy.size[1]} pixels")
    except Exception as e:
        print(f"   ❌ ERROR resizing image: {e}")
        return False
    
    # Test Tkinter display
    print("\n4. Testing Tkinter display...")
    try:
        root = tk.Tk()
        root.title("PyxelNyx Logo Test")
        root.geometry("400x200")
        
        # Create frame
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add label
        info_label = ttk.Label(frame, text="Testing logo display...", font=("Arial", 12))
        info_label.pack(pady=10)
        
        # Load and display logo
        logo_img = Image.open(logo_path)
        logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        
        logo_label = ttk.Label(frame, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference!
        logo_label.pack(pady=10)
        
        result_label = ttk.Label(
            frame, 
            text="✅ Logo loaded successfully!\nIf you can see the logo above, the test passed.",
            font=("Arial", 10),
            foreground="green"
        )
        result_label.pack(pady=10)
        
        # Auto-close after 3 seconds
        def close_window():
            print("   ✅ Logo displayed successfully in Tkinter window")
            root.quit()
            root.destroy()
        
        root.after(3000, close_window)
        root.mainloop()
        
    except Exception as e:
        print(f"   ❌ ERROR displaying in Tkinter: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("The logo.png is properly configured and displays correctly.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_logo_display()
    sys.exit(0 if success else 1)
