from ..models.model import Model
from ..models.grayscott import GrayScott

import unittest
import os

class OptimisationTests(unittest.TestCase):
	def setUp(self) -> None:
		self.file_1 = 'data/temp_1'
		self.file_2 = 'data/temp_2'
		return super().setUp()
	def test_opt_take_step(self):
		self.file_1 = 'data/temp_1'
		self.file_2 = 'data/temp_2'
		
		frames=100
		steps_per_frame=5
		
		gs1 = GrayScott()
		gs2 = GrayScott()
		
		Model.to_file(gs1, self.file_1, frames=frames, steps_per_frame=steps_per_frame)
		Model.to_file(gs2, self.file_2, frames=frames, steps_per_frame=steps_per_frame, optimised=True)
		
		diff_count = Model.compare_difference([self.file_1, self.file_2])
		print(f"Difference count is: {diff_count}")
		self.assertEqual(diff_count, 0)
		
		pass
	
	def tearDown(self) -> None:
		os.remove(self.file_1+'.dat')
		os.remove(self.file_2+'.dat')
		return super().tearDown()

if __name__ == '__main__':
	unittest.main()