# Quick Reference - New Features

## 🎯 What's New?

Two powerful new options have been added to the PyxelNyx GUI:

| Feature | Type | Default | Purpose |
|---------|------|---------|---------|
| **Audio Handling** | Checkbox | ☑ Checked | Choose to keep or remove audio from videos |
| **Filename Suffix** | Text Field | `-background` | Customize the suffix added to output files |

---

## 🖥️ Where to Find Them?

Look for the new **"Output Settings"** section in the GUI, located between:
- **Above:** Advanced Settings
- **Below:** Process Media button

```
[Advanced Settings Section]
         ↓
[OUTPUT SETTINGS SECTION] ← NEW!
         ↓
[Process Media Button]
```

---

## 📝 Filename Suffix - Quick Guide

### What It Does
Lets you customize the suffix added to processed files.

### Examples

| Original File | Suffix | Output File |
|--------------|--------|-------------|
| photo.jpg | `-background` | photo-background.jpg |
| photo.jpg | `-blurred` | photo-blurred.jpg |
| video.mp4 | `-privacy` | video-privacy.mp4 |
| image.png | `-censored` | image-censored.png |

### Common Use Cases
- `-privacy` - For privacy-focused processing
- `-blurred` - When using blur mode
- `-anonymous` - For anonymization
- `-processed` - Generic processing marker
- `-[date]` - Date-stamped processing (e.g., `-20251119`)

---

## 🔊 Audio Handling - Quick Guide

### What It Does
Controls whether audio is kept or removed from processed videos.

### Options

| Checkbox State | Result | Use When |
|----------------|--------|----------|
| ☑ **Checked** | Audio kept | You want to preserve narration/sounds |
| ☐ **Unchecked** | Audio removed | You want silent videos for privacy |

### Requirements
- **Needs:** ffmpeg installed on your system
- **Affects:** Video files only (.mp4, .mov)
- **Doesn't affect:** Image files

### Examples

**Keep Audio:**
```
Input:  presentation.mp4 (with narration)
Output: presentation-background.mp4 (narration preserved)
```

**Remove Audio:**
```
Input:  meeting.mp4 (with conversations)
Output: meeting-background.mp4 (silent video)
```

---

## 🚀 Quick Start Examples

### Example 1: Basic Usage (Default)
```
1. Open GUI
2. Select file: photo.jpg
3. Click "Process Media"
Result: photo-background.jpg
```

### Example 2: Custom Suffix
```
1. Open GUI
2. Select file: photo.jpg
3. Change suffix to: -privacy
4. Click "Process Media"
Result: photo-privacy.jpg
```

### Example 3: Remove Audio
```
1. Open GUI
2. Select file: video.mp4
3. Uncheck "Keep audio"
4. Click "Process Media"
Result: video-background.mp4 (no audio)
```

### Example 4: Custom Suffix + No Audio
```
1. Open GUI
2. Select file: video.mp4
3. Change suffix to: -anonymous
4. Uncheck "Keep audio"
5. Click "Process Media"
Result: video-anonymous.mp4 (no audio)
```

---

## 📊 Feature Comparison

### Before This Update
```
✗ Audio always kept (if present)
✗ Filename always used "-background" suffix
✗ No customization options
```

### After This Update
```
✓ Choose to keep or remove audio
✓ Customize filename suffix
✓ Full control over outputs
✓ Works in batch mode
```

---

## 🎯 Common Scenarios

### Scenario 1: Social Media Content
**Goal:** Privacy-friendly videos with custom branding

**Settings:**
- Suffix: `-social`
- Audio: Keep ☑
- Mask: Blur

**Output:** `video-social.mp4` (blurred faces, audio kept)

---

### Scenario 2: Documentation
**Goal:** Anonymized photos for documentation

**Settings:**
- Suffix: `-docs`
- Mask: Black

**Output:** `photo-docs.jpg` (black silhouettes)

---

### Scenario 3: Surveillance Footage
**Goal:** Anonymous, silent videos

