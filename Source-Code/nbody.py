import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video

def getAcc( pos, mass, G, law, softening, col ):

    # Calculate the acceleration on each particle due to Newton's Law 
    # pos  is an N x 3 matrix of positions
    # mass is an N x 1 vector of masses
    # G is Newton's Gravitational constant
    # softening is the softening length
    # a is N x 3 matrix of accelerations
    #
    # Also: update collisionTable

    global ncollisions

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

    # detect collisions 
    if collisions: 
        threshold = collThresh * softening**(-law)
        for i in range(N):
           for j in range(i+1,N):
               if  inv_r3[i][j] > threshold and mass[i] != 0 and mass[j] !=0:
                   print("Collision between body",i,"and",j)
                   dist=np.linalg.norm(pos[i] - centroid)  # distance to centroid
                   collData = str(ncollisions)+ " "+str(frame)+" "+str(i)+" "+str(j)
                   collData = collData + " "+col[i]+" "+col[j]
                   collData = collData +" "+str(mass[i])+" "+str(mass[j])+" "+str(dist)
                   # collData = collData +" "+str(centroid)
                   collisionTable.append(collData)
                   ncollisions += 1
                   mass[i]=mass[i]+mass[j] 
                   mass[j]=0  
                   col[i]='orange'
                   col[j]='black'

    ax = G * (dx * inv_r3) @ mass
    ay = G * (dy * inv_r3) @ mass
    az = G * (dz * inv_r3) @ mass
    
    # pack together the acceleration components
    a = np.hstack((ax,ay,az))
    return a

def vector_to_string(vector):
    # turn numpy array entry into string of tab-separated values 
    string = str(vector)
    string = " ".join(string.split()) # multiple spaces replaced by one space
    string = string.replace('[ ','').replace('[','')
    string = string.replace(' ]','').replace(']','')
    string = string.replace(' ',"\t")  ## .replace("\t\t","\t")
    return string

    
#--- main
    
# Simulation parameters
N             = 1000       # Number of stars
t             = 0          # current time of the simulation
tEnd          = 40.0       # time at which simulation ends 
dt            = 0.02       # timestep
softening     = 0.1        # softening length
G             = 0.1        # Newton's Gravitational Constant
starBoost     = 0.0        #  create one massive star in the system, if starBoost > 1 or < -1 
law           = 3          # exponent in denominator, gravitation law (should be set to 3) 
speed         = 0.8        # high initial speed, above 'escape velocity', results in dispersion
zoom          = 4          # output on [-zoom, zoom] x [-zoom, zoom ] image
seed          = 58         # set the random number generator seed
adjustVel     = False      # always True in original version
negativeMass  = False      # if true, bodies are allowed to have negative mass
collisions    = True       # if true, collisions are properly handled
collThresh    = 0.9        # < 1 and > 0.05; fewer collisions if close to 1
expand        = 2.0        # enlarge window over time if expand > 0 
origin        = 'Centroid' # options: 'Star_0', 'Zero', or 'Centroid'
threeClusters = True      # if true, generate three separate star clusters
p             = 0.0        # add one new star with proba p at each new frame if p > 0
Nstars        = 0          # if p > 0, start with Nstars; will add new stars up to N, over time        
fps           = 20         # frames per second in video
my_dpi        = 240        # dots per inch in video
createVideo   = True      # set to False for testing purposes (much faster!)
saveData      = True      # save data to nbody.txt if True (large file!)

# Handle configurations that are not supported
if threeClusters and p > 0:
    print("Error: adding new stars not supported with threeClusters set to True.")
    exit()
if Nstars >= N:
    print("Error: Nstars must be <= N.")
    exit()
    
# Generate Initial Conditions
np.random.seed(seed)            
if negativeMass:  
    mass = 1.25 + 0.75*np.random.randn(N,1) 
else:
    mass = np.random.exponential(2.0,(N,1))
adjustedMass = np.copy(mass)
if starBoost > 1 or starBoost < 0:
    mass[0]= starBoost * np.max(abs(mass))
