from pydantic import BaseModel


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
