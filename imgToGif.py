from PIL import Image, ImageDraw
import glob 


# def imgToGif():
#     for i in range(1, 9):
#         img = Image.open("images/image"+str(i)+".jpg")
#         images.append(img)
#     images[0].save('out.gif',
#                    save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)

# def imgToGif(folderCount):
#     images = []

#     for img in glob.glob("gifs/images" + str(folderCount) + "/" + "*.jpg"):
#         newJpg = Image.open(img)
#         images.append(newJpg)
#         print(img)
#     print(images)
#     # for i in range(1, len(images)):
#         #img = Image.open("images/image"+str(i)+".jpg")
#     #    images.append(img)
#     images[0].save('gifs/out'+ str(folderCount) + '.gif',
#                    save_all=True, append_images=images[1:], optimize=True, duration=200, loop=0)

def imgToGif(folderCount):
    images = []

    orderList = []

    testList = []

    finalNumberList = []

    for img in glob.glob("gifs/images" + str(folderCount) + "/" + "*.jpg"):
        orderList.append(img)

    for order in orderList:
        s = order.replace("gifs/images" + str(folderCount) + "/image", "")
        testList.append(s)

    for order in testList:
        s = order.replace(".jpg", "")
        finalNumberList.append(int(s))



        #print(img)
    #print(finalNumberList)

    for i in range(0, len(finalNumberList), 1):
        if i < 10:
            for img in glob.glob("gifs/images" + str(folderCount) + "/image1000" + str(i) + "*.jpg"):
                #print(img)
                newJpg = Image.open(img)
                images.append(newJpg)
        if i >= 10 and i < 100: 
            for img in glob.glob("gifs/images" + str(folderCount) + "/image100" + str(i) + "*.jpg"):
                #print(img)
                newJpg = Image.open(img)
                images.append(newJpg)
        if i >= 100: 
            for img in glob.glob("gifs/images" + str(folderCount) + "/image10" + str(i) + "*.jpg"):
                #print(img)
                newJpg = Image.open(img)
                images.append(newJpg)

    images[0].save('gifs/out'+ str(folderCount) + '.gif',
                   save_all=True, append_images=images[1:], optimize=True, duration=70, loop=0)

# imgToGif(0)