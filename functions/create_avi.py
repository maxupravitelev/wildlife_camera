import cv2
import os


class Avi_writer:
    def __init__(self, frame_on_startup ):

        self.file_done = False

        self.inactivityCounter = 0

        self.count = 0

        self.frame_height = frame_on_startup.shape[0]

        self.frame_width = frame_on_startup.shape[1]

        self.writer = cv2.VideoWriter("avi/output"+ str(self.count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 49,(self.frame_width,self.frame_height))
        
    def create_avi(self, motion, frame):

        
        if motion is not None:
            self.file_done = False
            #motionCounter = motionCounter + 1
            #print(motionCounter)
            self.writer.write(frame)
            self.inactivityCounter = 0


        else:
            if self.inactivityCounter <= 40:
                self.inactivityCounter += 1
                # writer.write(frame)
                #print(self.inactivityCounter)
            if self.file_done == False and self.inactivityCounter > 40:
                #print("test")
                print((self.frame_width,self.frame_height))
                #if file_done == False and motionCounter >= 3 and inactivityCounter > 100:
                
                #motionCounter = 0
                self.count += 1
                print("count: " + str(self.count))
                self.file_done = True
                self.writer = cv2.VideoWriter("avi/output"+ str(self.count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 49,(self.frame_width,self.frame_height))

