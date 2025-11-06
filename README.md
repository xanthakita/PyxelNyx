
# Human Blur CLI Tool 🎭

A Python command-line tool that automatically detects and blurs humans in images to enable easier analysis of backgrounds. Built with YOLOv8 for accurate human detection and OpenCV for image processing.

## Features ✨

- 🎯 **Accurate Human Detection**: Uses YOLOv8 (COCO-trained) for reliable person detection
- 🌀 **Adjustable Blur**: Maximum blur by default, with customizable intensity
- 📁 **Batch Processing**: Process single images or entire directories
- 🚀 **Performance Optimized**: Balanced approach with multiple model options
- 🔧 **Modular Design**: Easy to adapt for GUI or library use
- 📝 **Clear Output**: Progress feedback and informative messages
- 🎨 **Format Support**: JPG, PNG, BMP, TIFF, WebP

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

3. **First run** (downloads YOLO model automatically):
   ```bash
   python blur_humans.py --help
   ```

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
# Process a single image
python blur_humans.py photo.jpg

# Process all images in a directory
python blur_humans.py /path/to/images/
```

### Advanced Options

```bash
# Adjust blur intensity (1-99, higher = more blur)
python blur_humans.py photo.jpg --blur 51

# Adjust detection sensitivity (0.0-1.0, higher = more strict)
python blur_humans.py photo.jpg --confidence 0.7

# Use a more accurate model (slower but better detection)
python blur_humans.py photo.jpg --model yolov8m.pt

# Combine options
python blur_humans.py /path/to/images/ --blur 75 --confidence 0.6 --model yolov8s.pt
```

### Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `input` | - | str | required | Path to image file or directory |
| `--blur` | `-b` | int | 99 | Blur intensity (1-99, must be odd) |
| `--confidence` | `-c` | float | 0.5 | Detection confidence threshold (0.0-1.0) |
| `--model` | `-m` | str | yolov8n.pt | YOLO model selection |
| `--version` | `-v` | - | - | Show version information |
| `--help` | `-h` | - | - | Show help message |

### Model Selection

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `yolov8n.pt` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Default, fast processing |
| `yolov8s.pt` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| `yolov8m.pt` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Higher accuracy |
| `yolov8l.pt` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Professional use |
| `yolov8x.pt` | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy |

## Examples 💡

### Example 1: Basic Single Image Processing

```bash
$ python blur_humans.py family_photo.jpg

============================================================
Human Blur Tool - Background Analysis Helper
============================================================

Loading YOLO model: yolov8n.pt...
✓ Model loaded successfully

Processing single image: family_photo.jpg

  Detected 3 human(s) in family_photo.jpg
  ✓ Saved to family_photo-background.jpg

✓ Processing completed successfully!
```

**Output**: Creates `family_photo-background.jpg` with all humans blurred

### Example 2: Batch Processing Directory

```bash
$ python blur_humans.py ./vacation_photos/

============================================================
Human Blur Tool - Background Analysis Helper
============================================================

Loading YOLO model: yolov8n.pt...
✓ Model loaded successfully

Processing directory: vacation_photos

Found 15 image(s) to process

Processing [1/15]: beach.jpg
  Detected 2 human(s) in beach.jpg
  ✓ Saved to beach-background.jpg

Processing [2/15]: sunset.jpg
  No humans detected in sunset.jpg

...

============================================================
Results: 12/15 images processed successfully
============================================================
```

### Example 3: Custom Settings

```bash
# Medium blur with stricter detection
$ python blur_humans.py crowd.jpg --blur 51 --confidence 0.7

# Use more accurate model for challenging images
$ python blur_humans.py group_photo.jpg --model yolov8m.pt
```

## Output Naming Convention 📝

The tool automatically names output files by appending `-background` before the file extension:

- `photo.jpg` → `photo-background.jpg`
- `image.png` → `image-background.png`
- `my_picture.jpeg` → `my_picture-background.jpeg`

Original files are never modified.

## Supported Image Formats 🖼️

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- TIFF (`.tiff`)
- WebP (`.webp`)

## Error Handling 🛡️

The tool includes comprehensive error handling:

- ✓ Invalid file paths
- ✓ Unsupported image formats
- ✓ Corrupted image files
- ✓ Invalid parameter values
- ✓ Missing dependencies

## Performance Tips 🚀

1. **For speed**: Use default `yolov8n.pt` model
2. **For accuracy**: Use `yolov8m.pt` or higher
3. **For batch processing**: Process entire directories at once
4. **GPU acceleration**: Install CUDA-enabled PyTorch for 5-10x speedup
5. **Lower confidence**: Use `--confidence 0.3` to detect more people (more false positives)
6. **Higher confidence**: Use `--confidence 0.7` for stricter detection (fewer false positives)

## Technical Details 🔬

### Architecture

```
blur_humans.py
├── HumanBlurProcessor (Main class)
│   ├── detect_humans()    # YOLO-based detection
│   ├── blur_regions()     # Gaussian blur application
│   ├── process_image()    # Single image pipeline
│   └── process_directory() # Batch processing
└── main()                  # CLI interface
```

### Detection Method

- **Model**: YOLOv8 pre-trained on COCO dataset
- **Target Class**: Person (class ID: 0)
- **Default Confidence**: 0.5 (50% certainty)
- **Output**: Bounding boxes (x1, y1, x2, y2)

### Blur Method

- **Algorithm**: Gaussian Blur
- **Kernel Size**: User-defined (default: 99x99)
- **Application**: Region-based (only detected humans)

## Use Cases 🎯

1. **Real Estate Photography**: Remove people from property photos
2. **Background Analysis**: Study environments without human subjects
3. **Privacy Protection**: Anonymize people in public photos
4. **Research**: Analyze architectural or landscape features
5. **Data Preparation**: Create training data for background-focused models

## Future Enhancements 🔮

- [ ] GUI interface with preview
- [ ] Video processing support
- [ ] Alternative anonymization methods (pixelation, masking)
- [ ] Face-only detection and blur
- [ ] API/library mode for integration
- [ ] Undo/redo functionality
- [ ] Custom output directory

## Troubleshooting 🔧

### Model Download Issues

If YOLO model download fails:
```bash
# Manually download model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
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

## License 📄

This tool is provided as-is for personal and commercial use. Dependencies (YOLOv8, OpenCV) are subject to their respective licenses.

## Contributing 🤝

This is a modular design that can be easily extended. Feel free to adapt the `HumanBlurProcessor` class for your specific needs.

## Support 💬

For issues or questions:
1. Check the troubleshooting section
2. Review the examples
3. Verify your Python and dependency versions

---

**Made with ❤️ for easier background analysis**
