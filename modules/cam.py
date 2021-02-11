# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

from threading import Thread
import cv2

import json
import time

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class VideoStream:
    def __init__(self, src=0, name="VideoStream"):

        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        if boolcheck(config["general_config"]["stream_via_url"]) == True:
            src = config["general_config"]["stream_url"]

        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        # self.stream = cv2.VideoCapture("tcp://192.168.178.51:5000")  
        # time.sleep(1.0)
        #self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        self.frame_count = 0
        

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:

            if not self.stopped:
            
                # read next frame from  stream
                (self.grabbed, self.frame) = self.stream.read()

                # set to check if frame was updated in main thread
                if self.frame_count < 1000:
                    self.frame_count += 1
                else:
                    # reset counter
                    self.frame_count = 0

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True