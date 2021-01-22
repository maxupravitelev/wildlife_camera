import cv2
import time

from modules.cam import VideoStream
from flask import Response
from flask import Flask

from modules.PiCam import PiCam 

import argparse

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="gif",
        help="run in gif or avi mode") 

args = vars(parser.parse_args())

mode = args["mode"]

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

# frame_width = 1280
# frame_height = 720

frame_width = 1024
frame_height = 768

# picamera settings https://picamera.readthedocs.io/en/release-1.10/api_camera.html

#vs = VideoStream(usePiCamera=1,resolution=(frame_width,frame_height)).start()
#vs = VideoStream(usePiCamera=1).start()

#vs = VideoStream(src=0).start()
#vs = VideoStream(src=0, resolution=(1296,730)).start()

vs = PiCam(resolution=(frame_width,frame_height)).start()


# warmup
time.sleep(2.0)

background_image = None

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, background_image
    # loop over frames from the output stream
    while True:
        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        outputFrame = vs.read()
        if outputFrame is None:
            continue



        if mode == "bbox":

            gray_frame=cv2.cvtColor(outputFrame,cv2.COLOR_BGR2GRAY)
            gray_frame=cv2.GaussianBlur(gray_frame,(7,7),0)

            if background_image is None:
                background_image=gray_frame

            delta=cv2.absdiff(background_image,gray_frame)
            threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]

            (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours is not None:
                for contour in contours:
                    # print(cv2.contourArea(contour))
                    if cv2.contourArea(contour) >= 0:
                        
                        (x, y, w, h)=cv2.boundingRect(contour)
                        
                        cv2.rectangle(outputFrame, (x, y), (x+w, y+h), (255,255,255), 3)
                        
                        cv2.putText(outputFrame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
                # background_image = None


        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        # ensure the frame was successfully encoded
        if not flag:
                continue
        # yield the output frame in the byte format


        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

# Built upon: https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
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
cap.close()
vs.stop()