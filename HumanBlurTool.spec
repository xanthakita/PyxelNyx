# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Human Blur Tool GUI
This configuration ensures proper bundling of all dependencies and resources.
"""

import sys
from pathlib import Path

block_cipher = None

# Get the script directory
script_dir = Path.cwd()

a = Analysis(
    ['gui_enhanced.py'],
    pathex=[str(script_dir)],
    binaries=[],
    datas=[
        # Include logo for GUI
        ('logo.png', '.'),
    ],
    hiddenimports=[
        # GUI and image processing
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        
        # OpenCV and image processing
        'cv2',
        'numpy',
        'numpy.core._multiarray_umath',
        
        # YOLO and ultralytics
        'ultralytics',
        'ultralytics.models',
        'ultralytics.models.yolo',
        'ultralytics.nn',
        'ultralytics.nn.modules',
        'ultralytics.utils',
        'ultralytics.engine',
        'ultralytics.engine.results',
        'ultralytics.engine.predictor',
        
        # PyTorch
        'torch',
        'torch._C',
        'torch.nn',
        'torch.nn.functional',
        'torchvision',
        'torchvision.ops',
        
        # HEIC support (optional)
        'pillow_heif',
        
        # Other dependencies
        'yaml',
        'matplotlib',
        'scipy',
        'pandas',
        'tqdm',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out duplicate files and unnecessary binaries
# This helps reduce the final executable size
a.binaries = [x for x in a.binaries if not x[0].startswith('libQt')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create single-file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HumanBlurTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging (shows console output)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png' if Path('logo.png').exists() else None,
)

# For macOS: Create .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='HumanBlurTool.app',
        icon='logo.png' if Path('logo.png').exists() else None,
        bundle_identifier='org.globalemancipation.humanblur',
        info_plist={
            'CFBundleName': 'Human Blur Tool',
            'CFBundleDisplayName': 'Human Blur Tool',
            'CFBundleGetInfoString': 'AI-Powered Privacy Protection for Images & Videos',
            'CFBundleVersion': '3.0.0',
            'CFBundleShortVersionString': '3.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.13.0',
            'NSRequiresAquaSystemAppearance': False,
            'LSApplicationCategoryType': 'public.app-category.graphics-design',
            # Permissions for file access
            'NSPhotoLibraryUsageDescription': 'This app needs access to process your photos.',
            'NSCameraUsageDescription': 'This app needs access to process images.',
        },
    )
