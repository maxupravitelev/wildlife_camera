# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

from threading import Thread
import cv2

import numpy as np

class VideoStream:
    def __init__(self, src=0, name="VideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        # self.stream = cv2.VideoCapture("tcp://192.168.178.50:5000")  

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
            # if the thread indicator variable is set, stop the thread

            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            
            # set to check if frame was updated in main thread
            self.frame_count +=1

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True