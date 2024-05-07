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
# n=1
# x = GrayScott(bottom_left=(-n,-n), top_right=(n,n)).x

# # a GS with a fairly large scale by default.
# large_scale = lambda: 20*np.ones(x.shape)
# large_mapped_gs = MappedGS({'Scale': large_scale}, 
# 						   bottom_left=(-n,-n), top_right=(n,n))

# # a smaller one that varies it's scale between 0.1 and 0.5 based on the value of the larger one.
# def small_scale():
# 	return MappedGS.interpolate(large_mapped_gs.inhibitor, 0.1, 0.5)

# small_mapped_gs = MappedGS({'Scale': small_scale}, 
# 						   update_func=large_mapped_gs.take_step,
# 						   bottom_left=(-n,-n), top_right=(n,n))

# Model.to_file(small_mapped_gs, 'data/mappedgs/parallel_scale')
# Model.create_animation('mappedgs/parallel_scale', 
# 					   'data/mappedgs/parallel_scale',
# 					   'Inhibitor',
# 					   frame_count=1000)

'''
Generate two mapped gs, where the larger one is a regular gray scott, and the smaller
interprets it's phase from the larger.
Same as previous variedgs but both evolve at the same time.
'''

n=10
x = GrayScott(bottom_left=(-n,-n), top_right=(n,n)).x
large_scale = lambda: 20*np.ones(x.shape)
large_mapped_gs = MappedGS({'Scale': large_scale}, 
						   bottom_left=(-n,-n), top_right=(n,n))

def small_kill():
	return MappedGS.interpolate(large_mapped_gs.inhibitor, 0.06229, 0.06033)

def small_feed():
	return MappedGS.interpolate(large_mapped_gs.inhibitor, 0.03657, 0.02696)

small_mapped_gs = MappedGS({'Kill': small_kill, 
							  'Feed': small_feed}, 
							 update_func=large_mapped_gs.take_step,
							 bottom_left=(-n,-n), top_right=(n,n))

Model.to_file(small_mapped_gs, 'data/mappedgs/parallel_phase_fast',
			  frames=500, steps_per_frame=1000)
Model.create_animation('mappedgs/parallel_phase_fast', 
					   'data/mappedgs/parallel_phase_fast',
					   'Inhibitor',
					   frame_count=500,
					   steps_per_frame=1000)