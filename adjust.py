import cv2
import time

from flask import Response
from flask import Flask, request
from flask_cors import CORS

import json

# function to parse bool values from config file
from utils.boolcheck import boolcheck


# init settings
config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

camera_mode = config["general_config"]["camera"]
bbox_mode = boolcheck(config["adjust_config"]["bbox_mode"])
gpio_motor = boolcheck(config["adjust_config"]["gpio_motor"])
preview_mode = config["adjust_config"]["preview_mode"]["set"]

if gpio_motor == True:
    from modules.gpio_motor import GPIO_motor
    motor = GPIO_motor()

# init flask
app = Flask(__name__)
CORS(app)

# init cam
if camera_mode == "webcam":
    from modules.cam import VideoStream
    cap = VideoStream(src=0).start()
if camera_mode == "picam":
    from modules.PiCam import PiCam
    cap = PiCam().start()


# warmup cam
time.sleep(2.0)

frame = cap.read()

# init background image for bbox mode
background_image = None

# Built upon: https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
def generate():
    
    global frame, cap, background_image, config_path, preview_mode
    
    with open(config_path) as config_file:
        config = json.load(config_file)

    while True:
        if cap.stopped == True:
            # re-read config file after post config request
            with open(config_path) as config_file:
                config = json.load(config_file)

            # fetch preview mode
            preview_mode = config["adjust_config"]["preview_mode"]["set"]

            # start camera based on mode
            time.sleep(1.0)
            if camera_mode == "webcam":
                cap.start()                
                print("Webcam restarted")

            if camera_mode == "picam":
                cap = PiCam().start()
                print("PiCam restarted")
            time.sleep(0.5)
        
        frame = cap.read()

        if bbox_mode == True:

            gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
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
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 3)
                        cv2.putText(frame, str(cv2.contourArea(contour)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

        if preview_mode == "standard":
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if preview_mode == "threshold":

            # fetch threshold values from config file
            threshold_black = config["analyzer_config"]["threshold_black"]
            threshold_white = config["analyzer_config"]["threshold_white"]
            gauss_blur_factor = config["analyzer_config"]["gauss_blur_factor"]

            gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame,(gauss_blur_factor,gauss_blur_factor),0)

            threshold = cv2.threshold(gray_frame, threshold_black, threshold_white, cv2.THRESH_BINARY)[1]

            (flag, encodedImage) = cv2.imencode(".jpg", threshold)

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

        return config
    else:
        print("config received")
        config = request.json
        with open('config/config.json', 'w') as outfile:
            json.dump(config, outfile)
        
        cap.stop()
        
        return config

@app.route('/move', methods=['POST'])
def move_camera():

    move_json = request.json
    direction = move_json["direction"]
    steps = move_json["steps"]

    motor.start(steps, direction)

    return move_json

    

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