# PyxelNyx Electron Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the PyxelNyx Tkinter GUI to an Electron + React + MUI dark-mode front end, keeping `blur_humans.py` unchanged and wrapping it in a FastAPI backend with SSE progress streaming.

**Architecture:** Electron spawns a FastAPI/uvicorn process (`python-backend/main.py`) on port 8766, polls `/health` until ready, then exposes the backend URL to the React renderer via `contextBridge`. The renderer calls `POST /api/process` to start a job and subscribes to `GET /api/stream/{job_id}` (SSE) for real-time progress, matching the kirby-file-comparer pattern exactly.

**Tech Stack:** Electron 30, Vite 5 + vite-plugin-electron, React 18, TypeScript 5, MUI v5 (dark theme), axios, FastAPI, uvicorn, PyInstaller, electron-builder

**Reference implementation:** `/Users/jonathanwagner/repos/kirby-file-comparer` — copy patterns verbatim where noted.

---

## File Map

### New files to create
```
electron/main/index.ts
electron/main/python-bridge.ts
electron/main/tsconfig.json
electron/preload/index.ts
electron/renderer/index.html
electron/renderer/src/main.tsx
electron/renderer/src/global.css
electron/renderer/src/App.tsx
electron/renderer/src/types/index.ts
electron/renderer/src/types/electron.d.ts
electron/renderer/src/api/client.ts
electron/renderer/src/components/InputSection.tsx
electron/renderer/src/components/ProcessingMode.tsx
electron/renderer/src/components/BlurSettings.tsx
electron/renderer/src/components/AdvancedSettings.tsx
electron/renderer/src/components/OutputSettings.tsx
electron/renderer/src/components/ProgressSection.tsx
electron/renderer/src/components/HelpDialog.tsx
python-backend/main.py
python-backend/api/__init__.py
python-backend/api/models.py
python-backend/api/routes.py
python-backend/requirements.txt
python-backend/pyxlenyx-backend.spec
package.json
vite.config.ts
tsconfig.json
build/icon.ico          (placeholder — real icon added later)
build/icon.icns         (placeholder — real icon added later)
```

### Files to move
```
blur_humans.py  →  python-backend/blur_humans.py   (unchanged content)
logo.png        →  stays at root (referenced by renderer via /logo.png in dev,
                   and copied into renderer/public/ for production)
```

### Files that stay unchanged
```
blur_humans.py (content)   — moved but not edited
requirements.txt (root)    — kept for CLI use; python-backend/ gets its own
gui.py                     — kept for reference, no longer the entry point
PyxelNyx.spec              — kept for legacy builds; new spec in python-backend/
```

---

## Task 1: Project scaffolding — package.json, vite.config.ts, tsconfig

**Files:**
- Create: `package.json`
- Create: `vite.config.ts`
- Create: `tsconfig.json`
- Create: `electron/main/tsconfig.json`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "pyxlenyx",
  "version": "3.5.0",
  "description": "AI-Powered Privacy Protection for Images & Videos",
  "main": "dist/electron/main/index.js",
  "scripts": {
    "dev": "vite",
    "build": "npm run build:renderer && npm run build:main",
    "build:renderer": "vite build",
    "build:main": "tsc -p electron/main/tsconfig.json",
    "build:python": "cd python-backend && pyinstaller pyxlenyx-backend.spec",
    "build:all": "npm run build && npm run build:python && npm run package",
    "package": "electron-builder",
    "python:venv": "cd python-backend && uv venv",
    "python:install": "cd python-backend && uv pip install -r requirements.txt",
    "python:setup": "npm run python:venv && npm run python:install"
  },
  "dependencies": {
    "@emotion/react": "^11.11.4",
    "@emotion/styled": "^11.11.5",
    "@mui/icons-material": "^5.15.19",
    "@mui/material": "^5.15.19",
    "axios": "^1.6.8",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.12.12",
    "@types/react": "^18.3.2",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "electron": "^30.0.6",
    "electron-builder": "^24.13.3",
    "typescript": "^5.4.5",
    "vite": "^5.2.11",
    "vite-plugin-electron": "^0.28.6",
    "vite-plugin-electron-renderer": "^0.14.5"
  },
  "author": "Global Emancipation Network <apps@globalemancipation.ngo>",
  "license": "ISC",
  "build": {
    "appId": "ngo.globalemancipation.pyxlenyx",
    "productName": "PyxelNyx",
    "directories": {
      "output": "release",
      "buildResources": "build"
    },
    "files": [
      "dist/**/*",
      "package.json"
    ],
    "mac": {
      "target": [
        { "target": "dmg", "arch": ["x64", "arm64"] }
      ],
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
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,
      "createStartMenuShortcut": true
    }
  }
}
```

- [ ] **Step 2: Create `vite.config.ts`** — copy exactly from kirby, update paths

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import electron from 'vite-plugin-electron';
import renderer from 'vite-plugin-electron-renderer';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    electron([
      {
        entry: resolve(__dirname, 'electron/main/index.ts'),
        vite: {
          build: {
            outDir: resolve(__dirname, 'dist/electron/main'),
          },
        },
      },
      {
        entry: resolve(__dirname, 'electron/preload/index.ts'),
        onstart(options) {
          options.reload();
        },
        vite: {
          build: {
            outDir: resolve(__dirname, 'dist/electron/preload'),
          },
        },
      },
    ]),
    renderer(),
  ],
  root: resolve(__dirname, 'electron/renderer'),
  build: {
    outDir: resolve(__dirname, 'dist/electron/renderer'),
    emptyOutDir: true,
  },
  server: {
    port: 5173,
  },
});
```

