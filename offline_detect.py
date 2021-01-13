import cv2
from functions.imgToGif import imgToGif

import imutils

from imutils.video import VideoStream
from functions.create_avi import Avi_writer
from functions.create_gif import Gif_writer
from functions.analyzer import Analyzer


import os
import time

import argparse

import numpy as np

# from picamera.array import PiRGBArray
# from picamera import PiCamera

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 

args = vars(parser.parse_args())

mode = args["mode"]

bbox_mode = False

background_image = None

# frame_width = 1296
# frame_height = 736

frame_width = 1280
frame_height = 720

# frame_width = 640
# frame_height = 480

# framerate = 32

# camera = PiCamera()
# camera.resolution = (frame_width, frame_height)
# camera.framerate = framerate
# # camera.awb_mode = 'off'
# # camera.awb_gains = 1.3
# # camera.exposure_mode = 'off'
# cap = PiRGBArray(camera, size=(frame_width, frame_height))



#cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()

#cap=cv2.VideoCapture(0)

cap = VideoStream(src=0).start()

frame = cap.read()

analyzer = Analyzer(frame).start()
# cap = VideoStream(src=0, resolution=(1296,730)).start()

# cap.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
# cap.set(17, 5000 ) 

time.sleep(2.0)

#ret, frame = cap.read()

# print("Frame resolution: " + str(frame.shape))

detection_area = 0.002

contour_threshold = int((frame_height * frame_height) * (detection_area))

print("Total area: " + str(frame_width * frame_height) + " (frame width: " + str(frame_width) + " x " + "frame height: " + str(frame_height) + ")")
print("Detection area: " + str(contour_threshold) + " (" + str(detection_area * 100) + " % of total area)")

if mode == "avi":
    avi_writer = Avi_writer(frame)
else: 
# if mode == "gif":
    gif_writer = Gif_writer()

def check_movement(contours):
    # detected = False
    for contour in contours:
            if cv2.contourArea(contour) > 0:
                print(cv2.contourArea(contour))

                return True
            else:
                return False

# timer2 = time.time()

# timer2 = time.time()
# capture frames from the camera
# for image in camera.capture_continuous(cap, format="bgr", use_video_port=True):

counter = 0

while True:
    last_frame = frame.copy()
    # ret, frame = cap.read()
    frame = cap.read()

    if np.array_equal(last_frame,frame):
        # print("same")
        continue   

    if gif_writer.background_image is None:
        gif_writer.background_image="gray_frame"
        analyzer.set_background(frame)


    if analyzer.motion_detected == True:
        print("detected")

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

#     # timer1 = time.time()
#     # print("SPF: " + str(((timer1-timer2))))
#     # timer2 = time.time()

#     frame = image.array

#     resized_frame = imutils.resize(frame, width=200)
    
#     cap.truncate(0)
#     cap.seek(0)
    
#     # gauss_blur_factor = 25

#     gray_frame=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
#     # gray_frame=cv2.GaussianBlur(gray_frame,(gauss_blur_factor,gauss_blur_factor),0)


#     # print(movement_detected)

#     delta=cv2.absdiff(gif_writer.background_image,gray_frame)
#     threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
#     #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
#     (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     movement_detected = False

#     if contours != []: 

#         # movement_detected = True
#         # print("contours shape: " )
#         movement_detected = check_movement(contours)

#         # for contour in contours:
#             # movement_detected = check_movement(contours)
#             # print(movement_detected)
#             # print(cv2.contourArea(contour))
#             # if cv2.contourArea(contour) >= contour_threshold:
#             #     movement_detected = check_movement(contours)

#             #     movement_detected = True
#             #     print(cv2.contourArea(contour))

#             #     if bbox_mode == True:

#             #         (x, y, w, h)=cv2.boundingRect(contour)
                            
#             #         cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
                    
#             #         cv2.putText(frame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

#             #     #gif_writer.create_gif(movement_detected, frame)

#             #     continue
#             # else:
#             #     movement_detected = False
#             #     # gif_writer.create_gif(movement_detected, frame)
#             #     # continue

#             #     # (x, y, w, h)=cv2.boundingRect(contour)
#             #     # cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
#             #     # continue

#     if mode == "gif":
#         # if movement_detected == True:
#         #     print("mov detect")

#         # handle creating gifs from frames
#         gif_writer.create_gif(movement_detected, frame)



#     key = cv2.waitKey(1) & 0xFF

#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break

# while True:
#     last_frame = frame.copy()
#     ret, frame = cap.read()
#     #frame = cap.read()

#     if np.array_equal(last_frame,frame):
#         continue

#     gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     gray_frame=cv2.GaussianBlur(gray_frame,(7,7),0)

#     if gif_writer.background_image is None:
#         gif_writer.background_image=gray_frame

#     # print(movement_detected)

#     delta=cv2.absdiff(gif_writer.background_image,gray_frame)
#     threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
#     #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
#     (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     if contours == []: 
#         movement_detected = False
#     else:
#         movement_detected = True

#     # if contours == []: 
#     #     movement_detected = False

#     # if contours is not None:
#     #     for contour in contours:
#     #         # print(cv2.contourArea(contour))
#     #         if cv2.contourArea(contour) >= 0:
#     #             movement_detected = True
#     #             # (x, y, w, h)=cv2.boundingRect(contour)
#     #             # cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
#     #             continue
#     #         else: 
#     #             movement_detected = False       
   
#     # print(movement_detected)

#     if mode == "avi":

#         avi_writer.create_avi(movement_detected, frame)
#         if contours != None:
#         # if movement_detected is True:
#             #print(background_image)
#             background_image = None
       

#     if mode == "gif":

#         # handle creating gifs from frames
#         gif_writer.create_gif(movement_detected, frame)

            
#     if mode == "debug":

#         # draw rectangle around movement area
#         for contour in contours:
#             if cv2.contourArea(contour) < 8000:
#                 continue
#             (x, y, w, h)=cv2.boundingRect(contour)
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)

#         # view color frame
#         cv2.imshow("video feed", frame)

#         # view gray_frame
#         cv2.imshow("gray_frame", gray_frame)

#         # view delta between background and gray_frame

#         cv2.imshow("delta", delta)
        
#         # view threshold of delta frame
#         cv2.imshow("threshold", threshold)
        


#     key=cv2.waitKey(1)

#     if key==ord('x'):
#         break

if mode == "avi":
    writer.release()

#cap.release()
#cap.stop()
# cap.close()
camera.close()
cv2.destroyAllWindows
