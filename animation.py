import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from HullClass import MultiHull
from matplotlib.animation import FFMpegWriter
from Robot import RobotManager

fig, ax = plt.subplots()
ax.set_ylim(-4, 4)
ax.set_xlim(-1, 4)

targets = np.random.rand(10, 2) * 3
graham = MultiHull(targets)
hulls = graham.update_hulls()
half_length = len(targets)
manager = RobotManager(num = 10)
manager.assignRobots(hulls)
print(manager.robots)
vertexplots = [plt.plot([], [], 'x')[0] for _ in range(half_length)]
hullplots = [plt.plot([], [], 'rx-', alpha=0.5)[0] for _ in range(half_length)]
robotplots = [plt.plot([], [], 'bo-', alpha=0.5)[0] for _ in range(manager.size)]
text = plt.text(3, 3.5, "# Hulls")
#offset = np.linspace(0, np.pi, num = len(targets))
offset = np.random.rand(len(targets)) * np.pi

"""def init():  # only required for blitting to give a clean slate.
    for i, tar in enumerate(targets):
        vertexplots[i].set_data([tar[0]], [tar[1]])

    for i, hur in enumerate(hulls):
        hullplots[i].set_ydata([np.nan])
        hullplots[i].set_data(hur[:,0], hur[:,1])
    return vertexplots + hullplots
    #return vertexplots, hullplots"""

def animate(frame, vertexplots, hullplots):
    global targets
    amp = ax.get_ylim()[1] * 0.6
    for j, (line, off) in enumerate(zip(vertexplots, offset)):
        xdata = line.get_xdata()#[amp * np.sin(i / 100)]
        ydata = amp * np.sin(frame /200 + off)
        #print("j", j, "xdata", xdata, "ydata", ydata, "amp", amp, "off", off)
        targets[j][0] = xdata[0]
        targets[j][1] = ydata
        line.set_data(xdata, ydata)

    for i, line in enumerate(robotplots):
        step = manager.robots[i].step()
        line.set_data(step[0], step[1])

    if frame % 20 == 0:
        #print("recalculaing hull", i)
        update = graham.update_hulls(targets)
        manager.smartAssignRobots(update)
        text.set_text("# Hulls %2d" % len(update))

        for i, hur in enumerate(update):
            hullplots[i].set_data(hur[:,0], hur[:,1])

        for j, line in enumerate(hullplots):
            xdata = line.get_xdata()#[amp * np.sin(i / 100)]
            ydata = line.get_ydata()
            line.set_data(xdata, ydata)

        for z in range(i + 1, len(hullplots)):
            print("i", i)
            hullplots[z].set_data([-50, -50], [-500, -5000])


    return vertexplots + hullplots + robotplots + [text]
    
def saveVideo():
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=3600)
    line_ani = animation.FuncAnimation(fig, animate, 1000, fargs=(vertexplots, hullplots),
                                       interval=50, blit=True)
    line_ani.save('lines.mp4', writer=writer)

if __name__ == '__main__':

    for i, tar in enumerate(targets):
        vertexplots[i].set_data([tar[0]], [tar[1]])

    for i, hur in enumerate(hulls):
        hullplots[i].set_data(hur[:,0], hur[:,1])
    


    #saveVideo()
    ani = animation.FuncAnimation(fig, animate, interval=20, blit=False, fargs = (vertexplots, hullplots))
    

    plt.show()