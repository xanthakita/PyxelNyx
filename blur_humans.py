
#!/usr/bin/env python3
"""
Human Blur CLI Tool - Enhanced with Segmentation
A command-line tool to detect and blur humans in images and videos using instance segmentation.
"""

import argparse
import sys
import subprocess
import tempfile
import time
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

# HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False


class HumanBlurProcessor:
    """
    A class to handle human detection and blurring in images and videos using segmentation.
    This modular design allows for easy adaptation to GUI or library use.
    """
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mov'}
    SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | SUPPORTED_VIDEO_FORMATS
    
    def __init__(self, model_name: str = 'yolov8n-seg.pt', blur_intensity: int = 151, blur_passes: int = 3, mask_type: str = 'black', enable_object_detection: bool = False, detection_model: str = 'yolov8m.pt', filename_suffix: str = '-background', keep_audio: bool = True, progress_callback=None):
        """
        Initialize the human blur processor with segmentation support.
        
        Args:
            model_name: YOLO segmentation model to use (yolov8n-seg.pt for speed, yolov8m-seg.pt for better accuracy)
            blur_intensity: Blur kernel size (must be odd, higher = more blur)
            blur_passes: Number of blur passes for more intense effect (default: 3)
            mask_type: Type of masking to apply ('blur' or 'black', default: 'black')
            enable_object_detection: Enable background object detection (default: True)
            detection_model: YOLO model for object detection (default: yolov8m.pt)
            filename_suffix: Custom suffix for output filenames (default: '-background')
            keep_audio: Keep audio in output videos (default: True)
            progress_callback: Optional callback function for progress updates (receives current, total)
        """
        self.blur_intensity = blur_intensity if blur_intensity % 2 == 1 else blur_intensity + 1
        self.blur_passes = max(1, blur_passes)
        self.mask_type = mask_type
        self.use_segmentation = '-seg' in model_name
        self.enable_object_detection = enable_object_detection
        self.all_detections = []  # Store all object detections
        self.filename_suffix = filename_suffix  # Store custom filename suffix
        self.keep_audio = keep_audio  # Store audio handling preference
        self.progress_callback = progress_callback  # Store progress callback
        
        print(f"Loading YOLO model: {model_name}...")
        print(f"Segmentation mode: {'Enabled (Lasso effect)' if self.use_segmentation else 'Disabled (Box blur)'}")
        print(f"Mask type: {self.mask_type.upper()}")
        if self.mask_type == 'blur':
            print(f"Blur settings: intensity={self.blur_intensity}, passes={self.blur_passes}")
        else:
            print(f"Black mask mode enabled")
        
        try:
            self.model = YOLO(model_name)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            sys.exit(1)
        
        # Load object detection model if enabled
        if self.enable_object_detection:
            print(f"Loading object detection model: {detection_model}...")
            try:
                self.detection_model = YOLO(detection_model)
                print("✓ Object detection model loaded successfully")
            except Exception as e:
                print(f"✗ Error loading object detection model: {e}")
                print("⚠ Continuing without object detection")
                self.enable_object_detection = False
    
    def detect_humans_with_masks(self, image: np.ndarray, confidence: float = 0.5) -> List[Tuple[np.ndarray, Optional[np.ndarray]]]:
        """
        Detect humans in an image using YOLO segmentation.
        
        Args:
            image: Input image as numpy array
            confidence: Confidence threshold for detection
            
        Returns:
            List of tuples containing (bounding_box, segmentation_mask)
            - bounding_box: (x1, y1, x2, y2) as numpy array
            - segmentation_mask: Binary mask as numpy array (H, W) or None if not available
        """
        results = self.model(image, conf=confidence, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            masks = result.masks if hasattr(result, 'masks') and result.masks is not None else None
            
            for idx, box in enumerate(boxes):
                # Class 0 is 'person' in COCO dataset
                if int(box.cls[0]) == 0:
                    bbox = box.xyxy[0].cpu().numpy()
                    
                    # Get segmentation mask if available
                    mask = None
                    if masks is not None and self.use_segmentation:
                        # Get mask data
                        mask_data = masks[idx].data[0].cpu().numpy()
                        # Resize mask to match image dimensions
                        mask = cv2.resize(mask_data, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)
                        # Convert to binary mask
                        mask = (mask > 0.5).astype(np.uint8)
                    
                    detections.append((bbox, mask))
        
        return detections
    
    def detect_background_objects(self, image: np.ndarray, confidence: float = 0.5, frame_number: Optional[int] = None, timestamp: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Detect all objects in the image EXCEPT humans (person class).
        
        Args:
            image: Input image as numpy array
            confidence: Confidence threshold for detection
            frame_number: Frame number (for videos, optional)
            timestamp: Timestamp in format HH:MM:SS.mmm (for videos, optional)
            
        Returns:
            List of detection dictionaries with label, confidence, bbox, and frame/timestamp info
        """
        if not self.enable_object_detection:
            return []
        
        results = self.detection_model(image, conf=confidence, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                cls_id = int(box.cls[0])
                
                # Skip person class (class 0 in COCO dataset)
                if cls_id == 0:
                    continue
                
                label = self.detection_model.names[cls_id]
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                
                detection_dict = {
                    "label": label,
                    "confidence": round(conf, 4),
                    "bbox": {
                        "x1": round(xyxy[0], 2),
                        "y1": round(xyxy[1], 2),
                        "x2": round(xyxy[2], 2),
                        "y2": round(xyxy[3], 2)
                    }
                }
                
                # Add frame/timestamp info for videos
                if frame_number is not None:
                    detection_dict["frame"] = frame_number
                if timestamp is not None:
                    detection_dict["timestamp"] = timestamp
                
                detections.append(detection_dict)
        
        return detections
    
    def format_timestamp(self, frame_number: int, fps: float) -> str:
        """
        Convert frame number to timestamp format HH:MM:SS.mmm
        
        Args:
            frame_number: Frame number (0-indexed)
            fps: Frames per second of the video
            
        Returns:
            Timestamp string in format HH:MM:SS.mmm
        """
        total_seconds = frame_number / fps
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def save_detections_to_json(self, output_path: Path, media_path: Path) -> bool:
        """
        Save all collected detections to a JSON file.
        
        Args:
            output_path: Path for the JSON output file
            media_path: Path of the processed media file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_data = {
                "source_file": str(media_path.name),
                "total_detections": len(self.all_detections),
                "detections": self.all_detections
            }
            
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"  ✗ Error saving detections to JSON: {e}")
            return False
    
    def apply_intense_blur(self, image: np.ndarray, kernel_size: int, passes: int = 3) -> np.ndarray:
        """
        Apply multi-pass blur for more intense effect.
        
        Args:
            image: Input image region
            kernel_size: Blur kernel size
            passes: Number of blur iterations
            
        Returns:
            Intensely blurred image
        """
        blurred = image.copy()
        for _ in range(passes):
            blurred = cv2.GaussianBlur(blurred, (kernel_size, kernel_size), 0)
        return blurred
    
    def combine_masks(self, masks: List[np.ndarray]) -> np.ndarray:
        """
        Combine multiple segmentation masks into a single unified mask.
        
        Args:
            masks: List of binary segmentation masks
            
        Returns:
            Combined binary mask where any pixel marked in any mask is marked in result
        """
        if not masks:
            return None
        
        # Start with first mask
        combined = masks[0].astype(np.float32)
        
        # Merge remaining masks using logical OR
        for mask in masks[1:]:
            combined = np.maximum(combined, mask.astype(np.float32))
        
        return combined
    
    def blur_with_mask(self, image: np.ndarray, mask: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        """
        Apply blur to image using segmentation mask (lasso effect).
        
        Args:
            image: Input image
            mask: Binary segmentation mask (can be combined from multiple detections)
            bbox: Bounding box (x1, y1, x2, y2) - not used but kept for compatibility
            
        Returns:
            Image with masked region blurred
        """
        result = image.copy()
        
        # Create a full image mask
        full_mask = mask.astype(np.float32)
        
        # Apply intense blur to entire image
        blurred_full = self.apply_intense_blur(image, self.blur_intensity, self.blur_passes)
        
        # Blend original and blurred using mask
        # Expand mask to 3 channels for color images
        if len(image.shape) == 3:
            full_mask = np.stack([full_mask] * 3, axis=-1)
        
        # Use mask to blend: result = original * (1 - mask) + blurred * mask
        result = (image * (1 - full_mask) + blurred_full * full_mask).astype(np.uint8)
        
        return result
    
    def black_mask_with_mask(self, image: np.ndarray, mask: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        """
        Apply solid black color to image using segmentation mask (lasso effect).
        
        Args:
            image: Input image
            mask: Binary segmentation mask (can be combined from multiple detections)
            bbox: Bounding box (x1, y1, x2, y2) - not used but kept for compatibility
            
        Returns:
            Image with masked region replaced with solid black
        """
        result = image.copy()
        
        # Create a full image mask
        full_mask = mask.astype(np.float32)
        
        # Create black image with same shape
        black_image = np.zeros_like(image)
        
        # Expand mask to 3 channels for color images
        if len(image.shape) == 3:
            full_mask = np.stack([full_mask] * 3, axis=-1)
        
        # Use mask to blend: result = original * (1 - mask) + black * mask
        result = (image * (1 - full_mask) + black_image * full_mask).astype(np.uint8)
        
        return result
    
    def blur_with_box(self, image: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        """
        Apply blur to bounding box region (fallback method).
        
        Args:
            image: Input image
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Image with box region blurred
        """
        result = image.copy()
        x1, y1, x2, y2 = map(int, bbox)
        
        # Extract and blur region
        region = result[y1:y2, x1:x2]
        if region.size > 0:
            blurred_region = self.apply_intense_blur(region, self.blur_intensity, self.blur_passes)
            result[y1:y2, x1:x2] = blurred_region
        
        return result
    
    def black_mask_with_box(self, image: np.ndarray, bbox: np.ndarray) -> np.ndarray:
        """
        Apply black mask to bounding box region (fallback method).
        
        Args:
            image: Input image
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Image with box region replaced with solid black
        """
        result = image.copy()
        x1, y1, x2, y2 = map(int, bbox)
        
        # Replace region with black
        result[y1:y2, x1:x2] = 0
        
        return result
    
    def load_image(self, image_path: Path) -> Optional[np.ndarray]:
        """
        Load image with support for various formats including HEIC.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Image as numpy array (BGR format) or None if failed
        """
        # Check if HEIC format
        if image_path.suffix.lower() in {'.heic', '.heif'}:
            if not HEIC_SUPPORT:
                print(f"  ⚠ Warning: HEIC support not available. Install pillow-heif: pip install pillow-heif")
                return None
            
            try:
                # Load HEIC using PIL
                pil_image = Image.open(image_path)
                # Convert to RGB then to BGR for OpenCV
                pil_image = pil_image.convert('RGB')
                image = np.array(pil_image)
                # Convert RGB to BGR for OpenCV
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                return image
            except Exception as e:
                print(f"  ✗ Error loading HEIC image: {e}")
                return None
        else:
            # Standard OpenCV loading for other formats
            image = cv2.imread(str(image_path))
            if image is None:
                # Try with PIL as fallback
                try:
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.convert('RGB')
                    image = np.array(pil_image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    return image
                except Exception as e:
                    print(f"  ✗ Error loading image: {e}")
                    return None
            return image
    
    def save_image(self, image: np.ndarray, output_path: Path, original_path: Path) -> bool:
        """
        Save image with format handling.
        
        Args:
            image: Image to save as numpy array
            output_path: Path for output image
            original_path: Original image path for format reference
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # If output is HEIC/HEIF, convert to JPG
            if output_path.suffix.lower() in {'.heic', '.heif'}:
                output_path = output_path.with_suffix('.jpg')
                print(f"  ℹ Converting HEIC to JPG for output")
            
            # Save using OpenCV
            success = cv2.imwrite(str(output_path), image)
            
            if not success:
                # Try PIL as fallback
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image_rgb)
                pil_image.save(output_path)
            
            return True
        except Exception as e:
            print(f"  ✗ Error saving image: {e}")
            return False
    
    def process_image(self, image_path: Path, output_path: Path = None, confidence: float = 0.5) -> bool:
        """
        Process a single image: detect humans and blur them using segmentation.
        Also detect background objects if enabled.
        
        Args:
            image_path: Path to input image
            output_path: Path for output image (optional)
            confidence: Detection confidence threshold
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Start timing
            start_time = time.time()
            
            # Load image with format support
            image = self.load_image(image_path)
            if image is None:
                print(f"✗ Error: Could not read image {image_path}")
                return False
            
            # Detect humans with segmentation masks
            detections = self.detect_humans_with_masks(image, confidence)
            
            if not detections:
                print(f"  No humans detected in {image_path.name}")
                return False
            
            print(f"  Detected {len(detections)} human(s) in {image_path.name}")
            
            # Detect background objects (excluding humans) if enabled
            if self.enable_object_detection:
                print(f"  Detecting background objects...")
                object_detections = self.detect_background_objects(image, confidence)
                self.all_detections.extend(object_detections)
                print(f"  ✓ Detected {len(object_detections)} background object(s)")
            
            # Separate detections into those with masks and those without
            detections_with_masks = [(bbox, mask) for bbox, mask in detections if mask is not None and self.use_segmentation]
            detections_without_masks = [(bbox, mask) for bbox, mask in detections if mask is None or not self.use_segmentation]
            
            result = image.copy()
            
            # Step 1: Combine all segmentation masks and apply mask once
            if detections_with_masks:
                print(f"  Combining masks from {len(detections_with_masks)} person(s)...")
                masks_only = [mask for _, mask in detections_with_masks]
                combined_mask = self.combine_masks(masks_only)
                
                if combined_mask is not None:
                    if self.mask_type == 'blur':
                        print(f"  Applying unified lasso blur to all detected people...")
                        result = self.blur_with_mask(result, combined_mask, None)
                        print(f"  ✓ Lasso blur applied to {len(detections_with_masks)} person(s)")
                    else:  # black mask
                        print(f"  Applying unified black mask to all detected people...")
                        result = self.black_mask_with_mask(result, combined_mask, None)
                        print(f"  ✓ Black mask applied to {len(detections_with_masks)} person(s)")
            
            # Step 2: Apply box mask for any detections without masks (fallback)
            if detections_without_masks:
                if self.mask_type == 'blur':
                    print(f"  Applying box blur fallback to {len(detections_without_masks)} person(s)...")
                    for bbox, _ in detections_without_masks:
                        result = self.blur_with_box(result, bbox)
                    print(f"  ✓ Box blur applied to {len(detections_without_masks)} person(s)")
                else:  # black mask
                    print(f"  Applying box black mask fallback to {len(detections_without_masks)} person(s)...")
                    for bbox, _ in detections_without_masks:
                        result = self.black_mask_with_box(result, bbox)
                    print(f"  ✓ Box black mask applied to {len(detections_without_masks)} person(s)")
            
            # Determine output path
            if output_path is None:
                output_suffix = image_path.suffix
                # Convert HEIC to JPG for output
                if output_suffix.lower() in {'.heic', '.heif'}:
                    output_suffix = '.jpg'
                output_path = image_path.parent / f"{image_path.stem}{self.filename_suffix}{output_suffix}"
            
            # Save result
            if self.save_image(result, output_path, image_path):
                # Save object detections to JSON if enabled
                if self.enable_object_detection and self.all_detections:
                    json_path = image_path.parent / f"{image_path.stem}-detections.json"
                    if self.save_detections_to_json(json_path, image_path):
                        print(f"  ✓ Saved {len(self.all_detections)} detection(s) to {json_path.name}")
                
                # Calculate and display processing time
                processing_time = time.time() - start_time
                print(f"  Processing time: {processing_time:.2f} seconds")
                print(f"  ✓ Saved to {output_path.name}")
                return True
            else:
                return False
            
        except Exception as e:
            print(f"✗ Error processing {image_path}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def check_ffmpeg_available(self) -> bool:
        """
        Check if ffmpeg is available in system PATH.
        
        Returns:
            True if ffmpeg is available, False otherwise
        """
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """
        Extract audio from video using ffmpeg.
        
        Args:
            video_path: Path to input video
            audio_path: Path to save extracted audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run([
                'ffmpeg', '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'copy',  # Copy audio codec
                '-y',  # Overwrite output file
                str(audio_path)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def merge_audio(self, video_path: Path, audio_path: Path, output_path: Path) -> bool:
        """
        Merge audio into video using ffmpeg.
        
        Args:
            video_path: Path to video file (without audio)
            audio_path: Path to audio file
            output_path: Path for output video
            
        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run([
                'ffmpeg', '-i', str(video_path),
                '-i', str(audio_path),
                '-c:v', 'copy',  # Copy video codec
                '-c:a', 'aac',  # Encode audio to AAC
                '-strict', 'experimental',
                '-y',  # Overwrite output file
                str(output_path)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def process_video(self, video_path: Path, output_path: Path = None, confidence: float = 0.5) -> bool:
        """
        Process a video: detect humans and blur them frame by frame using segmentation.
        
        Args:
            video_path: Path to input video
            output_path: Path for output video (optional)
            confidence: Detection confidence threshold
            
        Returns:
            True if successful, False otherwise
        """
        temp_video_path = None
        audio_path = None
        has_audio = False
        
        try:
            # Start timing
            start_time = time.time()
            
            # Open video
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                print(f"  ✗ Error: Could not open video {video_path}")
                return False
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            print(f"  Video properties: {width}x{height} @ {fps:.2f} FPS, {total_frames} frames")
            
            # Determine output path
            if output_path is None:
                output_path = video_path.parent / f"{video_path.stem}{self.filename_suffix}{video_path.suffix}"
            
            # Check for ffmpeg availability for audio processing
            ffmpeg_available = self.check_ffmpeg_available()
            
            # Try to extract audio if ffmpeg is available and user wants to keep audio
            if ffmpeg_available and self.keep_audio:
                audio_path = Path(tempfile.mktemp(suffix='.aac'))
                print(f"  Extracting audio...")
                has_audio = self.extract_audio(video_path, audio_path)
                if has_audio:
                    print(f"  ✓ Audio extracted successfully")
                else:
                    print(f"  ℹ No audio track found or unable to extract")
            elif not self.keep_audio:
                print(f"  ℹ Audio removal requested - output will have no audio")
            else:
                print(f"  ⚠ ffmpeg not available - audio will not be preserved")
                print(f"  ℹ Install ffmpeg to enable audio preservation")
            
            # Create temporary video path for processing (without audio)
            if has_audio:
                temp_video_path = Path(tempfile.mktemp(suffix=video_path.suffix))
                video_writer_path = temp_video_path
            else:
                video_writer_path = output_path
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v codec
            out = cv2.VideoWriter(str(video_writer_path), fourcc, fps, (width, height))
            
            if not out.isOpened():
                print(f"  ✗ Error: Could not create video writer")
                cap.release()
                return False
            
            print(f"  Processing video frames...")
            
            frame_count = 0
            processed_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Call progress callback if provided
                if self.progress_callback:
                    self.progress_callback(frame_count, total_frames)
                
                # Show progress every 10 frames or at the end
                if frame_count % 10 == 0 or frame_count == total_frames:
                    print(f"  Processing frame {frame_count}/{total_frames} ({frame_count*100//total_frames}%)", end='\r')
                
                # Detect humans with segmentation masks
                detections = self.detect_humans_with_masks(frame, confidence)
                
                # Detect background objects (excluding humans) if enabled
                if self.enable_object_detection:
                    timestamp = self.format_timestamp(frame_count - 1, fps)  # frame_count is 1-indexed
                    object_detections = self.detect_background_objects(
                        frame, 
                        confidence, 
                        frame_number=frame_count,
                        timestamp=timestamp
                    )
                    self.all_detections.extend(object_detections)
                
                if detections:
                    processed_count += 1
                    
                    # Separate detections into those with masks and those without
                    detections_with_masks = [(bbox, mask) for bbox, mask in detections if mask is not None and self.use_segmentation]
                    detections_without_masks = [(bbox, mask) for bbox, mask in detections if mask is None or not self.use_segmentation]
                    
                    result = frame.copy()
                    
                    # Apply unified mask for all detections with masks
                    if detections_with_masks:
                        masks_only = [mask for _, mask in detections_with_masks]
                        combined_mask = self.combine_masks(masks_only)
                        
                        if combined_mask is not None:
                            if self.mask_type == 'blur':
                                result = self.blur_with_mask(result, combined_mask, None)
                            else:  # black mask
                                result = self.black_mask_with_mask(result, combined_mask, None)
                    
                    # Apply box mask for any detections without masks (fallback)
                    if detections_without_masks:
                        for bbox, _ in detections_without_masks:
                            if self.mask_type == 'blur':
                                result = self.blur_with_box(result, bbox)
                            else:  # black mask
                                result = self.black_mask_with_box(result, bbox)
                    
                    out.write(result)
                else:
                    # No humans detected, write original frame
                    out.write(frame)
            
            # Release resources
            cap.release()
            out.release()
            
            print(f"\n  ✓ Processed {frame_count} frames ({processed_count} frames with humans detected)")
            
            # Merge audio back if available
            if has_audio and ffmpeg_available and audio_path.exists():
                print(f"  Merging audio back into video...")
                if self.merge_audio(temp_video_path, audio_path, output_path):
                    print(f"  ✓ Audio merged successfully")
                    # Clean up temp files
                    temp_video_path.unlink()
                else:
                    print(f"  ⚠ Failed to merge audio, saving video without audio")
                    # If merge failed, use the video without audio
                    if temp_video_path.exists():
                        temp_video_path.rename(output_path)
                
                # Clean up audio file
                if audio_path.exists():
                    audio_path.unlink()
            
            # Save object detections to JSON if enabled
            if self.enable_object_detection and self.all_detections:
                json_path = video_path.parent / f"{video_path.stem}-detections.json"
                if self.save_detections_to_json(json_path, video_path):
                    print(f"  ✓ Saved {len(self.all_detections)} detection(s) to {json_path.name}")
            
            # Calculate and display processing time
            processing_time = time.time() - start_time
            avg_per_frame = processing_time / frame_count if frame_count > 0 else 0
            print(f"  Processing time: {processing_time:.2f} seconds (avg {avg_per_frame:.2f} sec/frame)")
            print(f"  ✓ Saved to {output_path.name}")
            return True
            
        except Exception as e:
            print(f"  ✗ Error processing video {video_path}: {e}")
            import traceback
            traceback.print_exc()
            
            # Clean up temp files on error
            if temp_video_path and temp_video_path.exists():
                temp_video_path.unlink()
            if audio_path and audio_path.exists():
                audio_path.unlink()
            
            return False
    
    def process_directory(self, directory_path: Path, confidence: float = 0.5, media_type: str = 'both') -> Tuple[int, int]:
        """
        Process all images and/or videos in a directory.
        
        Args:
            directory_path: Path to directory containing media files
            confidence: Detection confidence threshold
            media_type: Type of media to process ('images', 'videos', or 'both')
            
        Returns:
            Tuple of (successful_count, total_count)
        """
        # Determine which formats to search for based on media_type
        if media_type == 'images':
            formats_to_process = self.SUPPORTED_IMAGE_FORMATS
        elif media_type == 'videos':
            formats_to_process = self.SUPPORTED_VIDEO_FORMATS
        else:  # 'both'
            formats_to_process = self.SUPPORTED_FORMATS
        
        # Find all supported media files
        image_files = []
        video_files = []
        
        for ext in formats_to_process:
            found_files = list(directory_path.glob(f"*{ext}")) + list(directory_path.glob(f"*{ext.upper()}"))
            for file in found_files:
                if file.suffix.lower() in self.SUPPORTED_IMAGE_FORMATS:
                    image_files.append(file)
                elif file.suffix.lower() in self.SUPPORTED_VIDEO_FORMATS:
                    video_files.append(file)
        
        total_files = len(image_files) + len(video_files)
        
        if total_files == 0:
            print(f"✗ No supported media files found in {directory_path}")
            return 0, 0
        
        # Print summary
        if image_files and video_files:
            print(f"\nFound {len(image_files)} image(s) and {len(video_files)} video(s) to process\n")
        elif image_files:
            print(f"\nFound {len(image_files)} image(s) to process\n")
        else:
            print(f"\nFound {len(video_files)} video(s) to process\n")
        
        successful = 0
        current = 0
        
        # Process images first
        for image_path in image_files:
            current += 1
            self.all_detections = []  # Reset detections for each file
            print(f"Processing [{current}/{total_files}] (Image): {image_path.name}")
            if self.process_image(image_path, confidence=confidence):
                successful += 1
            print()
        
        # Process videos
        for video_path in video_files:
            current += 1
            self.all_detections = []  # Reset detections for each file
            print(f"Processing [{current}/{total_files}] (Video): {video_path.name}")
            if self.process_video(video_path, confidence=confidence):
                successful += 1
            print()
        
        return successful, total_files


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Detect and blur humans in images and videos using segmentation (lasso effect).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process image with black mask (default)
  %(prog)s photo.jpg
  
  # Process video with black mask
  %(prog)s video.mp4
  
  # Process with blur instead of black mask
  %(prog)s photo.jpg --mask-type blur
  
  # Process all media (images and videos) in a directory
  %(prog)s /path/to/media/
  
  # Process only videos in a directory
  %(prog)s /path/to/media/ --media-type videos
  
  # Process only images in a directory
  %(prog)s /path/to/media/ --media-type images
  
  # Extreme blur with multiple passes
  %(prog)s photo.jpg --mask-type blur --blur 201 --passes 5
  
  # Adjust detection confidence threshold
  %(prog)s photo.jpg --confidence 0.7
  
  # Use a more accurate segmentation model (slower)
  %(prog)s photo.jpg --model yolov8m-seg.pt
  
  # Process HEIC images from iPhone
  %(prog)s IMG_1234.HEIC

Supported image formats: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .webp, .heic, .heif
Supported video formats: .mp4, .mov
Output naming: input.jpg -> input-background.jpg
              input.mp4 -> input-background.mp4
              input.heic -> input-background.jpg (auto-converted)

Note: Audio preservation in videos requires ffmpeg to be installed.
      Install ffmpeg: sudo apt-get install ffmpeg (Linux) or brew install ffmpeg (Mac)
        """
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Path to an image/video file or directory containing media files'
    )
    
    parser.add_argument(
        '--media-type',
        type=str,
        default='both',
        choices=['images', 'videos', 'both'],
        help='Type of media to process when input is a directory (default: both)'
    )
    
    parser.add_argument(
        '-t', '--mask-type',
        type=str,
        default='black',
        choices=['blur', 'black'],
        help='Type of masking to apply: blur or black (default: black)'
    )
    
    parser.add_argument(
        '-b', '--blur',
        type=int,
        default=151,
        help='Blur intensity kernel size (must be odd, default: 151, range: 1-301) - only used with --mask-type blur'
    )
    
    parser.add_argument(
        '-p', '--passes',
        type=int,
        default=3,
        help='Number of blur passes for more intense effect (default: 3, range: 1-10) - only used with --mask-type blur'
    )
    
    parser.add_argument(
        '-c', '--confidence',
        type=float,
        default=0.5,
        help='Detection confidence threshold (0.0-1.0, default: 0.5)'
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='yolov8n-seg.pt',
        choices=['yolov8n-seg.pt', 'yolov8s-seg.pt', 'yolov8m-seg.pt', 'yolov8l-seg.pt', 'yolov8x-seg.pt',
                 'yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'],
        help='YOLO model to use (n=nano/fastest, x=extra-large/most accurate, -seg=segmentation, default: yolov8n-seg.pt)'
    )
    
    parser.add_argument(
        '--enable-detection',
        action='store_true',
        default=False,
        help='Enable background object detection (default: disabled)'
    )
    
    parser.add_argument(
        '--disable-detection',
        action='store_true',
        help='Disable background object detection'
    )
    
    parser.add_argument(
        '--detection-model',
        type=str,
        default='yolov8m.pt',
        choices=['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'],
        help='YOLO model for object detection (default: yolov8m.pt for better accuracy)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 3.1.0 - Enhanced with Object Detection'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"✗ Error: Path does not exist: {input_path}")
        sys.exit(1)
    
    if args.blur < 1 or args.blur > 301:
        print("✗ Error: Blur intensity must be between 1 and 301")
        sys.exit(1)
    
    if args.passes < 1 or args.passes > 10:
        print("✗ Error: Blur passes must be between 1 and 10")
        sys.exit(1)
    
    if args.confidence < 0.0 or args.confidence > 1.0:
        print("✗ Error: Confidence must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Check HEIC support if needed
    if input_path.is_file() and input_path.suffix.lower() in {'.heic', '.heif'}:
        if not HEIC_SUPPORT:
            print("\n⚠ WARNING: HEIC support not installed!")
            print("Install with: pip install pillow-heif")
            print()
    
    # Determine if object detection should be enabled
    enable_detection = args.enable_detection and not args.disable_detection
    
    # Initialize processor
    print("\n" + "="*70)
    print("Human Blur Tool v3.1 - With Background Object Detection")
    print("="*70 + "\n")
    
    processor = HumanBlurProcessor(
        model_name=args.model, 
        blur_intensity=args.blur,
        blur_passes=args.passes,
        mask_type=args.mask_type,
        enable_object_detection=enable_detection,
        detection_model=args.detection_model
    )
    
    # Process based on input type
    if input_path.is_file():
        # Determine if it's an image or video
        if input_path.suffix.lower() in processor.SUPPORTED_IMAGE_FORMATS:
            print(f"\nProcessing single image: {input_path.name}\n")
            success = processor.process_image(input_path, confidence=args.confidence)
        elif input_path.suffix.lower() in processor.SUPPORTED_VIDEO_FORMATS:
            print(f"\nProcessing single video: {input_path.name}\n")
            success = processor.process_video(input_path, confidence=args.confidence)
        else:
            print(f"✗ Error: Unsupported file format: {input_path.suffix}")
            print(f"Supported image formats: {', '.join(sorted(processor.SUPPORTED_IMAGE_FORMATS))}")
            print(f"Supported video formats: {', '.join(sorted(processor.SUPPORTED_VIDEO_FORMATS))}")
            sys.exit(1)
        
        if success:
            print("\n✓ Processing completed successfully!")
        else:
            print("\n✗ Processing failed")
            sys.exit(1)
    
    elif input_path.is_dir():
        print(f"\nProcessing directory: {input_path}")
        print(f"Media type filter: {args.media_type}\n")
        successful, total = processor.process_directory(input_path, confidence=args.confidence, media_type=args.media_type)
        print("="*70)
        print(f"Results: {successful}/{total} file(s) processed successfully")
        print("="*70)
        
        if successful == 0:
            sys.exit(1)
    
    else:
        print(f"✗ Error: Invalid input path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
