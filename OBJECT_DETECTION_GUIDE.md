# Object Detection Integration Guide

## Overview

The Human Blur Tool has been enhanced with **background object detection** capabilities. While the tool blurs or masks humans in images/videos, it now simultaneously detects and catalogs all other objects in the scene.

### Version 3.1.0 Features

✨ **Key Features:**
- 🎯 Simultaneous object detection during blur processing (single-pass efficiency)
- 🚫 Automatic filtering of human detections (person class excluded)
- ⏱️ Timestamp tracking for video frames (HH:MM:SS.mmm format)
- 📊 JSON export of all detections with structured data
- 🔧 Configurable detection models and confidence thresholds
- 🎨 Uses YOLOv8m by default for better accuracy

---

## Quick Start

### Basic Usage

**Process an image with object detection (enabled by default):**
```bash
python blur_humans.py photo.jpg
```

**Process a video with object detection:**
```bash
python blur_humans.py video.mp4
```

**Disable object detection if not needed:**
```bash
python blur_humans.py photo.jpg --disable-detection
```

**Use a different detection model:**
```bash
python blur_humans.py photo.jpg --detection-model yolov8s.pt
```

---

## Command-Line Arguments

### New Detection Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--enable-detection` | flag | True | Enable background object detection (default) |
| `--disable-detection` | flag | False | Disable object detection completely |
| `--detection-model` | str | yolov8m.pt | YOLO model for object detection |

### Detection Model Options

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `yolov8n.pt` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Fastest, lower accuracy |
| `yolov8s.pt` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| `yolov8m.pt` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Default**, best balance |
| `yolov8l.pt` | ⚡⚡ | ⭐⭐⭐⭐⭐ | Higher accuracy, slower |
| `yolov8x.pt` | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy, slowest |

---

## Output Format

### JSON Structure

The tool generates a JSON file for each processed media file:
- **For images:** `<filename>-detections.json`
- **For videos:** `<filename>-detections.json`

#### Example JSON Output (Image)

```json
{
  "source_file": "photo.jpg",
  "total_detections": 3,
  "detections": [
    {
      "label": "car",
      "confidence": 0.8945,
      "bbox": {
        "x1": 120.45,
        "y1": 230.12,
        "x2": 450.67,
        "y2": 520.89
      }
    },
    {
      "label": "bicycle",
      "confidence": 0.7621,
      "bbox": {
        "x1": 510.23,
        "y1": 340.56,
        "x2": 680.34,
        "y2": 590.78
      }
    },
    {
      "label": "traffic light",
      "confidence": 0.6789,
      "bbox": {
        "x1": 890.12,
        "y1": 50.34,
        "x2": 920.45,
        "y2": 150.67
      }
    }
  ]
}
```

#### Example JSON Output (Video)

```json
{
  "source_file": "video.mp4",
  "total_detections": 150,
  "detections": [
    {
      "label": "car",
      "confidence": 0.9234,
      "bbox": {
        "x1": 345.12,
        "y1": 456.78,
        "x2": 678.90,
        "y2": 890.12
      },
      "frame": 1,
      "timestamp": "00:00:00.033"
    },
    {
      "label": "traffic light",
      "confidence": 0.8567,
      "bbox": {
        "x1": 890.45,
        "y1": 120.67,
        "x2": 920.89,
        "y2": 180.34
      },
      "frame": 1,
      "timestamp": "00:00:00.033"
    },
    {
      "label": "dog",
      "confidence": 0.7845,
      "bbox": {
        "x1": 123.45,
        "y1": 567.89,
        "x2": 234.56,
        "y2": 678.90
      },
      "frame": 15,
      "timestamp": "00:00:00.500"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `source_file` | string | Name of the processed media file |
| `total_detections` | integer | Total number of objects detected |
| `label` | string | Object class name (e.g., "car", "dog", "bicycle") |
| `confidence` | float | Detection confidence (0.0-1.0), rounded to 4 decimals |
| `bbox` | object | Bounding box coordinates |
| `bbox.x1` | float | Top-left X coordinate |
| `bbox.y1` | float | Top-left Y coordinate |
| `bbox.x2` | float | Bottom-right X coordinate |
| `bbox.y2` | float | Bottom-right Y coordinate |
| `frame` | integer | Frame number (video only, 1-indexed) |
| `timestamp` | string | Time in video (video only, HH:MM:SS.mmm format) |

---

## Examples

### Example 1: Basic Image Processing with Detection

```bash
python blur_humans.py street_photo.jpg
```

**Output:**
- `street_photo-background.jpg` - Blurred image
- `street_photo-detections.json` - Object detections

**Console Output:**
```
======================================================================
Human Blur Tool v3.1 - With Background Object Detection
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLACK
Black mask mode enabled
✓ Model loaded successfully
Loading object detection model: yolov8m.pt...
✓ Object detection model loaded successfully

