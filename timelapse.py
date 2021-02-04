import cv2
import time
import argparse
import threading


from modules.file_writer import File_writer

## parse args from command line
parser = argparse.ArgumentParser()

parser.add_argument("--timelapse", type=int, default=5,
        help="set timelapse interval") 

args = vars(parser.parse_args())

timelapse = args["timelapse"]
mode = "webcam"

## init capture
frame_width = 1024
frame_height = 768

if mode == "webcam":
    from modules.cam import VideoStream
    cap = VideoStream(src=0).start()
if mode == "picam":
    from modules.PiCam import PiCam
    cap = PiCam(resolution=(frame_width,frame_height)).start()

time.sleep(2.0)

# read first frame
frame = cap.read()

frame_height = frame.shape[0]
frame_width = frame.shape[1]

# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

File_writer = File_writer(height=frame_height, width=frame_width).start()


def timelapse_capture():
    frame = cap.read()
    File_writer.motion_detected = True
    File_writer.handle_image_list(frame)

timer = threading.Event()
while not timer.wait(timelapse):
    timelapse_capture()

# clean up
cap.stop()
