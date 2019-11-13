import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
import scipy.spatial as spatial
from matplotlib.animation import FuncAnimation


range_gx = 15
range_gy = 15
axis_range = range_gx * 1.8 #adds buffer so you can see all the hulls.

# generate num targets. (0,0) is bottom left.
def generate_targets(num, range_x, range_y):
    targets = [None] * num
    i = 0
    while i < num:
        x = np.random.random() * range_x
        y = np.random.random() * range_y
        targets[i] = [x, y]
        i += 1
    return targets

# graham scan
def calculate_hulls(targets):
	# returns array of points in the hull
	# stack goes [last][][][][][first]
	stack = []


	#find point with lowest y
	p0 = find_p0(targets)
	sorted_targets = np.array(sort(p0, targets))
	print("sorted targets", sorted_targets)

	# pop the last point from the stack if we turn clockwise to reach this point
	for point in targets:
		p2, p3, cross = None, None, -1
		p1 = point
		if len(stack) > 1:
			p2 = stack[-1]
			p3 = stack[-2]
			cross = np.cross(p1 - p2, p1 - p3)

		while len(stack) > 1 and cross > 0:
			stack.pop()
		stack.append(point)
	return np.array(stack)

def find_p0(targets):
	mindex = np.argmin(targets, axis = 0)
	return targets[mindex[1]]

def sort(p0, targets):
	# create matrix with targets, polar angle to p0
	sorted_targets = np.empty([targets.shape[0], targets.shape[1] + 1])
	print("sorted targets shape", sorted_targets.shape)
	i = 0
	for i, point in enumerate(targets):
		angle = spatial.distance.cosine(p0, point)
		sorted_targets[i] = [point[0], point[1], angle]

	return sorted(sorted_targets, key=lambda x: x[2])


def plotme(ax, targets, hull):
	ax.set(title = 'Convex Hull Plot')
	ax.set_xlim(0, 15)
	ax.set_xlim(0, 15)
	ax.plot(targets[:, 0], targets[:,1], 'bo')
	ax.plot(hull[:, 0], hull[:,1], 'ro-')
	print()
	plt.show()

if __name__ == '__main__':
	fig, ax = plt.subplots(1, 1)
	targets = np.array(generate_targets(50, range_gx, range_gy))
	hull = calculate_hulls(targets)
	print("hull", hull)
	plotme(ax, targets, hull)
