# ArUco2osc
Send ArUco marker detections as OSC messages

To use: 
- pip install opencv-contrib-python
- pip install python-osc
- python aruco2osc.py

Args are:
- --input: camera to use; default 0
- --address: OSC message address to use; default /aruco/marker
- --ip: OSC IP address to use; default 127.0.0.1
- --port: OSC port to use; default 3001

Each message contains: 
- marker identity
- size as a normalised ratio
- angle in degrees
- x value of midpoint of marker as a normalised value
- y value of midpoint of marker as a normalised value
