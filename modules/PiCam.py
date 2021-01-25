# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

import numpy as np
import json


class PiCam:
    def __init__(self, resolution=(640, 480)):
        # initialize the camera

        self.update_values()

        self.camera = PiCamera()     

        # initialize the stream
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

        self.frame_count = 0

    def update_values(self):
        # picamera settings https://picamera.readthedocs.io/en/release-1.10/api_camera.html

        config_path = 'modules/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

                r = 0
        resolution = config["resolution"][r]
        self.camera.resolution = (resolution[0], resolution[1])
        print(self.camera.resolution)
        self.camera.framerate = config["framerate"]
        self.camera.awb_mode = config["awb_mode"]
        self.camera.awb_gains = config["awb_gains"]
        self.camera.exposure_mode = config["exposure_mode"]

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.frame_count += 1
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True