- [ ] **Step 3: Create `tsconfig.json`** (renderer)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["electron/renderer/src"]
}
```

- [ ] **Step 4: Create `electron/main/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "lib": ["ES2020"],
    "outDir": "../../dist/electron/main",
    "rootDir": ".",
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true
  },
  "include": ["."]
}
```

- [ ] **Step 5: Install dependencies**

```bash
cd /Users/jonathanwagner/repos/electron-pyxlenyx
npm install
```

Expected: `node_modules/` created, no errors.

- [ ] **Step 6: Commit**

```bash
git add package.json vite.config.ts tsconfig.json electron/main/tsconfig.json
git commit -m "feat: add project scaffolding (package.json, vite, tsconfig)"
```

---

## Task 2: Move Python files and create FastAPI backend

**Files:**
- Move: `blur_humans.py` → `python-backend/blur_humans.py`
- Create: `python-backend/main.py`
- Create: `python-backend/api/__init__.py`
- Create: `python-backend/api/models.py`
- Create: `python-backend/api/routes.py`
- Create: `python-backend/requirements.txt`

- [ ] **Step 1: Move `blur_humans.py` to `python-backend/`**

```bash
mkdir -p python-backend/api
cp blur_humans.py python-backend/blur_humans.py
```

Do NOT delete the original yet — keep for reference until build is verified.

- [ ] **Step 2: Create `python-backend/requirements.txt`**

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
opencv-python>=4.9.0
numpy>=1.26.0
ultralytics>=8.2.0
Pillow>=10.3.0
pillow-heif>=0.16.0
```

- [ ] **Step 3: Set up Python venv**

```bash
cd python-backend
uv venv
uv pip install -r requirements.txt
```

Expected: `.venv/` created, packages installed without errors.

- [ ] **Step 4: Create `python-backend/api/__init__.py`**

```python
```
(empty file)

- [ ] **Step 5: Create `python-backend/api/models.py`**

```python
from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):
    input_path: str
    mask_type: str = "black"            # "black" | "blur"
    blur_intensity: int = 151
    blur_passes: int = 3
    confidence: float = 0.33
    model_name: str = "yolov8n-seg.pt"
    media_type: str = "both"            # "images" | "videos" | "both"
    keep_audio: bool = True
    filename_suffix: str = "-background"
    frame_interval: int = 1
    enable_skin_detection: bool = False


class StartJobResponse(BaseModel):
    job_id: str


class CancelResponse(BaseModel):
    cancelled: bool
```

- [ ] **Step 6: Create `python-backend/api/routes.py`**

```python
import queue
import threading
import uuid
import json
from pathlib import Path
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from api.models import ProcessRequest, StartJobResponse, CancelResponse
from blur_humans import HumanBlurProcessor

router = APIRouter()

# In-memory job store — sufficient for single-user desktop app
class JobState:
    def __init__(self):
        self.status: str = "running"   # running | complete | error | cancelled
        self.queue: queue.Queue = queue.Queue()
        self.thread: threading.Thread | None = None
        self.cancelled: bool = False

jobs: Dict[str, JobState] = {}


def _sse_line(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _run_job(job_id: str, req: ProcessRequest) -> None:
    """Runs in a daemon thread. Feeds progress events into job.queue."""
    job = jobs[job_id]
    input_path = Path(req.input_path)

    supported_image = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}
    supported_video = {'.mp4', '.mov'}

    def progress_callback(current: int, total: int) -> None:
        if job.cancelled:
            return
        percent = (current / total * 100) if total > 0 else 0
        job.queue.put(("progress", {
            "current": current,
            "total": total,
            "file": input_path.name if input_path.is_file() else "",
            "percent": round(percent, 1),
        }))

    try:
        processor = HumanBlurProcessor(
            model_name=req.model_name,
            blur_intensity=req.blur_intensity,
            blur_passes=req.blur_passes,
            mask_type=req.mask_type,
            filename_suffix=req.filename_suffix,
            keep_audio=req.keep_audio,
            frame_interval=req.frame_interval,
            enable_skin_detection=req.enable_skin_detection,
            progress_callback=progress_callback,
        )

        if input_path.is_file():
            ext = input_path.suffix.lower()
            # Synthetic progress start for images (progress_callback not called by process_image)
            if ext in supported_image:
                job.queue.put(("progress", {"current": 0, "total": 1, "file": input_path.name, "percent": 0}))

            job.queue.put(("file_start", {"file": input_path.name, "index": 1, "total_files": 1}))

            if ext in supported_image:
                success = processor.process_image(input_path, confidence=req.confidence)
            elif ext in supported_video:
                success = processor.process_video(input_path, confidence=req.confidence)
            else:
                raise ValueError(f"Unsupported format: {ext}")

            if job.cancelled:
                job.queue.put(("complete", {"successful": 0, "total": 1, "output_path": str(input_path.parent), "cancelled": True}))
                return

            if success:
                # Determine actual output path (backend computes it, not renderer)
                output_ext = '.jpg' if ext in {'.heic', '.heif'} else ext
                output_path = input_path.parent / f"{input_path.stem}{req.filename_suffix}{output_ext}"
                # Synthetic progress complete for images
                if ext in supported_image:
                    job.queue.put(("progress", {"current": 1, "total": 1, "file": input_path.name, "percent": 100}))
                job.queue.put(("complete", {
                    "successful": 1, "total": 1,
                    "output_path": str(output_path),
                    "cancelled": False,
                }))
            else:
                job.queue.put(("error", {"message": f"Processing failed for {input_path.name}"}))

        elif input_path.is_dir():
            # Determine which formats to scan
            if req.media_type == "images":
                scan_formats = supported_image
            elif req.media_type == "videos":
                scan_formats = supported_video
            else:
                scan_formats = supported_image | supported_video

            media_files = []
            for ext in scan_formats:
                media_files.extend(list(input_path.glob(f"*{ext}")) + list(input_path.glob(f"*{ext.upper()}")))

            total_files = len(media_files)
            if total_files == 0:
                job.queue.put(("error", {"message": "No supported media files found in folder"}))
                return

            successful = 0
            for idx, file_path in enumerate(media_files, 1):
                if job.cancelled:
                    break

                # Reset processor state per file
                processor.all_detections = []
                processor.skin_tone_samples = []

                job.queue.put(("file_start", {"file": file_path.name, "index": idx, "total_files": total_files}))

                ext = file_path.suffix.lower()
                # Synthetic progress start for images
                if ext in supported_image:
                    job.queue.put(("progress", {"current": 0, "total": 1, "file": file_path.name, "percent": 0}))

                try:
                    if ext in supported_image:
                        success = processor.process_image(file_path, confidence=req.confidence)
                        if success:
                            job.queue.put(("progress", {"current": 1, "total": 1, "file": file_path.name, "percent": 100}))
                    else:
                        success = processor.process_video(file_path, confidence=req.confidence)

                    if success:
                        successful += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

            job.queue.put(("complete", {
                "successful": successful,
                "total": total_files,
                "output_path": str(input_path),
                "cancelled": job.cancelled,
            }))
        else:
            job.queue.put(("error", {"message": f"Path does not exist: {req.input_path}"}))

    except Exception as e:
        import traceback
        traceback.print_exc()
        job.queue.put(("error", {"message": str(e)}))
    finally:
        job.status = "complete"


@router.post("/process", response_model=StartJobResponse)
async def start_process(req: ProcessRequest) -> StartJobResponse:
    job_id = str(uuid.uuid4())
    job = JobState()
    jobs[job_id] = job

    thread = threading.Thread(target=_run_job, args=(job_id, req), daemon=True)
    job.thread = thread
    thread.start()

    return StartJobResponse(job_id=job_id)


@router.get("/stream/{job_id}")
async def stream_progress(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    def event_generator():
        while True:
            try:
                event_type, data = job.queue.get(timeout=60)
                yield _sse_line(event_type, data)
                if event_type in ("complete", "error"):
                    # Close the SSE connection — EventSource will NOT reconnect
                    # because the renderer closes it in onComplete/onError handlers
                    break
            except queue.Empty:
                # Timeout — job may have hung; send error and close
                yield _sse_line("error", {"message": "Job timed out"})
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/cancel/{job_id}", response_model=CancelResponse)
async def cancel_job(job_id: str) -> CancelResponse:
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    jobs[job_id].cancelled = True
    return CancelResponse(cancelled=True)
```

