#!/usr/bin/env python3
"""
Human Blur GUI Tool - Enhanced Graphical Interface
A comprehensive GUI for the human blur tool with advanced features.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import sys
import os
import platform
import subprocess
from blur_humans import HumanBlurProcessor
from PIL import Image, ImageTk


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for both development and PyInstaller frozen mode.
    
    Args:
        relative_path: Relative path to resource file
        
    Returns:
        Absolute path to resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # Running in normal Python environment
        base_path = Path(__file__).parent
    
    return base_path / relative_path


class HelpDialog:
    """Help dialog showing instructions for both GUI and CLI usage."""
    
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Help - PyxelNyx")
        self.dialog.geometry("700x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # GUI Help Tab
        gui_frame = ttk.Frame(notebook)
        notebook.add(gui_frame, text="GUI Usage")
        
        gui_text = scrolledtext.ScrolledText(gui_frame, wrap=tk.WORD, width=80, height=30)
        gui_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        gui_help = """PyxelNyx - GUI Usage Guide

OVERVIEW
--------
The PyxelNyx automatically detects and masks/blurs humans in images 
and videos using advanced AI (YOLOv8 segmentation).

GETTING STARTED
---------------
1. Select Input:
   - Click "Browse File" to process a single image or video
   - Click "Browse Folder" to batch process multiple files

2. Choose Mask Type:
   - Black Mask (Default): Replaces humans with solid black silhouettes
   - Blur: Applies intelligent blur following human contours

3. Adjust Settings (Optional):
   - Blur Intensity: How strong the blur effect is (51-301)
   - Blur Passes: Number of blur iterations for stronger effect (1-10)
   - Confidence: Detection sensitivity (0.1-1.0, default 0.33)
   - Model: Choose speed vs accuracy trade-off

4. Configure Output Settings (Optional):
   - Filename Suffix: Customize the suffix added to output files
     (e.g., '-background', '-blurred', '-processed')
   - Frame Interval: For videos, process every Nth frame (1-15)
     • 1 = process every frame (default, no skipping)
     • 3 = process every 3rd frame (faster, lower output frame rate)
     • 15 = process every 15th frame (fastest, lowest output frame rate)
   - Audio Handling: Choose whether to keep or remove audio from videos
     (Requires ffmpeg; automatically disabled when frame skipping is enabled)

5. Click "Process Media" button

6. View progress and results

SUPPORTED FORMATS
-----------------
Images: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .webp, .heic, .heif
Videos: .mp4, .mov

OUTPUT
------
Processed files are saved with a custom suffix (default "-background"):
- photo.jpg → photo[suffix].jpg
- video.mp4 → video[suffix].mp4

You can customize this suffix in the Output Settings section.
Original files are never modified!

SINGLE FILE PROCESSING
----------------------
After processing completes, you'll be prompted to open the processed file.

BATCH PROCESSING
----------------
When processing a folder:
- Individual progress shows current file processing
- Overall progress shows total batch progress
- Summary appears at the end

TIPS
----
• For speed: Use default yolov8n-seg.pt model
• For accuracy: Use yolov8m-seg.pt or higher
• Lower confidence (0.3): Detect more people (more false positives)
• Higher confidence (0.7): Stricter detection (fewer false positives)
• Black mask mode is fastest

ERRORS
------
If you encounter unsupported file errors, please contact:
apps@globalemancipation.ngo
"""
        gui_text.insert('1.0', gui_help)
        gui_text.config(state='disabled')
        
        # CLI Help Tab
        cli_frame = ttk.Frame(notebook)
        notebook.add(cli_frame, text="CLI Usage")
        
        cli_text = scrolledtext.ScrolledText(cli_frame, wrap=tk.WORD, width=80, height=30)
        cli_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        cli_help = """PyxelNyx - Command Line Usage Guide

BASIC USAGE
-----------
Process a single image with black mask (default):
    python blur_humans.py photo.jpg

Process with blur instead of black mask:
    python blur_humans.py photo.jpg --mask-type blur

Process a video:
    python blur_humans.py video.mp4

Process all files in a directory:
    python blur_humans.py /path/to/media/

