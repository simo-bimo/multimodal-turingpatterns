# Imports
from signal import signal, SIGINT

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from meshwork import MeshworkSystem
from grayscott import GrayScott

system = GrayScott()
system.activator = np.ones((system.x_count, system.y_count)) * 1.0
# system.activator = np.random.rand(system.x_count, system.y_count) * 0.5
# system.inhibitor = np.random.rand(system.x_count, system.y_count) * 0.5
# system.add_activator(r=0.5, amount=1.0)
system.add_inhibitor(r=0.2, amount=1.0)
x = system.x
y = system.y

## Animate Settings
plotee = system.activator
rng = (0, 1)
name = "grayscott/karlsims, rand both"

# fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(20,12))
fig, ax = plt.subplots()
fig.suptitle(f"Gray Scott Model: {system.curr_step}")
quad = ax.pcolormesh(x, y, plotee, vmin=rng[0], vmax=rng[1])
cb = plt.colorbar(quad)
# quad1 = ax1.pcolormesh(x, y, system.activator, vmin=rng[0], vmax=rng[1])
# quad2 = ax2.pcolormesh(x, y, system.inhibitor, vmin=rng[0], vmax=5)
# quad3 = ax3.pcolormesh(x, y, system.substrate, vmin=rng[0], vmax=5)
# quad4 = ax4.pcolormesh(x, y, system.differentiation, vmin=rng[0], vmax=5)
# cb1 = plt.colorbar(quad1, ax=ax1)
# cb2 = plt.colorbar(quad2, ax=ax2)
# cb3 = plt.colorbar(quad3, ax=ax3)
# cb4 = plt.colorbar(quad4, ax=ax4)

# ax1.set_title("Activator")
# ax2.set_title("Inhibitor")
# ax3.set_title("Substrate")
# ax4.set_title("Differentiation")

# plt.subplots_adjust(hspace=0.5)

interrupted = False
# def early_fin(signal, frame):
#     global interrupted
#     interrupted = True
#     pass
# signal(SIGINT, early_fin)

def init():
    quad.set_array(plotee.ravel())
    return quad,
    # quad1.set_array(system.activator.ravel())
    # quad2.set_array(system.inhibitor.ravel())
    # quad3.set_array(system.substrate.ravel())
    # quad4.set_array(system.differentiation.ravel())
    # return quad1,quad2,quad3,quad4

def animate(i):
    global interrupted
    if not interrupted:
        system.take_step(20)
        fig.suptitle(f"Meshwork Pattern: {system.curr_step}")

        quad.set_array(plotee.ravel())
    return quad,
    #     quad1.set_array(system.activator.ravel())
    #     quad2.set_array(system.inhibitor.ravel())
    #     quad3.set_array(system.substrate.ravel())
    #     quad4.set_array(system.differentiation.ravel())
    # return quad1,quad2,quad3,quad4

anim = FuncAnimation(fig, animate, init_func=init, frames=1000)

anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
# plt.show()

"""
Timing Results
noblit: 0m26s
blit: 0m28s
"""