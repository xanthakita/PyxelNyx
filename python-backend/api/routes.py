import queue
import threading
import uuid
import json
from pathlib import Path
from typing import Dict

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
                    break
            except queue.Empty:
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
