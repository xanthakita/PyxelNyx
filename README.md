
# PyxelNyx v3.0 Enhanced 🎭

A Python tool that automatically detects and masks/blurs humans in **images and videos** using **instance segmentation** for precise, lasso-style processing. Built with YOLOv8 segmentation models for accurate human shape detection. Available as both **CLI** and **enhanced GUI** applications with **cross-platform executable support** for Windows, macOS, and Linux.

## What's New in v3.0 Enhanced ✨

### GUI Enhancements (NEW!)
- 🎨 **Production-Ready GUI**: Professional interface suitable for non-technical users
- ✅ **File Validation**: Smart format validation with helpful error messages
- 📊 **Dual Progress Bars**: Individual file + overall batch progress tracking
- ❓ **Built-in Help**: Comprehensive help dialog for GUI and CLI
- 🖼️ **Logo Branding**: Professional organizational logo integration
- 🚀 **Open Result**: Instant option to view processed files
- 🎯 **Media Filter**: Choose images only, videos only, or both
- 📦 **Executable Support**: Build standalone apps for Windows, macOS, Linux

### Core Features
- 🎬 **Video Processing Support**: Process .mp4 and .mov video files frame-by-frame
- 🔊 **Audio Preservation**: Automatically preserves audio tracks when ffmpeg is available
- 🖤 **Black Mask Mode**: Solid black mask for complete privacy protection (default)
- 🎨 **Dual Masking Options**: Choose between black mask or blur mode
- 🎯 **Segmentation-Based Processing (Lasso Effect)**: Uses YOLOv8 segmentation models
- 🌀 **Intense Multi-Pass Blur**: Significantly stronger blur with multi-pass algorithm
- 📱 **HEIC Support**: Full support for Apple's HEIC/HEIF image format
- 🖼️ **Universal Format Support**: Enhanced format handling with PIL fallback
- ⚡ **Improved Processing**: Better error handling and format conversion

## Features ✨

- 🎯 **Accurate Human Detection**: Uses YOLOv8 segmentation (COCO-trained) for precise person detection
- 🎬 **Video Processing**: Frame-by-frame processing of .mp4 and .mov video files
- 🔊 **Audio Preservation**: Automatic audio extraction and merging (requires ffmpeg)
- 🖤 **Black Mask Mode**: Apply solid black mask for complete anonymization (default)
- 🎨 **Blur Mode**: Lasso-style blur that follows human shape/contour, not rectangular regions
- 🌀 **Intense Blur**: Multi-pass blur algorithm with large kernels for maximum effect (blur mode)
- 🖥️ **Dual Interface**: Command-line (CLI) and graphical (GUI) interfaces available
- 📁 **Batch Processing**: Process single files or entire directories with media type filtering
- 🚀 **Performance Optimized**: Multiple model options from nano to extra-large
- 🔧 **Modular Design**: Easy to adapt for library use or integration
- 📝 **Clear Output**: Detailed progress feedback with frame-by-frame statistics
- 🎨 **Universal Format Support**: Images (JPG, PNG, BMP, TIFF, WebP, HEIC/HEIF), Videos (.mp4, .mov)

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **First run** (downloads YOLO segmentation model automatically):
   ```bash
   python blur_humans.py --help
   ```

### HEIC Support

For processing Apple HEIC/HEIF images, the tool requires `pillow-heif`:
```bash
pip install pillow-heif
```

This is included in `requirements.txt`, but if you encounter issues on some systems:
- **macOS**: May require `libheif` via Homebrew: `brew install libheif`
- **Linux**: May require `libheif-dev`: `sudo apt-get install libheif-dev`
- **Windows**: Usually works out of the box with pip installation

### Optional: Video Audio Preservation

For preserving audio in video files, install ffmpeg:

