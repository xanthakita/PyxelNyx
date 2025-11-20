
# Installation Guide

Complete installation instructions for the Human Blur CLI Tool.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Verification](#verification)
- [GPU Setup (Optional)](#gpu-setup-optional)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS:** Linux, macOS, or Windows 10+
- **Python:** 3.8 or higher
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk:** 500 MB free space (for models and dependencies)
- **CPU:** Any modern multi-core processor

### Recommended for Best Performance
- **RAM:** 16 GB or more
- **GPU:** NVIDIA GPU with CUDA support (GTX 1060 or better)
- **CPU:** Intel i5/AMD Ryzen 5 or better

---

## Installation Methods

### Method 1: pip install (Recommended)

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Verify installation
python blur_humans.py --help
```

### Method 2: System-wide installation

```bash
# Install as a command-line tool
pip install -e .

# Now you can use it from anywhere
blur-humans --help
```

### Method 3: Virtual Environment (Recommended for Development)

#### On Linux/macOS:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Use the tool
python blur_humans.py --help
```

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Use the tool
python blur_humans.py --help
```

### Method 4: Using Conda

```bash
# Create conda environment
conda create -n blur-humans python=3.10

# Activate environment
conda activate blur-humans

# Install dependencies
pip install -r requirements.txt

# Use the tool
python blur_humans.py --help
```

---

## Verification

### Test Installation

```bash
# Check if all imports work
python -c "import cv2, numpy, ultralytics; print('✓ All dependencies installed')"

# Display help
python blur_humans.py --help

# Check version
python blur_humans.py --version
```

### First Run (Downloads YOLO Model)

The first time you run the tool, it will automatically download the YOLO model (~6 MB):

```bash
python blur_humans.py test.jpg
```

Expected output:
```
Loading YOLO model: yolov8n.pt...
Downloading https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt...
✓ Model loaded successfully
```

---

## GPU Setup (Optional)

GPU acceleration provides 5-10x faster processing. Only works with NVIDIA GPUs.

### Step 1: Check CUDA Availability

```bash
# Check if you have an NVIDIA GPU
nvidia-smi

# Check PyTorch CUDA support
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Step 2: Install CUDA-enabled PyTorch

#### For CUDA 11.8:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### For CUDA 12.1:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

#### For CUDA 12.4:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

### Step 3: Verify GPU Support

```bash
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Not available"}')"
```

Expected output:
```
GPU: NVIDIA GeForce RTX 3060
```

---

## Platform-Specific Instructions

### Ubuntu/Debian Linux

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Install Python packages
pip3 install -r requirements.txt
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install dependencies
pip3 install -r requirements.txt
```

**Note:** macOS doesn't support CUDA/GPU acceleration. Use CPU processing.

### Windows

```bash
# Download and install Python from python.org
# Make sure to check "Add Python to PATH" during installation

# Open Command Prompt or PowerShell
# Navigate to project directory
cd path\to\pyxelnyx

# Install dependencies
pip install -r requirements.txt
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cv2'"

**Solution:**
```bash
pip install opencv-python
```

### Issue: "No module named 'ultralytics'"

**Solution:**
```bash
pip install ultralytics
```

### Issue: PyTorch installation fails

**Solution 1:** Use conda
```bash
conda install pytorch torchvision -c pytorch
```

**Solution 2:** Install CPU-only version
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue: "Permission denied" on Linux/macOS

**Solution:**
```bash
# Make script executable
chmod +x blur_humans.py

# Or use python explicitly
python blur_humans.py --help
```

### Issue: YOLO model download fails

**Solution:** Manually download the model
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Issue: Out of memory error

**Solution 1:** Use smaller model
```bash
python blur_humans.py image.jpg --model yolov8n.pt
```

**Solution 2:** Process fewer images at once
```bash
# Instead of processing entire directory
# Process in batches
```

### Issue: ImportError with numpy/OpenCV

**Solution:** Reinstall with compatible versions
```bash
pip uninstall opencv-python numpy
pip install opencv-python numpy
```

### Issue: "CUDA out of memory" (GPU)

**Solution:** Force CPU processing
```bash
export CUDA_VISIBLE_DEVICES=""
python blur_humans.py image.jpg
```

---

## Updating

### Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade ultralytics
```

### Update YOLO Models

Models are cached after first download. To get latest:

```bash
# Remove cached model
rm yolov8n.pt

# Next run will download latest version
python blur_humans.py image.jpg
```

---

## Uninstallation

### Remove Dependencies Only

```bash
pip uninstall opencv-python numpy ultralytics torch torchvision
```

### Remove Everything

```bash
# If using virtual environment
rm -rf venv/

# If installed system-wide
pip uninstall pyxelnyx

# Remove cached models
rm -rf ~/.cache/ultralytics/
```

---

## Development Installation

For developers who want to modify the code:

```bash
# Clone/download the repository
git clone https://github.com/yourusername/pyxelnyx.git
cd pyxelnyx

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .

# Make changes to blur_humans.py
# Changes take effect immediately
```

---

## Docker Installation (Advanced)

For isolated environment:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY blur_humans.py .

ENTRYPOINT ["python", "blur_humans.py"]
```

```bash
# Build image
docker build -t blur-humans .

# Run tool
docker run -v $(pwd):/data blur-humans /data/image.jpg
```

---

## Support

If you encounter issues not covered here:

1. Check the main [README.md](README.md)
2. Review [EXAMPLES.md](EXAMPLES.md) for usage examples
3. Verify Python version: `python --version` (must be 3.8+)
4. Check pip version: `pip --version` (should be recent)
5. Try reinstalling in a fresh virtual environment

---

**Installation complete!** 🎉 Check out [EXAMPLES.md](EXAMPLES.md) for usage examples.
