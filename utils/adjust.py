import cv2
import time

from imutils.video import VideoStream
from flask import Response
from flask import Flask

from picamera.array import PiRGBArray
from picamera import PiCamera

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to

#frame_width = 640
#frame_height = 480

# frame_width = 1296
# frame_height = 730

frame_width = 1280
frame_height = 720

camera = PiCamera()
camera.resolution = (frame_width, frame_height)
camera.framerate = 30
camera.awb_mode = 'fluorescent'
camera.awb_gains = 4
#camera.exposure_mode = 'off'
cap = PiRGBArray(camera, size=(frame_width, frame_height))

#vs = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()
#vs = VideoStream(usePiCamera=1).start()

#vs = VideoStream(src=0).start()
#vs = VideoStream(src=0, resolution=(1296,730)).start()

# warmup
time.sleep(2.0)

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame
    # loop over frames from the output stream
    while True:
        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        outputFrame = vs.read()
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

def generate_picam():

    global outputFrame

    for image in camera.capture_continuous(cap, format="bgr", use_video_port=True):

        outputFrame = image.array
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
    return Response(generate_picam(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

# start the flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=True,
        threaded=True, use_reloader=False)

# release the video stream pointer
cap.close()
#vs.stop()