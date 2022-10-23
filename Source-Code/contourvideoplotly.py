import numpy as np
import plotly.graph_objects as go
import matplotlib

def create_3Dplot(frame):

    param1=-0.15 + 0.65*(1-np.exp(-3*frame/Nframes)) # height of small hill
    param2=-1+2*frame/(Nframes-1)     # rotation, x
    param3=0.75+(1-frame/(Nframes-1))  # rotation, y
    param4=1-0.7*frame/(Nframes-1)   # rotation z 

    X, Y = np.mgrid[-3:2:100j, -3:3:100j]
    Z= 0.5*np.exp(-(abs(X)**2 + abs(Y)**2)) \
        + param1*np.exp(-4*((abs(X+1.5))**4.2 + (abs(Y-1.4))**4.2))

    fig = go.Figure(data=[
        go.Surface(
            x=X, y=Y, z=Z,
            opacity=1.0,
            contours={
                "z": {"show": True, "start": 0, "end": 1, "size": 1/60,   
                      "width": 1, "color": 'black'} # add <"usecolormap": True>
            }, 
            showscale=False,  # try <showscale=True>
            colorscale='Peach')],
    )

    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=160),
        font=dict(color='blue'),
        scene = dict(xaxis_title='', yaxis_title='',zaxis_title='',
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            aspectratio=dict(x=1, y=1, z=0.6)),                       # resize by shrinkink z
        scene_camera = dict(eye=dict(x=param2, y=param3, z=param4)))  # change vantage point  

    return(fig)

#-- main

import moviepy.video.io.ImageSequenceClip  # to produce mp4 video
from PIL import Image  # for some basic image processing

Nframes=300 # must be > 50
flist=[]    # list of image filenames for the video
w, h, dpi = 4, 3, 300 # width and heigh in inches
fps=10   # frames per second

for frame in range(0,Nframes): 
    image='contour'+str(frame)+'.png' # filename of image in current frame
    print("Creating image",image) # show progress on the screen
    fig=create_3Dplot(frame)
    fig.write_image(file=image, width=w*dpi, height=h*dpi, scale=1)
    #  fig.show()
    flist.append(image)

# output video / fps is number of frames per second
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=fps) 
clip.write_videofile('contourvideo.mp4')
