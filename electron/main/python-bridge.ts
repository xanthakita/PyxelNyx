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
        // Backend not ready yet
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
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
