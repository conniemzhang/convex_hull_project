import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.cm as cm

def generate_targets(num, range_x, range_y, clustered = False):
    if clustered == False:
        targets = [None] * num
        for i in range(num):
            x = np.random.random() * range_x
            y = np.random.random() * range_y
            targets[i] = [x, y]
            i += 1
        return targets
    else:
        centers = [(10, 10), (5, 5), (0,10)]
        cluster_std = [0.6, 1, 0.5]

        targets, Y = make_blobs(n_samples=num, cluster_std=cluster_std, centers=centers, n_features=2, random_state=4)
        return targets

def calculate_hulls(targets, output = []):
    # returns array of points in the hull
    print("calculate_hulls")
    def turn(p1, p2, p3):
        return (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


    def sort_by_angle(targets):
        p0 = targets[np.argmin(targets[:,1])]
        # create matrix with [x, y, polar angle to p0]
        sorted_targets = np.empty([targets.shape[0], targets.shape[1] + 1])
        for i, point in enumerate(targets):
            u = [1,0]
            v = point - p0
            angle = 0
            if v[0] != 0 or v[1] != 0 :
                angle = spatial.distance.cosine(u, v)
            sorted_targets[i] = [point[0], point[1], angle]
        return np.array(sorted(sorted_targets, key=lambda x: x[2]))

    sorted_targets = sort_by_angle(targets)
    hull = []
    spares = []
    d = 2 # max distance between points
    for p1 in sorted_targets:
        print("p1 - ", p1)
        if len(hull) > 0 and np.linalg.norm(p1 - hull[-1]) > d:
            print("appending to spares")
            spares.append(p1)
        else:
            print("appending to hull")
            while len(hull) > 1 and turn(hull[-2], hull[-1], p1) < 0:
                print("popping")
                hull.pop()
            hull.append(p1)

    hull.append(sorted_targets[0])
    return hull, [[spare[0], spare[1]] for spare in spares]

def multi_hull(targets):
    hull, spares = calculate_hulls(targets)
    hullset = [] # a LIST of NUMPY arrays
    hullset.append(np.array(hull))
    while len(spares) != 0:
        hull, spares = calculate_hulls(np.array(spares))
        hullset.append(np.array(hull))
    return hullset

def plotme(targets, hulls):
    # target = np.array
    # hulls = [[np.array], [np.array], ...]
    fig, axes = plt.subplots(1, 1)
    axes.set_xlim(-2, 15)
    axes.set_xlim(-2, 15)
    axes.set(title = 'Single Convex Hull Plot')
    axes.plot(targets[:, 0], targets[:,1], 'bo')

    color = cm.rainbow(np.linspace(0, 1, len(hulls)))
    for i, hull in enumerate(hulls):
        axes.plot(hull[:, 0], hull[:,1], 'ro-', c=color[i], alpha = 0.5)
    plt.show()

if __name__ == '__main__':

    range_gx = 15
    range_gy = 15
    axis_range = range_gx * 1.8 #adds buffer so you can see all the hulls.
    targets2 = np.array(generate_targets(50, range_gx, range_gy, clustered = True))
    #targets2 = np.loadtxt('testbasic.txt', delimiter="\t")
    hull2 = multi_hull(targets2)
    #hull2 = np.array(multi_hull(targets2))

    plotme(targets2, hull2)
