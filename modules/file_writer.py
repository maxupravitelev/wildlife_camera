import cv2
import os
from utils.imgToGif import imgToGif
import threading
import json
import numpy as np

# function to parse bool value from config file
from utils.boolcheck import boolcheck

class File_writer:
    def __init__(self, height=480, width=680):

        # set setting from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        # init file creation handling
        self.writing_to_image_list = False
        self.fileCount = 0
        self.writing_to_file = False

        # init thread handling flag
        self.stopped = False

        # init image_list handling 

        self.image_list = []     
        self.image_counter = 0
        self.image_limit = config["file_writer_config"]["image_limit"]
        
        # init flag to handle reference background resetting after file is created
        self.background_image_set = False
        
        # init writing to image_list flag 
        self.motion_detected = False

        # init inactivity handling; needed if frames are skipped or contours are not found in inbetween frames
        self.inactivityCounter = 0
        self.inactivity_limit = config["file_writer_config"]["inactivity_limit"]

        # handle modes
        self.mode = config["file_writer_config"]["mode"]
        self.create_jpg_only = boolcheck(config["file_writer_config"]["create_jpg_only"])

        if self.mode == "avi":
            self.fps = config["file_writer_config"]["fps_in_avi_mode"]
            self.frame_width = width
            self.frame_height = height
            self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

        self.verbose = boolcheck(config["general_config"]["verbose"])

        # init buffer_mode
        self.buffer_mode = boolcheck(config["general_config"]["create_buffer"])
        self.create_buffer = True
        self.buffer_length = config["file_writer_config"]["buffer_length"]
        self.lock = threading.Lock()


    def start(self):    
        # lock = threading.Lock()
        # Thread(target=self.write_to_file, args=(lock,)).start()
        t = threading.Thread(target=self.write_to_file, args=())
        t.daemon = True
        t.start()        
        return self 


    def write_buffer(self, frame):
        # if self.create_buffer == True and self.motion_detected == False:
            if len(self.image_list) < self.buffer_length:
                self.image_list.append(frame)
            else:
                self.image_list.pop(0)
                self.image_list.append(frame)

    def handle_image_list(self, frame):

        if self.image_counter < self.image_limit and self.motion_detected == True:
            
            self.create_buffer = False

            if self.verbose == True:
                print("[filewriter] Image count: " + str(len(self.image_list)))

            self.inactivityCounter = 0
            self.writing_to_image_list = True
            self.image_list.append(frame)
            self.image_counter += 1
        
        if self.motion_detected == False and self.writing_to_image_list == True and self.inactivityCounter <= self.inactivity_limit:

            self.inactivityCounter += 1

            self.image_list.append(frame)
            self.image_counter += 1
            if self.verbose == True:
                print("[filewriter] append image while inactive | count: " + str(self.inactivityCounter))

        if self.inactivityCounter > self.inactivity_limit or self.image_counter >= self.image_limit:
            self.writing_to_file = True
            self.start()


    def write_to_file(self):

        with self.lock:
            if self.verbose == True:
                print("[filewriter] wrting to file...")

                print(self.check_for_duplicates())

                if self.check_for_duplicates() == "image list is empty":
                    return

                print("[filewriter] total images: " + str(len(self.image_list)))                    

            if self.mode == "gif":

                # create folder for images
                newFolder = 'gifs/images' + str(self.fileCount)
                if not os.path.isdir(newFolder):
                    os.makedirs(newFolder)

                # write individual images
                for num, image in enumerate(self.image_list, start=0):
                    if num < 10:
                        localPath = newFolder + '/image1000'+str(num)+'.jpg'                
                    if num >= 10 and num < 100: 
                        localPath = newFolder + '/image100'+str(num)+'.jpg'                
                    if num >= 100: 
                        localPath = newFolder + '/image10'+str(num)+'.jpg'
                    cv2.imwrite(localPath,image)  

                # convert folder to gif
                if self.create_jpg_only == False:
                    imgToGif(self.fileCount, self.image_list)
                    print("[filewriter] GIFs created: " + str(self.fileCount))

                self.fileCount +=1

                # reset values to handle next gif
                self.reset_values()
            
            elif self.mode == "avi":
                
                # create folder for images
                newFolder = 'avi'
                if not os.path.isdir(newFolder):
                    os.makedirs(newFolder)

                for frame in self.image_list:

                    self.writer.write(frame)
                    
                self.fileCount += 1
                print("[filewriter] AVIs created: " + str(self.fileCount))

                self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

                # reset values to handle next avi
                self.reset_values()

    def reset_values(self):
        if self.verbose == True:
                print("[filewriter] all values have been reset")

        self.image_list = []
        self.image_counter = 0

        self.writing_to_image_list = False
        self.background_image_set = False
        
        self.writing_to_file = False
        self.stop()

        self.create_buffer = True

    def stop(self):
        self.stopped = True

    def check_for_duplicates(self):
        if len(self.image_list) > 0:
            last_frame = self.image_list[0]

            final_image_list = []
            final_image_list.append(last_frame)

            for i, frame in enumerate(self.image_list, start=1):
                if np.array_equal(frame, last_frame):
                    continue
                else:
                    final_image_list.append(frame)
                    last_frame = frame
            
            if (len(self.image_list) == len(final_image_list)):
                return "No duplicates detected!"
            elif (len(self.image_list) != len(final_image_list)):
                delta = (len(self.image_list) - len(final_image_list))
                self.image_list = final_image_list
                return str(delta) + " duplicates detected and removed."
        else:
            return "image list is empty"