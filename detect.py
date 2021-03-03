import cv2
import time
import json

# module for handling movement detection
from modules.analyzer import Analyzer

# module for handling writing to files
from modules.file_writer import File_writer

# function to parse bool value from config file
from utils.boolcheck import boolcheck



# set setting from config file
config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

print("[init] get startup settings from config.json file")


# init different modes
camera_mode = config["general_config"]["camera"]
enable_timer = boolcheck(config["general_config"]["enable_fps_timer"])
buffer_mode = boolcheck(config["general_config"]["create_buffer"])

verbose = boolcheck(config["general_config"]["verbose"])


# init videostream (separate thread)
if camera_mode == "webcam":
    from modules.cam import VideoStream
    #cap = VideoStream(src=0, resolution=(frame_width,frame_height)).start()
    cap = VideoStream(src=0).start()
else: 
    from modules.PiCam import PiCam 
    cap = PiCam().start()


# warm um camera - without first frame returns empty
time.sleep(2.0)


# read first frame
frame = cap.read()


# get frame size from first frame making
print("Frame resolution: " + str(frame.shape))

# get current dimensions
frame_height = frame.shape[0]
frame_width = frame.shape[1]

# init writing files (separate thread)
File_writer = File_writer(height=frame_height, width=frame_width)

# init analyzer for movement detection (separate thread)
analyzer = Analyzer(frame).start()


# init timing FPS
if enable_timer == True:
    timer2 = time.time()
    timer2 = time.time()

# check if frame has been actually updated
previous_frame_count = cap.frame_count

fps_limit = 1/30
max_fps_in_ms = int((fps_limit)*1000) 

# main loop
while True:

    # set start timer
    if enable_timer == True:
        timer1 = time.time()

    # check if frame has been actually updated
    frame_count = cap.frame_count
    if frame_count == previous_frame_count:
        # print("same")
        continue
    previous_frame_count = frame_count

    # if frame is updated, read frame
    frame = cap.read()

    # print out output FPS based on duration of every loop with updated frames
    if enable_timer == True:
        print("FPS: " + str(1/((timer1-timer2))))
        timer2 = time.time()

    # set background image on startup / after file creation was completed
    if File_writer.background_image_set == False:
        analyzer.set_background(frame)
        File_writer.background_image_set = True


    # set frame handled by analyzer
    analyzer.frame = frame
    
    # sync threads
    analyzer.file_writing = File_writer.writing_to_file

    if File_writer.writing_to_file == False:

        if buffer_mode == True and File_writer.writing_to_image_list == False:
            File_writer.write_buffer(frame)
        
        if analyzer.motion_detected == True or File_writer.writing_to_image_list == True:
            # pass current analyzer result to file creator, file creator writes frames to file if motion_detected returns true
            File_writer.motion_detected = analyzer.motion_detected
            File_writer.handle_image_list(frame)

    # loop breaking condition
    key = cv2.waitKey(max_fps_in_ms) & 0xFF

    if key == ord("x"):
        break

# clean up

# todo: handle stopping all threads if one is stopped

cap.stop()
# cap.close()
