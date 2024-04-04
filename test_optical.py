from optical import Optical
import matplotlib.pyplot as plt

# import pdb
# pdb.set_trace()

model = Optical(dx=0.5, dy=0.5,  bottom_left=(-1,-1), top_right=(1,1), 
				dz=1, d=10,)

model.passover_fields()

model.plot_fields(plt, rng=range(0,model.num_z))

plt.show()
