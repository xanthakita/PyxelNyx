"""
Runtime hook for PyInstaller to fix multiprocessing issues in frozen executables.
This ensures that multiprocessing (used by PyTorch/ultralytics) works correctly.
"""

import sys
import multiprocessing

# Fix for multiprocessing in frozen executables
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    multiprocessing.freeze_support()
    
    # Set the multiprocessing start method
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        # Already set
        pass
