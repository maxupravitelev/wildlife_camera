# wildlife_detection

## about

Create GIF- or AVI-files after movement is detected in your video stream. 

## usage

Run `python detect.py` to start the wildlife detection mode. The default seting is set to producing gifs after movement is detected.

`python adjust.py` is meant to be run on a raspberry pi to help manualy adjusting the camera position while viewing it in the browser of a different device in the local network. 
You can also use the companion app [picam-config](https://github.com/maxupravitelev/picam-config) if you want to adjust the settings from a frontend GUI with a realtime preview. This app provides the possibility to move the camera from a frontend in case your Picam is utilizing a GPIO motor.

`python preview.py` opens a preview window where you can see the current camera frame. If you want to preview the bounding box around the detected area, set `["analyzer_config"]["bbox_mode"]` to `true` in the [config.json file](https://github.com/maxupravitelev/wildlife_detection/tree/main/config)

`python capture.py` captures the video stream immediately without detecting motion. Produces GIF by default.

`python timelapse.py` captures the video stream immediately based on a timelapse value (the default is set to 5 seconds and can be adjusted with the `--timelapse` flag). Produces GIF by default.

The exit of all scripts is rather ungraceful at the moment and requires hitting CTRL+C.

## hardware requirements

The app was tested with usb webcams on a laptop and camera modules on a raspberry pi 4B. It takes advantage of multithreading and produces okay-ish results (around 12 FPS) running on a raspberry pi. This can be improved immensely by running a raspivid stream and reading it via TCP on the same device (or another). [Start raspivid on your raspberry](https://wiki.marcluerssen.de/index.php?title=Raspberry_Pi/Camera_streaming#direct_tcp_stream_with_netcat) and change the [config.json file](https://github.com/maxupravitelev/wildlife_detection/tree/main/config) accordingly.

## current stage

The app is in an early prototype stage.