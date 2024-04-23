from optical import Optical
from model import Model

model = Optical(dx=0.05, dy=0.05, #  bottom_left=(-1,-1), top_right=(1,1), 
				dz=1.0, d=10, chi=-1, k = 0.5)
model.clip = False

Model.to_archive(model, "data/optical_1", frames=500, steps_per_frame=10)

# data = Model.from_file("data/optical_1.dat")
# print(data[0])

# fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(10,6))
# fig.suptitle(f"Optical Model: {model.curr_step}")
# ax1.pcolormesh(model.x, model.y, model.transverse_forward[0].real)
# ax2.pcolormesh(model.x, model.y, model.transverse_backward[0].real)

# plt.show()
