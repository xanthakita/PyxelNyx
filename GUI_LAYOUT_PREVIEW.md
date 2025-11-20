# GUI Layout Preview - New Features

## Complete GUI Layout with New Features

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]  PyxelNyx v3.0                                       │
│          AI-Powered Privacy Protection for Images & Videos          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─ Input Selection ─────────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  Select file or folder to process:                            │ │
│  │  [________________________________] [Browse File] [Browse Folder] │
│  │                                                                │ │
│  │  Folder media filter:                                         │ │
│  │  ⦿ Both   ○ Images Only   ○ Videos Only                       │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─ Processing Mode ──────────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  ○ ⬛ Black Mask (Recommended for maximum privacy)             │ │
│  │  ○ 🌫️  Blur (Intelligent contour-following blur)              │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─ Blur Settings (Blur Mode Only) ───────────────────────────────┐ │
│  │                                                                │ │
│  │  Intensity:   [━━━━━━●━━━━━━━━━━━━━━━━]  151                  │ │
│  │  Passes:      [3▼]  (More passes = stronger blur)             │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─ Advanced Settings ────────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  Confidence:  [━━━━━●━━━━━━━━━━━━━━━━]  0.50                  │ │
│  │  Model:       [yolov8n-seg.pt (Fastest)      ▼]               │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─ Output Settings ──────────────────────────────────────────────┐ │ 🆕
│  │                                                                │ │
│  │  Filename suffix:  [-background________]                      │ │ 🆕
│  │                    (e.g., '-background', '-blurred', ...)     │ │
│  │                                                                │ │
│  │  ☑ 🔊 Keep audio in output videos (requires ffmpeg)           │ │ 🆕
│  │     (Uncheck to remove audio from videos)                     │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  [🚀 Process Media]  [❓ Help]                                      │
│                                                                     │
│  ┌─ Processing Progress ──────────────────────────────────────────┐ │
│  │                                                                │ │
│  │  Processing: photo.jpg                                        │ │
│  │  Current file:  [━━━━━━━━━━━━━━━━━━━━]                       │ │
│  │  Overall progress: [━━━━━━━━━━━━━━━━━━]  45%                 │ │
│  │                                                                │ │
│  │  Status: Ready to process media files                         │ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## New "Output Settings" Section - Detailed View

```
┌─ Output Settings ────────────────────────────────────────────────────┐
│                                                                      │
│  📝 Custom Filename Suffix                                          │
│  ────────────────────────────────────────────────────────────────   │
│                                                                      │
│  Filename suffix:  [-background________________]  ← Text Input      │
│                    (e.g., '-background', '-blurred', '-processed')  │
│                                                                      │
│  • Default: "-background"                                           │
│  • Examples: "-privacy", "-censored", "-anonymous"                  │
│  • Applies to both images and videos                                │
│  • Used in both single file and batch processing                    │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🔊 Audio Handling (Videos Only)                                    │
│  ────────────────────────────────────────────────────────────────   │
│                                                                      │
│  ☑ Keep audio in output videos (requires ffmpeg)  ← Checkbox       │
│     (Uncheck to remove audio from videos)                           │
│                                                                      │
│  • Default: Checked (audio preserved)                               │
│  • Requires ffmpeg to be installed                                  │
│  • Only affects video files                                         │
│  • Uncheck to create silent videos                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Before vs After - File Output Examples

### Example 1: Image Processing
```
Before (original behavior):
input.jpg → input-background.jpg

After (with custom suffix "-privacy"):
input.jpg → input-privacy.jpg
```

### Example 2: Video with Audio (default)
```
Before:
video.mp4 → video-background.mp4 (with audio)

After (same default behavior):
video.mp4 → video-background.mp4 (with audio)
```

### Example 3: Video without Audio (new option)
```
Before:
video.mp4 → video-background.mp4 (always with audio if present)

After (audio checkbox unchecked):
video.mp4 → video-background.mp4 (audio removed)
```

### Example 4: Custom Suffix + No Audio
```
Before:
presentation.mp4 → presentation-background.mp4 (with audio)

