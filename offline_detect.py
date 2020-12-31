import cv2
from functions.imgToGif import imgToGif

from imutils.video import VideoStream

import os
import time

import argparse

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 

args = vars(parser.parse_args())

mode = args["mode"]

background_image=None
count = 0

frame_width = 1296
frame_height = 730
# frame_height = 736


cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
#cap = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()

#cap=cv2.VideoCapture(0)

# cap = VideoStream(src=0).start()
# cap = VideoStream(src=0, resolution=(1296,730)).start()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

time.sleep(2.0)

if mode == "avi":
    writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi",
    cv2.VideoWriter_fourcc(*"MJPG"), 30,(frame_width,frame_height))

gifDone = True
inactivityCounter = 0
motionCounter = 0

imageList = []

folderCount = 0

movement_detected = False

while True:
    #ret, frame = cap.read()
    frame = cap.read()

    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if background_image is None:
        print("Reference background image was resetted. Count: " + str(count))
        background_image=gray_frame
        continue

    delta=cv2.absdiff(background_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    #cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours == []: 
        movement_detected = False

    if contours is not None:
        for contour in contours:
            if cv2.contourArea(contour) > 6000:
                movement_detected = True
                #(x, y, w, h)=cv2.boundingRect(contour)
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
                continue       
   
    if mode == "avi":

        if movement_detected == True:
            gifDone = False
            motionCounter = motionCounter + 1
            # print(motionCounter)
            writer.write(frame)
            inactivityCounter = 0

        else:
            inactivityCounter += 1
            if gifDone == False and motionCounter >= 3 and inactivityCounter > 5:
                            
                motionCounter = 0
                count += 1
                print("count: " + str(count))
                writer.release()
                gifDone = True
                writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 60,(frame_width,frame_height))
                #out.release()
                background_image = None
                inactivityCounter = 0
    else: 
        
        if movement_detected == True:
            #print(count)
            gifDone = False
            imageList.append(frame)

            newFolder = 'gifs/images' + str(folderCount)
            if not os.path.isdir(newFolder):
                os.makedirs(newFolder)
            if count < 10:
                localPath = newFolder + '/image1000'+str(count)+'.jpg'                
            if count >= 10 and count < 100: 
                localPath = newFolder + '/image100'+str(count)+'.jpg'                
            if count >= 1000: 
                localPath = newFolder + '/image10'+str(count)+'.jpg'  
                
            #print(count)
            cv2.imwrite(localPath,frame)
            count += 1
            #time.sleep(0.1)
            # inactivityCounter = 0

        else:
            inactivityCounter += 1
            # print(newCounter)
            #if count < 6:
            #count = 0
            if gifDone == False and count >= 3 and inactivityCounter > 0:

            # if gifDone == False and count >= 8:
                imgToGif(folderCount)
                folderCount +=1
                print("count: " + str(folderCount))

                count = 0
                inactivitaCounter = 0
                gifDone = True
                background_image = None
                
    # for contour in contours:
    #     if cv2.contourArea(contour) < 8000:
    #         continue
    #     (x, y, w, h)=cv2.boundingRect(contour)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)

    # (x, y, w, h)=cv2.boundingRect(contour)
    # cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 2)

    #### preview capture   
    # cv2.imshow("Color Frame",frame)

#    image = cv2.rectangle(image, start_point, end_point, color, thickness) 

    # image = cv2.rectangle(frame, (0,0), (600,), (0,0,0), -1)
    # cv2.imshow('Video feed', image)

    #cv2.namedWindow('Video feed', cv2.WINDOW_FREERATIO)
    #cv2.setWindowProperty('Video feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #cv2.imshow('Video feed', cv2.flip(frame, 1))

    #cv2.imshow("gray_frame Frame",gray_frame)
    #cv2.imshow("Delta Frame",delta)
    #cv2.imshow("Threshold Frame",threshold)
    #if background_image is not None:
    #    cv2.imshow("background image",background_image)


    key=cv2.waitKey(1)

    if key==ord('x'):
        break

if mode == "avi":
    writer.release()
#cap.release()
cap.stop()
cv2.destroyAllWindows

# Built upon:
# https://github.com/arindomjit/Motion_Detected_Alarm/blob/master/motion_detector.py
