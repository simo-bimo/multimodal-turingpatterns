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

gs = GrayScott(bottom_left=(-2,-2), top_right=(2,2))
gs.set_activator(np.ones(gs.x.shape))
gs.add_inhibitor(r=0.4)

Model.to_file(gs, 'data/gs_normal')
Model.create_animation('grayscott/normal',
					   'data/gs_normal',
					   'Inhibitor')

'''
An attempt to generate a differently scaled model, to assert the effectiveness of the scale parameter
'''
# Hacky way to get default shape
# shape = GrayScott().x.shape
# mapgs = MappedGS({'Scale': lambda: 10*np.ones(shape)})
# mapgs.set_activator(np.ones(shape))
# mapgs.add_inhibitor(r=0.4)

# Model.to_file(mapgs, 'data/mapped_scale_large', frames=100, steps_per_frame=20)
# Model.create_animation('mappedgs/large_scale',
# 					   'data/mapped_scale_large',
# 					   'Inhibitor',
# 					   frame_count=100)