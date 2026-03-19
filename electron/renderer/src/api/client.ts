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

    return () => es.close();
  }

  isInitialized(): boolean { return this.client !== null; }
  getBaseURL(): string { return this.baseURL; }
}

export const apiClient = new APIClient();
