import cv2
from functions.imgToGif import imgToGif


from imutils.video import VideoStream
from functions.create_avi import Avi_writer
from functions.create_gif import Gif_writer

import os
import time

import argparse

import numpy as np


## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 

args = vars(parser.parse_args())

mode = args["mode"]

background_image=None

frame_width = 1296
frame_height = 730

cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()

#cap=cv2.VideoCapture(0)

# cap = VideoStream(src=0).start()
# cap = VideoStream(src=0, resolution=(1296,730)).start()


time.sleep(2.0)

frame = cap.read()

print("Frame resolution: " + str(frame.shape))

if mode == "avi":
    avi_writer = Avi_writer(frame)
else: 
# if mode == "gif":
    gif_writer = Gif_writer()

while True:
    #ret, frame = cap.read()
    last_frame = frame.copy()
    frame = cap.read()

    if np.array_equal(last_frame,frame):
        continue

    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(7,7),0)

    if gif_writer.background_image is None:
        gif_writer.background_image=gray_frame

    # print(movement_detected)

    delta=cv2.absdiff(gif_writer.background_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours == []: 
        movement_detected = False
    else:
        movement_detected = True

    # if contours == []: 
    #     movement_detected = False

    # if contours is not None:
    #     for contour in contours:
    #         # print(cv2.contourArea(contour))
    #         if cv2.contourArea(contour) >= 0:
    #             movement_detected = True
    #             # (x, y, w, h)=cv2.boundingRect(contour)
    #             # cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
    #             continue
    #         else: 
    #             movement_detected = False       
   
    # print(movement_detected)

    if mode == "avi":

        avi_writer.create_avi(movement_detected, frame)
        if contours != None:
        # if movement_detected is True:
            #print(background_image)
            background_image = None
       

    if mode == "gif":

        # handle creating gifs from frames
        gif_writer.create_gif(movement_detected, frame)

            
    if mode == "debug":

        # draw rectangle around movement area
        for contour in contours:
            if cv2.contourArea(contour) < 8000:
                continue
            (x, y, w, h)=cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)

        # view color frame
        cv2.imshow("video feed", frame)

        # view gray_frame
        cv2.imshow("gray_frame", gray_frame)

        # view delta between background and gray_frame

        cv2.imshow("delta", delta)
        
        # view threshold of delta frame
        cv2.imshow("threshold", threshold)
        


    key=cv2.waitKey(1)

    if key==ord('x'):
        break

if mode == "avi":
    writer.release()

#cap.release()
cap.stop()
cv2.destroyAllWindows
