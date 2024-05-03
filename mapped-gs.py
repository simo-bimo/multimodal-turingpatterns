from simulator.models import *
import numpy as np

'''
Creating a regular TP to see what happens
'''
mapgs = MappedGS(bottom_left=(-2,-2), top_right=(2,2))
mapgs.set_activator(np.ones(mapgs.x.shape))
mapgs.add_inhibitor(r=0.4)

Model.to_file(mapgs, 'data/mapped_normal', frames=1000, steps_per_frame=20)
Model.create_animation('mappedgs/normal',
					   'data/mapped_normal',
					   'Inhibitor',
					   frame_count=1000)

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