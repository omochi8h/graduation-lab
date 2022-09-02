from PIL import Image
img = Image.open("gakusyusyasakujo.png")

def scale(im,width):
    h = round(im.height * width/im.width)
    return im.resize((width,h))

imgr = scale(img,125)
imgr = imgr.save("gakusyusyasakujo.png",quality=95)