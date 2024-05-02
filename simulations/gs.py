from model import Model
from grayscott import GrayScott
import numpy as np

"""
Keeps a record of some of the simulations run,
and their parameters for later reference if needed.
"""

# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), )
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.2, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled", frames=1000, steps_per_frame=20)
# 
# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), activator_diffusion=0.5, inhibitor_diffusion=0.25)
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.2, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled_half", frames=1000, steps_per_frame=20)
# 
# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), activator_diffusion=2.0, inhibitor_diffusion=1.0)
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.4, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled_double", frames=1000, steps_per_frame=20)

# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2), activator_diffusion=3.0, inhibitor_diffusion=1.5)
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.2, amount=1.0)
# Model.to_file(gs, "data/gs_simple_scaled_triple", frames=1000, steps_per_frame=20)

'''
attempt to generate bigger scaling by just applying the laplacian multiple times
'''
# gs = GrayScott(dt=1.0, bottom_left=(-2,-2), top_right=(2,2))
# lapl = gs.laplace
# gs.laplace = lambda x: lapl(lapl(x))
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.4, amount=1.0)
# Model.to_file(gs, "data/gs_multi_laplace", frames=1000, steps_per_frame=20)

# Model.create_animation("grayscott/gs_multi_laplace", "data/gs_multi_laplace", "Inhibitor")
'''
Attempt to generate bigger scale/longer wavelength by shrinking feed / kill rates
Version two makes an edit so the reaction rate terms (AH**2) are scaled aswell.
'''
# gs = GrayScott(feed=0.055/2, decay=0.062/2, dt=2.0, bottom_left=(-2,-2), top_right=(2,2))
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.5, amount=1.0)
# Model.to_file(gs, "data/gs_shrink_other_params2", frames=1000, steps_per_frame=20)

# Model.create_animation("grayscott/gs_shrink_other_params2", "data/gs_shrink_other_params2", "Inhibitor")
'''
Attempt to generate bigger scale/longer wavelength by skipping over grayscott reaction for extra diffusion.
Required a change to the grayscott.py file.
The second sim doubled the feed and decay values aswell.
'''
gs = GrayScott(diffusion_extra=10, dt=1.0, bottom_left=(-10,-10), top_right=(10,10))
gs.set_activator(np.ones((gs.x_count, gs.y_count)))
gs.add_inhibitor(r=0.4, amount=1.0)
Model.to_file(gs, "data/gs_large_scale2", frames=1500, steps_per_frame=200)

Model.create_animation("grayscott/gs_large_scale2", "data/gs_large_scale2", "Inhibitor")

# '''
# Same as above but also with the feed kill parts ocurring during skipped steps. 
# i.e. only the AH^2 part is ignored every 2 steps.
# Requiree some changes to grayscott.py.
# '''
# gs = GrayScott(diffusion_extra=2, dt=1.0, bottom_left=(-2,-2), top_right=(2,2))
# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.4, amount=1.0)
# Model.to_file(gs, "data/gs_skip_react_extra_laplace_2", frames=1000, steps_per_frame=20)

# Model.create_animation("grayscott/gs_skip_react_extra_laplace_2", "data/gs_skip_react_extra_laplace_2", "Inhibitor")