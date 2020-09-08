# importing the required module 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt 
  
slam_stats = open("src/MAV_apps/data/package_delivery/stats.txt", "r")
stats = slam_stats.readlines()
for i in range(len(stats)):
	stats[i] = stats[i].strip('\t')
	stats[i] = stats[i].strip('\n')

ind = stats.index('RPE per pose: ')
gtpos_ind = stats.index('ground truth position: ')
slampos_ind = stats.index('slam position: ')

gtp = stats[gtpos_ind+1:slampos_ind]
sp = stats[slampos_ind+1:-1]
gmat = np.zeros((len(gtp), 3))
smat = np.zeros((len(sp), 3))
for i in range(len(gtp)):
	d = gtp[i].split()
	for j in range(len(d)):
		gmat[i, j] = float(d[j].strip('(),'))
	
for i in range(len(sp)):
	d = sp[i].split()
	for j in range(len(d)):
		smat[i, j] = float(d[j].strip('(),'))

rpe_tot = float(stats[ind-1].split()[1])
ate_tot = float(stats[ind-2].split()[1])
print ("RPE: " + str(rpe_tot) + "\n" + "ATE: " + str(ate_tot))

rpe = stats[ind+1:gtpos_ind]
rpe.pop(-1)
rpe.pop(-1)
for i in range(len(rpe)):
	rpe[i] = float(rpe[i])
x = list(range(len(rpe)+1))
x.pop(0)
plt.figure(1)
plt.plot(x, rpe)
plt.xlabel('time (tenths of a second)')
plt.ylabel('relative pose error (m)') 
plt.title('RPE over time') 

plt.figure(2)
ax = plt.gca(projection="3d")
x, y, z = gmat[:,0], gmat[:,1], gmat[:,2]
x0, y0, z0 = smat[:,0], smat[:,1], smat[:,2]
ax.scatter(x,y,z, c='r',s=10, label='ground truth', edgecolors='r')
ax.scatter(x0,y0,z0, c='g',s=10, label='SLAM localization', edgecolors='g')
ax.plot(x,y,z, color='r')
ax.plot(x0,y0,z0, color='g')
plt.title('Trajectory Plot') 
ax.legend(frameon=False, loc='lower center', ncol=2)

plt.show()


