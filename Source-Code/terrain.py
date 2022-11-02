# A Clean Implementation of the Diamond-Square Terrain Generating Algorithm

import random
import numpy as np

def fixed( d, i, j, v, offsets ):
    # For fixed bdries, all cells are valid. Define n so as to allow the
    # usual lower bound inclusive, upper bound exclusive indexing.
    n = d.shape[0]
    
    res, k = 0, 0
    for p, q in offsets:
        pp, qq = i + p*v, j + q*v
        if 0 <= pp < n and 0 <= qq < n:
            res += d[pp, qq]
            k += 1.0
    return res/k

def periodic( d, i, j, v, offsets ):
    # For periodic bdries, the last row/col mirrors the first row/col.
    # Hence the effective square size is (n-1)x(n-1). Redefine n accordingly!
    n = d.shape[0] - 1
    
    res = 0
    for p, q in offsets:
        res += d[(i + p*v)%n, (j + q*v)%n]
    return res/4.0

def update_random_table(rnd_table, s, frame):

    global counter

    if distribution == 'Uniform' and mode == 'Blending':
        print("Error: Blending allowed only with Gaussian distribution.")
        exit()

    if frame < 1: 
        if distribution == 'Gaussian':
            rnd_table[counter]=random.gauss(0,s)
        elif distribution == 'Uniform':
            rnd_table[counter]=random.uniform(-s,s) 
    else:
        if random.uniform(0,1) > 1 - jump:
            if mode == 'Blending':
                rnd_table[counter] += weight*random.gauss(0,s) # update random number table  # 0.5 * ..
                rnd_table[counter] /= np.sqrt(1+weight*weight)
            elif mode == 'Mixture':
                if distribution == 'Gaussian':
                    rnd_table[counter] = random.gauss(0,s)
                elif distribution == 'Uniform':
                    rnd_table[counter] = random.uniform(-s,s)  

def single_diamond_square_step(d, w, s, avg, frame):
    # w is the dist from one "new" cell to the next
    # v is the dist from a "new" cell to the nbs to average over

    global counter
    n = d.shape[0]
    v = w//2
    
    # offsets:
    diamond = [ (-1,-1), (-1,1), (1,1), (1,-1) ]
    square = [ (-1,0), (0,-1), (1,0), (0,1) ]

    # (i,j) are always the coords of the "new" cell

    # Diamond Step
    for i in range( v, n, w ):
        for j in range( v, n, w ):
            update_random_table(rnd_table, s, frame)
            d[i, j] = avg( d, i, j, v, diamond ) + rnd_table[counter]
            counter=counter+1

    # Square Step, rows
    for i in range( v, n, w ):
        for j in range( 0, n, w ):
            update_random_table(rnd_table, s, frame)
            d[i, j] = avg( d, i, j, v, square ) + rnd_table[counter] 
            counter=counter+1

    # Square Step, cols
    for i in range( 0, n, w ):
        for j in range( v, n, w ):
            update_random_table(rnd_table, s, frame)
            d[i, j] = avg( d, i, j, v, square ) + rnd_table[counter] 
            counter=counter+1
            
def make_terrain( n, ds, bdry, frame):
    # Returns an n-by-n landscape using the Diamond-Square algorithm, using
    # roughness delta ds (0..1). bdry is an averaging fct, including the
    # bdry conditions: fixed() or periodic(). n must be 1+2**k, k integer.
    
    global counter

    d = np.zeros( n*n ).reshape( n, n )
   
    w, s = n-1, 1.0
    counter = 0
    while w > 1:
        single_diamond_square_step(d, w, s, bdry, frame)

        w //= 2
        s *= ds

    return d

