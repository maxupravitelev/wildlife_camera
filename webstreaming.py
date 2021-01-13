# import the necessary packages
from pyimagesearch.motion_detection.SingleMotionDetector import SingleMotionDetector

from functions.imgToGif import imgToGif
from functions.create_avi import Avi_writer
from functions.create_gif import Gif_writer

from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from PIL import Image, ImageDraw
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy
import os
import collections 

import numpy as np

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# parse args from command line
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True,
    help="ip address of the device")
ap.add_argument("-o", "--port", type=int, required=True,
    help="ephemeral port number of the server (1024 to 65535)")
ap.add_argument("--mode", type=str, default="gif",
    help="run in gif or avi mode")        
args = vars(ap.parse_args())

#mode = args["mode"]

# initialize the video stream and allow the camera sensor to


#frame_width = 640
#frame_height = 480

# frame_width = 1296
# frame_height = 730

# frame_width = 1920
# frame_height = 1080

frame_width = 1280
frame_height = 720

vs = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()
#vs = VideoStream(usePiCamera=1).start()

#vs = VideoStream(src=0).start()
#vs = VideoStream(src=0, resolution=(1296,730)).start()

# warmup
time.sleep(2.0)

#cap = cv2.VideoCapture(0)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def detect_motion(mode):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.5)

    # read frame to get the correct frame.shape dimensions for writer
    frame = vs.read()

    print("Frame resolution: " + str(frame.shape))

    if mode == "avi":
        avi_writer = Avi_writer(frame)


    total = 0
    frameCount = 32

    if mode == "gif":
        gif_writer = Gif_writer()


        # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        #frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        #timestamp = datetime.datetime.now()
        #cv2.putText(frame, timestamp.strftime(
        #    "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)
            # check to see if motion was found in the frame
            
            if mode=="avi":
                avi_writer.create_avi(motion, frame)
                
            if mode == "gif":
                gif_writer.create_gif(motion, frame)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
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


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")



# check to see if this is the main thread of execution
if __name__ == '__main__':
    
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["mode"],))
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)

# clean up

# if mode == "avi":
#     writer.release()
vs.stop()