import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as path
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


def beta_pdf(x, a, b):
    return (x**(a-1) * (1-x)**(b-1) * math.gamma(a + b)
            / (math.gamma(a) * math.gamma(b)))

# generate num targets. (0,0) is bottom left.
def generate_targets(num, range_x, range_y):
    targets = [None] * num
    i = 0
    while i < num:
        x = np.random.random((2,)) * range_x
        y = np.random.random((2,)) * range_y
        targets[i] = [x, y]
        i += 1
    return targets

def calculate_hulls():
	return None

class GrahamHull(object):
    def __init__(self, ax, targets):
        self.success = 0
        self.line, = ax.plot([], [], 'k-')
        self.x = np.linspace(0, 1, 200)
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(0, 15)
        self.ax.grid(True)

        # This vertical line represents the theoretical value, to
        # which the plotted distribution should converge.
        #self.ax.axvline(prob, linestyle='--', color='black')

    def init(self):
        self.success = 0
        self.line.set_data([], [])
        return self.line,

    def build(self):
    	#hull calculation goes here I think
    	print("building hull")
    	self._visualize()

    def _visualize(self):
        print("_visualizing")
        fig = plt.figure()
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()

        # Choose success based on exceed a threshold with a uniform pick
        if np.random.rand(1,) < self.prob:
            self.success += 1
        y = beta_pdf(self.x, self.success + 1, (i - self.success) + 1)
        self.line.set_data(self.x, y)
        
        plt.show()
        return self.line,

# Fixing random state for reproducibility
np.random.seed(19680801)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    targets = generate_targets(3, 15, 15)
    print("targets", targets)
    hull = GrahamHull(ax, targets)
    hull.build()
    anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init,
                         interval=100, blit=True)
    