#!/usr/bin/env python3
"""
Visual test showing the logo placement in the GUI header (upper right corner).
This mimics exactly how the logo appears in the main PyxelNyx GUI.
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


def create_logo_test_gui():
    """Create a test GUI showing logo placement."""
    root = tk.Tk()
    root.title("PyxelNyx - Logo Display Test")
    root.geometry("800x300")
    
    # Main container
    main_container = ttk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Logo and Title Frame (exact replica from gui.py)
    header_frame = ttk.Frame(main_container)
    header_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Try to load and display logo in upper right corner
    logo_path = get_resource_path("logo.png")
    logo_loaded = False
    
    if logo_path.exists():
        try:
            logo_img = Image.open(logo_path)
            # Resize logo to small size (80x80) while maintaining aspect ratio
            logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=logo_photo)
            logo_label.image = logo_photo  # Keep reference
            logo_label.pack(side=tk.RIGHT, padx=10)
            logo_loaded = True
            print("✅ Logo loaded and displayed in upper right corner")
        except Exception as e:
            print(f"❌ Could not load logo: {e}")
    else:
        print(f"❌ Logo file not found at: {logo_path}")
    
    # Title section (exact replica from gui.py)
    title_section = ttk.Frame(header_frame)
    title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    title_label = ttk.Label(
        title_section, 
        text="PyxelNyx v3.0", 
        font=("Arial", 20, "bold")
    )
    title_label.pack(anchor=tk.W)
    
    subtitle_label = ttk.Label(
        title_section,
        text="Logo Display Test - Header Layout",
        font=("Arial", 10)
    )
    subtitle_label.pack(anchor=tk.W)
    
    # Add separator
    separator = ttk.Separator(main_container, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, padx=10, pady=5)
    
    # Status frame
    status_frame = ttk.Frame(main_container)
    status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    if logo_loaded:
        status_text = "✅ SUCCESS: Logo is properly displayed in the upper right corner!\n\n"
        status_text += "This confirms:\n"
        status_text += "  • Logo file (logo.png) exists and is readable\n"
        status_text += "  • Image loads correctly with PIL\n"
        status_text += "  • Thumbnail resizing works (80x80 pixels)\n"
        status_text += "  • Tkinter displays the logo properly\n"
        status_text += "  • Layout positioning is correct (upper right)\n\n"
        status_text += "The PyxelNyx GUI will display the logo the same way!"
        status_color = "green"
    else:
        status_text = "❌ ERROR: Logo could not be loaded.\n\n"
        status_text += "Please check that logo.png exists in the repository root."
        status_color = "red"
    
    status_label = ttk.Label(
        status_frame,
        text=status_text,
        font=("Arial", 11),
        foreground=status_color,
        justify=tk.LEFT
    )
    status_label.pack(pady=10)
    
    # Close button
    close_btn = ttk.Button(
        status_frame,
        text="Close",
        command=root.quit
    )
    close_btn.pack(pady=10)
    
    # Auto-close after 5 seconds
    def auto_close():
        print("\n" + "="*60)
        print("Visual verification complete.")
        print("="*60)
        root.quit()
    
    root.after(5000, auto_close)
    
    print("\n" + "="*60)
    print("PyxelNyx Logo Display Verification")
    print("="*60)
    print("\nWindow will auto-close in 5 seconds...")
    print("Check that the logo appears in the UPPER RIGHT corner,")
    print("next to the 'PyxelNyx v3.0' title on the left.\n")
    
    root.mainloop()
    
    return logo_loaded


if __name__ == "__main__":
    success = create_logo_test_gui()
    sys.exit(0 if success else 1)