**Linux (Debian/Ubuntu)**:
```bash
sudo apt-get install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

**Windows**:
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

> **Note**: Video processing works without ffmpeg, but audio tracks will not be preserved.

### Optional: GPU Acceleration

For faster processing with NVIDIA GPU:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## Usage 📖

### GUI Interface (Easiest Way!)

Launch the **enhanced** graphical interface for easy point-and-click operation:

```bash
python gui.py
```

The GUI provides:
- 📂 **File/Folder Browser**: Easy selection of images, videos, or directories
- 🎚️ **Mask Type Toggle**: Switch between Black Mask (default) and Blur modes
- ⚙️ **Adjustable Settings**: Blur intensity, passes, confidence, and model selection
- 📊 **Dual Progress Indicators**: Individual file and overall batch progress
- 🎯 **Media Type Filter**: Choose images only, videos only, or both for folders
- ✅ **File Validation**: Automatic validation with helpful error messages
- ❓ **Built-in Help**: Comprehensive help dialog for GUI and CLI usage
- 🖼️ **Logo Branding**: Professional interface with organizational logo
- 🚀 **Open Result**: Option to immediately view processed files
- ✅ **User-Friendly**: No command-line knowledge required
- 🌍 **Cross-Platform**: Works on Windows, macOS, and Linux

**New in Enhanced Version:**
- Smart file format validation
- Dual progress bars for batch operations
- Help dialog with complete instructions
- Open processed file after completion
- Media type filtering for folders
- Improved error handling and messaging

See `BUILD_EXECUTABLE.md` for instructions on building standalone executables for distribution.

### CLI Interface (Command Line)

#### Basic Usage

**Images:**
```bash
# Process a single image with black mask (default)
python blur_humans.py photo.jpg

# Process with blur instead of black mask
python blur_humans.py photo.jpg --mask-type blur
```

**Videos:**
```bash
# Process a video with black mask (default)
python blur_humans.py video.mp4

# Process video with blur effect
python blur_humans.py video.mp4 --mask-type blur

# Process all videos in a directory
python blur_humans.py /path/to/videos/ --media-type videos
```

**Mixed Media Directories:**
```bash
# Process both images and videos (default)
python blur_humans.py /path/to/media/

# Process only images
python blur_humans.py /path/to/media/ --media-type images

# Process only videos
python blur_humans.py /path/to/media/ --media-type videos

# Process all images in a directory
python blur_humans.py /path/to/images/

# Process HEIC images from iPhone
python blur_humans.py IMG_1234.HEIC
```

#### Advanced Options

```bash
# Use black mask (default behavior)
python blur_humans.py photo.jpg --mask-type black

# Use blur mode instead of black mask
python blur_humans.py photo.jpg --mask-type blur

# Extreme blur with more passes (blur mode only)
python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 5

# Adjust detection sensitivity (0.0-1.0, higher = more strict)
python blur_humans.py photo.jpg --confidence 0.7

# Use a more accurate segmentation model (slower but better)
python blur_humans.py photo.jpg --model yolov8m-seg.pt

# Combine options for maximum blur
python blur_humans.py /path/to/images/ --mask-type blur --blur 251 --passes 4 --confidence 0.6 --model yolov8s-seg.pt

# Process with box blur (legacy mode, no segmentation)
python blur_humans.py photo.jpg --mask-type blur --model yolov8n.pt
```

#### Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `input` | - | str | required | Path to image/video file or directory |
| `--media-type` | - | str | both | Media type filter for directories: 'images', 'videos', 'both' |
| `--mask-type` | `-t` | str | black | Masking type: 'black' or 'blur' |
| `--blur` | `-b` | int | 151 | Blur kernel size (1-301, must be odd) - blur mode only |
| `--passes` | `-p` | int | 3 | Number of blur passes (1-10) - blur mode only |
| `--confidence` | `-c` | float | 0.5 | Detection confidence threshold (0.0-1.0) |
| `--model` | `-m` | str | yolov8n-seg.pt | YOLO model selection |
| `--version` | `-v` | - | - | Show version information |
| `--help` | `-h` | - | - | Show help message |

### Segmentation Model Selection (Recommended)

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `yolov8n-seg.pt` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | **Default**, fast segmentation |
| `yolov8s-seg.pt` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| `yolov8m-seg.pt` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Higher accuracy |
| `yolov8l-seg.pt` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Professional use |
| `yolov8x-seg.pt` | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

### Legacy Detection Models (Box Blur Only)

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `yolov8n.pt` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Fast box blur |
| `yolov8s.pt` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| `yolov8m.pt` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Higher accuracy |
| `yolov8l.pt` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Professional use |
| `yolov8x.pt` | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

## Examples 💡

### Example 1: GUI Interface

```bash
$ python gui.py
```

**Output**: Opens a graphical interface where you can:
1. Browse and select files/folders
2. Choose between Black Mask and Blur modes
3. Adjust settings with sliders
4. Click "Process Images" button
5. View progress and results

### Example 2: Basic Black Mask (Default)

```bash
$ python blur_humans.py family_photo.jpg

======================================================================
PyxelNyx v3.0 - Segmentation-Based Blur (Images & Videos)
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLACK
Black mask mode enabled
✓ Model loaded successfully

