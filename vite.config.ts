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
