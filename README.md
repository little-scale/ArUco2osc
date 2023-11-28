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

Each message contains a list of 5 values per marker. The total list length is the number of markers * 5 values. The values in each
- marker identity
- size as a normalised ratio
- angle in degrees
- x value of midpoint of marker as a normalised value
- y value of midpoint of marker as a normalised value

To change the marker type used for detection, change DICT_4X4_50 to a different value

Use examples / files: 
- aruco2osc.py : python script that takes the ArUco marker data and sends via OSC to another app
- aruco_synth.maxpat: example of using six markers to drive a rectangle wave drone synth - see here: https://www.instagram.com/p/C0LVVTMLvMj/?img_index=1
- aruco_grid_synth.maxpat : example of using 48 markers printed as a grid to drive an additive synth - see here: https://www.instagram.com/p/C0GEJtYrUWq/?img_index=1
- aruco2osc.maxpat : shows how to get data from Python to OSC to Max
- little-scale.aruco-detection-receiver.amxd : receive marker data in Ableton, allowing x, y, z and rotation to be mapped to Live parameters 
