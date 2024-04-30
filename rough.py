# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from model import Model

def create_animation(name, source, to_plot, frame_skip=20):
    print(f"Beginning animation '{name}' from '{source}.dat'")
    data = Model.from_file(source)
    x = next(data)
    y = next(data)

    fig, ax = plt.subplots()
    fig.suptitle(f"{to_plot}: 0")


    quad = ax.pcolormesh(x, y, next(data)[to_plot])
    cb = plt.colorbar(quad)

    def animate(i):
        fig.suptitle(f"{to_plot}: {i*frame_skip}")
        quad.set_array(next(data)[to_plot])
        return quad,

    anim = FuncAnimation(fig, animate, frames=1000)

    anim.save('animations/'+name+'.gif', writer='pillow', fps=30)
    print("Saved animation: " + name)
    pass
    

create_animation("grayscott/mid_scale", "data/gs_simple_scaled", "Inhibitor")
create_animation("grayscott/half_scale", "data/gs_simple_scaled_half", "Inhibitor")
create_animation("grayscott/double_scale", "data/gs_simple_scaled_double", "Inhibitor")
