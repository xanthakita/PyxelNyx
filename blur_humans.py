
#!/usr/bin/env python3
"""
Human Blur CLI Tool - Enhanced with Segmentation
A command-line tool to detect and blur humans in images using instance segmentation.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional
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
    A class to handle human detection and blurring in images using segmentation.
    This modular design allows for easy adaptation to GUI or library use.
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}
    
    def __init__(self, model_name: str = 'yolov8n-seg.pt', blur_intensity: int = 151, blur_passes: int = 3):
        """
        Initialize the human blur processor with segmentation support.
        
        Args:
            model_name: YOLO segmentation model to use (yolov8n-seg.pt for speed, yolov8m-seg.pt for better accuracy)
            blur_intensity: Blur kernel size (must be odd, higher = more blur)
            blur_passes: Number of blur passes for more intense effect (default: 3)
        """
        self.blur_intensity = blur_intensity if blur_intensity % 2 == 1 else blur_intensity + 1
        self.blur_passes = max(1, blur_passes)
        self.use_segmentation = '-seg' in model_name
        
        print(f"Loading YOLO model: {model_name}...")
        print(f"Segmentation mode: {'Enabled (Lasso effect)' if self.use_segmentation else 'Disabled (Box blur)'}")
        print(f"Blur settings: intensity={self.blur_intensity}, passes={self.blur_passes}")
        
        try:
            self.model = YOLO(model_name)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            sys.exit(1)
    
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
        
        Args:
            image_path: Path to input image
            output_path: Path for output image (optional)
            confidence: Detection confidence threshold
            
        Returns:
            True if successful, False otherwise
        """
        try:
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
            
            # Separate detections into those with masks and those without
            detections_with_masks = [(bbox, mask) for bbox, mask in detections if mask is not None and self.use_segmentation]
            detections_without_masks = [(bbox, mask) for bbox, mask in detections if mask is None or not self.use_segmentation]
            
            result = image.copy()
            
            # Step 1: Combine all segmentation masks and apply blur once
            if detections_with_masks:
                print(f"  Combining masks from {len(detections_with_masks)} person(s)...")
                masks_only = [mask for _, mask in detections_with_masks]
                combined_mask = self.combine_masks(masks_only)
                
                if combined_mask is not None:
                    print(f"  Applying unified lasso blur to all detected people...")
                    result = self.blur_with_mask(result, combined_mask, None)
                    print(f"  ✓ Lasso blur applied to {len(detections_with_masks)} person(s)")
            
            # Step 2: Apply box blur for any detections without masks (fallback)
            if detections_without_masks:
                print(f"  Applying box blur fallback to {len(detections_without_masks)} person(s)...")
                for bbox, _ in detections_without_masks:
                    result = self.blur_with_box(result, bbox)
                print(f"  ✓ Box blur applied to {len(detections_without_masks)} person(s)")
            
            # Determine output path
            if output_path is None:
                output_suffix = image_path.suffix
                # Convert HEIC to JPG for output
                if output_suffix.lower() in {'.heic', '.heif'}:
                    output_suffix = '.jpg'
                output_path = image_path.parent / f"{image_path.stem}-background{output_suffix}"
            
            # Save result
            if self.save_image(result, output_path, image_path):
                print(f"  ✓ Saved to {output_path.name}")
                return True
            else:
                return False
            
        except Exception as e:
            print(f"✗ Error processing {image_path}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def process_directory(self, directory_path: Path, confidence: float = 0.5) -> Tuple[int, int]:
        """
        Process all images in a directory.
        
        Args:
            directory_path: Path to directory containing images
            confidence: Detection confidence threshold
            
        Returns:
            Tuple of (successful_count, total_count)
        """
        # Find all supported image files
        image_files = []
        for ext in self.SUPPORTED_FORMATS:
            image_files.extend(directory_path.glob(f"*{ext}"))
            image_files.extend(directory_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"✗ No supported image files found in {directory_path}")
            return 0, 0
        
        print(f"\nFound {len(image_files)} image(s) to process\n")
        
        successful = 0
        for i, image_path in enumerate(image_files, 1):
            print(f"Processing [{i}/{len(image_files)}]: {image_path.name}")
            if self.process_image(image_path, confidence=confidence):
                successful += 1
            print()
        
        return successful, len(image_files)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Detect and blur humans in images using segmentation (lasso effect).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process with segmentation (lasso effect, default)
  %(prog)s photo.jpg
  
  # Process all images in a directory
  %(prog)s /path/to/images/
  
  # Extreme blur with multiple passes
  %(prog)s photo.jpg --blur 201 --passes 5
  
  # Adjust detection confidence threshold
  %(prog)s photo.jpg --confidence 0.7
  
  # Use a more accurate segmentation model (slower)
  %(prog)s photo.jpg --model yolov8m-seg.pt
  
  # Process HEIC images from iPhone
  %(prog)s IMG_1234.HEIC

Supported formats: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .webp, .heic, .heif
Output naming: input.jpg -> input-background.jpg
              input.heic -> input-background.jpg (auto-converted)
        """
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Path to an image file or directory containing images'
    )
    
    parser.add_argument(
        '-b', '--blur',
        type=int,
        default=151,
        help='Blur intensity kernel size (must be odd, default: 151, range: 1-301)'
    )
    
    parser.add_argument(
        '-p', '--passes',
        type=int,
        default=3,
        help='Number of blur passes for more intense effect (default: 3, range: 1-10)'
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
        '-v', '--version',
        action='version',
        version='%(prog)s 2.0.0 - Enhanced with Segmentation'
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
    
    # Initialize processor
    print("\n" + "="*70)
    print("Human Blur Tool v2.0 - Segmentation-Based Background Blur")
    print("="*70 + "\n")
    
    processor = HumanBlurProcessor(
        model_name=args.model, 
        blur_intensity=args.blur,
        blur_passes=args.passes
    )
    
    # Process based on input type
    if input_path.is_file():
        print(f"\nProcessing single image: {input_path.name}\n")
        success = processor.process_image(input_path, confidence=args.confidence)
        if success:
            print("\n✓ Processing completed successfully!")
        else:
            print("\n✗ Processing failed")
            sys.exit(1)
    
    elif input_path.is_dir():
        print(f"\nProcessing directory: {input_path}\n")
        successful, total = processor.process_directory(input_path, confidence=args.confidence)
        print("="*70)
        print(f"Results: {successful}/{total} images processed successfully")
        print("="*70)
        
        if successful == 0:
            sys.exit(1)
    
    else:
        print(f"✗ Error: Invalid input path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
