## Shondell Baijoo
## Computer Vision Project
## Dec 2017

from PIL import  Image, ImageFilter, ImageDraw

PICTUREOUT = "tdo.png" # input
PICTUREDOT = "tstipple.png" # output

## dots! 
image = Image.open(PICTUREOUT) # image to pull color from
width, height = image.size 
dot = Image.open(PICTUREOUT) # recieve drawn output 
p = image.load() # pixel array
draw = ImageDraw.Draw(dot) 
pdot = dot.load()

# set everything to white
for i in range(0,width):
    for j in range(0, height):
        pdot[i,j] = (255,255,255) 

# draw greyscale dots 
i=0
while i < width - 2:
    j = 0
    while j < height - 2:
        value = int((p[i,j][0] + p[i,j][1] + p[i,j][2])/3) - 50
        if(value < 50 and i>3 and j>3): #if pixel is dark, draw dot closer 
            draw.ellipse( [(i-2+1,j-2+1), (i-2+1, j-2+1)], fill=((value, value, value)))
            draw.ellipse( [(i-1+1,j-3+1), (i-1+1, j-1+1)], fill=((value, value, value)))
        draw.ellipse( [(i+1,j+1),(i+1,j+1)], fill=((value,value,value)))
        j = j+2
    i=i+2

dot.save(PICTUREDOT) # save output

