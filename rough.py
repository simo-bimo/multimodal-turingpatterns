# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from model import Model


## Animate Settings
name = "optical/from_data_2"
source = "data/optical_1"
to_plot = "backward field"

data = Model.from_file(source)

x = next(data)
y = next(data)

fig, ax = plt.subplots()
fig.suptitle(f"Backward Field: 0")


quad = ax.pcolormesh(x, y, np.real(next(data)[to_plot][0]))
cb = plt.colorbar(quad)

def animate(i):
    fig.suptitle(f"Backward Field: {i}")

    quad.set_array(np.real(next(data)[to_plot][0]))
    return quad,

anim = FuncAnimation(fig, animate, frames=100)

anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
# plt.show()

"""
Timing Results
noblit: 0m26s
blit: 0m28s
"""