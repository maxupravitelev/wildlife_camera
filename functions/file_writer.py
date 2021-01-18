import cv2
import os
from functions.imgToGif import imgToGif
import numpy as np
from threading import Thread
import threading

class File_writer:
    def __init__(self, mode="avi"):

        self.file_done = True

        self.fileCount = 0

        self.inactivityCounter = 0

        self.image_counter = 0

        self.image_limit = 100

        self.image_list = []

        self.inactivity_limit = 4

        self.background_image = None

        self.motion_detected = False

        self.frame = None

        self.stopped = False

        self.last_frame = None

        self.lock = threading.Lock()

        self.writing = False

        self.same_frame = False

        self.mode = mode

        if self.mode == "avi":
            self.fps = 30
            self.frame_width = 640
            self.frame_height = 480
            self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

    def start(self):    
        lock = threading.Lock()
        Thread(target=self.create_gif, args=(lock,)).start()
        return self  

    def create_gif(self, lock):
        while not self.stopped:
            if self.motion_detected == True and self.image_counter < self.image_limit and self.same_frame == False:
                if np.array_equal(self.last_frame,self.frame):
                #     # print("same frame")
                    continue   
                # print("write to gif")
                self.inactivityCounter = 0
                self.file_done = False
                self.image_list.append(self.frame)
                self.image_counter += 1
                # print("Image count: " + str(self.image_counter))
                self.last_frame = self.frame.copy()

            else:
                if self.file_done == False and self.inactivityCounter <= self.inactivity_limit:
                    if np.array_equal(self.last_frame,self.frame):
                        # print("same frame")
                        continue  
                    self.inactivityCounter += 1

                    self.image_list.append(self.frame)
                    self.image_counter += 1
                    # print("Image count: " + str(self.image_counter))
                    self.last_frame = self.frame.copy()

                    print("Append while inactive. Count: " + str(self.inactivityCounter))

                if self.file_done == False and self.inactivityCounter > self.inactivity_limit:

                    # if self.image_counter > 4:
                        # create folder for images
                        
                        # use lock to reset backgroung image for all processes 
                        # with self.lock:
                    # print("active threads: " + str(threading.active_count()))
                    # print("current thread: " + str(threading.current_thread()))
                    
                    with lock:

                        if self.mode == "gif":

                            # print("lock check: " + str(lock.locked()))
                            # print("wrting to file")
                            # print("active threads: " + str(threading.active_count()))
                            # print("current thread: " + str(threading.current_thread()))
                        

                            self.writing = True

                            newFolder = 'gifs/images' + str(self.fileCount)
                            if not os.path.isdir(newFolder):
                                os.makedirs(newFolder)

                            print("Total images: " + str(len(self.image_list)))

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
                            imgToGif(self.fileCount)

                            self.fileCount +=1
                            print("GIFs created: " + str(self.fileCount))
                        
                            # reset values to handle next gif
                            self.image_list = []
                            self.image_counter = 0

                            self.file_done = True
                            self.background_image = None
                            
                            self.writing = False
                        
                        elif self.mode == "avi":

                            for frame in self.image_list:

                                self.writer.write(frame)
                            self.fileCount += 1
                            print("AVIs created: " + str(self.fileCount))
                            self.file_done = True
                            self.writer = cv2.VideoWriter("avi/output"+ str(self.fileCount) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

                            # reset values to handle next gif
                            self.image_list = []
                            self.image_counter = 0

                            self.file_done = True
                            self.background_image = None
                            
                            self.writing = False

                    # self.image_list = []
                    # self.image_counter = 0

                    # self.file_done = True
                    # self.background_image = None

        if cv2.waitKey(1) == ord("x"):
            print("analyzer stopped")
            self.stopped = True

    def stop(self):
        self.stopped = True