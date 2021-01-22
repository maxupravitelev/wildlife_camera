from PIL import Image, ImageDraw
import glob 


# init modes
image_magic_mode = False

if image_magic_mode == True:
    from wand.image import Image as ImageFromWand


def imgToGif(folderCount):
    
    # read images from files into imagelist while preserving the correct order
    images = []
    files_in_folder = 0

    for path in glob.glob("gifs/images" + str(folderCount) + "/" + "*.jpg"):
        files_in_folder += 1
   
    if image_magic_mode == False:

        for i in range(0, files_in_folder):
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
                        save_all=True, append_images=images[1:], optimize=True, duration=50, loop=0)

    if image_magic_mode == True:

        # with ImageFromWand(filename='gifs/out'+ str(folderCount) + '.gif') as img:
        #     img.save(filename='gifs/outCompressed'+ str(folderCount) + '.gif')

        with ImageFromWand() as wand:

            for i in range(0, len(finalNumberList), 1):
                if i < 10:
                    for img in glob.glob("gifs/images" + str(folderCount) + "/image1000" + str(i) + "*.jpg"):

                        with ImageFromWand(filename=img) as one:
                            wand.sequence.append(one)
                if i >= 10 and i < 100: 
                    for img in glob.glob("gifs/images" + str(folderCount) + "/image100" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as two:
                            wand.sequence.append(two)
                if i >= 100: 
                    for img in glob.glob("gifs/images" + str(folderCount) + "/image10" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as three:
                            wand.sequence.append(three)

            # Create progressive delay for each frame
            for cursor in range(len(finalNumberList)):
                with wand.sequence[cursor] as frame:
                    frame.delay = 1 * (cursor + 1)
            # Set layer type
            wand.type = 'optimize'
            wand.save(filename='gifs/out'+ str(folderCount) + '.gif')