import unittest

from ..models.model import Model

class ComparisonTests(unittest.TestCase):
	def setUp(self):
		self.file = 'data/gs_temp'
		self.file2 = 'data/variedgs-small'
		self.file3 = 'data/variedgs-small2'
		pass
	
	def test_two_equal(self):
		self.assertEqual(Model.compare_difference([self.file, self.file]), 0)
		
	def test_three_equal(self):
		self.assertEqual(Model.compare_difference([self.file, self.file, self.file]), 0)
		
	def test_two_unequal(self):
		self.assertNotEqual(Model.compare_difference([self.file2, self.file3]), 0)

if __name__ == '__main__':
	unittest.main()