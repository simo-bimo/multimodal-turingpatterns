# Imports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from meshwork import MeshworkSystem

system = MeshworkSystem()
x = system.x
y = system.y



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
plotee = system.differentiation
rng = (-40, 40)

fig,ax = plt.subplots()
plt.title(f"Meshwork Pattern: {system.curr_step}")
quad = ax.pcolormesh(x, y, plotee, vmin=rng[0], vmax=rng[1])
cb = plt.colorbar(quad)


def init():
    quad.set_array(plotee.ravel())
    return quad,


def animate(i):
    system.take_step(1)
    plt.title(f"Meshwork Pattern: {system.curr_step}")

    # quad = ax.pcolormesh(x, y, plotee, vmin=rng[0], vmax=rng[1])
    # cb = plt.colorbar(quad)
    quad.set_array(plotee.ravel())
    return quad,

anim = FuncAnimation(fig, animate, init_func=init, frames=300)

anim.save('test1-set-array-init.gif', writer='pillow')
# plt.show()

"""
Timing Results
test1.gif: 1m50s
test1-set-array: 0m7.8s
test1-set-array-init: 0m7.7s
"""