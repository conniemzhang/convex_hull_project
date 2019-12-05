import math
import numpy as np
import matplotlib.cm as cm
import scipy.spatial as spatial
import matplotlib.pyplot as plt

class MultiHull():
    def __init__(self, targets, robots=[]):
        self.targets = targets
        self.robots = robots
        self.hullset = self.multi_hull(targets)

        self.size = len(targets)


    def __calculate_hulls(self, targets, output = []):
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
        spares = []
        d = 2 # max distance between points
        for p1 in sorted_targets:
            if len(hull) > 0 and np.linalg.norm(p1 - hull[-1]) > d:
                spares.append(p1)
            else:
                while len(hull) > 1 and turn(hull[-2], hull[-1], p1) < 0:
                    hull.pop()
                hull.append(p1)

        hull.append(sorted_targets[0])
        return hull, [[spare[0], spare[1]] for spare in spares]

    def multi_hull(self, targets):
        hull, spares = self.__calculate_hulls(targets)
        hullset = [] # a LIST of NUMPY arrays
        hullset.append(np.array(hull))
        while len(spares) != 0:
            hull, spares = self.__calculate_hulls(np.array(spares))
            hullset.append(np.array(hull))
        return hullset

    def update_hulls(self, targets = []):
        new_hullset = self.multi_hull(self.targets)
        return new_hullset


""" for in-house testing """
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
    targets = np.random.rand(10, 2) * 3
    test = MultiHull(targets)
    test.update_hulls()
    plotme(targets, test.hullset)
    print("hullset")
    print(test.hullset)
