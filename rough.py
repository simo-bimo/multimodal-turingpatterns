# Imports
from signal import signal, SIGINT

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from meshwork import MeshworkSystem

system = MeshworkSystem()
x = system.x
y = system.y

system.add_differentiation(p=(0,15), r=1)


## PLOTTING
# plt.pcolor(x, y, plotee)
# plt.savefig('1.png')

# system.take_step(10)
# plt.pcolor(x, y, plotee)
# plt.savefig('10.png')

# system.take_step(90)
# plt.pcolor(x, y, plotee)
# plt.savefig('100.png')

# system.take_step(100)
# plt.pcolor(x, y, plotee)
# plt.savefig('200.png')


## Animate
plotee = system.activator
rng = (0, 1)
name = "meshwork-random-AHD"

fig,ax = plt.subplots()
plt.title(f"Meshwork Pattern: {system.curr_step}")
quad = ax.pcolormesh(x, y, plotee, vmin=rng[0], vmax=rng[1])
cb = plt.colorbar(quad)

interrupted = False
def early_fin(signal, frame):
    global interrupted
    interrupted = True
    pass
signal(SIGINT, early_fin)

def init():
    quad.set_array(plotee.ravel())
    return quad,

def animate(i):
    global interrupted
    if not interrupted:
        system.take_step(50)
        plt.title(f"Meshwork Pattern: {system.curr_step}")

        quad.set_array(plotee.ravel())
    return quad,

anim = FuncAnimation(fig, animate, init_func=init, frames=300)

anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
# plt.show()

"""
Timing Results
noblit: 0m26s
blit: 0m28s
"""