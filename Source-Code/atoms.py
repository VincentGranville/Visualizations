# atoms.py
# Generating and videolizing agglomerative processes

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import moviepy.video.io.ImageSequenceClip

N       = 8000    # initial number of particles (hydrogen atoms) 
n_iter  = 9000    # number of iterations (time)
limit   = 50      # max number of electrons/atom allowed
N_simul = 100     # number of systems (atom configurations) running in parallel
max_trials = 1    # trials allowed until 1 collision happens
seed = 87
np.random.seed(seed)

atom_sizes = np.zeros((N_simul,limit+1))
collisions = np.zeros(N_simul)
arr_N = []
arr_t = []
N_0 = N
for simul in range(N_simul):
    atom_sizes[(simul,1)] = N
    arr_N.append(N)
    arr_t.append(0.0)

def sample_size(pvals):
    u = np.random.uniform()
    k = 0
    cdf_val = pvals[0]
    while cdf_val < u:
        k = k + 1
        cdf_val = cdf_val + pvals[k] 
    return(k)

def my_plot_init(plt):
    # produces professional-looking plots
    axes = plt.axes()
    [axx.set_linewidth(0.2) for axx in axes.spines.values()]
    axes.margins(x=0)
    axes.margins(y=0)
    axes.tick_params(axis='both', which='major', labelsize=12)
    axes.tick_params(axis='both', which='minor', labelsize=12)
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

def get_summary_stats(pvals):
    min  = -1
    mean = 0
    for k in range(limit+1):    # k is the atom size
        if pvals[k] > 0: 
            if min == -1:
                min = k   # minimum size
            max = k       # maximum size
            mean += k * pvals[k]
    return(min, max, mean)


#---
mode   = 'atom_size'  # options: 'n_collisions', 'time' or 'atom_size'
yaxis  = 'variable'      # options: 'fixed' or 'variable'
show_last_frame = False  # options: True or False
n_frames = -1
t_last = 0.0
n_collisions_last = 0
mean_last = 1
my_dpi = 300          # dots per each for images and videos 
width  = 2400         # image width
height = 1800         # image height
flist = []            # list image filenames for video
history_time = []
history_min  = []     # min atom size over time
history_max  = []     # max atom size over time
history_mean = []     # mean atom size over time
history_collisions = [] 

for iter in range(n_iter+1):

    #-- core of the algorithm (agglomeration)
    for simul in range(N_simul):
        old_N = arr_N[simul]
        trial = 0
        while old_N == arr_N[simul] and trial < max_trials:  
            arr_t[simul] += N_0/arr_N[simul]
            pvals = np.copy(atom_sizes[simul,:])
            pvals = pvals / old_N 
            k = sample_size(pvals)
            aux = np.copy(atom_sizes[simul,:])
            aux[k] = aux[k] - 1      # must be >= 0
            pvals = aux /(old_N - 1)
            l = sample_size(pvals)
            if k + l <= limit and N > 1:
                atom_sizes[(simul,k)] = atom_sizes[(simul,k)] - 1   # must be >= 0
                atom_sizes[(simul,l)] = atom_sizes[(simul,l)] - 1   # must be >= 0
                atom_sizes[(simul,k+l)] = atom_sizes[(simul,k+l)] + 1
                arr_N[simul] = old_N - 1
                collisions[simul] += 1
            trial +=1 

    #-- compute summary stats across the N_simul simulations and over time        
    pvals = np.zeros(limit+1)
    for k in range(limit+1):
        for simul in range(N_simul):
            pvals[k] += atom_sizes[simul,k]/arr_N[simul]
        pvals[k] /= N_simul  # proba a particle (atom) is of size k
    mean_time = np.mean(arr_t)
    mean_collisions = np.mean(collisions)
    (min, max, mean) = get_summary_stats(pvals)  
    print("Frame:%4d Iteration:%6d Time:%6.0f Mean size:%6.2f" 
         %  (n_frames, iter, mean_time, mean))
    history_time.append(mean_time)
    history_min.append(min)
    history_max.append(max)
    history_mean.append(mean)
    history_collisions.append(mean_collisions) 

    #-- visualizations 
    show_image = False
    if mode == 'time':
        if mean_time - t_last > 20 and mean_time > 50:
            show_image = True
            t_last = mean_time
    elif mode == 'n_collisions':
        if mean_collisions - n_collisions_last > 30 and mean_collisions > 500:  # 9000, 20, -1
            show_image = True
            n_collisions_last = mean_collisions
    elif mode == 'atom_size':
        if mean - mean_last > 0.1: 
            show_image = True
            mean_last = mean
    if show_last_frame and iter == n_iter - 1:
       show_image = True   
    if show_image:
        if n_frames == -1:
            n_frames = 0
        plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)
        my_plot_init(plt)
        if yaxis == 'fixed':
            if n_frames == 0:
                y_axis_lim = max(pvals)
            plt.ylim(0, y_axis_lim)
        x_axis = np.linspace(0,limit,limit+1)
        plt.bar(x_axis[1:], pvals[1:])
        fname='histo_frame'+str(n_frames)+'.png'
        flist.append(fname)
        save_image(fname,n_frames)
        n_frames += 1 
        plt.close()
    
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=10)
clip.write_videofile('histo.mp4')
    
plt.close()
my_plot_init(plt)
plt.ylim(0,max+2)
plt.plot(history_time,history_max, linewidth=0.4)
plt.plot(history_time,history_mean, linewidth=0.4)
plt.show()
plt.close()

my_plot_init(plt)
plt.plot(history_time,history_collisions, linewidth=0.4)
plt.show()
plt.close()
