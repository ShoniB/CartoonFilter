## Shondell Baijoo 
## Computer Vision Project
## Dec 2017

from PIL import  Image, ImageFilter
import cv2

# input and output image names
PICTURE = "silva.png"
PICTUREBLUR = "sb.jpg" #blur output
PICTURETHRES = "st.jpg" # threshold output with pasted eyes
PICTUREFACE = "sf.jpg" # face/eye detection
PICTUREOUT = "so.jpg" # Final output

#blur image
img = cv2.imread(PICTURE) 
blur = cv2.GaussianBlur(img, (5,5), 2) 
cv2.imwrite(PICTUREBLUR, blur) 

image = Image.open(PICTUREBLUR)
width, height = image.size
p=image.load() # pixel array

# Color posterizing
# 0-30 30-60=50 60-90=80 90-120=110  120-150=140 150-180=170  180-210 = 200   210+ = 255
for i in range(0, width):
    for j in range(0, height):
        value = [0,0,0]
        value[0]= p[i,j][0] - (p[i,j][0]%30) + 30
        value[1] = p[i,j][1] - (p[i,j][1]%30) + 30
        value[2] = p[i,j][2] - (p[i,j][2]%30) + 30
        p[i,j] = tuple(value) 
image.save(PICTURETHRES)

# darken shadows
for i in range(0,width):
    for j in range(0, height):
        if(p[i,j] < (150,150,150)):
            value = [0,0,0]
            value[0] = p[i,j][0] - 25
            value[1] = p[i,j][1] - 25
            value[2] = p[i,j][2] - 25
            p[i,j] = tuple(value)

# average filter 
holding = []
for i in range(1, width-1): #ignore boundaries
    temp = [] 
    holding.append(temp)
    for j in range(1, height-1):
        value = [0,0,0]
        value[0] = int((p[i,j][0] + p[i+1, j][0] + p[i, j+1][0] + p[i+1, j+1][0])/4)
        value[1] = int((p[i,j][1] + p[i+1, j][1] + p[i, j+1][1] + p[i+1, j+1][1])/4)
        value[2] = int((p[i,j][2] + p[i+1, j][2] + p[i, j+1][2] + p[i+1, j+1][2])/4)      
        holding[i-1].append(value)
for i in range (1, width-1):
    for j in range(1, height-1):
        p[i,j] = tuple(holding[i-1][j-1]) 

#lighten highlights
for i in range(0, width):
    for j in range(0, height): 
        if(p[i,j] > (210,210,210)):
            value = [0,0,0] 
            value[0] = p[i,j][0] + 20
            value[1] = p[i,j][1] + 20
            value[2] = p[i,j][2] + 20
            p[i,j] = tuple(value) 

##########  Get coordinates of eyes ################################################

face_cascade = cv2.CascadeClassifier('/home/hercules/Documents/Fall17/Vision/Final/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('/home/hercules/Documents/Fall17/Vision/Final/opencv-master/data/haarcascades/haarcascade_eye.xml')

img = cv2.imread(PICTURE)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

eyes = []
face = face_cascade.detectMultiScale(gray, 1.3, 5) # run detection on greyscale
for(x,y,w,h) in face:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2) # draw rectangle around face
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray) 
    for (ex,ey,ew,eh) in eyes: 
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2) # draw rectangle around eyes

if(len(face) !=0): # if face is found
    fx,fy,fw,fh = face[0] # get coordinates

cv2.imwrite(PICTUREFACE, img)

######################################################################################

eyeImage = Image.open(PICTURE) # open original picture
peye = eyeImage.load()

# posterize original image
# 0-30 30-60=50 60-90=80 90-120=110  120-150=140 150-180=170  180-210 = 200   210+ = 255
for i in range(0, width):
    for j in range(0, height):
        value = [0,0,0]
        value[0]= peye[i,j][0] - (peye[i,j][0]%30) + 30
        value[1] = peye[i,j][1] - (peye[i,j][1]%30) + 30
        value[2] = peye[i,j][2] - (peye[i,j][2]%30) + 30
        peye[i,j] = tuple(value) 

## paste eyes in blurred, thresholded image
for (ex,ey,ew,eh) in eyes:
    box = (ex+fx, ey+fy, ex+fx+ew, ey+fy+eh) 
    ic = eyeImage.crop(box) 
    image.paste(ic, box) # paste eyes
    # blur edges of pasted eyes
    for i in range(ex+fx, ex+fx+ew):
        box = (i, ey+fy, i+5, ey+fy+5)
        box2 = (i, ey+fy+eh-5, i+5, ey+fy+eh)
        blurcrop = image.crop(box)
        blurcrop2= image.crop(box2)
        blurcrop = blurcrop.filter(ImageFilter.BLUR)
        blurcrop2 = blurcrop2.filter(ImageFilter.BLUR)
        image.paste(blurcrop, box)
        image.paste(blurcrop2, box2) 
    for i in range(ey + fy, ey+fy+eh):
        box = (ex+fx, i, ex+fx+5, i+5)
        box2 = (ex+fx+ew-5, i, ex+fx+ew, i+5)
        blurcrop = image.crop(box) 
        blurcrop2 = image.crop(box2) 
        blurcrop = blurcrop.filter(ImageFilter.BLUR)
        blurcrop2 = blurcrop2.filter(ImageFilter.BLUR)
        image.paste(blurcrop,box)
        image.paste(blurcrop2,box2)

####################################################################################

image.save(PICTURETHRES) # save blurred, thresholded image with pasted eyes
image = Image.open(PICTURETHRES)
p=image.load()

#lighten highlights and darken shadows in eyes
for(ex,ey,ew,eh) in eyes:
    for i in range(ex+fx, ex+fx+ew):
        for j in range(ey + fy, ey+fy+eh):
            if(p[i,j] > (210,210,210)):
                value = [0,0,0] 
                value[0] = p[i,j][0] + 20
                value[1] = p[i,j][1] + 20
                value[2] = p[i,j][2] + 20
                p[i,j] = tuple(value)
            if(p[i,j] < (160,160,160)):
                value = [0,0,0]
                value[0] = p[i,j][0] - 20
                value[1] = p[i,j][1] - 20
                value[2] = p[i,j][2] - 20
                p[i,j] = tuple(value)

# average filter over whole image
holding = []
# boundaries
for i in range(1, width-1): #ignore boundaries
    temp = [] 
    holding.append(temp)
    for j in range(1, height-1):
        value = [0,0,0]
        value[0] = int((p[i,j][0] + p[i+1, j][0] + p[i, j+1][0] + p[i+1, j+1][0] )/4)
        value[1] = int((p[i,j][1] + p[i+1, j][1] + p[i, j+1][1] + p[i+1, j+1][1])/4)
        value[2] = int((p[i,j][2] + p[i+1, j][2] + p[i, j+1][2] + p[i+1, j+1][2] )/4)      
        holding[i-1].append(value)
for i in range (1, width-1):
    for j in range(1, height-1):
        p[i,j] = tuple(holding[i-1][j-1]) 

image.save(PICTUREOUT) # save final output

 

