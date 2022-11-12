import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video

def getAcc( pos, mass, G, law, softening ):

    # Calculate the acceleration on each particle due to Newton's Law 
    # pos  is an N x 3 matrix of positions
    # mass is an N x 1 vector of masses
    # G is Newton's Gravitational constant
    # softening is the softening length
    # a is N x 3 matrix of accelerations

    # positions r = [x,y,z] for all particles
    x = pos[:,0:1]
    y = pos[:,1:2]
    z = pos[:,2:3]

    # matrix that stores all pairwise particle separations: r_j - r_i
    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    # matrix that stores 1/r^(law) for all particle pairwise particle separations 
    inv_r3 = np.sqrt(dx**2 + dy**2 + dz**2 + softening**2)
    inv_r3 = inv_r3**(-law)  

    ax = G * (dx * inv_r3) @ mass
    ay = G * (dy * inv_r3) @ mass
    az = G * (dz * inv_r3) @ mass
    
    # pack together the acceleration components
    a = np.hstack((ax,ay,az))
    return a
    
#--- main
    
# Simulation parameters
N         = 100     # Number of particles
t         = 0       # current time of the simulation
tEnd      = 20.0    # time at which simulation ends
dt        = 0.01    # timestep
softening = 0.1     # softening length
G         = 1       # Newton's Gravitational Constant
starBoost = -30     #  create one massive star in the system, if starBoost > 1 or < -1 
law       = 0.5     # exponent in denominator, gravitation law (should be set to 3) 
## -3 ### compare with 3 orbits RH // try -0.5 ## 4 videos in one video
speed     = 0.2     # high initial speed, above 'escape velocity', results in dispersion
zoom      = 40      # output on [-zoom, zoom] x [-zoom, zoom ] image
seed      = 58      # set the random number generator seed
adjustVel = False 
negativeMass = True
expand    = 1.0     # enlarge window over time if expand > 0 
fps       = 20      # frames per second in video
my_dpi    = 240     # dots per inch in video
createVideo = True
    
# Generate Initial Conditions
np.random.seed(seed)            
if negativeMass:  
    mass = 1.25 + 0.75*np.random.randn(N,1) 
else:
    mass = np.random.exponential(2.0,(N,1))
adjustedMass = mass
if starBoost > 1 or starBoost < 0:
    mass[0]= starBoost * np.max(abs(mass))
col=[]  # bodies with positive mass in blue; other ones in red
for k in range(N):
    if mass[k] > 0:
        col.append('blue')
    else:
        col.append('red')
pos  = np.random.randn(N,3)   # randomly selected positions and velocities
vel  = speed * np.random.randn(N,3)  
    
# Convert to Center-of-Mass frame
if adjustVel:
    for k in range(N):
        vel[k] -= np.mean(abs(mass[k]) * vel[k]) / np.mean(abs(mass))
    
# calculate initial gravitational accelerations
acc = getAcc( pos, mass, G, law, softening )
    
# number of timesteps (or frames in the video)
Nt = int(np.ceil(tEnd/dt))  
        
# prep figure
fig = plt.figure(figsize=(4,5),dpi=80) 
ax1 = fig.gca()    # or ax1 = plt.subplot() ??  
plt.setp(ax1.spines.values(), linewidth=0.1)
plt.rc('xtick', labelsize=5)    # fontsize of the tick labels
plt.rc('ytick', labelsize=5)    # fontsize of the tick labels
ax1.xaxis.set_tick_params(width=0.1)
ax1.yaxis.set_tick_params(width=0.1)

flist=[] # list of image filenames for the video

if Nt > 2000:
    print("About to generate", Nt, "images.")
    answer = input ("Type y to proceed: ")
    if answer != 'y':
        exit()

# Simulation Main Loop
for frame in range(Nt): 
        
    vel += acc * dt/2.0 # (1/2) kick
    pos += vel * dt # drift
    acc = getAcc( pos, mass, G, law, softening ) # update accelerations
    vel += acc * dt/2.0 # (1/2) kick
    t += dt  # update time
                
    image='nbody'+str(frame)+'.png'   # filename of image in current frame
    if frame % 10 == 0:
        print("Creating image",image) # show progress on the screen

    plt.sca(ax1)
    plt.cla()
    centroid = np.zeros(3)
    totalMass=np.sum(abs(mass))
    for k in range(N):
        centroid += abs(mass[k]) * pos[k] / totalMass 
    adjustedMass /= (1.0 + expand/Nt)
    plt.scatter(pos[:,0]-centroid[0],pos[:,1]-centroid[1],s=abs(adjustedMass),color=col)
    zoom *= (1.0 + expand/Nt) 
    ax1.set(xlim=(-zoom, zoom), ylim=(-zoom, zoom)) 
    ax1.set_aspect('equal', 'box')          
    if createVideo and frame>0:
        # plt.axis('off')
        plt.savefig(image,bbox_inches='tight',pad_inches=0.2,dpi=my_dpi)          
        im = Image.open(image)
        if i==1:  
            width, height = im.size
            width=2*int(width/2)
            height=2*int(height/2)
            fixedSize=(width,height)
        im = im.resize(fixedSize) 
        im.save(image,"PNG")
        flist.append(image)   
    plt.pause(0.001)
            
# output video / fps is number of frames per second
if createVideo:
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=fps) 
    clip.write_videofile('nbody.mp4')