After (suffix="-anonymous", audio unchecked):
presentation.mp4 → presentation-anonymous.mp4 (no audio)
```

---

## Interactive Elements Detail

### 1. Filename Suffix Text Field
```
┌──────────────────────────────────────────────────────┐
│ Filename suffix: │-background_____________│          │
│                  └─────────────────────────┘          │
│                  ▲                                    │
│                  │ User can type custom suffix here   │
│                                                       │
│ Default: "-background"                                │
│ Validation: None (user responsible)                   │
│ Max length: ~50 characters (reasonable)               │
│ Tooltip: Shows example values                         │
└───────────────────────────────────────────────────────┘
```

### 2. Audio Handling Checkbox
```
┌──────────────────────────────────────────────────────┐
│ [✓] Keep audio in output videos (requires ffmpeg)    │
│     ▲                                                 │
│     │ Checked = Keep audio (default)                 │
│     │ Unchecked = Remove audio                       │
│                                                       │
│ State: Boolean (True/False)                           │
│ Effect: Only applies to video files                   │
│ Requirement: ffmpeg must be installed for audio       │
└───────────────────────────────────────────────────────┘
```

---

## User Interaction Flow

### Flow 1: Using Custom Suffix
```
1. User opens GUI
2. User clicks in "Filename suffix" field
3. User deletes "-background"
4. User types their custom suffix (e.g., "-privacy")
5. User selects file/folder
6. User clicks "Process Media"
7. Output files have custom suffix: "file-privacy.jpg"
```

### Flow 2: Removing Audio from Video
```
1. User opens GUI
2. User selects a video file
3. User unchecks "Keep audio in output videos"
4. User clicks "Process Media"
5. Video is processed
6. Console shows: "Audio removal requested - output will have no audio"
7. Output video has no audio track
```

### Flow 3: Batch Processing with Custom Settings
```
1. User opens GUI
2. User clicks "Browse Folder"
3. User sets "Filename suffix" to "-batch-processed"
4. User unchecks "Keep audio in output videos"
5. User clicks "Process Media"
6. All files in folder are processed with:
   - Custom suffix: "-batch-processed"
   - No audio in videos
7. Progress shows: "Processing [5/20] video-batch-processed.mp4"
```

---

## Settings Persistence During Session

### What is Remembered
```
During a single session (GUI open):
✅ Filename suffix → Kept between different file selections
✅ Audio handling → Kept between different file selections
✅ All other settings → Kept as before

After closing and reopening:
❌ Filename suffix → Returns to default "-background"
❌ Audio handling → Returns to default (checked)
```

---

## Visual Design Notes

### Color Scheme
- Labels: Default text color
- Input fields: Standard entry background
- Help text: Gray color (less prominent)
- Icons: Emoji for visual appeal (🔊, 🆕)

### Layout Principles
- Consistent spacing with other sections
- Clear visual hierarchy
- Helpful contextual information
- No clutter, clean design

### Accessibility
- Clear labels for screen readers
- Logical tab order
- Keyboard accessible
- Visual feedback on interaction

---

## Error Messages and Warnings

### When ffmpeg is not installed
```
Console output:
"⚠ ffmpeg not available - audio will not be preserved"
"ℹ Install ffmpeg to enable audio preservation"
```

### When audio checkbox is unchecked
```
Console output:
"ℹ Audio removal requested - output will have no audio"
```

### When custom suffix is empty
```
Behavior: Uses empty suffix (filename has no suffix)
Example: input.jpg → input.jpg (may overwrite!)
Note: No validation currently implemented
```

---

## Responsive Behavior

### Window Resize
- GUI is non-resizable (fixed size)
- All elements maintain position
- No overlap or clipping issues

### With/Without Logo
- If logo not found: Text layout adjusts
- Title and subtitle remain visible
- No crash or error

---

## Integration with Existing Features

### Works With:
✅ Single file processing (images and videos)
✅ Batch folder processing
✅ All mask types (Black and Blur)
✅ All model selections
✅ All confidence levels
✅ Media type filters (Both, Images Only, Videos Only)

### Does Not Affect:
✅ Detection confidence
✅ Blur intensity and passes
✅ Model selection
✅ Processing speed
✅ Output quality

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║         HUMAN BLUR TOOL - OUTPUT SETTINGS                ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📝 Filename Suffix                                      ║
║  ─────────────────                                       ║
║  • Customize output file names                           ║
║  • Default: "-background"                                ║
║  • Examples: "-privacy", "-blurred", "-censored"         ║
║  • Works with all file types                             ║
║                                                          ║
║  🔊 Audio Handling (Videos)                              ║
║  ────────────────────────                                ║
║  • Keep: ☑ (default) - Preserves audio                  ║
║  • Remove: ☐ - Creates silent video                     ║
║  • Requires: ffmpeg installed                            ║
║  • Only for: Video files (.mp4, .mov)                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## Screenshots (Conceptual)

```
[Input Selection Section]
    ↓
[Processing Mode Section]
    ↓
[Blur Settings Section (conditional)]
    ↓
[Advanced Settings Section]
    ↓
[OUTPUT SETTINGS SECTION] ← NEW! 🆕
    ↓
[Action Buttons]
    ↓
[Processing Progress Section]
```

---

**Note:** This is a conceptual preview. The actual GUI will render with native tkinter widgets and may have slight visual differences depending on the operating system theme.

**To see the actual GUI:** Run `python gui_enhanced.py` after installing dependencies.