**Settings:**
- Suffix: `-surveillance`
- Audio: Remove ☐
- Mask: Blur

**Output:** `footage-surveillance.mp4` (blurred, no audio)

---

### Scenario 4: Training Materials
**Goal:** Anonymized with narration kept

**Settings:**
- Suffix: `-training`
- Audio: Keep ☑
- Mask: Black

**Output:** `training-training.mp4` (anonymized, audio kept)

---

## ⚙️ Technical Details

### File Processing
- **Applies to:** Both single files and batch folders
- **Works with:** All supported image and video formats
- **Processing order:** Detect → Blur/Mask → Save with custom name

### Audio Processing (Videos Only)
1. Check ffmpeg availability
2. Extract audio if "Keep audio" is checked
3. Process video frames
4. Merge audio back (if extracted)
5. Save final video

### Filename Generation
```
Original: filename.ext
Pattern: filename[suffix].ext
Example: photo-privacy.jpg
```

---

## 💡 Pro Tips

### Tip 1: Batch Processing
Use descriptive suffixes when processing folders:
```
-batch1, -batch2, etc. for multiple batches
-[project-name] for project-specific processing
```

### Tip 2: Audio File Size
Removing audio can reduce file size by 10-30%:
```
With audio: 100MB
Without audio: 70-90MB
```

### Tip 3: Suffix Organization
Use consistent naming for easy sorting:
```
Good: -privacy, -public, -internal
Better: -priv, -pub, -int (shorter)
```

### Tip 4: Test First
Always test with a single file before batch processing:
```
1. Process one file
2. Check output quality
3. Verify suffix and audio
4. Then process batch
```

---

## ❓ FAQ

**Q: Does the suffix need to start with a dash?**
A: No, but it's recommended for clarity. You can use: `-suffix`, `_suffix`, or just `suffix`

**Q: What happens if I leave the suffix field empty?**
A: The file will have no suffix (may overwrite original if same directory)

**Q: Can I use special characters in the suffix?**
A: Yes, but avoid characters invalid in filenames (/, \, :, *, ?, ", <, >, |)

**Q: Will the audio checkbox affect image files?**
A: No, it only affects video files. Images don't have audio.

**Q: What if ffmpeg is not installed?**
A: Audio cannot be preserved. Install ffmpeg or uncheck the audio option.

**Q: Are my settings saved when I close the GUI?**
A: Settings are remembered during the session but reset when you close the GUI.

**Q: Can I process files with different suffixes in one batch?**
A: No, all files in a batch use the same suffix. Process in separate batches for different suffixes.

**Q: What's the maximum suffix length?**
A: No hard limit, but keep it under 50 characters for compatibility.

---

## 🔧 Troubleshooting

### Problem: Audio checkbox is grayed out
**Solution:** Install ffmpeg on your system

### Problem: Custom suffix not appearing
**Solution:** Check that you entered text in the suffix field

### Problem: Output file overwrites original
**Solution:** Use a suffix (at least "-" or "_")

### Problem: Audio not removed even though unchecked
**Solution:** Verify ffmpeg is installed and working

### Problem: Can't find Output Settings section
**Solution:** Update to latest version of the tool

---

## 📱 Contact & Support

**Email:** apps@globalemancipation.ngo

**Documentation:**
- NEW_FEATURES.md - Full feature documentation
- USAGE_EXAMPLES.md - Detailed examples
- GUI_LAYOUT_PREVIEW.md - Visual guide

---

## ✅ Checklist - Before You Start

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ffmpeg installed (for audio handling)
- [ ] Test file ready for processing
- [ ] Output suffix decided
- [ ] Audio preference determined

---

## 🎉 You're Ready!

Launch the GUI and start using your new features:

```bash
python gui_enhanced.py
```

**Enjoy greater control over your output files!** 🚀

---

**Version:** 3.0 Enhanced
**Date:** November 19, 2025
**Status:** Ready for Use ✅