Processing single image: street_photo.jpg

  Detected 2 human(s) in street_photo.jpg
  Detecting background objects...
  ✓ Detected 5 background object(s)
  Combining masks from 2 person(s)...
  Applying unified black mask to all detected people...
  ✓ Black mask applied to 2 person(s)
  ✓ Saved 5 detection(s) to street_photo-detections.json
  Processing time: 2.34 seconds
  ✓ Saved to street_photo-background.jpg

✓ Processing completed successfully!
```

### Example 2: Video Processing with Timestamps

```bash
python blur_humans.py traffic_video.mp4 --detection-model yolov8s.pt
```

**Output:**
- `traffic_video-background.mp4` - Processed video
- `traffic_video-detections.json` - All detections with timestamps

**Console Output:**
```
======================================================================
Human Blur Tool v3.1 - With Background Object Detection
======================================================================

Loading YOLO model: yolov8n-seg.pt...
Segmentation mode: Enabled (Lasso effect)
Mask type: BLACK
Black mask mode enabled
✓ Model loaded successfully
Loading object detection model: yolov8s.pt...
✓ Object detection model loaded successfully

Processing single video: traffic_video.mp4

  Video properties: 1920x1080 @ 30.00 FPS, 300 frames
  Extracting audio...
  ✓ Audio extracted successfully
  Processing video frames...
  Processing frame 300/300 (100%)
  ✓ Processed 300 frames (250 frames with humans detected)
  Merging audio back into video...
  ✓ Audio merged successfully
  ✓ Saved 1247 detection(s) to traffic_video-detections.json
  Processing time: 45.67 seconds (avg 0.15 sec/frame)
  ✓ Saved to traffic_video-background.mp4

✓ Processing completed successfully!
```

### Example 3: Disable Detection for Faster Processing

```bash
python blur_humans.py large_video.mp4 --disable-detection
```

This runs only the human blurring without object detection for faster processing.

### Example 4: Custom Confidence Threshold

```bash
python blur_humans.py photo.jpg --confidence 0.7 --detection-model yolov8m.pt
```

Uses higher confidence threshold (0.7) for both human detection and object detection.

---

## Detected Object Classes

The YOLO model can detect 80 different object classes from the COCO dataset:

**Vehicles:** car, truck, bus, train, boat, airplane, bicycle, motorcycle

**Animals:** dog, cat, bird, horse, sheep, cow, elephant, bear, zebra, giraffe

**People:** person (automatically filtered out)

**Indoor Objects:** chair, couch, bed, dining table, tv, laptop, mouse, keyboard, cell phone, book

**Outdoor Objects:** traffic light, fire hydrant, stop sign, parking meter, bench

**Sports:** sports ball, baseball bat, baseball glove, skateboard, surfboard, tennis racket

**Food:** banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

And many more... (full list of 80 classes)

---

## Performance Considerations

### Processing Speed

- **Single-pass efficiency:** Object detection runs simultaneously with blur processing (no extra pass needed)
- **Model choice matters:** 
  - `yolov8n.pt` - Fastest, ~2x speed of yolov8m.pt
  - `yolov8m.pt` - Default, best balance
  - `yolov8x.pt` - Slowest, ~3x slower than yolov8m.pt

### Memory Usage

- Object detection increases memory usage by ~500MB-2GB depending on model
- For videos, detections are accumulated in memory before writing to JSON
- For very long videos (>10,000 frames), consider processing in chunks

### Tips for Large Videos

1. Use `yolov8n.pt` or `yolov8s.pt` for faster processing
2. Reduce confidence threshold to `0.3` for fewer detections
3. Consider disabling detection with `--disable-detection` if not needed
4. Process on GPU for 5-10x speedup (requires CUDA-enabled PyTorch)

---

## Use Cases

### 1. **Traffic Analysis**
Process traffic camera footage to:
- Identify vehicles and their timestamps
- Track object movement patterns
- Analyze scene composition

### 2. **Scene Understanding**
Catalog objects in images/videos for:
- Automated tagging and indexing
- Content moderation
- Scene classification

### 3. **Privacy-Preserving Analysis**
Blur humans while preserving information about:
- Background objects
- Environmental context
- Scene attributes

### 4. **Data Annotation**
Generate training data with:
- Automated bounding boxes
- Class labels
- Temporal information

### 5. **Security and Surveillance**
Analyze footage while protecting privacy:
- Object tracking
- Event detection
- Anomaly identification

---

## Technical Details

### Detection Pipeline

```
Input Media (Image/Video Frame)
    ↓
