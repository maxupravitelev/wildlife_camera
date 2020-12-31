import cv2
import os
from .. import imgToGif
               


def create_gif(motion):

       
    if motion is not None:

        gifDone = False

        newFolder = 'gifs/images' + str(folderCount)
        if not os.path.isdir(newFolder):
            os.makedirs(newFolder)
                            
        if count < 10:
            localPath = newFolder + '/image1000'+str(count)+'.jpg'                
        if count >= 10 and count < 100: 
            localPath = newFolder + '/image100'+str(count)+'.jpg'                
        if count >= 1000: 
            localPath = newFolder + '/image10'+str(count)+'.jpg'  
                    
        #print(count)
        cv2.imwrite(localPath,frame)
        count += 1
        #time.sleep(0.1)
        inactivityCounter = 0
                    

    else:
        #print(inactivityCounter)
        if inactivityCounter <= 175:
            inactivityCounter += 1
            # if localPath != "":
            #     print(inactivityCounter)
            if count < 10:
                localPath = newFolder + '/image1000'+str(count)+'.jpg'                
            if count >= 10 and count < 100: 
                    localPath = newFolder + '/image100'+str(count)+'.jpg'                
            if count >= 1000: 
                localPath = newFolder + '/image10'+str(count)+'.jpg'  

            cv2.imwrite(localPath,frame)
            count += 1
            # continue
    
            # print(newCounter)
            #if count < 6:
            #count = 0
        if gifDone == False and count >= 3 and inactivityCounter > 175:
            imgToGif(folderCount)
            folderCount +=1
            print("count: " + str(folderCount))

            count = 0
            gifDone = True
            inactivityCounter = 0