import scrcpy
import cv2
# If you already know the device serial
# client = scrcpy.Client(device="FYP7F6VGNBFIBA6L")
# You can also pass an ADBClient instance to it
# from adbutils import adb
# adb.connect("127.0.0.1:5555")
# client = scrcpy.Client(device=adb.devices()[0])

class ScreenMonitor:
    client = None
    current_frame = None

    def __init__(self):
        self.client = scrcpy.Client(device="FYP7F6VGNBFIBA6L")
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

    def on_frame(self,frame):
        # If you set non-blocking (default) in constructor, the frame event receiver
        # may receive None to avoid blocking event.
        if frame is not None:
            # frame is an bgr numpy ndarray (cv2' default format)
            self.current_frame = frame
            # cv2.imshow("viz", frame)

    def start_monitor(self):
        self.client.start(threaded=True)

    def stop_monitor(self):
        self.client.stop()