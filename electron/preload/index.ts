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
