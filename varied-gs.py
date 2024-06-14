from simulator.models import Model, GrayScott, VariedGS
import numpy as np
from scipy import ndimage

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.colorbar import Colorbar

# variedgs = VariedGS(dt=1.0, bottom_left=(-5,-5), top_right=(5,5))
# variedgs.set_activator(np.ones((variedgs.x_count, variedgs.y_count)))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, "data/variedgs-medium3", frames=2600, steps_per_frame=100)
# Model.create_animation("variedgs/medium2", "data/variedgs-medium3", "Inhibitor", frame_count=2600, frame_skip=100)

"""
First test from a source model.
"""
# variedgs = VariedGS(source="data/gs_large_scale2", dt=1.0, bottom_left=(-10,-10), top_right=(10,10))
# variedgs.set_activator(np.ones(variedgs.x.shape))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, "data/variedgs-nested", frames=2600, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation("variedgs/nested", "data/variedgs-nested", "Inhibitor", frame_count=2600, frame_skip=100)

"""
Second go with slightly different scales, making the smaller one even smaller so the pattern is clearer.
"""

# Model.to_file(gs, "data/gs_large_scale2", frames=1500, steps_per_frame=200)

# variedgs = VariedGS(source="data/gs_large_scale2", 
# 					activator_diffusion=0.5, 
# 					inhibitor_diffusion=0.25, 
# 					dt=1.0, 
# 					bottom_left=(-10,-10), 
# 					top_right=(10,10))

# variedgs.set_activator(np.ones(variedgs.x.shape))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, "data/variedgs-nested2", frames=2600, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation('variedgs/nested2', 'data/variedgs-nested2', 'Inhibitor', frame_count=2600, frame_skip=100)

"""
Third attempt, this time make the starting model even larger.
"""

# gs = GrayScott(diffusion_extra=40, 
# 			   dt=1.0, 
# 			   bottom_left=(-10,-10), 
# 			   top_right=(10,10))

# gs.set_activator(np.ones((gs.x_count, gs.y_count)))
# gs.add_inhibitor(r=0.4, amount=1.0)

# Model.to_file(gs, 'data/gs_large_scale3', frames=1500, steps_per_frame=200)

# variedgs = VariedGS(source='data/gs_large_scale3', 
# 					activator_diffusion=0.5, 
# 					inhibitor_diffusion=0.25, 
# 					dt=1.0, 
# 					bottom_left=(-10,-10), 
# 					top_right=(10,10))

# variedgs.set_activator(np.ones(variedgs.x.shape))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, 'data/variedgs-nested3', frames=1000, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation('variedgs/nested3_cut_mores', 'data/variedgs/variedgs-nested3', 'Inhibitor', frame_count=681, frame_skip=100)

"""
Plot an average value of the previous nested graph against the 
"""
# original_pattern, x, y = Model.get_last("data/gs/gs_large_scale3")
# nested_pattern, _, _ = Model.get_last("data/variedgs/variedgs-nested3")

# # Perform a Gaussian blur and then 
# # average over an area of n*n cells
# n = 10
# stencil = np.ones((n,n))/(n*n)
# recovered_pattern = nested_pattern['Inhibitor']
# # recovered_pattern = 1 - recovered_pattern
# recovered_pattern = ndimage.convolve(recovered_pattern, stencil, mode='wrap')
# recovered_pattern = ndimage.gaussian_filter(recovered_pattern, 5.5, mode='wrap')

# fig = plt.figure(figsize=(8,3))
# axs = ImageGrid(fig, 111,
# 			nrows_ncols=(1,3),
# 			axes_pad=0.2,
# 			share_all=True,
# 			cbar_location="right",
# 			cbar_mode="single",
# 			cbar_size="7%",
# 			cbar_pad=0.25,
# 			)

# fig.suptitle("Figure 1: Pre-Computed Double Gray-Scott")
# quad0=axs[0].pcolormesh(x,y,original_pattern['Inhibitor'])
# axs[0].set_title("a) Primary Pattern")
# quad1=axs[1].pcolormesh(x,y,nested_pattern['Inhibitor'])
# axs[1].set_title("b) Secondary Pattern")
# quad2=axs[2].pcolormesh(x,y,recovered_pattern)
# axs[2].set_title("c) Recovered Pattern")

# axs[0].cax.cla()
# cb = Colorbar(axs[0].cax, quad1)
# cb2 = Colorbar(axs[1].cax, quad1)

# [ax.set_box_aspect(1.0) for ax in axs]

# fig.savefig("plots/variedgs/nested_comparisons.png")

# '''
# Just a plot of the recovered pattern.
# '''
# original_pattern, x, y = Model.get_last("data/gs/gs_large_scale3")
# # Model.create_plot('variedgs/nested_pattern', 'data/variedgs/variedgs-nested3', ['Inhibitor'],)

'''
More plots
'''

original_pattern, x, y = Model.get_last("data/gs/gs_large_scale3")
nested_pattern, _, _ = Model.get_last("data/variedgs/variedgs-nested3")

# Perform a Gaussian blur and then 
# average over an area of n*n cells
n = 10
stencil = np.ones((n,n))/(n*n)
recovered_pattern = nested_pattern['Inhibitor']
# recovered_pattern = 1 - recovered_pattern
recovered_pattern = ndimage.convolve(recovered_pattern, stencil, mode='wrap')
recovered_pattern = ndimage.gaussian_filter(recovered_pattern, 5.5, mode='wrap')

fig = plt.figure(figsize=(8,3))
axs = ImageGrid(fig, 111,
			nrows_ncols=(1,3),
			axes_pad=0.2,
			share_all=True,
			cbar_location="right",
			cbar_mode="single",
			cbar_size="7%",
			cbar_pad=0.25,
			)

fig.suptitle("Figure 1: Pre-Computed Double Gray-Scott")
quad0=axs[0].pcolormesh(x,y,original_pattern['Inhibitor'])
axs[0].set_title("a) Primary Pattern")
quad1=axs[1].pcolormesh(x,y,nested_pattern['Inhibitor'])
axs[1].set_title("b) Secondary Pattern")
quad2=axs[2].pcolormesh(x,y,recovered_pattern)
axs[2].set_title("c) Recovered Pattern")

axs[0].cax.cla()
cb = Colorbar(axs[0].cax, quad1)
cb2 = Colorbar(axs[1].cax, quad1)

[ax.set_box_aspect(1.0) for ax in axs]

fig.savefig("plots/variedgs/nested_comparisons.png")

'''
Just a plot of the recovered pattern.
'''
original_pattern, x, y = Model.get_last("data/gs/gs_large_scale3")
# Model.create_plot('variedgs/nested_pattern', 'data/variedgs/variedgs-nested3', ['Inhibitor'],)