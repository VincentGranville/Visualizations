# atoms.py
# Generating and videolizing agglomerative processes

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import moviepy.video.io.ImageSequenceClip

N      = 10000   # initial number of particles (hydrogen atoms) 
n_iter = 90000   # number of iterations
limit  = 100     # max number of electrons/atom allowed
mode   = 'n_collisions'  # options: 'n_collisions' or 'time'
yaxis  = 'variable'      # options: 'fixed' or 'variable'
show_last_frame = False  # options: True or False
seed   = 533
np.random.seed(seed)

def sample_size(pvals):
    u = np.random.uniform()
    k = 0
    cdf_val = pvals[0]
    while cdf_val < u:
        k = k + 1
        cdf_val = cdf_val + pvals[k] 
    return(k)

def my_plot_init():
    # produces professional-looking plots
    axes = plt.axes()
    [axx.set_linewidth(0.2) for axx in axes.spines.values()]
    axes.margins(x=0)
    axes.margins(y=0)
    axes.tick_params(axis='both', which='major', labelsize=7)
    axes.tick_params(axis='both', which='minor', labelsize=7)
    return()

def save_image(fname,frame):
    global fixedSize
    plt.savefig(fname, bbox_inches='tight')    
    # make sure each image has same size and size is multiple of 2
    # required to produce a viewable video   
    im = Image.open(fname)
    if frame == 0:  
        # fixedSize determined once for all in the first frame
        width, height = im.size
        width=2*int(width/2)
        height=2*int(height/2)
        fixedSize=(width,height)
    im = im.resize(fixedSize) 
    im.save(fname,"PNG")
    return()

def get_summary_stats(atom_sizes):
    n = len(atom_sizes)
    min = -1
    wsum = 0
    weight = 0
    for k in range(n):    # k is the atom size
        if atom_sizes[k] > 0: 
            if min == -1:
                min = k   # minimum size
            max = k       # maximum size
            wsum += k * atom_sizes[k]
            weight += atom_sizes[k]
    mean = wsum / weight  # average size 
    return(min, max, mean)

n_frames = 0
atom_sizes = np.zeros(limit+1) 
atom_sizes[1] = N
N_0 = N
t   = 0.0
t_last = 0.0
n_collisions = 0
n_collisions_last = 0
x_axis = np.linspace(0,limit,len(atom_sizes))
my_dpi = 300          # dots per each for images and videos 
width  = 2400         # image width
height = 1800         # image height
flist = []            # list image filenames for video
arr_time  = []        # list of times (indexed by video frame)
arr_min   = []        # min atom size (indexed by video frame)
arr_max   = []        # max atom size (indexed by video frame)
arr_mean  = []        # mean atom size (indexed by video frame)
arr_n_collisions = [] # number of collisions (indexed by video frame)

for iter in range(n_iter):
    # collision between one atom with k electrons, and one with l electrons
    t = t + N_0 / N         # time of collision
    pvals = atom_sizes / N 
    k = sample_size(pvals)
    aux = atom_sizes.copy()
    aux[k] = aux[k] - 1      # must be >= 0
    pvals = aux /(N - 1)
    l = sample_size(pvals)
    if k + l <= limit and N > 1:
        n_collisions += 1
        atom_sizes[k] = atom_sizes[k] - 1   # must be >= 0
        atom_sizes[l] = atom_sizes[l] - 1   # must be >= 0
        atom_sizes[k+l] = atom_sizes[k+l] + 1
        N = N - 1
    show_image = False
    if mode == 'time':
        if t - t_last > 2000 and time > 5000:
            show_image = True
            t_last = t
    elif mode == 'n_collisions':
        if n_collisions - n_collisions_last > 20 and n_collisions > -1:
            show_image = True
            n_collisions_last = n_collisions
    if show_last_frame and iter == n_iter - 1:
       show_image = True   
    if show_image:
        pvals = atom_sizes / N
        my_plot_init()
        plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)
        if yaxis == 'fixed':
            if n_frames == 0:
                y_axis_lim = max(pvals)
            plt.ylim(0, y_axis_lim)
        plt.bar(x_axis, pvals)
        fname='histo_frame'+str(n_frames)+'.png'
        flist.append(fname)
        save_image(fname,n_frames)
        n_frames += 1 
        (min, max, mean) = get_summary_stats(atom_sizes) 
        print("Frame:%4d Time:%6.0f Size: min=%3d max=%3d mean =%8.4f" %  
             (n_frames, t, min, max, mean))
        arr_time.append(t)
        arr_min.append(min)
        arr_max.append(max)
        arr_mean.append(mean)
        arr_n_collisions.append(n_collisions) 
        plt.close()

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=10)
clip.write_videofile('histo.mp4')

plt.close()
my_plot_init()
plt.ylim(0,max+2)
plt.plot(arr_time,arr_max, linewidth=0.4)
plt.plot(arr_time,arr_mean, linewidth=0.4)
plt.show()
plt.close()

my_plot_init()
plt.plot(arr_time,arr_n_collisions, linewidth=0.4)
plt.show()
plt.close()