- [ ] **Step 7: Create `python-backend/main.py`**

```python
import sys
import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="PyxelNyx Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "PyxelNyx backend is running"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()

    print(f"Starting PyxelNyx Backend on port {args.port}", flush=True)
    sys.stdout.flush()

    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="info")
```

- [ ] **Step 8: Smoke test the backend**

```bash
cd python-backend
uv run python main.py --port 8766
```

In a separate terminal:
```bash
curl http://127.0.0.1:8766/health
```
Expected: `{"status":"healthy","message":"PyxelNyx backend is running"}`

Stop the server with Ctrl+C.

- [ ] **Step 9: Commit**

```bash
git add python-backend/
git commit -m "feat: add FastAPI backend wrapping HumanBlurProcessor with SSE progress"
```

---

## Task 3: Electron main process — python-bridge and index

**Files:**
- Create: `electron/main/python-bridge.ts`
- Create: `electron/main/index.ts`

- [ ] **Step 1: Create `electron/main/python-bridge.ts`**

Copied verbatim from kirby, changing port to 8766, executable name to `pyxlenyx-backend`, and cwd to `python-backend`.

```typescript
import { spawn, ChildProcess, exec } from 'child_process';
import { app } from 'electron';
import path from 'path';
import axios from 'axios';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class PythonBridge {
  private process: ChildProcess | null = null;
  private port: number = 8766;
  private baseURL: string = '';
  private isReady: boolean = false;

  private async killProcessOnPort(port: number): Promise<void> {
    try {
      if (process.platform === 'win32') {
        const { stdout } = await execAsync(`netstat -ano | findstr :${port}`);
        if (stdout) {
          const lines = stdout.trim().split('\n');
          const pids = new Set<string>();
          for (const line of lines) {
            const match = line.trim().match(/\s+(\d+)\s*$/);
            if (match) pids.add(match[1]);
          }
          for (const pid of pids) {
            try {
              await execAsync(`taskkill /PID ${pid} /T /F`);
            } catch {}
          }
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      } else {
        const { stdout } = await execAsync(`lsof -ti:${port}`);
        if (stdout) {
          const pid = stdout.trim();
          await execAsync(`kill -9 ${pid}`);
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
    } catch (error: any) {
      if (error.code !== 1) {
        console.log(`Error checking port ${port}:`, error.message);
      }
    }
  }

  async start(): Promise<void> {
    await this.killProcessOnPort(this.port);

    const isDev = !app.isPackaged;

    const execName = process.platform === 'win32' ? 'pyxlenyx-backend.exe' : 'pyxlenyx-backend';

    const pythonPath = isDev
      ? 'uv'
      : path.join(process.resourcesPath, 'backend', execName);

    const scriptPath = isDev
      ? path.join(app.getAppPath(), 'python-backend', 'main.py')
      : '';

    const args = isDev
      ? ['run', 'python', scriptPath, '--port', String(this.port)]
      : ['--port', String(this.port)];

    console.log(`Starting Python backend: ${pythonPath} ${args.join(' ')}`);

    this.process = spawn(pythonPath, args, {
      stdio: ['ignore', 'pipe', 'pipe'],
      cwd: isDev ? path.join(app.getAppPath(), 'python-backend') : undefined,
    });

    this.process.stdout?.on('data', (data) => {
      console.log(`[Python] ${data.toString().trim()}`);
    });

    this.process.stderr?.on('data', (data) => {
      console.error(`[Python Error] ${data.toString().trim()}`);
    });

    this.process.on('error', (error) => {
      console.error(`[Python Process Error] ${error.message}`);
    });

    this.process.on('exit', (code, signal) => {
      console.log(`[Python] Process exited with code ${code} and signal ${signal}`);
      this.isReady = false;
    });

    await this.waitForReady();
    this.baseURL = `http://127.0.0.1:${this.port}`;
    this.isReady = true;
    console.log(`Python backend ready at ${this.baseURL}`);
  }

  private async waitForReady(maxAttempts: number = 30): Promise<void> {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const response = await axios.get(`http://127.0.0.1:${this.port}/health`, { timeout: 1000 });
        if (response.status === 200) {
          console.log(`Backend health check passed on attempt ${i + 1}`);
          return;
        }
      } catch {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    throw new Error('Python backend failed to start within 30 seconds');
  }

  async stop(): Promise<void> {
    if (this.process && this.process.pid) {
      try {
        if (process.platform === 'win32') {
          await execAsync(`taskkill /PID ${this.process.pid} /T /F`);
        } else {
          this.process.kill('SIGTERM');
        }
      } catch (error: any) {
        console.log(`Error stopping backend: ${error.message}`);
      }
      this.process = null;
      this.isReady = false;
    }
  }

  getBaseURL(): string { return this.baseURL; }
  getPort(): number { return this.port; }
  isBackendReady(): boolean { return this.isReady; }
}

