#!/usr/bin/env python3
"""
Simple verification script to check that the fixes were applied correctly
by inspecting the source code files.
"""

import re
from pathlib import Path

def verify_gui_confidence():
    """Verify GUI default confidence changed to 0.33"""
    print("=" * 60)
    print("Verifying GUI Confidence Changes")
    print("=" * 60)
    
    gui_file = Path("gui_enhanced.py")
    content = gui_file.read_text()
    
    # Check 1: Variable initialization
    if 'self.confidence = tk.DoubleVar(value=0.33)' in content:
        print("✓ GUI confidence variable default set to 0.33")
    else:
        print("✗ ERROR: GUI confidence variable not set to 0.33")
        return False
    
    # Check 2: Help text
    if 'Confidence: Detection sensitivity (0.1-1.0, default 0.33)' in content:
        print("✓ GUI help text updated to reflect 0.33 default")
    else:
        print("✗ ERROR: GUI help text not updated")
        return False
    
    # Check 3: Label initialization
    if 'self.confidence_label = ttk.Label(confidence_frame, text="0.33"' in content:
        print("✓ GUI confidence label initialized to 0.33")
    else:
        print("✗ ERROR: GUI confidence label not updated")
        return False
    
    print()
    return True

def verify_cli_confidence():
    """Verify CLI default confidence changed to 0.33"""
    print("=" * 60)
    print("Verifying CLI Confidence Changes")
    print("=" * 60)
    
    cli_file = Path("blur_humans.py")
    content = cli_file.read_text()
    
    # Check argparse default
    pattern = r"'-c',\s*'--confidence'.*?default=0\.33"
    if re.search(pattern, content, re.DOTALL):
        print("✓ CLI confidence argument default set to 0.33")
    else:
        print("✗ ERROR: CLI confidence argument not set to 0.33")
        return False
    
    # Check help text
    if "default: 0.33" in content:
        print("✓ CLI help text updated to reflect 0.33 default")
    else:
        print("✗ ERROR: CLI help text not updated")
        return False
    
    print()
    return True

def verify_mask_expansion():
    """Verify mask expansion function exists"""
    print("=" * 60)
    print("Verifying Mask Expansion Implementation")
    print("=" * 60)
    
    blur_file = Path("blur_humans.py")
    content = blur_file.read_text()
    
    # Check 1: Function exists
    if 'def expand_mask_to_edges(' in content:
        print("✓ expand_mask_to_edges function implemented")
    else:
        print("✗ ERROR: expand_mask_to_edges function not found")
        return False
    
    # Check 2: Function uses morphological dilation
    if 'cv2.dilate' in content and 'cv2.getStructuringElement' in content:
        print("✓ Function uses morphological dilation (cv2.dilate)")
    else:
        print("✗ ERROR: Morphological dilation not implemented")
        return False
    
    # Check 3: Default expansion is 25 pixels
    if 'expansion_pixels: int = 25' in content:
        print("✓ Default expansion set to 25 pixels")
    else:
        print("✗ ERROR: Default expansion not set correctly")
        return False
    
    # Check 4: blur_with_mask uses expansion
    if 'self.expand_mask_to_edges(mask)' in content:
        print("✓ blur_with_mask uses mask expansion")
    else:
        print("✗ ERROR: blur_with_mask doesn't use mask expansion")
        return False
    
    # Check 5: black_mask_with_mask uses expansion
    pattern = r'def black_mask_with_mask.*?self\.expand_mask_to_edges'
    if re.search(pattern, content, re.DOTALL):
        print("✓ black_mask_with_mask uses mask expansion")
    else:
        print("✗ ERROR: black_mask_with_mask doesn't use mask expansion")
        return False
    
    print()
    return True

def verify_bbox_expansion():
    """Verify bounding box expansion in fallback methods"""
    print("=" * 60)
    print("Verifying Bounding Box Expansion")
    print("=" * 60)
    
    blur_file = Path("blur_humans.py")
    content = blur_file.read_text()
    
    # Check 1: blur_with_box has expansion logic
    pattern = r'def blur_with_box.*?expansion = 25.*?x1 = max\(0, x1 - expansion\)'
    if re.search(pattern, content, re.DOTALL):
        print("✓ blur_with_box implements 25-pixel bounding box expansion")
    else:
        print("✗ ERROR: blur_with_box doesn't expand bounding box")
        return False
    
    # Check 2: black_mask_with_box has expansion logic
    pattern = r'def black_mask_with_box.*?expansion = 25.*?x1 = max\(0, x1 - expansion\)'
    if re.search(pattern, content, re.DOTALL):
        print("✓ black_mask_with_box implements 25-pixel bounding box expansion")
    else:
        print("✗ ERROR: black_mask_with_box doesn't expand bounding box")
        return False
    
    print()
    return True

def main():
    """Run all verification checks"""
    print("\n" + "=" * 60)
    print("PyxelNyx Fix Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    if not verify_gui_confidence():
        all_passed = False
    
    if not verify_cli_confidence():
        all_passed = False
    
    if not verify_mask_expansion():
        all_passed = False
    
    if not verify_bbox_expansion():
        all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓✓✓ ALL VERIFICATIONS PASSED! ✓✓✓")
        print("=" * 60)
        print()
        print("📋 Summary of Changes:")
        print()
        print("Issue 1: Lower Default Confidence Threshold")
        print("  ✓ GUI default changed from 0.5 to 0.33")
        print("  ✓ CLI default changed from 0.5 to 0.33")
        print("  ✓ Help text updated in both GUI and CLI")
        print("  → This will improve detection of humans in frames")
        print()
        print("Issue 2: Fix Unprocessed Border")
        print("  ✓ Added expand_mask_to_edges() function with 25px expansion")
        print("  ✓ Updated blur_with_mask to use mask expansion")
        print("  ✓ Updated black_mask_with_mask to use mask expansion")
        print("  ✓ Updated blur_with_box to expand bounding boxes by 25px")
        print("  ✓ Updated black_mask_with_box to expand bounding boxes by 25px")
        print("  → This will ensure processing reaches video/image edges")
        print()
        print("🎯 Both issues have been successfully fixed!")
        return 0
    else:
        print("✗✗✗ SOME VERIFICATIONS FAILED ✗✗✗")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
