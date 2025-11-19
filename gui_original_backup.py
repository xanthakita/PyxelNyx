#!/usr/bin/env python3
"""
Human Blur GUI Tool - Graphical Interface
A simple GUI for the human blur tool with support for both blur and black mask modes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import sys
from blur_humans import HumanBlurProcessor


class HumanBlurGUI:
    """
    GUI application for human blur tool with black mask option.
    """
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Human Blur Tool v2.0")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Variables
        self.input_path = tk.StringVar()
        self.mask_type = tk.StringVar(value="black")
        self.blur_intensity = tk.IntVar(value=151)
        self.blur_passes = tk.IntVar(value=3)
        self.confidence = tk.DoubleVar(value=0.5)
        self.model_name = tk.StringVar(value="yolov8n-seg.pt")
        self.processing = False
        
        # Setup UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="Human Blur Tool v2.0", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="Segmentation-Based Privacy Protection", 
            font=("Arial", 10)
        )
        subtitle_label.grid(row=1, column=0)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File/Folder Selection
        ttk.Label(main_frame, text="Input:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse File", command=self.browse_file).grid(
            row=0, column=1, padx=(0, 5)
        )
        ttk.Button(input_frame, text="Browse Folder", command=self.browse_folder).grid(
            row=0, column=2
        )
        
        # Mask Type Selection
        ttk.Label(main_frame, text="Mask Type:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        mask_frame = ttk.Frame(main_frame)
        mask_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        ttk.Radiobutton(
            mask_frame, 
            text="Black Mask (Default)", 
            variable=self.mask_type, 
            value="black",
            command=self.update_blur_controls
        ).grid(row=0, column=0, padx=(0, 20))
        
        ttk.Radiobutton(
            mask_frame, 
            text="Blur", 
            variable=self.mask_type, 
            value="blur",
            command=self.update_blur_controls
        ).grid(row=0, column=1)
        
        # Blur Settings (only for blur mode)
        blur_settings_frame = ttk.LabelFrame(main_frame, text="Blur Settings", padding="10")
        blur_settings_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Blur Intensity
        ttk.Label(blur_settings_frame, text="Intensity:").grid(row=0, column=0, sticky=tk.W)
        self.intensity_slider = ttk.Scale(
            blur_settings_frame, 
            from_=51, 
            to=301, 
            variable=self.blur_intensity,
            orient=tk.HORIZONTAL,
            length=400
        )
        self.intensity_slider.grid(row=0, column=1, padx=(10, 0))
        
        self.intensity_label = ttk.Label(blur_settings_frame, text="151")
        self.intensity_label.grid(row=0, column=2, padx=(10, 0))
        
        self.blur_intensity.trace_add("write", self.update_intensity_label)
        
        # Blur Passes
        ttk.Label(blur_settings_frame, text="Passes:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.passes_spinbox = ttk.Spinbox(
            blur_settings_frame, 
            from_=1, 
            to=10, 
            textvariable=self.blur_passes,
            width=10
        )
        self.passes_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Advanced Settings
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Settings", padding="10")
        advanced_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Confidence
        ttk.Label(advanced_frame, text="Confidence:").grid(row=0, column=0, sticky=tk.W)
        self.confidence_slider = ttk.Scale(
            advanced_frame, 
            from_=0.1, 
            to=1.0, 
            variable=self.confidence,
            orient=tk.HORIZONTAL,
            length=200
        )
        self.confidence_slider.grid(row=0, column=1, padx=(10, 0))
        
        self.confidence_label = ttk.Label(advanced_frame, text="0.50")
        self.confidence_label.grid(row=0, column=2, padx=(10, 0))
        
        self.confidence.trace_add("write", self.update_confidence_label)
        
        # Model Selection
        ttk.Label(advanced_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        model_combo = ttk.Combobox(
            advanced_frame,
            textvariable=self.model_name,
            values=["yolov8n-seg.pt", "yolov8s-seg.pt", "yolov8m-seg.pt", 
                   "yolov8l-seg.pt", "yolov8x-seg.pt"],
            width=20,
            state="readonly"
        )
        model_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Process Button
        self.process_button = ttk.Button(
            main_frame, 
            text="Process Images", 
            command=self.process,
            style="Accent.TButton"
        )
        self.process_button.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        # Status Label
        self.status_label = ttk.Label(
            main_frame, 
            text="Ready to process images", 
            font=("Arial", 9),
            foreground="gray"
        )
        self.status_label.grid(row=8, column=0, columnspan=2)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Initial update
        self.update_blur_controls()
        
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
    
    def browse_file(self):
        """Open file dialog to select an image."""
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.heic *.heif"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
    
    def browse_folder(self):
        """Open folder dialog to select a directory."""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.input_path.set(folder)
    
    def update_status(self, message, color="gray"):
        """Update status label."""
        self.status_label.config(text=message, foreground=color)
        
    def process_thread(self):
        """Process images in a separate thread."""
        try:
            input_path = Path(self.input_path.get())
            
            if not input_path.exists():
                self.update_status("Error: Path does not exist", "red")
                return
            
            # Ensure odd blur intensity
            blur_intensity = self.blur_intensity.get()
            if blur_intensity % 2 == 0:
                blur_intensity += 1
            
            # Create processor
            processor = HumanBlurProcessor(
                model_name=self.model_name.get(),
                blur_intensity=blur_intensity,
                blur_passes=self.blur_passes.get(),
                mask_type=self.mask_type.get()
            )
            
            # Process based on input type
            if input_path.is_file():
                self.update_status(f"Processing {input_path.name}...", "blue")
                success = processor.process_image(input_path, confidence=self.confidence.get())
                if success:
                    self.update_status(f"✓ Successfully processed {input_path.name}", "green")
                    messagebox.showinfo("Success", f"Successfully processed {input_path.name}")
                else:
                    self.update_status("✗ Processing failed", "red")
                    messagebox.showerror("Error", "Processing failed. Check console for details.")
            
            elif input_path.is_dir():
                self.update_status(f"Processing directory...", "blue")
                successful, total = processor.process_directory(input_path, confidence=self.confidence.get())
                
                if successful > 0:
                    self.update_status(
                        f"✓ Processed {successful}/{total} images successfully", 
                        "green"
                    )
                    messagebox.showinfo(
                        "Success", 
                        f"Successfully processed {successful}/{total} images"
                    )
                else:
                    self.update_status("✗ No images processed", "red")
                    messagebox.showwarning("Warning", "No images were processed successfully.")
            
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
            self.progress.stop()
            self.process_button.config(state="normal")
    
    def process(self):
        """Start processing images."""
        if self.processing:
            return
        
        if not self.input_path.get():
            messagebox.showwarning("Warning", "Please select a file or folder first")
            return
        
        self.processing = True
        self.process_button.config(state="disabled")
        self.progress.start()
        self.update_status("Processing...", "blue")
        
        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.process_thread, daemon=True)
        thread.start()


def main():
    """Main entry point for GUI application."""
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
