# PyxelNyx Build Quick Reference

**Updated:** December 2, 2025  
**Version:** 3.0 Enhanced

---

## 🚀 Quick Build Commands

### Windows
```cmd
build.bat
```

### macOS / Linux
```bash
./build.sh
```

### Manual Build
```bash
pyinstaller PyxelNyx.spec --clean
```

---

## 📋 Pre-Build Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] PyInstaller installed: `pip install pyinstaller`
- [ ] `gui_enhanced.py` present (entry point)
- [ ] `logo.png` present (GUI branding)
- [ ] `runtime_hook.py` present (multiprocessing fix)

---

## 📦 Output Locations

| Platform | Location | Type |
|----------|----------|------|
| Windows | `dist/PyxelNyx.exe` | Executable |
| macOS | `dist/PyxelNyx.app` | App Bundle |
| Linux | `dist/PyxelNyx` | Executable |

---

## ✅ Post-Build Testing

### Windows
```cmd
dist\PyxelNyx.exe
```

### macOS
```bash
open dist/PyxelNyx.app

# If Gatekeeper blocks:
xattr -cr dist/PyxelNyx.app
```

### Linux
```bash
chmod +x dist/PyxelNyx
./dist/PyxelNyx
```

---

## 🔧 Key Spec File Features

✅ **Entry Point:** gui_enhanced.py (latest version)  
✅ **Hidden Imports:** 80+ dependencies included  
✅ **Runtime Hook:** Multiprocessing fix integrated  
✅ **Resources:** Logo bundled  
✅ **Mode:** GUI (no console)  
✅ **Compression:** UPX enabled  
✅ **Platform:** Cross-platform support  

---

## ⚠️ Important Notes

### YOLO Models
- **Not bundled** in executable (size optimization)
- **Auto-downloaded** on first run by ultralytics
- **Requires internet** on first launch
- **Cached** in `~/.cache/ultralytics/`

### File Sizes
- Windows/Linux: 400-800 MB
- macOS: 450-900 MB
- CPU-only PyTorch: ~100 MB smaller

---

## 🐛 Quick Troubleshooting

### Build Fails
```bash
# Clean everything
rm -rf build/ dist/ __pycache__/

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Try again
pyinstaller PyxelNyx.spec --clean
```

### Missing Modules
Add to `hiddenimports` in `PyxelNyx.spec`

### Logo Missing
Check `logo.png` exists and is in `datas` section

### Processing Hangs
Verify `runtime_hook.py` is referenced in spec

---

## 📚 Documentation

- **Comprehensive Guide:** BUILD_EXECUTABLE.md
- **Detailed Review:** SPEC_FILE_REVIEW_SUMMARY.md
- **User Guide:** README.md
- **Spec File:** PyxelNyx.spec (with inline docs)

---

## 🎯 What's New in This Build Config

✅ Correct entry point (gui_enhanced.py)  
✅ All latest features included:
  - Skin tone detection with temporal tracking
  - Lowered confidence threshold (0.33)
  - Frame skipping capability
  - Border processing fixes
  - Enhanced UI controls

✅ Legacy files backed up (.legacy_files/)  
✅ Build scripts updated for rebranding  
✅ Comprehensive documentation  

---

## 🔗 Quick Links

- **Support:** apps@globalemancipation.ngo
- **Project:** PyxelNyx v3.0 - AI-Powered Privacy Protection
- **Repository:** /home/ubuntu/pyxelnyx_review

---

**Ready to build? Run `build.bat` (Windows) or `./build.sh` (macOS/Linux)** 🚀