ADVANCED OPTIONS
----------------
Use black mask (default):
    python blur_humans.py photo.jpg --mask-type black

Use blur mode:
    python blur_humans.py photo.jpg --mask-type blur

Extreme blur with more passes:
    python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 5

Adjust detection sensitivity:
    python blur_humans.py photo.jpg --confidence 0.7

Use more accurate model (slower):
    python blur_humans.py photo.jpg --model yolov8m-seg.pt

MEDIA TYPE FILTERING
--------------------
Process both images and videos (default):
    python blur_humans.py /path/to/media/

Process only images:
    python blur_humans.py /path/to/media/ --media-type images

Process only videos:
    python blur_humans.py /path/to/media/ --media-type videos

COMMAND-LINE ARGUMENTS
----------------------
input                  Path to image/video file or directory (required)
--media-type          Media filter: 'images', 'videos', 'both' (default: both)
--mask-type, -t       Masking type: 'black' or 'blur' (default: black)
--blur, -b            Blur kernel size 1-301, must be odd (default: 151)
--passes, -p          Number of blur passes 1-10 (default: 3)
--confidence, -c      Detection threshold 0.0-1.0 (default: 0.5)
--model, -m           YOLO model selection (default: yolov8n-seg.pt)
--version, -v         Show version information
--help, -h            Show help message

MODEL SELECTION
---------------
Speed vs Accuracy (Segmentation models recommended):

yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Default, fastest
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Good balance
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Higher accuracy
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Professional use
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Maximum accuracy

EXAMPLES
--------
# Basic black mask (fast, maximum privacy)
python blur_humans.py family_photo.jpg

# Blur mode with custom intensity
python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 4

# Process iPhone HEIC images
python blur_humans.py IMG_1234.HEIC

# Batch process vacation photos
python blur_humans.py ./vacation_photos/

# Process only videos in a folder
python blur_humans.py ./media/ --media-type videos

# High accuracy mode
python blur_humans.py photo.jpg --model yolov8m-seg.pt --confidence 0.7

