import scrcpy
import cv2

# If you already know the device serial
client = scrcpy.Client(device="FYP7F6VGNBFIBA6L")
# You can also pass an ADBClient instance to it
# from adbutils import adb
# adb.connect("127.0.0.1:5555")
# client = scrcpy.Client(device=adb.devices()[0])

def on_frame(frame):
    # If you set non-blocking (default) in constructor, the frame event receiver
    # may receive None to avoid blocking event.
    print(111)
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        cv2.imshow("viz", frame)
    cv2.waitKey(10)

client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.start()
