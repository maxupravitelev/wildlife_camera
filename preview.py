import cv2
import time
import imutils
import json

# module for handling movement detection
from modules.analyzer import Analyzer

# function to parse bool value from config file
from utils.boolcheck import boolcheck

config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)


camera_mode = config["general_config"]["camera"]
if camera_mode == "webcam":
    from modules.cam import VideoStream
    cap = VideoStream(src=0).start()
else: 
    from modules.PiCam import PiCam 
    cap = PiCam().start()

time.sleep(2.0)

# read first frame
frame = cap.read()

# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

# init analyzer for movement detection (separate thread)
analyzer = Analyzer(frame).start()

analyzer.preview = True

while analyzer.stopped == False:

    frame = cap.read()

    # # set frame handled by analyzer
    analyzer.frame = frame




cap.release()
cv2.destroyAllWindows()