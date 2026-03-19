import { app, BrowserWindow, ipcMain, dialog, shell } from 'electron';
import path from 'path';
import { pythonBridge } from './python-bridge';

let mainWindow: BrowserWindow | null = null;

function setupIPC() {
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
}

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

  const devServerURL = process.env.VITE_DEV_SERVER_URL;
  if (devServerURL) {
    mainWindow.loadURL(devServerURL);
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => { mainWindow = null; });
}

app.whenReady().then(async () => {
  setupIPC();
  await createWindow();
});

app.on('window-all-closed', () => {
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