Processing single image: family_photo.jpg

  Detected 3 human(s) in family_photo.jpg
  Combining masks from 3 person(s)...
  Applying unified black mask to all detected people...
  ✓ Black mask applied to 3 person(s)
  ✓ Saved to family_photo-background.jpg

✓ Processing completed successfully!
```

**Output**: Creates `family_photo-background.jpg` with solid black silhouettes for complete anonymization

### Example 3: Blur Mode Processing

```bash
$ python blur_humans.py family_photo.jpg --mask-type blur

======================================================================
PyxelNyx v2.0 - Segmentation-Based Background Blur
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLUR
Blur settings: intensity=151, passes=3
✓ Model loaded successfully

Processing single image: family_photo.jpg

  Detected 3 human(s) in family_photo.jpg
  Combining masks from 3 person(s)...
  Applying unified lasso blur to all detected people...
  ✓ Lasso blur applied to 3 person(s)
  ✓ Saved to family_photo-background.jpg

✓ Processing completed successfully!
```

**Output**: Creates `family_photo-background.jpg` with precise lasso-style blur around each person

### Example 4: Processing HEIC Images from iPhone

```bash
$ python blur_humans.py IMG_1234.HEIC

======================================================================
PyxelNyx v2.0 - Segmentation-Based Background Blur
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Blur settings: intensity=151, passes=3
✓ Model loaded successfully

Processing single image: IMG_1234.HEIC

  Detected 2 human(s) in IMG_1234.HEIC
  Applied lasso blur to 2 person(s)
  ℹ Converting HEIC to JPG for output
  ✓ Saved to IMG_1234-background.jpg

✓ Processing completed successfully!
```

**Output**: Loads HEIC, applies black mask by default, saves as JPG

### Example 5: Video Processing with Audio Preservation

```bash
$ python blur_humans.py family_video.mp4

======================================================================
PyxelNyx v3.0 - Segmentation-Based Blur (Images & Videos)
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLACK
Black mask mode enabled
✓ Model loaded successfully

Processing single video: family_video.mp4

  Video properties: 1920x1080 @ 30.00 FPS, 900 frames
  Extracting audio...
  ✓ Audio extracted successfully
  Processing video frames...
  Processing frame 90/900 (10%)
  Processing frame 180/900 (20%)
  ...
  Processing frame 900/900 (100%)
  ✓ Processed 900 frames (750 frames with humans detected)
  Merging audio back into video...
  ✓ Audio merged successfully
  ✓ Saved to family_video-background.mp4

✓ Processing completed successfully!
```

**Output**: Creates `family_video-background.mp4` with masked humans and preserved audio

### Example 7: Extreme Blur for Maximum Privacy

```bash
$ python blur_humans.py sensitive_photo.jpg --mask-type blur --blur 251 --passes 5

======================================================================
PyxelNyx v3.0 - Segmentation-Based Blur (Images & Videos)
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Blur settings: intensity=251, passes=5
✓ Model loaded successfully

Processing single image: sensitive_photo.jpg

  Detected 1 human(s) in sensitive_photo.jpg
  Applied lasso blur to 1 person(s)
  ✓ Saved to sensitive_photo-background.jpg

✓ Processing completed successfully!
```

**Output**: Creates extremely blurred output with 5 blur passes

### Example 8: Batch Processing Directory

```bash
$ python blur_humans.py ./vacation_photos/

======================================================================
PyxelNyx v3.0 - Segmentation-Based Blur (Images & Videos)
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLACK
Black mask mode enabled
✓ Model loaded successfully

Processing directory: vacation_photos

Found 15 image(s) to process

Processing [1/15]: beach.jpg
  Detected 2 human(s) in beach.jpg
  Applied lasso blur to 2 person(s)
  ✓ Saved to beach-background.jpg

Processing [2/15]: sunset.jpg
  No humans detected in sunset.jpg

Processing [3/15]: IMG_5678.HEIC
  Detected 3 human(s) in IMG_5678.HEIC
  Applied lasso blur to 3 person(s)
  ℹ Converting HEIC to JPG for output
  ✓ Saved to IMG_5678-background.jpg

...

