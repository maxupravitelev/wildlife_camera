from threading import Thread
import cv2
import imutils
import json

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class Analyzer:
    def __init__(self, frame):
        
        # set setting from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        # init frame analysis
        self.gauss_blur_factor = config["analyzer_config"]["gauss_blur_factor"]
        self.resize_width = config["analyzer_config"]["resize_width"]
        self.frame = frame
        self.background_image = imutils.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), self.resize_width)

        # set detection area
        self.detection_area = 0
        self.detection_area_factor = config["analyzer_config"]["detection_area_factor"]

        # print current dimensions
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        contour_threshold = int((frame_height * frame_height) * (self.detection_area_factor))

        print("Total area: " + str(frame_width * frame_height) + " (frame width: " + str(frame_width) + " x " + "frame height: " + str(frame_height) + ")")
        print("Approx. detection area: " + str(contour_threshold) + " (" + str(self.detection_area_factor * 100) + " % of total area)")

        # init motion detection
        self.motion_detected = False

        # init thread handling
        self.stopped = False

        # set for drawing bounding box around detected area 
        self.bbox_mode = boolcheck(config["analyzer_config"]["bbox_mode"])
        
        # bbox has to be resized according to original frame size
        self.resize_factor = self.frame.shape[1] / self.resize_width

        # flag to stop analyzing while file is being written
        self.file_writing = False

        # set verbose mode
        self.verbose = boolcheck(config["general_config"]["verbose"])

        # fetch threshold values from config file
        self.threshold_black = config["analyzer_config"]["threshold_black"]
        self.threshold_white = config["analyzer_config"]["threshold_white"]

        # init preview mode as false, set true to show frames in window
        self.preview = False

        
    def start(self):    
        Thread(target=self.analyze, args=()).start()
        return self    

    def analyze(self):
        while not self.stopped:

            if self.file_writing == False:
            
                resized_frame = imutils.resize(self.frame, self.resize_width)
                if self.detection_area == 0:
                    self.detection_area = int((resized_frame.shape[0] * resized_frame.shape[1]) * (self.detection_area_factor))


                gray_frame=cv2.cvtColor(resized_frame,cv2.COLOR_BGR2GRAY)
                gray_frame=cv2.GaussianBlur(gray_frame,(self.gauss_blur_factor,self.gauss_blur_factor),0)

                delta=cv2.absdiff(self.background_image,gray_frame)
                threshold=cv2.threshold(delta, self.threshold_black, self.threshold_white, cv2.THRESH_BINARY)[1]
                threshold = cv2.erode(threshold, None, iterations=2)
                threshold = cv2.dilate(threshold, None, iterations=2)
                (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if self.preview == True:
                    cv2.imshow("video feed", self.frame)

                if contours != []: 
                    for contour in contours:
                        if cv2.contourArea(contour) > self.detection_area:
                            if self.verbose == True:
                                print("[analyzer] motion detected: " + str(cv2.contourArea(contour)))

                            self.motion_detected = True
                            
                            if self.bbox_mode == True:

                                (x, y, w, h)=cv2.boundingRect(contour)

                                x = int(x*self.resize_factor)
                                y = int(y*self.resize_factor)
                                w = int(w*self.resize_factor)
                                h = int(h*self.resize_factor)

                                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255,255,255), 3)
                                
                                cv2.putText(self.frame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

                        # time.sleep(1.0)
                        # break

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