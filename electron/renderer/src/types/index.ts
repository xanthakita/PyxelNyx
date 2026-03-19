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
