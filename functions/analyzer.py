from threading import Thread
import cv2
import os
import imutils

class Analyzer:
    def __init__(self, frame, contour_threshold, bbox_mode):
        self.contourAreaLimit = contour_threshold

        self.gauss_blur_factor = 25

        self.motion_detected = False

        self.frame = frame

        self.stopped = False

        self.bbox_mode = bbox_mode
        
        self.resize_width = 300

        self.background_image = imutils.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), self.resize_width)

        self.same_frame = False

    def start(self):    
        Thread(target=self.analyze, args=()).start()
        return self    

    def analyze(self):
        while not self.stopped:
            # cv2.imshow("gray_frame", self.frame)
            resized_frame = imutils.resize(self.frame, self.resize_width)
            
            gray_frame=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
            gray_frame=cv2.GaussianBlur(gray_frame,(self.gauss_blur_factor,self.gauss_blur_factor),0)

            delta=cv2.absdiff(self.background_image,gray_frame)
            threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]

            (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours != [] and self.same_frame == False: 
                
                self.motion_detected = False
                
                for contour in contours:
                    if cv2.contourArea(contour) > 50:
                        # print(cv2.contourArea(contour))
                        self.motion_detected = True
                        
                        if self.bbox_mode == True:

                            (x, y, w, h)=cv2.boundingRect(contour)
                                    
                            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255,255,255), 3)
                            
                            cv2.putText(self.frame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

                        break
                    else:
                        self.motion_detected = False
            

            if cv2.waitKey(1) == ord("x"):
                print("analyzer stopped")
                self.stopped = True

    def set_background(self, image):
        self.background_image = imutils.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), self.resize_width)

    def stop(self):
        self.stopped = True

