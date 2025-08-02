from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from threading import Thread
import cv2, time, os, psutil
import input_blocker

app = FastAPI()
# Serve all files from current directory
app.mount('/', StaticFiles(directory='.', html=True), name='static')

RTSP_URL = 'rtsp://your_4k_stream_url'
CAPTURE_PATH = 'last.jpg'
USB_PATHS = ['E:/', 'F:/', 'G:/', 'H:/']  # adjust drive letters
last_timestamp = '--'

def capture_loop():
    global last_timestamp
    while True:
        now = time.localtime()
        # Snap on even minute at second zero between 06:00 and 22:00
        if now.tm_min % 2 == 0 and now.tm_sec == 0 and 6 <= now.tm_hour < 22:
            cap = cv2.VideoCapture(RTSP_URL)
            ret, frame = cap.read()
            cap.release()
            if ret:
                img = cv2.resize(frame, (1920, 1080))
                ts = time.strftime('%Y-%m-%d_%H-%M-%S')
                last_timestamp = ts
                cv2.imwrite(CAPTURE_PATH, img)
                for drive in USB_PATHS:
                    try:
                        cv2.imwrite(os.path.join(drive, f"{ts}.jpg"), img)
                    except:
                        pass
            # avoid double-capture
            time.sleep(1)
        else:
            time.sleep(1)

Thread(target=capture_loop, daemon=True).start()

@app.get('/status')
def status():
    usages = []
    for d in USB_PATHS:
        try:
            u = psutil.disk_usage(d)
            usages.append(int(u.used / u.total * 100))
        except:
            usages.append(0)
    return JSONResponse({'timestamp': last_timestamp, 'image_url': '/last.jpg', 'usb': usages})

@app.get('/capture')
def manual_capture():
    return {'status': 'ok'}

@app.get('/shutdown')
def shutdown():
    input_blocker.keyboard_listener.stop()
    input_blocker.mouse_listener.stop()
    os._exit(0)
