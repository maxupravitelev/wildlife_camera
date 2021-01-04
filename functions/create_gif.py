import cv2
import os
from functions.imgToGif import imgToGif
import numpy as np


class Gif_writer:
    def __init__(self):

        self.file_done = True

        self.folderCount = 0

        self.inactivityCounter = 0

        self.count = 0

        self.image_list = []

        self.inactivity_limit = 175

        
    def create_gif(self, motion, frame):

        
        if motion is True:
            # print("write to gif")
            self.inactivityCounter = 0
            self.file_done = False

            imageListIndex = len(self.image_list)
            
            if imageListIndex != 0:
                lastElement = self.image_list[imageListIndex - 1]

                if np.array_equal(lastElement,frame):
                    return

            self.image_list.append(frame)

        else:
            #print(inactivityCounter)
            if self.inactivityCounter <= self.inactivity_limit:
                self.inactivityCounter += 1
                # frame = vs.read()
                # if np.array_equal(imageList[-1:],frame):
                # if (imageList[-1:]==frame).all():
                    # print("same")
                    # continue
                # imageList.append(frame)
                
                return

            # print(newCounter)
            #if count < 6:
                #count = 0
            if self.file_done == False and self.inactivityCounter > self.inactivity_limit:

            # if self.file_done == False a                # print(self.inactivityCounter)
nd count >= 3 and inactivityCounter > 100:

                newFolder = 'gifs/images' + str(self.folderCount)
                if not os.path.isdir(newFolder):
                    os.makedirs(newFolder)
                # print(str(len(self.image_list)))
                for num, image in enumerate(self.image_list, start=0):
                    if num < 10:
                        localPath = newFolder + '/image1000'+str(num)+'.jpg'                
                    if num >= 10 and num < 100: 
                        localPath = newFolder + '/image100'+str(num)+'.jpg'                
                    if num >= 100: 
                        localPath = newFolder + '/image10'+str(num)+'.jpg'
                    cv2.imwrite(localPath,image)  

                imgToGif(self.folderCount)
                self.folderCount +=1
                print("count: " + str(self.folderCount))
                self.image_list = []
                # count = 0
                self.file_done = True

                #inactivityCounter = 0