def set_palette(palette): 
    # Create a colormap  (palette with ordered RGB colors)

    color_table_storm = [] 
    for k in range(0,29):  
        color_table_storm.append([k/29, k/29, k/29])

    color_table_terrain = [
            (0.44314, 0.67059, 0.84706),
            (0.47451, 0.69804, 0.87059),
            (0.51765, 0.72549, 0.89020),
            (0.55294, 0.75686, 0.91765),
            (0.58824, 0.78824, 0.94118),
            (0.63137, 0.82353, 0.96863),
            (0.67451, 0.85882, 0.98431),
            (0.72549, 0.89020, 1.00000),
            (0.77647, 0.92549, 1.00000),
            (0.84706, 0.94902, 0.99608),
            (0.67451, 0.81569, 0.64706),
            (0.58039, 0.74902, 0.54510),
            (0.65882, 0.77647, 0.56078),
            (0.74118, 0.80000, 0.58824),
            (0.81961, 0.84314, 0.67059),
            (0.88235, 0.89412, 0.70980),
            (0.93725, 0.92157, 0.75294),
            (0.90980, 0.88235, 0.71373),
            (0.87059, 0.83922, 0.63922),
            (0.82745, 0.79216, 0.61569),
            (0.79216, 0.72549, 0.50980),
            (0.76471, 0.65490, 0.41961),
            (0.72549, 0.59608, 0.35294),
            (0.66667, 0.52941, 0.32549),
            (0.67451, 0.60392, 0.48627),
            (0.72941, 0.68235, 0.60392),
            (0.79216, 0.76471, 0.72157),
            (0.87843, 0.87059, 0.84706),
            (0.96078, 0.95686, 0.94902)
    ]
    if palette == 'Storm':
        color_table = color_table_storm
    elif palette == 'Terrain':
        color_table = color_table_terrain
    return(color_table)

def morphing(start, end):
    # create all the images for the video
    # morphing from 'start' to 'end' image
    
    size = (n - 1) / 64 

    random.seed(start)
    frame=0
    start_terrain = make_terrain( n, ds, bdry, frame)
    random.seed(end)
    frame=-1
    end_terrain = make_terrain( n, ds, bdry, frame)
    if col_morphing:
        col_table_start=np.array(set_palette('Storm'))
        col_table_end=np.array(set_palette('Terrain'))

    for frame in range(0,Nframes): 
        A = frame/(Nframes - 1)
        B = 1 - A
        tmp_terrain = B * start_terrain + A * end_terrain
        if col_morphing:    # both palettes must have same size
            tmp_col_table = B * col_table_start + A * col_table_end  
            tmp_cm = matplotlib.colors.LinearSegmentedColormap.from_list('temp',tmp_col_table)
        else:
            tmp_cm = cm
        image='terrain'+str(frame)+'.png' # filename of image in current frame
        print("Creating image",image) # show progress on the screen
        plt.figure( figsize=(size, size), dpi=my_dpi ) # create n-by-n pixel fig
        plt.tick_params( left=False, bottom=False, labelleft=False, labelbottom=False )
        plt.imshow( tmp_terrain, cmap=tmp_cm )
        plt.savefig(image)  # Save to file
        plt.close()
        flist.append(image)   

def evolution(start):
    # create all the images for the video
    
    random.seed(start) 
    for frame in range(0,Nframes): 
        image='terrain'+str(frame)+'.png' # filename of image in current frame
        print("Creating image",image) # show progress on the screen
        size = (n - 1) / 64 
        plt.figure( figsize=(size, size), dpi=my_dpi ) # create n-by-n pixel fig
        plt.tick_params( left=False, bottom=False, labelleft=False, labelbottom=False )
        terrain = make_terrain( n, ds, bdry, frame )
        plt.imshow( terrain, cmap=cm )
        plt.savefig(image)  # Save to file
        plt.close()
        flist.append(image)  

#--- Main

import matplotlib.colors
import matplotlib.pyplot as plt
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video


n            = 1 + 2**9     # Edge size of the resulting image in pixels
ds           = 0.7          # Roughness delta, 0 < ds < 1 : smaller ds => smoother results
bdry         = periodic     # One of the averaging routines: fixed or periodic
Nframes      = 40           # must be > 10
my_dpi       = 300          # dots per inch (image resolution)
fps          = 1            # frames per second
mode         = 'Mixture'    # options: 'Blending' or 'Mixture'
jump         = 0.05         # the lower, the smoother the image transitions (0 < jump < 1) 
weight       = 0.5          # used in Gaussian mixture: low weight keeps pixel color little changed
start        = 134          # seed for random number generator, for initial image
end          = 143          # seed for target image, used in morphing only
distribution = 'Uniform'    # option: 'Gaussian' or 'Uniform'
palette      = 'Terrain'    # options: 'Storm' or 'Terrain'
method       = 'Evolution'  # options: 'Morphing' or 'Evolution'
col_morphing = False        # available in morphing method only

flist     = []              # list of image filenames for the video
rnd_table = {}              # dynamic list of random numbers for simulations 

color_table = set_palette(palette)
cm = matplotlib.colors.LinearSegmentedColormap.from_list('geo-smooth',color_table)

if method == 'Evolution':
    evolution(start)
elif method == 'Morphing':
    morphing(start,end)

# output video 
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=fps) 
clip.write_videofile('terrain.mp4')
        
