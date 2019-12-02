import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

#x = np.arange(0, 2*np.pi, 0.01)
#line, = ax.plot(0, 0, 'o')
#targets = [[0, 0], [0, 0.5]]
targets = np.random.rand(10, 2)
vertexplots = [plt.plot([], [], 'o')[0] for _ in range(len(targets))]
offset = np.linspace(0, np.pi, num = len(targets))
offset = np.random.rand(len(targets), 2) * np.pi

def datastream():
    for j, (ax, off) in enumerate(zip(vertexplots, offset)):
        ax.set_data([np.sin(i/200) / 10], ax.get_ydata())
    print(ax.get_data())

def init():  # only required for blitting to give a clean slate.
    ax.set_ylim(-4, 4)
    ax.set_xlim(-4, 4)
    for i,tar in enumerate(targets):
        vertexplots[i].set_ydata ([np.nan] * 1)
        vertexplots[i].set_data([tar[0]], [tar[1]])
    return vertexplots

def animate(i):
    #data = next(datastream())

    """for j, ax in enumerate(vertexplots):
        ax.set_data([np.sin(i/200) / 10], ax.get_ydata())
        print(ax.get_data())
    return vertexplots"""
    amp = ax.get_ylim()[0] * 0.6
    for j, (line, off) in enumerate(zip(vertexplots, offset)):
        xdata = line.get_xdata()#[amp * np.sin(i / 100)]
        ydata = [amp * np.sin(i /200 + off)]
        line.set_data(xdata, ydata)
    return vertexplots


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=4, blit=True, save_count=50)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# from matplotlib.animation import FFMpegWriter
# writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()