import numpy as np
from skimage.measure import EllipseModel, CircleModel
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt


def ellipse_fitting(points):
    #points = [(339.65, 195.013), (291.77, 240.5), (319.3, 288.38), (371.97, 275.21), (377.95, 220.15)]

    a_points = np.array(points)
    #x = a_points[:, 0]
    #y = a_points[:, 1]

    ell = EllipseModel()
    ell.estimate(a_points)

    return ell.params
    #xc, yc, a, b, theta = ell.params

    #print("center = ",  (xc, yc))
    #print("angle of rotation = ",  theta)
    #print("axes = ", (a,b))

    #fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
    #axs[0].plot(x,y)

    #axs[1].plot(x, y)
    #axs[1].scatter(xc, yc, color='red', s=100)
    #axs[1].set_xlim(x.min(), x.max())
    #axs[1].set_ylim(y.min(), y.max())

    #ell_patch = Ellipse((xc, yc), 2*a, 2*b, theta*180/np.pi, edgecolor='red', facecolor='none')

    #axs[1].add_patch(ell_patch)
    #plt.show()
    #return None

def circle_fitting(points):
    a_points = np.array(points)
    cir = CircleModel()
    cir.estimate(a_points)

    return cir.params




