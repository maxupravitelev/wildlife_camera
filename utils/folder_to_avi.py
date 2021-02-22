import glob 
import cv2


def folder_to_avi(folder_path=""):

    # init image list
    images = []

    # init counter to count total files in folder
    files_in_folder = 0

    # count total files in folder
    for path in glob.glob(folder_path + "*.jpg"):
        files_in_folder += 1
    print("Total images in folder: " + str(files_in_folder))

    for i in range(0, files_in_folder):
        if i < 10:
            for img in glob.glob("image1000" + str(i) + ".jpg"):
                newJpg = cv2.imread(img)
                images.append(newJpg)
        if i >= 10 and i < 100: 
            for img in glob.glob("image100" + str(i) + ".jpg"):
                newJpg = cv2.imread(img)
                images.append(newJpg)
        if i >= 100: 
            for img in glob.glob("image10" + str(i) + ".jpg"):
                newJpg = cv2.imread(img)
                images.append(newJpg)
    fps = 30
    frame_width = images[0].shape[1]
    frame_height = images[0].shape[0]
    

    writer = cv2.VideoWriter("video_file"+ ".avi", cv2.VideoWriter_fourcc(*"MJPG"), fps,(frame_width,frame_height))

    for image in images:
        writer.write(image)


folder_to_avi()
