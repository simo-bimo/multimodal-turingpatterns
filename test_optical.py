from optical import Optical
import matplotlib.pyplot as plt

# import pdb
# pdb.set_trace()

model = Optical(dx=0.5, dy=0.5, #  bottom_left=(-1,-1), top_right=(1,1), 
				dz=1.0, d=10, chi=-1)

# model.passover_fields()
# model.debug_take_step(num=20)

model.take_step(num=50)


fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(10,6))
model.plot_fields([ax1,ax2])

plt.show()
