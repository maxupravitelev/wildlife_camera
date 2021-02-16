import cv2
import os
import time
import argparse
import numpy as np
import json

from modules.file_writer import File_writer

# function to parse bool value from config file
from utils.boolcheck import boolcheck

# set setting from config file
config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

camera_mode = config["general_config"]["camera"]


## mode selection
enable_fps_timer = boolcheck(config["general_config"]["enable_fps_timer"])
debug_mode = False
approx_fps = False

## init capture
frame_width = 1024
frame_height = 768

print(enable_fps_timer)

if camera_mode == "webcam":
    from modules.cam import VideoStream
    cap = VideoStream(src=0).start()
if camera_mode == "picam":
    from modules.PiCam import PiCam
    cap = PiCam(resolution=(frame_width,frame_height)).start()

time.sleep(2.0)

# read first frame
frame = cap.read()

frame_height = frame.shape[0]
frame_width = frame.shape[1]

# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

if approx_fps == True:

    start = time.time()

    frames = 0
    time_limit = 60

    previous_frame_count = cap.frame_count
    while frames < time_limit:
        # print(cap.frame_count)
        frame_count = cap.frame_count
        if frame_count > previous_frame_count:
            previous_frame_count = frame_count
            frames += 1

    end = time.time()

    print("approx. FPS: " + str(time_limit/(end-start)))

    cap.stop()

if approx_fps == False:

    if debug_mode == False:
        File_writer = File_writer(height=frame_height, width=frame_width)
        File_writer.motion_detected = True

    if enable_fps_timer == True:
        timer2 = time.time()

    # check if frame has been actually updated
    previous_frame_count = cap.frame_count

    frame = cap.read()

    # previous_frame_count = cap.frame_count

    while True:
 
        if enable_fps_timer == True:
            timer1 = time.time()

        frame = cap.read()

        # check if frame has been actually updated
        frame_count = cap.frame_count
        if frame_count == previous_frame_count:
            #print("same")
            continue
        previous_frame_count = frame_count
        
        if debug_mode == False:
            if File_writer.writing_to_file == False:
                File_writer.handle_image_list(frame)

        if debug_mode == True:
            # view color frame
            cv2.imshow("video feed", frame)

        if enable_fps_timer == True:
            print("FPS: " + str(1/((timer1-timer2))))
            timer2 = time.time()

        # loop breaking condition
        key = cv2.waitKey(1) & 0xFF

        if key == ord("x"):
            break

# clean up
cap.stop()
