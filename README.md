# wildlife_detection

## about

Create short GIF- or AVI-Files after detection movement on camera.

## Usage

Run `python adjust.py` to start the app. The default mode is set to producing gif after movement is detected.

## Hardware requirements

The app was tested with usb webcams on a laptop and camera modules on a raspberry pi 4B. It takes advantage of multithreading and produces okay-ish results (around 12 FPS) running on a raspberry pi. This can be improved by running a raspivid stream and reading it via TCP on the same device (or another). 

## note

The app is in early stages and is not yet exactly user-friendly at this point :)