[Simultaneous Processing]
    ├── Human Detection (YOLO Segmentation) → Blur/Mask Application
    └── Object Detection (YOLO Detection) → Filter Person Class → JSON Output
    ↓
Output Media + Detections JSON
```

### Implementation Details

1. **Two YOLO Models:**
   - Segmentation model for human blur (yolov8n-seg.pt default)
   - Detection model for objects (yolov8m.pt default)

2. **Person Filtering:**
   - Class ID 0 ("person") is automatically excluded
   - All other 79 COCO classes are included

3. **Timestamp Calculation:**
   - Format: `HH:MM:SS.mmm`
   - Calculated from frame number and FPS
   - Millisecond precision

4. **Bounding Box Format:**
   - Coordinates are in pixels
   - Format: (x1, y1) = top-left, (x2, y2) = bottom-right
   - Rounded to 2 decimal places for cleaner output

---

## Troubleshooting

### Issue: Out of Memory

**Solution:**
- Use smaller detection model (`yolov8n.pt`)
- Process shorter video segments
- Reduce confidence threshold

### Issue: Too Many/Few Detections

**Solution:**
- Adjust confidence threshold with `--confidence` flag
- Higher value (0.7-0.9) = fewer, more confident detections
- Lower value (0.3-0.4) = more detections, some false positives

### Issue: Slow Processing

**Solution:**
- Use faster model (`yolov8n.pt` or `yolov8s.pt`)
- Disable detection with `--disable-detection`
- Enable GPU acceleration (install CUDA-enabled PyTorch)

### Issue: Wrong Objects Detected

**Solution:**
- Increase confidence threshold for more reliable detections
- Use larger model (`yolov8l.pt` or `yolov8x.pt`) for better accuracy
- YOLO is trained on COCO dataset - some specialized objects may not be detected

---

## API/Library Usage

The `HumanBlurProcessor` class can be used programmatically:

```python
from pathlib import Path
from blur_humans import HumanBlurProcessor

# Initialize with detection enabled
processor = HumanBlurProcessor(
    model_name='yolov8n-seg.pt',
    enable_object_detection=True,
    detection_model='yolov8m.pt'
)

# Process an image
image_path = Path('photo.jpg')
processor.process_image(image_path, confidence=0.5)

# Access detections
print(f"Total detections: {len(processor.all_detections)}")
for detection in processor.all_detections:
    print(f"{detection['label']}: {detection['confidence']}")

# Process a video
video_path = Path('video.mp4')
processor.all_detections = []  # Reset for new file
processor.process_video(video_path, confidence=0.5)

# Save detections manually
json_path = Path('custom_detections.json')
processor.save_detections_to_json(json_path, video_path)
```

---

## Future Enhancements

Planned features for future versions:

- [ ] Custom object class filtering (detect only specific classes)
- [ ] Object tracking across frames (track same object over time)
- [ ] Heatmap generation (show where objects appear most)
- [ ] CSV export option
- [ ] Real-time detection visualization
- [ ] Multi-threaded frame processing
- [ ] Custom confidence per object class

---

## Version History

### v3.1.0 (Current)
- ✨ Added background object detection with YOLOv8m
- ✨ Automatic person class filtering
- ✨ Timestamp tracking for video frames
- ✨ JSON export of detections
- ✨ Configurable detection models

### v3.0.0
- Video processing support
- Audio preservation

### v2.1.0
- Black mask mode
- GUI interface

### v2.0.0
- Segmentation-based blur
- HEIC support

---

## License

This tool uses:
- **YOLOv8** (Ultralytics) - AGPL-3.0 License
- **OpenCV** - Apache 2.0 License
- **PyTorch** - BSD-style License

---

## Support

For issues or questions:
1. Check this guide
2. Review the main README.md
3. Test with different confidence thresholds
4. Try different detection models

---

**Made with ❤️ for privacy-preserving object detection and analysis**
