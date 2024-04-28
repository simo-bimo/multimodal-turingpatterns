# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from model import Model


## Animate Settings
name = "optical/photon_from_oscillation_clipped"
source = "data/optical_1_clip"
to_plot = "excitation density"

data = Model.from_file(source)

x = next(data)
y = next(data)

fig, ax = plt.subplots()
fig.suptitle(f"{to_plot}: 0")


quad = ax.pcolormesh(x, y, np.real(next(data)[to_plot]))
cb = plt.colorbar(quad)

def animate(i):
    fig.suptitle(f"{to_plot}: {i}")

    quad.set_array(np.real(next(data)[to_plot]))
    return quad,

anim = FuncAnimation(fig, animate, frames=500)

anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
# plt.show()

"""
Timing Results
noblit: 0m26s
blit: 0m28s
"""