from model import Model
import numpy as np
import matplotlib.pyplot as plt

class Optical(Model):
	def __init__(self, d=1.0, dz=0.04, chi=1, R=0.9, **kwargs):
		super().__init__(**kwargs)
		self.cavity_distance = d
		self.dz = dz
		
		self.num_z = int(self.cavity_distance / self.dz)
		self.reflectivity = R
		self.kerr_effect = chi
		
		self.excitation_density = np.zeros((self.x_count, self.y_count))
		self.transverse_forward = np.zeros((self.num_z, self.x_count, self.y_count), dtype=np.cdouble)
		self.transverse_backward = np.zeros((self.num_z, self.x_count, self.y_count), dtype=np.cdouble)
		
		# Add a gaussian as initial state.
		self.excitation_density += 100*np.exp(-(self.x**2 + self.y**2))
		self.transverse_forward += np.exp(-(self.x**2 + self.y**2))
		# self.excitation_density += np.exp(-(self.x**2 + self.y**2))
		
		pass
	
	def passover_fields(self):
		for i in range(1, self.num_z):
			self.transverse_forward[i] = 1j * self.kerr_effect * self.excitation_density * self.transverse_forward[i-1] * self.dz
		
		self.transverse_backward[self.num_z-1] = self.reflectivity * self.transverse_forward[self.num_z-1]
		
		for i in range(self.num_z-1, 0, -1):
			self.transverse_backward[i] = -1j * self.kerr_effect * self.excitation_density * self.transverse_backward[i-1] * self.dz
		
		pass
	
	def plot_fields(self, ax, rng=range(0,1)):
		for i in rng:
			ax.quiver(self.x, self.y, self.transverse_forward[i].real, self.transverse_forward[i].imag, 'red')
			ax.quiver(self.x, self.y, self.transverse_backward[i].real, self.transverse_backward[i].imag, 'blue')
		
		pass
		