For more information, visit the README.md file.
"""
        cli_text.insert('1.0', cli_help)
        cli_text.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(self.dialog, text="Close", command=self.dialog.destroy)
        close_btn.pack(pady=10)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()


class HumanBlurGUI:
    """
    Enhanced GUI application for human blur tool with comprehensive features.
    """
    
    def __init__(self, root):
        """Initialize the enhanced GUI application."""
        self.root = root
        self.root.title("PyxelNyx v3.0 - Enhanced")
        # Set initial size and minimum size - compact to fit on standard screens
        self.root.geometry("1000x720")
        self.root.minsize(950, 650)
        self.root.resizable(True, True)
        
        # Variables
        self.input_path = tk.StringVar()
        self.mask_type = tk.StringVar(value="black")
        self.blur_intensity = tk.IntVar(value=151)
        self.blur_passes = tk.IntVar(value=3)
        self.confidence = tk.DoubleVar(value=0.33)
        self.model_name = tk.StringVar(value="yolov8n-seg.pt")
        self.media_type = tk.StringVar(value="both")
        self.keep_audio = tk.BooleanVar(value=True)  # New: Audio handling option
        self.filename_suffix = tk.StringVar(value="-background")  # New: Custom filename suffix
        self.frame_interval = tk.IntVar(value=1)  # New: Frame skipping interval (1 = every frame)
        self.processing = False
        self.last_output_path = None
        
        # Batch processing variables
        self.current_file_progress = tk.DoubleVar(value=0)
        self.overall_progress = tk.DoubleVar(value=0)
        self.current_file_name = tk.StringVar(value="")
        self.current_file_percentage = tk.StringVar(value="0%")  # Progress percentage text
        
        # Supported formats
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}
        self.supported_video_formats = {'.mp4', '.mov'}
        self.supported_formats = self.supported_image_formats | self.supported_video_formats
        
        # Setup UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Logo and Title Frame
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, padx=10, pady=(5, 3))
        
        # Try to load and display logo
        logo_path = get_resource_path("logo.png")
        if logo_path.exists():
            try:
                logo_img = Image.open(logo_path)
                # Resize logo to small size (100x100)
                logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(header_frame, image=self.logo_photo)
                logo_label.pack(side=tk.RIGHT, padx=10)
            except Exception as e:
                print(f"Could not load logo: {e}")
        
        # Title section
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
            text="AI-Powered Privacy Protection for Images & Videos", 
            font=("Arial", 10)
        )
        subtitle_label.pack(anchor=tk.W)
        
        # Separator
        ttk.Separator(main_container, orient='horizontal').pack(fill=tk.X, padx=10, pady=3)
        
        # Main content frame with grid layout
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(3, 8))
        
        # Configure grid columns with equal weight for resizing
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        # Configure rows to expand
        content_frame.rowconfigure(1, weight=1)
        content_frame.rowconfigure(2, weight=1)
        
        # ========== File/Folder Selection Section (Full Width - Row 0) ==========
        input_section = ttk.LabelFrame(content_frame, text="Input Selection", padding="8")
        input_section.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6), padx=5)
        
        ttk.Label(input_section, text="Select file or folder to process:").pack(anchor=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(input_section)
        input_frame.pack(fill=tk.X)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, width=50)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse File", command=self.browse_file, width=12).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(input_frame, text="Browse Folder", command=self.browse_folder, width=12).pack(
            side=tk.LEFT
        )
        
        # Media Type Filter (for folders)
        media_filter_frame = ttk.Frame(input_section)
        media_filter_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(media_filter_frame, text="Folder media filter:").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            media_filter_frame, text="Both", variable=self.media_type, value="both"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            media_filter_frame, text="Images Only", variable=self.media_type, value="images"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            media_filter_frame, text="Videos Only", variable=self.media_type, value="videos"
        ).pack(side=tk.LEFT, padx=5)
        
        # ========== ROW 1: Processing Mode (Left) | Blur Settings (Right) ==========
        
        # Processing Mode Section (Left Column - Row 1)
        mask_section = ttk.LabelFrame(content_frame, text="Processing Mode", padding="8")
        mask_section.grid(row=1, column=0, sticky="nsew", pady=(0, 6), padx=(5, 3))
        
        mask_frame = ttk.Frame(mask_section)
        mask_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Radiobutton(
            mask_frame, 
            text="⬛ Black Mask (Recommended for maximum privacy)", 
            variable=self.mask_type, 
            value="black",
            command=self.update_blur_controls
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            mask_frame, 
            text="🌫️  Blur (Intelligent contour-following blur)", 
            variable=self.mask_type, 
            value="blur",
            command=self.update_blur_controls
        ).pack(anchor=tk.W, pady=2)
        
        # Blur Settings Section (Right Column - Row 1)
        blur_settings_frame = ttk.LabelFrame(content_frame, text="Blur Settings (Blur Mode Only)", padding="8")
        blur_settings_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 6), padx=(3, 5))
        
        # Blur Intensity
        intensity_frame = ttk.Frame(blur_settings_frame)
        intensity_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(intensity_frame, text="Intensity:", width=10).pack(side=tk.LEFT)
        self.intensity_slider = ttk.Scale(
            intensity_frame, 
            from_=51, 
            to=301, 
            variable=self.blur_intensity,
            orient=tk.HORIZONTAL
        )
        self.intensity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.intensity_label = ttk.Label(intensity_frame, text="151", width=5)
        self.intensity_label.pack(side=tk.LEFT)
        
        self.blur_intensity.trace_add("write", self.update_intensity_label)
        
        # Blur Passes
        passes_frame = ttk.Frame(blur_settings_frame)
        passes_frame.pack(fill=tk.X)
        
        ttk.Label(passes_frame, text="Passes:", width=10).pack(side=tk.LEFT)
        self.passes_spinbox = ttk.Spinbox(
            passes_frame, 
            from_=1, 
            to=10, 
            textvariable=self.blur_passes,
            width=10
        )
        self.passes_spinbox.pack(side=tk.LEFT)
        ttk.Label(passes_frame, text="(More passes = stronger blur)", 
                 font=("Arial", 8), foreground="gray").pack(side=tk.LEFT, padx=(10, 0))
        
        # ========== ROW 2: Advanced Settings (Left) | Output Settings (Right) ==========
        
        # Advanced Settings Section (Left Column - Row 2)
        advanced_frame = ttk.LabelFrame(content_frame, text="Advanced Settings", padding="8")
        advanced_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 6), padx=(5, 3))
        
        # Confidence
        confidence_frame = ttk.Frame(advanced_frame)
        confidence_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(confidence_frame, text="Confidence:", width=10).pack(side=tk.LEFT)
        self.confidence_slider = ttk.Scale(
            confidence_frame, 
            from_=0.1, 
            to=1.0, 
            variable=self.confidence,
            orient=tk.HORIZONTAL
        )
        self.confidence_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.confidence_label = ttk.Label(confidence_frame, text="0.33", width=5)
        self.confidence_label.pack(side=tk.LEFT)
        
        self.confidence.trace_add("write", self.update_confidence_label)
        
        # Model Selection
        model_frame = ttk.Frame(advanced_frame)
        model_frame.pack(fill=tk.X)
        
        ttk.Label(model_frame, text="Model:", width=10).pack(side=tk.LEFT)
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_name,
            values=[
                "yolov8n-seg.pt",
                "yolov8s-seg.pt",
                "yolov8m-seg.pt",
                "yolov8l-seg.pt",
                "yolov8x-seg.pt"
            ],
            width=18,
            state="readonly"
        )
        model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        model_combo.current(0)
        
        # Output Settings Section (Right Column - Row 2)
        output_frame = ttk.LabelFrame(content_frame, text="Output Settings", padding="8")
        output_frame.grid(row=2, column=1, sticky="nsew", pady=(0, 6), padx=(3, 5))
        
        # Custom Filename Suffix
        suffix_frame = ttk.Frame(output_frame)
        suffix_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(suffix_frame, text="Filename suffix:").pack(anchor=tk.W, pady=(0, 3))
        suffix_entry = ttk.Entry(suffix_frame, textvariable=self.filename_suffix, width=25)
        suffix_entry.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(
            suffix_frame, 
            text="(e.g., '-background', '-blurred', '-processed')", 
            font=("Arial", 8), 
            foreground="gray"
        ).pack(anchor=tk.W)
        
        # Frame Interval Option (for videos)
        frame_interval_frame = ttk.Frame(output_frame)
        frame_interval_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(frame_interval_frame, text="Frame interval (videos):").pack(anchor=tk.W, pady=(0, 3))
        
        interval_control_frame = ttk.Frame(frame_interval_frame)
        interval_control_frame.pack(fill=tk.X, pady=(0, 3))
        
        self.frame_interval_spinbox = ttk.Spinbox(
            interval_control_frame,
            from_=1,
            to=15,
            textvariable=self.frame_interval,
            width=8,
            command=self.update_audio_checkbox_state
        )
        self.frame_interval_spinbox.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Label(
            interval_control_frame,
            text="(1 = every frame, 3 = every 3rd frame)",
            font=("Arial", 8),
            foreground="gray"
        ).pack(side=tk.LEFT)
        
        # Trace frame_interval changes to update audio checkbox
        self.frame_interval.trace_add("write", self.update_audio_checkbox_state)
        
        # Audio Handling Option (for videos)
        audio_frame = ttk.Frame(output_frame)
        audio_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.audio_checkbox = ttk.Checkbutton(
            audio_frame,
            text="🔊 Keep audio in output videos",
            variable=self.keep_audio
        )
        self.audio_checkbox.pack(anchor=tk.W)
        self.audio_info_label = ttk.Label(
            audio_frame,
            text="(requires ffmpeg)",
            font=("Arial", 8),
            foreground="gray"
        )
        self.audio_info_label.pack(anchor=tk.W, padx=(20, 0))
        
        # ========== Action Buttons Section (Full Width - Row 3) ==========
        action_frame = ttk.Frame(content_frame)
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 6), padx=5)
        
        self.process_button = ttk.Button(
            action_frame, 
            text="🚀 Process Media", 
            command=self.process,
            width=20
        )
        self.process_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        help_button = ttk.Button(
            action_frame,
            text="❓ Help",
            command=self.show_help,
            width=15
        )
        help_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # ========== Progress Section (2-Column Layout - Row 4) ==========
        progress_frame = ttk.LabelFrame(content_frame, text="Processing Progress", padding="8")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 5), padx=5)
        
        # Configure 2-column grid for progress bars
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(1, weight=1)
        
        # Left Column: Individual File Progress
        file_progress_frame = ttk.Frame(progress_frame)
        file_progress_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        ttk.Label(file_progress_frame, text="Individual File Progress:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 3))
        
        self.current_file_label = ttk.Label(
            file_progress_frame, 
            textvariable=self.current_file_name,
            font=("Arial", 8),
            foreground="blue"
        )
        self.current_file_label.pack(anchor=tk.W, pady=(0, 3))
        
        # Percentage label above progress bar
        self.file_percentage_label = ttk.Label(
            file_progress_frame,
            textvariable=self.current_file_percentage,
            font=("Arial", 9, "bold"),
            foreground="blue"
        )
        self.file_percentage_label.pack(anchor=tk.W, pady=(0, 2))
        
        self.file_progress = ttk.Progressbar(
            file_progress_frame,
            mode='determinate',
            variable=self.current_file_progress,
            maximum=100
        )
        self.file_progress.pack(fill=tk.X, pady=(0, 5))
        
        # Right Column: Overall Progress
        overall_progress_frame = ttk.Frame(progress_frame)
        overall_progress_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        ttk.Label(overall_progress_frame, text="Overall Progress (Batch):", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 3))
        
        self.overall_label = ttk.Label(overall_progress_frame, text="0%", font=("Arial", 8), foreground="green")
        self.overall_label.pack(anchor=tk.W, pady=(0, 3))
        
        self.overall_progressbar = ttk.Progressbar(
            overall_progress_frame,
            mode='determinate',
            variable=self.overall_progress
        )
        self.overall_progressbar.pack(fill=tk.X, pady=(0, 5))
        
        # Status Label (Full Width below both progress bars)
        self.status_label = ttk.Label(
            progress_frame, 
            text="Ready to process media files", 
            font=("Arial", 9, "bold"),
            foreground="gray"
        )
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Initial update
        self.update_blur_controls()
        
        # Update overall progress label
        self.overall_progress.trace_add("write", self.update_overall_label)
        
        # Update file progress percentage label
        self.current_file_progress.trace_add("write", self.update_file_progress_label)
        
    def update_overall_label(self, *args):
        """Update overall progress percentage label."""
        value = self.overall_progress.get()
        self.overall_label.config(text=f"{int(value)}%")
    
    def update_file_progress_label(self, *args):
        """Update file progress percentage label."""
        value = self.current_file_progress.get()
        self.current_file_percentage.set(f"{int(value)}%")
    
    def progress_callback(self, current: int, total: int):
        """
        Progress callback for file processing.
        Called by HumanBlurProcessor during processing.
        
        Args:
            current: Current frame/step number
            total: Total frames/steps
        """
        if total > 0:
            percentage = (current * 100) / total
            # Use root.after to update GUI from processing thread
            self.root.after(0, lambda: self.current_file_progress.set(percentage))
        
    def show_help(self):
        """Show help dialog."""
        HelpDialog(self.root)
        
    def update_intensity_label(self, *args):
        """Update intensity label when slider changes."""
        value = self.blur_intensity.get()
        # Ensure odd number
        if value % 2 == 0:
            value += 1
            self.blur_intensity.set(value)
        self.intensity_label.config(text=str(value))
        
    def update_confidence_label(self, *args):
        """Update confidence label when slider changes."""
        value = self.confidence.get()
        self.confidence_label.config(text=f"{value:.2f}")
        
    def update_blur_controls(self):
        """Enable/disable blur controls based on mask type."""
        if self.mask_type.get() == "blur":
            self.intensity_slider.config(state="normal")
            self.passes_spinbox.config(state="normal")
        else:
            self.intensity_slider.config(state="disabled")
            self.passes_spinbox.config(state="disabled")
    
    def update_audio_checkbox_state(self, *args):
        """Disable audio checkbox and auto-disable audio when frame skipping is enabled."""
        frame_interval = self.frame_interval.get()
        
        if frame_interval > 1:
            # Disable audio checkbox and set keep_audio to False
            self.audio_checkbox.config(state="disabled")
            self.keep_audio.set(False)
            self.audio_info_label.config(
                text="(audio auto-disabled with frame skipping)",
                foreground="orange"
            )
        else:
            # Enable audio checkbox
            self.audio_checkbox.config(state="normal")
            self.audio_info_label.config(
                text="(requires ffmpeg)",
                foreground="gray"
            )
    
    def validate_file_format(self, file_path: Path) -> bool:
        """
        Validate if file format is supported.
        
        Args:
            file_path: Path to file to validate
            
        Returns:
            True if supported, False otherwise
        """
        return file_path.suffix.lower() in self.supported_formats
    
    def show_unsupported_format_error(self, file_path: Path):
        """Show error message for unsupported file format."""
        error_msg = (
            f"Unsupported File Format\n\n"
            f"The file '{file_path.name}' has an unsupported format.\n\n"
            f"Supported formats:\n"
            f"Images: {', '.join(sorted(self.supported_image_formats))}\n"
            f"Videos: {', '.join(sorted(self.supported_video_formats))}\n\n"
            f"If you need support for additional formats, please contact:\n"
            f"apps@globalemancipation.ngo"
        )
        messagebox.showerror("Unsupported Format", error_msg)
    
    def browse_file(self):
        """Open file dialog to select a media file."""
        filename = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=[
                ("All Supported", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.heic *.heif *.mp4 *.mov"),
                ("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.heic *.heif"),
                ("Videos", "*.mp4 *.mov"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            file_path = Path(filename)
            if not self.validate_file_format(file_path):
                self.show_unsupported_format_error(file_path)
                return
            self.input_path.set(filename)
    
    def browse_folder(self):
        """Open folder dialog to select a directory."""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.input_path.set(folder)
    
    def update_status(self, message, color="gray"):
        """Update status label."""
        self.status_label.config(text=message, foreground=color)
    
    def open_file(self, file_path: Path):
        """
        Open a file using the system's default application.
        
        Args:
            file_path: Path to file to open
        """
        try:
            system = platform.system()
            if system == 'Darwin':  # macOS
                subprocess.run(['open', str(file_path)])
            elif system == 'Windows':
                os.startfile(str(file_path))
            else:  # Linux
                subprocess.run(['xdg-open', str(file_path)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def process_thread(self):
        """Process media files in a separate thread."""
        try:
            input_path = Path(self.input_path.get())
            
            if not input_path.exists():
                self.update_status("Error: Path does not exist", "red")
                messagebox.showerror("Error", "The specified path does not exist.")
                return
            
            # Ensure odd blur intensity
            blur_intensity = self.blur_intensity.get()
            if blur_intensity % 2 == 0:
                blur_intensity += 1
            
            # Get actual model name (remove display text if present)
            model = self.model_name.get().split()[0]  # Get first part before space
            
            # Create processor with new parameters
            processor = HumanBlurProcessor(
                model_name=model,
                blur_intensity=blur_intensity,
                blur_passes=self.blur_passes.get(),
                mask_type=self.mask_type.get(),
                filename_suffix=self.filename_suffix.get(),
                keep_audio=self.keep_audio.get(),
                frame_interval=self.frame_interval.get(),
                progress_callback=self.progress_callback
            )
            
            # Process based on input type
            if input_path.is_file():
                # Validate file format
                if not self.validate_file_format(input_path):
                    self.update_status("Error: Unsupported file format", "red")
                    self.root.after(0, lambda: self.show_unsupported_format_error(input_path))
                    return
                
                # Process single file
                self.current_file_name.set(f"Processing: {input_path.name}")
                self.update_status(f"Processing {input_path.name}...", "blue")
                
                success = processor.process_image(input_path, confidence=self.confidence.get()) if input_path.suffix.lower() in self.supported_image_formats else processor.process_video(input_path, confidence=self.confidence.get())
                
                if success:
                    # Determine output path using custom filename suffix
                    output_suffix = input_path.suffix
                    if output_suffix.lower() in {'.heic', '.heif'}:
                        output_suffix = '.jpg'
                    output_path = input_path.parent / f"{input_path.stem}{self.filename_suffix.get()}{output_suffix}"
                    self.last_output_path = output_path
                    
                    self.update_status(f"✓ Successfully processed {input_path.name}", "green")
                    self.current_file_name.set(f"Completed: {input_path.name}")
                    
                    # Ask if user wants to open the file
                    self.root.after(0, lambda: self.prompt_open_file(output_path))
                else:
                    self.update_status("✗ Processing failed", "red")
                    self.current_file_name.set("")
                    messagebox.showerror("Error", "Processing failed. Check console for details.")
            
            elif input_path.is_dir():
                # Process directory
                self.update_status("Processing directory...", "blue")
                self.current_file_name.set("Scanning directory...")
                
                # Get files to process
                formats_to_scan = self.supported_formats
                if self.media_type.get() == "images":
                    formats_to_scan = self.supported_image_formats
                elif self.media_type.get() == "videos":
                    formats_to_scan = self.supported_video_formats
                
                media_files = []
                for ext in formats_to_scan:
                    media_files.extend(list(input_path.glob(f"*{ext}")) + list(input_path.glob(f"*{ext.upper()}")))
                
                total_files = len(media_files)
                
                if total_files == 0:
                    self.update_status("No supported media files found", "orange")
                    messagebox.showwarning("No Files", "No supported media files found in the selected folder.")
                    return
                
                successful = 0
                
                # Process each file
                for idx, file_path in enumerate(media_files, 1):
                    # Reset file progress for each file
                    self.current_file_progress.set(0)
                    
                    # Update progress
                    progress_pct = (idx / total_files) * 100
                    self.overall_progress.set(progress_pct)
                    self.current_file_name.set(f"[{idx}/{total_files}] {file_path.name}")
                    self.update_status(f"Processing {idx}/{total_files}: {file_path.name}", "blue")
                    
                    # Reset processor's detection list for each file
                    processor.all_detections = []
                    
                    # Process based on file type
                    try:
                        if file_path.suffix.lower() in self.supported_image_formats:
                            success = processor.process_image(file_path, confidence=self.confidence.get())
                        else:
                            success = processor.process_video(file_path, confidence=self.confidence.get())
                        
                        if success:
                            successful += 1
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                
                # Show results
                self.overall_progress.set(100)
                self.update_status(
                    f"✓ Processed {successful}/{total_files} files successfully", 
                    "green" if successful > 0 else "orange"
                )
                self.current_file_name.set(f"Completed: {successful}/{total_files} files")
                
                messagebox.showinfo(
                    "Batch Processing Complete", 
                    f"Successfully processed {successful} out of {total_files} media files.\n\n"
                    f"Processed files are saved with '{self.filename_suffix.get()}' suffix in the same folder."
                )
            
            else:
                self.update_status("Error: Invalid path", "red")
                messagebox.showerror("Error", "Invalid path specified")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.processing = False
            self.process_button.config(state="normal")
    
    def prompt_open_file(self, output_path: Path):
        """
        Prompt user to open the processed file.
        
        Args:
            output_path: Path to processed file
        """
        result = messagebox.askyesno(
            "Processing Complete",
            f"File processed successfully!\n\n"
            f"Output: {output_path.name}\n\n"
            f"Would you like to open the processed file?"
        )
        
        if result:
            self.open_file(output_path)
    
    def process(self):
        """Start processing media files."""
        if self.processing:
            return
        
        if not self.input_path.get():
            messagebox.showwarning("Warning", "Please select a file or folder first")
            return
        
        self.processing = True
        self.process_button.config(state="disabled")
        self.current_file_progress.set(0)
        self.overall_progress.set(0)
        self.current_file_name.set("")
        self.update_status("Processing...", "blue")
        
        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.process_thread, daemon=True)
        thread.start()


def main():
    """Main entry point for enhanced GUI application."""
    # Fix for multiprocessing in frozen executables
    import multiprocessing
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    
    # Try to use a modern theme
    try:
        style.theme_use('clam')
    except:
        pass
    
    app = HumanBlurGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
