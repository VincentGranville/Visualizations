from PIL import Image, ImageDraw           # ImageDraw to draw ellipses etc.
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video
from moviepy.editor import VideoFileClip   # to convert mp4 to gif

import numpy as np
import math
import random
random.seed(100)

#--- Global variables ---

m=6               # number of curves
nframe=20000      # number of images 
count=0           # frame counter 
start=2000        # must be smaller than nframe
r=20             # one out of every r image is included in the video

width = 3200 # 1600 # 1600
height =2400 #1200 # 1200

images=[]

etax=[]
etay=[]
sigma=[]
t=[]
x0=[]
y0=[]
flist=[]  # filenames of the images representing each video frame

etax=list(map(float,etax))
etay=list(map(float,etay))
sigma=list(map(float,sigma))
t=list(map(float,t))
x0=list(map(float,x0))
y0=list(map(float,y0))
flist=list(map(str,flist))

#--- Initializing comet parameters ---

for n in range (0,m):
  etax.append(1.0)
  etay.append(0.0)
  t.append(5555555+n/10)
  sigma.append(0.75)
sign=1

minx= 9999.0
miny= 9999.0
maxx=-9999.0
maxy=-9999.0

for n in range (0,m):
  sign=1
  sumx=1.0
  sumy=0.0
  for k in range (2,nframe,1):
    sign=-sign
    sumx=sumx+sign*np.cos(t[n]*np.log(k))/pow(k,sigma[n])
    sumy=sumy+sign*np.sin(t[n]*np.log(k))/pow(k,sigma[n])
    if k >= start:
      if sumx < minx:
        minx=sumx
      if sumy < miny:
        miny=sumy
      if sumx > maxx:
        maxx=sumx
      if sumy > maxy:
        maxy=sumy
sign=1
rangex=maxx-minx
rangey=maxy-miny

img  = Image.new( mode = "RGB", size = (width, height), color = (255, 255, 255) )
pix = img.load()
draw = ImageDraw.Draw(img)

red=255
green=255
blue=255
col=(red,green,blue)
count=0

#--- Main Loop ---

for k in range (2,nframe,1): # loop over time, each t corresponds to a ideo frame
  if k%10 == 0:
    print("Building frame:",k)
  sign=-sign
  for n in range (0,m):  # loop over curves
    x0.insert(n,int(width*(etax[n]-minx)/rangex))
    y0.insert(n,int(height*(etay[n]-miny)/rangey))
    etax[n]=etax[n]+sign*np.cos(t[n]*np.log(k))/pow(k,sigma[n])
    etay[n]=etay[n]+sign*np.sin(t[n]*np.log(k))/pow(k,sigma[n])
    x=int(width*(etax[n]-minx)/rangex)
    y=int(height*(etay[n]-miny)/rangey)
    shape = [(x0[n], y0[n]), (x, y)]
    red  = int(255*0.9*abs(np.sin((n+1)*0.00100*k)))
    green= int(255*0.6*abs(np.sin((n+2)*0.00075*k)))
    blue = int(255*abs(np.sin((n+3)*0.00150*k)))

    if k>=start:
      # draw line from (x0[n],y0[n]) to (x_new,y_new)
      draw.line(shape, fill =(red,green,blue), width = 1)

  if k>=start and k%r==0:
    fname='imgpy'+str(count)+'.png'
    count=count+1
    # anti-aliasing mechanism
    img2 = img.resize((width // 2, height // 2), Image.LANCZOS) #ANTIALIAS)
    # output curent frame to a png file
    img2.save(fname)     # write png image on disk
    flist.append(fname)  # add its filename (fname) to flist
    images.append(img2)  # to produce Gif image

# output video file
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=20) 
clip.write_videofile('riemann.mp4')


