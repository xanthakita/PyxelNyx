# PyxelNyx Electron Migration — Design Spec

**Date**: 2026-03-19
**Version**: 1.0
**Status**: Approved

---

## Overview

Migrate the PyxelNyx Tkinter GUI (`gui.py`) to an Electron front end while keeping the Python backend (`blur_humans.py`) intact. Goals: better cross-platform packaging and a modern dark UI matching the kirby-file-comparer pattern.

---

## Architecture

### High-Level

```
Electron Main Process
  ├── python-bridge.ts    Spawns FastAPI server on port 8766, polls /health
  └── index.ts            BrowserWindow, dialog IPC handlers

Electron Renderer Process (React + MUI dark)
  ├── App.tsx             Initializing state → main UI
  └── api/client.ts       axios (REST) + EventSource (SSE progress)

Python Backend (FastAPI + uvicorn, port 8766)
  ├── main.py             FastAPI app, /health endpoint
  ├── api/routes.py       /process, /stream/{job_id}, /cancel/{job_id}
  └── blur_humans.py      HumanBlurProcessor (unchanged from original)
```

### Communication Flow

1. Electron main spawns `pyxlenyx-backend` (dev: `uv run python main.py --port 8766`)
2. Main polls `GET /health` every second until 200 or 30s timeout → quits app on failure
3. Main passes backend URL to renderer via `ipcMain.handle('get-backend-url')`
4. Renderer calls `POST /api/process` to start a job → receives `{ job_id }`
5. Renderer opens `EventSource` to `GET /api/stream/{job_id}` for real-time progress
6. SSE emits `progress`, `file_start`, `complete`, and `error` event types
7. On app quit, python-bridge sends SIGTERM (Unix) or `taskkill /T /F` (Windows)

### Why SSE (not polling or WebSocket)

