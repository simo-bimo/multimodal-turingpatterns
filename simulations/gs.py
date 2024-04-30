from model import Model
from grayscott import GrayScott
import numpy as np
# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), )
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.2, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled", frames=1000, steps_per_frame=20)

# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), activator_diffusion=0.5, inhibitor_diffusion=0.25)
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.2, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled_half", frames=1000, steps_per_frame=20)

gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), activator_diffusion=1.0, inhibitor_diffusion=0.5)
lapl = gs.laplace
# just make the laplacian apply itself twice... see if it works.
gs.laplace = lambda x: lapl(lapl(x))
gs.set_activator(np.ones((gs.x_count, gs.y_count)))
gs.add_inhibitor(r=0.2, amount=1.0)
Model.to_file(gs, "data/gs_simple_scaled_double", frames=1000, steps_per_frame=20)