export const pythonBridge = new PythonBridge();
```

- [ ] **Step 2: Create `electron/main/index.ts`**

```typescript
import { app, BrowserWindow, ipcMain, dialog, shell } from 'electron';
import path from 'path';
import { pythonBridge } from './python-bridge';

let mainWindow: BrowserWindow | null = null;

async function createWindow() {
  try {
    console.log('Starting Python backend...');
    await pythonBridge.start();
    console.log('Python backend started successfully');
  } catch (error) {
    console.error('Failed to start Python backend:', error);
    app.quit();
    return;
  }

  mainWindow = new BrowserWindow({
    width: 1000,
    height: 760,
    minWidth: 950,
    minHeight: 650,
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    title: 'PyxelNyx v3.5',
  });

  ipcMain.handle('get-backend-url', () => pythonBridge.getBaseURL());

  ipcMain.handle('browse-file', async () => {
    const result = await dialog.showOpenDialog(mainWindow!, {
      title: 'Select Media File',
      properties: ['openFile'],
      filters: [
        {
          name: 'All Supported',
          extensions: ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'webp', 'heic', 'heif', 'mp4', 'mov'],
        },
        { name: 'Images', extensions: ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif', 'webp', 'heic', 'heif'] },
        { name: 'Videos', extensions: ['mp4', 'mov'] },
        { name: 'All Files', extensions: ['*'] },
      ],
    });
    if (result.canceled || result.filePaths.length === 0) return { canceled: true };
    return { canceled: false, filePath: result.filePaths[0] };
  });

  ipcMain.handle('browse-folder', async () => {
    const result = await dialog.showOpenDialog(mainWindow!, {
      title: 'Select Folder',
      properties: ['openDirectory'],
    });
    if (result.canceled || result.filePaths.length === 0) return { canceled: true };
    return { canceled: false, folderPath: result.filePaths[0] };
  });

  ipcMain.handle('open-file', async (_event, filePath: string) => {
    await shell.openPath(filePath);
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => { mainWindow = null; });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', async () => {
  await pythonBridge.stop();
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) createWindow();
});

app.on('before-quit', async (event) => {
  event.preventDefault();
  await pythonBridge.stop();
  app.exit();
});
```

- [ ] **Step 3: Commit**

```bash
git add electron/main/
git commit -m "feat: add Electron main process with python-bridge (port 8766)"
```

---

## Task 4: Preload script and renderer entry

**Files:**
- Create: `electron/preload/index.ts`
- Create: `electron/renderer/index.html`
- Create: `electron/renderer/src/main.tsx`
- Create: `electron/renderer/src/global.css`
- Create: `electron/renderer/src/types/electron.d.ts`

- [ ] **Step 1: Create `electron/preload/index.ts`**

```typescript
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
  versions: {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron,
  },
  getBackendURL: () => ipcRenderer.invoke('get-backend-url'),
  browseFile: () => ipcRenderer.invoke('browse-file'),
  browseFolder: () => ipcRenderer.invoke('browse-folder'),
  openFile: (filePath: string) => ipcRenderer.invoke('open-file', filePath),
});
```

- [ ] **Step 2: Create `electron/renderer/src/types/electron.d.ts`**

```typescript
export {};

declare global {
  interface Window {
    electron: {
      versions: {
        node: () => string;
        chrome: () => string;
        electron: () => string;
      };
      getBackendURL: () => Promise<string>;
      browseFile: () => Promise<{ canceled: boolean; filePath?: string }>;
      browseFolder: () => Promise<{ canceled: boolean; folderPath?: string }>;
      openFile: (filePath: string) => Promise<void>;
    };
  }
}
```

- [ ] **Step 3: Create `electron/renderer/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PyxelNyx</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 4: Create `electron/renderer/src/main.tsx`**

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './global.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

- [ ] **Step 5: Create `electron/renderer/src/global.css`** — copy verbatim from kirby

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden;
}

#root {
  width: 100vw;
  height: 100vh;
}
```

- [ ] **Step 6: Commit**

```bash
git add electron/preload/ electron/renderer/index.html electron/renderer/src/main.tsx electron/renderer/src/global.css electron/renderer/src/types/
git commit -m "feat: add preload, renderer entry, electron type declarations"
```

---

## Task 5: Types and API client

**Files:**
- Create: `electron/renderer/src/types/index.ts`
- Create: `electron/renderer/src/api/client.ts`

- [ ] **Step 1: Create `electron/renderer/src/types/index.ts`**

```typescript
export interface ProcessRequest {
  input_path: string;
  mask_type: 'black' | 'blur';
  blur_intensity: number;
  blur_passes: number;
  confidence: number;
  model_name: string;
  media_type: 'images' | 'videos' | 'both';
  keep_audio: boolean;
  filename_suffix: string;
  frame_interval: number;
  enable_skin_detection: boolean;
}

export interface ProgressEvent {
  current: number;
  total: number;
  file: string;
  percent: number;
}

export interface FileStartEvent {
  file: string;
  index: number;
  total_files: number;
}

export interface CompleteEvent {
  successful: number;
  total: number;
  output_path: string;
  cancelled: boolean;
}

export interface ErrorEvent {
  message: string;
}

export type StatusColor = 'text.secondary' | 'primary.main' | 'success.main' | 'error.main' | 'warning.main';

export interface AppState {
  inputPath: string;
  maskType: 'black' | 'blur';
  blurIntensity: number;
  blurPasses: number;
  confidence: number;
  modelName: string;
  mediaType: 'images' | 'videos' | 'both';
  keepAudio: boolean;
  filenameSuffix: string;
  frameInterval: number;
  enableSkinDetection: boolean;
  processing: boolean;
  jobId: string | null;
  fileProgress: number;
  overallProgress: number;
  currentFileName: string;
  statusMessage: string;
  statusColor: StatusColor;
}
```

- [ ] **Step 2: Create `electron/renderer/src/api/client.ts`**

```typescript
import axios, { AxiosInstance } from 'axios';
import type { ProcessRequest, CompleteEvent, ErrorEvent, FileStartEvent, ProgressEvent } from '../types';

