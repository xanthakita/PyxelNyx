# -*- mode: python ; coding: utf-8 -*-
"""
PyxelNyx v3.0 - Enhanced PyInstaller Spec File
AI-Powered Privacy Protection for Images & Videos

This spec file is optimized for building standalone executables with:
- Correct entry point (gui_enhanced.py)
- All dependencies (PyTorch, ultralytics, OpenCV, etc.)
- Logo and resource bundling
- Multiprocessing support for frozen executables
- Cross-platform compatibility (Windows, macOS, Linux)

Build command:
    pyinstaller PyxelNyx.spec --clean

Or use the automated build scripts:
    Windows: build.bat
    macOS/Linux: ./build.sh
"""

import sys
from pathlib import Path

block_cipher = None

# Define all hidden imports needed for PyxelNyx
hidden_imports = [
    # Core GUI dependencies
    'PIL._tkinter_finder',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    '_tkinter',
    
    # PIL/Pillow components
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    
    # HEIC/HEIF support
    'pillow_heif',
    'pillow_heif.HeifImagePlugin',
    
    # OpenCV and image processing
    'cv2',
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    'numpy.fft',
    
    # PyTorch dependencies
    'torch',
    'torch.nn',
    'torch.nn.functional',
    'torchvision',
    'torchvision.ops',
    'torchvision.models',
    
    # Ultralytics YOLO
    'ultralytics',
    'ultralytics.nn',
    'ultralytics.nn.modules',
    'ultralytics.nn.tasks',
    'ultralytics.models',
    'ultralytics.models.yolo',
    'ultralytics.models.yolo.segment',
    'ultralytics.engine',
    'ultralytics.engine.predictor',
    'ultralytics.utils',
    'ultralytics.utils.torch_utils',
    'ultralytics.data',
    'ultralytics.data.augment',
    
    # Video processing
    'moviepy',
    'moviepy.editor',
    'moviepy.video.io.VideoFileClip',
    'moviepy.audio.io.AudioFileClip',
    
    # Multiprocessing support
    'multiprocessing',
    'multiprocessing.pool',
    'multiprocessing.queues',
    
    # Standard library
    'pathlib',
    'threading',
    'queue',
    'datetime',
    'json',
    'yaml',
    'requests',
    
    # Additional ultralytics dependencies
    'tqdm',
    'matplotlib',
    'pandas',
    'seaborn',
    'scipy',
]

# Data files to include
datas = [
    ('logo.png', '.'),  # Logo for GUI
    # Note: YOLO models (.pt files) are downloaded automatically by ultralytics
    # on first run to ~/.cache/ultralytics/ - no need to bundle them
]

# Binaries (none needed for now, auto-detected)
binaries = []

a = Analysis(
    ['gui_enhanced.py'],  # CORRECT ENTRY POINT
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],  # Fixes multiprocessing in frozen mode
    excludes=[
        # Exclude unused modules to reduce size
        'pytest',
        'setuptools',
        'pip',
        'wheel',
        'distutils',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Single-file executable (recommended for easy distribution)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PyxelNyx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI mode - no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png' if sys.platform == 'win32' else None,  # Windows icon
)

# macOS app bundle configuration
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='PyxelNyx.app',
        icon='logo.png',
        bundle_identifier='org.globalemancipation.pyxelnyx',
        info_plist={
            'CFBundleName': 'PyxelNyx',
            'CFBundleDisplayName': 'PyxelNyx',
            'CFBundleShortVersionString': '3.0',
            'CFBundleVersion': '3.0',
            'CFBundlePackageType': 'APPL',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
            'NSPrincipalClass': 'NSApplication',
            'NSRequiresAquaSystemAppearance': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeExtensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'heic', 'heif'],
                    'CFBundleTypeName': 'Image Files',
                    'CFBundleTypeRole': 'Viewer',
                },
                {
                    'CFBundleTypeExtensions': ['mp4', 'avi', 'mov', 'mkv'],
                    'CFBundleTypeName': 'Video Files',
                    'CFBundleTypeRole': 'Viewer',
                }
            ]
        },
    )

# Alternative: Directory-based build (faster startup, slightly larger)
# Uncomment the following and comment out the single-file EXE section above
# to create a directory-based build instead:

"""
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PyxelNyx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyxelNyx',
)

# macOS app bundle for directory build
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='PyxelNyx.app',
        icon='logo.png',
        bundle_identifier='org.globalemancipation.pyxelnyx',
        info_plist={
            'CFBundleName': 'PyxelNyx',
            'CFBundleDisplayName': 'PyxelNyx',
            'CFBundleShortVersionString': '3.0',
            'CFBundleVersion': '3.0',
            'CFBundlePackageType': 'APPL',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
"""
