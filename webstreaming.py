# import the necessary packages
from pyimagesearch.motion_detection.SingleMotionDetector import SingleMotionDetector

from imgToGif import imgToGif

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

#writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi",
#cv2.VideoWriter_fourcc(*"MJPG"), 30,(frame_width,frame_height))

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")



def detect_motion(mode):
    # grab global references to the video stream, output frame, and
    # lock variables
    global writer, vs, outputFrame, lock, count, folderCount, motionCounter, frame_width, frame_height
    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.5)
    total = 0
    frameCount = 32

    gifDone = True
    imageList = []
    inactivityCounter = 0

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

                if motion is not None:

                    gifDone = False
                    motionCounter = motionCounter + 1
                    print(motionCounter)
                    writer.write(frame)

                else:
                    if gifDone == False:
                        motionCounter = 0
                        count += 1
                        print("count: " + str(count))
                        writer.release()
                        gifDone = True
                        writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 60,(frame_width,frame_height))
                        #out.release()


             
            if mode == "gif":
                if motion is not None:

                    gifDone = False
                    imageList.append(frame)

                    newFolder = 'gifs/images' + str(folderCount)
                    if not os.path.isdir(newFolder):
                        os.makedirs(newFolder)
                    if count < 10:
                        localPath = newFolder + '/image1000'+str(count)+'.jpg'                
                    if count >= 10 and count < 100: 
                        localPath = newFolder + '/image100'+str(count)+'.jpg'                
                    if count >= 1000: 
                        localPath = newFolder + '/image10'+str(count)+'.jpg'  
                
                    print(count)
                    cv2.imwrite(localPath,frame)
                    count += 1
                    #time.sleep(0.1)
                    inactivityCounter = 0

                else:
                    inactivityCounter += 1
                    # print(newCounter)
                    #if count < 6:
                        #count = 0
                    if gifDone == False and count >= 3 and inactivityCounter > 500:
                        imgToGif(folderCount)
                        folderCount +=1
                        print("count: " + str(folderCount))

                        count = 0
                        gifDone = True

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
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("--mode", type=str, default="gif",
        help="# of frames used to construct the background model")        
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["mode"],))
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)
# release the video stream pointer
#writer.release()
vs.stop()