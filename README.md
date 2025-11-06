
# Human Blur CLI Tool v2.0 🎭

A Python command-line tool that automatically detects and blurs humans in images using **instance segmentation** for precise, lasso-style blurring. Built with YOLOv8 segmentation models for accurate human shape detection and enhanced blur algorithms for maximum privacy.

## What's New in v2.0 ✨

- 🎨 **Segmentation-Based Blurring (Lasso Effect)**: Uses YOLOv8 segmentation models to blur only the actual human silhouette, not rectangular boxes
- 🌀 **Intense Multi-Pass Blur**: Significantly stronger blur with multi-pass algorithm (default: 3 passes with kernel size 151)
- 📱 **HEIC Support**: Full support for Apple's HEIC/HEIF image format
- 🖼️ **Universal Format Support**: Enhanced format handling with PIL fallback for maximum compatibility
- ⚡ **Improved Processing**: Better error handling and format conversion

## Features ✨

- 🎯 **Accurate Human Detection**: Uses YOLOv8 segmentation (COCO-trained) for precise person detection
- 🎨 **Lasso-Style Blur**: Blurs only the human shape/contour, not rectangular regions
- 🌀 **Intense Blur**: Multi-pass blur algorithm with large kernels for maximum effect
- 📁 **Batch Processing**: Process single images or entire directories
- 🚀 **Performance Optimized**: Multiple model options from nano to extra-large
- 🔧 **Modular Design**: Easy to adapt for GUI or library use
- 📝 **Clear Output**: Detailed progress feedback with segmentation statistics
- 🎨 **Universal Format Support**: JPG, PNG, BMP, TIFF, WebP, HEIC/HEIF

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

### Optional: GPU Acceleration

For faster processing with NVIDIA GPU:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## Usage 📖

### Basic Usage

```bash
# Process a single image with segmentation (lasso effect)
python blur_humans.py photo.jpg

# Process all images in a directory
python blur_humans.py /path/to/images/

# Process HEIC images from iPhone
python blur_humans.py IMG_1234.HEIC
```

### Advanced Options

```bash
# Extreme blur with more passes
python blur_humans.py photo.jpg --blur 201 --passes 5

# Adjust detection sensitivity (0.0-1.0, higher = more strict)
python blur_humans.py photo.jpg --confidence 0.7

# Use a more accurate segmentation model (slower but better)
python blur_humans.py photo.jpg --model yolov8m-seg.pt

# Combine options for maximum blur
python blur_humans.py /path/to/images/ --blur 251 --passes 4 --confidence 0.6 --model yolov8s-seg.pt

# Process with box blur (legacy mode, no segmentation)
python blur_humans.py photo.jpg --model yolov8n.pt
```

### Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `input` | - | str | required | Path to image file or directory |
| `--blur` | `-b` | int | 151 | Blur kernel size (1-301, must be odd) |
| `--passes` | `-p` | int | 3 | Number of blur passes (1-10) |
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

### Example 1: Basic Single Image Processing with Segmentation

```bash
$ python blur_humans.py family_photo.jpg

======================================================================
Human Blur Tool v2.0 - Segmentation-Based Background Blur
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Blur settings: intensity=151, passes=3
✓ Model loaded successfully

Processing single image: family_photo.jpg

  Detected 3 human(s) in family_photo.jpg
  Applied lasso blur to 3 person(s)
  ✓ Saved to family_photo-background.jpg

✓ Processing completed successfully!
```

**Output**: Creates `family_photo-background.jpg` with precise lasso-style blur around each person

### Example 2: Processing HEIC Images from iPhone

```bash
$ python blur_humans.py IMG_1234.HEIC

======================================================================
Human Blur Tool v2.0 - Segmentation-Based Background Blur
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

**Output**: Loads HEIC, applies segmentation blur, saves as JPG

### Example 3: Extreme Blur for Maximum Privacy

```bash
$ python blur_humans.py sensitive_photo.jpg --blur 251 --passes 5

======================================================================
Human Blur Tool v2.0 - Segmentation-Based Background Blur
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

### Example 4: Batch Processing Directory

```bash
$ python blur_humans.py ./vacation_photos/

======================================================================
Human Blur Tool v2.0 - Segmentation-Based Background Blur
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Blur settings: intensity=151, passes=3
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

- `photo.jpg` → `photo-background.jpg`
- `image.png` → `image-background.png`
- `my_picture.jpeg` → `my_picture-background.jpeg`
- `IMG_1234.HEIC` → `IMG_1234-background.jpg` (auto-converted to JPG)

Original files are **never modified**.

## Supported Image Formats 🖼️

### Fully Supported (Read & Write)
- **JPEG** (`.jpg`, `.jpeg`)
- **PNG** (`.png`)
- **BMP** (`.bmp`)
- **TIFF** (`.tiff`, `.tif`)
- **WebP** (`.webp`)

### Read-Only (Output as JPG)
- **HEIC/HEIF** (`.heic`, `.heif`) - Apple's image format
  - Requires `pillow-heif` package
  - Automatically converted to JPG for output

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

- [x] **Segmentation-based blur** (lasso effect) ✅ v2.0
- [x] **Intense multi-pass blur** ✅ v2.0
- [x] **HEIC format support** ✅ v2.0
- [x] **Universal format support** ✅ v2.0
- [ ] GUI interface with preview
- [ ] Video processing support
- [ ] Alternative anonymization methods (pixelation, masking)
- [ ] Face-only detection and blur
- [ ] API/library mode for integration
- [ ] Custom output directory
- [ ] Background replacement options

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

### v2.0.0 (Current) - Enhanced with Segmentation
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

**Made with ❤️ for privacy-preserving background analysis**
**v2.0 - Now with precision segmentation**
