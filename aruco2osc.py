import argparse
import cv2 
import numpy as np
import time
import math

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

parser = argparse.ArgumentParser()
parser.add_argument("--input", default = 0, help = "Camera source")
parser.add_argument("--address", default = "/aruco/marker", help = "OSC address")
parser.add_argument("--ip", default = "127.0.0.1", help = "OSC IP")
parser.add_argument("--port", type=int, default = 3001, help = "OSC PORT")
args = parser.parse_args()

osc_address = args.address
client = udp_client.SimpleUDPClient(args.ip, args.port)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # dictionary of aruco markers
cap = cv2.VideoCapture(args.input) 

time.sleep(2) # wait for camera

while(True):
    ret, image = cap.read()
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    height, width, _ = image.shape

    detector = cv2.aruco.ArucoDetector(aruco_dict)

    corners, ids, rejectedImgPoints = detector.detectMarkers(greyscale)
    if ids is not None:
        for idx, identity in enumerate(ids): 
            message = OscMessageBuilder(address = osc_address)
            corner_0 = corners[idx][0][0]
            corner_2 = corners[idx][0][2]
            
            x,y = corner_2 - corner_0
            
            mid_x = ((corner_0[0] + corner_2[0])/2) / width
            mid_y = ((corner_0[1] + corner_2[1])/2) / height
            
            size = math.sqrt(((x/width) ** 2) + ((y/height) ** 2))
            angle = math.degrees(math.atan(y / x)) - 45
            
            message.add_arg(int(identity[0]))
            message.add_arg(size)
            message.add_arg(angle)
            message.add_arg(mid_x)
            message.add_arg(mid_y)
            
            msg = message.build()
            client.send(msg)
                
    # Draw markers
    cv2.aruco.drawDetectedMarkers(image, corners, ids, (0, 255, 0))

    cv2.imshow('Aruco Detection',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break