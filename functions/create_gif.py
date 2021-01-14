import cv2
import os
from functions.imgToGif import imgToGif
import numpy as np


class Gif_writer:
    def __init__(self):

        self.file_done = True

        self.folderCount = 0

        self.inactivityCounter = 0

        self.image_counter = 0

        self.image_limit = 80

        self.image_list = []

        self.inactivity_limit = 3

        self.background_image = None

        
    def create_gif(self, motion, frame):

        if motion == True and self.image_counter < self.image_limit:
            # print("write to gif")
            self.inactivityCounter = 0
            self.file_done = False
            self.image_list.append(frame)
            self.image_counter += 1
            # print("Image count: " + str(self.image_counter))

        else:
            if self.file_done == False and self.inactivityCounter <= self.inactivity_limit:
                self.inactivityCounter += 1

                self.image_list.append(frame)
                self.image_counter += 1
                # print("Image count: " + str(self.image_counter))

                print("Append while inactive. Count: " + str(self.inactivityCounter))

            if self.file_done == False and self.inactivityCounter > self.inactivity_limit:

                # create folder for images
                newFolder = 'gifs/images' + str(self.folderCount)
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
                imgToGif(self.folderCount)

                self.folderCount +=1
                print("Files created: " + str(self.folderCount))
                
                # reset values to handle next gif
                self.image_list = []
                self.image_counter = 0

                self.file_done = True
                self.background_image = None