import cv2
import os
import time
import argparse
import numpy as np

# module for handling movement detection
from modules.analyzer import Analyzer

# module for handling writing to files
from modules.file_writer import File_writer


## parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode")
parser.add_argument("--verbose", type=bool, default=True,
        help="activate status updates") 
args = vars(parser.parse_args())
mode = args["mode"]
verbose = args["verbose"]

print("[init] startup settings | mode " + str(mode) + " verbose | " + str(verbose))

# init different modes
bbox_mode = False
picamera_mode = False
enable_timer = False
debug_mode = False

# set frame dimensions
# frame_width = 1296
# frame_height = 736

# frame_width = 1280
# frame_height = 720

# frame_width = 1024
# frame_height = 768

# frame_width = 1640
# frame_height = 1232

frame_width = 640
frame_height = 480

# init videostream (separate thread)

if picamera_mode == False:
    from modules.cam import VideoStream
    #cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
    cap = VideoStream(src=0).start()

else: 
    from modules.PiCam import PiCam 

    cap = PiCam(resolution=(frame_width,frame_height)).start()


# warm um camera - without first frame returns empty
time.sleep(2.0)


# read first frame
frame = cap.read()


# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

frame_height = frame.shape[0]
frame_width = frame.shape[1]

# set size of changed area that triggers movement detection
detection_area = 0.002
contour_threshold = int((frame_height * frame_height) * (detection_area))
print("Total area: " + str(frame_width * frame_height) + " (frame width: " + str(frame_width) + " x " + "frame height: " + str(frame_height) + ")")
print("Detection area: " + str(contour_threshold) + " (" + str(detection_area * 100) + " % of total area)")


# init writing files (separate thread)
File_writer = File_writer(mode=mode, verbose=verbose).start()
# todo: CHECK IF WRITING FOLDER EXIST!


# init analyzer for movement detection (separate thread)
analyzer = Analyzer(frame, contour_threshold, bbox_mode, verbose=verbose).start()

if enable_timer == True:
    timer2 = time.time()
    timer2 = time.time()

# check if frame has been actually updated
previous_frame_count = cap.frame_count

# main loop
while True:

    # set start timer
    if enable_timer == True:
        timer1 = time.time()

    # check if frame has been actually updated
    frame_count = cap.frame_count
    if frame_count == previous_frame_count:
        # print("same")
        continue
    previous_frame_count = frame_count

    # if frame is updated, read frame
    frame = cap.read()

    # print out output FPS based on duration of every loop with updated frames
    if enable_timer == True:
        print("FPS: " + str(1/((timer1-timer2))))
        timer2 = time.time()

    # set background image on startup / after file creation was completed
    if File_writer.background_image_set == False:
        analyzer.set_background(frame)
        File_writer.background_image_set = True


    # set frame handled by analyzer
    File_writer.frame = frame
    analyzer.frame = frame
    
    # sync threads
    File_writer.motion_detected = analyzer.motion_detected
    analyzer.file_writing = File_writer.writing

    if File_writer.writing == False:

        if analyzer.motion_detected == True or File_writer.file_done == False:
            # print("[main] write | motion detected: " + str(analyzer.motion_detected) + " file done: " + str(File_writer.file_done) )
            # pass current analyzer result to file creator, file creator writes frames to file if motion_detected returns true
            File_writer.handle_image_list(frame)
   

    #File_writer.handle_image_list(analyzer.motion_detected, frame)

    if debug_mode == True:

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
