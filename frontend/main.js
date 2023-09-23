const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            devTools: true,  // Ensure this is set to true
            preload: path.join(app.getAppPath(), 'preload.js'),
            nodeIntegration: true
        }
    });
    win.loadFile('index.html');
}

app.on('ready', createWindow);