class APIClient {
  private client: AxiosInstance | null = null;
  private baseURL: string = '';

  async initialize(): Promise<void> {
    this.baseURL = await window.electron.getBackendURL();
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  private getClient(): AxiosInstance {
    if (!this.client) throw new Error('API client not initialized');
    return this.client;
  }

  async processMedia(request: ProcessRequest): Promise<{ job_id: string }> {
    const response = await this.getClient().post<{ job_id: string }>('/api/process', request);
    return response.data;
  }

  async cancelJob(jobId: string): Promise<void> {
    await this.getClient().post(`/api/cancel/${jobId}`);
  }

  streamProgress(
    jobId: string,
    handlers: {
      onProgress: (event: ProgressEvent) => void;
      onFileStart: (event: FileStartEvent) => void;
      onComplete: (event: CompleteEvent) => void;
      onError: (event: ErrorEvent) => void;
    }
  ): () => void {
    const url = `${this.baseURL}/api/stream/${jobId}`;
    const es = new EventSource(url);

    es.addEventListener('progress', (e) => {
      handlers.onProgress(JSON.parse(e.data));
    });

    es.addEventListener('file_start', (e) => {
      handlers.onFileStart(JSON.parse(e.data));
    });

    es.addEventListener('complete', (e) => {
      const data: CompleteEvent = JSON.parse(e.data);
      es.close();
      handlers.onComplete(data);
    });

    es.addEventListener('error', (e: MessageEvent) => {
      es.close();
      try {
        handlers.onError(JSON.parse(e.data));
      } catch {
        handlers.onError({ message: 'Connection error' });
      }
    });

    // Return cleanup function
    return () => es.close();
  }

  isInitialized(): boolean { return this.client !== null; }
  getBaseURL(): string { return this.baseURL; }
}

export const apiClient = new APIClient();
```

- [ ] **Step 3: Commit**

```bash
git add electron/renderer/src/types/index.ts electron/renderer/src/api/
git commit -m "feat: add TypeScript types and API client with SSE streaming"
```

---

## Task 6: App.tsx — initializing state and main layout shell

**Files:**
- Create: `electron/renderer/src/App.tsx`

- [ ] **Step 1: Create `electron/renderer/src/App.tsx`**

This is the full App component. It owns all state (no Zustand). Components receive props.

```typescript
import React, { useEffect, useState, useRef } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';

import { apiClient } from './api/client';
import type { AppState, ProcessRequest, StatusColor } from './types';

import InputSection from './components/InputSection';
import ProcessingMode from './components/ProcessingMode';
import BlurSettings from './components/BlurSettings';
import AdvancedSettings from './components/AdvancedSettings';
import OutputSettings from './components/OutputSettings';
import ProgressSection from './components/ProgressSection';
import HelpDialog from './components/HelpDialog';

const theme = createTheme({ palette: { mode: 'dark' } });

const DEFAULT_STATE: AppState = {
  inputPath: '',
  maskType: 'black',
  blurIntensity: 151,
  blurPasses: 3,
  confidence: 0.33,
  modelName: 'yolov8n-seg.pt',
  mediaType: 'both',
  keepAudio: true,
  filenameSuffix: '-background',
  frameInterval: 1,
  enableSkinDetection: false,
  processing: false,
  jobId: null,
  fileProgress: 0,
  overallProgress: 0,
  currentFileName: '',
  statusMessage: 'Ready to process media files',
  statusColor: 'text.secondary',
};

function App() {
  const [isInitializing, setIsInitializing] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);
  const [state, setState] = useState<AppState>(DEFAULT_STATE);
  const [helpOpen, setHelpOpen] = useState(false);
  const cleanupSseRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    apiClient
      .initialize()
      .then(() => setIsInitializing(false))
      .catch((err) => {
        setInitError(err.message || 'Failed to connect to backend');
        setIsInitializing(false);
      });
  }, []);

  const update = (partial: Partial<AppState>) =>
    setState((prev) => ({ ...prev, ...partial }));

  const setStatus = (message: string, color: StatusColor) =>
    update({ statusMessage: message, statusColor: color });

  const handleProcess = async () => {
    if (!state.inputPath.trim()) {
      setStatus('Please select a file or folder first', 'warning.main');
      return;
    }

    // Ensure odd blur intensity
    const blurIntensity = state.blurIntensity % 2 === 0 ? state.blurIntensity + 1 : state.blurIntensity;

    const request: ProcessRequest = {
      input_path: state.inputPath,
      mask_type: state.maskType,
      blur_intensity: blurIntensity,
      blur_passes: state.blurPasses,
      confidence: state.confidence,
      model_name: state.modelName,
      media_type: state.mediaType,
      keep_audio: state.keepAudio,
      filename_suffix: state.filenameSuffix,
      frame_interval: state.frameInterval,
      enable_skin_detection: state.enableSkinDetection,
    };

    update({
      processing: true,
      fileProgress: 0,
      overallProgress: 0,
      currentFileName: '',
    });
    setStatus('Starting...', 'primary.main');

    try {
      const { job_id } = await apiClient.processMedia(request);
      update({ jobId: job_id });
      setStatus('Processing...', 'primary.main');

      cleanupSseRef.current = apiClient.streamProgress(job_id, {
        onProgress: (evt) => {
          update({ fileProgress: evt.percent, currentFileName: evt.file });
        },
        onFileStart: (evt) => {
          const overall = ((evt.index - 1) / evt.total_files) * 100;
          update({
            overallProgress: overall,
            currentFileName: evt.file,
            fileProgress: 0,
          });
          setStatus(`Processing ${evt.index}/${evt.total_files}: ${evt.file}`, 'primary.main');
        },
        onComplete: (evt) => {
          cleanupSseRef.current = null;
          update({
            processing: false,
            jobId: null,
            fileProgress: 100,
            overallProgress: 100,
          });

          if (evt.cancelled) {
            setStatus('Processing cancelled', 'warning.main');
          } else {
            setStatus(`✓ Processed ${evt.successful}/${evt.total} file(s) successfully`, 'success.main');
            // For single-file jobs, offer to open the output
            if (evt.total === 1 && evt.successful === 1) {
              window.electron.openFile(evt.output_path);
            }
          }
        },
        onError: (evt) => {
          cleanupSseRef.current = null;
          update({ processing: false, jobId: null });
          setStatus(`Error: ${evt.message}`, 'error.main');
        },
      });
    } catch (err: any) {
      update({ processing: false, jobId: null });
      setStatus(`Error: ${err.message}`, 'error.main');
    }
  };

  const handleCancel = async () => {
    if (state.jobId) {
      await apiClient.cancelJob(state.jobId);
      if (cleanupSseRef.current) {
        cleanupSseRef.current();
        cleanupSseRef.current = null;
      }
      update({ processing: false, jobId: null });
      setStatus('Cancelling...', 'warning.main');
    }
  };

  if (isInitializing) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box sx={{ width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 2, backgroundColor: '#1a1a1a' }}>
          <CircularProgress />
          <Typography variant="body1" color="text.secondary">Connecting to backend...</Typography>
        </Box>
      </ThemeProvider>
    );
  }

  if (initError) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box sx={{ width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#1a1a1a' }}>
          <Typography color="error">Error: {initError}</Typography>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#1a1a1a', overflow: 'auto' }}>
        {/* Header */}
        <Box sx={{ p: 2, pb: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box>
            <Typography variant="h5" fontWeight="bold">PyxelNyx v3.5</Typography>
            <Typography variant="caption" color="text.secondary">AI-Powered Privacy Protection for Images & Videos</Typography>
          </Box>
        </Box>

        <Divider />

        {/* Main content */}
        <Box sx={{ flex: 1, p: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <InputSection
            inputPath={state.inputPath}
            mediaType={state.mediaType}
            onInputPathChange={(v) => update({ inputPath: v })}
            onMediaTypeChange={(v) => update({ mediaType: v })}
          />

          <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
            <ProcessingMode
              maskType={state.maskType}
              onChange={(v) => update({ maskType: v })}
            />
            <BlurSettings
              disabled={state.maskType !== 'blur'}
              blurIntensity={state.blurIntensity}
              blurPasses={state.blurPasses}
              onIntensityChange={(v) => update({ blurIntensity: v })}
              onPassesChange={(v) => update({ blurPasses: v })}
            />
          </Box>

          <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
            <AdvancedSettings
              confidence={state.confidence}
              modelName={state.modelName}
              enableSkinDetection={state.enableSkinDetection}
              onConfidenceChange={(v) => update({ confidence: v })}
              onModelChange={(v) => update({ modelName: v })}
              onSkinDetectionChange={(v) => update({ enableSkinDetection: v })}
            />
            <OutputSettings
              filenameSuffix={state.filenameSuffix}
              frameInterval={state.frameInterval}
              keepAudio={state.keepAudio}
              onSuffixChange={(v) => update({ filenameSuffix: v })}
              onFrameIntervalChange={(v) => {
                const next: Partial<AppState> = { frameInterval: v };
                if (v > 1) next.keepAudio = false;
                update(next);
              }}
              onKeepAudioChange={(v) => update({ keepAudio: v })}
            />
          </Box>

          {/* Action buttons */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleProcess}
              disabled={state.processing}
              sx={{ flex: 1 }}
            >
              {state.processing ? 'Processing...' : '🚀 Process Media'}
            </Button>
            {state.processing && (
              <Button variant="outlined" color="warning" size="large" onClick={handleCancel}>
                Cancel
              </Button>
            )}
            <Button variant="outlined" size="large" onClick={() => setHelpOpen(true)}>
              ❓ Help
            </Button>
          </Box>

          <ProgressSection
            fileProgress={state.fileProgress}
            overallProgress={state.overallProgress}
            currentFileName={state.currentFileName}
            statusMessage={state.statusMessage}
            statusColor={state.statusColor}
          />
        </Box>
      </Box>

      <HelpDialog open={helpOpen} onClose={() => setHelpOpen(false)} />
    </ThemeProvider>
  );
}

export default App;
```

- [ ] **Step 2: Commit**

```bash
git add electron/renderer/src/App.tsx
git commit -m "feat: add App.tsx with full state management and SSE job handling"
```

---

## Task 7: UI Components

**Files:**
- Create: `electron/renderer/src/components/InputSection.tsx`
- Create: `electron/renderer/src/components/ProcessingMode.tsx`
- Create: `electron/renderer/src/components/BlurSettings.tsx`
- Create: `electron/renderer/src/components/AdvancedSettings.tsx`
- Create: `electron/renderer/src/components/OutputSettings.tsx`
- Create: `electron/renderer/src/components/ProgressSection.tsx`

- [ ] **Step 1: Create `InputSection.tsx`**

```typescript
import React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import FormLabel from '@mui/material/FormLabel';

interface Props {
  inputPath: string;
  mediaType: 'images' | 'videos' | 'both';
  onInputPathChange: (v: string) => void;
  onMediaTypeChange: (v: 'images' | 'videos' | 'both') => void;
}

export default function InputSection({ inputPath, mediaType, onInputPathChange, onMediaTypeChange }: Props) {
  const handleBrowseFile = async () => {
    const result = await window.electron.browseFile();
    if (!result.canceled && result.filePath) onInputPathChange(result.filePath);
  };

  const handleBrowseFolder = async () => {
    const result = await window.electron.browseFolder();
    if (!result.canceled && result.folderPath) onInputPathChange(result.folderPath);
  };

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Input Selection</Typography>
      <Box sx={{ display: 'flex', gap: 1, mb: 1.5 }}>
        <TextField
          size="small"
          fullWidth
          placeholder="Select a file or folder..."
          value={inputPath}
          onChange={(e) => onInputPathChange(e.target.value)}
        />
        <Button variant="outlined" size="small" onClick={handleBrowseFile} sx={{ whiteSpace: 'nowrap' }}>
          Browse File
        </Button>
        <Button variant="outlined" size="small" onClick={handleBrowseFolder} sx={{ whiteSpace: 'nowrap' }}>
          Browse Folder
        </Button>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <FormLabel sx={{ fontSize: 13, color: 'text.secondary' }}>Folder filter:</FormLabel>
        <RadioGroup row value={mediaType} onChange={(e) => onMediaTypeChange(e.target.value as typeof mediaType)}>
          <FormControlLabel value="both" control={<Radio size="small" />} label="Both" />
          <FormControlLabel value="images" control={<Radio size="small" />} label="Images Only" />
          <FormControlLabel value="videos" control={<Radio size="small" />} label="Videos Only" />
        </RadioGroup>
      </Box>
    </Paper>
  );
}
```

- [ ] **Step 2: Create `ProcessingMode.tsx`**

```typescript
import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';

interface Props {
  maskType: 'black' | 'blur';
  onChange: (v: 'black' | 'blur') => void;
}

export default function ProcessingMode({ maskType, onChange }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Processing Mode</Typography>
      <RadioGroup value={maskType} onChange={(e) => onChange(e.target.value as 'black' | 'blur')}>
        <FormControlLabel
          value="black"
          control={<Radio size="small" />}
          label="⬛ Black Mask (Recommended for maximum privacy)"
        />
        <FormControlLabel
          value="blur"
          control={<Radio size="small" />}
          label="🌫️ Blur (Intelligent contour-following blur)"
        />
      </RadioGroup>
    </Paper>
  );
}
```

- [ ] **Step 3: Create `BlurSettings.tsx`**

Slider uses `step={2}` starting at `min={51}` to enforce odd values only.

```typescript
import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import TextField from '@mui/material/TextField';

interface Props {
  disabled: boolean;
  blurIntensity: number;
  blurPasses: number;
  onIntensityChange: (v: number) => void;
  onPassesChange: (v: number) => void;
}

export default function BlurSettings({ disabled, blurIntensity, blurPasses, onIntensityChange, onPassesChange }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2, opacity: disabled ? 0.5 : 1 }}>
      <Typography variant="subtitle2" gutterBottom>Blur Settings (Blur Mode Only)</Typography>

      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">Intensity</Typography>
          <Typography variant="caption">{blurIntensity}</Typography>
        </Box>
        <Slider
          disabled={disabled}
          value={blurIntensity}
          min={51}
          max={301}
          step={2}
          onChange={(_, v) => onIntensityChange(v as number)}
          size="small"
        />
      </Box>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="caption" color="text.secondary" sx={{ whiteSpace: 'nowrap' }}>Passes:</Typography>
        <TextField
          type="number"
          size="small"
          disabled={disabled}
          value={blurPasses}
          onChange={(e) => {
            const v = Math.max(1, Math.min(10, parseInt(e.target.value) || 1));
            onPassesChange(v);
          }}
          inputProps={{ min: 1, max: 10 }}
          sx={{ width: 80 }}
        />
        <Typography variant="caption" color="text.secondary">More passes = stronger blur</Typography>
      </Box>
    </Paper>
  );
}
```

- [ ] **Step 4: Create `AdvancedSettings.tsx`**

```typescript
import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

