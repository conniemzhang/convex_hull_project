import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

#x = np.arange(0, 2*np.pi, 0.01)
#line, = ax.plot(0, 0, 'o')
targets = [[0, 0], [0, 0.5]]
vertexplots = [plt.plot([], [], 'o')[0] for _ in range(len(targets))]


def init():  # only required for blitting to give a clean slate.
    for i,tar in enumerate(targets):
        vertexplots[i].set_ydata ([np.nan] * 1)
        vertexplots[i].set_data([tar[0]], [tar[1]])
    return vertexplots


def animate(i):
    for j, ax in enumerate(vertexplots):
        ax.set_data([np.sin(i/200) / 10], ax.get_ydata())
        print(ax.get_data())
    return vertexplots


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=2, blit=True, save_count=50)

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