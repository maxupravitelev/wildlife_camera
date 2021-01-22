from threading import Thread
import cv2
import os
import imutils
import time


class Analyzer:
    def __init__(self, frame, contour_threshold, bbox_mode, verbose=True):
        
        # set detection area
        self.contourAreaLimit = contour_threshold

        # init frame analysis
        self.gauss_blur_factor = 15
        self.resize_width = 300
        self.frame = frame
        self.background_image = imutils.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), self.resize_width)

        # init motion detection
        self.motion_detected = False

        # init thread handling
        self.stopped = False

        # set for drawing bounding box around detected area 
        self.bbox_mode = bbox_mode
        
        self.file_writing = False

        # set verbose mode
        self.verbose = verbose

    def start(self):    
        Thread(target=self.analyze, args=()).start()
        return self    

    def analyze(self):
        while not self.stopped:
            
            if self.file_writing == False:
            
                # cv2.imshow("gray_frame", self.frame)
                resized_frame = imutils.resize(self.frame, self.resize_width)
                
                gray_frame=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
                gray_frame=cv2.GaussianBlur(gray_frame,(self.gauss_blur_factor,self.gauss_blur_factor),0)

                delta=cv2.absdiff(self.background_image,gray_frame)
                threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
                threshold = cv2.erode(threshold, None, iterations=2)
                threshold = cv2.dilate(threshold, None, iterations=2)
                (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours != []: 
                    for contour in contours:
                        if cv2.contourArea(contour) > 300:
                            if self.verbose == True:
                                print("[analyzer] motion detected: " + str(cv2.contourArea(contour)))

                            self.motion_detected = True
                            
                            if self.bbox_mode == True:

                                (x, y, w, h)=cv2.boundingRect(contour)
                                        
                                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255,255,255), 3)
                                
                                cv2.putText(self.frame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

                            time.sleep(1.0)
                            break

                        else:
                            self.motion_detected = False
                

                else:
                    self.motion_detected = False


            if cv2.waitKey(1) == ord("x"):
                if self.verbose == True:
                    print("analyzer stopped")
                self.stopped = True

    def set_background(self, image):
        self.background_image = imutils.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.resize_width)
        self.motion_detected = False

    def stop(self):
        self.stopped = True

