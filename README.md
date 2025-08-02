1. Create a task:
   - **Trigger:** At log on
   - **Action:** `C:\Path\To\kiosk_win\start_kiosk.bat`
   - **Run with highest privileges**
2. Install Python deps:
   ```bat
   pip install fastapi uvicorn opencv-python psutil pynput
   ```
3. Launch kiosk browser (Edge example):
   ```powershell
   Start-Process "msedge.exe" -ArgumentList "--kiosk http://localhost:8000 --edge-kiosk-type=fullscreen"
   ```
