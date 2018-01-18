## Shondell Baijoo
## Computer Vision Project
## Dec 2017

from PIL import  Image, ImageFilter, ImageDraw
import cv2

PICTUREOUT = "tdo.png" # output of cartoon.py, input to popart
PICTUREDOT = "tdot.png" # output of popart

## dots! 
image = Image.open(PICTUREOUT) # to pull original pixel color from
width, height = image.size 
dot = Image.open(PICTUREOUT) # for drawing output
p = image.load() 
draw = ImageDraw.Draw(dot)
pdot = dot.load()

#lighten all pixels
for i in range(0,width):
    for j in range(0, height):
        value = [0,0,0]
        value[0] = p[i,j][0] + 50
        value[1] = p[i,j][1] + 50
        value[2] = p[i,j][2] + 50
        pdot[i,j] = tuple(value) 
# draw dots in 4*4 window
i=0
while i < width - 4:
    j = 0
    while j < height - 4:
        value = [0,0,0]
        value[0] = p[i,j][0] - 30
        value[1] = p[i,j][1] - 30
        value[2] = p[i,j][2] - 30
        draw.ellipse( [(i+1,j+1), (i+4, j+4)], fill=(tuple(value)))
        j = j+4
    i=i+4

dot.save(PICTUREDOT)
 

