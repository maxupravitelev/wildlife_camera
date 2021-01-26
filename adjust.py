import cv2
import time

from flask import Response
from flask import Flask, request
from flask_cors import CORS

import json

import argparse

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--mode", type=str, default="picam",
        help="run in gif or avi mode") 

parser.add_argument("--bbox", type=bool, default=False,
        help="enable motion detection and draw bounding box around detected area")

args = vars(parser.parse_args())

mode = args["mode"]

bbox_mode = args["bbox"]


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None

# initialize a flask object
app = Flask(__name__)
CORS(app)


if mode == "webcam":
    from modules.cam import VideoStream
    cap = VideoStream(src=0).start()
if mode == "picam":
    from modules.PiCam import PiCam
    cap = PiCam().start()

# warmup
time.sleep(2.0)

background_image = None

# Built upon: https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
def generate():
    # grab global references to the output frame and lock variables
    
    global outputFrame, cap
    # loop over frames from the output stream
    


    while True:


        if cap.stopped == True:
            time.sleep(1.0)
            cap = PiCam().start()
            print("PiCam restarted")
            time.sleep(1.0)

        # check if the output frame is available, otherwise skip
        # the iteration of the loop
        outputFrame = cap.read()
        if outputFrame is None:
            continue

        if bbox_mode == True:

            gray_frame = cv2.cvtColor(outputFrame,cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame,(7,7),0)

            if background_image is None:
                background_image=gray_frame

            delta = cv2.absdiff(background_image,gray_frame)
            threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
            threshold = cv2.erode(threshold, None, iterations=2)
            threshold = cv2.dilate(threshold, None, iterations=2)

            (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours is not None:
                for contour in contours:
                    # print(cv2.contourArea(contour))
                    if cv2.contourArea(contour) >= 0:
                        
                        (x, y, w, h)=cv2.boundingRect(contour)
                        
                        cv2.rectangle(outputFrame, (x, y), (x+w, y+h), (255,255,255), 3)
                        
                        cv2.putText(outputFrame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        # ensure the frame was successfully encoded
        if not flag:
                continue
       
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route('/config', methods=['GET', 'POST'])
def config():

    global cap

    if request.method == 'GET':
        print("config sent")
        
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        # config.headers.add("Access-Control-Allow-Origin", "*")
        return config
    else:
        config = request.json
        with open('config/config.json', 'w') as outfile:
            json.dump(config, outfile)
        
        cap.stop()
        

        return config






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
cap.stop()