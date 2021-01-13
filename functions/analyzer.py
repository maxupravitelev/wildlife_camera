 
from threading import Thread
import cv2
import os
import imutils

class Analyzer:
    def __init__(self, frame):
        self.contourAreaLimit = 0

        self.gauss_blur_factor = 7

        self.motion_detected = False

        self.frame = frame
        self.stopped = False

        self.background_image = imutils.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), width=200)


    def start(self):    
        Thread(target=self.analyze, args=()).start()
        return self    

    def analyze(self):
        while not self.stopped:
            resized_frame = imutils.resize(self.frame, width=200)
            
            gray_frame=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
            gray_frame=cv2.GaussianBlur(gray_frame,(self.gauss_blur_factor,self.gauss_blur_factor),0)

            delta=cv2.absdiff(self.background_image,gray_frame)
            threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]

            (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours != []: 
                for contour in contours:
                    if cv2.contourArea(contour) > self.contourAreaLimit:
                        self.motion_detected = True
                        break
                    else:
                        self.motion_detected = False
        
        if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def set_background(self, image):
        self.background_image = imutils.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), width=200)

    def stop(self):
        self.stopped = True

