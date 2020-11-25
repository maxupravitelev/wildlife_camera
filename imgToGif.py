from PIL import Image, ImageDraw

images = []

def imgToGif():
    for i in range(1, 9):
        img = Image.open("images/image"+str(i)+".jpg")
        images.append(img)
    images[0].save('out.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

imgToGif()