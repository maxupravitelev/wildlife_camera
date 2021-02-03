# wildlife_detection

## about

Create GIF- or AVI-Files after movement is detected in your video stream. 

## Usage

Run `python detect.py` to start the app. The default mode is set to producing gif after movement is detected.

`python adjust.py` is meant to be run on a raspberry pi to help adjusting the camera position while viewing it in the browser of a different device in the local network. 
You can also use the companion app [picam-config](https://github.com/maxupravitelev/picam-config) if you want to adjust the settings from a frontend GUI with a realtime preview. This app provides the possibility to move the camera from a frontend in case your Picam is utilizing a GPIO motor.

`python capture.py` captures the video stream immediately without detecting motion. Produces AVI by default.

`python preview.py` opens a preview window where you can see the current camera frame. If you want to preview the bounding box around the detected area, set `["analyzer_config"]["bbox_mode"]` to `true` in the [config.json file](https://github.com/maxupravitelev/wildlife_detection/tree/main/config)


## Hardware requirements

The app was tested with usb webcams on a laptop and camera modules on a raspberry pi 4B. It takes advantage of multithreading and produces okay-ish results (around 12 FPS) running on a raspberry pi. This can be improved immensely by running a raspivid stream and reading it via TCP on the same device (or another). [Start raspivid on your raspberry](https://wiki.marcluerssen.de/index.php?title=Raspberry_Pi/Camera_streaming#direct_tcp_stream_with_netcat), change the config.json

## current stage

The app is in early stages and is not yet exactly user-friendly at this point :). GIF creation is not optimized yet, so the produced files are rather large.