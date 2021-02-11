# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
# import cv2

# import numpy as np
import json


class PiCam:
    def __init__(self, resolution=(640, 480)):
        # initialize the camera

        # self.update_values()

        self.frame = None

        # init thread
        self.stopped = False

        # init check to identify duplicate frames
        self.frame_count = 0

        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        self.camera = PiCamera() 

        # set resolution
        resolution = config["picam_config"]["resolution"]["set"]
        self.camera.resolution = (resolution[0], resolution[1])
        #print(self.camera.resolution)
        
        # set picamera setting
        # picamera settings https://picamera.readthedocs.io/en/release-1.10/api_camera.html
        self.camera.framerate = config["picam_config"]["framerate"]
        self.camera.awb_mode = config["picam_config"]["awb_mode"]
        self.camera.awb_gains = config["picam_config"]["awb_gains"]
        self.camera.exposure_mode = config["picam_config"]["exposure_mode"]
        self.camera.image_effect = config["picam_config"]["image_effect"]["set"]
        #print(self.camera.image_effect)
        
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        
        self.picam_fully_stopped = False

    # def update_values(self):

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array

            # set to check if frame was updated in main thread 
            if self.frame_count < 1000:
                self.frame_count += 1
            else:
                # reset counter
                self.frame_count = 0

            self.rawCapture.truncate(0)



    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True