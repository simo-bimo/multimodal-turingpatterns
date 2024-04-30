from model import Model
from grayscott import GrayScott
from variedgs import VariedGS
import numpy as np
variedgs = VariedGS(dt=1.0, bottom_left=(-5,-5), top_right=(5,5))
variedgs.set_activator(np.ones((variedgs.x_count, variedgs.y_count)))
variedgs.add_inhibitor(r=0.5, amount=1.0)

Model.to_file(variedgs, "data/variedgs-medium3", frames=2600, steps_per_frame=100)
Model.create_animation("variedgs/medium2", "data/variedgs-medium3", "Inhibitor", frame_count=2600, frame_skip=100)