======================================================================
Results: 12/15 images processed successfully
======================================================================
```

## Output Naming Convention 📝

The tool automatically names output files by appending `-background` before the file extension:

**Images:**
- `photo.jpg` → `photo-background.jpg`
- `image.png` → `image-background.png`
- `my_picture.jpeg` → `my_picture-background.jpeg`
- `IMG_1234.HEIC` → `IMG_1234-background.jpg` (auto-converted to JPG)

**Videos:**
- `video.mp4` → `video-background.mp4`
- `clip.mov` → `clip-background.mov`

Original files are **never modified**.

## Supported Media Formats 🖼️

### Image Formats

**Fully Supported (Read & Write):**
- **JPEG** (`.jpg`, `.jpeg`)
- **PNG** (`.png`)
- **BMP** (`.bmp`)
- **TIFF** (`.tiff`, `.tif`)
- **WebP** (`.webp`)

**Read-Only (Output as JPG):**
- **HEIC/HEIF** (`.heic`, `.heif`) - Apple's image format
  - Requires `pillow-heif` package
  - Automatically converted to JPG for output

### Video Formats

**Fully Supported:**
- **MP4** (`.mp4`) - Most common video format
- **MOV** (`.mov`) - Apple's video format

**Audio Preservation:**
- Requires `ffmpeg` to be installed
- Audio tracks are automatically extracted and merged back
- Works without ffmpeg, but audio will not be preserved

## Error Handling 🛡️

The tool includes comprehensive error handling:

- ✓ Invalid file paths
- ✓ Unsupported image formats
- ✓ Corrupted image files
- ✓ Invalid parameter values
- ✓ Missing dependencies

## Performance Tips 🚀

1. **For speed**: Use default `yolov8n-seg.pt` model (fastest segmentation)
2. **For accuracy**: Use `yolov8m-seg.pt` or higher for better edge detection
3. **For batch processing**: Process entire directories at once
4. **GPU acceleration**: Install CUDA-enabled PyTorch for 5-10x speedup
5. **Lower confidence**: Use `--confidence 0.3` to detect more people (more false positives)
6. **Higher confidence**: Use `--confidence 0.7` for stricter detection (fewer false positives)
7. **Intense blur**: Use `--blur 201 --passes 5` for maximum blur effect
8. **Moderate blur**: Use `--blur 99 --passes 2` for faster processing with good privacy

## Technical Details 🔬

### Architecture

```
blur_humans.py
├── HumanBlurProcessor (Main class)
│   ├── detect_humans_with_masks()  # Segmentation-based detection
│   ├── apply_intense_blur()        # Multi-pass blur algorithm
│   ├── blur_with_mask()            # Lasso-style segmentation blur
│   ├── blur_with_box()             # Legacy box blur (fallback)
│   ├── load_image()                # Universal format loader (HEIC, etc.)
│   ├── save_image()                # Format-aware image saver
│   ├── process_image()             # Single image pipeline
│   └── process_directory()         # Batch processing
└── main()                           # CLI interface
```

### Detection Method

- **Model**: YOLOv8 Segmentation pre-trained on COCO dataset
- **Target Class**: Person (class ID: 0)
- **Default Confidence**: 0.5 (50% certainty)
- **Output**: Instance segmentation masks + bounding boxes
- **Mask Processing**: Binary masks resized to image dimensions

### Blur Method

- **Algorithm**: Multi-pass Gaussian Blur
- **Kernel Size**: User-defined (default: 151x151, range: 1-301)
- **Blur Passes**: User-defined (default: 3, range: 1-10)
- **Application**: Mask-based (precise lasso-style blur following human contour)
- **Blending**: Alpha blending using segmentation mask for smooth edges

### Format Support

- **Standard Formats**: OpenCV with PIL fallback
- **HEIC/HEIF**: pillow-heif library for Apple format support
- **Conversion**: Automatic HEIC → JPG for output compatibility

## Use Cases 🎯

1. **Real Estate Photography**: Remove people from property photos
2. **Background Analysis**: Study environments without human subjects
3. **Privacy Protection**: Anonymize people in public photos
4. **Research**: Analyze architectural or landscape features
5. **Data Preparation**: Create training data for background-focused models

## Future Enhancements 🔮

### Completed ✅
- [x] **Segmentation-based blur** (lasso effect) ✅ v2.0
- [x] **Intense multi-pass blur** ✅ v2.0
- [x] **HEIC format support** ✅ v2.0
- [x] **Universal format support** ✅ v2.0
- [x] **Black mask mode** ✅ v2.1
- [x] **GUI interface** ✅ v2.1
- [x] **Video processing support** ✅ v3.0
- [x] **Enhanced GUI with validation** ✅ v3.0 Enhanced
- [x] **Progress tracking** ✅ v3.0 Enhanced
- [x] **Help system** ✅ v3.0 Enhanced
- [x] **Executable building support** ✅ v3.0 Enhanced

### Planned 🔜
- [ ] GUI preview before processing
- [ ] Drag & drop file support
- [ ] Alternative anonymization methods (pixelation, color masking)
- [ ] Face-only detection and masking
- [ ] API/library mode for integration
- [ ] Custom output directory selection
- [ ] Background replacement options
- [ ] Batch export with custom naming patterns
- [ ] Real-time camera feed processing
- [ ] Multi-language support

## Troubleshooting 🔧

### Model Download Issues

If YOLO segmentation model download fails:
```bash
# Manually download model
python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')"
```

### HEIC Support Issues

If HEIC images fail to load:
```bash
# Install HEIC support
pip install pillow-heif