const MODELS = [
  'yolov8n-seg.pt',
  'yolov8s-seg.pt',
  'yolov8m-seg.pt',
  'yolov8l-seg.pt',
  'yolov8x-seg.pt',
];

interface Props {
  confidence: number;
  modelName: string;
  enableSkinDetection: boolean;
  onConfidenceChange: (v: number) => void;
  onModelChange: (v: string) => void;
  onSkinDetectionChange: (v: boolean) => void;
}

export default function AdvancedSettings({ confidence, modelName, enableSkinDetection, onConfidenceChange, onModelChange, onSkinDetectionChange }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Advanced Settings</Typography>

      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="caption" color="text.secondary">Confidence</Typography>
          <Typography variant="caption">{confidence.toFixed(2)}</Typography>
        </Box>
        <Slider
          value={confidence}
          min={0.1}
          max={1.0}
          step={0.01}
          onChange={(_, v) => onConfidenceChange(v as number)}
          size="small"
        />
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>Person Model</Typography>
        <Select
          size="small"
          fullWidth
          value={modelName}
          onChange={(e) => onModelChange(e.target.value)}
        >
          {MODELS.map((m) => (
            <MenuItem key={m} value={m}>{m}</MenuItem>
          ))}
        </Select>
      </Box>

      <FormControlLabel
        control={
          <Checkbox
            size="small"
            checked={enableSkinDetection}
            onChange={(e) => onSkinDetectionChange(e.target.checked)}
          />
        }
        label={
          <Box>
            <Typography variant="body2">Enable Skin Tone Detection</Typography>
            <Typography variant="caption" color="text.secondary">Detects skin tones near YOLO regions for better coverage</Typography>
          </Box>
        }
      />
    </Paper>
  );
}
```

- [ ] **Step 5: Create `OutputSettings.tsx`**

```typescript
import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

