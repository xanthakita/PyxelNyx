# New Features Added to Human Blur Tool

## Overview
Two new options have been successfully added to the Human Blur Tool GUI to provide users with more control over their output files:

1. **Audio Handling Option** - Choose whether to keep or remove audio from video files
2. **Custom Filename Suffix** - Specify a custom suffix for output filenames

---

## 1. Audio Handling Option 🔊

### Description
Users can now choose whether to keep or remove audio from processed video files. This is particularly useful when:
- You want to create silent videos for privacy reasons
- The audio contains sensitive information that should be removed
- You need smaller file sizes (removing audio reduces file size)
- You're creating content for specific platforms that don't require audio

### Location in GUI
Found in the **Output Settings** section, below the filename suffix field.

### How to Use
- **Checkbox Label:** "🔊 Keep audio in output videos (requires ffmpeg)"
- **Default:** Checked (audio is kept by default)
- **Action:** 
  - **Checked:** Audio will be preserved in the output video (requires ffmpeg to be installed)
  - **Unchecked:** Audio will be removed from the output video

### Technical Details
- Requires ffmpeg to be installed on the system for audio extraction and merging
- If ffmpeg is not available, a warning message will be displayed
- Audio is extracted before processing and merged back after video processing is complete
- Works for both single file and batch folder processing

### Example Output
- With audio: `video.mp4` → `video-background.mp4` (with audio)
- Without audio: `video.mp4` → `video-background.mp4` (silent video)

---

## 2. Custom Filename Suffix 📝

### Description
Users can now customize the suffix that gets appended to output filenames instead of using the default `-background` suffix. This allows for:
- Better organization of processed files
- Meaningful naming conventions for different processing types
- Easier identification of processed files in large batches

### Location in GUI
Found in the **Output Settings** section, above the audio handling checkbox.

### How to Use
- **Field Label:** "Filename suffix:"
- **Default Value:** `-background`
- **Input Type:** Text field
- **Example Values:**
  - `-background` (default)
  - `-blurred`
  - `-processed`
  - `-censored`
  - `-privacy`
  - Any custom text you prefer!

### Technical Details
- The suffix is appended before the file extension
- Works for both images and videos
- Works for both single file and batch folder processing
- Supports all special characters that are valid in filenames
- The suffix is remembered during the session

### Example Outputs

| Original File | Custom Suffix | Output File |
|--------------|---------------|-------------|
| photo.jpg | `-background` | photo-background.jpg |
| photo.jpg | `-blurred` | photo-blurred.jpg |
| video.mp4 | `-processed` | video-processed.mp4 |
| image.png | `-privacy` | image-privacy.png |
| IMG_1234.HEIC | `-censored` | IMG_1234-censored.jpg |

---

## GUI Layout

The new **Output Settings** section appears after the **Advanced Settings** section and contains:

```
┌─ Output Settings ─────────────────────────────────────────┐
│                                                            │
│  Filename suffix: [_____________]                         │
│                   (e.g., '-background', '-blurred', etc.) │
│                                                            │
│  ☑ Keep audio in output videos (requires ffmpeg)          │
│     (Uncheck to remove audio from videos)                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Code Changes Summary

### Files Modified

#### 1. `gui_enhanced.py`
- Added two new GUI variables: `keep_audio` and `filename_suffix`
- Created new "Output Settings" section with:
  - Text entry field for custom filename suffix
  - Checkbox for audio handling
- Updated processor initialization to pass new parameters
- Updated output path generation to use custom suffix
- Updated help documentation to explain new features
- Updated batch processing completion message to show custom suffix

#### 2. `blur_humans.py`
- Updated `HumanBlurProcessor.__init__()` to accept:
  - `filename_suffix` parameter (default: `-background`)
  - `keep_audio` parameter (default: `True`)
- Modified `process_image()` to use custom filename suffix
- Modified `process_video()` to:
  - Use custom filename suffix
  - Respect the `keep_audio` setting
  - Display appropriate messages based on audio handling choice

---

## Usage Examples

### Example 1: Keep Audio with Custom Suffix
1. Select a video file
2. Set filename suffix to: `-privacy`
3. Keep audio checkbox: **Checked**
4. Process the video
5. Result: `video-privacy.mp4` (with audio)

### Example 2: Remove Audio with Custom Suffix
1. Select a video file
2. Set filename suffix to: `-silent`
3. Keep audio checkbox: **Unchecked**
4. Process the video
5. Result: `video-silent.mp4` (without audio)

### Example 3: Batch Processing with Custom Settings
1. Select a folder containing multiple videos
2. Set filename suffix to: `-blurred`
3. Keep audio checkbox: **Checked**
4. Click "Process Media"
5. Result: All videos processed with `-blurred` suffix and audio preserved

---

## Benefits

### For Users
- **More Control:** Fine-tune output files to match specific needs
- **Better Organization:** Use meaningful suffixes for different processing batches
- **Privacy Options:** Remove audio when needed for sensitive content
- **Flexibility:** Works seamlessly with all existing features

### For Workflows
- **Professional Use:** Create standardized naming conventions
- **Batch Processing:** Process large folders with consistent settings
- **Storage Management:** Remove audio to save disk space when not needed
- **Quality Assurance:** Easily identify which processing settings were used

---

## Backward Compatibility

All changes are backward compatible:
- Default suffix is still `-background`
- Audio is kept by default (existing behavior)
- All existing features work unchanged
- CLI tool maintains original functionality

---

## Requirements

- **Audio Handling:** Requires ffmpeg to be installed for audio preservation
  - Install on Linux: `sudo apt-get install ffmpeg`
  - Install on Mac: `brew install ffmpeg`
  - Install on Windows: Download from [ffmpeg.org](https://ffmpeg.org/)

---

## Future Enhancements

Possible future improvements:
- Save custom suffix preferences between sessions
- Preset suffix templates
- Audio format options (MP3, AAC, etc.)
- Audio quality settings
- Output directory selection

---

## Support

For questions or issues, contact: apps@globalemancipation.ngo

---

**Version:** 3.0 (Enhanced with Audio Handling and Custom Filename Suffix)
**Date:** November 19, 2025
