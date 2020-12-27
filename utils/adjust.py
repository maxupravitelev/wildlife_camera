# import the necessary packages
from pyimagesearch.motion_detection.SingleMotionDetector import SingleMotionDetector

from imgToGif import imgToGif

from imutils.video import VideoStream
from flask import Response
from flask import Flask
from PIL import Image, ImageDraw
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy
import os

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup

#frame_width = 640
#frame_height = 480

frame_width = 1296
frame_height = 730

#vs = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()
#vs = VideoStream(usePiCamera=1).start()

vs = VideoStream(src=0).start()
#vs = VideoStream(src=0, resolution=(1296,730)).start()

time.sleep(2.0)

#cap = cv2.VideoCapture(0)

motion_detected = False

count = 0
folderCount = 0

motionCounter = 0

writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi",
cv2.VideoWriter_fourcc(*"MJPG"), 49,(frame_width,frame_height))

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        frame = vs.read()
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            outputFrame = frame.copy()
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

# start the flask app
if __name__ == '__main__':

    app.run(host="0.0.0.0", port="8000", debug=True,
        threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()