from model import Model
from grayscott import GrayScott
from variedgs import VariedGS
import numpy as np
# variedgs = VariedGS(dt=1.0, bottom_left=(-5,-5), top_right=(5,5))
# variedgs.set_activator(np.ones((variedgs.x_count, variedgs.y_count)))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, "data/variedgs-medium3", frames=2600, steps_per_frame=100)
# Model.create_animation("variedgs/medium2", "data/variedgs-medium3", "Inhibitor", frame_count=2600, frame_skip=100)

"""
First test from a source model.
"""
# variedgs = VariedGS(source="data/gs_large_scale2", dt=1.0, bottom_left=(-10,-10), top_right=(10,10))
# variedgs.set_activator(np.ones(variedgs.x.shape))
# variedgs.add_inhibitor(r=0.5, amount=1.0)

# Model.to_file(variedgs, "data/variedgs-nested", frames=2600, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation("variedgs/nested", "data/variedgs-nested", "Inhibitor", frame_count=2600, frame_skip=100)

"""
Second go with slightly different scales, making the smaller one even smaller so the pattern is clearer.
"""
variedgs = VariedGS(source="data/gs_large_scale2", 
					left=(0.06332, 0.04188),
					right=(0.05784, 0.01876),
					activator_diffusion=0.5, 
					inhibitor_diffusion=0.25, 
					dt=1.0, 
					bottom_left=(-10,-10), 
					top_right=(10,10))

variedgs.set_activator(np.ones(variedgs.x.shape))
variedgs.add_inhibitor(r=0.5, amount=1.0)

Model.to_file(variedgs, "data/variedgs-nested2", frames=2600, steps_per_frame=100)

# Ran this line in parallel to above.
# Model.create_animation("variedgs/nested2", "data/variedgs-nested2", "Inhibitor", frame_count=2600, frame_skip=100)