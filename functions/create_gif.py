import cv2
import os
from imgToGif import imgToGif
import numpy as np


class Gif_writer:
    def __init__(self ):

        self.file_done = False

        self.folderCount = 0

        self.inactivityCounter = 0

        self.count = 0

        self.image_list = []

        
    def create_gif(self, motion, frame):

        
        if motion is not None:
            self.inactivityCounter = 0
            self.file_done = False

            imageListIndex = len(imageList)
            
            if imageListIndex != 0:
                lastElement = imageList[imageListIndex - 1]

                if np.array_equal(lastElement,frame):
                    return

            self.imageList.append(frame)

        else:
            #print(inactivityCounter)
            if self.inactivityCounter <= 15:
                self.inactivityCounter += 1
                # print(inactivityCounter)
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
            if self.file_done == False and self.inactivityCounter > 15:

            # if self.file_done == False and count >= 3 and inactivityCounter > 100:

                newFolder = 'gifs/images' + str(self.folderCount)
                if not os.path.isdir(newFolder):
                    os.makedirs(newFolder)
                # print(str(len(imageList)))
                for num, image in enumerate(imageList, start=0):
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
                self.imageList = []
                # count = 0
                self.file_done = True
                #inactivityCounter = 0