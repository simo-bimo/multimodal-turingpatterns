from model import Model
import numpy as np
import matplotlib.pyplot as plt


class Optical(Model):
	def __init__(self, d=1.0, dz=0.04, chi=-0.9, R=0.9, l_d=1.0, tau=1.0, **kwargs):
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
		
		# initial condition is a gaussian from the laser
		# I'm just assuming that this is what it should look like. I don't know if the forwards field is
		# actually affected in this way.
		self.excitation_density += np.exp(-(self.x**2 + self.y**2))
		self.transverse_forward[0] += np.exp(-(self.x**2 + self.y**2))
		# self.excitation_density += np.exp(-(self.x**2 + self.y**2))
  
		self.values = {
			"forward field": (self.transverse_forward, self.del_transverse_forward),
			"backward field": (self.transverse_backward, self.del_transverse_backward),
			"excitation density": (self.excitation_density, self.del_excitation_density),
		}
		
		self.clip = False
		
		pass
	
	def passover_fields(self):
		for i in range(1, self.num_z):
			self.transverse_forward[i] += 1j * self.kerr_effect * self.excitation_density * self.transverse_forward[i-1] * self.dz
		
		self.transverse_backward[self.num_z-1] = self.reflectivity * self.transverse_forward[self.num_z-1]
		
		for i in range(self.num_z-1, 0, -1):
			self.transverse_backward[i] += -1j * self.kerr_effect * self.excitation_density * self.transverse_backward[i-1] * self.dz
		
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
		change = 1j * self.kerr_effect * \
			np.tile(self.excitation_density, (self.num_z, 1, 1)) * \
			np.roll(self.transverse_forward, 1, 0) * self.dz
		
		# don't change initial condition (assume laser is giving constant output:
		change[0] = np.zeros((self.x_count, self.y_count)) 
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
		