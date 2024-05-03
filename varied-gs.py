from simulator.models import Model, GrayScott, VariedGS
import numpy as np
from scipy import ndimage

import matplotlib.pyplot as plt

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

# Model.to_file(variedgs, 'data/variedgs-nested3', frames=2600, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation('variedgs/nested3', 'data/variedgs-nested3', 'Inhibitor', frame_count=2600, frame_skip=100)

"""
Plot an average value of the previous nested graph against the 
"""
original_pattern, x, y = Model.get_last("data/gs_large_scale3")
nested_pattern, _, _ = Model.get_last("data/variedgs-nested3")

# Perform a Gaussian blur and then 
# average over an area of n*n cells
n = 15
stencil = np.ones((n,n))/(n*n)
recovered_pattern = nested_pattern['Inhibitor']
# recovered_pattern = ndimage.convolve(recovered_pattern, stencil, mode='wrap')
# recovered_pattern = ndimage.gaussian_filter(recovered_pattern, 5.5, mode='wrap')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

fig.suptitle("Original Pattern v Recovered Pattern")
ax[0].pcolormesh(x,y,original_pattern['Inhibitor'])
ax[0].set_title("Original Pattern")
ax[1].pcolormesh(x,y,recovered_pattern)
ax[1].set_title("Recovered Pattern")

plt.show()
fig.savefig("plots/original_v_recovered.png")