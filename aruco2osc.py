import argparse
import cv2
import numpy as np
import time
import math

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=int, default=0, help="Camera source")
parser.add_argument("--address", default="/aruco/marker", help="OSC address")
parser.add_argument("--ip", default="127.0.0.1", help="OSC IP")
parser.add_argument("--port", type=int, default=3000, help="OSC PORT")
parser.add_argument("--overlay-only", action="store_true",
                    help="Hide camera feed; show overlay only (black background)")
args = parser.parse_args()

osc_address = args.address
client = udp_client.SimpleUDPClient(args.ip, args.port)

# ArUco setup
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict)

cap = cv2.VideoCapture(args.input)
time.sleep(2)  # wait for camera

while True:
    ret, image = cap.read()
    if not ret:
        break

    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = greyscale.shape[:2]

    corners, ids, _ = detector.detectMarkers(greyscale)

    # Send OSC if markers found
    if ids is not None:
        message = OscMessageBuilder(address=osc_address)
        for idx, identity in enumerate(ids):
            corner_0 = corners[idx][0][0]
            corner_2 = corners[idx][0][2]

            x, y = corner_2 - corner_0
            mid_x = float(((corner_0[0] + corner_2[0]) / 2) / width)
            mid_y = float(((corner_0[1] + corner_2[1]) / 2) / height)
            size = math.sqrt(((x / width) ** 2) + ((y / height) ** 2))
            angle = math.degrees(math.atan2(y, x))
            angle = (angle + 360.0 - 45) % 360.0

            message.add_arg(int(identity[0]))
            message.add_arg(size)
            message.add_arg(angle)
            message.add_arg(mid_x)
            message.add_arg(mid_y)

        client.send(message.build())

    # ===== Display frame selection =====
    # If overlay-only, draw on a black canvas; otherwise, draw on the camera frame.
    display = np.zeros_like(image) if args.overlay_only else image.copy()

    # Draw overlay (only if we have detections)
    if ids is not None and len(ids) > 0:
        cv2.aruco.drawDetectedMarkers(display, corners, ids, (0, 255, 0))

    cv2.imshow('Aruco Detection', display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