interface Props {
  filenameSuffix: string;
  frameInterval: number;
  keepAudio: boolean;
  onSuffixChange: (v: string) => void;
  onFrameIntervalChange: (v: number) => void;
  onKeepAudioChange: (v: boolean) => void;
}

export default function OutputSettings({ filenameSuffix, frameInterval, keepAudio, onSuffixChange, onFrameIntervalChange, onKeepAudioChange }: Props) {
  const audioDisabled = frameInterval > 1;

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Output Settings</Typography>

      <Box sx={{ mb: 2 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>Filename Suffix</Typography>
        <TextField
          size="small"
          fullWidth
          value={filenameSuffix}
          onChange={(e) => onSuffixChange(e.target.value)}
          placeholder="-background"
          helperText="e.g. -background, -blurred, -processed"
        />
      </Box>

      <Box sx={{ mb: 1.5 }}>
        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>Frame Interval (videos)</Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <TextField
            type="number"
            size="small"
            value={frameInterval}
            onChange={(e) => {
              const v = Math.max(1, Math.min(15, parseInt(e.target.value) || 1));
              onFrameIntervalChange(v);
            }}
            inputProps={{ min: 1, max: 15 }}
            sx={{ width: 80 }}
          />
          <Typography variant="caption" color="text.secondary">1 = every frame, 3 = every 3rd frame</Typography>
        </Box>
      </Box>

      <FormControlLabel
        control={
          <Checkbox
            size="small"
            checked={keepAudio}
            disabled={audioDisabled}
            onChange={(e) => onKeepAudioChange(e.target.checked)}
          />
        }
        label={
          <Box>
            <Typography variant="body2">🔊 Keep audio in output videos</Typography>
            <Typography variant="caption" color={audioDisabled ? 'warning.main' : 'text.secondary'}>
              {audioDisabled ? 'Auto-disabled with frame skipping' : 'Requires ffmpeg'}
            </Typography>
          </Box>
        }
      />
    </Paper>
  );
}
```

- [ ] **Step 6: Create `ProgressSection.tsx`**

```typescript
import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import type { StatusColor } from '../types';

interface Props {
  fileProgress: number;
  overallProgress: number;
  currentFileName: string;
  statusMessage: string;
  statusColor: StatusColor;
}

export default function ProgressSection({ fileProgress, overallProgress, currentFileName, statusMessage, statusColor }: Props) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>Processing Progress</Typography>
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 3 }}>
        <Box>
          <Typography variant="caption" color="text.secondary" fontWeight="bold">Individual File Progress</Typography>
          {currentFileName && (
            <Typography variant="caption" display="block" color="primary.main" noWrap sx={{ mb: 0.5 }}>{currentFileName}</Typography>
          )}
          <Typography variant="caption" display="block" sx={{ mb: 0.5 }}>{Math.round(fileProgress)}%</Typography>
          <LinearProgress variant="determinate" value={fileProgress} />
        </Box>
        <Box>
          <Typography variant="caption" color="text.secondary" fontWeight="bold">Overall Progress (Batch)</Typography>
          <Typography variant="caption" display="block" color="success.main" sx={{ mb: 0.5, mt: '20px' }}>{Math.round(overallProgress)}%</Typography>
          <LinearProgress variant="determinate" value={overallProgress} color="success" />
        </Box>
      </Box>
      <Typography variant="body2" color={statusColor} sx={{ mt: 1.5, textAlign: 'center' }}>
        {statusMessage}
      </Typography>
    </Paper>
  );
}
```

- [ ] **Step 7: Commit**

```bash
git add electron/renderer/src/components/InputSection.tsx \
        electron/renderer/src/components/ProcessingMode.tsx \
        electron/renderer/src/components/BlurSettings.tsx \
        electron/renderer/src/components/AdvancedSettings.tsx \
        electron/renderer/src/components/OutputSettings.tsx \
        electron/renderer/src/components/ProgressSection.tsx
