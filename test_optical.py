from optical import Optical
import matplotlib.pyplot as plt

# import pdb
# pdb.set_trace()

model = Optical(dx=0.5, dy=0.5,  bottom_left=(-1,-1), top_right=(1,1), 
				dz=1.0, d=10, chi=-1)

# model.passover_fields()
model.take_step(num=20)


# fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(10,6))
# for i in range(model.num_z, 1, -1):
	# model.plot_fields([ax1,ax2], rng=range(i-1,i))

plt.show()
