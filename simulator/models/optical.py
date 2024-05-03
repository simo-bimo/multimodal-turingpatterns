from .model import Model
import numpy as np
import matplotlib.pyplot as plt


class Optical(Model):
	def __init__(self, d=1.0, dz=0.04, chi=0.9, R=0.9, l_d=1.0, tau=1.0, k=1, **kwargs):
		"""
		Creates and Optical model based on Huang et McDonald (2005).
		"""
		super().__init__(**kwargs)
		self.cavity_distance = d
		self.dz = dz
		
		self.num_z = int(self.cavity_distance / self.dz)
		self.reflectivity = R
		self.kerr_effect = chi
		
		self.diffusion_distance = l_d
		self.relaxation_time = tau
		
		self.excitation_density = np.zeros((self.x_count, self.y_count))
		self.transverse_forward = np.zeros((self.num_z, self.x_count, self.y_count), dtype=np.cdouble)
		self.transverse_backward = np.zeros((self.num_z, self.x_count, self.y_count), dtype=np.cdouble)
		
		self.input_freq = k
		# the derivative of the laser oscillation.
		self.d_input_laser = lambda x: -2*np.pi*self.input_freq*np.sin(2*np.pi * x * self.input_freq)\
			* np.exp(-(self.x**2 + self.y**2))
		self.transverse_forward[0] += np.exp(-(self.x**2 + self.y**2))
  
		self.values = {
			"forward field": (self.transverse_forward, self.del_transverse_forward),
			"backward field": (self.transverse_backward, self.del_transverse_backward),
			"excitation density": (self.excitation_density, self.del_excitation_density),
		}
		pass

	
	def debug_take_step(self, num=1):
		# print max value. with each step we should see the value move through the list.
		for i in range (0, num):
			print(["{0:07.2f}".format(np.max(np.abs(x))) for x in self.transverse_forward])
			print(["{0:07.2f}".format(np.max(np.abs(x))) for x in self.transverse_backward])
			self.transverse_forward += self.del_transverse_forward()
			self.transverse_backward += self.del_transverse_backward()
		
		self.curr_step += 1
		pass
		
	def del_transverse_forward(self):
		"""
		Function that shifts the forwards field one step and bounces it back.
		"""
		change = 1j * self.kerr_effect * \
			np.tile(self.excitation_density, (self.num_z, 1, 1)) * \
			np.roll(self.transverse_forward, 1, 0) * self.dz
		
		# change initial condition based on laser
		change[0] = self.d_input_laser(self.curr_step) #- self.transverse_forward[0]
		return change
	
	def del_transverse_backward(self):
		change = -1j * self.kerr_effect * \
			np.tile(self.excitation_density, (self.num_z, 1, 1)) * \
			np.roll(self.transverse_backward, -1, 0) * self.dz
		# the last value is the forwards values reflected.
		change[self.num_z-1] = (self.reflectivity * self.transverse_forward[self.num_z-1]) - self.transverse_backward[self.num_z-1]
		return change
	
	def del_excitation_density(self):
		change = np.abs(self.transverse_forward[0])**2 + \
			np.abs(self.transverse_backward[0])**2 - \
			self.excitation_density
		change += self.diffusion_distance**2 * self.laplace(self.excitation_density)
		return change / self.relaxation_time
	
	def plot_fields(self, ax, rng=range(0,1)):
		"""
		Plots the forwards and backwards fields as quiver plots.
		"""
		modulus_forward = np.abs(self.transverse_forward)
		modulus_backward = np.abs(self.transverse_backward)
		for i in rng:
			ax[0].quiver(self.x, self.y, 
			 	self.transverse_forward[i].real, 
			 	self.transverse_forward[i].imag, 
				modulus_forward[i], # colour by length
				angles='xy',
				scale_units='xy',
				scale=np.max(modulus_forward[i])/self.dx,
				)
			ax[1].quiver(self.x, self.y, 
			 	self.transverse_backward[i].real, 
			 	self.transverse_backward[i].imag, 
				modulus_backward[i], # colour by length
				angles='xy',
				scale_units='xy',
				scale=np.max(modulus_backward[i])/self.dx,
				)
		pass
		