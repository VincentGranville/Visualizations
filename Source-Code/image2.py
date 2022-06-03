from PIL import Image, ImageDraw           # ImageDraw to draw ellipses etc.
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video
from moviepy.editor import VideoFileClip   # to convert mp4 to gif
import numpy as np
import math
import random
random.seed(100)

#--- Global variables ---

m=300            # number of comets
nframe=100       # number of frames in video
ShowOrbit=False  # do not show orbit (default)

count=0          # frame counter 

count1=0
count2=0
count3=0
count4=0

width = 1600
height = 1200

a=[]
b=[]
gx=[]     # focus of ellipse (x coord.)
gy=[]     # focus of ellipse (y coord.)
theta=[]  # rotation angle of ellpise (the orbit)
v=[]      # spped of comet
tau=[]    # position of comet on the orbit path, at t = 0
col=[]    # RGB color of the comet
size=[]   # size of the comet
flist=[]  # filenames of the images representing each video frame

a=list(map(float,a))
b=list(map(float,b))
gx=list(map(float,gx))
gy=list(map(float,gy))
theta=list(map(float,theta))
v=list(map(float,v))
tau=list(map(float,tau))
flist=list(map(str,flist))

#--- Initializing comet parameters ---

for n in range (m):
  a.append(width*(0.1+0.3*random.random()))
  b.append((0.5+1.5*random.random())*a[n])
  theta.append(2*math.pi*random.random())
  tau.append(2*math.pi*random.random())
  if a[n]>b[n]:
    gyy=0.0
    gxx=math.sqrt(a[n]*a[n]-b[n]*b[n]) # should use -gxx 50% of the time
  else:
    gyy=math.sqrt(b[n]*b[n]-a[n]*a[n]) # should use -gyy 50% of the time
    gxx=0.0
  gx.append(gxx*np.cos(theta[n])-gyy*np.sin(theta[n])) 
  gy.append(gxx*np.sin(theta[n])+gyy*np.cos(theta[n])) 
  if random.random() < 0.5:
    v.append(0.04*random.random())
  else:
    v.append(-0.04*random.random())
  if abs(a[n]*a[n]-b[n]*b[n])> 0.15*width*width: 
    if abs(v[n]) > 0.03:  
    # fast comet with high eccentricity 
      red=255
      green=0
      blue=255
      count1=count1+1
    else:                 
    # slow comet with high eccentricity
      red=0
      green=255
      blue=0
      count2=count2+1
  else:
    if abs(v[n]) > 0.03:  
    # fast comet with low eccebtricity
      red=255
      green=0
      blue=0
      count3=count3+1
    else:
    # slow comet with low eccentricity
      red=255
      green=255
      blue=255
      count4=count4+1
  col.append((red,green,blue))
  if ShowOrbit:
     size.append(1)
  else: 
    if min(a[n],b[n]) > 0.3*width:  # orbit with large radius 
      size.append(8)
    else:
      size.append(4)

sunx=int(width/2)  # position of the sun (x)
suny=int(height/2) # position of the sun (y)
if ShowOrbit:
  img  = Image.new( mode = "RGB", size = (width, height), color = (0, 0, 0) )
  pix = img.load()
  draw = ImageDraw.Draw(img)
  draw.ellipse((sunx-16, suny-16, sunx+16, suny+16), fill=(255,180,0))

#--- Main Loop ---

for t in range (0,nframe,1): # loop over time, each t corresponds to a ideo frame
  print("Building frame:",t)
  if not ShowOrbit:
    img  = Image.new( mode = "RGB", size = (width, height), color = (0, 0, 0) )
    pix = img.load()
    draw = ImageDraw.Draw(img)
    draw.ellipse((sunx-16, suny-16, sunx+16, suny+16), fill=(255,180,0))
  for n in range (m):  # loop over asteroid
    x0=a[n]*np.cos(v[n]*t+tau[n]) 
    y0=b[n]*np.sin(v[n]*t+tau[n])
    x=x0*np.cos(theta[n])-y0*np.sin(theta[n])
    y=x0*np.sin(theta[n])+y0*np.cos(theta[n])
    x=int(x+width/2 -gx[n])
    y=int(y+height/2-gy[n])
    if x >= 0 and x < width and y >=0 and y < height:
      draw.ellipse((x-size[n], y-size[n], x+size[n], y+size[n]), fill=col[n]) # (255,255,255))
  count=count+1
  fname='imgpy'+str(count)+'.png'

  # ant-aliasing mechanism
  img2 = img.resize((width // 2, height // 2), Image.LANCZOS) #ANTIALIAS)

  # output curent frame to a png file
  img2.save(fname,optimize=True,quality=30)
  flist.append(fname)

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=20)

# output video file
clip.write_videofile('videopy.mp4')

videoClip = VideoFileClip("videopy.mp4")

# output gif image [converting mp4 to gif with ffmpeg compression]
videoClip.write_gif("videopy.gif",program='ffmpeg') #,fps=2)

print("count 1-4:",count1,count2,count3,count4)
