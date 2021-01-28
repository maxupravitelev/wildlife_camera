from PIL import Image, ImageDraw
import glob 
import json
import numpy as np

# function to parse bool value from config file
from modules.utils import boolcheck

config_path = 'config/config.json'

with open(config_path) as config_file:
    config = json.load(config_file)

gif_duration = config["gif_config"]['gif_duration']
loop_gif = config["gif_config"]['loop_gif']
imagemagick_installed = boolcheck(config["gif_config"]['imagemagick_installed'])

if imagemagick_installed == True:
    from wand.image import Image as ImageFromWand

def imgToGif(folderCount, image_list):
    
    if imagemagick_installed == False:

        pil_image_list = []

        for image in image_list:
            im = Image.fromarray(image)
            pil_image_list.append(im)

        pil_image_list[0].save('gifs/out_pil'+ str(folderCount) + '.gif',
                    save_all=True, append_images=pil_image_list[1:], optimize=False, duration=(gif_duration), loop=loop_gif)


    else:

        # with ImageFromWand(filename='gifs/out'+ str(folderCount) + '.gif') as img:
        #     img.save(filename='gifs/outCompressed'+ str(folderCount) + '.gif')

        with ImageFromWand() as wand:

            for image in image_list:
                im = ImageFromWand.from_array(image)
                wand.sequence.append(im)

            # Create progressive delay for each frame
            for cursor in range(len(wand.sequence)):
                with wand.sequence[cursor] as frame:
                    frame.delay = int(gif_duration / 7)

            # print(len(wand.sequence))

            # Set layer type
            wand.type = 'optimize'
            wand.save(filename='gifs/out'+ str(folderCount) + '.gif')



def folder_to_gif(folderCount):

    # read images from files into imagelist while preserving the correct order
    images = []
    files_in_folder = 0

    for path in glob.glob("gifs/images" + str(folderCount) + "/" + "*.jpg"):
        files_in_folder += 1
   
    if imagemagick_installed == False:
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
                    save_all=True, append_images=images[1:], optimize=True, duration=(gif_duration), loop=loop_gif)

    if imagemagick_installed == True:

        # with ImageFromWand(filename='gifs/out'+ str(folderCount) + '.gif') as img:
        #     img.save(filename='gifs/outCompressed'+ str(folderCount) + '.gif')

        with ImageFromWand() as wand:

            for i in range(0, len(wand.sequence), 1):
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