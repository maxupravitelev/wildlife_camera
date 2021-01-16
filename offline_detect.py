import cv2
import os
import time
import argparse
import numpy as np

# modules for handling file writing
from functions.create_avi import Avi_writer
from functions.create_gif import Gif_writer

# module for handling movement detection
from functions.analyzer import Analyzer

from functions.PiCam import PiCam 

# modules by pyimagesearch
import imutils
from imutils.video import VideoStream


## parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 
args = vars(parser.parse_args())
mode = args["mode"]


# init different modes
bbox_mode = False
picamera_manual = False
enable_timer = False
debug_mode = False

# set frame dimensions
# frame_width = 1296
# frame_height = 736

# frame_width = 1280
# frame_height = 720

frame_width = 1024
frame_height = 768

# frame_width = 1640
# frame_height = 1232

# frame_width = 640
# frame_height = 480

# if picamera_manual == True:
#     from picamera.array import PiRGBArray
#     from picamera import PiCamera

#     framerate = 32

#     camera = PiCamera()
#     camera.resolution = (frame_width, frame_height)
#     camera.framerate = framerate
#     # camera.awb_mode = 'off'
#     # camera.awb_gains = 1.3
#     # camera.exposure_mode = 'off'
#     cap = PiRGBArray(camera, size=(frame_width, frame_height))


# init videostream (separate thread)
#cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1).start()
#cap=cv2.VideoCapture(0)
#cap = VideoStream(src=0).start()

# cap = VideoStream(resolution="3").start()

cap = PiCam(resolution=(frame_width,frame_height)).start()

# warm um camera - without first frame returns empty
time.sleep(2.0)


# read first frame
frame = cap.read()


# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))


# set size of changed area that triggers movement detection
detection_area = 0.002
contour_threshold = int((frame_height * frame_height) * (detection_area))
print("Total area: " + str(frame_width * frame_height) + " (frame width: " + str(frame_width) + " x " + "frame height: " + str(frame_height) + ")")
print("Detection area: " + str(contour_threshold) + " (" + str(detection_area * 100) + " % of total area)")


# handle different file writing formats
if mode == "avi":
    avi_writer = Avi_writer(frame)
else: 
# if mode == "gif":
    gif_writer = Gif_writer().start()


# init analyzer for movement detection (separate thread)
analyzer = Analyzer(frame, contour_threshold, bbox_mode).start()

if enable_timer == True:
    timer2 = time.time()
    timer2 = time.time()

# loop definition for manual picamera mode
# for image in camera.capture_continuous(cap, format="bgr", use_video_port=True):

#     frame = image.array

#     cap.truncate(0)
#     cap.seek(0)


# main loop
while True:
    last_frame = frame.copy()
    # ret, frame = cap.read()
    frame = cap.read()

    # check if grabbed frame equals the previos one
    if np.array_equal(last_frame,frame):
        # print("same frame")
        analyzer.same_frame = True
        gif_writer.same_frame = True
        continue   
    
    analyzer.same_frame = False
    gif_writer.same_frame = False

    if enable_timer == True:
        timer1 = time.time()
        print("SPF: " + str(((timer1-timer2))))
        timer2 = time.time()

    # set background image on startup / after file creation was comleted
    if gif_writer.background_image is None:
        gif_writer.background_image="gray_frame"
        analyzer.set_background(frame)

    # set frame handled by analyzer
    gif_writer.frame = frame.copy()
    analyzer.frame = frame
    

    gif_writer.motion_detected = analyzer.motion_detected

    # pass current analyzer result to file creator, file creator writes frames to file if motion_detected returns true
    #gif_writer.create_gif(analyzer.motion_detected, frame)

    if debug_mode == True:
        cv2.imshow("video feed", analyzer.frame)

        # view color frame
        cv2.imshow("video feed", analyzer.frame)

        # todo: save processed frames to and fetch them from analyzer
        # # view gray_frame
        # cv2.imshow("gray_frame", gray_frame)

        # # view delta between background and gray_frame

        # cv2.imshow("delta", delta)
        
        # # view threshold of delta frame
        # cv2.imshow("threshold", threshold)

    # loop breaking condition
    key = cv2.waitKey(1) & 0xFF

    if key == ord("x"):
        break

# clean up

# todo: handle stopping all threads if one is stopped

cap.stop()
# cap.close()

if picamera_manual == True:
    camera.close()

if debug_mode == True:
    cv2.destroyAllWindows