col=[]  # bodies with positive mass in blue; other ones in red
for k in range(N):
    if mass[k] > 0:
        col.append('blue')
    else:
        col.append('red')
    if p > 0 and k >= Nstars:
        mass[k] = 0      # make room for future stars 
        col[k] = 'darkviolet'  # newly added stars appear in pink

pos  = np.random.randn(N,3)   # randomly selected positions and velocities
if threeClusters:
    for k in range(int(N/3)):
        pos[k] += [5.0, 0.0, 0.0]
        col[k] = 'green'
    for k in range(int(N/3),int(2*N/3)):
        pos[k] += [0.0, 5.0, 1.0]
        col[k] = 'magenta'
vel  = speed * np.random.randn(N,3)  
    
# Convert to Center-of-Mass frame
if adjustVel:
    for k in range(N):
        vel[k] -= np.mean(abs(mass[k]) * vel[k]) / np.mean(abs(mass))
    
# calculate initial gravitational accelerations
frame=-1
acc = getAcc( pos, mass, G, law, softening, col )
    
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

flist=[]          # list of image filenames for the video
collisionTable=[] # collision table
ncollisions=1 
                  
if Nt > 2000:
    print("About to generate", Nt, "images.")
    answer = input ("Type y to proceed: ")
    if answer != 'y':
        exit()

# Simulation Main Loop

if saveData:
    OUT=open("nbody.txt","w")

for frame in range(Nt): 
    if p > 0 and Nstars < N:  # add new star with proba p
        if np.random.uniform() < p:
            mass[Nstars] =  np.random.exponential(2.0,1)
            Nstars += 1
        
    vel += acc * dt/2.0 # (1/2) kick
    pos += vel * dt # drift
    acc = getAcc( pos, mass, G, law, softening, col ) # update accelerations
    vel += acc * dt/2.0 # (1/2) kick
    t += dt  # update time
                
    image='nbody'+str(frame)+'.png'   # filename of image in current frame
    if frame % 10 == 0:
        print("Creating image",image) # show progress on the screen

    plt.sca(ax1)
    plt.cla()
    centroid = np.zeros(3)
    totalMass=np.sum(abs(mass))
    if origin == 'Star_0':
        centroid = pos[0]
    elif origin == 'Centroid':
        for k in range(N):
            centroid += abs(mass[k]) * pos[k] / totalMass

    # save results
    if saveData:
        for k in range(N):
            line=str(frame)+"\t"+str(k)+"\t"+str(float(mass[k]))+"\t"+str(col[k])+"\t"
            string1 = vector_to_string(pos[k])
            string2 = vector_to_string(centroid)
            string3 = vector_to_string(vel[k])
            line=line+string1+"\t"+string2+"\t"+string3+"\n"
            OUT.write(line)    

    adjustedMass /= (1.0 + expand/Nt) # for visualization only
    plt.scatter(pos[:,0]-centroid[0],pos[:,1]-centroid[1],s=abs(adjustedMass),color=col)
    zoom *= (1.0 + expand/Nt) 

    ax1.set(xlim=(-zoom, zoom), ylim=(-zoom, zoom)) 
    ax1.set_aspect('equal', 'box')  
        
    if createVideo and frame>0:
        # plt.axis('off')
        plt.savefig(image,bbox_inches='tight',pad_inches=0.2,dpi=my_dpi)          
        im = Image.open(image)
        if frame == 1:  
            width, height = im.size
            width=2*int(width/2)
            height=2*int(height/2)
            fixedSize=(width,height)
        im = im.resize(fixedSize) 
        im.save(image,"PNG")
        flist.append(image)   
    plt.pause(0.001)
if saveData:
    OUT.close()

# output collision table
OUT2=open("nbody_collisions.txt","w")
for entry in collisionTable:
    OUT2.write(vector_to_string(entry)+"\n")
            
# output video / fps is number of frames per second
if createVideo:
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=fps) 
    clip.write_videofile('nbody.mp4')
