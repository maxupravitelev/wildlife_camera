import cv2
import os
import numpy as np

class Avi_writer:
    def __init__(self, frame_on_startup ):

        self.file_done = False

        self.inactivityCounter = 0

        self.count = 0

        self.frame_height = frame_on_startup.shape[0]

        self.frame_width = frame_on_startup.shape[1]

        self.fps = 30

        self.writer = cv2.VideoWriter("avi/output"+ str(self.count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))
        
        self.inactivity_limit = 175

        self.image_list = []


    def create_avi(self, motion, frame):

        
        if motion is True:
            self.file_done = False
            #motionCounter = motionCounter + 1
            #print(motionCounter)
            # self.writer.write(frame)
            # self.frame_list.append()
            imageListIndex = len(self.image_list)
            
            if imageListIndex != 0:
                lastElement = self.image_list[imageListIndex - 1]

                if np.array_equal(lastElement,frame):
                    return

            self.image_list.append(frame)
            self.inactivityCounter = 0


        else:
            if self.inactivityCounter <= self.inactivity_limit:
                self.inactivityCounter += 1
                imageListIndex = len(self.image_list)

                if imageListIndex != 0:
                    lastElement = self.image_list[imageListIndex - 1]

                    if np.array_equal(lastElement,frame):
                        return

                self.image_list.append(frame)
                # writer.write(frame)
                #print(self.inactivityCounter)
            if self.file_done == False and self.inactivityCounter > self.inactivity_limit:
                print("writing avi")
                #print((self.frame_width,self.frame_height))
                #if file_done == False and motionCounter >= 3 and inactivityCounter > 100:
                for frame in self.image_list:
                    self.writer.write(frame)
                #motionCounter = 0
                self.count += 1
                print("count: " + str(self.count))
                self.file_done = True
                self.writer = cv2.VideoWriter("avi/output"+ str(self.count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), self.fps,(self.frame_width,self.frame_height))

