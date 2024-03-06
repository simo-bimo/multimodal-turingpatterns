# Imports
from signal import signal, SIGINT

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from meshwork import MeshworkSystem

system = MeshworkSystem()
x = system.x
y = system.y

system.add_differentiation()


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
name = "meshwork-init-params-allplot"

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
fig.suptitle(f"Meshwork Pattern: {system.curr_step}")
# quad = ax.pcolormesh(x, y, plotee, vmin=rng[0], vmax=rng[1])
# cb = plt.colorbar(quad)
quad1 = ax1.pcolormesh(x, y, system.activator, vmin=rng[0], vmax=rng[1])
quad2 = ax2.pcolormesh(x, y, system.inhibitor, vmin=rng[0], vmax=rng[1])
quad3 = ax3.pcolormesh(x, y, system.substrate, vmin=rng[0], vmax=rng[1])
quad4 = ax4.pcolormesh(x, y, system.differentiation, vmin=rng[0], vmax=rng[1])

ax1.set_title("Activator")
ax2.set_title("Inhibitor")
ax3.set_title("Substrate")
ax4.set_title("Differentiation")

plt.subplots_adjust(hspace=0.5)

interrupted = False
def early_fin(signal, frame):
    global interrupted
    interrupted = True
    pass
signal(SIGINT, early_fin)

def init():
    # quad.set_array(plotee.ravel())
    # return quad,
    quad1.set_array(system.activator.ravel())
    quad2.set_array(system.inhibitor.ravel())
    quad3.set_array(system.substrate.ravel())
    quad4.set_array(system.differentiation.ravel())
    return quad1,quad2,quad3,quad4

def animate(i):
    global interrupted
    if not interrupted:
        system.take_step(500)
        fig.suptitle(f"Meshwork Pattern: {system.curr_step}")

        # quad.set_array(plotee.ravel())
    # return quad,
        quad1.set_array(system.activator.ravel())
        quad2.set_array(system.inhibitor.ravel())
        quad3.set_array(system.substrate.ravel())
        quad4.set_array(system.differentiation.ravel())
    return quad1,quad2,quad3,quad4

anim = FuncAnimation(fig, animate, init_func=init, frames=300)

anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
# plt.show()

"""
Timing Results
noblit: 0m26s
blit: 0m28s
"""