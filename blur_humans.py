
#!/usr/bin/env python3
"""
Human Blur CLI Tool
A command-line tool to detect and blur humans in images.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np
from ultralytics import YOLO


class HumanBlurProcessor:
    """
    A class to handle human detection and blurring in images.
    This modular design allows for easy adaptation to GUI or library use.
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    def __init__(self, model_name: str = 'yolov8n.pt', blur_intensity: int = 99):
        """
        Initialize the human blur processor.
        
        Args:
            model_name: YOLO model to use (yolov8n.pt for speed, yolov8m.pt for better accuracy)
            blur_intensity: Blur kernel size (must be odd, higher = more blur)
        """
        self.blur_intensity = blur_intensity if blur_intensity % 2 == 1 else blur_intensity + 1
        print(f"Loading YOLO model: {model_name}...")
        try:
            self.model = YOLO(model_name)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            sys.exit(1)
    
    def detect_humans(self, image: np.ndarray, confidence: float = 0.5) -> List[Tuple[int, int, int, int]]:
        """
        Detect humans in an image using YOLO.
        
        Args:
            image: Input image as numpy array
            confidence: Confidence threshold for detection
            
        Returns:
            List of bounding boxes as (x1, y1, x2, y2) tuples
        """
        results = self.model(image, conf=confidence, verbose=False)
        
        human_boxes = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Class 0 is 'person' in COCO dataset
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    human_boxes.append((x1, y1, x2, y2))
        
        return human_boxes
    
    def blur_regions(self, image: np.ndarray, boxes: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Apply blur to specified regions of an image.
        
        Args:
            image: Input image as numpy array
            boxes: List of bounding boxes to blur
            
        Returns:
            Image with blurred regions
        """
        result = image.copy()
        
        for x1, y1, x2, y2 in boxes:
            # Extract region
            region = result[y1:y2, x1:x2]
            
            # Apply Gaussian blur
            blurred_region = cv2.GaussianBlur(region, (self.blur_intensity, self.blur_intensity), 0)
            
            # Replace original region with blurred version
            result[y1:y2, x1:x2] = blurred_region
        
        return result
    
    def process_image(self, image_path: Path, output_path: Path = None, confidence: float = 0.5) -> bool:
        """
        Process a single image: detect humans and blur them.
        
        Args:
            image_path: Path to input image
            output_path: Path for output image (optional)
            confidence: Detection confidence threshold
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                print(f"✗ Error: Could not read image {image_path}")
                return False
            
            # Detect humans
            human_boxes = self.detect_humans(image, confidence)
            
            if not human_boxes:
                print(f"  No humans detected in {image_path.name}")
                return False
            
            print(f"  Detected {len(human_boxes)} human(s) in {image_path.name}")
            
            # Blur detected regions
            result = self.blur_regions(image, human_boxes)
            
            # Determine output path
            if output_path is None:
                output_path = image_path.parent / f"{image_path.stem}-background{image_path.suffix}"
            
            # Save result
            cv2.imwrite(str(output_path), result)
            print(f"  ✓ Saved to {output_path.name}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error processing {image_path}: {e}")
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
        description='Detect and blur humans in images to enable background analysis.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single image with default settings
  %(prog)s photo.jpg
  
  # Process all images in a directory
  %(prog)s /path/to/images/
  
  # Adjust blur intensity (1-99, must be odd, higher = more blur)
  %(prog)s photo.jpg --blur 51
  
  # Adjust detection confidence threshold
  %(prog)s photo.jpg --confidence 0.7
  
  # Use a more accurate model (slower)
  %(prog)s photo.jpg --model yolov8m.pt

Supported formats: .jpg, .jpeg, .png, .bmp, .tiff, .webp
Output naming: input.jpg -> input-background.jpg
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
        default=99,
        help='Blur intensity (1-99, must be odd, default: 99 for maximum blur)'
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
        default='yolov8n.pt',
        choices=['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'],
        help='YOLO model to use (n=nano/fastest, x=extra-large/most accurate, default: yolov8n.pt)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"✗ Error: Path does not exist: {input_path}")
        sys.exit(1)
    
    if args.blur < 1 or args.blur > 99:
        print("✗ Error: Blur intensity must be between 1 and 99")
        sys.exit(1)
    
    if args.confidence < 0.0 or args.confidence > 1.0:
        print("✗ Error: Confidence must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Initialize processor
    print("\n" + "="*60)
    print("Human Blur Tool - Background Analysis Helper")
    print("="*60 + "\n")
    
    processor = HumanBlurProcessor(model_name=args.model, blur_intensity=args.blur)
    
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
        print("="*60)
        print(f"Results: {successful}/{total} images processed successfully")
        print("="*60)
        
        if successful == 0:
            sys.exit(1)
    
    else:
        print(f"✗ Error: Invalid input path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