`HumanBlurProcessor.progress_callback` is called per-frame during video processing — jobs can run for many minutes. SSE provides real-time one-way streaming with zero extra dependencies (FastAPI's `StreamingResponse` + browser `EventSource`). WebSocket is overkill for one-way progress.

---

## Folder Structure

```
electron-pyxlenyx/
├── electron/
│   ├── main/
│   │   ├── index.ts              BrowserWindow, dialog IPC (browseFile, browseFolder, openFile)
│   │   ├── python-bridge.ts      PythonBridge class (start/stop/health-poll, port 8766)
│   │   └── tsconfig.json
│   ├── preload/
│   │   └── index.ts              contextBridge: getBackendURL, browseFile, browseFolder, openFile
│   └── renderer/
│       ├── index.html
│       └── src/
│           ├── App.tsx            Init state → main layout
│           ├── main.tsx
│           ├── global.css
│           ├── components/
│           │   ├── InputSection.tsx       Path input, Browse File/Folder, media type radio
│           │   ├── ProcessingMode.tsx     Black mask / Blur radio
│           │   ├── BlurSettings.tsx       Intensity slider, passes spinbox (disabled when black mask)
│           │   ├── AdvancedSettings.tsx   Confidence slider, model select, skin detection checkbox
│           │   ├── OutputSettings.tsx     Filename suffix, frame interval, audio checkbox
│           │   ├── ProgressSection.tsx    File progress bar, overall progress bar, status label
│           │   └── HelpDialog.tsx         Modal with GUI and CLI usage tabs
│           ├── api/
│           │   └── client.ts     axios instance + processMedia() + streamProgress()
│           └── types/
│               └── index.ts      ProcessRequest, ProgressEvent, JobStatus types
├── python-backend/
│   ├── main.py                   FastAPI app entry
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py             Pydantic: ProcessRequest, ProgressEvent, JobStatus
│   │   └── routes.py             /process, /stream/{job_id}, /cancel/{job_id}
│   ├── blur_humans.py            HumanBlurProcessor — moved from root, no changes
│   ├── pyxlenyx-backend.spec     PyInstaller spec (mac + win)
│   └── requirements.txt          fastapi, uvicorn, + existing blur_humans deps
├── build/
│   ├── icon.ico
│   └── icon.icns
├── logo.png                      (moved from root for renderer access)
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## Python Backend

### Job Lifecycle

```python
# In-memory job store (sufficient for single-user desktop app)
jobs: Dict[str, JobState] = {}

class JobState:
    status: "running" | "complete" | "error" | "cancelled"
    queue: queue.Queue        # progress events fed by progress_callback
    thread: threading.Thread  # daemon thread running HumanBlurProcessor
    cancelled: bool = False
```

- `POST /api/process` creates a `JobState`, starts a daemon thread, returns `{ job_id }`
- The thread runs `HumanBlurProcessor` with a `progress_callback` that puts events into `job.queue`
- `GET /api/stream/{job_id}` is a FastAPI `StreamingResponse` that drains the queue and yields SSE lines
- `POST /api/cancel/{job_id}` sets `job.cancelled = True`; the thread checks this flag and exits early

### SSE Event Schema

```
event: progress
data: {"current": 45, "total": 300, "file": "video.mp4", "percent": 15.0}

event: file_start
data: {"file": "photo.jpg", "index": 1, "total_files": 5}

event: complete
data: {"successful": 4, "total": 5, "output_path": "/path/to/file-background.jpg"}

event: error
data: {"message": "Processing failed: <reason>"}
```

### Routes

| Method | Path | Body / Params | Response |
|--------|------|---------------|----------|
| `GET` | `/health` | — | `{ status: "healthy" }` |
| `POST` | `/api/process` | `ProcessRequest` JSON | `{ job_id: string }` |
| `GET` | `/api/stream/{job_id}` | — | SSE stream |
| `POST` | `/api/cancel/{job_id}` | — | `{ cancelled: true }` |

### ProcessRequest (Pydantic)

```python
class ProcessRequest(BaseModel):
    input_path: str
    mask_type: str = "black"           # "black" | "blur"
    blur_intensity: int = 151
    blur_passes: int = 3
    confidence: float = 0.33
    model_name: str = "yolov8n-seg.pt"
    media_type: str = "both"           # "images" | "videos" | "both"
    keep_audio: bool = True
    filename_suffix: str = "-background"
    frame_interval: int = 1
    enable_skin_detection: bool = False
```

---

## Electron Main Process

### IPC Handlers (index.ts)

| Channel | Handler | Notes |
|---------|---------|-------|
| `get-backend-url` | returns `pythonBridge.getBaseURL()` | called once on init |
| `browse-file` | `dialog.showOpenDialog` | returns `{ filePath }` or `{ canceled }` |
| `browse-folder` | `dialog.showOpenDialog({ properties: ['openDirectory'] })` | returns `{ folderPath }` or `{ canceled }` |
| `open-file` | `shell.openPath(filePath)` | opens output file in system viewer |

### python-bridge.ts

Identical pattern to kirby:
- Dev: `uv run python main.py --port 8766` from `python-backend/` directory
- Production: bundled executable `pyxlenyx-backend` (`.exe` on Windows, no extension on macOS)
- Health poll: 30 attempts × 1s = 30s timeout
- Stop: SIGTERM on Unix, `taskkill /PID /T /F` on Windows

---

## Renderer

### App.tsx

Three states: `initializing` (CircularProgress) → `error` (Typography error) → `ready` (main UI).

### State Management

Local React state in `App.tsx` (no Zustand needed — single-page tool with one active job at a time). State shape:

```typescript
interface AppState {
  inputPath: string;
  maskType: 'black' | 'blur';
  blurIntensity: number;        // 51–301, odd only
  blurPasses: number;           // 1–10
  confidence: number;           // 0.1–1.0
  modelName: string;
  mediaType: 'images' | 'videos' | 'both';
  keepAudio: boolean;
  filenameSuffix: string;
  frameInterval: number;        // 1–15
  enableSkinDetection: boolean;
  processing: boolean;
  jobId: string | null;
  fileProgress: number;         // 0–100
  overallProgress: number;      // 0–100
  currentFileName: string;
  statusMessage: string;
  statusColor: string;
}
```

### Component Interactions

- `ProcessingMode` changing to `"black"` disables `BlurSettings` controls
- `OutputSettings.frameInterval > 1` disables and unchecks `keepAudio`
- `ProgressSection` receives progress values and status as props
- `HelpDialog` is a stateless modal — content is static text (same as Tkinter version)

### api/client.ts

```typescript
// REST
processMedia(request: ProcessRequest): Promise<{ job_id: string }>
cancelJob(jobId: string): Promise<void>

// SSE
streamProgress(
  jobId: string,
  handlers: {
    onProgress: (event: ProgressEvent) => void,
    onFileStart: (event: FileStartEvent) => void,
    onComplete: (event: CompleteEvent) => void,
    onError: (event: ErrorEvent) => void,
  }
): () => void   // returns cleanup function that closes EventSource
```

---

## Packaging

### electron-builder config (package.json)

```json
{
  "build": {
    "appId": "ngo.globalemancipation.pyxlenyx",
    "productName": "PyxelNyx",
    "mac": {
      "target": [{ "target": "dmg", "arch": ["x64", "arm64"] }],
      "icon": "build/icon.icns",
      "extraResources": [
        { "from": "python-backend/dist/pyxlenyx-backend", "to": "backend/pyxlenyx-backend" }
      ]
    },
    "win": {
      "target": [
        { "target": "nsis", "arch": ["x64"] },
        { "target": "portable", "arch": ["x64"] }
      ],
      "icon": "build/icon.ico",
      "extraResources": [
        { "from": "python-backend/dist/pyxlenyx-backend.exe", "to": "backend/pyxlenyx-backend.exe" }
      ]
    }
  }
}
```

### python-bridge.ts production paths

```typescript
const execName = process.platform === 'win32' ? 'pyxlenyx-backend.exe' : 'pyxlenyx-backend';
const pythonPath = path.join(process.resourcesPath, 'backend', execName);
```

### PyInstaller spec

Bundles `blur_humans.py` + all model/CV dependencies. `--onefile` for simple distribution.

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Backend fails to start | Main process quits app with error dialog |
| Input path doesn't exist | Backend returns 400; renderer shows error status |
| Unsupported file format | Backend returns 400 with format list |
| Processing error mid-job | SSE `error` event; renderer shows red status |
| Job cancelled by user | `POST /cancel` → thread checks flag → SSE `complete` with cancelled flag |
| YOLO model not found | Backend returns 500; renderer shows error status |

---

## Testing Considerations

- Dev workflow: `npm run dev` starts Vite + Electron; Python backend via `uv run`
- No automated tests scoped for this migration (matching existing project's test posture)
- Manual verification: single image, single video, batch folder, cancel mid-job

---

## Out of Scope

- CLI interface (unchanged, still available via `blur_humans.py` directly)
- Object detection mode (`enable_object_detection`) — not exposed in Tkinter UI, stays backend-only
- Auto-updater
