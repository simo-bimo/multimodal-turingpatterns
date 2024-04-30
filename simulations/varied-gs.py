from model import Model
from grayscott import GrayScott
from variedgs import VariedGS
import numpy as np
gs = GrayScott(dt=1.0, bottom_left=(-10,-10), top_right=(10,10))
gs.set_activator(np.ones((gs.x_count, gs.y_count)))
gs.add_inhibitor(r=2.0, amount=1.0)
Model.to_file(gs, "data/gs_temp", frames=1, steps_per_frame=20000)

variedgs = VariedGS(source="data/gs_temp", dt=1.0, bottom_left=(-10,-10), top_right=(10,10))
variedgs.set_activator(np.ones((variedgs.x_count, variedgs.y_count)))
variedgs.add_inhibitor(r=0.2, amount=1.0)

Model.to_file(gs, "data/variedgs", frames=20000, steps_per_frame=1)