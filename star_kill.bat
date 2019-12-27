taskkill /T /F /IM RSI*
timeout /T 5
rmdir /S /Q "C:\Program Files\Roberts Space Industries\StarCitizen\LIVE\USER\Shaders"
start "" "C:\Program Files\Roberts Space Industries\RSI Launcher\RSI Launcher.exe"