# On macOS (if needed)
brew install libheif

# On Linux (if needed)
sudo apt-get install libheif-dev
```

### Import Errors

If you encounter import errors:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### GPU Not Detected

Check CUDA availability:
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Segmentation Not Working

If you see "Box blur" instead of "Lasso blur":
- Ensure you're using a segmentation model (e.g., `yolov8n-seg.pt`)
- Check model name includes `-seg` suffix
- Try: `python blur_humans.py photo.jpg --model yolov8n-seg.pt`

## Version History 📋

### v3.0 Enhanced (Current) - Professional GUI & Executables
- ✨ **New**: Enhanced GUI with comprehensive features for non-technical users
- ✨ **New**: File format validation with custom error messaging
- ✨ **New**: Dual progress bars (individual file + overall batch)
- ✨ **New**: Built-in help dialog with GUI and CLI instructions
- ✨ **New**: Logo integration for professional branding
- ✨ **New**: Open processed file option after completion
- ✨ **New**: Media type filtering for folder processing
- ✨ **New**: Cross-platform executable building support
- 📝 **New**: `BUILD_EXECUTABLE.md` - Complete guide for creating executables
- 📝 **New**: `GUI_ENHANCEMENTS_SUMMARY.md` - Detailed feature documentation
- ⚡ **Enhanced**: Better error handling and user messaging
- ⚡ **Enhanced**: Improved UI layout and organization
- 🔧 **Changed**: GUI now production-ready for end users
- ✅ **Maintained**: 100% CLI functionality preserved

### v3.0 (Previous) - Video Support
- ✨ **New**: Video processing (.mp4, .mov)
- ✨ **New**: Audio preservation with ffmpeg
- ✨ **New**: Frame-by-frame progress indicators
- ✨ **New**: Media type filtering

### v2.1.0 - Black Mask & Basic GUI
- ✨ **New**: Black mask mode for complete anonymization
- ✨ **New**: Basic GUI interface with tkinter
- ✨ **New**: Mask type selection (black or blur)
- 🔧 **Changed**: Default mask type to 'black' (was blur)
- ⚡ **Enhanced**: Better user experience with both CLI and GUI options
- 📝 **Enhanced**: Updated documentation with new features

### v2.0.0 - Enhanced with Segmentation
- ✨ **New**: Segmentation-based blurring (lasso effect)
- ✨ **New**: HEIC/HEIF format support
- ⚡ **Enhanced**: Multi-pass blur with larger kernels (up to 301x301)
- ⚡ **Enhanced**: Universal format support with PIL fallback
- ⚡ **Enhanced**: Better error handling and format conversion
- 🔧 **Changed**: Default model to `yolov8n-seg.pt`
- 🔧 **Changed**: Default blur intensity to 151 with 3 passes

### v1.0.0 - Initial Release
- Basic human detection with YOLOv8
- Rectangle-based blur
- Support for JPG, PNG, BMP, TIFF, WebP
- Batch processing

## License 📄

This tool is provided as-is for personal and commercial use. Dependencies (YOLOv8, OpenCV, Pillow) are subject to their respective licenses.

## Contributing 🤝

This is a modular design that can be easily extended. Feel free to adapt the `HumanBlurProcessor` class for your specific needs. The segmentation-based architecture makes it easy to add new features like:
- Custom blur patterns
- Alternative anonymization methods
- Background replacement
- GUI interfaces

## Support 💬

For issues or questions:
1. Check the troubleshooting section
2. Review the examples
3. Verify your Python and dependency versions
4. Ensure you're using a segmentation model for lasso effect

---

**Made with ❤️ for privacy-preserving media processing**
**v3.0 Enhanced - Professional GUI with Cross-Platform Executable Support**

For support or questions about GUI enhancements or executable building:
**apps@globalemancipation.ngo**
