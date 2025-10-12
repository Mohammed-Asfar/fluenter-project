const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');

let overlayWindow = null;

function createOverlayWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    
    overlayWindow = new BrowserWindow({
        width: 400,
        height: 200,
        x: width - 420,
        y: height - 220,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        }
    });
    
    overlayWindow.loadFile('overlay.html');
    overlayWindow.setIgnoreMouseEvents(false);
    
    // Hide initially
    overlayWindow.hide();
    
    // DevTools for debugging (comment out in production)
    // overlayWindow.webContents.openDevTools({ mode: 'detach' });
    
    overlayWindow.on('closed', () => {
        overlayWindow = null;
    });
}

app.whenReady().then(() => {
    createOverlayWindow();
    
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createOverlayWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// IPC handlers
ipcMain.on('show-suggestion', (event, data) => {
    if (overlayWindow) {
        overlayWindow.webContents.send('update-suggestion', data);
        overlayWindow.show();
    }
});

ipcMain.on('hide-overlay', () => {
    if (overlayWindow) {
        overlayWindow.hide();
    }
});

ipcMain.on('apply-correction', (event, correctedText) => {
    // Signal to watcher.py to apply the correction
    console.log('Apply correction:', correctedText);
    // This will be handled by the watcher script
});

// Keep track of cursor position for overlay positioning
ipcMain.on('update-position', (event, { x, y }) => {
    if (overlayWindow) {
        const display = screen.getDisplayNearestPoint({ x, y });
        const { width, height } = display.workArea;
        
        // Position overlay near cursor but ensure it stays on screen
        let overlayX = x + 20;
        let overlayY = y + 20;
        
        if (overlayX + 400 > width) {
            overlayX = width - 420;
        }
        if (overlayY + 200 > height) {
            overlayY = height - 220;
        }
        
        overlayWindow.setPosition(overlayX, overlayY);
    }
});
