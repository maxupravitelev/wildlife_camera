import cv2

background_image=None
count = 0

frame_width = 1296
frame_height = 730

cap=cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi",
cv2.VideoWriter_fourcc(*"MJPG"), 30,(frame_width,frame_height))

gifDone = True
inactivityCounter = 0
motionCounter = 0

while True:
    ret, frame = cap.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    if background_image is None:
        background_image=gray_frame
        continue

    delta=cv2.absdiff(background_image,gray_frame)
    threshold=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    if cnts[1] is not None:
        gifDone = False
        motionCounter = motionCounter + 1
        print(motionCounter)
        writer.write(frame)
        inactivityCounter = 0

    else:
        inactivityCounter += 1
        if gifDone == False and motionCounter >= 3 and inactivityCounter > 200:
                        
            motionCounter = 0
            count += 1
            print("count: " + str(count))
            writer.release()
            gifDone = True
            writer = cv2.VideoWriter("avi/output"+ str(count) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 60,(frame_width,frame_height))
            #out.release()

    # (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    # for contour in contours:
    #     if cv2.contourArea(contour) < 8000:
    #         continue
    #     (x, y, w, h)=cv2.boundingRect(contour)
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,255), 10)
    
    #cv2.imshow("Color Frame",frame)
#    image = cv2.rectangle(image, start_point, end_point, color, thickness) 

    # image = cv2.rectangle(frame, (0,0), (600,), (0,0,0), -1)
    # cv2.imshow('Video feed', image)

    cv2.namedWindow('Video feed', cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty('Video feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video feed', cv2.flip(frame, 1))

    #cv2.imshow("gray_frame Frame",gray_frame)
    #cv2.imshow("Delta Frame",delta)
    #cv2.imshow("Threshold Frame",threshold)
    

    key=cv2.waitKey(1)

    if key==ord('x'):
        break

writer.release()
cap.release()
cv2.destroyAllWindows

# Built upon:
# https://github.com/arindomjit/Motion_Detected_Alarm/blob/master/motion_detector.py