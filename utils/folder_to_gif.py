from PIL import Image
import glob 


gif_duration = 50
imagemagick_installed = True

if imagemagick_installed == True:
    from wand.image import Image as ImageFromWand


def folder_to_gif(folder_path=""):

    # init image list
    images = []

    # init counter to count total files in folder
    files_in_folder = 0

    # count total files in folder
    for path in glob.glob(folder_path + "*.jpg"):
        files_in_folder += 1
    print(files_in_folder)

    if imagemagick_installed == False:
        for i in range(0, files_in_folder):
            if i < 10:
                for img in glob.glob("image1000" + str(i) + "*.jpg"):
                    # print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)
            if i >= 10 and i < 100: 
                for img in glob.glob("/image100" + str(i) + "*.jpg"):
                    #print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)
            if i >= 100: 
                for img in glob.glob("/image10" + str(i) + "*.jpg"):
                    #print(img)
                    newJpg = Image.open(img)
                    images.append(newJpg)

        images[0].save("gif_from_folder" + '.gif',
                    save_all=True, append_images=images[1:], optimize=True, duration=(gif_duration), loop=0)

    if imagemagick_installed == True:

        with ImageFromWand() as wand:

            for i in range(0, files_in_folder, 1):
                if i < 10:
                    for img in glob.glob("image1000" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as one:
                            wand.sequence.append(one)
                if i >= 10 and i < 100: 
                    for img in glob.glob("image100" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as two:
                            wand.sequence.append(two)
                if i >= 100: 
                    for img in glob.glob("image10" + str(i) + "*.jpg"):
                        with ImageFromWand(filename=img) as three:
                            wand.sequence.append(three)

            # Create progressive delay for each frame
            for cursor in range(len(wand.sequence)):
                with wand.sequence[cursor] as frame:
                    frame.delay = 1 * (cursor + 1)

            # Set layer type
            wand.type = 'optimize'
            wand.save(filename="gif_from_folder" + '.gif')

folder_to_gif()