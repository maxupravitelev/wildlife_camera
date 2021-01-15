import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera

from threading import Thread

class PiCam:
    def __init__(self, resolution="2"):
        self.camera = PiCamera()

        # set camera parameters
        if resolution == "1":
            self.camera.resolution = (640, 480)

        elif resolution == "2":
            self.camera.resolution = (1024, 768)

        elif resolution == "3":
            self.camera.resolution = (1640, 1232)

        elif resolution == "1w":
            self.camera.resolution = (1280, 720)

        elif resolution == "2w":
            self.camera.resolution = (1640, 922)

        elif resolution == "3w":
            self.camera.resolution = (1920, 1080)        

        self.camera.framerate = 30
        camera.awb_mode = 'off'
        camera.awb_gains = 1.3

        # camera.exposure_mode = 'off'

        # set optional camera parameters (refer to PiCamera docs)
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        # initialize the stream
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

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
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True    

# built upon: https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py