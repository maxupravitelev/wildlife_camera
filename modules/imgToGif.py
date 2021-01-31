from PIL import Image
import glob 
import json
import cv2

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

        for bgr_image in image_list:
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image, mode="RGB")
            pil_image_list.append(image)

        pil_image_list[0].save('gifs/out_pil'+ str(folderCount) + '.gif',
                    save_all=True, append_images=pil_image_list[1:], optimize=False, duration=(gif_duration), loop=loop_gif)


    else:

        with ImageFromWand() as wand:

            for bgr_image in image_list:
                rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
                image = wand.from_array(rgb_image)
                wand.sequence.append(image)


            for cursor in range(len(wand.sequence)):
                with wand.sequence[cursor] as frame:
                    frame.delay = int(gif_duration / 7)

            wand.type = 'optimize'
            wand.save(filename='gifs/out'+ str(folderCount) + '.gif')



def folder_to_gif():

    # init image list
    images = []

    # init counter to count total files in folder
    files_in_folder = 0

    # count total files in folder
    for path in glob.glob("gifs/images" + "/" + "*.jpg"):
        files_in_folder += 1
   
    if imagemagick_installed == False:
        for i in range(0, files_in_folder):
            if i < 10:
                for img in glob.glob("gifs/images" + "/image1000" + str(i) + "*.jpg"):
                    #print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)
            if i >= 10 and i < 100: 
                for img in glob.glob("gifs/images" + "/image100" + str(i) + "*.jpg"):
                    #print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)
            if i >= 100: 
                for img in glob.glob("gifs/images" + "/image10" + str(i) + "*.jpg"):
                    #print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)

        images[0].save('gifs/out'+ '.gif',
                    save_all=True, append_images=images[1:], optimize=True, duration=(gif_duration), loop=loop_gif)

    if imagemagick_installed == True:

        with ImageFromWand() as wand:

            for i in range(0, len(wand.sequence), 1):
                if i < 10:
                    for img in glob.glob("gifs/images" + "/image1000" + str(i) + "*.jpg"):

                        with ImageFromWand(filename=img) as one:
                            wand.sequence.append(one)
                if i >= 10 and i < 100: 
                    for img in glob.glob("gifs/images" + "/image100" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as two:
                            wand.sequence.append(two)
                if i >= 100: 
                    for img in glob.glob("gifs/images" + "/image10" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as three:
                            wand.sequence.append(three)

            # Create progressive delay for each frame
            for cursor in range(len(files_in_folder)):
                with wand.sequence[cursor] as frame:
                    frame.delay = 1 * (cursor + 1)

            # Set layer type
            wand.type = 'optimize'
            wand.save(filename='gifs/out'+ str(folderCount) + '.gif')