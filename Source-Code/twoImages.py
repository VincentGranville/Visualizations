import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import moviepy.video.io.ImageSequenceClip  # to produce mp4 video

my_dpi = 300
Nframes=100
fps=5
flist=[]

for frame in range(0,Nframes):
    image ='output'+str(frame)+'.png'
    print('Creating image',image)
    image1='terrainA'+str(frame)+'.png'    # subplot 1 (input)
    image2='terrainB'+str(frame)+'.png'  # subplot 2 (input)
    image3='terrainC'+str(frame)+'.png' # subplot 3 (input)
    image4='terrainD'+str(frame)+'.png' # subplot 4 (input)
    imgs=[]
    imgs.append(mpimg.imread(image1))
    imgs.append(mpimg.imread(image2))
    imgs.append(mpimg.imread(image3))
    imgs.append(mpimg.imread(image4))

    fig, axs = plt.subplots(2, 2,figsize=(6,6)) ## , dpi=300) # 4 4
    axs = axs.flatten()
    for img, ax in zip(imgs, axs):
        ax.set_axis_off()
        ax.set_xticklabels([])
        ax.imshow(img)
    plt.subplots_adjust(wspace=0.025, hspace=0.025)
    plt.savefig(image,bbox_inches='tight',pad_inches=0.00,dpi=my_dpi)
    plt.close()
    flist.append(image)

# output video 
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(flist, fps=fps) 
clip.write_videofile('terrainx4.mp4')

