from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import sys
import numpy as np



if __name__ == "__main__":
	csv = sys.argv[1]
	data = np.loadtxt(open(csv,"rb"),delimiter=" ",skiprows=1)

	f = open(csv,'r+')
	labels = f.readlines()[0].split(" ")
	x = data[:,0]
	y = data[:,1]
	Z1 = data[:,2]
	Z2 = data[:,3]

	z = np.sqrt(np.multiply(Z1,Z2))
	
	xi = np.linspace(min(x), max(x))
	yi = np.linspace(min(y), max(y))

	X, Y = np.meshgrid(xi, yi)
	Z = griddata(x, y, z, xi, yi)


	fig = plt.figure()
	ax = fig.gca(projection='3d')

	surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.jet,
                       linewidth=1, antialiased=True)

	ax.set_zlim3d(np.min(Z), np.max(Z))

	ax.set_xlabel(labels[0])
	ax.set_ylabel(labels[1])
	ax.set_zlabel("Geometric mean of errors")

	fig.colorbar(surf)

	plt.show()
