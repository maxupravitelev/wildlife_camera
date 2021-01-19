# import the necessary packages
from threading import Thread
import cv2

import numpy as np

class VideoStream:
    def __init__(self, src=0, name="VideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        self.last_frame = None
        
        self.same_frame = False

        self.frame_count = 0

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
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
            self.frame_count +=1



    def read(self):
        # return the frame most recently read
        # if np.array_equal(self.last_frame,self.frame):
        #     # print("same frame")
        #     self.same_frame = True
        # else:
        #     self.same_frame = False
        #     self.last_frame = self.frame
        #     self.frame_count +=1
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True