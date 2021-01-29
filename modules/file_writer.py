import cv2
import os
from modules.imgToGif import imgToGif
import numpy as np
from threading import Thread
import threading
import json

# function to parse bool value from config file
from modules.utils import boolcheck

class File_writer:
    def __init__(self, height=480, width=680):

        # set setting from config file
        config_path = 'config/config.json'

        with open(config_path) as config_file:
            config = json.load(config_file)

        # init file creation handling
        self.file_done = True
        self.fileCount = 0
        self.writing = False

        # init thread handling flag
        self.stopped = False

        # init image_list handling 

        self.image_list = []     
        self.image_counter = 0
        self.image_limit = 50
        
        # init flag to handle reference background resetting after file is created
        self.background_image_set = False
        
        # init writing to image_list flag 
        self.motion_detected = False

        # init inactivity handling; needed if frames are skipped or contours are not found in inbetween frames
        self.inactivityCounter = 0
        self.inactivity_limit = 4

        # handle modes
        self.mode = config["file_writer_config"]["mode"]

        if self.mode == "avi":
            self.fps = 30
            self.frame_width = width
            self.frame_height = height
            self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

        self.verbose = boolcheck(config["general_config"]["verbose"])


        
        # init buffer_mode
        self.buffer_mode = boolcheck(config["general_config"]["create_buffer"])
        self.create_buffer = True


    def start(self):    
        lock = threading.Lock()
        Thread(target=self.write_to_file, args=(lock,)).start()
        return self 


    def write_buffer(self, frame):
        # if self.create_buffer == True and self.motion_detected == False:
            if len(self.image_list) < 10:
                self.image_list.append(frame)
            else:
                self.image_list.pop(0)
                self.image_list.append(frame)

    def handle_image_list(self, frame):

        if self.image_counter < self.image_limit and self.motion_detected == True:
            
            self.create_buffer = False

            if self.verbose == True:
                print("[filewriter] Image count: " + str(self.image_counter))

            self.inactivityCounter = 0
            self.file_done = False
            self.image_list.append(frame)
            self.image_counter += 1
        else:
            if self.file_done == False and self.inactivityCounter <= self.inactivity_limit:

                self.inactivityCounter += 1

                self.image_list.append(frame)
                self.image_counter += 1
                if self.verbose == True:
                    print("[filewriter] append image while inactive | count: " + str(self.inactivityCounter))

            if self.file_done == False and self.inactivityCounter > self.inactivity_limit:

                self.writing = True


    def write_to_file(self, lock):
        while not self.stopped:
            if self.writing == False:
                continue

            with lock:
                if self.verbose == True:
                    print("[filewriter] wrting to file...")

                    if self.verbose == True:
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
                    imgToGif(self.fileCount, self.image_list)

                    self.fileCount +=1
                    print("[filewriter] GIFs created: " + str(self.fileCount))
                
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
                    self.file_done = True
                    self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

                    # reset values to handle next avi
                    self.reset_values()

    def reset_values(self):
        self.image_list = []
        self.image_counter = 0

        self.file_done = True
        self.background_image_set = False
        
        self.writing = False

        self.create_buffer = True

    def stop(self):
        self.stopped = True