git commit -m "feat: add all UI components (InputSection, ProcessingMode, BlurSettings, AdvancedSettings, OutputSettings, ProgressSection)"
```

---

## Task 8: HelpDialog component

**Files:**
- Create: `electron/renderer/src/components/HelpDialog.tsx`

- [ ] **Step 1: Create `HelpDialog.tsx`**

```typescript
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
```

- [ ] **Step 2: Commit**

```bash
git add electron/renderer/src/components/HelpDialog.tsx
git commit -m "feat: add HelpDialog with GUI and CLI usage tabs"
```

---

## Task 9: First dev run — smoke test the full app

- [ ] **Step 1: Start the dev server**

```bash
cd /Users/jonathanwagner/repos/electron-pyxlenyx
npm run dev
```

Expected: Electron window opens, shows "Connecting to backend..." then the main UI.

- [ ] **Step 2: Verify backend connectivity**

In the Electron DevTools console (Ctrl+Shift+I), confirm no errors. Check that status shows "Ready to process media files".

- [ ] **Step 3: Test Browse File**

Click "Browse File", select any `.jpg` image. Verify path appears in the text field.

- [ ] **Step 4: Test single image processing**

Select a test image, leave defaults, click "Process Media". Verify:
- Status changes to "Processing..."
- File progress bar fills to 100%
- Status shows green "✓ Processed 1/1 file(s) successfully"
- Output file appears in same folder with `-background` suffix

- [ ] **Step 5: Test Cancel**

Select a `.mp4` video (long enough to cancel), click "Process Media", then "Cancel" quickly. Verify status shows "Cancelling..." and processing stops.

- [ ] **Step 6: Test Help dialog**

Click "❓ Help", verify both tabs show content, close works.

- [ ] **Step 7: Commit if all checks pass**

```bash
git add .
git commit -m "chore: verify dev smoke test passes (single image, cancel, help)"
```

---

## Task 10: PyInstaller spec and packaging config

**Files:**
- Create: `python-backend/pyxlenyx-backend.spec`
- Create: `build/icon.ico` (copy from existing `logo.png` converted, or use placeholder)

- [ ] **Step 1: Create `python-backend/pyxlenyx-backend.spec`**

```python
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=collect_dynamic_libs('cv2') + collect_dynamic_libs('torch'),
    datas=collect_data_files('ultralytics') + collect_data_files('cv2'),
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'fastapi',
        'starlette',
        'pydantic',
        'ultralytics',
        'cv2',
        'PIL',
        'PIL.Image',
        'pillow_heif',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pyxlenyx-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

- [ ] **Step 2: Install PyInstaller in venv**

```bash
cd python-backend
uv pip install pyinstaller
```

- [ ] **Step 3: Test PyInstaller build (optional — skip if no time)**

```bash
cd python-backend
pyinstaller pyxlenyx-backend.spec
```

Expected: `dist/pyxlenyx-backend` (or `.exe` on Windows) created. Test it:
```bash
./dist/pyxlenyx-backend --port 8766 &
curl http://127.0.0.1:8766/health
kill %1
```

- [ ] **Step 4: Commit**

```bash
git add python-backend/pyxlenyx-backend.spec
git commit -m "feat: add PyInstaller spec for pyxlenyx-backend"
```

---

## Task 11: Final cleanup and deprecated file handling

- [ ] **Step 1: Update `.gitignore`**

Add to existing `.gitignore` (or create if missing):
```
# Electron build outputs
dist/
release/
node_modules/

# Python
python-backend/.venv/
python-backend/dist/
python-backend/build/
python-backend/__pycache__/
python-backend/api/__pycache__/
*.pyc
*.pyo
```

- [ ] **Step 2: Add deprecation note to `gui.py`**

Add at the very top of `gui.py` (first line after shebang):
```python
# DEPRECATED: This Tkinter GUI has been replaced by the Electron front end.
# Keep for reference only. Run `npm run dev` from the repo root instead.
```

- [ ] **Step 3: Final commit**

```bash
git add .gitignore gui.py
git commit -m "chore: update gitignore, mark gui.py as deprecated"
```
