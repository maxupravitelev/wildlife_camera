import cv2
import os
import time
import argparse
import numpy as np

from functions.cam import VideoStream

# from functions.PiCam import PiCam 

from functions.file_writer import File_writer

## mode selection
debug_mode = False
enable_timer = True

cap = VideoStream(src=0).start()

time.sleep(2.0)

# read first frame
frame = cap.read()


# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))



start = time.time()

frames = 0
time_limit = 60

while time_limit < time_limit:
    frame = cap.read()
    if cap.same_frame == False:
        frames += 1

end = time.time()

print("FPS: " + str(time_limit/(end-start)))


if debug_mode == False:
    File_writer = File_writer(mode="gif").start()
    File_writer.motion_detected = True

if enable_timer == True:
    timer2 = time.time()
    timer2 = time.time()

frame = cap.read()

while True:
    last_frame = frame.copy()
    frame = cap.read()


    if debug_mode == False:
        File_writer.frame = frame.copy()

    
    if debug_mode == True:
        # view color frame
        cv2.imshow("video feed", frame)

    if enable_timer == True:

        timer1 = time.time()
    
        if (cap.same_frame == False):
            
            print("FPS: " + str(1/((timer1-timer2))))
            timer2 = time.time()

    # loop breaking condition
    key = cv2.waitKey(1) & 0xFF

    if key == ord("x"):
        break

# clean up
cap.stop()
