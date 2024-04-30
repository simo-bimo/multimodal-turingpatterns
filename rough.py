# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from model import Model

Model.create_animation("grayscott/mid_scale", "data/gs_simple_scaled", "Inhibitor")
Model.create_animation("grayscott/half_scale", "data/gs_simple_scaled_half", "Inhibitor")
Model.create_animation("grayscott/double_scale", "data/gs_simple_scaled_double", "Inhibitor")
