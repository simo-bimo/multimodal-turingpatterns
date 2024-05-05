from simulator.models import *
import numpy as np

'''
Creating a regular TP to see what happens
'''
# mapgs = MappedGS(bottom_left=(-2,-2), top_right=(2,2))
# mapgs.set_activator(np.ones(mapgs.x.shape))
# mapgs.add_inhibitor(r=0.4)

# Model.to_file(mapgs, 'data/mapped_normal')
# Model.create_animation('mappedgs/normal',
# 					   'data/mapped_normal',
# 					   'Inhibitor')

# gs = GrayScott(bottom_left=(-2,-2), top_right=(2,2))
# gs.set_activator(np.ones(gs.x.shape))
# gs.add_inhibitor(r=0.4)

# Model.to_file(gs, 'data/gs_normal')
# Model.create_animation('grayscott/normal',
# 					   'data/gs_normal',
# 					   'Inhibitor')

'''
An attempt to generate a differently scaled model, to assert the effectiveness of the scale parameter
'''
#Hacky way to get default shape
# x = GrayScott().x
# y = GrayScott().y

# # scale varies from 1 to 2 going from left to right.
# scale_func = lambda: 2*((x+5)/10) + np.ones(x.shape)

# mapgs = MappedGS({'Scale': scale_func})
# mapgs.set_activator(np.ones(x.shape))
# mapgs.add_inhibitor(r=0.4)

# Model.to_file(mapgs, 'data/mapped_scale_large', frames=1000, steps_per_frame=200)
# Model.create_animation('mappedgs/large_scale',
# 					   'data/mapped_scale_large',
# 					   'Inhibitor',
# 					   frame_count=1000)

# All the above models generated with dt=0.1 by accident, hence their slowness and frame count
# Updated default in Model.y to be 1.0, as it has been for past simulations.

'''
Generate two Mapped GS, where one defines the scale of the other, to get a variable scale.
'''

x = GrayScott(bottom_left=(-10,-10), top_right=(10,10)).x

# a GS with a fairly large scale by default.
large_scale = lambda: 20*np.ones(x.shape)
large_mapped_gs = MappedGS({'Scale': large_scale}, 
						   bottom_left=(-10,-10), top_right=(10,10))
large_mapped_gs.set_activator(np.ones(x.shape))
large_mapped_gs.add_inhibitor(r=0.5)

# a smaller one that varies it's scale between 0.001 and 0.02 based on the value of the larger one.
smaller_scale = lambda: VariedGS.interpolate(large_mapped_gs.inhibitor, 0.001, 0.02)

small_mapped_gs = MappedGS({'Scale': smaller_scale}, 
						   update_func=large_mapped_gs.take_step,
						   bottom_left=(-10,-10), top_right=(10,10))

small_mapped_gs.set_activator(np.ones(x.shape))
small_mapped_gs.add_inhibitor(r=0.5)


Model.to_file(small_mapped_gs, 'data/mappedgs/parallel_scale')
Model.create_animation('mappedgs/parallel_scale', 
					   'data/mappedgs/parallel_scale',
					   'Inhibitor',
					   frame_count=1000)