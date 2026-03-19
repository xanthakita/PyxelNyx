import React, { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const GUI_HELP = `OVERVIEW
PyxelNyx automatically detects and masks/blurs humans in images and videos using AI (YOLOv8 segmentation).

GETTING STARTED
1. Select Input: Click "Browse File" for a single file, or "Browse Folder" for batch processing
2. Choose Mask Type: Black Mask (default) or Blur
3. Adjust Settings (Optional): blur intensity, passes, confidence, model, skin tone detection
4. Configure Output Settings (Optional): filename suffix, frame interval, audio handling
5. Click "Process Media"

SUPPORTED FORMATS
Images: .jpg .jpeg .png .bmp .tiff .tif .webp .heic .heif
Videos: .mp4 .mov

OUTPUT
Processed files are saved with your chosen suffix (default "-background"):
  photo.jpg → photo-background.jpg
  video.mp4 → video-background.mp4
Original files are never modified.

TIPS
• For speed: Use default yolov8n-seg.pt model
• For accuracy: Use yolov8m-seg.pt or higher
• Lower confidence (0.3): Detect more people (more false positives)
• Higher confidence (0.7): Stricter detection (fewer false positives)
• Black mask mode is fastest

ERRORS
If you encounter unsupported file errors: apps@globalemancipation.ngo`;

const CLI_HELP = `BASIC USAGE
Process a single image with black mask (default):
  python blur_humans.py photo.jpg

Process with blur instead of black mask:
  python blur_humans.py photo.jpg --mask-type blur

Process a video:
  python blur_humans.py video.mp4

Process all files in a directory:
  python blur_humans.py /path/to/media/

ADVANCED OPTIONS
Extreme blur with more passes:
  python blur_humans.py photo.jpg --mask-type blur --blur 201 --passes 5

Adjust detection sensitivity:
  python blur_humans.py photo.jpg --confidence 0.7

Use more accurate model (slower):
  python blur_humans.py photo.jpg --model yolov8m-seg.pt

COMMAND-LINE ARGUMENTS
input               Path to image/video file or directory (required)
--media-type        Media filter: images, videos, both (default: both)
--mask-type, -t     Masking type: black or blur (default: black)
--blur, -b          Blur kernel size 1-301 (default: 151)
--passes, -p        Number of blur passes 1-10 (default: 3)
--confidence, -c    Detection threshold 0.0-1.0 (default: 0.33)
--model, -m         YOLO model selection (default: yolov8n-seg.pt)

MODEL SELECTION
yolov8n-seg.pt  ⚡⚡⚡⚡⚡ ⭐⭐⭐       Default, fastest
yolov8s-seg.pt  ⚡⚡⚡⚡   ⭐⭐⭐⭐     Good balance
yolov8m-seg.pt  ⚡⚡⚡     ⭐⭐⭐⭐⭐   Higher accuracy
yolov8l-seg.pt  ⚡⚡       ⭐⭐⭐⭐⭐   Professional use
yolov8x-seg.pt  ⚡         ⭐⭐⭐⭐⭐   Maximum accuracy`;

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function HelpDialog({ open, onClose }: Props) {
  const [tab, setTab] = useState(0);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Help — PyxelNyx</DialogTitle>
      <DialogContent>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
          <Tab label="GUI Usage" />
          <Tab label="CLI Usage" />
        </Tabs>
        <Box sx={{ height: 400, overflow: 'auto' }}>
          <Typography
            component="pre"
            variant="body2"
            sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: 12 }}
          >
            {tab === 0 ? GUI_HELP : CLI_HELP}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}
