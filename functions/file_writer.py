import cv2
import os
from ... import imgToGif


class File_writer:
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

    # def create_gif(motion):

        
    #     if motion is not None:

    #         gifDone = False

    #         newFolder = 'gifs/images' + str(folderCount)
    #         if not os.path.isdir(newFolder):
    #             os.makedirs(newFolder)
                                
    #         if count < 10:
    #             localPath = newFolder + '/image1000'+str(count)+'.jpg'                
    #         if count >= 10 and count < 100: 
    #             localPath = newFolder + '/image100'+str(count)+'.jpg'                
    #         if count >= 1000: 
    #             localPath = newFolder + '/image10'+str(count)+'.jpg'  
                        
    #         #print(count)
    #         cv2.imwrite(localPath,frame)
    #         count += 1
    #         #time.sleep(0.1)
    #         inactivityCounter = 0
                        

    #     else:
    #         #print(inactivityCounter)
    #         if inactivityCounter <= 175:
    #             inactivityCounter += 1
    #             # if localPath != "":
    #             #     print(inactivityCounter)
    #             if count < 10:
    #                 localPath = newFolder + '/image1000'+str(count)+'.jpg'                
    #             if count >= 10 and count < 100: 
    #                     localPath = newFolder + '/image100'+str(count)+'.jpg'                
    #             if count >= 1000: 
    #                 localPath = newFolder + '/image10'+str(count)+'.jpg'  

    #             cv2.imwrite(localPath,frame)
    #             count += 1
    #             # continue
        
    #             # print(newCounter)
    #             #if count < 6:
    #             #count = 0
    #         if gifDone == False and count >= 3 and inactivityCounter > 175:
    #             imgToGif(folderCount)
    #             folderCount +=1
    #             print("count: " + str(folderCount))

    #             count = 0
    #             gifDone = True
    #             inactivityCounter = 0