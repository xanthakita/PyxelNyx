import axios from 'axios';
import type { ProcessRequest, ProgressEvent, FileStartEvent, CompleteEvent, ErrorEvent } from '../types';

let backendURL = '';

export function setBackendURL(url: string): void {
  backendURL = url;
}

const client = axios.create();

client.interceptors.request.use((config) => {
  if (!config.baseURL) {
    config.baseURL = backendURL;
  }
  return config;
});

export async function processMedia(request: ProcessRequest): Promise<{ job_id: string }> {
  const response = await client.post<{ job_id: string }>('/api/process', request);
  return response.data;
}

export async function cancelJob(jobId: string): Promise<void> {
  await client.post(`/api/cancel/${jobId}`);
}

export function streamProgress(
  jobId: string,
  handlers: {
    onProgress: (event: ProgressEvent) => void;
    onFileStart: (event: FileStartEvent) => void;
    onComplete: (event: CompleteEvent) => void;
    onError: (event: ErrorEvent) => void;
  }
): () => void {
  const eventSource = new EventSource(`${backendURL}/api/stream/${jobId}`);

  eventSource.addEventListener('progress', (e) => {
    handlers.onProgress(JSON.parse(e.data) as ProgressEvent);
  });

  eventSource.addEventListener('file_start', (e) => {
    handlers.onFileStart(JSON.parse(e.data) as FileStartEvent);
  });

  eventSource.addEventListener('complete', (e) => {
    handlers.onComplete(JSON.parse(e.data) as CompleteEvent);
    eventSource.close();
  });

  eventSource.addEventListener('error', (e) => {
    if ((e as MessageEvent).data) {
      handlers.onError(JSON.parse((e as MessageEvent).data) as ErrorEvent);
    } else {
      handlers.onError({ message: 'Connection lost' });
    }
    eventSource.close();
  });

  return () => eventSource.close();
}
