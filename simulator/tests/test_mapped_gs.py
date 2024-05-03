from simulator.models import *

import unittest
import os
import numpy as np

class MappedGSTests(unittest.TestCase):
	def setUp(self):
		self.file_1 = 'data/test_temp_1'
		self.file_2 = 'data/test_temp_2'
		self.frame_count=100
		self.frame_skip=10
		return
	
	def test_default(self):
		# The defaults should match, so we don't need to set anything fancy.
		gs = GrayScott()
		mapped_gs = MappedGS({})
		
		Model.to_file(gs, 
				self.file_1, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		Model.to_file(mapped_gs, 
				self.file_2, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		diff_count = Model.compare_difference([self.file_1, self.file_2])
		self.assertEqual(diff_count, 0)
		return
	
	def test_default_with_initial(self):
		gs = GrayScott()
		gs.set_activator(np.ones(gs.x.shape))
		gs.add_inhibitor(r=0.4, amount=1)
		mapped_gs = MappedGS({})
		mapped_gs.set_activator(np.ones(gs.x.shape))
		mapped_gs.add_inhibitor(r=0.4, amount=1)
		
		
		Model.to_file(gs, 
				self.file_1, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		Model.to_file(mapped_gs, 
				self.file_2, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		diff_count = Model.compare_difference([self.file_1, self.file_2])
		self.assertEqual(diff_count, 0)
		return
	
	def test_simple_param_change(self):
		gs = GrayScott(feed=0.044)
		mapped_gs = MappedGS({'Feed': lambda: 0.044*np.ones(gs.x.shape)})
		
		self.assertNotEqual(mapped_gs.mapping['Feed']().any(), 0.055*np.ones(gs.x.shape).any())
		
		Model.to_file(gs, 
				self.file_1, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		Model.to_file(mapped_gs, 
				self.file_2, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		diff_count = Model.compare_difference([self.file_1, self.file_2])
		self.assertEqual(diff_count, 0)
		return
	
	def test_simple_param_change_with_initial(self):
		gs = GrayScott(feed=0.044)
		gs.set_activator(np.ones(gs.x.shape))
		gs.add_inhibitor(r=0.4, amount=1)
		mapped_gs = MappedGS({'Feed': lambda: 0.044*np.ones(gs.x.shape)})
		mapped_gs.set_activator(np.ones(gs.x.shape))
		mapped_gs.add_inhibitor(r=0.4, amount=1)
		
		self.assertNotEqual(mapped_gs.mapping['Feed']().any(), 0.055*np.ones(gs.x.shape).any())
		
		Model.to_file(gs, 
				self.file_1, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		Model.to_file(mapped_gs, 
				self.file_2, 
				frames=self.frame_count, 
				steps_per_frame=self.frame_skip)
		
		diff_count = Model.compare_difference([self.file_1, self.file_2])
		self.assertEqual(diff_count, 0)
		return
	
	def tearDown(self) -> None:
		os.remove(self.file_1+'.dat')
		os.remove(self.file_2+'.dat')
		return super().tearDown()
	
if __name__ == '__main__':
	unittest.main()