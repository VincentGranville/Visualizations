import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

plt.rcParams['lines.linewidth']= 0.5
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['axes.linewidth'] = 0.5
 
SMALL_SIZE  = 6
MEDIUM_SIZE = 8
BIGGER_SIZE = 10

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")   
X, Y = np.mgrid[-3:3:30j, -3:3:30j]
Z= np.exp(-(abs(X)**2 + abs(Y)**2)) + 0.8*np.exp(-4*((abs(X-1.5))**4.2 + (abs(Y-1.4))**4.2))

ax.plot_surface(X, Y, Z, cmap="coolwarm", rstride=1, cstride=1, alpha=0.2)
# ax.contourf(X, Y, Z, levels=60, colors="k", linestyles="solid", alpha=0.9, antialiased=True) 
ax.contour(X, Y, Z, levels=60, linestyles="solid", alpha=0.9, antialiased=True) 

plt.savefig('contour3D.png', dpi=300)
plt.show()
