import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial
from sklearn.datasets.samples_generator import make_blobs

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
        centers = [(10, 10), (5, 5)]
        cluster_std = [0.8, 1]

        targets, Y = make_blobs(n_samples=num, cluster_std=cluster_std, centers=centers, n_features=2, random_state=1)
        return targets

def calculate_hulls(targets):
    # returns array of points in the hull
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
    for p1 in sorted_targets:
        while len(hull) > 1 and turn(hull[-2], hull[-1], p1) < 0:
            hull.pop()
        hull.append(p1)
    hull.append(sorted_targets[0])
    return np.array(hull)


def plotme(ax, targets, hull):
    ax.set(title = 'Convex Hull Plot')
    ax.set_xlim(-2, 15)
    ax.set_xlim(-2, 15)
    ax.plot(targets[:, 0], targets[:,1], 'bo')
    ax.plot(hull[:, 0], hull[:,1], 'ro-')
    plt.show()

if __name__ == '__main__':
    fig, ax = plt.subplots(1, 1)

    range_gx = 15
    range_gy = 15
    axis_range = range_gx * 1.8 #adds buffer so you can see all the hulls.
    #targets = np.array(generate_targets(50, range_gx, range_gy, clustered = True))
    targets = np.loadtxt('testbasic.txt', delimiter="\t")
    hull = calculate_hulls(targets)
    print("hull", hull)
    plotme(ax, targets, hull)
