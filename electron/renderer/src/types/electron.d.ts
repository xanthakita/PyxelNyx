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
