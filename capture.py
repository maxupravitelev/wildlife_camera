import cv2
import os
import time
import argparse
import numpy as np

from functions.cam import VideoStream

# from functions.PiCam import PiCam 

from functions.file_writer import File_writer


cap = VideoStream(src=0).start()

time.sleep(2.0)

# read first frame
frame = cap.read()


# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

File_writer = File_writer(mode="gif").start()

File_writer.motion_detected = True

while True:
    frame = cap.read()

    File_writer.frame = frame.copy()

    # loop breaking condition
    key = cv2.waitKey(1) & 0xFF

    if key == ord("x"):
        break

# clean up

cap.stop()
