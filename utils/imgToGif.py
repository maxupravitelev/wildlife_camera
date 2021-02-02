from PIL import Image
import glob 
import json
import cv2

# function to parse bool value from config file
from utils.boolcheck import boolcheck

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