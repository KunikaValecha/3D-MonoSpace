from PIL import Image
import numpy as np

im = Image.open('000001.png')

pixels = list(im.getdata())
width, height = im.size 
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
np.savetxt("pixel_data.txt", pixels,fmt='%d', delimiter=" ") 
