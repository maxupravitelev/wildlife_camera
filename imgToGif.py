from PIL import Image, ImageDraw
import glob 


# def imgToGif():
#     for i in range(1, 9):
#         img = Image.open("images/image"+str(i)+".jpg")
#         images.append(img)
#     images[0].save('out.gif',
#                    save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)

def imgToGif(folderCount):
    images = []

    for img in glob.glob("gifs/images" + str(folderCount) + "/" + "*.jpg"):
        newJpg = Image.open(img)
        images.append(newJpg)
        print(img)

    # for i in range(1, len(images)):
        #img = Image.open("images/image"+str(i)+".jpg")
    #    images.append(img)
    images[0].save('gifs/out'+ str(folderCount) + '.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=80, loop=0)

# imgToGif(0)