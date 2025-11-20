
#!/usr/bin/env python3
"""
Setup script for Human Blur CLI Tool
Allows installation as a system-wide command
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="pyxelnyx",
    version="1.0.0",
    description="CLI tool to detect and blur humans in images for background analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DeepAgent",
    url="https://github.com/yourusername/pyxelnyx",
    py_modules=["blur_humans"],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "ultralytics>=8.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "blur-humans=blur_humans:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="image-processing computer-vision blur anonymization yolo opencv",
)
